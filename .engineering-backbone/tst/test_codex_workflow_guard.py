"""Run the pinned Codex guard with approved historical consumer tooling."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy
import yaml

from src.maintenance.compile_toolchain_fingerprint import FILES, replace_codex_guard
from tst.test_workflows import historical_source, run_shell_payload


ROOT = Path(__file__).resolve().parents[2]


class CodexWorkflowGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='backbone-codex-guard-source-')
        cls.addClassCleanup(cls.temp.cleanup)
        parent = Path(cls.temp.name)
        old_source = parent / 'old-source'
        historical_source(old_source, 'attested-review')
        cls.pristine = parent / 'old-consumer'
        run_copy(str(old_source), cls.pristine, defaults=True, quiet=True, skip_tasks=True)
        cls.workflow = (ROOT / '.github/workflows/governance-checks.yml').read_text()
        cls.step = next(step for step in yaml.safe_load(cls.workflow)['jobs']['validate']['steps']
                        if step['name'] == 'Validate generated consumer with trusted tooling')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-codex-guard-run-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.base = self.workspace / 'trusted-base'
        self.candidate = self.workspace / 'candidate'
        shutil.copytree(self.pristine, self.base)
        shutil.copytree(self.base, self.candidate)

    def write(self, relative, content):
        path = self.candidate / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def run_guard(self):
        env = dict(os.environ)
        env.update(self.step['env'])
        env.update({'GITHUB_WORKSPACE': str(self.workspace),
                    'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH']})
        return run_shell_payload(self.workspace, self.step['run'], env=env)

    def run_old_validator(self):
        return subprocess.run([sys.executable, '-I',
                               str(self.base / '.engineering-backbone/validate.py'),
                               '--root', str(self.candidate), '--trusted-base', str(self.base)],
                              cwd=self.base, text=True, capture_output=True)

    def assert_guard_rejects(self):
        result = self.run_guard()
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn('PASS: structural', result.stdout)
        return result

    def assert_historical_bundle_unchanged(self):
        for name in FILES:
            self.assertEqual((self.base / '.engineering-backbone' / name).read_bytes(),
                             (self.candidate / '.engineering-backbone' / name).read_bytes(), name)

    def test_approved_historical_consumer_remains_valid_with_pinned_guard(self):
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('PASS: structural contracts validated', result.stdout)
        self.assert_historical_bundle_unchanged()

    def test_old_validator_passes_collision_while_pinned_guard_rejects_it(self):
        path = self.write('.codex/agents/00-local.toml',
                          'name = "backbone_reviewer"\n'
                          'developer_instructions = "Use substituted review instructions."\n')
        before = path.read_bytes()
        legacy = self.run_old_validator()
        self.assertEqual(0, legacy.returncode, legacy.stdout + legacy.stderr)
        result = self.assert_guard_rejects()
        self.assertIn('.codex/agents/00-local.toml', result.stderr)
        self.assertEqual(before, path.read_bytes())
        self.assert_historical_bundle_unchanged()

    def test_recursive_and_nested_project_names_are_checked_with_old_tooling(self):
        for relative in ('.codex/agents/team/local.toml',
                         'packages/web/.codex/agents/backbone-reviewer.toml',
                         'artifacts/project/.codex/agents/local.toml'):
            with self.subTest(relative=relative):
                path = self.write(relative, 'name = "\\u2003backbone_reviewer\\u0085"\n')
                before = path.read_bytes()
                result = self.assert_guard_rejects()
                self.assertIn(relative, result.stderr)
                self.assertEqual(before, path.read_bytes())
                path.unlink()

    def test_case_variant_native_paths_are_rejected_by_actual_historical_workflow(self):
        aliases = (
            ('.CODEX/agents/local.toml', 'name = "backbone_reviewer"\n'),
            ('.codex/Agents/local.toml', 'name = "backbone_reviewer"\n'),
            ('.codex/CONFIG.TOML', '[agents.backbone_reviewer]\ndescription = "Substitute"\n'),
        )
        for coexist in (False, True):
            for relative, content in aliases:
                with self.subTest(relative=relative, coexist=coexist):
                    self.write('packages/web/' + relative, content)
                    if coexist:
                        self.write('packages/web/.codex/agents/local.toml',
                                   'name = "project_owned"\n')
                        self.write('packages/web/.codex/config.toml',
                                   '# Local canonical settings.\nmodel = "local-model"\n')
                    project = self.candidate / 'packages/web'
                    originals = {path.relative_to(project): path.read_bytes()
                                 for path in project.rglob('*') if path.is_file()}
                    legacy = self.run_old_validator()
                    self.assertEqual(0, legacy.returncode, legacy.stdout + legacy.stderr)
                    result = self.assert_guard_rejects()
                    self.assertIn('case-variant Codex native path', result.stderr)
                    self.assertEqual(originals,
                                     {path.relative_to(project): path.read_bytes()
                                      for path in project.rglob('*') if path.is_file()})
                    self.assert_historical_bundle_unchanged()
                    shutil.rmtree(project)

    def test_case_variant_codex_file_entries_are_rejected_by_historical_workflow(self):
        for location in ('', 'packages/web/'):
            if location:
                self.write(location + '.codex/agents/local.toml', 'name = "project_owned"\n')
            for kind, filename in (('file', '.CODEX'), ('symlink', '.CoDeX')):
                with self.subTest(location=location, kind=kind):
                    target = self.write('application-target.txt', 'Project-owned target bytes.\n')
                    relative = location + filename
                    alias = self.candidate / relative
                    if kind == 'symlink':
                        alias.symlink_to(target)
                    else:
                        alias.write_text('Project-owned ordinary file bytes.\n')
                    original_link = alias.readlink() if alias.is_symlink() else None
                    originals = {path.relative_to(self.candidate): path.read_bytes()
                                 for path in self.candidate.rglob('*') if path.is_file()}
                    legacy = self.run_old_validator()
                    self.assertEqual(0, legacy.returncode, legacy.stdout + legacy.stderr)
                    result = self.assert_guard_rejects()
                    self.assertIn(relative, result.stderr)
                    self.assertIn('case-variant Codex native path', result.stderr)
                    self.assertEqual(originals,
                                     {path.relative_to(self.candidate): path.read_bytes()
                                      for path in self.candidate.rglob('*') if path.is_file()})
                    self.assertEqual(kind == 'symlink', alias.is_symlink())
                    if original_link is not None:
                        self.assertEqual(original_link, alias.readlink())
                    self.assert_historical_bundle_unchanged()
                    alias.unlink()
                    target.unlink()

    def test_old_tooling_cannot_approve_config_alias_or_reserved_fallback(self):
        role = self.write('role-files/review.toml',
                          'name = "backbone_reviewer"\n'
                          'developer_instructions = "Substituted instructions."\n')
        config = self.write('.codex/config.toml',
                            '[agents.project_alias]\nconfig_file = "../role-files/review.toml"\n')
        legacy = self.run_old_validator()
        self.assertEqual(0, legacy.returncode, legacy.stdout + legacy.stderr)
        originals = {path: path.read_bytes() for path in (config, role)}
        self.assert_guard_rejects()
        self.assertEqual(originals, {path: path.read_bytes() for path in originals})
        role.write_text('developer_instructions = "No name; use declaration key."\n')
        config.write_text(config.read_text().replace('project_alias', 'backbone_reviewer'))
        self.assert_guard_rejects()
        self.assert_historical_bundle_unchanged()

    def test_canonical_references_and_unrelated_settings_keep_their_bytes(self):
        local = self.write('role-files/local.toml',
                           '# Project-owned role outside native discovery.\n'
                           'name = "project_audit"\nmodel = "project-model"\n')
        config = self.write('.codex/config.toml',
                            '# Preserve local preferences.\nmodel = "project-model"\n'
                            '[agents.backbone_reviewer]\n'
                            'config_file = "agents/backbone-reviewer.toml"\n'
                            '[agents.project_audit]\nconfig_file = "../role-files/local.toml"\n')
        role = self.candidate / '.codex/agents/backbone-implementer.toml'
        role.write_text(role.read_text().replace('workspace-write', 'read-only'))
        upper = self.write('.codex/agents/distinct.toml', 'name = "BACKBONE_REVIEWER"\n')
        ignored = self.write('.codex/agents/ignored.TOML', 'name = "backbone_reviewer"\nnot TOML\n')
        originals = {path: path.read_bytes() for path in (local, config, role, upper, ignored)}
        result = self.run_guard()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(originals, {path: path.read_bytes() for path in originals})
        self.assert_historical_bundle_unchanged()

    def test_disabled_provider_cannot_bypass_pinned_preflight(self):
        facts = self.candidate / '.engineering-backbone/project.json'
        data = json.loads(facts.read_text())
        data['agents']['codex'] = False
        facts.write_text(json.dumps(data) + '\n')
        self.write('.codex/agents/00-local.toml', 'name = "backbone_reviewer"\n')
        result = self.assert_guard_rejects()
        self.assertIn('Candidate cannot disable trusted-base agent: codex', result.stderr)
        self.assert_historical_bundle_unchanged()

    def test_candidate_imports_cannot_replace_executed_namespace_guard(self):
        marker = self.workspace / 'candidate-import-executed'
        for module in ('tomllib.py', 'yaml.py', 'jsonschema.py', 'pathlib.py'):
            self.write(module, f'from pathlib import Path\nPath({str(marker)!r}).touch()\n'
                       'raise RuntimeError("candidate module executed")\n')
        path = self.write('.codex/agents/00-local.toml', 'name = "backbone_reviewer"\n')
        result = self.assert_guard_rejects()
        self.assertIn('.codex/agents/00-local.toml', result.stderr)
        self.assertFalse(marker.exists())
        self.assertNotIn('candidate module executed', result.stdout + result.stderr)
        self.assertTrue(path.is_file())
        self.assert_historical_bundle_unchanged()

    def test_ambiguous_native_paths_or_identity_data_fail_before_structural_pass(self):
        path = self.candidate / '.codex/agents/local.toml'
        outside = self.workspace / 'outside.toml'
        outside.write_text('name = "backbone_reviewer"\n')
        path.symlink_to(outside)
        self.assert_guard_rejects()
        path.unlink()
        for body in ('name = "project_local"\nname = "backbone_reviewer"\n',
                     'description = "Standalone role with missing identity"\n'):
            with self.subTest(body=body):
                path.write_text(body)
                self.assert_guard_rejects()
        path.unlink()
        self.write('.codex/config.toml',
                   '[agents.project_alias]\nconfig_file = "../../outside.toml"\n')
        self.assert_guard_rejects()

    def test_compiler_reconstructs_codex_guard_and_detects_its_drift(self):
        self.assertEqual(self.workflow, replace_codex_guard(self.workflow, ROOT))
        changed = self.workflow.replace('def codex_errors(', 'def codex_guard_drift(', 1)
        self.assertNotEqual(self.workflow, changed)
        self.assertEqual(self.workflow, replace_codex_guard(changed, ROOT))


if __name__ == '__main__':
    unittest.main()
