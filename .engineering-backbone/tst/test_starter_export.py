"""Real neutral export/verification and read-only trusted update boundaries."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = '.engineering-backbone/src/starter.py'
spec = importlib.util.spec_from_file_location('starter_under_test', ROOT / SCRIPT)
starter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = starter
spec.loader.exec_module(starter)


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()


def commit(root, message):
    git(root, 'add', '-A')
    git(root, 'commit', '-m', message)
    return git(root, 'rev-parse', 'HEAD')


def file_snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob('*') if path.is_file() and '.git' not in path.parts}


class StarterExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='backbone-starter-tests-')
        cls.workspace = Path(cls.temporary.name)
        cls.source = cls.workspace / 'trusted'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns(
            '.git', '.venv', 'venv', '__pycache__', 'node_modules', 'artifacts',
            '.pytest_cache', '.mypy_cache', 'dist', 'build'))
        # These sentinel files demonstrate that neither tracked nor untracked real
        # environment values enter the executable-owned export plan.
        (cls.source / '.env').write_text('DO_NOT_EXPORT=sentinel-secret\n')
        git(cls.source, 'init', '-q')
        git(cls.source, 'config', 'user.name', 'Starter test')
        git(cls.source, 'config', 'user.email', 'starter-test@example.invalid')
        git(cls.source, 'config', 'core.autocrlf', 'false')
        cls.ref = commit(cls.source, 'Frozen starter fixture')
        cls.authority = starter.TrustedSource(cls.source, cls.ref)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        self.run_directory = tempfile.TemporaryDirectory(prefix='starter-project-')
        self.addCleanup(self.run_directory.cleanup)
        self.project = Path(self.run_directory.name) / 'project'
        starter.write_export(self.authority, self.project, 'example')

    def test_real_export_verifies_without_source_history_or_git(self):
        self.assertGreater(starter.verify_project(self.authority, self.project), 100)
        for omitted in ('.git', '.env', 'copier.yml', '.github/workflows',
                        '.engineering-backbone/src/validate.py', '.engineering-backbone/legacy',
                        '.engineering-backbone/tst', 'docs/changes/backbone-project-starter'):
            self.assertFalse((self.project / omitted).exists(), omitted)
        self.assertTrue((self.project / '.env.example').is_file())
        facts = json.loads((self.project / '.engineering-backbone/project.json').read_text())
        self.assertEqual(facts['project']['name'], 'example')
        for filename in ('AGENTS.md', 'README.md', 'CONTRIBUTING.md',
                         '.github/copilot-instructions.md', 'docs/changes/README.md',
                         'docs/operations/development.md'):
            text = (self.project / filename).read_text()
            self.assertNotIn('BB-START-018', text)
            self.assertNotIn('BB-TEST-017', text)
            self.assertNotIn('python .engineering-backbone/src/validate.py', text)
        self.assertFalse(any(b'sentinel-secret' in data for data in file_snapshot(self.project).values()))
        # An ordinary product fixture remains independent of governance JSON.
        fixture = self.project / 'apps/backend/tst/examples/request.json'
        fixture.parent.mkdir(parents=True)
        fixture.write_text('{"value": 1}')
        shutil.rmtree(self.project / 'apps/frontend')
        starter.verify_project(self.authority, self.project)

    def test_export_refuses_existing_content_symlinks_and_traversal_without_overwrite(self):
        before = file_snapshot(self.project)
        with self.assertRaises(starter.StarterError):
            starter.write_export(self.authority, self.project, 'other')
        self.assertEqual(before, file_snapshot(self.project))
        linked = self.project.parent / 'linked'
        linked.symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(starter.StarterError):
            starter.write_export(self.authority, linked / 'new', 'other')
        with self.assertRaises(starter.StarterError):
            starter.write_export(self.authority, self.project / '..' / 'new', 'other')
        self.assertEqual(before, file_snapshot(self.project))

    def test_managed_policy_and_schema_tampering_cannot_be_authorized_by_manifest(self):
        for relative in ('docs/agent-governance/core.md', '.engineering-backbone/schemas/requirement.schema.json'):
            with self.subTest(path=relative):
                target = self.project / relative
                original = target.read_bytes()
                target.write_bytes(original + b'\n')
                manifest = self.project / starter.MANIFEST
                metadata = json.loads(manifest.read_text())
                for row in metadata['files']:
                    if row['path'] == relative:
                        row['sha256'] = starter.digest(target.read_bytes())
                manifest.write_text(json.dumps(metadata))
                with self.assertRaises(starter.StarterError):
                    starter.verify_project(self.authority, self.project)
                target.write_bytes(original)
                manifest.write_text(json.dumps(starter.manifest_for(self.authority, starter.build_plan(self.authority, 'example'))))
        missing = self.project / '.engineering-backbone/core.json'
        original = missing.read_bytes()
        missing.unlink()
        with self.assertRaises(starter.StarterError):
            starter.verify_project(self.authority, self.project)
        missing.write_bytes(original)

    def test_symlink_and_case_variant_managed_paths_rejected(self):
        target = self.project / 'docs/agent-governance/core.md'
        original = target.read_bytes()
        other = self.project.parent / 'policy.md'
        other.write_bytes(original)
        target.unlink()
        target.symlink_to(other)
        with self.assertRaises(starter.StarterError):
            starter.verify_project(self.authority, self.project)
        target.unlink()
        target.write_bytes(original)
        (self.project / 'docs/agent-governance/Core.md').write_bytes(original)
        with self.assertRaises(starter.StarterError):
            starter.verify_project(self.authority, self.project)

    def test_project_metadata_governance_and_context_remain_checked(self):
        registry = self.project / 'config/environment.json'
        registry.write_text('{"version": 1, "variables": [], "secret_default": "not-allowed"}')
        with self.assertRaisesRegex(starter.StarterError, 'environment metadata'):
            starter.verify_project(self.authority, self.project)
        registry.write_text('{"version": 1, "variables": []}')
        invalid = self.project / 'docs/changes/delivery/task-packet.json'
        invalid.parent.mkdir(parents=True)
        invalid.write_text('{"scope": {}}')
        with self.assertRaisesRegex(starter.StarterError, 'task-packet'):
            starter.verify_project(self.authority, self.project)
        invalid.unlink()
        agents = self.project / 'AGENTS.md'
        agents.write_text('No canonical context here.\n')
        with self.assertRaisesRegex(starter.StarterError, 'canonical context'):
            starter.verify_project(self.authority, self.project)

    def test_source_legacy_and_optional_contracts_cannot_switch_to_seed_gate(self):
        for relative in ('.engineering-backbone/workflows.json', '.engineering-backbone/quality-profile.json',
                         '.engineering-backbone/navigation.json', '.engineering-backbone/dependencies.json'):
            for enabled in (False, True):
                with self.subTest(path=relative, enabled=enabled):
                    target = self.project / relative
                    target.write_text(json.dumps({'enabled': enabled}))
                    with self.assertRaisesRegex(starter.StarterError, 'separately reviewed integration'):
                        starter.verify_project(self.authority, self.project)
                    target.unlink()
        marker = self.project / '.engineering-backbone/validate.py'
        marker.write_text('raise RuntimeError("candidate code must never run")')
        with self.assertRaisesRegex(starter.StarterError, 'source/legacy'):
            starter.verify_project(self.authority, self.project)
        marker.unlink()
        workflow = self.project / '.github/workflows/ci.yml'
        workflow.parent.mkdir()
        workflow.write_text('name: unreviewed\n')
        with self.assertRaisesRegex(starter.StarterError, 'active CI'):
            starter.verify_project(self.authority, self.project)
        with self.assertRaisesRegex(starter.StarterError, 'source/legacy'):
            starter.verify_project(self.authority, self.source)

    def test_native_reserved_alias_and_selection_cannot_bypass_baseline(self):
        alias = self.project / '.codex/agents/other.toml'
        alias.write_text((self.project / '.codex/agents/backbone-planner.toml').read_text())
        with self.assertRaisesRegex(starter.StarterError, 'native instruction'):
            starter.verify_project(self.authority, self.project)
        alias.unlink()
        facts = self.project / '.engineering-backbone/project.json'
        data = json.loads(facts.read_text())
        data['agents']['codex'] = False
        facts.write_text(json.dumps(data))
        with self.assertRaisesRegex(starter.StarterError, 'cannot be disabled'):
            starter.verify_project(self.authority, self.project)

    def test_immutable_ref_and_dirty_executing_helper_are_rejected(self):
        for invalid in ('HEAD', 'main', self.ref[:8], '0' * 40):
            with self.subTest(ref=invalid), self.assertRaises(starter.StarterError):
                starter.TrustedSource(self.source, invalid)
        script = self.source / SCRIPT
        original = script.read_bytes()
        try:
            script.write_bytes(original + b'\n# dirty executable\n')
            with self.assertRaisesRegex(starter.StarterError, 'trusted Git blob'):
                starter.TrustedSource(self.source, self.ref)
        finally:
            script.write_bytes(original)
        helper = self.source / '.engineering-backbone/src/environment.py'
        original = helper.read_bytes()
        try:
            helper.write_bytes(original + b'\nraise RuntimeError("not executed")\n')
            with self.assertRaisesRegex(starter.StarterError, 'environment helper differs'):
                starter.verify_project(self.authority, self.project)
        finally:
            helper.write_bytes(original)

    def test_compare_uses_two_trusted_revisions_and_never_applies_or_reads_real_env(self):
        newer = self.project.parent / 'new-trusted'
        git(self.source, 'clone', '--quiet', str(self.source), str(newer))
        git(newer, 'config', 'user.name', 'Starter test')
        git(newer, 'config', 'user.email', 'starter-test@example.invalid')
        # One unchanged upstream managed file modified locally.
        local_only = 'docs/quality/testing.md'
        (self.project / local_only).write_bytes((self.project / local_only).read_bytes() + b'\nlocal note\n')
        # One upstream-only and one conflicting managed change.
        upstream = 'docs/quality/policy.md'
        conflict = 'docs/quality/ci-cd.md'
        for path in (upstream, conflict):
            with (newer / path).open('ab') as stream:
                stream.write(b'\nupstream note\n')
        with (self.project / conflict).open('ab') as stream:
            stream.write(b'\nother local note\n')
        added = newer / 'docs/templates/testing/new-guide.md'
        added.write_text('# New guide\n')
        removed = 'docs/templates/testing/review.md'
        (newer / removed).unlink()
        # Change one path's ownership in the NEW trusted executable, not project metadata.
        code = newer / SCRIPT
        text = code.read_text().replace("PROJECT_FILES = (", "PROJECT_FILES = ('docs/templates/testing/test-design.md',")
        code.write_text(text)
        new_ref = commit(newer, 'Reviewed new baseline')
        new_authority = starter.TrustedSource(newer, new_ref)
        # A named pipe would block if the comparator tried to read real .env values.
        secret = self.project / '.env'
        if hasattr(__import__('os'), 'mkfifo'):
            __import__('os').mkfifo(secret)
        before = file_snapshot(self.project)
        completed = subprocess.run([sys.executable, '-I', str(newer / SCRIPT), 'compare',
                                    '--source-ref', new_ref, '--old-source', str(self.source),
                                    '--old-ref', self.ref, '--root', str(self.project)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        rows = json.loads(completed.stdout)['files']
        self.assertEqual(before, file_snapshot(self.project))
        statuses = {row['path']: row['status'] for row in rows}
        self.assertEqual(statuses[local_only], 'local-modification')
        self.assertEqual(statuses[upstream], 'upstream-only')
        self.assertEqual(statuses[conflict], 'conflict')
        self.assertEqual(statuses['docs/templates/testing/new-guide.md'], 'new-upstream')
        self.assertEqual(statuses[removed], 'removed-upstream')
        self.assertEqual(statuses['docs/templates/testing/test-design.md'], 'ownership-change')
        self.assertTrue(all(row['action'] == 'preserve-project-owned' for row in rows if row['owner'] == 'project'))

    def test_real_cli_and_autocrlf_checkout_preserve_managed_bytes(self):
        command = [sys.executable, '-I', str(self.source / SCRIPT), 'verify', '--source-ref', self.ref, '--root', str(self.project)]
        checked = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn('No product/runtime/human approval claim', checked.stdout)
        git(self.project, 'init', '-q')
        git(self.project, 'config', 'user.name', 'Starter test')
        git(self.project, 'config', 'user.email', 'starter-test@example.invalid')
        commit(self.project, 'Reviewed project seed')
        checkout = self.project.parent / 'autocrlf-project'
        subprocess.run(['git', '-c', 'core.autocrlf=true', 'clone', '--quiet', str(self.project), str(checkout)], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        starter.verify_project(self.authority, checkout)


if __name__ == '__main__':
    unittest.main()
