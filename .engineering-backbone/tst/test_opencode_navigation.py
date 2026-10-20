"""OpenCode role context and historical reviewer-plan procedure regressions."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import unittest

from tst import test_navigation as navigation_fixture

ROLES = navigation_fixture.ROLES


class OpenCodeNavigationTests(navigation_fixture.NavigationTests):
    # Reuse the actual resolver and realistic project fixture without rerunning the
    # base navigation cases here; inherited cases are hidden below after creation.
    def setUp(self):
        super().setUp()
        self.install_opencode()

    def install_opencode(self, enabled=True):
        self.companion = {'schema_version': '1', 'adapter_version': '1.0.0', 'enabled': enabled,
                          'opencode_version': '1.19.0', 'native_config': 'opencode.json'}
        self.write_json('.engineering-backbone/opencode.json', self.companion)
        instructions = ['AGENTS.md', '.engineering-backbone/core.md', '.engineering-backbone/core.json',
                        '.engineering-backbone/quality-policy.md', '.engineering-backbone/dependency-policy.md',
                        '.engineering-backbone/project.json', '.engineering-backbone/opencode-guide.md']
        self.write_json('opencode.json', {'$schema': 'https://opencode.ai/config.json',
                                        'instructions': instructions, 'permission': {'*': 'deny'}})
        for name in instructions:
            if not (self.root / name).exists():
                self.write(name, '# Required OpenCode policy\nRead before use.\n')
        self.write('.engineering-backbone/opencode-runner-contract.md', '# Runner\nQualify actual runtime.\n')
        for role in ROLES:
            self.write('.opencode/agents/backbone-' + role.replace('_', '-') + '.md', '# Role\n' + role + '\n')
        for skill in ('task-intake', 'implementation-plan', 'bug-reproduction', 'test-and-quality',
                      'code-review', 'finding-triage', 'delta-review', 'docs-traceability'):
            self.write('.opencode/skills/' + skill + '/SKILL.md', '# Procedure\n' + skill + '\n')

    def test_opencode_each_role_binds_only_its_selected_role_and_procedures(self):
        procedures = {'planner': {'implementation-plan'},
                      'implementer': {'bug-reproduction', 'test-and-quality', 'docs-traceability'},
                      'reviewer': {'implementation-plan', 'code-review', 'delta-review'},
                      'quality_checker': {'test-and-quality'}, 'triage': {'finding-triage'}}
        for role in ROLES:
            with self.subTest(role=role):
                packet = json.loads((self.root / 'plans/task.json').read_text())
                packet['role'] = role
                self.write_json('plans/task.json', packet)
                context = self.resolve_ok()
                paths = {item['path'] for item in context['documents']}
                self.assertEqual({path for path in paths if path.startswith('.opencode/agents/')},
                                 {'.opencode/agents/backbone-' + role.replace('_', '-') + '.md'})
                self.assertEqual({Path(path).parent.name for path in paths if path.startswith('.opencode/skills/')},
                                 {'task-intake', *procedures[role]})
                for name in ('.engineering-backbone/opencode.json', 'opencode.json',
                             '.engineering-backbone/opencode-guide.md', '.engineering-backbone/opencode-runner-contract.md'):
                    self.assertIn(name, paths)

    def test_opencode_reviewer_plan_procedure_changed_or_missing_invalidates_receipt(self):
        packet = json.loads((self.root / 'plans/task.json').read_text())
        packet['role'] = 'reviewer'
        self.write_json('plans/task.json', packet)
        context = self.resolve_ok()
        name = '.opencode/skills/implementation-plan/SKILL.md'
        self.assertIn(name, {item['path'] for item in context['documents']})
        self.write(name, '# Changed independent plan review\nNew obligations.\n')
        self.reject('differs from recomputed', self.request(), expected=context)
        (self.root / name).unlink()
        self.reject('absent', self.request())

    def test_opencode_all_mandatory_inputs_are_hashed_and_stale(self):
        context = self.resolve_ok()
        names = ['.engineering-backbone/opencode.json', 'opencode.json',
                 '.engineering-backbone/opencode-guide.md', '.engineering-backbone/opencode-runner-contract.md',
                 '.opencode/agents/backbone-implementer.md', '.opencode/skills/task-intake/SKILL.md',
                 '.engineering-backbone/dependency-policy.md']
        documents = {item['path']: item['sha256'] for item in context['documents']}
        for name in names:
            path = self.root / name
            original = path.read_bytes()
            self.assertEqual(documents[name], hashlib.sha256(original).hexdigest())
            path.write_bytes(original + b'\n')
            self.reject('differs from recomputed', self.request(), expected=context)
            path.write_bytes(original)

    def test_opencode_inactive_omits_routing_and_requires_active_navigation(self):
        self.install_opencode(enabled=False)
        context = self.resolve_ok()
        self.assertFalse(any(item['path'].startswith('.opencode/') for item in context['documents']))
        self.companion['enabled'] = True
        self.write_json('.engineering-backbone/opencode.json', self.companion)
        self.nav['enabled'] = False
        self.save_nav()
        self.reject('requires active navigation')

    def test_opencode_activation_inheritance_and_package_removal(self):
        base = self.workspace / 'base'
        shutil.copytree(self.root, base)
        self.write_json('.engineering-backbone/opencode.json', dict(self.companion, enabled=False), base)
        self.assertEqual(self.resolve(self.root, base)['errors'], [])
        (base / '.engineering-backbone/opencode.json').unlink()
        self.reject('already reviewed inactive seed', trusted_base=base)
        self.write_json('.engineering-backbone/opencode.json', self.companion, base)
        self.write_json('.engineering-backbone/opencode.json', dict(self.companion, enabled=False))
        self.reject('cannot be disabled', trusted_base=base)
        (self.root / '.engineering-backbone/opencode.json').unlink()
        self.reject('installed OpenCode package cannot disappear', trusted_base=base)

    def test_opencode_activation_binds_every_reviewed_package_input(self):
        # The task selects implementer; other roles and their procedures must
        # still belong to the same reviewed seed when the package is activated.
        config = json.loads((self.root / 'opencode.json').read_text())
        config['instructions'].append('docs/native-local.md')
        self.write('docs/native-local.md', '# Reviewed local instructions\n')
        self.write_json('opencode.json', config)
        base = self.workspace / 'inactive-seed'
        shutil.copytree(self.root, base)
        self.write_json('.engineering-backbone/opencode.json', dict(self.companion, enabled=False), base)
        self.resolve_ok(trusted_base=base)
        names = [
            'opencode.json', *config['instructions'],
            '.engineering-backbone/opencode-runner-contract.md',
            *('.opencode/agents/backbone-' + role.replace('_', '-') + '.md' for role in ROLES),
            *('.opencode/skills/' + skill + '/SKILL.md' for skill in (
                'task-intake', 'implementation-plan', 'bug-reproduction', 'test-and-quality',
                'code-review', 'finding-triage', 'delta-review', 'docs-traceability')),
        ]
        for name in names:
            with self.subTest(changed_input=name):
                path = self.root / name
                original = path.read_bytes()
                try:
                    # Even a parse-equivalent JSON change must not be admitted
                    # as flag-only activation of the reviewed input bytes.
                    path.write_bytes(original + b'\n')
                    self.reject('OpenCode activation must match the reviewed seed input: ' + name,
                                self.request(), trusted_base=base)
                finally:
                    path.write_bytes(original)
        self.resolve_ok(trusted_base=base)

    def test_opencode_activation_rejects_added_or_removed_instruction_paths(self):
        config = json.loads((self.root / 'opencode.json').read_text())
        config['instructions'].append('docs/native-local.md')
        self.write('docs/native-local.md', '# Reviewed local instructions\n')
        self.write('docs/another-local.md', '# Other local instructions\n')
        self.write_json('opencode.json', config)
        base = self.workspace / 'inactive-seed'
        shutil.copytree(self.root, base)
        self.write_json('.engineering-backbone/opencode.json', dict(self.companion, enabled=False), base)
        for instructions in (config['instructions'][:-1],
                             [*config['instructions'], 'docs/another-local.md']):
            with self.subTest(instructions=instructions):
                self.write_json('opencode.json', dict(config, instructions=instructions))
                self.reject('OpenCode activation must match the reviewed seed input paths',
                            self.request(), trusted_base=base)

    def test_opencode_seed_preparation_active_updates_and_unrelated_activation_edits_remain_valid(self):
        base = self.workspace / 'reviewed-package'
        shutil.copytree(self.root, base)
        name = '.opencode/agents/backbone-triage.md'
        self.write(name, '# Reviewed replacement triage instructions\n')
        # Already-active updates retain the existing contract; they are not a
        # second inactive-to-active transition.
        self.resolve_ok(trusted_base=base)
        inactive = dict(self.companion, enabled=False)
        self.write_json('.engineering-backbone/opencode.json', inactive, base)
        self.write_json('.engineering-backbone/opencode.json', inactive)
        self.resolve_ok(trusted_base=base)
        # Finish reviewing the inactive seed before the separate flag change.
        shutil.copyfile(self.root / name, base / name)
        self.write_json('.engineering-backbone/opencode.json', self.companion)
        self.write('src/backend/main.py', 'Unrelated application change.\n')
        self.resolve_ok(trusted_base=base)

    def test_opencode_explicit_local_instructions_are_bound_and_unsafe_inputs_reject(self):
        config = json.loads((self.root / 'opencode.json').read_text())
        self.write('docs/native-local.md', '# Extra local rules\nDo these as well.\n')
        config['instructions'].append('docs/native-local.md')
        self.write_json('opencode.json', config)
        self.assertIn('docs/native-local.md', {item['path'] for item in self.resolve_ok()['documents']})
        for path in ('https://example.invalid/rules', 'docs/*.md', '../rules.md', 'docs/native-local.md#extra'):
            config['instructions'][-1] = path
            self.write_json('opencode.json', config)
            self.assertTrue(self.resolve(self.root, request=self.request())['errors'])
        self.write('opencode.json', '{"instructions":[],"instructions":[]}')
        self.reject('Duplicate JSON')

    def test_opencode_active_implementer_null_head_keeps_existing_packet_grammar(self):
        packet = json.loads((self.root / 'plans/task.json').read_text())
        packet['repository']['head_revision'] = None
        self.write_json('plans/task.json', packet)
        self.resolve_ok()
        packet['role'] = 'reviewer'
        self.write_json('plans/task.json', packet)
        self.reject('missing Task Packet revision', self.request())


# Inherit only fixture helpers; unittest should execute base cases exactly once in
# test_navigation, where their package-absent compatibility remains explicit.
for _name in dir(navigation_fixture.NavigationTests):
    if _name.startswith('test_'):
        setattr(OpenCodeNavigationTests, _name, None)


if __name__ == '__main__':
    unittest.main()
