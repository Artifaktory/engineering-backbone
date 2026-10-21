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

from tst.test_source_layout_compatibility import archived_records


ROOT = Path(__file__).resolve().parents[2]
MAP = 'docs/changes/backbone-layout/layout-map.json'
VALIDATOR = '.engineering-backbone/src/validate.py'
BASE = '212608aa50ee517b3dd3107a9480da997222fd4f'
MAP_SHA256 = 'c907065edf050a7d30a2307243f4117c22307d957c61b54b83122000cc493b0d'


def git_blob(content):
    return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def assert_reference_ownership(case, root):
    """Product/IDE folders are optional; retained tooling has canonical paths."""
    for app in ('frontend', 'backend', 'automation'):
        component = root / 'apps' / app
        if component.exists():
            case.assertTrue(component.is_dir(), str(component))
            for directory in ('src', 'tst'):
                case.assertTrue((component / directory).is_dir(), str(component / directory))
    for directory in ('packages', 'contracts', 'tst', 'config', 'scripts',
                      'docs/requirements', 'docs/architecture', '.vscode'):
        path = root / directory
        if path.exists():
            case.assertTrue(path.is_dir(), directory)
    for filename in ('requirements.txt', 'requirements.lock'):
        case.assertTrue((root / '.engineering-backbone' / filename).is_file())
    case.assertTrue((root / 'infra/docker/engineering-backbone/Dockerfile').is_file())


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

    def test_product_and_backbone_paths_have_distinct_ownership(self):
        assert_reference_ownership(self, ROOT)


