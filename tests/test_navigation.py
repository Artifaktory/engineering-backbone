"""Deterministic route and handoff contract tests; no native client loading claim."""
import ast
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ROLES = ('planner', 'implementer', 'reviewer', 'quality_checker', 'triage')
TASKS = ('bugfix', 'implementation', 'architecture', 'review', 'documentation')
CATALOG = {
    'version': '1.0.0',
    'sources': [{'id': 'SRC-TEST', 'title': 'Trusted synthetic test authority'}],
    'rules': [{'id': 'TECH-' + name.upper() + '-001', 'version': '1',
               'check_kind_groups': groups} for name, groups in (
                   ('python', [['lint'], ['test']]), ('postgresql', [['test'], ['migration']]),
                   ('bash', [['lint'], ['test']]), ('powershell', [['lint'], ['test']]),
                   ('linux', [['test']]), ('windows', [['test']]), ('docker', [['container']]))],
    'profiles': [{'id': name, 'version': '1', 'rules': ['TECH-' + name.upper() + '-001'],
                  'quality_profiles': ['python'] if name == 'python' else []}
                 for name in ('python', 'postgresql', 'bash', 'powershell', 'linux', 'windows', 'docker')],
}


def manifest():
    return {
        'schema_version': '1', 'enabled': True,
        'documents': {'architecture': 'docs/architecture.md#design',
                      'review': 'docs/review.md', 'local': 'docs/local.md'},
        'always': ['local'],
        'roles': {role: ['review'] if role == 'reviewer' else [] for role in ROLES},
        'tasks': {task: ['architecture'] if task in ('architecture', 'bugfix') else [] for task in TASKS},
        'components': [
            {'id': component, 'paths': [prefix], 'profiles': profiles,
             'documents': ['architecture'] if component == 'backend' else ['local'],
             'checks': [{'rule_id': 'TECH-' + profile.upper() + '-001',
                         'check_ids': [kind for group in next(rule['check_kind_groups'] for rule in CATALOG['rules']
                                                            if rule['id'] == 'TECH-' + profile.upper() + '-001')
                                       for kind in group]}
                        for profile in profiles]}
            for component, prefix, profiles in (
                ('backend', 'src/backend', ['python', 'postgresql']),
                ('windows-shell', 'scripts/windows', ['powershell', 'windows']),
                ('linux-shell', 'scripts/linux', ['bash', 'linux', 'docker']))],
    }


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        content = (ROOT / 'scripts/navigation.py').read_text()
        node = next(node for node in ast.parse(content).body if isinstance(node, ast.FunctionDef)
                    and node.name == 'navigation_context')
        assignment = next(node for node in node.body if isinstance(node, ast.Assign)
                          and isinstance(node.targets[0], ast.Name)
                          and node.targets[0].id == 'technology_catalog_json')
        assignment.value = ast.Constant(json.dumps(CATALOG))
        namespace = {}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])),
                     'trusted-navigation-fixture', 'exec'), namespace)
        core = {
            'rules': json.loads((ROOT / 'standards/rules.json').read_text())['rules'],
            'profiles': [json.loads(path.read_text()) for path in sorted((ROOT / 'standards/profiles').glob('*.json'))],
        }
        engine = namespace['navigation_context']
        cls.resolve = staticmethod(lambda *args, **kwargs: engine(*args, authority=core, **kwargs))
        cls.schemas = {}
        for name in ('navigation', 'navigation-request'):
            schema = json.loads((ROOT / 'schemas' / (name + '.schema.json')).read_text())
            Draft202012Validator.check_schema(schema)
            cls.schemas[name] = Draft202012Validator(schema)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-navigation-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.root = self.workspace / 'candidate'
        self.root.mkdir()
        self.nav = manifest()
        self.install(self.root)

    def write(self, name, content, root=None):
        path = (root or self.root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def write_json(self, name, value, root=None):
        return self.write(name, json.dumps(value, indent=2) + '\n', root)

    def install(self, root):
        for section in ('sources', 'rules'):
            self.write_json('.engineering-backbone/standards/technologies/' + section + '.json',
                            {'schema_version': '1', 'version': CATALOG['version'], section: CATALOG[section]}, root)
            shutil.copyfile(ROOT / 'standards' / (section + '.json'),
                            self.write('.engineering-backbone/standards/' + section + '.json', '', root))
        for profile in CATALOG['profiles']:
            self.write_json('.engineering-backbone/standards/technologies/profiles/' + profile['id'] + '.json', profile, root)
        for name in ('baseline', 'python'):
            self.write('.engineering-backbone/standards/profiles/' + name + '.json',
                       (ROOT / 'standards/profiles' / (name + '.json')).read_text(), root)
        quality = {'schema_version': '1', 'enabled': True, 'catalog_version': '1.0.0',
                   'backbone_ref': 'b' * 40, 'profiles': ['baseline', 'python'],
                   'documents': {key: 'docs/' + key + '.md' for key in
                                 ('quality_plan', 'test_strategy', 'traceability', 'exceptions')},
                   'checks': [{'rule_id': 'QUAL-TEST-001', 'check_ids': ['test']}], 'exceptions': []}
        self.write_json('.engineering-backbone/quality-profile.json', quality, root)
        self.write_json('.engineering-backbone/workflows.json', {
            'schema_version': '1', 'enabled': True, 'profiles': ['python'], 'capabilities': ['database'],
            'runtimes': {'python': '3.12'}, 'checks': [
                {'id': kind, 'kind': kind, 'argv': ['python', '-c', 'raise SystemExit(7)'],
                 'cwd': '.', 'timeout_seconds': 30, 'phases': ['pr']}
                for kind in ('build', 'lint', 'test', 'migration', 'sast', 'container')]}, root)
        for name in quality['documents'].values():
            self.write(name, '# Project declaration\nStructural fixture only.\n', root)
        for name in ('.engineering-backbone/core.md', '.engineering-backbone/quality-policy.md',
                     '.engineering-backbone/quality-guide.md', '.engineering-backbone/technology-guide.md',
                     '.engineering-backbone/navigation-guide.md',
                     'AGENTS.md', 'CONTRIBUTING.md', '.github/copilot-instructions.md',
                     'docs/local.md', 'docs/review.md'):
            self.write(name, '# Instructions\nRetain stricter local obligations.\n', root)
        self.write('docs/architecture.md', '# Architecture\n## Design\nDatabase boundary.\n', root)
        self.write('src/backend/AGENTS.md', '# Backend\nRead local design constraints.\n', root)
        for name in ('src/backend/main.py', 'scripts/windows/build.ps1', 'scripts/linux/build.sh'):
            self.write(name, 'Fixture input; no executable command is run.\n', root)
        packet = json.loads((ROOT / 'plans/technology-navigation-task.json').read_text())
        packet.update(id='TASK-1', role='implementer', status='active')
        packet['repository']['head_revision'] = 'a' * 40
        packet['scope'] = {'include': ['src/**', 'scripts/**', 'docs/**'], 'exclude': ['src/backend/private/**']}
        self.write_json('plans/task.json', packet, root)
        self.write_json('.engineering-backbone/navigation.json', self.nav, root)

    def request(self, **changes):
        value = {'schema_version': '1', 'task_packet': 'plans/task.json', 'task_type': 'bugfix',
                 'paths': ['src/backend/main.py'], 'components': [], 'revision': 'a' * 40}
        value.update(changes)
        return value

    def resolve_ok(self, request=None, **kwargs):
        result = self.resolve(self.root, request=request or self.request(), **kwargs)
        self.assertEqual(result['errors'], [], result)
        self.assertEqual(result['context']['claim'], 'structural-context-only')
        self.assertEqual(result['context']['runtime_loading'], 'unverified')
        return result['context']

    def reject(self, phrase, request=None, **kwargs):
        result = self.resolve(self.root, request=request, **kwargs)
        self.assertTrue(result['errors'], result)
        self.assertIsNone(result['context'])
        self.assertIn(phrase, ' '.join(result['errors']))

    def save_nav(self):
        self.write_json('.engineering-backbone/navigation.json', self.nav)

    def test_python_postgresql_bugfix_routes_rules_checks_and_ancestor_instructions(self):
        self.schemas['navigation'].validate(self.nav)
        self.schemas['navigation-request'].validate(self.request())
        context = self.resolve_ok()
        self.assertEqual(context['components'], ['backend'])
        self.assertEqual([item['id'] for item in context['technology_profiles']], ['postgresql', 'python'])
        self.assertEqual({item['id'] for item in context['checks']}, {'lint', 'migration', 'test'})
        paths = {item['path'] for item in context['documents']}
        self.assertTrue({'AGENTS.md', 'src/backend/AGENTS.md', 'docs/architecture.md#design',
                         '.engineering-backbone/core.md', 'plans/task.json'} <= paths)
        self.assertEqual(context, self.resolve_ok(expected=context))

    def test_powershell_and_bash_platform_scenarios(self):
        for path, selected in [('scripts/windows/build.ps1', {'powershell', 'windows'}),
                               ('scripts/linux/build.sh', {'bash', 'linux', 'docker'})]:
            with self.subTest(path=path):
                context = self.resolve_ok(self.request(paths=[path], task_type='implementation'))
                self.assertEqual({item['id'] for item in context['technology_profiles']}, selected)

    def test_architecture_named_component_and_independent_reviewer(self):
        context = self.resolve_ok(self.request(paths=[], components=['backend'], task_type='architecture'))
        self.assertEqual(context['components'], ['backend'])
        packet = json.loads((self.root / 'plans/task.json').read_text())
        packet['role'] = 'reviewer'
        self.write_json('plans/task.json', packet)
        context = self.resolve_ok(self.request(task_type='review'))
        self.assertEqual(context['role'], 'reviewer')
        self.assertIn('docs/review.md', {item['path'] for item in context['documents']})

    def test_overlapping_routes_union_obligations(self):
        extra = copy.deepcopy(self.nav['components'][1])
        extra.update(id='shared-shell-policy', paths=['src'])
        self.nav['components'].append(extra)
        self.save_nav()
        context = self.resolve_ok()
        self.assertEqual(context['components'], ['backend', 'shared-shell-policy'])
        self.assertEqual({item['id'] for item in context['technology_profiles']},
                         {'python', 'postgresql', 'powershell', 'windows'})

    def test_legacy_absence_and_inactive_seed(self):
        (self.root / '.engineering-backbone/navigation.json').unlink()
        self.assertEqual(self.resolve(self.root), {'errors': [], 'context': None})
        self.nav.update(enabled=False, documents={}, always=[], components=[],
                        roles={role: [] for role in ROLES}, tasks={task: [] for task in TASKS})
        self.save_nav()
        self.assertEqual(self.resolve(self.root)['errors'], [])
        self.reject('requires active navigation', self.request())

    def test_activation_requires_reviewed_complete_seed_and_enabled_only_change(self):
        base = self.workspace / 'base'
        shutil.copytree(self.root, base)
        self.reject('already reviewed inactive seed', trusted_base=self.workspace)
        inactive = dict(self.nav, enabled=False)
        self.write_json('.engineering-backbone/navigation.json', inactive, base)
        self.assertEqual(self.resolve(self.root, base)['errors'], [])
        self.nav['always'].append('review')
        self.save_nav()
        self.reject('match the reviewed seed', trusted_base=base)

    def test_active_inheritance_rejects_disabled_removed_routes_and_checks(self):
        base = self.workspace / 'base'
        shutil.copytree(self.root, base)
        mutations = [lambda nav: nav.update(enabled=False),
                     lambda nav: nav['always'].clear(),
                     lambda nav: nav['roles']['reviewer'].clear(),
                     lambda nav: nav['tasks']['bugfix'].clear(),
                     lambda nav: nav['components'][0]['documents'].clear(),
                     lambda nav: nav['components'].pop(0)]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.nav = manifest()
                mutate(self.nav)
                self.save_nav()
                self.reject('Inherited' if self.nav['enabled'] else 'Active navigation', trusted_base=base)

    def test_missing_anchor_empty_document_and_renamed_document(self):
        for content, phrase in [('', 'Empty'), ('# Other\n', 'Missing or unsupported')]:
            self.write('docs/architecture.md', content)
            self.reject(phrase)
        (self.root / 'docs/architecture.md').rename(self.root / 'docs/renamed.md')
        self.reject('absent')

    def test_case_mismatch_collision_symlink_and_unsafe_paths(self):
        original = self.nav['documents']['local']
        for value in ('docs/Local.md', '../outside.md', '/tmp/a', 'docs\\a',
                      'docs/CON.md', 'docs/file. ', 'docs/local.md#missing'):
            with self.subTest(value=value):
                self.nav['documents']['local'] = value
                self.save_nav()
                self.assertTrue(self.resolve(self.root)['errors'])
        self.nav['documents']['local'] = original
        self.save_nav()
        self.write('docs/LOCAL.md', 'Case collision.\n')
        self.reject('ambiguous')
        (self.root / 'docs/LOCAL.md').unlink()
        (self.root / 'docs/local.md').unlink()
        (self.root / 'docs/local.md').symlink_to(self.root / 'docs/review.md')
        self.reject('Symlink')

    def test_null_duplicate_json_unknown_ids_and_unknown_schema_are_rejected(self):
        for content in ('null', '{"enabled":false,"enabled":true}', '{}'):
            self.write('.engineering-backbone/navigation.json', content)
            self.assertTrue(self.resolve(self.root)['errors'])
        for mutate, phrase in [(lambda: self.nav['components'][0]['profiles'].append('unknown'), 'Unknown technology'),
                               (lambda: self.nav['always'].append('unknown'), 'Unknown navigation'),
                               (lambda: self.nav.update(schema_version='2'), 'Invalid navigation')]:
            self.nav = manifest()
            mutate()
            self.save_nav()
            self.reject(phrase)

    def test_unknown_unmatched_out_of_scope_and_excluded_requests(self):
        for request, phrase in [(self.request(components=['unknown']), 'Unknown requested'),
                                (self.request(paths=['src/unmapped.py']), 'no component route'),
                                (self.request(paths=['outside/file.py']), 'outside Task Packet'),
                                (self.request(paths=['src/backend/private/secret.py']), 'outside Task Packet'),
                                (self.request(paths=[], components=[]), 'needs affected')]:
            with self.subTest(request=request):
                self.reject(phrase, request)

    def test_scope_globs_are_segment_bounded_and_double_star_can_recurse(self):
        packet = json.loads((self.root / 'plans/task.json').read_text())
        packet['scope'] = {'include': ['src/backend/*'], 'exclude': []}
        self.write_json('plans/task.json', packet)
        self.resolve_ok()
        self.reject('outside Task Packet', self.request(paths=['src/backend/deep/new.py']))
        packet['scope']['include'] = ['src/backend/**']
        self.write_json('plans/task.json', packet)
        self.resolve_ok(self.request(paths=['src/backend/deep/new.py']))

    def test_review_revision_request_role_injection_and_unresolved_override(self):
        self.reject('differs from Task Packet', self.request(revision='c' * 40))
        self.reject('missing or unknown keys', dict(self.request(), role='reviewer'))
        self.write('src/backend/AGENTS.override.md', '# Unexpected override\n')
        self.reject('Unresolved instruction override', self.request())

    def test_required_guides_are_resolved_and_missing_or_changed_guides_reject(self):
        context = self.resolve_ok()
        guides = {'.engineering-backbone/quality-guide.md',
                  '.engineering-backbone/technology-guide.md',
                  '.engineering-backbone/navigation-guide.md'}
        self.assertTrue(guides <= {item['path'] for item in context['documents']})
        for name in sorted(guides):
            with self.subTest(guide=name):
                path = self.root / name
                original = path.read_text()
                path.unlink()
                self.reject('absent', self.request())
                path.write_text('# Changed guide\nDifferent obligations.\n')
                self.reject('differs from recomputed', self.request(), expected=context)
                path.write_text(original)

    def test_stale_tampered_and_truncated_handoff(self):
        context = self.resolve_ok()
        for mutate in (lambda value: value.update(role='planner'),
                       lambda value: value['documents'].pop(),
                       lambda value: value.update(context_sha256='0' * 64)):
            old = copy.deepcopy(context)
            mutate(old)
            self.reject('differs from recomputed', self.request(), expected=old)
        self.write('docs/local.md', '# Stricter instructions\nRequire another human gate.\n')
        self.reject('differs from recomputed', self.request(), expected=context)

    def test_missing_technology_check_kind_and_required_quality_profile_fail(self):
        self.nav['components'][0]['checks'][1]['check_ids'] = ['test']
        self.save_nav()
        self.reject('check-kind coverage')
        self.nav = manifest()
        self.save_nav()
        path = self.root / '.engineering-backbone/quality-profile.json'
        quality = json.loads(path.read_text())
        quality['profiles'] = ['baseline']
        path.write_text(json.dumps(quality))
        self.reject('Required quality profile missing')

    def test_managed_catalog_poisoning_extra_file_and_nonpr_binding_fail(self):
        name = '.engineering-backbone/standards/technologies/rules.json'
        path = self.root / name
        original = path.read_text()
        value = json.loads(original)
        value['rules'][0]['check_kind_groups'] = []
        self.write_json(name, value)
        self.reject('differs from trusted authority')
        path.write_text(original)
        extra = self.write('.engineering-backbone/standards/technologies/profiles/fake.json', '{}')
        self.reject('profile set differs')
        extra.unlink()
        flow = json.loads((self.root / '.engineering-backbone/workflows.json').read_text())
        next(item for item in flow['checks'] if item['id'] == 'migration')['phases'] = ['release']
        self.write_json('.engineering-backbone/workflows.json', flow)
        self.reject('PR workflow check')

    def test_workflow_and_packet_changes_invalidate_receipt_without_execution(self):
        context = self.resolve_ok()
        workflow = json.loads((self.root / '.engineering-backbone/workflows.json').read_text())
        workflow['checks'][0]['argv'] = ['never-run-this-command']
        self.write_json('.engineering-backbone/workflows.json', workflow)
        self.reject('differs from recomputed', self.request(), expected=context)
        self.assertEqual(self.resolve(self.root)['errors'], [])

    def test_directory_and_named_component_discover_descendant_instructions(self):
        self.write('src/backend/nested/AGENTS.md', '# Nested rules\nApply extra gates.\n')
        for request in (self.request(paths=['src/backend']),
                        self.request(paths=[], components=['backend'], task_type='architecture')):
            with self.subTest(request=request):
                context = self.resolve_ok(request)
                self.assertTrue({'src/backend/AGENTS.md', 'src/backend/nested/AGENTS.md'} <=
                                {item['path'] for item in context['documents']})
        self.write('src/backend/nested/AGENTS.override.md', '# Override\n')
        self.reject('Unresolved instruction override', self.request(paths=[], components=['backend']))

    def test_named_component_cannot_select_fully_excluded_subtree(self):
        packet = json.loads((self.root / 'plans/task.json').read_text())
        packet['scope']['exclude'] = ['src/backend/**']
        self.write_json('plans/task.json', packet)
        self.reject('outside Task Packet', self.request(paths=[], components=['backend']))
        self.reject('outside Task Packet', self.request(paths=['src/backend']))

    def test_malformed_task_packet_fields_fail_closed(self):
        original = json.loads((self.root / 'plans/task.json').read_text())
        mutations = [lambda packet: packet.update(acceptance=[]),
                     lambda packet: packet['acceptance'][0].update(verification='guess'),
                     lambda packet: packet['acceptance'][0].update(status='pass', evidence=[]),
                     lambda packet: packet.update(validation={'commands': []}),
                     lambda packet: packet['repository'].update(base_revision='bad'),
                     lambda packet: packet.update(status='completed'),
                     lambda packet: packet['execution_budget'].update(max_iterations=True),
                     lambda packet: packet.update(forbidden_actions=[])]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                packet = copy.deepcopy(original)
                mutation(packet)
                self.write_json('plans/task.json', packet)
                self.assertTrue(self.resolve(self.root, request=self.request())['errors'])

    def test_document_identity_cannot_be_remapped_in_active_inherited_manifest(self):
        base = self.workspace / 'base'
        shutil.copytree(self.root, base)
        self.nav['documents']['local'] = 'docs/review.md'
        self.save_nav()
        self.reject('cannot be removed or remapped', trusted_base=base)

    def test_symlink_ancestor_and_new_path_discovery(self):
        context = self.resolve_ok(self.request(paths=['src/backend/new.py']))
        self.assertIn('src/backend/AGENTS.md', {item['path'] for item in context['documents']})
        link = self.root / 'src/link'
        link.symlink_to(self.root / 'src/backend', target_is_directory=True)
        self.reject('Symlink', self.request(paths=['src/link/new.py']))


if __name__ == '__main__':
    unittest.main()
