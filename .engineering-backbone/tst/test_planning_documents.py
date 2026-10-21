"""Exercise planning guidance distribution, updates and existing packet boundaries.

These are real copy/update and validation checks. They do not certify plan quality,
story independence, native instruction loading or assembled-system behavior.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from copier import run_update

from tst import test_copier as copier_tests


SOURCE_GUIDE = 'docs/agent-governance/planning.md'
SOURCE_PROVENANCE = 'docs/agent-governance/planning-sources.md'
SOURCE_TEMPLATES = 'docs/templates/planning'
INSTALLED_GUIDE = '.engineering-backbone/planning.md'
INSTALLED_PROVENANCE = '.engineering-backbone/planning-sources.md'
INSTALLED_TEMPLATES = '.engineering-backbone/planning-templates'
TEMPLATES = (
    'README.md', 'delivery-plan.md', 'delivery-item.md', 'decomposition.md',
    'review.md', 'project-mapping.md', 'worked-example.md',
)


def installed_guide_text(text):
    for source, destination in (
        ('(../../.engineering-backbone/schemas/', '(schemas/'),
        ('(../templates/examples/', '(examples/'),
        ('(../templates/architecture/', '(architecture-templates/'),
        ('(../templates/planning/', '(planning-templates/'),
        ('(../quality/policy.md', '(quality-policy.md'),
    ):
        text = text.replace(source, destination)
    return text.strip()


def installed_template_text(text):
    for source, destination in (
        ('(../../agent-governance/planning.md', '(../planning.md'),
        ('(../../agent-governance/planning-sources.md', '(../planning-sources.md'),
        ('(../../agent-governance/architecture.md', '(../architecture.md'),
        ('(../../agent-governance/core.md', '(../core.md'),
        ('(../../../.engineering-backbone/schemas/', '(../schemas/'),
        ('(../../quality/policy.md', '(../quality-policy.md'),
        ('(../architecture/', '(../architecture-templates/'),
    ):
        text = text.replace(source, destination)
    return text.strip()


class PlanningDocumentTests(unittest.TestCase):
    # Reuse real Copier fixtures without inheriting unrelated test methods.
    setUp = copier_tests.CopierTests.setUp
    copy = copier_tests.CopierTests.copy
    validation_result = copier_tests.CopierTests.validation_result
    validate = copier_tests.CopierTests.validate

    def assert_package(self, target):
        self.assertEqual(
            (target / INSTALLED_GUIDE).read_text().strip(),
            installed_guide_text((self.source / SOURCE_GUIDE).read_text()))
        self.assertEqual(
            (target / INSTALLED_PROVENANCE).read_text().strip(),
            (self.source / SOURCE_PROVENANCE).read_text().strip())
        self.assertEqual(
            {path.name for path in (target / INSTALLED_TEMPLATES).iterdir()},
            set(TEMPLATES))
        for name in TEMPLATES:
            with self.subTest(template=name):
                self.assertEqual(
                    (target / INSTALLED_TEMPLATES / name).read_text().strip(),
                    installed_template_text(
                        (self.source / SOURCE_TEMPLATES / name).read_text()))
        # The always-installed core reaches the kit even with all adapters off.
        self.assertIn('(planning.md)',
                      (target / '.engineering-backbone/core.md').read_text())
        for name in ('task-packet.json', 'requirement.json', 'review-evidence.json'):
            self.assertEqual(
                json.loads((target / '.engineering-backbone/examples' / name).read_text()),
                json.loads((self.source / 'docs/templates/examples' / name).read_text()),
                name)

    def test_copy_distributes_planning_without_creating_product_records(self):
        for selected in (False, True):
            with self.subTest(adapters_and_quality=selected):
                target = self.copy(use_codex=selected, use_copilot=selected,
                                   use_opencode=selected, use_quality_framework=selected)
                self.assert_package(target)
                for relative in ('docs/planning', 'docs/changes', 'docs/requirements',
                                 'docs/architecture', 'package.json', 'pyproject.toml'):
                    self.assertFalse((target / relative).exists(), relative)
                self.validate(target)

    def test_update_refreshes_managed_planning_and_preserves_project_ownership(self):
        target = self.copy()
        protected = {
            'docs/planning/delivery-plan.md': '# Local delivery plan\nKeep local decisions.\n',
            'docs/changes/local-feature/item.md': '# Local work item\nKeep local scope.\n',
            'docs/requirements/REQ-LOCAL.md': '# Local requirement\nKeep acceptance.\n',
            'docs/architecture/ADR-LOCAL.md': '# Local architecture\nKeep rationale.\n',
            'docs/templates/planning/local.md': '# Local template\nKeep extensions.\n',
        }
        for relative, content in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        for relative in ('AGENTS.md', '.github/copilot-instructions.md'):
            path = target / relative
            path.write_text(path.read_text() + '\nPreserve stricter local delivery gates.\n',
                            encoding='utf-8')
            protected[relative] = path.read_text()
        before = {relative: (target / relative).read_bytes() for relative in protected}
        copier_tests.initialize(target)
        copier_tests.commit(target, 'Project-owned planning and native instructions')
        for relative in (SOURCE_GUIDE, SOURCE_PROVENANCE,
                         SOURCE_TEMPLATES + '/delivery-item.md'):
            path = self.source / relative
            path.write_text(path.read_text() + '\nReviewed planning update fixture.\n',
                            encoding='utf-8')
        copier_tests.commit(self.source, 'Managed planning update fixture')
        copier_tests.git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True,
                   overwrite=True, skip_tasks=True)
        for relative, content in before.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assert_package(target)
        self.validate(target)

    def test_missing_managed_planning_context_is_rejected(self):
        target = self.copy(use_codex=False, use_copilot=False,
                           use_opencode=False, use_quality_framework=False)
        self.validate(target)
        for relative in (INSTALLED_GUIDE, INSTALLED_PROVENANCE,
                         INSTALLED_TEMPLATES + '/decomposition.md'):
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

    def test_direct_copy_requires_planning_contract_and_template_links(self):
        def validate_source():
            return subprocess.run(
                [sys.executable, str(self.source / '.engineering-backbone/src/validate.py'),
                 '--root', str(self.source)], cwd=self.source,
                capture_output=True, text=True)

        result = validate_source()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for relative in (SOURCE_GUIDE, SOURCE_TEMPLATES + '/delivery-item.md'):
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

    def test_planning_adoption_preserves_packet_review_and_schema_boundaries(self):
        target = self.copy(use_codex=False, use_copilot=False,
                           use_opencode=False, use_quality_framework=False)
        source_schema = self.source / '.engineering-backbone/schemas/task-packet.schema.json'
        installed_schema = target / '.engineering-backbone/schemas/task-packet.schema.json'
        self.assertEqual(json.loads(source_schema.read_text()),
                         json.loads(installed_schema.read_text()))
        packet_path = target / '.engineering-backbone/examples/task-packet.json'
        packet = json.loads(packet_path.read_text())
        # Synthetic fixture identities exercise structural state rules only.
        packet['repository']['base_revision'] = '1' * 40
        packet['repository']['head_revision'] = None
        packet['status'] = 'active'
        packet_path.write_text(json.dumps(packet), encoding='utf-8')
        self.validate(target)

        review = deepcopy(packet)
        review['status'] = 'ready_for_review'
        packet_path.write_text(json.dumps(review), encoding='utf-8')
        result = self.validation_result(target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('head_revision', result.stdout + result.stderr)

        review['repository']['head_revision'] = '2' * 40
        packet_path.write_text(json.dumps(review), encoding='utf-8')
        self.validate(target)
        review['integration_owner'] = 'unsupported-new-packet-field'
        packet_path.write_text(json.dumps(review), encoding='utf-8')
        result = self.validation_result(target)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('integration_owner', result.stdout + result.stderr)
        self.assertIn('Additional properties', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
