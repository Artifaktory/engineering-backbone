"""Exact, offline source-layout transitions through the executing trusted bridge.

Snapshots are data from Git, not a projection. The PR18 validator is never run;
only the current bridge and the independently frozen prior-main validator run.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/layout-compatibility'
SNAPSHOTS = {
    'old-source': ('212608aa50ee517b3dd3107a9480da997222fd4f',
                   'c31ee9b6e418325936b59e31cd7e9b9865ed0064', 495),
    'pr18-source': ('c50108773ba3195bf0f7503e5dffb2d7bfc78cd3',
                    'af532155a9f1196aa65e553b24b957f5f50297a3', 542),
}
HISTORICAL = 'docs/changes/backbone-bootstrap/reviews/bootstrap-result.md'
LAYOUT_MAP = 'docs/changes/backbone-layout/layout-map.json'


def git_object(kind, content):
    return hashlib.sha1(kind.encode() + b' ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def git_tree(entries):
    tree = {}
    for entry in entries:
        parent = tree
        parts = entry['path'].split('/')
        for part in parts[:-1]:
            parent = parent.setdefault(part, {})
        parent[parts[-1]] = (entry['mode'], entry['git_blob'])

    def digest(directory):
        output = bytearray()
        for name, value in sorted(directory.items(),
                                  key=lambda pair: (pair[0] + ('/' if isinstance(pair[1], dict) else '')).encode()):
            mode, blob = ('40000', digest(value)) if isinstance(value, dict) else value
            output.extend(mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(blob))
        return git_object('tree', bytes(output))
    return digest(tree)


def frozen_files(name):
    """Verify archive bytes, Git blobs, modes and the independently pinned tree."""
    commit, tree, count = SNAPSHOTS[name]
    manifest = json.loads((FIXTURES / 'manifest.json').read_text())['snapshots'][name]
    assert (manifest['commit'], manifest['git_tree'], manifest['file_count']) == (commit, tree, count)
    assert manifest['archive'] == name + '.zip'
    archive = FIXTURES / manifest['archive']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['archive_sha256']
    entries = manifest['entries']
    assert len(entries) == count
    assert len({entry['path'] for entry in entries}) == count
    result = {}
    with zipfile.ZipFile(archive) as zipped:
        assert len(zipped.namelist()) == count
        assert set(zipped.namelist()) == {entry['path'] for entry in entries}
        for entry in entries:
            path = PurePosixPath(entry['path'])
            assert not path.is_absolute() and '..' not in path.parts and path.as_posix() == entry['path']
            assert entry['mode'] in {'100644', '100755'}
            assert zipped.getinfo(entry['path']).external_attr >> 16 == int(entry['mode'], 8)
            data = zipped.read(entry['path'])
            assert hashlib.sha256(data).hexdigest() == entry['sha256']
            assert git_object('blob', data) == entry['git_blob']
            result[entry['path']] = data
    assert git_tree(entries) == tree
    return result


class SourceLayoutCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Verification precedes every extraction/validator call, including the
        # prior-main executable. No checkout, Git object access or network in CI.
        cls.snapshots = {name: frozen_files(name) for name in SNAPSHOTS}

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-source-layout-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.candidate = self.extract('pr18-source', 'candidate')
        self.base = self.extract('old-source', 'base')

    def extract(self, name, folder):
        root = self.workspace / folder
        for relative, content in self.snapshots[name].items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            # Both frozen trees contain regular 100644 files only (verified by
            # the manifest); preserve that mode rather than the host umask.
            path.chmod(0o644)
        return root

    def write(self, relative, content, root=None):
        path = (root or self.candidate) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def change_json(self, relative, update, root=None):
        path = (root or self.candidate) / relative
        value = json.loads(path.read_text())
        update(value)
        path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

    def validate(self, candidate=None, base=None, validator=None):
        return subprocess.run(
            [sys.executable, '-I', '-B', str(validator or ROOT / 'scripts/validate.py'),
             '--root', str(candidate or self.candidate), '--trusted-base', str(base or self.base)],
            cwd=self.workspace, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=60, check=False)

    def assert_pass(self, **kwargs):
        result = self.validate(**kwargs)
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertNotIn('Traceback', result.stdout)

    def assert_reject(self, fragment, **kwargs):
        result = self.validate(**kwargs)
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertNotIn('Traceback', result.stdout)
        self.assertIn(fragment, result.stdout)

    def test_exact_frozen_git_trees_are_used_without_projection(self):
        for name, (_, _, count) in SNAPSHOTS.items():
            with self.subTest(snapshot=name):
                self.assertEqual(count, len(self.snapshots[name]))
        self.assertFalse((self.candidate / 'policy/core.json').exists())
        self.assertTrue((self.candidate / '.engineering-backbone/core.json').is_file())
        self.assertEqual(self.snapshots['pr18-source']['.engineering-backbone/src/validate.py'],
                         (self.candidate / '.engineering-backbone/src/validate.py').read_bytes())
        self.assert_pass()

    def test_candidate_and_base_layouts_are_independent(self):
        old_candidate = self.extract('old-source', 'old-candidate')
        new_base = self.extract('pr18-source', 'new-base')
        for candidate in (old_candidate, self.candidate):
            for base in (self.base, new_base):
                with self.subTest(candidate=candidate.name, base=base.name):
                    self.assert_pass(candidate=candidate, base=base)

    def test_actual_prior_main_validator_accepts_old_layout_bridge(self):
        self.assert_pass(candidate=ROOT, validator=self.base / 'scripts/validate.py')

    def test_product_root_manifests_do_not_select_source_layout(self):
        for name, content in {
            'requirements.txt': 'project-library>=1\n',
            'requirements.lock': 'project-owned resolution format\n',
            'package.json': '{"name":"project-ui","private":true}\n',
            'pnpm-lock.yaml': 'lockfileVersion: 9\n',
            'Cargo.toml': '[package]\nname = "desktop-project"\nversion = "1.0.0"\n',
            'Dockerfile': 'FROM scratch\n',
        }.items():
            self.write(name, content)
        self.assert_pass()

    def test_candidate_validator_is_never_executed(self):
        marker = self.workspace / 'candidate-validator-executed'
        self.write('.engineering-backbone/src/validate.py',
                   'from pathlib import Path\nPath(' + repr(str(marker)) + ').touch()\nraise SystemExit(0)\n')
        self.change_json('.engineering-backbone/core.json',
                         lambda data: data['invariants'].update(human_merge_required=False))
        self.assert_reject('mandatory policy invariant human_merge_required must be True')
        self.assertFalse(marker.exists())

    def test_stricter_base_invariants_survive_either_layout(self):
        for name, core in (('old-source', 'policy/core.json'),
                           ('pr18-source', '.engineering-backbone/core.json')):
            base = self.extract(name, name + '-stricter')
            self.change_json(core, lambda data: data['invariants'].update(project_extra_review=True), root=base)
            with self.subTest(base=name):
                self.assert_reject('policy regression: trusted-base invariant project_extra_review', base=base)
                self.change_json('.engineering-backbone/core.json',
                                 lambda data: data['invariants'].update(project_extra_review=True))
                self.assert_pass(base=base)
                self.change_json('.engineering-backbone/core.json',
                                 lambda data: data['invariants'].pop('project_extra_review'))

    def test_invalid_selected_policy_does_not_fall_back(self):
        self.write('.engineering-backbone/core.json', '{broken JSON\n')
        self.assert_reject('.engineering-backbone/core.json:')

    def test_new_named_task_and_review_records_are_validated(self):
        for filename in ('task-packet.json', 'review-evidence.json'):
            self.write('docs/changes/new-change/' + filename,
                       self.snapshots['pr18-source']['docs/templates/examples/' + filename].decode())
        self.assert_pass()
        self.change_json('docs/changes/new-change/task-packet.json', lambda data: data.pop('objective'))
        self.assert_reject("task-packet.json: <root>: 'objective' is a required property")

    def test_candidate_schema_cannot_authorize_malformed_new_task(self):
        self.write('.engineering-backbone/schemas/task-packet.schema.json', '{}\n')
        self.write('docs/changes/new-change/task-packet.json', '{"scope": {}}\n')
        self.assert_reject("task-packet.json: <root>: 'schema_version' is a required property")

    def test_new_evidence_schema_and_independent_reviewer_are_enforced(self):
        name = 'docs/changes/new-change/review-evidence.json'
        original = self.snapshots['pr18-source']['docs/templates/examples/review-evidence.json'].decode()
        self.write(name, original)
        self.change_json(name, lambda data: data.pop('subject'))
        self.assert_reject("review-evidence.json: <root>: 'subject' is a required property")
        self.write(name, original)
        self.change_json(name, lambda data: data['reviewers'][0].update(id=data['implementer']))
        self.assert_reject('implementer cannot be their own independent reviewer')

    def test_candidate_flags_cannot_disable_inherited_adapters(self):
        self.change_json('.engineering-backbone/project.json',
                         lambda data: data['agents'].update(codex=False, copilot=False))
        self.assert_reject('adapter regression: trusted-base enabled codex must remain enabled')
        self.assert_reject('adapter regression: trusted-base enabled copilot must remain enabled')

    def test_native_permission_broadening_is_rejected(self):
        self.change_json('opencode.json', lambda data: data['permission'].update(bash='allow'))
        self.assert_reject('permission keys exceed')

    def test_inherited_extra_instructions_are_not_dropped_or_remapped(self):
        old_path = 'docs/owner-policy.md'
        new_path = 'docs/agent-governance/owner-policy.md'
        self.write(old_path, '# Additional owner restriction\n', root=self.base)
        self.change_json('opencode.json', lambda data: data['instructions'].append(old_path), root=self.base)
        self.assert_reject('inherited OpenCode instructions cannot disappear')
        self.write(new_path, '# Additional owner restriction\n')
        self.change_json('opencode.json', lambda data: data['instructions'].append(new_path))
        self.change_json(LAYOUT_MAP, lambda data: data['entries'].append({
            'old_path': old_path, 'new_path': new_path, 'preserve_bytes': True}))
        self.assert_reject('inherited OpenCode instructions cannot disappear')
        self.write(old_path, '# Additional owner restriction\n')
        self.change_json('opencode.json', lambda data: data['instructions'].append(old_path))
        self.assert_pass()

    def test_changed_archive_bytes_cannot_be_authorized_by_candidate_map(self):
        path = self.candidate / HISTORICAL
        path.write_bytes(path.read_bytes() + b'\nCandidate edits archived evidence.\n')
        self.assert_reject('historical record bytes differ from the reviewed archive')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        def forge(data):
            for entry in data['entries']:
                if entry['new_path'] == HISTORICAL:
                    entry.update(preserve_bytes=False, sha256=digest, base_sha256=digest)
        self.change_json(LAYOUT_MAP, forge)
        self.assert_reject('historical record bytes differ from the reviewed archive')

    def test_candidate_mapping_cannot_redirect_missing_historical_target(self):
        target = 'docs/operations/engineering/repository-controls.md'
        (self.candidate / target).unlink()
        self.write('candidate-approved.md', '# Candidate replacement\n')
        def forge(data):
            for entry in data['entries']:
                if entry['old_path'] == 'docs/repository-controls.md':
                    entry['new_path'] = 'candidate-approved.md'
        self.change_json(LAYOUT_MAP, forge)
        self.assert_reject(HISTORICAL + ': broken local Markdown link ../repository-controls.md')

    def test_broken_current_link_does_not_receive_historical_exemption(self):
        self.write('docs/changes/new-change/current.md', '# New work\n[Broken](absent-current-file.md)\n')
        self.assert_reject('current.md: broken local Markdown link absent-current-file.md')

    def test_selected_tooling_manifest_cannot_be_hidden_by_root_manifest(self):
        selected = self.candidate / '.engineering-backbone/requirements.txt'
        original = selected.read_bytes()
        self.write('requirements.txt', original.decode())
        self.write('requirements.lock', (self.candidate / '.engineering-backbone/requirements.lock').read_text())
        selected.unlink()
        self.assert_reject('missing required file: .engineering-backbone/requirements.txt')
        selected.write_text('unlocked>=1\n')
        self.assert_reject('dependency entries must use exact == pins')
        selected.write_text('nonexistent-package==1.0\n')
        self.assert_reject('dependency lock mismatch: nonexistent-package==1.0')

    def test_missing_dual_and_mixed_policy_authorities_fail_closed(self):
        core = self.candidate / '.engineering-backbone/core.json'
        original = core.read_bytes()
        core.unlink()
        self.assert_reject('Source layout: absent canonical policy')
        core.write_bytes(original)
        old_core = self.write('policy/core.json', original.decode())
        self.assert_reject('Source layout: ambiguous canonical policy')
        old_core.unlink()
        self.write('policy/core.md', '# Stale old policy\n')
        self.assert_reject('Source layout: mixed canonical policy')

    def test_incomplete_canonical_policy_documents_fail_closed(self):
        for relative in ('docs/agent-governance/core.md', 'docs/quality/policy.md',
                         'docs/quality/dependencies.md'):
            path = self.candidate / relative
            original = path.read_bytes()
            path.unlink()
            with self.subTest(path=relative):
                self.assert_reject('Source layout: missing canonical policy file: ' + relative)
            path.write_bytes(original)

    def test_selected_policy_leaf_symlink_is_rejected(self):
        path = self.candidate / '.engineering-backbone/core.json'
        original = path.read_bytes()
        path.unlink()
        target = self.workspace / 'policy-target.json'
        target.write_bytes(original)
        path.symlink_to(target)
        self.assert_reject('symlinked canonical policy: .engineering-backbone/core.json')

    def test_selected_policy_ancestor_symlink_is_rejected(self):
        path = self.candidate / 'docs/agent-governance'
        target = self.workspace / 'policy-documents'
        shutil.move(str(path), target)
        path.symlink_to(target, target_is_directory=True)
        self.assert_reject('symlinked canonical policy: docs/agent-governance/core.md')

    def test_dangling_alternate_policy_leaf_and_parent_are_ambiguous(self):
        path = self.candidate / 'policy'
        path.mkdir()
        leaf = path / 'core.json'
        leaf.symlink_to(self.workspace / 'absent-policy.json')
        self.assert_reject('Source layout: ambiguous canonical policy')
        leaf.unlink()
        path.rmdir()
        path.symlink_to(self.workspace / 'absent-policy-directory', target_is_directory=True)
        self.assert_reject('Source layout: ambiguous canonical policy')

    def test_trusted_base_policy_ambiguity_cannot_remove_history_checks(self):
        self.write('.engineering-backbone/core.json',
                   (self.base / 'policy/core.json').read_text(), root=self.base)
        self.assert_reject('Source layout: ambiguous canonical policy')


if __name__ == '__main__':
    unittest.main()
