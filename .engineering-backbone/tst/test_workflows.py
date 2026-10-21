"""Execute the actual reusable-workflow shell payloads against real Git consumers."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from copier import run_copy, run_update
import yaml

from src.maintenance.compile_toolchain_fingerprint import bundle_digest, rendered_digest
from tst.test_source_layout_compatibility import frozen_files


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = yaml.safe_load((ROOT / '.github/workflows/governance-checks.yml').read_text())
STEPS = {step['name']: step for step in WORKFLOW['jobs']['validate']['steps']}
PREVIOUS_TREES = {
    'bootstrap': 'da5e4b16db198a583ca252f109d33778de0a3f78',
    'pre-attestation': 'd28d6972fa999e785af13b315ce4daf570c73aea',
    'attested-review': '2727bd2a2c0f7a10bca749165f29a9a50021343b',
}
HISTORICAL_FIXTURES = ROOT / '.engineering-backbone/tst/fixtures/historical'
PREDECESSOR_COMMIT = 'bf8e901ecd066e8e6d1b05f0c56a66081a473c0a'
PREDECESSOR_TREE = '7e4bc46ec7d4ca4805bcd9f03d49c05d662ebd31'
PREDECESSOR_DIGEST = 'dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615'
PREDECESSOR_FIXTURE = ROOT / '.engineering-backbone/tst/fixtures/opencode-predecessor'
LAYOUT_PREDECESSOR_COMMIT = '212608aa50ee517b3dd3107a9480da997222fd4f'
LAYOUT_PREDECESSOR_TREE = 'c31ee9b6e418325936b59e31cd7e9b9865ed0064'
LAYOUT_PREDECESSOR_DIGEST = '35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b'
LAYOUT_PREDECESSOR_ARCHIVE = 'a67c6db7f5e418a414b09f3433548990c60964bd613c577b3e8abfe49a377ea0'
LAYOUT_PREDECESSOR_FIXTURE = ROOT / '.engineering-backbone/tst/fixtures/layout-predecessor'
MERGED_MAIN_DIGEST = 'a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524'
# Actual merged planning baseline 4394763d03c1d1302b6b37cef142d0f98f848be4.
PLANNING_PREDECESSOR_DIGEST = '94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120'


def predecessor_consumer(destination, *, fixture=PREDECESSOR_FIXTURE,
                         commit=PREDECESSOR_COMMIT, tree=PREDECESSOR_TREE,
                         digest=PREDECESSOR_DIGEST, archive_digest=None):
    """Restore verified rendered data without history, network or source execution."""
    manifest = json.loads((fixture / 'manifest.json').read_text())
    if (manifest['format'] != 'engineering-backbone-rendered-predecessor-v1'
            or manifest['source_commit'] != commit
            or manifest['source_tree'] != tree
            or manifest['rendered_toolchain_sha256'] != digest):
        raise ValueError('Immediate predecessor fixture provenance mismatch')
    if archive_digest is not None and manifest['archive_sha256'] != archive_digest:
        raise ValueError('Reviewed predecessor archive identity mismatch')
    archive = fixture / 'consumer.zip'
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['archive_sha256']:
        raise ValueError('Immediate predecessor archive differs from reviewed bytes')
    with zipfile.ZipFile(archive) as bundle:
        entries = bundle.infolist()
        names = [item.filename for item in entries]
        if (len(names) != len(set(names)) or set(names) != set(manifest['files'])
                or len(names) > 64 or sum(item.file_size for item in entries) > 1048576):
            raise ValueError('Immediate predecessor fixture has unexpected input paths or size')
        for item in entries:
            name = item.filename
            if (name.startswith('/') or '\\' in name or ':' in name
                    or any(part in ('', '.', '..') for part in name.split('/'))
                    or item.external_attr >> 16 & 0o170000 != 0o100000
                    or item.file_size > 524288):
                raise ValueError('Immediate predecessor fixture contains a nonregular path')
            content = bundle.read(item)
            if hashlib.sha256(content).hexdigest() != manifest['files'][name]:
                raise ValueError('Immediate predecessor rendered file differs: ' + name)
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if bundle_digest(destination) != digest:
        raise ValueError('Immediate predecessor fixture does not reproduce the exact toolchain')



def historical_source(destination, version):
    """Reconstruct immutable Copier inputs without requiring Git history objects."""
    manifest = json.loads((HISTORICAL_FIXTURES / 'manifest.json').read_text())
    if manifest['format'] != 'engineering-backbone-historical-source-v1':
        raise ValueError('Unknown historical fixture format')
    record = manifest['versions'][version]
    if record['source_tree'] != PREVIOUS_TREES[version]:
        raise ValueError('Historical fixture tree provenance mismatch')
    baseline = manifest['baseline']
    shutil.copytree(HISTORICAL_FIXTURES / baseline, destination, symlinks=True)
    if version != baseline:
        shutil.copytree(HISTORICAL_FIXTURES / version, destination, dirs_exist_ok=True, symlinks=True)
    paths = {path.relative_to(destination).as_posix(): path for path in destination.rglob('*') if path.is_file()}
    if set(paths) != set(record['files']):
        raise ValueError('Historical fixture input paths do not match the original source')
    for name, path in paths.items():
        content = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        if path.is_symlink() or digest != record['files'][name]:
            raise ValueError('Historical fixture differs from original Git blob: ' + name)
    return record


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def initialize(root):
    git(root, '-c', 'init.defaultBranch=main', 'init')
    git(root, 'config', 'user.email', 'workflow-tests@example.invalid')
    git(root, 'config', 'user.name', 'Workflow fixture')


def commit(root, message):
    git(root, 'add', '.')
    git(root, 'commit', '-m', message)
    return git(root, 'rev-parse', 'HEAD')


def run_shell_payload(workspace, content, *, env):
    """Match Actions' script-file execution without OS command-argument limits."""
    script = workspace / 'workflow-step.sh'
    script.write_bytes(content.encode('utf-8'))
    return subprocess.run(['bash', str(script)], cwd=workspace,
                          env=env, capture_output=True, text=True)


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='backbone-workflow-source-')
        cls.addClassCleanup(cls.fixture.cleanup)
        cls.source = Path(cls.fixture.name) / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns('.git', '__pycache__', 'artifacts', '.venv'))
        initialize(cls.source)
        commit(cls.source, 'Reviewed template fixture')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-workflow-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.candidate = self.workspace / 'candidate'
        run_copy(str(self.source), self.candidate, defaults=True, quiet=True, skip_tasks=True, vcs_ref='HEAD')
        self.trusted = self.workspace / 'trusted-base'
        shutil.copytree(self.candidate, self.trusted)

    def shell(self, step, **overrides):
        env = os.environ.copy()
        env.update({
            'GITHUB_WORKSPACE': str(self.workspace),
            'GITHUB_REPOSITORY': 'example/consumer',
            'EVENT_NAME': 'pull_request',
            'SOURCE_MODE': 'false',
            'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH'],
        })
        env.update({key: value for key, value in STEPS[step].get('env', {}).items()
                    if '${{' not in str(value)})
        env.update(overrides)
        return run_shell_payload(self.workspace, STEPS[step]['run'], env=env)

    def validate(self, **env):
        return self.shell('Validate generated consumer with trusted tooling', **env)

    def mutate(self, path, fn, root=None):
        file = (root or self.candidate) / path
        data = json.loads(file.read_text())
        fn(data)
        file.write_text(json.dumps(data) + '\n')

    def test_valid_consumer_uses_prior_bundle(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('no trusted base supplied', result.stdout)

    def test_candidate_noop_validator_and_empty_lock_cannot_bypass_policy(self):
        marker = self.workspace / 'candidate-validator-executed'
        (self.candidate / '.engineering-backbone/validate.py').write_text(
            f'from pathlib import Path\nPath({str(marker)!r}).touch()\nprint("forged PASS")\n')
        (self.candidate / '.engineering-backbone/requirements.lock').write_text('# empty malicious lock\n')
        self.mutate('.engineering-backbone/core.json', lambda d: d['invariants'].update(human_merge_required=False))
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Candidate toolchain fingerprint', result.stdout + result.stderr)
        self.assertFalse(marker.exists())
        self.assertNotIn('forged PASS', result.stdout)

    def test_trusted_extra_invariant_cannot_be_removed(self):
        self.mutate('.engineering-backbone/core.json', lambda d: d['invariants'].update(security_review_required=True), self.trusted)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('trusted-base invariant security_review_required', result.stdout + result.stderr)

    def test_candidate_import_paths_and_schema_cannot_replace_trusted_tooling(self):
        (self.candidate / 'yaml.py').write_text('raise RuntimeError("candidate import executed")\n')
        (self.candidate / 'jsonschema.py').write_text('raise RuntimeError("candidate import executed")\n')
        (self.candidate / '.engineering-backbone/schemas/core-policy.schema.json').write_text('{}\n')
        self.mutate('.engineering-backbone/core.json', lambda d: d.update(version='invalid'))
        result = self.validate(PYTHONPATH=str(self.candidate))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Candidate toolchain fingerprint', result.stdout + result.stderr)
        self.assertNotIn('candidate import executed', result.stdout + result.stderr)

    def test_absent_or_partial_base_fails_before_python_execution(self):
        python_marker = self.workspace / 'python-executed'
        fake_bin = self.workspace / 'fake-bin'
        fake_bin.mkdir()
        fake_python = fake_bin / 'python'
        fake_python.write_text(f'#!/bin/bash\ntouch "{python_marker}"\nexit 0\n')
        fake_python.chmod(0o755)
        original_path = os.environ['PATH']
        for missing in ('validate.py', 'requirements.lock', 'schemas/project.schema.json'):
            with self.subTest(missing=missing):
                file = self.trusted / '.engineering-backbone' / missing
                original = file.read_bytes()
                file.unlink()
                for event in ('pull_request', 'workflow_dispatch'):
                    result = self.validate(EVENT_NAME=event, PATH=str(fake_bin) + os.pathsep + original_path)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('No complete trusted consumer baseline', result.stdout)
                    self.assertFalse(python_marker.exists())
                file.write_bytes(original)
        shutil.rmtree(self.trusted)
        for event in ('pull_request', 'workflow_dispatch'):
            result = self.validate(EVENT_NAME=event, PATH=str(fake_bin) + os.pathsep + original_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('workflow inactive', result.stdout)
            self.assertFalse(python_marker.exists())

    def test_source_mode_cannot_bypass_consumer_gate(self):
        step = 'Check workflow mode and event'
        self.assertNotEqual(self.shell(step, SOURCE_MODE='true').returncode, 0)
        self.assertEqual(self.shell(step, SOURCE_MODE='true', GITHUB_REPOSITORY='Artifaktory/engineering-backbone').returncode, 0)
        self.assertEqual(self.shell(step).returncode, 0)
        self.assertNotEqual(self.shell(step, EVENT_NAME='pull_request_target').returncode, 0)

    def test_checkout_uses_explicit_revisions_and_no_credentials(self):
        head = STEPS['Checkout candidate snapshot']['with']
        base = STEPS['Checkout trusted consumer snapshot']['with']
        self.assertEqual(head['ref'], '${{ github.event.pull_request.head.sha || github.sha }}')
        self.assertEqual(head['fetch-depth'], 0)
        self.assertEqual(base['ref'], '${{ github.event.pull_request.base.sha || github.event.before }}')
        self.assertFalse(head['persist-credentials'])
        self.assertFalse(base['persist-credentials'])
        self.assertNotIn("workflow_dispatch", STEPS['Checkout trusted consumer snapshot']['if'])
        dispatch = STEPS['Checkout trusted consumer default branch']
        self.assertEqual(dispatch['if'], "${{ !inputs.source_mode && github.event_name == 'workflow_dispatch' }}")
        self.assertEqual(dispatch['with']['ref'], 'refs/heads/${{ github.event.repository.default_branch }}')
        self.assertFalse(dispatch['with']['persist-credentials'])

    def dispatch_snapshots(self, *, malicious):
        # The workflow's actual ref mapping selects default-branch tooling even
        # when dispatch selects a different feature commit as the candidate.
        repository = self.workspace / 'dispatch-repository'
        shutil.copytree(self.trusted, repository)
        initialize(repository)
        default_name = 'reviewed-default'
        git(repository, 'branch', '-m', default_name)
        reviewed = commit(repository, 'Reviewed default-branch bundle')
        git(repository, 'checkout', '-b', 'unapproved-feature')
        marker = self.workspace / 'dispatch-candidate-executed'
        if malicious:
            (repository / '.engineering-backbone/validate.py').write_text(
                f'from pathlib import Path\nPath({str(marker)!r}).touch()\nprint("forged dispatch PASS")\n')
            (repository / '.engineering-backbone/requirements.lock').write_text('# empty candidate lock\n')
            self.mutate('.engineering-backbone/core.json',
                        lambda d: d['invariants'].update(human_merge_required=False), repository)
        else:
            self.mutate('.engineering-backbone/core.json', lambda d: d.update(version='0.1.1'), repository)
        selected = commit(repository, 'Selected dispatch candidate')
        candidate_ref = STEPS['Checkout candidate snapshot']['with']['ref']
        self.assertEqual(candidate_ref, '${{ github.event.pull_request.head.sha || github.sha }}')
        dispatch_ref = STEPS['Checkout trusted consumer default branch']['with']['ref']
        trusted_ref = dispatch_ref.replace('${{ github.event.repository.default_branch }}', default_name)
        self.assertEqual(git(repository, 'rev-parse', trusted_ref), reviewed)
        self.assertNotEqual(reviewed, selected)
        shutil.rmtree(self.candidate)
        shutil.rmtree(self.trusted)
        git(repository, 'checkout', '--detach', selected)
        shutil.copytree(repository, self.candidate, ignore=shutil.ignore_patterns('.git'))
        git(repository, 'checkout', '--detach', trusted_ref)
        shutil.copytree(repository, self.trusted, ignore=shutil.ignore_patterns('.git'))
        return marker

    def test_dispatch_selected_feature_cannot_supply_trusted_tooling(self):
        marker = self.dispatch_snapshots(malicious=True)
        result = self.validate(EVENT_NAME='workflow_dispatch')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Candidate toolchain fingerprint', result.stdout + result.stderr)
        self.assertFalse(marker.exists())
        self.assertNotIn('forged dispatch PASS', result.stdout)

    def test_dispatch_valid_selected_feature_uses_default_branch_tooling(self):
        marker = self.dispatch_snapshots(malicious=False)
        result = self.validate(EVENT_NAME='workflow_dispatch')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists())

    def legacy_source(self, version):
        source = self.workspace / ('legacy-source-' + version)
        if not source.exists():
            historical_source(source, version)
        return source

    def use_legacy_base(self, version='pre-attestation', **data):
        shutil.rmtree(self.trusted)
        run_copy(str(self.legacy_source(version)), self.trusted, data=data,
                 defaults=True, quiet=True, skip_tasks=True)
        shutil.rmtree(self.candidate)
        shutil.copytree(self.trusted, self.candidate)

    def use_immediate_predecessor(self):
        shutil.rmtree(self.trusted)
        predecessor_consumer(self.trusted)
        shutil.rmtree(self.candidate)
        shutil.copytree(self.trusted, self.candidate)

    def test_immediate_predecessor_unchanged_and_coherent_current_tooling_pass(self):
        modern = self.workspace / 'current-consumer'
        shutil.copytree(self.candidate, modern)  # Actual current Copier rendering.
        self.use_immediate_predecessor()
        self.assertEqual(bundle_digest(self.trusted), PREDECESSOR_DIGEST)
        self.assertEqual(bundle_digest(self.candidate), PREDECESSOR_DIGEST)
        unchanged = self.validate()
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)
        shutil.rmtree(self.candidate)
        shutil.copytree(modern, self.candidate)
        current = STEPS['Validate generated consumer with trusted tooling']['env']['CURRENT_TOOLCHAIN_SHA256']
        self.assertEqual(bundle_digest(self.candidate), current)
        upgraded = self.validate()
        self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)

    def test_exact_main_legacy_refresh_preserves_facts_and_rejects_policy_weakening(self):
        # Fixed rendered main input works even in a single-commit source clone.
        # This is a real overwrite-copy refresh; historical tests separately
        # exercise Copier run_update and its old-source reconstruction protocol.
        shutil.rmtree(self.trusted)
        predecessor_consumer(self.trusted, fixture=LAYOUT_PREDECESSOR_FIXTURE,
                             commit=LAYOUT_PREDECESSOR_COMMIT, tree=LAYOUT_PREDECESSOR_TREE,
                             digest=LAYOUT_PREDECESSOR_DIGEST,
                             archive_digest=LAYOUT_PREDECESSOR_ARCHIVE)
        self.mutate('.engineering-backbone/project.json',
                    lambda data: data['project'].update(name='local-main-project',
                                                       base_branch='reviewed/base'), self.trusted)
        self.mutate('.engineering-backbone/core.json',
                    lambda data: data['invariants'].update(local_security_review_required=True), self.trusted)
        (self.trusted / 'AGENTS.md').write_text('Reviewed local instructions remain binding.\n')
        shutil.rmtree(self.candidate)
        shutil.copytree(self.trusted, self.candidate)
        unchanged = self.validate()
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)
        facts = (self.candidate / '.engineering-backbone/project.json').read_bytes()
        run_copy(str(self.source), self.candidate, defaults=True, quiet=True,
                 skip_tasks=True, overwrite=True, vcs_ref='HEAD')
        self.assertEqual((self.candidate / '.engineering-backbone/project.json').read_bytes(), facts)
        self.assertEqual((self.candidate / 'AGENTS.md').read_text(),
                         'Reviewed local instructions remain binding.\n')
        self.assertEqual(bundle_digest(self.candidate),
                         STEPS['Validate generated consumer with trusted tooling']['env']['CURRENT_TOOLCHAIN_SHA256'])
        # Copier policy integration cannot silently discard the stricter base.
        rejected = self.validate()
        self.assertNotEqual(rejected.returncode, 0, rejected.stdout + rejected.stderr)
        self.assertIn('local_security_review_required', rejected.stdout + rejected.stderr)
        self.mutate('.engineering-backbone/core.json',
                    lambda data: data['invariants'].update(local_security_review_required=True))
        refreshed = self.validate()
        self.assertEqual(refreshed.returncode, 0, refreshed.stdout + refreshed.stderr)

    def test_immediate_predecessor_unknown_and_mixed_tooling_stay_rejected(self):
        self.use_immediate_predecessor()
        marker = self.workspace / 'unapproved-predecessor-validator-executed'
        validator = self.candidate / '.engineering-backbone/validate.py'
        original = validator.read_bytes()
        validator.write_text(f'from pathlib import Path\nPath({str(marker)!r}).touch()\n')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Candidate toolchain fingerprint', result.stderr)
        self.assertFalse(marker.exists())
        shutil.copy2(validator, self.trusted / '.engineering-backbone/validate.py')
        validator.write_bytes(original)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Trusted base toolchain fingerprint', result.stderr)
        self.assertFalse(marker.exists())
        (self.trusted / '.engineering-backbone/validate.py').write_bytes(original)
        historical = self.workspace / 'bootstrap-consumer'
        run_copy(str(self.legacy_source('bootstrap')), historical,
                 defaults=True, quiet=True, skip_tasks=True)
        # Both complete versions are approved; their mixed tuple is not. The
        # immediate predecessor/current tuples differ only in validate.py, so use
        # an actually different approved historical schema for this negative case.
        shutil.copy2(historical / '.engineering-backbone/schemas/project.schema.json',
                     self.candidate / '.engineering-backbone/schemas/project.schema.json')
        self.assertNotEqual(bundle_digest(self.candidate), PREDECESSOR_DIGEST)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Candidate toolchain fingerprint', result.stderr)
        self.assertFalse(marker.exists())

    def test_approved_historical_copies_match_authority_and_remain_usable(self):
        authority = STEPS['Validate generated consumer with trusted tooling']['env']
        previous = json.loads(authority['PREVIOUS_TOOLCHAIN_SHA256'])
        observed = []
        for version in PREVIOUS_TREES:
            with self.subTest(version=version):
                self.use_legacy_base(version)
                observed.append(bundle_digest(self.trusted))
                manifest = json.loads((HISTORICAL_FIXTURES / 'manifest.json').read_text())
                self.assertEqual(observed[-1], manifest['versions'][version]['rendered_toolchain_sha256'])
                result = self.validate()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        # Retain the prerequisite's real historical rendering check, and add
        # actual merged main. Verify Git bytes independently before Copier,
        # measure each rendered identity and exercise the current workflow.
        for snapshot in ('old-source', 'merged-main'):
            with self.subTest(snapshot=snapshot):
                source = self.workspace / (snapshot + '-source')
                for relative, content in frozen_files(snapshot).items():
                    path = source / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                    path.chmod(0o644)
                shutil.rmtree(self.trusted)
                run_copy(str(source), self.trusted, defaults=True, quiet=True, skip_tasks=True)
                shutil.rmtree(self.candidate)
                shutil.copytree(self.trusted, self.candidate)
                measured = bundle_digest(self.trusted)
                if snapshot == 'old-source':
                    self.assertEqual(measured, LAYOUT_PREDECESSOR_DIGEST)
                else:
                    self.assertEqual(measured, MERGED_MAIN_DIGEST)
                result = self.validate()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                observed.append(measured)
        # Preserve original and explicitly reviewed predecessor identities,
        # including merged dependency/navigation tooling and the reviewed
        # OpenCode PR snapshot before its activation repair. Never infer
        # authority from candidate-provided hashes.
        preceding = "5bca19e704f2e6ca5744cfccb10e52b862dc7b9d4c18ed5f5cb3a6db8aadab4a"
        merged_copilot = "91f4d1d7be5573f0939cdb9f3859d3ff236807504abaa554207dfc1705190321"
        merged_codex_security = "ac82ff9e47346f754865aa322db29089281569e1cf432edd43c624026f8ad3fb"
        merged_workflow_kit = "7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb"
        merged_quality_framework = "88d2d1e89cbff9fd925cac1a235de60867ae90a9ae231cde6cbc0a5eed8ee9b2"
        merged_technology_navigation = "e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450"
        reviewed_opencode_seed = "a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896"
        self.assertEqual(set(previous), set(observed) | {
            preceding, merged_copilot, merged_codex_security,
            merged_workflow_kit, merged_quality_framework, merged_technology_navigation,
            PREDECESSOR_DIGEST, reviewed_opencode_seed, LAYOUT_PREDECESSOR_DIGEST,
            PLANNING_PREDECESSOR_DIGEST,
        })
        self.assertEqual(authority['CURRENT_TOOLCHAIN_SHA256'], rendered_digest(ROOT))

    def test_historical_compatibility_survives_clean_single_commit_clone(self):
        self.historical_checkout_checks(autocrlf=False)

    def test_historical_compatibility_survives_autocrlf_source_checkout(self):
        self.historical_checkout_checks(autocrlf=True)

    def historical_checkout_checks(self, *, autocrlf):
        # Squash merging and new repositories need not contain our original
        # local tree objects. Execute the real copy and upgrade checks there.
        seed = self.workspace / 'single-commit-source'
        shutil.copytree(ROOT, seed, ignore=shutil.ignore_patterns('.git', '__pycache__', 'artifacts', '.venv'))
        initialize(seed)
        commit(seed, 'Single squashed source snapshot')
        checkout = self.workspace / 'clean-source-clone'
        git(self.workspace, 'clone', '--no-local', '--no-checkout', str(seed), str(checkout))
        git(checkout, 'config', 'core.autocrlf', str(autocrlf).lower())
        git(checkout, 'checkout', '-f', 'HEAD')
        self.assertEqual(git(checkout, 'rev-list', '--count', 'HEAD'), '1')
        for tree in (*PREVIOUS_TREES.values(), PREDECESSOR_TREE, PREDECESSOR_COMMIT):
            probe = subprocess.run(['git', 'cat-file', '-e', tree], cwd=checkout, capture_output=True)
            self.assertNotEqual(probe.returncode, 0, tree)
        result = subprocess.run([
            sys.executable, '-m', 'unittest',
            'tst.test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable',
            'tst.test_workflows.WorkflowTests.test_real_copier_upgrade_accepts_coherent_tooling_and_preserves_local_facts',
            'tst.test_workflows.WorkflowTests.test_immediate_predecessor_unchanged_and_coherent_current_tooling_pass',
            'tst.test_workflows.WorkflowTests.test_exact_main_legacy_refresh_preserves_facts_and_rejects_policy_weakening',
            'tst.test_workflows.WorkflowTests.test_immediate_predecessor_unknown_and_mixed_tooling_stay_rejected',
            '-v',
        ], cwd=checkout, env=dict(os.environ, PYTHONPATH=str(checkout / '.engineering-backbone')),
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legacy_base_cannot_disable_any_previously_enabled_provider(self):
        for codex, copilot in ((False, True), (True, False), (False, False)):
            with self.subTest(codex=codex, copilot=copilot):
                self.use_legacy_base()
                self.mutate('.engineering-backbone/project.json',
                            lambda d: d['agents'].update(codex=codex, copilot=copilot))
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('cannot disable trusted-base agent', result.stderr)
                self.assertNotIn('Requirement already satisfied', result.stdout)

    def test_initially_disabled_legacy_adapters_are_supported(self):
        self.use_legacy_base(use_codex=False, use_copilot=False)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_workflow_rejects_invalid_or_duplicate_project_selections(self):
        original = (self.candidate / '.engineering-backbone/project.json').read_bytes()
        for value in ('null', '{"agents":{"codex":true,"codex":false,"copilot":true}}',
                      '{"agents":{"codex":1,"copilot":true}}',
                      '{"agents":{"codex":true}}'):
            with self.subTest(value=value):
                (self.candidate / '.engineering-backbone/project.json').write_text(value)
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Requirement already satisfied', result.stdout)
        (self.candidate / '.engineering-backbone/project.json').write_bytes(original)

    def test_toolchain_poisoning_is_rejected_before_merge_and_after_simulated_merge(self):
        for kind in ('validator', 'schema', 'dependency'):
            with self.subTest(kind=kind):
                self.use_legacy_base()
                marker = self.workspace / ('poison-executed-' + kind)
                if kind == 'validator':
                    (self.candidate / '.engineering-backbone/validate.py').write_text(
                        f'from pathlib import Path\nPath({str(marker)!r}).touch()\nprint("poison PASS")\n')
                elif kind == 'schema':
                    (self.candidate / '.engineering-backbone/schemas/core-policy.schema.json').write_text('{}\n')
                else:
                    with (self.candidate / '.engineering-backbone/requirements.lock').open('a') as lock:
                        lock.write('# unapproved lock-only change\n')
                first = self.validate()
                self.assertNotEqual(first.returncode, 0)
                self.assertIn('Candidate toolchain fingerprint', first.stderr)
                self.assertFalse(marker.exists())
                # Even bypassing the merge process cannot promote unknown bytes.
                shutil.rmtree(self.trusted)
                shutil.copytree(self.candidate, self.trusted)
                self.mutate('.engineering-backbone/core.json',
                            lambda d: d['invariants'].update(human_merge_required=False))
                second = self.validate()
                self.assertNotEqual(second.returncode, 0)
                self.assertIn('Trusted base toolchain fingerprint', second.stderr)
                self.assertFalse(marker.exists())

    def test_mixed_approved_versions_and_downgrade_are_rejected(self):
        self.use_legacy_base('bootstrap')
        modern = self.workspace / 'modern'
        run_copy(str(self.source), modern, defaults=True, quiet=True, skip_tasks=True, vcs_ref='HEAD')
        shutil.copy2(modern / '.engineering-backbone/validate.py', self.candidate / '.engineering-backbone/validate.py')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Candidate toolchain fingerprint', result.stderr)
        shutil.rmtree(self.candidate)
        run_copy(str(self.legacy_source('pre-attestation')), self.candidate,
                 defaults=True, quiet=True, skip_tasks=True)
        self.assertNotEqual(self.validate().returncode, 0)
        # Current tooling may stay current, but not downgrade to historical code.
        shutil.rmtree(self.trusted)
        shutil.copytree(modern, self.trusted)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Candidate toolchain fingerprint', result.stderr)

    def test_leaf_and_in_repository_bundle_or_schema_aliases_are_rejected(self):
        original = self.workspace / 'original-consumer'
        shutil.copytree(self.candidate, original)
        for snapshot in (self.candidate, self.trusted):
            for alias in ('validate.py', 'schemas', 'bundle'):
                with self.subTest(snapshot=snapshot.name, alias=alias):
                    shutil.rmtree(snapshot)
                    shutil.copytree(original, snapshot)
                    bundle = snapshot / '.engineering-backbone'
                    if alias == 'bundle':
                        target = snapshot / 'approved-alias'
                        bundle.rename(target)
                        bundle.symlink_to(target, target_is_directory=True)
                    else:
                        source = bundle / alias
                        target = snapshot / ('alias-' + alias)
                        source.rename(target)
                        source.symlink_to(target, target_is_directory=alias == 'schemas')
                    result = self.validate()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('symlinked managed file', result.stderr)
                    self.assertNotIn('Requirement already satisfied', result.stdout)
            shutil.rmtree(snapshot)
            shutil.copytree(original, snapshot)

    def test_policy_alias_is_rejected_before_pip_and_after_simulated_promotion(self):
        for filename in ('core.json', 'core.md'):
            with self.subTest(filename=filename):
                self.use_legacy_base('pre-attestation')
                for root in (self.trusted, self.candidate):
                    self.mutate('.engineering-backbone/core.json',
                                lambda d: d['invariants'].update(security_review_required=True), root)
                original = self.candidate / '.engineering-backbone' / filename
                target = self.candidate / ('strict-' + filename)
                target.write_bytes(original.read_bytes())
                original.unlink()
                # In the first snapshot this resolves inside candidate. After a
                # symlink-preserving merge copy it aliases the next candidate.
                original.symlink_to('../../candidate/' + target.name)
                first = self.validate()
                self.assertNotEqual(first.returncode, 0)
                self.assertIn('symlinked managed file: ' + filename, first.stderr)
                self.assertNotIn('Requirement already satisfied', first.stdout)
                shutil.rmtree(self.trusted)
                shutil.copytree(self.candidate, self.trusted, symlinks=True)
                if filename == 'core.json':
                    data = json.loads(target.read_text())
                    data['invariants'].pop('security_review_required')
                    target.write_text(json.dumps(data) + '\n')
                else:
                    target.write_text('Next candidate changed the aliased policy document.\n')
                second = self.validate()
                self.assertNotEqual(second.returncode, 0)
                self.assertIn('symlinked managed file: ' + filename, second.stderr)
                self.assertNotIn('Requirement already satisfied', second.stdout)

    def test_regular_strict_policy_data_and_document_remain_supported(self):
        self.use_legacy_base('pre-attestation')
        for root in (self.trusted, self.candidate):
            self.mutate('.engineering-backbone/core.json',
                        lambda d: d['invariants'].update(security_review_required=True), root)
            with (root / '.engineering-backbone/core.md').open('a') as policy:
                policy.write('\nProject security review is mandatory.\n')
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_real_copier_upgrade_accepts_coherent_tooling_and_preserves_local_facts(self):
        self.real_copier_upgrade()

    def test_real_copier_upgrade_without_local_object_copy(self):
        self.real_copier_upgrade(require_transport=True)

    def real_copier_upgrade(self, *, require_transport=False):
        source = self.legacy_source('pre-attestation')
        initialize(source)
        commit(source, 'Historical template')
        git(source, 'tag', 'v0.1.0')
        if require_transport:
            # A valid object store that native Git refuses to copy with --local
            # makes this regression deterministic without recreating race timing.
            objects = source / '.git/objects'
            objects.rename(objects.with_name('fixture-objects'))
            objects.symlink_to('fixture-objects', target_is_directory=True)
            git(source, 'fsck', '--full')
            local_clone = subprocess.run(
                ['git', 'clone', '--no-checkout', str(source),
                 str(self.workspace / 'local-clone-control')],
                capture_output=True, text=True,
            )
            self.assertNotEqual(local_clone.returncode, 0, local_clone.stdout + local_clone.stderr)
            self.assertIn('symlink', local_clone.stderr)
        shutil.rmtree(self.candidate)
        # Persist transport access for both adoption and update, avoiding Git's
        # local loose-object copying when the temporary source changes.
        run_copy('git+' + source.resolve().as_uri(), self.candidate,
                 defaults=True, quiet=True, skip_tasks=True, vcs_ref='v0.1.0')
        facts = self.candidate / '.engineering-backbone/project.json'
        data = json.loads(facts.read_text())
        data['project'].update(name='local-stricter-project', language='Go', base_branch='reviewed/base',
                               validation_command='go test ./...')
        facts.write_text(json.dumps(data) + '\n')
        (self.candidate / 'AGENTS.md').write_text('Local stricter instructions remain binding.\n')
        self.mutate('.engineering-backbone/core.json',
                    lambda d: d['invariants'].update(security_review_required=True))
        initialize(self.candidate)
        commit(self.candidate, 'Trusted local adoption')
        shutil.rmtree(self.trusted)
        shutil.copytree(self.candidate, self.trusted)
        saved_facts = facts.read_bytes()
        # Replace only the trusted temporary template source, not a real checkout.
        for item in source.iterdir():
            if item.name != '.git':
                shutil.rmtree(item) if item.is_dir() else item.unlink()
        shutil.copytree(ROOT, source, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('.git', '__pycache__', 'artifacts', '.venv'))
        commit(source, 'Current template')
        git(source, 'tag', 'v0.2.0')
        run_update(self.candidate, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        # Copier-owned policy refresh needs manual integration of stricter rules.
        self.mutate('.engineering-backbone/core.json',
                    lambda d: d['invariants'].update(security_review_required=True))
        self.assertEqual(saved_facts, facts.read_bytes())
        self.assertEqual('Local stricter instructions remain binding.\n',
                         (self.candidate / 'AGENTS.md').read_text())
        expected = STEPS['Validate generated consumer with trusted tooling']['env']['CURRENT_TOOLCHAIN_SHA256']
        self.assertEqual(expected, bundle_digest(self.candidate))
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_managed_attributes_keep_real_autocrlf_checkout_fingerprint_stable(self):
        initialize(self.candidate)
        (self.candidate / 'application.txt').write_text('Application text\n')
        commit(self.candidate, 'Generated adoption')
        checkout = self.workspace / 'windows-checkout'
        subprocess.run(['git', '-c', 'core.autocrlf=true', 'clone', str(self.candidate), str(checkout)],
                       check=True, capture_output=True)
        self.assertIn(b'\r\n', (checkout / 'application.txt').read_bytes())
        self.assertEqual(bundle_digest(self.candidate), bundle_digest(checkout))

    def test_compiler_tracks_uncommitted_tooling_and_ignores_document_metadata(self):
        source = self.workspace / 'compiler-source'
        shutil.copytree(self.source, source)
        baseline = rendered_digest(source)
        with (source / 'docs/agent-governance/adoption.md').open('a') as docs:
            docs.write('\nUncommitted documentation metadata.\n')
        self.assertEqual(baseline, rendered_digest(source))
        with (source / '.engineering-backbone/src/validate.py').open('a') as validator:
            validator.write('\n# Uncommitted tooling fixture requires a new pin.\n')
        self.assertNotEqual(baseline, rendered_digest(source))
        command = [sys.executable, str(ROOT / '.engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py'), '--source', str(source)]
        stale = subprocess.run(command + ['--check'], text=True, capture_output=True)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn('fingerprint is stale', stale.stdout)
        written = subprocess.run(command + ['--write'], text=True, capture_output=True)
        self.assertEqual(written.returncode, 0, written.stdout + written.stderr)
        checked = subprocess.run(command + ['--check'], text=True, capture_output=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_both_generated_callers_expose_documented_manual_dispatch(self):
        target = self.workspace / 'active-consumer'
        run_copy(str(self.source), target, data={'backbone_workflow_ref': 'a' * 40},
                 defaults=True, quiet=True, skip_tasks=True, vcs_ref='HEAD')
        actual = yaml.safe_load((target / '.github/workflows/engineering-backbone.yml').read_text())
        example = (target / '.engineering-backbone/workflow-example.md').read_text().split('```yaml\n', 1)[1].split('```', 1)[0]
        sample = yaml.safe_load(example)
        for caller in (actual, sample):
            self.assertIn('workflow_dispatch', caller.get('on', caller.get(True)))

    def whitespace_fixture(self, *, first_commit=False, bad=True):
        shutil.rmtree(self.candidate)
        self.candidate.mkdir()
        initialize(self.candidate)
        file = self.candidate / 'text.txt'
        file.write_text('valid\n')
        base = None if first_commit else commit(self.candidate, 'Base')
        file.write_text('valid\n' + ('trailing whitespace  \n' if bad else 'clean patch\n'))
        head = commit(self.candidate, 'Candidate')
        self.assertEqual(git(self.candidate, 'diff', '--check'), '')
        return base, head

    def test_committed_whitespace_fails_pr_and_push_on_clean_checkout(self):
        base, head = self.whitespace_fixture()
        for event in ('pull_request', 'push'):
            with self.subTest(event=event):
                result = self.shell('Check committed patch whitespace', EVENT_NAME=event, BASE_SHA=base, HEAD_SHA=head)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('trailing whitespace', result.stdout)

    def test_clean_committed_patch_passes_pr_and_push(self):
        base, head = self.whitespace_fixture(bad=False)
        for event in ('pull_request', 'push'):
            result = self.shell('Check committed patch whitespace', EVENT_NAME=event, BASE_SHA=base, HEAD_SHA=head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dispatch_checks_selected_commits_latest_patch(self):
        _, head = self.whitespace_fixture()
        result = self.shell('Check committed patch whitespace', EVENT_NAME='workflow_dispatch', BASE_SHA='', HEAD_SHA=head)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('trailing whitespace', result.stdout)

    def test_first_commit_whitespace_is_checked_for_push_and_dispatch(self):
        for bad in (False, True):
            _, head = self.whitespace_fixture(first_commit=True, bad=bad)
            for event in ('push', 'workflow_dispatch'):
                with self.subTest(event=event, bad=bad):
                    result = self.shell('Check committed patch whitespace', EVENT_NAME=event,
                                        BASE_SHA='0' * 40 if event == 'push' else '', HEAD_SHA=head)
                    self.assertEqual(result.returncode == 0, not bad, result.stdout + result.stderr)

    def test_whitespace_guard_rejects_invalid_context_and_events(self):
        base, head = self.whitespace_fixture(bad=False)
        for env in ({'HEAD_SHA': 'main'}, {'BASE_SHA': 'main'}, {'BASE_SHA': '0' * 40},
                    {'HEAD_SHA': 'f' * 40}, {'EVENT_NAME': 'schedule'}):
            with self.subTest(env=env):
                values = {'BASE_SHA': base, 'HEAD_SHA': head}
                values.update(env)
                result = self.shell('Check committed patch whitespace', **values)
                self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
