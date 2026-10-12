"""Codex role identity contracts; these checks do not claim client confinement."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from scripts.validate import codex_errors


ROLES = ('planner', 'implementer', 'reviewer')


def write(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return path


def codex_fixture(root):
    write(root, '.engineering-backbone/project.json',
          json.dumps({'agents': {'codex': True, 'copilot': False}}))
    write(root, 'AGENTS.md', 'Preserve local task scope and independent review.\n')
    for role in ROLES:
        mode = 'workspace-write' if role == 'implementer' else 'read-only'
        write(root, f'.codex/agents/backbone-{role}.toml',
              f'name = "backbone_{role}"\n'
              f'description = "Scoped {role} responsibility"\n'
              f'sandbox_mode = "{mode}"\n'
              'developer_instructions = "Follow the scoped task and report actual evidence."\n')


class CodexSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-codex-security-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'candidate'
        self.root.mkdir()
        codex_fixture(self.root)

    def errors(self, base=None, *, source=False):
        return codex_errors(self.root, base, source=source)

    def assert_rejected(self, *, base=None, source=False):
        errors = self.errors(base, source=source)
        self.assertTrue(errors, 'The native identity substitution must be rejected')
        return errors

    def test_canonical_source_and_consumer_are_accepted_without_mutation(self):
        before = {path.relative_to(self.root): path.read_bytes()
                  for path in self.root.rglob('*') if path.is_file()}
        self.assertEqual([], self.errors(source=True))
        self.assertEqual([], self.errors())
        self.assertEqual(before, {path.relative_to(self.root): path.read_bytes()
                                  for path in self.root.rglob('*') if path.is_file()})

    def test_reserved_aliases_are_rejected_in_root_recursive_and_nested_projects(self):
        for role in ROLES:
            for directory in ('.codex/agents', '.codex/agents/team',
                              'packages/frontend/.codex/agents'):
                with self.subTest(role=role, directory=directory):
                    path = write(self.root, f'{directory}/00-local.toml',
                                 f'name = "backbone_{role}"\n'
                                 'developer_instructions = "Use the substituted instructions."\n')
                    before = path.read_bytes()
                    self.assert_rejected()
                    self.assert_rejected(source=True)
                    self.assertEqual(before, path.read_bytes())
                    path.unlink()

    def test_nested_canonical_filename_cannot_own_root_reserved_identity(self):
        for role in ROLES:
            with self.subTest(role=role):
                relative = f'.codex/agents/backbone-{role}.toml'
                path = write(self.root, 'packages/api/' + relative,
                             (self.root / relative).read_text())
                self.assert_rejected()
                path.unlink()

    def test_case_variant_native_paths_fail_for_source_and_consumer_without_rewriting(self):
        aliases = (
            ('.CODEX/agents/local.toml', 'name = "backbone_reviewer"\n'),
            ('.codex/Agents/local.toml', 'name = "backbone_reviewer"\n'),
            ('.codex/CONFIG.TOML', '[agents.backbone_reviewer]\ndescription = "Substitute"\n'),
        )
        for coexist in (False, True):
            for index, (relative, content) in enumerate(aliases):
                with self.subTest(relative=relative, coexist=coexist):
                    case_root = Path(self.temp.name) / f'case-{coexist}-{index}'
                    codex_fixture(case_root)
                    write(case_root, 'packages/web/' + relative, content)
                    if coexist:
                        write(case_root, 'packages/web/.codex/agents/local.toml',
                              'name = "project_owned"\n')
                        write(case_root, 'packages/web/.codex/config.toml',
                              '# Canonical project-owned runtime settings.\nmodel = "local-model"\n')
                    originals = {path.relative_to(case_root): path.read_bytes()
                                 for path in case_root.rglob('*') if path.is_file()}
                    for source in (False, True):
                        errors = codex_errors(case_root, source=source)
                        self.assertTrue(any('case-variant Codex native path' in error
                                            for error in errors), errors)
                        self.assertEqual(originals,
                                         {path.relative_to(case_root): path.read_bytes()
                                          for path in case_root.rglob('*') if path.is_file()})

    def test_case_variant_codex_file_entries_fail_without_rewriting_links_or_targets(self):
        for location in ('', 'packages/web/'):
            for kind, filename in (('file', '.CODEX'), ('symlink', '.CoDeX')):
                with self.subTest(location=location, kind=kind):
                    case_root = Path(self.temp.name) / f'file-case-{bool(location)}-{kind}'
                    codex_fixture(case_root)
                    if location:
                        write(case_root, location + '.codex/agents/local.toml',
                              'name = "project_owned"\n')
                    target = write(case_root, 'application-target.txt', 'Project-owned target bytes.\n')
                    alias = case_root / (location + filename)
                    if kind == 'symlink':
                        alias.symlink_to(target)
                    else:
                        alias.write_text('Project-owned ordinary file bytes.\n')
                    original_link = alias.readlink() if alias.is_symlink() else None
                    originals = {path.relative_to(case_root): path.read_bytes()
                                 for path in case_root.rglob('*') if path.is_file()}
                    for source in (False, True):
                        errors = codex_errors(case_root, source=source)
                        self.assertTrue(any('case-variant Codex native path' in error
                                            for error in errors), errors)
                        self.assertEqual(originals,
                                         {path.relative_to(case_root): path.read_bytes()
                                          for path in case_root.rglob('*') if path.is_file()})
                        self.assertEqual(kind == 'symlink', alias.is_symlink())
                        if original_link is not None:
                            self.assertEqual(original_link, alias.readlink())

    def test_native_unicode_whitespace_is_trimmed_for_reserved_names(self):
        for whitespace in (' ', '\t', '\n', '\u0085', '\u00a0', '\u2003', '\u3000'):
            with self.subTest(whitespace=repr(whitespace)):
                path = write(self.root, '.codex/agents/00-local.toml',
                             'name = ' + json.dumps(whitespace + 'backbone_reviewer' + whitespace) + '\n')
                self.assert_rejected()
                path.unlink()

    def test_case_sensitive_names_exact_extensions_and_non_native_trim_are_preserved(self):
        originals = {}
        for filename, name in (
            ('uppercase.toml', 'BACKBONE_REVIEWER'),
            ('mixed-case.toml', 'Backbone_reviewer'),
            ('python-only-whitespace.toml', '\u001cbackbone_reviewer\u001c'),
            ('zero-width.toml', '\u200bbackbone_reviewer\u200b'),
        ):
            path = write(self.root, '.codex/agents/' + filename,
                         'name = ' + json.dumps(name) + '\n')
            originals[path] = path.read_bytes()
        for filename in ('ignored.TOML', 'ignored.toml.bak'):
            path = write(self.root, '.codex/agents/' + filename,
                         'name = "backbone_reviewer"\nthis is not TOML\n')
            originals[path] = path.read_bytes()
        self.assertEqual([], self.errors())
        self.assertEqual(originals, {path: path.read_bytes() for path in originals})

    def test_unrelated_roles_runtime_settings_and_reference_bytes_remain_local(self):
        config = write(self.root, '.codex/config.toml',
                       '# Project-owned settings and comments remain untouched.\n'
                       'model = "project-choice"\nsandbox_mode = "read-only"\n'
                       '[agents]\nmax_threads = 3\nmax_depth = 2\n'
                       '[agents.project_audit]\ndescription = "Local audit"\n'
                       'config_file = "../role-files/audit.toml"\n')
        local = write(self.root, 'role-files/audit.toml',
                      '# A referenced role is not required to live in agents/.\n'
                      'name = "project_audit"\nmodel = "local-model"\n'
                      'developer_instructions = "Use the local review contract."\n')
        nested = write(self.root, 'packages/web/.codex/agents/local.toml',
                       'name = "frontend_audit"\nmodel = "local-frontend-model"\n')
        originals = {path: path.read_bytes() for path in (config, local, nested)}
        self.assertEqual([], self.errors())
        self.assertEqual([], self.errors(source=True))
        self.assertEqual(originals, {path: path.read_bytes() for path in originals})

    def test_stronger_implementer_default_is_consumer_compatible(self):
        path = self.root / '.codex/agents/backbone-implementer.toml'
        path.write_text(path.read_text().replace('workspace-write', 'read-only'))
        before = path.read_bytes()
        self.assertEqual([], self.errors())
        self.assert_rejected(source=True)
        self.assertEqual(before, path.read_bytes())

    def test_managed_profiles_keep_existing_name_field_and_default_contracts(self):
        path = self.root / '.codex/agents/backbone-reviewer.toml'
        original = path.read_text()
        for changed in (
            original.replace('backbone_reviewer', 'project_reviewer'),
            original.replace('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"'),
            original.replace('description = "Scoped reviewer responsibility"', 'description = ""'),
            original + 'model = "unapproved-managed-override"\n',
        ):
            with self.subTest(changed=changed):
                path.write_text(changed)
                self.assert_rejected()
        path.write_text(original)
        self.assertEqual([], self.errors())

    def test_managed_config_declarations_reference_only_corresponding_root_profile(self):
        for role in ROLES:
            with self.subTest(role=role):
                config = write(self.root, '.codex/config.toml',
                               f'[agents.backbone_{role}]\n'
                               f'config_file = "./agents/backbone-{role}.toml"\n')
                original = config.read_bytes()
                self.assertEqual([], self.errors())
                self.assertEqual(original, config.read_bytes())
                config.unlink()
        nested = write(self.root, 'packages/web/.codex/config.toml',
                       '[agents.backbone_reviewer]\n'
                       'config_file = "../../../.codex/agents/backbone-reviewer.toml"\n')
        self.assertEqual([], self.errors())
        nested.unlink()

    def test_managed_config_keys_without_canonical_reference_are_rejected(self):
        write(self.root, 'role-files/local.toml', 'name = "project_local"\n')
        for declaration in (
            '[agents.backbone_reviewer]\ndescription = "Substituted managed role"\n',
            '[agents.backbone_reviewer]\nconfig_file = "../role-files/local.toml"\n',
            '[agents.backbone_reviewer]\nconfig_file = "agents/backbone-planner.toml"\n',
        ):
            with self.subTest(declaration=declaration):
                config = write(self.root, '.codex/config.toml', declaration)
                self.assert_rejected()
                config.unlink()

    def test_alias_config_key_cannot_reference_a_reserved_effective_name(self):
        for directory in ('.codex', 'packages/web/.codex'):
            with self.subTest(directory=directory):
                write(self.root, f'{directory}/other/role.toml',
                      'name = " backbone_reviewer "\ndeveloper_instructions = "Substituted."\n')
                config = write(self.root, f'{directory}/config.toml',
                               '[agents.project_alias]\nconfig_file = "other/role.toml"\n')
                before = config.read_bytes()
                self.assert_rejected()
                self.assertEqual(before, config.read_bytes())
                config.unlink()

    def test_alias_config_key_cannot_point_to_the_canonical_managed_profile(self):
        write(self.root, '.codex/config.toml',
              '[agents.project_alias]\nconfig_file = "agents/backbone-reviewer.toml"\n')
        self.assert_rejected()

    def test_reference_name_fallback_is_bound_to_exact_declaration_key(self):
        for body in ('developer_instructions = "Local instructions."\n',
                     'name = ""\n', 'name = " \\u2003 "\n'):
            with self.subTest(body=body):
                role = write(self.root, 'role-files/fallback.toml', body)
                config = write(self.root, '.codex/config.toml',
                               '[agents.backbone_reviewer]\nconfig_file = "../role-files/fallback.toml"\n')
                self.assert_rejected()
                config.write_text(config.read_text().replace('backbone_reviewer', 'project_reviewer'))
                originals = {path: path.read_bytes() for path in (config, role)}
                self.assertEqual([], self.errors())
                self.assertEqual(originals, {path: path.read_bytes() for path in originals})
                config.unlink()

    def test_standalone_identity_ambiguity_and_invalid_toml_fail_closed(self):
        path = self.root / '.codex/agents/local.toml'
        for body in ('description = "Missing identity"\n', 'name = ""\n',
                     'name = " \\u2003 "\n', 'name = 42\n',
                     'name = "local"\nname = "backbone_reviewer"\n',
                     'name = [\n'):
            with self.subTest(body=body):
                write(self.root, '.codex/agents/local.toml', body)
                self.assert_rejected()
                path.unlink()
        path.write_bytes(b'name = "local"\n# invalid UTF-8: \xff\n')
        self.assert_rejected()

    def test_config_parse_errors_or_uninspectable_references_fail_closed(self):
        outside = Path(self.temp.name) / 'outside.toml'
        outside.write_text('name = "backbone_reviewer"\n')
        for body in (
            '[agents.local]\nconfig_file = "missing.toml"\n',
            '[agents.local]\nconfig_file = "../../outside.toml"\n',
            '[agents.local]\nconfig_file = ' + json.dumps(str(outside)) + '\n',
            '[agents.local]\nconfig_file = ' + json.dumps('role-files/\0review.toml') + '\n',
            '[agents.local]\nconfig_file = 42\n',
            '[agents.local]\nconfig_file = "a.toml"\nconfig_file = "b.toml"\n',
            '[agents.local\n',
        ):
            with self.subTest(body=body):
                config = write(self.root, '.codex/config.toml', body)
                self.assert_rejected()
                config.unlink()

    def test_native_leaf_directory_and_nested_codex_symlinks_fail_closed(self):
        outside = Path(self.temp.name) / 'outside-role.toml'
        outside.write_text('name = "backbone_reviewer"\n')
        leaf = self.root / '.codex/agents/local.toml'
        leaf.symlink_to(outside)
        self.assert_rejected()
        leaf.unlink()
        directory = self.root / '.codex/agents'
        actual = self.root / 'actual-agents'
        directory.rename(actual)
        directory.symlink_to(actual, target_is_directory=True)
        self.assert_rejected()
        directory.unlink()
        actual.rename(directory)
        nested = Path(self.temp.name) / 'outside-project'
        write(nested, '.codex/agents/local.toml', 'name = "backbone_reviewer"\n')
        ancestor = self.root / 'packages/web/.codex'
        ancestor.parent.mkdir(parents=True)
        ancestor.symlink_to(nested / '.codex', target_is_directory=True)
        self.assert_rejected()

    def test_config_file_and_referenced_file_symlinks_fail_closed(self):
        actual = write(self.root, 'local-config.toml', '[agents.project_local]\n')
        config = self.root / '.codex/config.toml'
        config.symlink_to(actual)
        self.assert_rejected()
        config.unlink()
        referenced = write(self.root, 'role-files/actual.toml', 'name = "project_local"\n')
        alias = self.root / 'role-files/alias.toml'
        alias.symlink_to(referenced)
        write(self.root, '.codex/config.toml',
              '[agents.project_local]\nconfig_file = "../role-files/alias.toml"\n')
        self.assert_rejected()

    def test_disabled_provider_flag_cannot_hide_installed_or_new_collisions(self):
        base = Path(self.temp.name) / 'trusted-base'
        shutil.copytree(self.root, base)
        write(self.root, '.engineering-backbone/project.json',
              json.dumps({'agents': {'codex': False, 'copilot': False}}))
        alias = write(self.root, '.codex/agents/00-local.toml', 'name = "backbone_reviewer"\n')
        self.assert_rejected(base=base)
        alias.unlink()
        (self.root / '.codex/agents/backbone-reviewer.toml').unlink()
        self.assert_rejected(base=base)

    def test_absent_uninstalled_adapter_does_not_claim_codex_is_required(self):
        shutil.rmtree(self.root / '.codex')
        (self.root / 'AGENTS.md').unlink()
        write(self.root, '.engineering-backbone/project.json',
              json.dumps({'agents': {'codex': False, 'copilot': False}}))
        self.assertEqual([], self.errors())

    def test_source_review_artifacts_are_isolated_but_consumer_artifacts_are_checked(self):
        write(self.root, 'artifacts/prior-checkout/.codex/agents/00-local.toml',
              'name = "backbone_reviewer"\n')
        self.assertEqual([], self.errors(source=True))
        self.assert_rejected()

    def test_source_artifact_exclusion_does_not_hide_explicit_referenced_identity(self):
        role = write(self.root, 'artifacts/prior-checkout/.codex/agents/local.toml',
                     'name = "backbone_reviewer"\n')
        config = write(self.root, '.codex/config.toml',
                       '[agents.project_alias]\n'
                       'config_file = "../artifacts/prior-checkout/.codex/agents/local.toml"\n')
        originals = {path: path.read_bytes() for path in (role, config)}
        self.assert_rejected(source=True)
        self.assertEqual(originals, {path: path.read_bytes() for path in originals})

    def test_unrelated_application_directory_symlink_is_preserved_without_runtime_claim(self):
        outside = Path(self.temp.name) / 'project-assets'
        asset = write(outside, 'asset.txt', 'Project-owned application asset.\n')
        link = self.root / 'application-assets'
        link.symlink_to(outside, target_is_directory=True)
        original_target, original_bytes = link.readlink(), asset.read_bytes()
        # This is only preservation of a generic application link. Executing
        # Codex from aliased/external working directories needs separate review.
        self.assertEqual([], self.errors())
        self.assertTrue(link.is_symlink())
        self.assertEqual(original_target, link.readlink())
        self.assertEqual(original_bytes, asset.read_bytes())


if __name__ == '__main__':
    unittest.main()
