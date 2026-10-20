"""Data-only native contract regressions; these do not establish runtime safety."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from scripts.validate import opencode_errors


ROLES = ('planner', 'implementer', 'reviewer', 'quality-checker', 'triage')
SKILLS = ('task-intake', 'implementation-plan', 'bug-reproduction', 'test-and-quality',
          'code-review', 'finding-triage', 'delta-review', 'docs-traceability')
SOURCE_INSTRUCTIONS = ['AGENTS.md', 'policy/core.md', 'policy/core.json', 'policy/quality.md',
                       'policy/dependencies.md', '.engineering-backbone/project.json',
                       'docs/opencode/workflow.md', 'CONTRIBUTING.md']
INSTALLED_INSTRUCTIONS = ['AGENTS.md', '.engineering-backbone/core.md', '.engineering-backbone/core.json',
                          '.engineering-backbone/quality-policy.md', '.engineering-backbone/dependency-policy.md',
                          '.engineering-backbone/project.json', '.engineering-backbone/opencode-guide.md']


def opencode_fixture(root, *, source=False):
    if source:
        # Replacing an installed fixture with a source fixture must leave one
        # canonical policy authority, just as a real source checkout does.
        (root / '.engineering-backbone/core.json').unlink(missing_ok=True)
    def write(relative, value):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding='utf-8')
    instructions = SOURCE_INSTRUCTIONS if source else INSTALLED_INSTRUCTIONS
    for relative in instructions:
        write(relative, '{}\n' if relative.endswith('.json') else '# Shared governance\nRead the scoped task and preserve stricter project instructions.\n')
    for name in ('opencode.fragment.json', 'opencode.schema.json', 'opencode-runner-contract.md'):
        write('.engineering-backbone/' + name, '{}\n' if name.endswith('.json') else '# Controlled runner\n')
    write('.engineering-backbone/opencode.json', json.dumps({
        'schema_version': '1', 'adapter_version': '1.0.0', 'enabled': False,
        'opencode_version': '1.19.0', 'native_config': 'opencode.json'}))
    permission = {'*': 'deny', 'read': 'allow', 'glob': 'allow', 'grep': 'allow', 'skill': 'allow'}
    write('opencode.json', json.dumps({'$schema': 'https://opencode.ai/config.json',
                                     'instructions': instructions, 'permission': permission}))
    for role in ROLES:
        budget = dict(permission)
        if role == 'implementer':
            budget.update(edit='ask', bash='ask')
        elif role == 'quality-checker':
            budget['bash'] = 'ask'
        write(f'.opencode/agents/backbone-{role}.md',
              f'---\ndescription: Scoped {role} responsibility\nmode: primary\npermission: {json.dumps(budget)}\n---\n'
              'Read the canonical shared policy and scoped task. Preserve stronger local rules and report actual evidence.\n')
    for skill in SKILLS:
        write(f'.opencode/skills/{skill}/SKILL.md',
              f'---\nname: {skill}\ndescription: Use the shared scoped procedure.\n---\n'
              '# Procedure\nRead the scoped task and canonical policy before acting. Record actual evidence, failures and blocked checks.\n'
              'Preserve the review and handoff contract and stop when required context is absent.\n')


class OpenCodeValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-opencode-validation-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'candidate'
        self.root.mkdir()
        opencode_fixture(self.root)

    def errors(self, base=None, source=False):
        return opencode_errors(self.root, base, source=source)

    def reject(self, fragment, base=None, source=False):
        errors = self.errors(base, source)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def change_json(self, relative, update):
        path = self.root / relative
        value = json.loads(path.read_text())
        update(value)
        path.write_text(json.dumps(value))

    def test_complete_inactive_consumer_and_exact_source_defaults(self):
        self.assertEqual([], self.errors())
        opencode_fixture(self.root, source=True)
        self.assertEqual([], self.errors(source=True))

    def test_legacy_absence_does_not_claim_or_mutate_unmanaged_native_files(self):
        shutil.rmtree(self.root)
        self.root.mkdir()
        path = self.root / 'opencode.json'
        path.write_text('{"model": "project-owned"}')
        self.assertEqual([], self.errors())
        self.assertEqual('{"model": "project-owned"}', path.read_text())

    def test_companion_exact_keys_types_versions_and_duplicate_json(self):
        path = self.root / '.engineering-backbone/opencode.json'
        original = path.read_text()
        for key, value in (('enabled', 1), ('adapter_version', '2'), ('opencode_version', 'latest'),
                           ('schema_version', 1), ('native_config', 'elsewhere.json'), ('unknown', False)):
            with self.subTest(key=key):
                obj = json.loads(original)
                obj[key] = value
                path.write_text(json.dumps(obj))
                self.reject('exact supported versions')
        path.write_text(original[:-1] + ', "enabled": true}')
        self.reject('duplicate JSON key')

    def test_inactive_seed_still_validates_native_files(self):
        path = self.root / '.opencode/agents/backbone-reviewer.md'
        path.write_text(path.read_text().replace('"read": "allow"', '"bash": "allow"'))
        self.reject('permission keys exceed')

    def test_activation_requires_active_navigation_and_cannot_be_disabled(self):
        self.change_json('.engineering-backbone/opencode.json', lambda obj: obj.update(enabled=True))
        self.reject('requires active navigation')
        path = self.root / '.engineering-backbone/navigation.json'
        path.write_text('{"schema_version":"1","enabled":true}')
        self.assertEqual([], self.errors())
        base = Path(self.temp.name) / 'base'
        shutil.copytree(self.root, base)
        self.change_json('.engineering-backbone/opencode.json', lambda obj: obj.update(enabled=False))
        self.reject('enabled OpenCode must remain enabled', base)

    def test_partial_or_inherited_package_cannot_disappear(self):
        base = Path(self.temp.name) / 'base'
        resource = self.root / '.opencode/skills/code-review/reference.txt'
        resource.write_text('Ordinary supporting resource.\n')
        shutil.copytree(self.root, base)
        for relative in ('.engineering-backbone/opencode.json', '.opencode/agents/backbone-reviewer.md',
                         '.opencode/skills/code-review/SKILL.md', '.opencode/skills/code-review/reference.txt'):
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_bytes()
                path.unlink()
                self.reject('installed OpenCode package cannot disappear', base)
                path.write_bytes(original)
        shutil.rmtree(self.root / '.opencode')
        self.reject('missing or case-ambiguous')

    def test_duplicate_native_config_and_frontmatter_never_win_by_order(self):
        path = self.root / 'opencode.json'
        original = path.read_text()
        path.write_text(original[:-1] + ', "permission": {"*":"allow"}}')
        self.reject('duplicate JSON key')
        path.write_text(original)
        profile = self.root / '.opencode/agents/backbone-reviewer.md'
        original = profile.read_text()
        profile.write_text(original.replace('mode: primary', 'mode: primary\nmode: all'))
        self.reject('duplicate YAML key')
        profile.write_text(original.replace('"read": "allow"', '"read": "allow", "read": "deny"'))
        self.reject('duplicate YAML key')

    def test_permissions_reject_wildcard_reordering_unknown_patterns_and_escalation(self):
        for role in ROLES:
            path = self.root / f'.opencode/agents/backbone-{role}.md'
            original = path.read_text()
            variants = (
                ('"*": "deny", "read": "allow"', '"read": "allow", "*": "deny"', 'must begin'),
                ('"*": "deny"', '"*": "ask"', 'must begin'),
                ('"read": "allow"', '"github/*": "deny"', 'keys exceed'),
                ('"read": "allow"', '"task": "deny"', 'keys exceed'),
                ('"read": "allow"', '"read": {"*": "allow"}', 'must not exceed'),
            )
            for old, new, error in variants:
                with self.subTest(role=role, error=error):
                    path.write_text(original.replace(old, new))
                    self.reject(error)
            if role in {'implementer', 'quality-checker'}:
                path.write_text(original.replace('"bash": "ask"', '"bash": "allow"'))
                self.reject('must not exceed ask')
            path.write_text(original)

    def test_consumer_restrictions_allowed_but_inherited_cannot_weaken(self):
        path = self.root / '.opencode/agents/backbone-implementer.md'
        original = path.read_text()
        path.write_text(original.replace('"bash": "ask"', '"bash": "deny"').replace(', "edit": "ask"', ''))
        self.assertEqual([], self.errors())
        base = Path(self.temp.name) / 'base'
        shutil.copytree(self.root, base)
        path.write_text(original)
        self.reject('inherited OpenCode permission bash cannot weaken', base)
        self.reject('inherited OpenCode permission edit cannot weaken', base)
        opencode_fixture(self.root, source=True)
        path.write_text(path.read_text().replace('"bash": "ask"', '"bash": "deny"'))
        self.reject('source defaults must match exactly', source=True)

    def test_explicit_instruction_additions_are_regular_and_inherited(self):
        extra = self.root / 'local-policy.md'
        extra.write_text('Stronger local project rules.\n')
        self.change_json('opencode.json', lambda obj: obj['instructions'].append('local-policy.md'))
        self.assertEqual([], self.errors())
        base = Path(self.temp.name) / 'base'
        shutil.copytree(self.root, base)
        self.change_json('opencode.json', lambda obj: obj['instructions'].remove('local-policy.md'))
        self.reject('inherited OpenCode instructions cannot disappear', base)

    def test_invalid_instruction_paths_missing_files_and_duplicates(self):
        path = self.root / 'opencode.json'
        original = path.read_text()
        for value in ('../outside.md', '/absolute.md', 'https://example.test/policy', '*.md', 'AGENTS.md#scope',
                      'docs\\policy.md', 'CON', 'AGENTS.md.', 'Absent.md', 'agents.md', 'AGENTS.md'):
            with self.subTest(value=value):
                path.write_text(original)
                self.change_json('opencode.json', lambda obj: obj['instructions'].append(value))
                self.assertTrue(self.errors())
        path.write_text(original)
        self.change_json('opencode.json', lambda obj: obj['instructions'].remove('AGENTS.md'))
        self.reject('missing mandatory shared instructions')

    def test_native_overrides_plugin_layers_and_legacy_mode_aliases_rejected(self):
        for name in ('agent', 'skill', 'plugin', 'plugins', 'tool', 'tools', 'command', 'commands', 'mode', 'modes',
                     'MODE', 'Modes', 'Agents', 'Skills'):
            with self.subTest(name=name):
                path = self.root / '.opencode' / name
                path.mkdir()
                self.reject('unsupported native alias')
                path.rmdir()
        for relative in ('opencode.jsonc', 'OpenCode.JSON', '.opencode/opencode.json',
                         '.opencode/opencode.jsonc', 'nested/opencode.json', 'nested/.opencode', '.OpenCode'):
            with self.subTest(relative=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.name.casefold() == '.opencode':
                    path.mkdir()
                else:
                    path.write_text('{}')
                self.reject('native configuration layer')
                path.rmdir() if path.is_dir() else path.unlink()

    def test_exact_recursive_skill_allowlist_regression_same_new_and_case_names(self):
        canonical = self.root / '.opencode/skills/code-review/SKILL.md'
        original = canonical.read_text()
        for relative, name in (('.opencode/skills/code-review/nested/SKILL.md', 'code-review'),
                                ('.opencode/skills/code-review/nested/SKILL.md', 'new-local-name'),
                                ('.opencode/skills/code-review/nested/skill.md', 'code-review'),
                                ('.opencode/skills/Code-Review/SKILL.md', 'code-review'),
                                ('.opencode/skills/new-local-name/SKILL.md', 'new-local-name')):
            with self.subTest(relative=relative, name=name):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(original.replace('name: code-review', 'name: ' + name))
                self.reject('eight exact canonical paths')
                path.unlink()
                if 'Code-Review' in relative:
                    path.parent.rmdir()
        resources = canonical.parent / 'resources'
        resources.mkdir()
        (resources / 'reference.md').write_text('# Supporting reference\nOrdinary resource.\n')
        (resources / 'sample.json').write_text('{}')
        self.assertEqual([], self.errors())

    def test_extra_agents_and_unsafe_metadata_cannot_override_role(self):
        path = self.root / '.opencode/agents/project-local.md'
        path.write_text('---\nmode: primary\npermission: {"*":"allow"}\n---\nLocal agent.\n')
        self.reject('five exact canonical paths')
        path.unlink()
        path = self.root / '.opencode/agents/backbone-reviewer.md'
        original = path.read_text()
        for old, new in (('mode: primary', 'mode: subagent'), ('mode: primary', 'mode: primary\nmodel: arbitrary'),
                         ('mode: primary', 'mode: primary\ntools: {bash: true}')):
            path.write_text(original.replace(old, new))
            self.reject('only description, mode primary and permission')

    def test_alternate_recursive_skill_names_reserved_unrelated_metadata_remains_local(self):
        for directory in ('.agents', '.claude', 'nested/.agents'):
            path = self.root / directory / 'skills/local/nested/SKILL.md'
            path.parent.mkdir(parents=True, exist_ok=True)
            for name in ('code-review', '" CODE-REVIEW "', '"\u0063ode-review"'):
                path.write_text(f'---\nname: {name}\ndescription: Alias\n---\nLocal body.\n')
                self.reject('reserved managed OpenCode skill name')
            path.write_text('---\nname: unrelated-local\ntools: ["*"]\n---\n[Local link](missing.md)\n')
        self.assertEqual([], self.errors())

    def test_alternate_skill_directory_case_ambiguity_is_rejected(self):
        path = self.root / '.agents/Skills'
        path.mkdir(parents=True)
        self.reject('case-variant alternate skill namespace')

    def test_alternate_uninspectable_namespace_is_rejected(self):
        path = self.root / '.claude/skills/local/SKILL.md'
        path.parent.mkdir(parents=True)
        for content in ('---\nname: local\nname: code-review\n---\nBody',
                        '---\nname: code-review\n', '---\nname: [code-review]\n---\nBody',
                        '---\nname: !!python/object/apply:os.system ["false"]\n---\nBody'):
            path.write_text(content)
            self.assertTrue(self.errors())

    def test_symlink_files_directories_resources_and_instruction_ancestors_rejected(self):
        path = self.root / '.opencode/skills/code-review/reference.md'
        path.symlink_to(self.root / 'AGENTS.md')
        self.reject('no symlink ancestors')
        path.unlink()
        path = self.root / '.opencode/skills/code-review/nested'
        path.symlink_to(self.root / '.opencode/skills/task-intake', target_is_directory=True)
        self.reject('no symlink ancestors')
        path.unlink()
        source = self.root / 'AGENTS.md'
        source.rename(self.root / 'local-rules.md')
        source.symlink_to(self.root / 'local-rules.md')
        self.reject('no symlink ancestors')

    def test_managed_text_bounds_utf8_conflicts_and_links(self):
        path = self.root / '.opencode/skills/code-review/SKILL.md'
        original = path.read_bytes()
        for value, expected in ((b'x' * 131073, 'exceeds 128 KiB'), (b'\xff', 'utf-8'),
                                 (original + b'\n<<<<<<< candidate\n', 'conflict marker'),
                                 (original + b'\n[Missing](absent.md)\n', 'broken local Markdown link')):
            path.write_bytes(value)
            self.reject(expected)
        path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
