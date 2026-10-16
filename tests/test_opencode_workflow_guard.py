"""Trusted compiled OpenCode checks precede an approved predecessor validator."""
from pathlib import Path
import os
import shutil
import sys
import tempfile
import unittest

from copier import run_copy
import yaml

from scripts.compile_toolchain_fingerprint import FILES, guard_function, replace_opencode_guard
from tests.test_opencode_validation import opencode_fixture
from tests.test_workflows import historical_source, run_shell_payload


ROOT = Path(__file__).resolve().parents[1]


class OpenCodeWorkflowGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='backbone-opencode-guard-source-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.old_source = Path(cls.temp.name) / 'old-source'
        historical_source(cls.old_source, 'attested-review')
        cls.workflow = (ROOT / '.github/workflows/governance-checks.yml').read_text()
        # Other owners regenerate shared source after editing. This refresh is
        # data-only; test_compiled_guard_is_current separately gates drift.
        workflow = replace_opencode_guard(cls.workflow, ROOT)
        cls.step = next(step for step in yaml.safe_load(workflow)['jobs']['validate']['steps']
                        if step.get('name') == 'Validate generated consumer with trusted tooling')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-opencode-guard-run-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.base = self.workspace / 'trusted-base'
        run_copy(str(self.old_source), self.base, defaults=True, quiet=True, skip_tasks=True)
        self.candidate = self.workspace / 'candidate'
        shutil.copytree(self.base, self.candidate)

    def install_package(self):
        previous = {path.relative_to(self.candidate).as_posix(): path.read_bytes()
                    for path in self.candidate.rglob('*') if path.is_file()}
        opencode_fixture(self.candidate)
        # This models an adapter installation without changing the coherent,
        # previously approved eight-file toolchain or existing project facts.
        for relative, content in previous.items():
            (self.candidate / relative).write_bytes(content)
        for relative in FILES:
            self.assertEqual((self.base / '.engineering-backbone' / relative).read_bytes(),
                             (self.candidate / '.engineering-backbone' / relative).read_bytes())

    def run_guard(self):
        env = dict(os.environ)
        env.update(self.step['env'])
        env.update({'GITHUB_WORKSPACE': str(self.workspace),
                    'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH']})
        return run_shell_payload(self.workspace, self.step['run'], env=env)

    def reject(self, fragment):
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(fragment, result.stderr)
        self.assertNotIn('PASS: structural', result.stdout)

    def test_compiled_guard_is_current_and_source_extraction_is_not_import(self):
        self.assertEqual(self.workflow, replace_opencode_guard(self.workflow, ROOT))
        altered = self.workflow.replace('def opencode_errors(', 'def stale_opencode_guard(', 1)
        self.assertNotEqual(altered, replace_opencode_guard(altered, ROOT))
        content = guard_function('opencode_errors', ROOT)
        self.assertIn('import yaml', content)
        self.assertNotIn('from scripts', content)

    def test_legacy_absence_and_new_package_with_unchanged_old_tooling_pass(self):
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.install_package()
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('PASS: structural contracts validated', result.stdout)

    def test_previous_validator_does_not_approve_elevated_role_or_candidate_import(self):
        self.install_package()
        (self.candidate / 'yaml.py').write_text('raise RuntimeError("candidate module is not trusted")\n')
        path = self.candidate / '.opencode/agents/backbone-implementer.md'
        path.write_text(path.read_text().replace('"bash": "ask"', '"bash": "allow"'))
        self.reject('permission bash must not exceed ask')

    def test_recursive_skills_regression_checked_before_old_validator(self):
        self.install_package()
        original = (self.candidate / '.opencode/skills/code-review/SKILL.md').read_text()
        for relative, identity in (('.opencode/skills/code-review/nested/SKILL.md', 'code-review'),
                                    ('.opencode/skills/code-review/nested/SKILL.md', 'new-local'),
                                    ('.opencode/skills/code-review/nested/skill.md', 'code-review')):
            with self.subTest(relative=relative, identity=identity):
                path = self.candidate / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(original.replace('name: code-review', 'name: ' + identity))
                self.reject('eight exact canonical paths')
                path.unlink()
        path = self.candidate / '.opencode/skills/code-review/nested/reference.md'
        path.write_text('# Ordinary supporting resource\n')
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_legacy_mode_and_modes_regression_checked_before_old_validator(self):
        self.install_package()
        for name in ('mode', 'modes', 'MODE', 'Modes'):
            with self.subTest(name=name):
                directory = self.candidate / '.opencode' / name
                directory.mkdir()
                self.reject('unsupported native alias')
                directory.rmdir()

    def test_external_reserved_skill_name_and_duplicate_permission_fail(self):
        self.install_package()
        path = self.candidate / '.claude/skills/project/nested/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\nname: code-review\n---\nLocal alternate skill.\n')
        self.reject('reserved managed OpenCode skill name')
        path.write_text('---\nname: unrelated-local\n---\nLocal alternate skill.\n')
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        path = self.candidate / 'opencode.json'
        path.write_text(path.read_text()[:-1] + ', "permission": {"*": "allow"}}')
        self.reject('duplicate JSON key')

    def test_inherited_package_removal_and_permission_weakening_rejected(self):
        self.install_package()
        path = self.candidate / '.opencode/agents/backbone-implementer.md'
        original = path.read_text()
        path.write_text(original.replace('"bash": "ask"', '"bash": "deny"'))
        shutil.copytree(self.candidate, self.base, dirs_exist_ok=True)
        path.write_text(original)
        self.reject('inherited OpenCode permission bash cannot weaken')
        path.write_text(original.replace('"bash": "ask"', '"bash": "deny"'))
        (self.candidate / '.engineering-backbone/opencode.json').unlink()
        self.reject('installed OpenCode package cannot disappear')


if __name__ == '__main__':
    unittest.main()
