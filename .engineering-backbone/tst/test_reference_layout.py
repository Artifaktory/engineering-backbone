"""Exercise real direct copies and immutable relocation/history contracts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
MAP = 'docs/changes/backbone-layout/layout-map.json'
VALIDATOR = '.engineering-backbone/src/validate.py'
BASE = '212608aa50ee517b3dd3107a9480da997222fd4f'
MAP_SHA256 = 'c907065edf050a7d30a2307243f4117c22307d957c61b54b83122000cc493b0d'


def git_blob(content):
    return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()


class ReferenceMappingTests(unittest.TestCase):
    def test_all_baseline_files_have_unique_present_destinations_and_preserved_bytes(self):
        raw = (ROOT / MAP).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), MAP_SHA256,
                         'The reviewed migration inventory is immutable.')
        mapping = json.loads(raw)
        self.assertEqual(mapping['base_revision'], BASE)
        entries = mapping['entries']
        self.assertEqual(mapping['entry_count'], 495)
        self.assertEqual(len(entries), 495)
        self.assertEqual(len({item['old_path'] for item in entries}), 495)
        self.assertEqual(len({item['new_path'] for item in entries}), 495)
        self.assertEqual(sum(item['preserve_bytes'] for item in entries), 152)
        for item in entries:
            with self.subTest(old=item['old_path']):
                relative = Path(item['new_path'])
                self.assertFalse(relative.is_absolute())
                self.assertNotIn('..', relative.parts)
                path = ROOT / relative
                self.assertTrue(path.is_file(), str(relative))
                self.assertFalse(path.is_symlink(), str(relative))
                if item['preserve_bytes']:
                    content = path.read_bytes()
                    self.assertEqual(len(content), item['base_size'])
                    self.assertEqual(git_blob(content), item['base_blob'])
                if item['old_path'] != item['new_path']:
                    self.assertFalse((ROOT / item['old_path']).exists(), item['old_path'])

    def test_product_and_backbone_paths_have_distinct_ownership(self):
        for app in ('frontend', 'backend', 'automation'):
            for directory in ('src', 'tst'):
                self.assertTrue((ROOT / 'apps' / app / directory).is_dir())
        for directory in ('packages', 'contracts', 'tst', 'infra', 'config', 'scripts',
                          'docs/requirements', 'docs/architecture', '.vscode'):
            self.assertTrue((ROOT / directory).is_dir(), directory)
        for filename in ('requirements.txt', 'requirements.lock'):
            self.assertTrue((ROOT / '.engineering-backbone' / filename).is_file())
            self.assertFalse((ROOT / filename).exists())
        self.assertTrue((ROOT / 'infra/docker/engineering-backbone/Dockerfile').is_file())
        self.assertFalse((ROOT / 'Dockerfile').exists())


class DirectCopyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-reference-copy-')
        self.addCleanup(temporary.cleanup)
        self.destination = Path(temporary.name) / 'different-product-name'
        shutil.copytree(ROOT, self.destination, ignore=shutil.ignore_patterns(
            '.git', '.venv', 'venv', '__pycache__', 'node_modules', 'artifacts',
            '.pytest_cache', '.mypy_cache', 'dist', 'build'))
        # A raw copy needs only reviewed project facts, not Jinja or Copier.
        project_path = self.destination / '.engineering-backbone/project.json'
        project = json.loads(project_path.read_text())
        project['project']['name'] = 'different-product-name'
        project_path.write_text(json.dumps(project) + '\n')

    def validate(self, *, trusted_source=False):
        executable = ROOT / VALIDATOR if trusted_source else self.destination / VALIDATOR
        command = [sys.executable, '-I', str(executable), '--root', str(self.destination)]
        if trusted_source:
            command.extend(['--trusted-base', str(ROOT)])
        return subprocess.run(command, cwd=self.destination,
                              capture_output=True, text=True, timeout=60)

    def assert_valid(self, *, trusted_source=False):
        result = self.validate(trusted_source=trusted_source)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_invalid(self, fragment, *, trusted_source=False):
        result = self.validate(trusted_source=trusted_source)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(fragment, result.stdout + result.stderr)

    def test_copied_validator_runs_from_renamed_copy_without_git_or_rendering(self):
        self.assertFalse((self.destination / '.git').exists())
        self.assertTrue((self.destination / '.codex/agents/backbone-reviewer.toml').is_file())
        self.assertTrue((self.destination / '.opencode/agents/backbone-reviewer.md').is_file())
        self.assert_valid()
        self.assert_valid(trusted_source=True)

    def test_copy_rejects_policy_weakening_and_missing_canonical_policy(self):
        path = self.destination / '.engineering-backbone/core.json'
        original = path.read_bytes()
        policy = json.loads(original)
        policy['invariants']['human_merge_required'] = False
        path.write_text(json.dumps(policy))
        self.assert_invalid('human_merge_required')
        self.assert_invalid('human_merge_required', trusted_source=True)
        path.write_bytes(original)
        (self.destination / 'docs/agent-governance/core.md').unlink()
        self.assert_invalid('docs/agent-governance/core.md')

    def test_copy_rejects_native_reviewer_permission_escalation(self):
        path = self.destination / '.codex/agents/backbone-reviewer.toml'
        original = path.read_text()
        self.assertIn('sandbox_mode = "read-only"', original)
        path.write_text(original.replace('sandbox_mode = "read-only"',
                                         'sandbox_mode = "workspace-write"'))
        self.assert_invalid('read-only')
        self.assert_invalid('read-only', trusted_source=True)

    def test_candidate_map_cannot_relabel_current_document_as_historical(self):
        path = self.destination / 'README.md'
        path.write_text('[Missing current guide](missing-current-guide.md)\n')
        inventory = self.destination / MAP
        mapping = json.loads(inventory.read_text())
        entry = next(item for item in mapping['entries'] if item['new_path'] == 'README.md')
        entry.update(disposition='archive-history', preserve_bytes=True,
                     base_blob=git_blob(path.read_bytes()), base_size=path.stat().st_size)
        inventory.write_text(json.dumps(mapping))
        self.assert_invalid('broken local Markdown link missing-current-guide.md')
        self.assert_invalid('broken local Markdown link missing-current-guide.md', trusted_source=True)

    def test_candidate_map_cannot_authorize_changed_historical_bytes(self):
        inventory = self.destination / MAP
        mapping = json.loads(inventory.read_text())
        entry = next(item for item in mapping['entries']
                     if item['old_path'] == 'docs/reviews/bootstrap-result.md')
        path = self.destination / entry['new_path']
        path.write_bytes(path.read_bytes() + b'\nForged new historical approval.\n')
        entry.update(base_blob=git_blob(path.read_bytes()), base_size=path.stat().st_size)
        inventory.write_text(json.dumps(mapping))
        self.assert_invalid(entry['new_path'])
        self.assert_invalid(entry['new_path'], trusted_source=True)

    def test_new_change_task_and_links_remain_governed(self):
        directory = self.destination / 'docs/changes/product-change'
        directory.mkdir(parents=True)
        (directory / 'task-packet.json').write_text(json.dumps({'scope': {}}))
        (directory / 'review.md').write_text('[Missing current evidence](absent.txt)\n')
        self.assert_invalid('task-packet.json')
        self.assert_invalid('broken local Markdown link absent.txt')

    def test_historical_link_still_requires_its_relocated_target(self):
        (self.destination / 'docs/changes/backbone-bootstrap/reviews/bootstrap-triage.md').unlink()
        self.assert_invalid('bootstrap-triage.md')
        self.assert_invalid('bootstrap-triage.md', trusted_source=True)


if __name__ == '__main__':
    unittest.main()
