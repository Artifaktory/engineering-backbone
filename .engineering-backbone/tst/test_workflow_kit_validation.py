"""Current source and copied validators enforce the optional kit contract."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy

ROOT = Path(__file__).resolve().parents[2]


class WorkflowKitValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='backbone-kit-validation-')
        cls.addClassCleanup(cls.fixture.cleanup)
        cls.source = Path(cls.fixture.name) / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', 'artifacts', '.venv'))
        # Real Git distribution omits empty local scaffolding directories.
        for arguments in (('init', '-b', 'main'),
                          ('config', 'user.name', 'Workflow validation fixture'),
                          ('config', 'user.email', 'validation@example.invalid'),
                          ('add', '.'), ('commit', '-m', 'Reviewed source fixture')):
            subprocess.run(['git', *arguments], cwd=cls.source, check=True,
                           capture_output=True, text=True)
        cls.original = Path(cls.fixture.name) / 'consumer'
        run_copy(str(cls.source), cls.original, data={'use_workflow_kit': True,
            'workflow_kit_ref': 'a' * 40}, defaults=True, quiet=True, skip_tasks=True,
            vcs_ref='HEAD')

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='backbone-kit-validate-case-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'candidate'
        shutil.copytree(self.original, self.root)

    def validate(self, trusted=None):
        command = [sys.executable, '-I', str(self.root / '.engineering-backbone/validate.py'),
                   '--root', str(self.root)]
        if trusted is not None:
            command += ['--trusted-base', str(trusted)]
        return subprocess.run(command, cwd=self.root, capture_output=True, text=True,
                              env=os.environ.copy())

    def test_generated_inactive_seed_is_valid_and_not_executed(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_current_validator_rejects_malformed_and_removed_kit(self):
        config = self.root / '.engineering-backbone/workflows.json'
        config.write_text('{"schema_version":"1","enabled":true}\n')
        self.assertNotEqual(self.validate().returncode, 0)
        config.unlink()
        result = self.validate(self.original)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cannot be removed', result.stdout + result.stderr)

    def test_integrated_validation_rejects_present_candidate_and_base_null(self):
        path = self.root / '.engineering-backbone/workflows.json'
        path.write_text('null\n')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('workflow kit:', result.stderr)
        self.assertNotIn('PASS: structural', result.stdout)
        shutil.copyfile(self.original / '.engineering-backbone/workflows.json', path)
        base = Path(self.temporary.name) / 'null-base'
        shutil.copytree(self.original, base)
        (base / '.engineering-backbone/workflows.json').write_text('null\n')
        result = self.validate(base)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('workflow kit:', result.stderr)
        self.assertNotIn('PASS: structural', result.stdout)

    def test_both_managed_callers_reject_unpinned_and_write_permissions(self):
        for name in ('backbone-pr-checks.yml', 'backbone-maintenance.yml'):
            path = self.root / '.github/workflows' / name
            original = path.read_text()
            for content in (original.replace('@' + 'a' * 40, '@main'),
                            original.replace('contents: read', 'contents: write')):
                with self.subTest(name=name, content=content):
                    path.write_text(content)
                    result = self.validate()
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            path.write_text(original)

    def test_managed_caller_links_do_not_inspect_external_files(self):
        path = self.root / '.github/workflows/backbone-pr-checks.yml'
        path.unlink()
        external = Path(self.temporary.name) / 'outside.yml'
        external.write_text('external caller bytes remain untouched\n')
        path.symlink_to(external)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no symlink ancestors', result.stdout + result.stderr)
        self.assertEqual(external.read_text(), 'external caller bytes remain untouched\n')
