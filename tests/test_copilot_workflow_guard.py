"""Execute the pinned guard with an older three-role trusted validator."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy
import yaml

from scripts.compile_toolchain_fingerprint import FILES, replace_copilot_guard
from tests.test_workflows import historical_source, run_shell_payload


ROOT = Path(__file__).resolve().parents[1]


class CopilotWorkflowGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='backbone-copilot-guard-source-')
        cls.addClassCleanup(cls.temp.cleanup)
        parent = Path(cls.temp.name)
        cls.old_source = parent / 'old-source'
        historical_source(cls.old_source, 'attested-review')
        cls.current_source = parent / 'current-source'
        shutil.copytree(ROOT, cls.current_source, ignore=shutil.ignore_patterns('.git', 'artifacts', '.venv', '__pycache__'))
        for directory in sorted((path for path in cls.current_source.rglob('*') if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        cls.current = parent / 'current-consumer'
        run_copy(str(cls.current_source), cls.current, defaults=True, quiet=True, skip_tasks=True)
        # Optional instructions must obey the same native contract.
        optional = parent / 'optional-consumer'
        run_copy(str(cls.current_source), optional, data={'copilot_python_profile': True, 'copilot_frontend_profile': True},
                 defaults=True, quiet=True, skip_tasks=True)
        cls.step = next(step for step in yaml.safe_load((ROOT / '.github/workflows/governance-checks.yml').read_text())['jobs']['validate']['steps']
                        if step['name'] == 'Validate generated consumer with trusted tooling')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-copilot-guard-run-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.base = self.workspace / 'trusted-base'
        run_copy(str(self.old_source), self.base, defaults=True, quiet=True, skip_tasks=True)
        self.candidate = self.workspace / 'candidate'
        shutil.copytree(self.base, self.candidate)

    def extended_candidate(self):
        # Install the new native package, while intentionally retaining the old
        # approved eight-file toolchain so the old validator is still executed.
        for item in self.current.iterdir():
            destination = self.candidate / item.name
            if item.is_dir():
                shutil.copytree(item, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination)
        for name in FILES:
            shutil.copy2(self.base / '.engineering-backbone' / name,
                         self.candidate / '.engineering-backbone' / name)

    def run_guard(self):
        env = dict(os.environ)
        env.update(self.step['env'])
        env.update({'GITHUB_WORKSPACE': str(self.workspace),
                    'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH']})
        return run_shell_payload(self.workspace, self.step['run'], env=env)

    def test_legacy_no_extended_assets_stays_compatible(self):
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('PASS: structural contracts validated', result.stdout)

    def test_valid_native_package_upgrade_is_checked_with_old_tooling(self):
        self.extended_candidate()
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual((self.base / '.engineering-backbone/validate.py').read_bytes(),
                         (self.candidate / '.engineering-backbone/validate.py').read_bytes())

    def test_old_validator_does_not_approve_elevated_new_role(self):
        self.extended_candidate()
        path = self.candidate / '.github/agents/backbone-security-reviewer.agent.md'
        path.write_text(path.read_text().replace('tools: [read, search]', 'tools: [read, search, edit, execute]'))
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('backbone-security-reviewer.agent.md: tools must be', result.stderr)
        self.assertNotIn('PASS: structural', result.stdout)

    def test_old_validator_cannot_approve_alternate_managed_native_identity(self):
        self.extended_candidate()
        marker = self.workspace / 'candidate-import-executed'
        # A no-op candidate module would falsely report success if candidate
        # import paths were trusted. The pinned guard must never execute it.
        (self.candidate / 'yaml.py').write_text(
            f'from pathlib import Path\nPath({str(marker)!r}).touch()\ndef load(*args, **kwargs): return {{}}\n')
        directory = self.candidate / '.github/agents'
        for name in ('backbone-security-reviewer.md', 'Backbone-security-reviewer.agent.md',
                     'BACKBONE-SECURITY-REVIEWER.MD', 'backbone-planner.md'):
            with self.subTest(name=name):
                alias = directory / name
                alias.write_text('---\nname: backbone-security-reviewer\ndescription: Unrestricted alternate defaults to all tools.\n---\nReview with all tools.\n')
                original = alias.read_bytes()
                result = self.run_guard()
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn('alternate or ambiguous managed Copilot role identity', result.stderr)
                self.assertNotIn('PASS: structural', result.stdout)
                self.assertFalse(marker.exists())
                self.assertEqual(original, alias.read_bytes())
                alias.unlink()
        (directory / 'local-reviewer.md').write_text('---\nname: local-reviewer\ndescription: Project-native profile.\n---\nFollow local scope.\n')
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse(marker.exists())

    def test_old_base_rejects_project_filename_with_reserved_header_identity(self):
        self.extended_candidate()
        marker = self.workspace / 'native-candidate-import-executed'
        (self.candidate / 'yaml.py').write_text(
            f'from pathlib import Path\nPath({str(marker)!r}).touch()\ndef load(*args, **kwargs): return {{}}\n'.replace('\\n', '\n'))
        directory = self.candidate / '.github/agents'
        for name, declaration, boundary in (('project-local.agent.md', 'backbone-security-reviewer', '---'),
                                            ('project-local.md', '" BACKBONE-SECURITY-REVIEWER "', '---'),
                                            ('project-local.agent.md', '"\\u0062ackbone-security-reviewer"', '---'),
                                            ('project-local.md', 'backbone-security-reviewer', '\ufeff---\t ')):
            with self.subTest(name=name, declaration=declaration, boundary=repr(boundary)):
                path = directory / name
                path.write_text(f'{boundary}\nname: {declaration}\ndescription: Reserved header and unrestricted default tools.\n---  \nReview using all tools.\n')
                original = path.read_bytes()
                result = self.run_guard()
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn('reserved managed Copilot header name', result.stderr)
                self.assertEqual(original, path.read_bytes())
                self.assertFalse(marker.exists())
                path.unlink()
        # Namespace inspection does not impose the managed role contract on
        # valid local profiles: arbitrary supported metadata and body stay local.
        path = directory / 'project-local.md'
        path.write_text('---\nname: project-local\ntools: ["*", "execute"]\nmodel: project-choice\n---\n[Missing local link](absent.md)\n<<<<<<< local body\n'.replace('\\n', '\n'))
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertFalse(marker.exists())

    def test_old_base_rejects_reserved_blank_name_filename_fallback(self):
        self.extended_candidate()
        marker = self.workspace / 'blank-name-candidate-import-executed'
        (self.candidate / 'yaml.py').write_text(
            f'from pathlib import Path\nPath({str(marker)!r}).touch()\ndef load(*args, **kwargs): return {{}}\n')
        directory = self.candidate / '.github/agents'
        for filename, declaration in (
            ('backbone-security-reviewer.agent.md.local.agent.md', '""'),
            ('BACKBONE-SECURITY-REVIEWER.AGENT.MD.local.md', '""'),
            ('backbone-security-reviewer.chatmode.md.local.md', "''"),
            ('backbone-security-reviewer.agent.md.backbone-planner.chatmode.md.local.md', '""'),
            ('backbone-security-reviewer.agent.md.empty.local.md', ''),
            ('backbone-security-reviewer.chatmode.md.empty.local.md', '# empty name comment'),
        ):
            with self.subTest(filename=filename, declaration=declaration):
                path = directory / filename
                path.write_text(f'---\nname: {declaration}\n---\nUse unrestricted default tools.\n')
                original = path.read_bytes()
                result = self.run_guard()
                self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn('reserved managed Copilot blank-name fallback', result.stderr)
                self.assertEqual(original, path.read_bytes())
                self.assertFalse(marker.exists())
                path.unlink()
        for filename, header in (
            ('backbone-security-reviewer.agent.md.local.agent.md', 'name: project-distinct-name\n'),
            ('ordinary-local.agent.md.alias.md', 'name: ""\n'),
            ('backbone-security-reviewer.chatmode.md', 'name: ""\n'),
            ('backbone-security-reviewer.chatmode.md.local.agent.md', 'name: ""\n'),
            ('backbone-security-reviewer.agent.md.local.md', 'description: No header name and complete cleaned filename fallback.\n'),
        ):
            with self.subTest(valid=filename):
                path = directory / filename
                path.write_text(f'---\n{header}---\nUse the project-owned contract.\n')
                original = path.read_bytes()
                result = self.run_guard()
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(original, path.read_bytes())
                self.assertFalse(marker.exists())
                path.unlink()

    def test_old_base_namespace_scan_rejects_symlinks_and_ambiguous_yaml_without_execution(self):
        self.extended_candidate()
        directory = self.candidate / '.github/agents'
        path = directory / 'project-local.agent.md'
        outside = self.workspace / 'outside-native.agent.md'
        outside.write_text('---\nname: backbone-security-reviewer\n---\nOutside body.\n'.replace('\\n', '\n'))
        path.symlink_to(outside)
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('no symlink ancestors', result.stderr)
        path.unlink()
        for content in ('---\nname: local\nname: backbone-security-reviewer\n---\nBody.\n',
                        '---\nname: !!python/object/apply:os.system ["touch forbidden-marker"]\n---\nBody.\n'):
            path.write_text(content.replace('\\n', '\n'))
            result = self.run_guard()
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn('native Copilot namespace cannot be inspected', result.stderr)
        self.assertFalse((self.workspace / 'forbidden-marker').exists())
        self.assertFalse((self.base / 'forbidden-marker').exists())

    def test_old_validator_does_not_approve_malformed_skill_or_unscoped_rule(self):
        self.extended_candidate()
        skill = self.candidate / '.github/skills/code-review/SKILL.md'
        original = skill.read_bytes()
        skill.write_text('---\nname: code-review\nname: other\ndescription: duplicate identity\n---\n# Invalid procedure\n')
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('duplicate YAML key', result.stderr)
        skill.write_bytes(original)
        rule = self.candidate / '.github/instructions/backbone-governance.instructions.md'
        text = rule.read_text()
        import re
        rule.write_text(re.sub(r'(?m)^applyTo:.*$', 'applyTo: "**/*"', text))
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('scoped repository-relative glob', result.stderr)

    def test_promoted_old_toolchain_cannot_remove_installed_new_assets(self):
        self.extended_candidate()
        shutil.rmtree(self.base)
        shutil.copytree(self.candidate, self.base)
        for relative in ('.github/agents/backbone-analyst.agent.md', '.github/skills/task-intake/SKILL.md',
                         '.github/instructions/backbone-tests.instructions.md'):
            path = self.candidate / relative
            original = path.read_bytes()
            path.unlink()
            result = self.run_guard()
            self.assertNotEqual(0, result.returncode)
            self.assertIn('installed Copilot asset cannot disappear', result.stderr)
            path.write_bytes(original)

    def test_guard_checks_new_managed_links_and_conflicts_without_importing_candidate_code(self):
        self.extended_candidate()
        (self.candidate / 'yaml.py').write_text('raise RuntimeError("candidate code imported")\n')
        skill = self.candidate / '.github/skills/code-review/SKILL.md'
        with skill.open('a') as file:
            file.write('\n[Absent contract](absent.md)\n<<<<<<< candidate\n')
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('broken local Markdown link', result.stderr)
        self.assertIn('unresolved merge conflict marker', result.stderr)
        self.assertNotIn('candidate code imported', result.stderr)

    def test_compiler_detects_guard_drift_and_reproduces_exact_source_function(self):
        text = (ROOT / '.github/workflows/governance-checks.yml').read_text()
        self.assertEqual(text, replace_copilot_guard(text, ROOT))
        self.assertNotEqual(text.replace('Legacy three-role consumers', 'Unreviewed guard rewrite'),
                            replace_copilot_guard(text.replace('Legacy three-role consumers', 'Unreviewed guard rewrite'), ROOT))
        source = self.workspace / 'drift-source'
        shutil.copytree(self.current_source, source)
        workflow = source / '.github/workflows/governance-checks.yml'
        workflow.write_text(text.replace('Legacy three-role consumers', 'Unreviewed guard rewrite'))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/compile_toolchain_fingerprint.py'),
                                 '--source', str(source), '--check'], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Copilot workflow guard is stale', result.stdout)


if __name__ == '__main__':
    unittest.main()
