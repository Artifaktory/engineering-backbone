"""Execute the current quality gate against an approved historical consumer.

The historical eight-file tooling bundle remains untouched. These tests prove
that the workflow's own compiled authority closes an old validator's blind spot;
they do not execute candidate quality code or assert semantic certification.
"""
from __future__ import annotations

import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy
import yaml

from scripts.compile_toolchain_fingerprint import FILES, bundle_digest
from tests.test_workflows import commit, historical_source, initialize


ROOT = Path(__file__).resolve().parents[1]
PROFILE = '.engineering-backbone/quality-profile.json'
VALIDATE_STEP = 'Validate generated consumer with trusted tooling'
HEADERS = ('rule_id', 'requirement_id', 'risk', 'architecture', 'tests',
           'check_ids', 'evidence', 'status')


class QualityWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = tempfile.TemporaryDirectory(prefix='backbone-quality-workflow-source-')
        cls.addClassCleanup(fixture.cleanup)
        cls.fixture = Path(fixture.name)
        cls.source = cls.fixture / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', 'artifacts', '.venv'))
        initialize(cls.source)
        commit(cls.source, 'Reviewed quality workflow fixture')
        cls.rendered = cls.fixture / 'quality-consumer'
        run_copy(str(cls.source), cls.rendered, data={
            'use_quality_framework': True, 'use_workflow_kit': True,
        }, vcs_ref='HEAD', defaults=True, quiet=True, skip_tasks=True)
        cls.legacy_source = cls.fixture / 'historical-source'
        historical_source(cls.legacy_source, 'pre-attestation')
        cls.legacy = cls.fixture / 'historical-consumer'
        run_copy(str(cls.legacy_source), cls.legacy, defaults=True, quiet=True,
                 skip_tasks=True)
        workflow = yaml.safe_load((cls.source / '.github/workflows/governance-checks.yml').read_text())
        cls.step = next(step for step in workflow['jobs']['validate']['steps']
                        if step.get('name') == VALIDATE_STEP)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-quality-workflow-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.candidate = self.workspace / 'candidate'
        self.trusted = self.workspace / 'trusted-base'
        shutil.copytree(self.legacy, self.trusted)
        shutil.copytree(self.legacy, self.candidate)
        self.original_tooling = {
            name: (self.candidate / '.engineering-backbone' / name).read_bytes()
            for name in FILES
        }
        self.original_digest = bundle_digest(self.trusted)
        self.assertIn(self.original_digest, json.loads(self.step['env']['PREVIOUS_TOOLCHAIN_SHA256']))
        self.assertNotIn(b'quality_errors', self.original_tooling['validate.py'])
        # Copy only the new optional package and project-owned declarations,
        # never the current validator, schemas or dependency manifests.
        for relative in (
            PROFILE, '.engineering-backbone/quality-policy.md',
            '.engineering-backbone/quality-guide.md',
            '.engineering-backbone/quality-profile.schema.json',
            '.engineering-backbone/quality-guard.py',
            '.engineering-backbone/workflows.json',
        ):
            shutil.copyfile(self.rendered / relative, self.candidate / relative)
        for relative in ('.engineering-backbone/standards', 'docs/quality'):
            shutil.copytree(self.rendered / relative, self.candidate / relative)
        self.marker = self.workspace / 'candidate-quality-code-executed'
        (self.candidate / '.engineering-backbone/quality-guard.py').write_text(
            f'from pathlib import Path\nPath({str(self.marker)!r}).touch()\n'
            'raise RuntimeError("candidate quality module executed")\n', encoding='utf-8')

    def assert_tooling_unchanged(self):
        for root in (self.candidate, self.trusted):
            self.assertEqual(self.original_digest, bundle_digest(root))
            for name, content in self.original_tooling.items():
                self.assertEqual(content, (root / '.engineering-backbone' / name).read_bytes(), name)

    def validate(self):
        self.assert_tooling_unchanged()
        env = os.environ.copy()
        env.update({
            'GITHUB_WORKSPACE': str(self.workspace),
            'GITHUB_REPOSITORY': 'example/consumer',
            'EVENT_NAME': 'pull_request', 'SOURCE_MODE': 'false',
            'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH'],
        })
        env.update({key: value for key, value in self.step.get('env', {}).items()
                    if '${{' not in str(value)})
        return subprocess.run(['bash', '-c', self.step['run']], cwd=self.workspace,
                              env=env, capture_output=True, text=True)

    def old_validator(self):
        return subprocess.run([
            sys.executable, '-I', str(self.trusted / '.engineering-backbone/validate.py'),
            '--root', str(self.candidate), '--trusted-base', str(self.trusted),
        ], cwd=self.trusted, capture_output=True, text=True)

    def assert_quality_rejected(self, phrase=None):
        result = self.validate()
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn('Quality framework:', output)
        if phrase:
            self.assertIn(phrase, output)
        self.assertNotIn('candidate quality module executed', output)
        self.assertFalse(self.marker.exists())

    def test_valid_inactive_package_passes_without_executing_candidate_guard(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.marker.exists())
        self.assertNotIn('candidate quality module executed', result.stdout + result.stderr)

    def test_current_workflow_rejects_null_and_malformed_profile_old_validator_accepts(self):
        for content in ('null\n', '{"schema_version": "1",'):
            with self.subTest(content=content):
                (self.candidate / PROFILE).write_text(content, encoding='utf-8')
                old = self.old_validator()
                self.assertEqual(old.returncode, 0, old.stdout + old.stderr)
                self.assert_quality_rejected()

    def test_current_workflow_rejects_consumer_catalog_poisoning_old_validator_accepts(self):
        path = self.candidate / '.engineering-backbone/standards/rules.json'
        rules = json.loads(path.read_text())
        rules['rules'][0]['statement'] = 'Consumer substituted its own rule authority.'
        path.write_text(json.dumps(rules) + '\n', encoding='utf-8')
        old = self.old_validator()
        self.assertEqual(old.returncode, 0, old.stdout + old.stderr)
        self.assert_quality_rejected('Managed rules catalog differs from trusted authority')

    def test_first_activation_cannot_manufacture_a_reviewed_quality_seed(self):
        value = json.loads((self.candidate / PROFILE).read_text())
        value.update(enabled=True, backbone_ref='a' * 40,
                     checks=[{'rule_id': 'QUAL-TEST-001', 'check_ids': ['project-docs']}])
        (self.candidate / PROFILE).write_text(json.dumps(value) + '\n', encoding='utf-8')
        flow = {
            'schema_version': '1', 'enabled': True, 'profiles': ['docs'],
            'capabilities': [], 'runtimes': {}, 'checks': [{
                'id': 'project-docs', 'kind': 'docs',
                'argv': [sys.executable, '-c', 'raise SystemExit(31)'],
                'cwd': '.', 'timeout_seconds': 5, 'phases': ['pr'],
            }],
        }
        (self.candidate / '.engineering-backbone/workflows.json').write_text(
            json.dumps(flow) + '\n', encoding='utf-8')
        rules = json.loads((self.candidate / '.engineering-backbone/standards/profiles/baseline.json').read_text())
        buffer = io.StringIO(newline='')
        writer = csv.DictWriter(buffer, fieldnames=HEADERS)
        writer.writeheader()
        for rule_id in rules['rules']:
            writer.writerow({
                'rule_id': rule_id, 'requirement_id': 'REQ-1', 'risk': 'Incorrect behavior',
                'architecture': 'ADR-1', 'tests': 'Project verification declaration',
                'check_ids': 'project-docs' if rule_id == 'QUAL-TEST-001' else '',
                'evidence': '', 'status': 'planned',
            })
        (self.candidate / 'docs/quality/traceability.csv').write_text(buffer.getvalue(), encoding='utf-8')
        old = self.old_validator()
        self.assertEqual(old.returncode, 0, old.stdout + old.stderr)
        self.assert_quality_rejected('already reviewed inactive seed')


class QualityCompilerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-quality-compiler-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.source = self.workspace / 'source'
        (self.source / 'scripts').mkdir(parents=True)
        (self.source / '.github/workflows').mkdir(parents=True)
        shutil.copytree(ROOT / 'standards', self.source / 'standards')
        for relative in ('scripts/quality_framework.py', 'scripts/validate.py',
                         '.github/workflows/governance-checks.yml'):
            shutil.copyfile(ROOT / relative, self.source / relative)

    def compiler(self, mode):
        return subprocess.run([
            sys.executable, '-I', str(ROOT / 'scripts/compile_quality_framework.py'),
            mode, '--source', str(self.source),
        ], cwd=self.workspace, capture_output=True, text=True)

    def assert_compiler_ok(self, mode):
        result = self.compiler(mode)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_source_catalog_change_requires_refreshing_every_compiled_entry_point(self):
        self.assert_compiler_ok('--check')
        path = self.source / 'standards/rules.json'
        value = json.loads(path.read_text())
        value['rules'][0]['statement'] += ' Reviewed source fixture change.'
        path.write_text(json.dumps(value) + '\n', encoding='utf-8')
        stale = self.compiler('--check')
        self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
        for relative in ('scripts/quality_framework.py', 'scripts/validate.py',
                         '.github/workflows/governance-checks.yml'):
            self.assertIn(relative, stale.stdout)
        self.assert_compiler_ok('--write')
        self.assert_compiler_ok('--check')
        for relative in ('scripts/quality_framework.py', 'scripts/validate.py',
                         '.github/workflows/governance-checks.yml'):
            self.assertIn('Reviewed source fixture change.', (self.source / relative).read_text())

    def test_compilation_never_imports_quality_engine_module_code(self):
        marker = self.workspace / 'quality-engine-module-executed'
        path = self.source / 'scripts/quality_framework.py'
        content = path.read_text()
        injected = (f'from pathlib import Path\nPath({str(marker)!r}).touch()\n'
                    'raise RuntimeError("quality engine module imported")\n\n')
        self.assertEqual(content.count('def quality_errors('), 1)
        path.write_text(content.replace('def quality_errors(', injected + 'def quality_errors(', 1), encoding='utf-8')
        self.assert_compiler_ok('--write')
        self.assert_compiler_ok('--check')
        self.assertFalse(marker.exists())
        self.assertIn('quality engine module imported', path.read_text())

    def test_compiler_detects_and_repairs_independent_entry_point_drift(self):
        for relative, indent in (('scripts/validate.py', ''),
                                 ('.github/workflows/governance-checks.yml', '          ')):
            with self.subTest(relative=relative):
                path = self.source / relative
                original = path.read_text()
                marker = indent + '# BEGIN COMPILED QUALITY GUARD\n'
                self.assertEqual(original.count(marker), 1)
                path.write_text(original.replace(marker, marker + indent + '# Stale compiled fixture.\n', 1),
                                encoding='utf-8')
                stale = self.compiler('--check')
                self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
                self.assertIn(relative, stale.stdout)
                self.assert_compiler_ok('--write')
                self.assert_compiler_ok('--check')
                self.assertEqual(original, path.read_text())


if __name__ == '__main__':
    unittest.main()
