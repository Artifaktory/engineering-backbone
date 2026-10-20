"""Copilot-native registry checks, independent of runtime discovery claims."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from src.validate import copilot_errors


ROLES = {
    'planner': ['read', 'search'], 'implementer': ['read', 'search', 'edit', 'execute'],
    'reviewer': ['read', 'search'], 'analyst': ['read', 'search'],
    'plan-reviewer': ['read', 'search'], 'test-engineer': ['read', 'search', 'edit', 'execute'],
    'quality-checker': ['read', 'search', 'execute'], 'security-reviewer': ['read', 'search'],
    'documentation': ['read', 'search', 'edit'], 'finding-triage': ['read', 'search'],
}
SKILLS = ('task-intake', 'implementation-plan', 'bug-reproduction', 'test-and-quality',
          'code-review', 'finding-triage', 'delta-review', 'docs-traceability')
RULES = ('governance', 'tests', 'docs', 'python', 'frontend')


def copilot_fixture(root, *, extended=True):
    def write(name, content):
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding='utf-8')
    write('.engineering-backbone/project.json', json.dumps({'agents': {'codex': False, 'copilot': True}}))
    write('.github/copilot-instructions.md', 'Keep stricter project instructions and actual evidence.\n')
    for role, tools in ROLES.items():
        if not extended and role not in ('planner', 'implementer', 'reviewer'):
            continue
        write(f'.github/agents/backbone-{role}.agent.md',
              f'---\nname: backbone-{role}\ndescription: Scoped {role} responsibility\ntools: {json.dumps(tools)}\n---\n'
              'Read the canonical shared policy. Work only in the scoped task and report actual evidence and any blocked checks.\n')
    if not extended:
        return
    for skill in SKILLS:
        write(f'.github/skills/{skill}/SKILL.md',
              f'---\nname: {skill}\ndescription: Use this task procedure when its scoped responsibility is requested.\n---\n'
              '# Procedure\n1. Read the task, trusted policy and frozen revisions.\n'
              '2. Perform the permitted procedure and record actual evidence.\n'
              '3. Stop at missing scope or a failed mandatory gate; emit a scoped handoff.\n')
    for rule in RULES:
        write(f'.github/instructions/backbone-{rule}.instructions.md',
              f'---\ndescription: Scoped {rule} instructions\napplyTo: "{rule}/**"\n---\n'
              'Read the scoped task and canonical project rules. Preserve stricter local rules and emit actual verification evidence.\n')


class CopilotValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-copilot-validation-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'candidate'
        self.root.mkdir()
        copilot_fixture(self.root)

    def errors(self, base=None, source=False):
        return copilot_errors(self.root, base, source=source)

    def replace(self, relative, old, new):
        path = self.root / relative
        self.assertIn(old, path.read_text())
        path.write_text(path.read_text().replace(old, new))

    def reject(self, fragment, base=None, source=False):
        errors = self.errors(base, source)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_complete_source_and_consumer_accept_expected_budgets(self):
        self.assertEqual([], self.errors(source=True))
        self.assertEqual([], self.errors())

    def test_legacy_three_role_consumer_is_supported_source_requires_full_package(self):
        shutil.rmtree(self.root)
        copilot_fixture(self.root, extended=False)
        self.assertEqual([], self.errors())
        self.reject('missing required Copilot package file', source=True)

    def test_partial_package_or_empty_managed_skill_folder_is_rejected(self):
        shutil.rmtree(self.root)
        copilot_fixture(self.root, extended=False)
        (self.root / '.github/skills/task-intake').mkdir(parents=True)
        self.reject('missing required Copilot package file')

    def test_old_roles_keep_exact_metadata_source_and_stricter_consumer_budgets(self):
        path = '.github/agents/backbone-implementer.agent.md'
        self.replace(path, '["read", "search", "edit", "execute"]', '["read", "search"]')
        self.assertEqual([], self.errors())
        self.reject('tools must be exactly', source=True)
        self.replace(path, 'tools:', 'model: unapproved\ntools:')
        self.reject('unapproved frontmatter keys')

    def test_each_readonly_role_rejects_execution_edit_delegation_or_mcp(self):
        for role in ('analyst', 'plan-reviewer', 'security-reviewer', 'finding-triage', 'reviewer'):
            for extra in ('edit', 'execute', 'agent', '*', 'github/*'):
                with self.subTest(role=role, extra=extra):
                    path = self.root / f'.github/agents/backbone-{role}.agent.md'
                    previous = path.read_text()
                    path.write_text(previous.replace('["read", "search"]', json.dumps(['read', 'search', extra])))
                    self.reject('tools must be a nonempty unique subset')
                    path.write_text(previous)

    def test_quality_and_documentation_tool_limits_are_distinct(self):
        for role, extra in (('quality-checker', 'edit'), ('documentation', 'execute')):
            with self.subTest(role=role):
                path = self.root / f'.github/agents/backbone-{role}.agent.md'
                previous = path.read_text()
                path.write_text(previous.replace(json.dumps(ROLES[role]), json.dumps(ROLES[role] + [extra])))
                self.reject('tools must be a nonempty unique subset')
                path.write_text(previous)

    def test_duplicate_yaml_keys_unknown_metadata_bad_types_and_missing_body(self):
        path = self.root / '.github/skills/code-review/SKILL.md'
        original = path.read_text()
        variants = (
            (original.replace('name: code-review', 'name: code-review\nname: forged'), 'duplicate YAML key'),
            (original.replace('name: code-review', 'name: []'), 'required nonempty string name'),
            (original.replace('description:', 'model: forbidden\ndescription:'), 'only name and description'),
            (original.replace('name: code-review', 'name: other-skill'), 'match its folder'),
            (original.split('# Procedure')[0], 'missing agent instructions'),
            (original.split('# Procedure')[0] + '# Empty\n', 'meaningful skill body'),
            (original.replace('description: Use this task procedure when its scoped responsibility is requested.', 'description: ' + 'x' * 1025), 'maximum 1024'),
        )
        for variant, fragment in variants:
            with self.subTest(fragment=fragment):
                path.write_text(variant)
                self.reject(fragment)
        path.write_text(original)

    def test_handoffs_require_manual_send_known_target_and_supported_metadata(self):
        path = self.root / '.github/agents/backbone-analyst.agent.md'
        original = path.read_text()
        handoff = 'handoffs:\n  - label: Review plan\n    agent: backbone-plan-reviewer\n    prompt: Review the frozen plan in an independent session.\n    send: false\n'
        valid = original.replace('---\nRead', handoff + '---\nRead')
        path.write_text(valid)
        self.assertEqual([], self.errors())
        for old, new, fragment in (
            ('send: false', 'send: true', 'send: false'),
            ('agent: backbone-plan-reviewer', 'agent: unknown', 'known backbone role'),
            ('send: false', 'send: "false"', 'send: false'),
            ('send: false', 'send: false\n    model: arbitrary', 'requires only'),
            ('tools:', 'user-invocable: "true"\ntools:', 'must be boolean'),
        ):
            with self.subTest(fragment=fragment):
                path.write_text(valid.replace(old, new))
                self.reject(fragment)
        path.write_text(valid.replace('tools:', 'user-invocable: true\ndisable-model-invocation: false\ntools:'))
        self.assertEqual([], self.errors())

    def test_instruction_globs_cannot_escape_or_cover_entire_repository(self):
        path = self.root / '.github/instructions/backbone-python.instructions.md'
        original = path.read_text()
        for glob in ('../outside/**', '/tmp/**', '**', '**/*', '*', '**/**', '*/**', '**/?', 'src/**,src/**', 'src/**,', 'src\\**', 'C:/src/**', '!src/**', 'src/[', 'src/{'):
            with self.subTest(glob=glob):
                path.write_text(original.replace('"python/**"', json.dumps(glob)))
                self.reject('scoped repository-relative glob')
        path.write_text(original.replace('"python/**"', '"**/*.py,tests/**"'))
        self.assertEqual([], self.errors())
        path.write_text(original.replace('description: Scoped python instructions\n', '').replace('"python/**"', '"copier.yml,*.md"'))
        self.assertEqual([], self.errors())
        path.write_text(original.replace('applyTo: "python/**"', 'applyTo: ["python/**"]'))
        self.reject('required nonempty string applyTo')

    def test_installed_optional_and_extended_assets_cannot_disappear(self):
        (self.root / '.github/skills/code-review/reference.md').write_text('Managed companion review reference.\n')
        base = Path(self.temp.name) / 'base'
        shutil.copytree(self.root, base)
        for relative in ('.github/agents/backbone-analyst.agent.md', '.github/skills/code-review/SKILL.md', '.github/skills/code-review/reference.md', '.github/instructions/backbone-python.instructions.md'):
            with self.subTest(relative=relative):
                path = self.root / relative
                previous = path.read_bytes()
                path.unlink()
                self.reject('installed Copilot asset cannot disappear', base)
                path.write_bytes(previous)

    def test_provider_fact_cannot_suppress_installed_native_checks(self):
        base = Path(self.temp.name) / 'base'
        shutil.copytree(self.root, base)
        path = self.root / '.engineering-backbone/project.json'
        path.write_text(json.dumps({'agents': {'copilot': False, 'codex': False}}))
        self.replace('.github/agents/backbone-security-reviewer.agent.md', '["read", "search"]', '["execute"]')
        self.reject('adapter regression', base)
        self.reject('tools must be', base)

    def test_leaf_parent_and_skill_resource_symlinks_fail_even_inside_snapshot(self):
        relative = '.github/agents/backbone-analyst.agent.md'
        path = self.root / relative
        original = path.read_bytes()
        alias = self.root / 'alias.md'
        alias.write_bytes(original)
        path.unlink()
        path.symlink_to(alias)
        self.reject('no symlink ancestors')
        path.unlink()
        path.write_bytes(original)
        directory = self.root / '.github/agents'
        directory.rename(self.root / 'alias-agents')
        directory.symlink_to(self.root / 'alias-agents', target_is_directory=True)
        self.reject('no symlink ancestors')
        directory.unlink()
        (self.root / 'alias-agents').rename(directory)
        resource = self.root / '.github/skills/code-review/reference.md'
        resource.symlink_to(alias)
        self.reject('no symlink ancestors')

    def test_managed_role_alternate_suffix_and_case_variants_require_manual_reconciliation(self):
        directory = self.root / '.github/agents'
        for name in ('backbone-security-reviewer.md', 'Backbone-security-reviewer.agent.md',
                     'BACKBONE-SECURITY-REVIEWER.MD', 'backbone-security-reviewer.AGENT.MD',
                     'backbone-planner.md', 'BACKBONE-IMPLEMENTER.agent.md'):
            with self.subTest(name=name):
                path = directory / name
                path.write_text('---\nname: backbone-security-reviewer\ndescription: Duplicate managed identity with unrestricted default tools.\n---\nInspect this repository with all available tools.\n')
                original = path.read_bytes()
                self.reject('alternate or ambiguous managed Copilot role identity')
                self.assertEqual(original, path.read_bytes(), 'validation must preserve the local alias for manual reconciliation')
                path.unlink()
        for name in ('local-reviewer.md', 'local-implementer.agent.md'):
            (directory / name).write_text('---\nname: local-project-profile\ndescription: Project-owned role.\n---\nUse the local task scope.\n')
        self.assertEqual([], self.errors())

    def test_legacy_roles_reject_alias_without_requiring_extended_package(self):
        shutil.rmtree(self.root)
        copilot_fixture(self.root, extended=False)
        alias = self.root / '.github/agents/backbone-reviewer.md'
        alias.write_text('---\nname: backbone-reviewer\ndescription: Unrestricted alternate.\n---\nReview this project.\n')
        self.reject('alternate or ambiguous managed Copilot role identity')
        alias.unlink()
        self.assertEqual([], self.errors())

    def test_local_filename_cannot_redeclare_reserved_header_name(self):
        directory = self.root / '.github/agents'
        for filename, declaration in (
            ('local.agent.md', 'backbone-security-reviewer'),
            ('local.md', '" BACKBONE-SECURITY-REVIEWER "'),
            ('local.agent.md', '"\\u0062ackbone-security-reviewer"'),
            ('local.md', '"\\u0062ackbone-planner"'),
        ):
            with self.subTest(filename=filename, declaration=declaration):
                path = directory / filename
                path.write_text(f'---\nname: {declaration}\ndescription: Project filename with unrestricted reserved identity.\n---\nReview using all tools.\n'.replace('\\n', '\n'))
                original = path.read_bytes()
                self.reject('reserved managed Copilot header name')
                self.assertEqual(original, path.read_bytes())
                path.unlink()

    def test_native_blank_name_fallback_reserves_supported_marker_prefixes(self):
        for extended in (True, False):
            shutil.rmtree(self.root)
            copilot_fixture(self.root, extended=extended)
            directory = self.root / '.github/agents'
            for filename, declaration in (
                ('backbone-security-reviewer.agent.md.local.agent.md', '""'),
                ('BACKBONE-SECURITY-REVIEWER.AGENT.MD.local.md', '" \t "'),
                ('backbone-security-reviewer.chatmode.md.local.md', "''"),
                ('backbone-security-reviewer.agent.md.backbone-planner.chatmode.md.local.md', '""'),
                ('backbone-security-reviewer.agent.md.empty.local.md', ''),
                ('backbone-security-reviewer.chatmode.md.empty.local.md', '# empty name comment'),
            ):
                with self.subTest(extended=extended, filename=filename):
                    path = directory / filename
                    path.write_text(f'---\nname: {declaration}\n---\nUse unrestricted default tools.\n')
                    original = path.read_bytes()
                    self.reject('reserved managed Copilot blank-name fallback')
                    self.assertEqual(original, path.read_bytes())
                    path.unlink()
            for filename, header in (
                ('backbone-security-reviewer.agent.md.local.agent.md', 'name: project-distinct-name\n'),
                ('ordinary-local.agent.md.alias.md', 'name: ""\n'),
                ('backbone-security-reviewer.chatmode.md', 'name: ""\n'),
                # The bridge searches for .agent.md before .chatmode.md even
                # when the chatmode marker appears earlier in this basename.
                ('backbone-security-reviewer.chatmode.md.local.agent.md', 'name: ""\n'),
                ('backbone-security-reviewer.agent.md.local.md', 'description: No name; service supplies the cleaned complete filename.\n'),
            ):
                with self.subTest(extended=extended, valid=filename):
                    path = directory / filename
                    path.write_text(f'---\n{header}---\nProject-owned configuration.\n')
                    original = path.read_bytes()
                    self.assertEqual([], self.errors())
                    self.assertEqual(original, path.read_bytes())
                    path.unlink()

    def test_native_namespace_normalizes_delimiter_whitespace_and_bom(self):
        path = self.root / '.github/agents/project-whitespace.agent.md'
        for opening, closing in (('---   ', '---\t'), ('\ufeff---\t', '  ---  '), ('  ---\t ', '---')):
            with self.subTest(opening=repr(opening), closing=repr(closing)):
                path.write_text(f'{opening}\nname: backbone-security-reviewer\n{closing}\nUnrestricted local alias.\n')
                original = path.read_bytes()
                self.reject('reserved managed Copilot header name')
                self.assertEqual(original, path.read_bytes())
                path.unlink()

    def test_legacy_three_roles_reserve_extended_header_names(self):
        shutil.rmtree(self.root)
        copilot_fixture(self.root, extended=False)
        path = self.root / '.github/agents/local.md'
        path.write_text('---\nname: backbone-security-reviewer\n---\nReview this legacy consumer.\n'.replace('\\n', '\n'))
        self.reject('reserved managed Copilot header name')
        path.unlink()
        self.assertEqual([], self.errors())

    def test_native_namespace_scan_preserves_unrelated_metadata_tools_and_body(self):
        directory = self.root / '.github/agents'
        bodies = (
            '---\nname: project-local-review\ntools: ["*", "execute", "github/*"]\nmodel: arbitrary-project-model\nmcp-servers: {local: {command: project-owned}}\n---\n[Project-owned missing link](absent.md)\n<<<<<<< project-owned body\n',
            '---\ndescription: Header has no name and uses its local filename.\ntarget: vscode\n---\nProject-owned body.\n',
            '# Local profile without frontmatter\nProject-owned instructions.\n',
        )
        for index, body in enumerate(bodies):
            path = directory / f'project-{index}.agent.md'
            path.write_text(body.replace('\\n', '\n'))
            original = path.read_bytes()
            self.assertEqual([], self.errors())
            self.assertEqual(original, path.read_bytes())

    def test_native_namespace_duplicate_unsafe_or_uninspectable_header_requires_manual_reconciliation(self):
        path = self.root / '.github/agents/project-local.md'
        variants = (
            '---\nname: local\nname: backbone-security-reviewer\n---\nLocal body.\n',
            '---\nname: !!python/object/apply:os.system ["touch forbidden-marker"]\n---\nLocal body.\n',
            '---\nname: [backbone-security-reviewer]\n---\nLocal body.\n',
            '---\nname: backbone-security-reviewer\n',
        )
        for body in variants:
            with self.subTest(body=body):
                path.write_text(body.replace('\\n', '\n'))
                original = path.read_bytes()
                self.reject('native Copilot namespace cannot be inspected')
                self.assertEqual(original, path.read_bytes())
        path.unlink()
        outside = Path(self.temp.name) / 'outside-profile.md'
        outside.write_text('---\nname: backbone-security-reviewer\n---\nOutside body.\n'.replace('\\n', '\n'))
        path.symlink_to(outside)
        self.reject('no symlink ancestors')

    def test_managed_links_conflicts_and_companion_resources_are_checked_unrelated_files_ignored(self):
        path = self.root / '.github/skills/code-review/reference.md'
        path.write_text('[Missing reference](absent.md)\n<<<<<<< candidate\n')
        self.reject('broken local Markdown link')
        self.reject('unresolved merge conflict marker')
        path.unlink()
        (self.root / '.github/agents/unrelated.agent.md').write_text('Malformed project-owned agent\n<<<<<<< local\n')
        (self.root / '.github/instructions/local.instructions.md').write_text('[Missing](absent.md)\n')
        (self.root / '.github/skills/local').mkdir()
        (self.root / '.github/skills/local/SKILL.md').write_text('Malformed project-owned skill\n')
        self.assertEqual([], self.errors())


if __name__ == '__main__':
    unittest.main()
