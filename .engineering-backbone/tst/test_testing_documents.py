"""Real testing-contract copies, protected updates and missing-context rejection.

These checks qualify distribution and existing structural boundaries. They do not
establish semantic test adequacy, authentic execution evidence or CI activation.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from copier import run_update

from tst import test_copier as copier_tests


GUIDES = {
    'testing.md': 'docs/quality/testing.md',
    'testing-sources.md': 'docs/quality/testing-sources.md',
    'ci-cd.md': 'docs/quality/ci-cd.md',
}
SOURCE_TEMPLATES = 'docs/templates/testing'
INSTALLED_ROOT = '.engineering-backbone'
INSTALLED_TEMPLATES = INSTALLED_ROOT + '/testing-templates'
TEMPLATES = (
    'README.md', 'test-strategy.md', 'test-design.md', 'test-run.md',
    'test-completion.md', 'ci-mapping.md', 'review.md', 'worked-example.md',
)
QUALITY_DOCUMENTS = (
    'docs/quality/quality-plan.md', 'docs/quality/test-strategy.md',
    'docs/quality/traceability.csv', 'docs/quality/exceptions.md',
)


def installed_guide_text(text):
    for source, destination in (
        ('(../../.engineering-backbone/schemas/', '(schemas/'),
        ('(../templates/examples/', '(examples/'),
        ('(../templates/testing/', '(testing-templates/'),
        ('(../templates/architecture/', '(architecture-templates/'),
        ('(../templates/planning/', '(planning-templates/'),
        ('(../agent-governance/', '('),
        ('(policy.md)', '(quality-policy.md)'),
        ('(dependencies.md)', '(dependency-policy.md)'),
    ):
        text = text.replace(source, destination)
    return text.strip()


def installed_template_text(text):
    for source, destination in (
        ('(../../../.engineering-backbone/schemas/', '(../schemas/'),
        ('(../../quality/testing.md', '(../testing.md'),
        ('(../../quality/testing-sources.md', '(../testing-sources.md'),
        ('(../../quality/ci-cd.md', '(../ci-cd.md'),
        ('(../../quality/policy.md', '(../quality-policy.md'),
        ('(../../quality/dependencies.md', '(../dependency-policy.md'),
        ('(../../agent-governance/core.md', '(../core.md'),
        ('(../../agent-governance/architecture.md', '(../architecture.md'),
        ('(../../agent-governance/planning.md', '(../planning.md'),
        ('(../architecture/', '(../architecture-templates/'),
        ('(../planning/', '(../planning-templates/'),
    ):
        text = text.replace(source, destination)
    return text.strip()


class TestingDocumentTests(unittest.TestCase):
    # Reuse real fixtures without inheriting the unrelated Copier test methods.
    setUp = copier_tests.CopierTests.setUp
    copy = copier_tests.CopierTests.copy
    validation_result = copier_tests.CopierTests.validation_result
    validate = copier_tests.CopierTests.validate

    def assert_package(self, target):
        for installed, source in GUIDES.items():
            with self.subTest(guide=installed):
                expected = (self.source / source).read_text(encoding='utf-8')
                self.assertEqual(
                    (target / INSTALLED_ROOT / installed).read_text(encoding='utf-8').strip(),
                    installed_guide_text(expected))
        self.assertEqual(
            {path.name for path in (target / INSTALLED_TEMPLATES).iterdir()},
            set(TEMPLATES))
        for name in TEMPLATES:
            with self.subTest(template=name):
                self.assertEqual(
                    (target / INSTALLED_TEMPLATES / name).read_text(encoding='utf-8').strip(),
                    installed_template_text(
                        (self.source / SOURCE_TEMPLATES / name).read_text(encoding='utf-8')))
        core = (target / INSTALLED_ROOT / 'core.md').read_text(encoding='utf-8')
        self.assertIn('(testing.md)', core)
        self.assertIn('(ci-cd.md)', core)

    def test_copy_distributes_context_without_activating_optional_packages(self):
        for quality, workflow in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(quality=quality, workflow=workflow):
                target = self.copy(
                    use_codex=quality, use_copilot=quality, use_opencode=workflow,
                    use_quality_framework=quality, use_workflow_kit=workflow,
                    workflow_kit_ref='')
                self.assert_package(target)
                self.validate(target)
                quality_profile = target / INSTALLED_ROOT / 'quality-profile.json'
                workflow_profile = target / INSTALLED_ROOT / 'workflows.json'
                self.assertEqual(quality_profile.exists(), quality)
                self.assertEqual(workflow_profile.exists(), workflow)
                if quality:
                    self.assertFalse(json.loads(quality_profile.read_text())['enabled'])
                else:
                    for relative in QUALITY_DOCUMENTS:
                        self.assertFalse((target / relative).exists(), relative)
                if workflow:
                    self.assertFalse(json.loads(workflow_profile.read_text())['enabled'])
                for relative in (
                    'docs/testing', 'docs/changes', 'docs/templates/testing',
                    'package.json', 'pyproject.toml',
                    '.github/workflows/backbone-pr-checks.yml',
                    '.github/workflows/backbone-maintenance.yml',
                    '.github/workflows/backbone-release.yml',
                    '.github/workflows/backbone-deploy.yml',
                ):
                    self.assertFalse((target / relative).exists(), relative)

    def test_update_refreshes_managed_context_preserving_project_evidence_and_workflows(self):
        target = self.copy(use_quality_framework=True, use_workflow_kit=True)
        protected = {
            'docs/quality/quality-plan.md': '# Local quality plan\nKeep local decisions.\n',
            'docs/quality/test-strategy.md': '# Local test strategy\nKeep actual coverage.\n',
            'docs/quality/traceability.csv': (
                'rule_id,requirement_id,risk,architecture,tests,check_ids,evidence,status\n'
                'QUAL-TEST-001,REQ-LOCAL,Local risk,ADR-LOCAL,TEST-LOCAL,,,planned\n'),
            'docs/quality/exceptions.md': '# Local exceptions\nNo exception is granted.\n',
            'docs/testing/run-local.md': '# Local run\nNot executed.\n',
            'docs/templates/testing/local.md': '# Local template\nKeep extensions.\n',
            '.github/workflows/project-tests.yml': (
                'name: Local checks\non: workflow_dispatch\njobs: {}\n'),
        }
        for relative, content in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        for relative in ('AGENTS.md', '.github/copilot-instructions.md'):
            path = target / relative
            path.write_text(path.read_text() + '\nPreserve stricter local test gates.\n',
                            encoding='utf-8')
            protected[relative] = path.read_text()
        for relative in (INSTALLED_ROOT + '/quality-profile.json',
                         INSTALLED_ROOT + '/workflows.json'):
            protected[relative] = (target / relative).read_text()
        before = {relative: (target / relative).read_bytes() for relative in protected}
        copier_tests.initialize(target)
        copier_tests.commit(target, 'Project-owned testing, evidence and workflow')
        for relative in tuple(GUIDES.values()) + (SOURCE_TEMPLATES + '/test-run.md',):
            path = self.source / relative
            path.write_text(path.read_text() + '\nReviewed testing update fixture.\n',
                            encoding='utf-8')
        copier_tests.commit(self.source, 'Managed testing context update fixture')
        copier_tests.git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True,
                   overwrite=True, skip_tasks=True)
        for relative, content in before.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assert_package(target)
        self.validate(target)

    def test_rendered_copy_rejects_missing_required_testing_context(self):
        target = self.copy(use_codex=False, use_copilot=False, use_opencode=False,
                           use_quality_framework=False, use_workflow_kit=False)
        self.validate(target)
        for relative in tuple(INSTALLED_ROOT + '/' + name for name in GUIDES) + (
                INSTALLED_TEMPLATES + '/test-design.md',
                INSTALLED_TEMPLATES + '/ci-mapping.md'):
            with self.subTest(missing=relative):
                path = target / relative
                content = path.read_bytes()
                path.unlink()
                try:
                    result = self.validation_result(target)
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('broken local Markdown link', result.stdout + result.stderr)
                    self.assertIn(Path(relative).name, result.stdout + result.stderr)
                finally:
                    path.write_bytes(content)

    def test_direct_source_copy_rejects_missing_contract_and_verification_records(self):
        def validate_source():
            return subprocess.run(
                [sys.executable, str(self.source / '.engineering-backbone/src/validate.py'),
                 '--root', str(self.source)], cwd=self.source,
                capture_output=True, text=True)

        baseline = validate_source()
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
        for relative in tuple(GUIDES.values()) + (
                SOURCE_TEMPLATES + '/test-run.md', SOURCE_TEMPLATES + '/test-completion.md'):
            with self.subTest(missing=relative):
                path = self.source / relative
                content = path.read_bytes()
                path.unlink()
                try:
                    result = validate_source()
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('broken local Markdown link', result.stdout + result.stderr)
                    self.assertIn(Path(relative).name, result.stdout + result.stderr)
                finally:
                    path.write_bytes(content)

    def test_document_adoption_does_not_expand_json_states_or_workflow_phases(self):
        target = self.copy(use_codex=False, use_copilot=False, use_quality_framework=False,
                           use_workflow_kit=True)
        self.validate(target)
        requirement_path = target / INSTALLED_ROOT / 'examples/requirement.json'
        requirement = json.loads(requirement_path.read_text())
        for unsupported in ('error', 'skipped'):
            with self.subTest(requirement_state=unsupported):
                changed = deepcopy(requirement)
                changed['verification']['status'] = unsupported
                requirement_path.write_text(json.dumps(changed), encoding='utf-8')
                result = self.validation_result(target)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('verification.status', result.stdout + result.stderr)
        requirement_path.write_text(json.dumps(requirement), encoding='utf-8')
        packet_path = target / INSTALLED_ROOT / 'examples/task-packet.json'
        packet = json.loads(packet_path.read_text())
        changed = deepcopy(packet)
        changed['acceptance'][0]['status'] = 'not_run'
        packet_path.write_text(json.dumps(changed), encoding='utf-8')
        result = self.validation_result(target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('acceptance.0.status', result.stdout + result.stderr)
        packet_path.write_text(json.dumps(packet), encoding='utf-8')

        workflow_path = target / INSTALLED_ROOT / 'workflows.json'
        workflow = json.loads(workflow_path.read_text())
        workflow['checks'] = [{
            'id': 'selected-test', 'kind': 'test', 'argv': [sys.executable, '-V'],
            'cwd': '.', 'timeout_seconds': 5, 'phases': ['pr'],
        }]
        workflow_path.write_text(json.dumps(workflow), encoding='utf-8')
        self.validate(target)
        workflow['checks'][0]['phases'] = ['release']
        workflow_path.write_text(json.dumps(workflow), encoding='utf-8')
        result = self.validation_result(target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('workflow kit:', result.stdout + result.stderr)
        self.assertIn('Check kind does not support selected phases',
                      result.stdout + result.stderr)
        workflow['checks'][0]['phases'] = ['pr']
        workflow_path.write_text(json.dumps(workflow), encoding='utf-8')
        self.validate(target)


if __name__ == '__main__':
    unittest.main()