class ReferenceCheckoutTests(unittest.TestCase):
    def test_fresh_autocrlf_checkout_preserves_archives_and_nested_fixture_contract(self):
        with tempfile.TemporaryDirectory(prefix='backbone-reference-checkout-') as temporary:
            workspace = Path(temporary)
            seed = workspace / 'seed'
            checkout = workspace / 'checkout'
            shutil.copytree(ROOT, seed, ignore=shutil.ignore_patterns(
                '.git', '.venv', 'venv', '__pycache__', 'node_modules', 'artifacts',
                '.pytest_cache', '.mypy_cache', 'dist', 'build'))

            def git(directory, *args):
                return subprocess.run(['git', *args], cwd=directory, check=True,
                                      capture_output=True, text=True, timeout=60).stdout

            git(seed, '-c', 'init.defaultBranch=main', 'init')
            git(seed, 'config', 'user.name', 'Archive checkout fixture')
            git(seed, 'config', 'user.email', 'archive-checkout@example.invalid')
            git(seed, 'config', 'core.autocrlf', 'false')
            git(seed, 'add', '.')
            git(seed, 'commit', '-m', 'Exact integration fixture for fresh checkout')
            git(workspace, 'clone', '--no-local', '--no-checkout', str(seed), str(checkout))
            git(checkout, 'config', 'core.autocrlf', 'true')
            git(checkout, 'checkout', '-f', 'HEAD')
            self.assertEqual(git(checkout, 'config', '--get', 'core.autocrlf').strip(), 'true')
            archive = archived_records()
            self.assertEqual(len(archive), 88)
            for relative, expected in archive.items():
                with self.subTest(archive=relative):
                    actual = (checkout / relative).read_bytes()
                    self.assertEqual(hashlib.sha256(actual).hexdigest(), hashlib.sha256(expected).hexdigest())
                    self.assertNotIn(b'\r\n', actual)
            # The original 88-document archive is only part of the relocation
            # contract. Check every byte-preserved input, including inventories,
            # the core policy JSON and nested manifest, against immutable blobs.
            mapping_bytes = (ROOT / MAP).read_bytes()
            self.assertEqual(hashlib.sha256(mapping_bytes).hexdigest(), MAP_SHA256)
            preserved = [entry for entry in json.loads(mapping_bytes)['entries']
                         if entry['preserve_bytes']]
            self.assertEqual(len(preserved), 152)
            for entry in preserved:
                with self.subTest(preserved=entry['new_path']):
                    actual = (checkout / entry['new_path']).read_bytes()
                    self.assertEqual(len(actual), entry['base_size'])
                    self.assertEqual(git_blob(actual), entry['base_blob'])
            fixture_root = '.engineering-backbone/tst/fixtures/historical'
            for path in (ROOT / fixture_root).rglob('*'):
                if path.is_file():
                    relative = path.relative_to(ROOT)
                    with self.subTest(nested_fixture=relative.as_posix()):
                        self.assertEqual((checkout / relative).read_bytes(), path.read_bytes())
            archived = 'docs/changes/backbone-bootstrap/plans/bootstrap-task.json'
            nested = fixture_root + '/bootstrap/policy/core.md'
            attributes = git(checkout, 'check-attr', 'text', 'eol', 'filter',
                             'working-tree-encoding', '--', archived, nested)
            for attribute, value in (('text', 'set'), ('eol', 'lf'), ('filter', 'unset'),
                                     ('working-tree-encoding', 'unset')):
                self.assertIn(archived + ': ' + attribute + ': ' + value, attributes)
            for attribute in ('text', 'filter', 'working-tree-encoding'):
                self.assertIn(nested + ': ' + attribute + ': unset', attributes)
            result = subprocess.run([sys.executable, '-I', str(checkout / VALIDATOR),
                                     '--root', str(checkout)], cwd=checkout,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


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

    def test_optional_product_and_ide_folders_can_be_omitted(self):
        for relative in ('apps/frontend', '.vscode'):
            path = self.destination / relative
            if path.exists():
                shutil.rmtree(path)
            self.assertFalse(path.exists(), relative)
        self.assert_valid()
        self.assert_valid(trusted_source=True)
        assert_reference_ownership(self, self.destination)

    def test_product_json_and_schema_fixtures_remain_product_owned(self):
        # Names reserved within engineering paths have no governance meaning
        # within product components or the new layout's root product examples.
        fixtures = {
            'apps/backend/tst/examples/request.json': '{"value": 1}\n',
            'apps/backend/tst/tasks/task-packet.json': '{"scope": {}}\n',
            'packages/client/tst/reviews/review-evidence.json': '{"reviewers": []}\n',
            'tst/requirements/request.json': '{"statement": "fixture"}\n',
            'contracts/examples/invalid.schema.json': '{"type": "made-up"}\n',
            'examples/malformed.json': '{"unterminated":\n',
        }
        for relative, content in fixtures.items():
            path = self.destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        self.assert_valid()
        self.assert_valid(trusted_source=True)

    def test_pruned_copy_can_execute_its_ownership_and_pruning_regressions(self):
        for relative in ('apps/frontend', '.vscode'):
            path = self.destination / relative
            if path.exists():
                shutil.rmtree(path)
            self.assertFalse(path.exists(), relative)
        result = subprocess.run([
            sys.executable, '-m', 'unittest',
            'tst.test_reference_layout.ReferenceMappingTests',
            'tst.test_reference_layout.DirectCopyTests.test_optional_product_and_ide_folders_can_be_omitted',
            '-v',
        ], cwd=self.destination / '.engineering-backbone',
            capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_root_build_inputs_are_independent_of_backbone_tooling(self):
        (self.destination / 'requirements.txt').write_text('project-runtime==1.0.0\n')
        (self.destination / 'requirements.lock').write_text(
            'project-runtime==1.0.0 --hash=sha256:' + 'a' * 64 + '\n')
        (self.destination / 'Dockerfile').write_text('FROM scratch\n')
        self.assert_valid()
        self.assert_valid(trusted_source=True)
        result = subprocess.run([
            sys.executable, '-m', 'unittest',
            'tst.test_reference_layout.ReferenceMappingTests', '-v',
        ], cwd=self.destination / '.engineering-backbone',
            capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        # Root application manifests do not replace or relax the actual tooling
        # bundle: its own direct/resolved dependency mismatch still rejects.
        manifest = self.destination / '.engineering-backbone/requirements.txt'
        original = manifest.read_text()
        self.assertIn('jsonschema==4.26.0', original)
        manifest.write_text(original.replace('jsonschema==4.26.0', 'jsonschema==999.0.0'))
        self.assert_invalid('dependency lock mismatch')
        self.assert_invalid('dependency lock mismatch', trusted_source=True)

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
