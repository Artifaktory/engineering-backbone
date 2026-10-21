"""Exercise source dependency failure paths in real Git fixtures."""
from __future__ import annotations

import importlib.metadata
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

from src import check_source_dependencies as source


ROOT = Path(__file__).resolve().parents[2]


class SourceDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-dependencies-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init')
        for name in source.REQUIRED_PATHS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Tracked source fixture.\n', encoding='utf-8')
        (self.root / 'infra/docker/engineering-backbone/Dockerfile').write_text(
            'FROM python:3.12-bookworm@sha256:' + 'a' * 64 + '\n')
        self.set_requirements('Example_Package==1.2.3\n',
                              'example-package==1.2.3 --hash=sha256:' + 'b' * 64 + '\n')
        self.git('add', '--', *source.REQUIRED_PATHS)

    def git(self, *argv):
        return subprocess.run(['git', *argv], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout

    def set_requirements(self, direct, locked):
        (self.root / '.engineering-backbone/requirements.txt').write_text(direct, encoding='utf-8')
        (self.root / '.engineering-backbone/requirements.lock').write_text(locked, encoding='utf-8')

    def test_tracked_inputs_and_normalized_direct_pins_pass(self):
        self.assertEqual(source.check_inputs(self.root), {'example-package': '1.2.3'})

    def test_missing_untracked_and_empty_required_files_fail(self):
        for name in ('infra/docker/engineering-backbone/Dockerfile', 'docs/quality/dependencies.md', 'docs/operations/engineering/dependency-compatibility.md'):
            with self.subTest(name=name):
                path = self.root / name
                content = path.read_bytes()
                path.unlink()
                with self.assertRaisesRegex(source.DependencyError, 'missing, empty'):
                    source.check_inputs(self.root)
                path.write_bytes(b'\n')
                with self.assertRaisesRegex(source.DependencyError, 'missing, empty'):
                    source.check_inputs(self.root)
                path.write_bytes(content)
                self.git('rm', '--cached', '-f', '--', name)
                with self.assertRaisesRegex(source.DependencyError, 'not Git-tracked'):
                    source.check_inputs(self.root)
                self.git('add', '--', name)

    def test_required_file_or_parent_symlink_fails(self):
        path = self.root / 'docs/quality/dependencies.md'
        alternate = self.root / 'alternate-policy.md'
        path.rename(alternate)
        path.symlink_to(alternate)
        with self.assertRaisesRegex(source.DependencyError, 'symlinked required input'):
            source.check_inputs(self.root)
        path.unlink()
        alternate.rename(path)
        directory = self.root / 'docs/quality'
        alternate = self.root / 'alternate-policy'
        directory.rename(alternate)
        directory.symlink_to(alternate, target_is_directory=True)
        with self.assertRaisesRegex(source.DependencyError, 'symlinked required input'):
            source.check_inputs(self.root)

    def test_git_index_symlink_cannot_be_hidden_by_regular_worktree_file(self):
        path = self.root / 'docs/quality/dependencies.md'
        path.unlink()
        path.symlink_to('../../AGENTS.md')
        self.git('add', '--', 'docs/quality/dependencies.md')
        path.unlink()
        path.write_text('A regular worktree file masks a staged symlink.\n')
        with self.assertRaisesRegex(source.DependencyError, 'non-regular or conflicted tracked input'):
            source.check_inputs(self.root)

    def test_non_git_or_nested_source_root_fails(self):
        shutil.rmtree(self.root / '.git')
        with self.assertRaisesRegex(source.DependencyError, 'Git checkout root'):
            source.check_inputs(self.root)

    def test_mutable_wrong_runtime_and_additional_bases_fail(self):
        for value in ('FROM python:3.12-bookworm\n',
                      'FROM python:3.13-bookworm@sha256:' + 'a' * 64 + '\n',
                      'FROM python:3.12-bookworm@sha256:invalid\n',
                      'ARG BASE=python:3.12-bookworm\nFROM ${BASE}\n',
                      'FROM python:3.12-bookworm@sha256:' + 'a' * 64 + '\nFROM alpine\n'):
            with self.subTest(value=value):
                (self.root / 'infra/docker/engineering-backbone/Dockerfile').write_text(value)
                with self.assertRaisesRegex(source.DependencyError, 'immutable Python 3.12'):
                    source.check_inputs(self.root)

    def test_missing_or_mismatched_direct_resolution_fails(self):
        for direct in ('example-package==1.2.4\n', 'missing-package==1.2.3\n'):
            with self.subTest(direct=direct):
                (self.root / '.engineering-backbone/requirements.txt').write_text(direct)
                with self.assertRaisesRegex(source.DependencyError, 'direct pin and locked resolution differ'):
                    source.check_inputs(self.root)

    def test_hash_continuations_and_existing_source_resolution(self):
        lock = '# generated\nExample==1.2.3 \\\n    --hash=sha256:' + 'b' * 64 + ' \\\n    --hash=sha256:' + 'c' * 64 + '\n    # via direct\n'
        self.assertEqual(source.parse_pins(lock, hashed=True), {'example': '1.2.3'})
        actual = source.parse_pins((ROOT / '.engineering-backbone/requirements.lock').read_text(), hashed=True)
        direct = source.parse_pins((ROOT / '.engineering-backbone/requirements.txt').read_text(), hashed=False)
        self.assertGreater(len(actual), len(direct))
        self.assertTrue(all(actual[name] == value for name, value in direct.items()))

    def test_unsupported_or_ambiguous_requirements_fail_closed(self):
        for value, hashed in (
            ('example>=1\n', False), ('example==1.*\n', False),
            ('example==1 --extra-index-url https://example.invalid\n', False),
            ('example==1; python_version < "3.13"\n', False),
            ('example==1\n', True),
            ('example==1 --hash=sha256:invalid\n', True),
            ('example==1 --hash=sha256:' + 'b' * 64 + ' --no-deps\n', True),
            ('Example_Package==1\nexample-package==1\n', False),
            ('example==1 \\\n', True),
            ('example==1 \\\n# interrupted\n', True),
            ('# no packages\n', False),
        ):
            with self.subTest(value=value, hashed=hashed):
                with self.assertRaises(source.DependencyError):
                    source.parse_pins(value, hashed=hashed)

    def test_installed_mismatch_or_missing_package_fails_before_pip(self):
        for outcome in ('9.9', importlib.metadata.PackageNotFoundError('example')):
            with self.subTest(outcome=outcome), patch.object(source.importlib.metadata, 'version') as version:
                if isinstance(outcome, Exception):
                    version.side_effect = outcome
                else:
                    version.return_value = outcome
                with patch.object(source.subprocess, 'run') as run:
                    with self.assertRaises(source.DependencyError):
                        source.check_installed({'example': '1.2.3'})
                    run.assert_not_called()

    def test_declared_dependency_conflict_fails(self):
        with patch.object(source.importlib.metadata, 'version', return_value='1.2.3'):
            with patch.object(source.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 1, 'example requires incompatible dependency', '')):
                with self.assertRaisesRegex(source.DependencyError, 'metadata is inconsistent'):
                    source.check_installed({'example': '1.2.3'})

    def test_actual_source_resolution_checks_in_real_git_fixture(self):
        for name in ('.engineering-backbone/requirements.txt', '.engineering-backbone/requirements.lock'):
            shutil.copy2(ROOT / name, self.root / name)
        result = subprocess.run([sys.executable, str(ROOT / '.engineering-backbone/src/check_source_dependencies.py'),
                                 '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('installed locked versions and declared dependency consistency', result.stdout)
        self.git('rm', '--cached', '-f', '--', 'infra/docker/engineering-backbone/Dockerfile')
        result = subprocess.run([sys.executable, str(ROOT / '.engineering-backbone/src/check_source_dependencies.py'),
                                 '--root', str(self.root)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('not Git-tracked: infra/docker/engineering-backbone/Dockerfile', result.stderr)

    def test_ci_runs_tracking_before_real_image_build_and_offline_smoke(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/quality.yml').read_text())
        job = workflow['jobs']['source-dependencies']
        self.assertEqual(job['runs-on'], ['self-hosted', 'Linux', 'X64', 'backbone-ci'])
        steps = job['steps']
        scripts = [step.get('run', '') for step in steps]
        tracking = next(i for i, script in enumerate(scripts) if 'check_source_dependencies.py' in script)
        build = next(i for i, script in enumerate(scripts) if 'docker build ' in script)
        smoke = next(i for i, script in enumerate(scripts) if 'docker run ' in script)
        self.assertLess(tracking, build)
        self.assertLess(build, smoke)
        self.assertIn('--require-hashes --only-binary=:all:', scripts[tracking])
        self.assertIn('--file infra/docker/engineering-backbone/Dockerfile .', scripts[build])
        self.assertIn('--network none', scripts[smoke])
        self.assertIn('python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_copier.py -v', scripts[smoke])
        self.assertNotIn('continue-on-error', job)
        self.assertTrue(all('continue-on-error' not in step for step in steps))


if __name__ == '__main__':
    unittest.main()
