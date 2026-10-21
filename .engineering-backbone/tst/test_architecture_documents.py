"""Exercise actual architecture-guide distribution, updates and broken links.

These checks establish delivery and link integrity, not architectural fitness,
human approval, model instruction loading or project behavior.
"""
from pathlib import Path
import subprocess
import sys
import unittest

from copier import run_update

from tst import test_copier as copier_tests


SOURCE_GUIDE = 'docs/agent-governance/architecture.md'
SOURCE_PROVENANCE = 'docs/agent-governance/architecture-sources.md'
SOURCE_TEMPLATES = 'docs/templates/architecture'
INSTALLED_GUIDE = '.engineering-backbone/architecture.md'
INSTALLED_PROVENANCE = '.engineering-backbone/architecture-sources.md'
INSTALLED_TEMPLATES = '.engineering-backbone/architecture-templates'
TEMPLATES = (
    'README.md', 'architecture.md', 'decision.md', 'quality-scenario.md',
    'traceability.md', 'review.md', 'project-mapping.md', 'worked-example.md',
)


class ArchitectureDocumentTests(unittest.TestCase):
    # Reuse actual Copier fixtures without inheriting/rerunning the unrelated suite.
    setUp = copier_tests.CopierTests.setUp
    copy = copier_tests.CopierTests.copy
    validation_result = copier_tests.CopierTests.validation_result
    validate = copier_tests.CopierTests.validate

    def assert_package(self, target):
        expected = (self.source / SOURCE_GUIDE).read_text().replace(
            '(../templates/architecture/', '(architecture-templates/').replace(
            '(../quality/testing.md)', '(testing.md)').replace(
            '(../quality/ci-cd.md)', '(ci-cd.md)')
        self.assertEqual((target / INSTALLED_GUIDE).read_text().strip(), expected.strip())
        self.assertEqual((target / INSTALLED_PROVENANCE).read_text().strip(),
                         (self.source / SOURCE_PROVENANCE).read_text().strip())
        self.assertIn('(architecture.md)',
                      (target / '.engineering-backbone/core.md').read_text())
        self.assertEqual({p.name for p in (target / INSTALLED_TEMPLATES).iterdir()},
                         set(TEMPLATES))
        for name in TEMPLATES:
            expected = (self.source / SOURCE_TEMPLATES / name).read_text().replace(
                '(../../agent-governance/architecture.md', '(../architecture.md').replace(
                '(../../agent-governance/architecture-sources.md', '(../architecture-sources.md')
            self.assertEqual((target / INSTALLED_TEMPLATES / name).read_text().strip(),
                             expected.strip(), name)

    def test_copy_distributes_complete_guidance_without_product_documents(self):
        for selected in (False, True):
            with self.subTest(adapters_and_quality=selected):
                target = self.copy(use_codex=selected, use_copilot=selected,
                                   use_opencode=selected, use_quality_framework=selected)
                self.assert_package(target)
                self.assertFalse((target / 'docs/architecture').exists())
                self.assertFalse((target / 'docs/requirements').exists())
                self.assertFalse((target / 'package.json').exists())
                self.assertFalse((target / 'pyproject.toml').exists())
                self.validate(target)

    def test_update_refreshes_managed_guides_and_preserves_project_authorship(self):
        target = self.copy()
        protected = {
            'docs/architecture/architecture.md': '# Project design\nOwned by this project.\n',
            'docs/architecture/decisions/ADR-LOCAL.md': '# Local decision\nKeep rationale.\n',
            'docs/requirements/REQ-LOCAL.md': '# Local requirement\nKeep acceptance.\n',
            'docs/templates/architecture/local.md': '# Project template\nKeep extensions.\n',
        }
        for relative, text in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        for relative in ('AGENTS.md', '.github/copilot-instructions.md'):
            path = target / relative
            path.write_text(path.read_text() + '\nPreserve stricter local review ownership.\n',
                            encoding='utf-8')
            protected[relative] = path.read_text()
        before = {relative: (target / relative).read_bytes() for relative in protected}
        copier_tests.initialize(target)
        copier_tests.commit(target, 'Project-owned design and native instructions')
        for relative in (SOURCE_GUIDE, SOURCE_TEMPLATES + '/decision.md'):
            path = self.source / relative
            path.write_text(path.read_text() + '\nReviewed architecture update fixture.\n',
                            encoding='utf-8')
        copier_tests.commit(self.source, 'Architecture reference update fixture')
        copier_tests.git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        for relative, content in before.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assert_package(target)
        self.validate(target)

    def test_missing_managed_contract_or_template_is_rejected(self):
        target = self.copy(use_codex=False, use_copilot=False, use_quality_framework=False)
        self.validate(target)
        for relative in (INSTALLED_GUIDE, INSTALLED_TEMPLATES + '/decision.md'):
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

    def test_direct_copy_requires_resolvable_contract_and_template_links(self):
        # setUp copied the complete current source tree into an isolated fixture.
        def validate_source():
            return subprocess.run(
                [sys.executable, str(self.source / '.engineering-backbone/src/validate.py'),
                 '--root', str(self.source)], cwd=self.source, capture_output=True, text=True)

        result = validate_source()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for relative in (SOURCE_GUIDE, SOURCE_TEMPLATES + '/decision.md'):
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


if __name__ == '__main__':
    unittest.main()
