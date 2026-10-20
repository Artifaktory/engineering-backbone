"""Dependency input/route/approved-check failures; no package commands execute."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import unittest

from jsonschema import Draft202012Validator

from tst import test_navigation as navigation_fixture

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = '.engineering-backbone/dependencies.json'
POLICY = '.engineering-backbone/dependency-policy.md'
COMPATIBILITY = 'src/backend/dependency-compatibility.md'
ARTIFACTS = {
    'manifests': 'src/backend/requirements.in',
    'resolution_files': 'src/backend/requirements.lock',
    'runtime_files': 'src/backend/.python-version',
    'dockerfiles': 'src/backend/Dockerfile',
}


class DependencyTests(unittest.TestCase):
    # Reuse only the navigation fixture, without inheriting its test methods.
    write = navigation_fixture.NavigationTests.write
    write_json = navigation_fixture.NavigationTests.write_json
    install = navigation_fixture.NavigationTests.install
    request = navigation_fixture.NavigationTests.request
    resolve_ok = navigation_fixture.NavigationTests.resolve_ok
    reject = navigation_fixture.NavigationTests.reject
    save_nav = navigation_fixture.NavigationTests.save_nav

    @classmethod
    def setUpClass(cls):
        navigation_fixture.NavigationTests.setUpClass.__func__(cls)
        schema = json.loads((ROOT / '.engineering-backbone/schemas/dependencies.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        cls.schema = Draft202012Validator(schema)

    def setUp(self):
        navigation_fixture.NavigationTests.setUp(self)
        self.write(POLICY, '# Dependency policy\nReviewed compatible resolution and behavior evidence.\n')
        self.write(COMPATIBILITY, '# Compatibility\nLibrary ranges and reproducible test environment.\n')
        for field, path in ARTIFACTS.items():
            self.write(path, 'Declared input for ' + field + '\n')
        self.deps = {
            'schema_version': '1', 'enabled': True,
            'components': [{
                'id': 'backend', 'kind': 'application',
                'compatibility_document': COMPATIBILITY,
                **{field: [path] for field, path in ARTIFACTS.items()},
                'check_ids': ['dependency', 'build', 'test', 'container'],
            }],
        }
        flow = self.workflow()
        flow['checks'].append({'id': 'dependency', 'kind': 'dependency',
                               'argv': ['python', '-c', 'raise SystemExit(8)'],
                               'cwd': '.', 'timeout_seconds': 30, 'phases': ['pr']})
        self.save_workflow(flow)
        self.save_deps()

    def workflow(self):
        return json.loads((self.root / '.engineering-backbone/workflows.json').read_text())

    def save_workflow(self, value, root=None):
        self.write_json('.engineering-backbone/workflows.json', value, root)

    def save_deps(self, root=None):
        self.write_json(CONTRACT, self.deps, root)

    def base(self):
        base = self.workspace / 'approved'
        shutil.copytree(self.root, base)
        return base

    def test_active_contract_routes_exact_bytes_and_effective_checks(self):
        self.schema.validate(self.deps)
        context = self.resolve_ok()
        documents = {item['path']: item['sha256'] for item in context['documents']}
        for name in (CONTRACT, POLICY, COMPATIBILITY, *ARTIFACTS.values()):
            self.assertEqual(documents[name], hashlib.sha256((self.root / name).read_bytes()).hexdigest())
        self.assertTrue({'dependency', 'build', 'test', 'container'} <=
                        {item['id'] for item in context['checks']})
        self.resolve_ok(expected=context)

    def test_every_role_and_task_routes_dependencies_for_selected_component(self):
        for role in navigation_fixture.ROLES:
            packet = json.loads((self.root / 'plans/task.json').read_text())
            packet['role'] = role
            self.write_json('plans/task.json', packet)
            for task in navigation_fixture.TASKS:
                with self.subTest(role=role, task=task):
                    context = self.resolve_ok(self.request(task_type=task, paths=[], components=['backend']))
                    self.assertTrue({CONTRACT, POLICY, COMPATIBILITY, *ARTIFACTS.values()} <=
                                    {item['path'] for item in context['documents']})

    def test_unselected_components_receive_policy_and_contract_but_not_other_artifacts(self):
        context = self.resolve_ok(self.request(paths=['scripts/windows/build.ps1']))
        paths = {item['path'] for item in context['documents']}
        self.assertTrue({CONTRACT, POLICY} <= paths)
        self.assertFalse(set(ARTIFACTS.values()) & paths)
        self.assertNotIn(COMPATIBILITY, paths)
        self.assertNotIn('dependency', {item['id'] for item in context['checks']})

    def test_dependency_artifact_request_selects_its_component(self):
        for name in (COMPATIBILITY, *ARTIFACTS.values()):
            with self.subTest(path=name):
                context = self.resolve_ok(self.request(paths=[name]))
                self.assertEqual(context['components'], ['backend'])
                self.assertIn('dependency', {item['id'] for item in context['checks']})

    def test_legacy_absence_and_inactive_empty_seed_need_no_dependencies(self):
        (self.root / CONTRACT).unlink()
        original_context = self.resolve_ok()
        self.assertNotIn(POLICY, {item['path'] for item in original_context['documents']})
        self.deps.update(enabled=False, components=[])
        self.save_deps()
        self.schema.validate(self.deps)
        (self.root / POLICY).unlink()
        self.assertEqual(original_context, self.resolve_ok())
        (self.root / '.engineering-backbone/navigation.json').unlink()
        (self.root / '.engineering-backbone/quality-profile.json').unlink()
        (self.root / '.engineering-backbone/workflows.json').unlink()
        self.assertEqual(self.resolve(self.root), {'errors': [], 'context': None})

    def test_inactive_seed_checks_shape_and_referenced_files_without_activation(self):
        self.deps['enabled'] = False
        self.deps['components'][0]['check_ids'] = []
        self.save_deps()
        self.nav['enabled'] = False
        self.save_nav()
        self.assertEqual(self.resolve(self.root)['errors'], [])
        (self.root / ARTIFACTS['manifests']).unlink()
        self.reject('absent')

    def test_library_ranges_allowed_but_application_and_tooling_require_resolution(self):
        component = self.deps['components'][0]
        component.update(kind='library', resolution_files=[])
        self.save_deps()
        self.schema.validate(self.deps)
        self.resolve_ok()
        for kind in ('application', 'tooling'):
            with self.subTest(kind=kind):
                component['kind'] = kind
                self.save_deps()
                self.assertTrue(list(self.schema.iter_errors(self.deps)))
                self.reject('dependency resolution_files')
        component.update(kind='library', manifests=[])
        self.save_deps()
        self.reject('dependency manifests')

    def test_active_dependencies_need_all_active_prerequisites_and_policy(self):
        for name in ('navigation', 'quality-profile', 'workflows'):
            with self.subTest(profile=name):
                path = self.root / '.engineering-backbone' / (name + '.json')
                original = path.read_text()
                value = json.loads(original)
                value['enabled'] = False
                path.write_text(json.dumps(value))
                self.assertTrue(self.resolve(self.root)['errors'])
                path.unlink()
                self.assertTrue(self.resolve(self.root)['errors'])
                path.write_text(original)
        (self.root / POLICY).unlink()
        self.reject('absent')

    def test_missing_empty_nonregular_and_oversized_artifacts_fail(self):
        for name in (COMPATIBILITY, *ARTIFACTS.values()):
            with self.subTest(path=name):
                path = self.root / name
                original = path.read_bytes()
                path.unlink()
                self.reject('absent')
                path.mkdir()
                self.reject('Nonregular')
                path.rmdir()
                path.write_text(' \n')
                self.reject('Empty')
                path.write_bytes(original)
        path = self.root / ARTIFACTS['resolution_files']
        with path.open('wb') as stream:
            stream.truncate(16777217)
        self.reject('oversized')

    def test_artifact_case_symlink_collision_and_unsafe_paths_fail(self):
        component = self.deps['components'][0]
        original = component['manifests'][:]
        for path in ('../outside', '/tmp/a', 'src/backend/CON', 'src/backend/foo.',
                     'src/backend/foo ', 'src/backend/Requirements.in', 'src\\backend\\x',
                     'src/backend/requirements.in#anchor', 'src/backend/foo\nbar'):
            with self.subTest(path=path):
                component['manifests'] = [path]
                self.save_deps()
                self.assertTrue(self.resolve(self.root)['errors'])
        component['manifests'] = original
        self.save_deps()
        self.write('src/backend/REQUIREMENTS.in', 'case collision')
        self.reject('ambiguous')
        (self.root / 'src/backend/REQUIREMENTS.in').unlink()
        path = self.root / ARTIFACTS['manifests']
        path.unlink()
        path.symlink_to(self.root / ARTIFACTS['resolution_files'])
        self.reject('Symlink')

    def test_malformed_duplicate_and_bounded_contracts_fail(self):
        for content in ('null', '{}', '{"enabled":true,"enabled":false}'):
            with self.subTest(content=content):
                self.write(CONTRACT, content)
                self.assertTrue(self.resolve(self.root)['errors'])
        original = copy.deepcopy(self.deps)
        changes = [lambda d: d.update(schema_version='2'),
                   lambda d: d.update(enabled=1),
                   lambda d: d.update(unknown=[]),
                   lambda d: d.update(components=[]),
                   lambda d: d.update(components=d['components'] * 257),
                   lambda d: d['components'].append(copy.deepcopy(d['components'][0])),
                   lambda d: d['components'][0].update(kind='unknown'),
                   lambda d: d['components'][0].update(kind=[]),
                   lambda d: d['components'][0].update(manifests=None),
                   lambda d: d['components'][0].update(manifests=[ARTIFACTS['manifests']] * 2),
                   lambda d: d['components'][0].update(check_ids=['test'] * 101),
                   lambda d: d['components'][0].update(check_ids=['test', 'test']),
                   lambda d: d['components'][0].update(check_ids=['unsafe/id'])]
        for change in changes:
            self.deps = copy.deepcopy(original)
            change(self.deps)
            self.save_deps()
            self.assertTrue(self.resolve(self.root)['errors'], self.deps)

    def test_component_identity_and_all_reference_prefixes_are_required(self):
        component = self.deps['components'][0]
        component['id'] = 'unknown'
        self.save_deps()
        self.reject('Unknown dependency navigation component')
        component['id'] = 'backend'
        for field in ('compatibility_document', *ARTIFACTS):
            with self.subTest(field=field):
                original = copy.deepcopy(component[field])
                self.write('docs/external-input.txt', '# Unmapped dependency input\n')
                component[field] = 'docs/external-input.txt' if field == 'compatibility_document' else ['docs/external-input.txt']
                self.save_deps()
                self.reject('outside its component navigation paths')
                component[field] = original
        self.save_deps()
        self.nav['components'][0]['paths'].append('docs/external-input.txt')
        self.save_nav()
        component['runtime_files'].append('docs/external-input.txt')
        self.save_deps()
        self.resolve_ok()

    def test_every_required_check_kind_and_pr_phase_is_enforced(self):
        component = self.deps['components'][0]
        original = component['check_ids'][:]
        for kind in ('dependency', 'build', 'test', 'container'):
            with self.subTest(kind=kind):
                component['check_ids'] = [item for item in original if item != kind]
                self.save_deps()
                self.reject('dependency check-kind coverage')
        component['check_ids'] = original + ['unknown']
        self.save_deps()
        self.reject('Dependency check binding')
        component['check_ids'] = original
        self.save_deps()
        flow = self.workflow()
        next(item for item in flow['checks'] if item['id'] == 'dependency')['phases'] = ['maintenance']
        self.save_workflow(flow)
        self.reject('PR workflow check')

    def test_no_container_check_needed_without_declared_dockerfiles(self):
        component = self.deps['components'][0]
        component['dockerfiles'] = []
        component['check_ids'].remove('container')
        self.save_deps()
        self.resolve_ok()

    def test_activation_requires_complete_reviewed_seed_and_enabled_only_change(self):
        base = self.base()
        (base / CONTRACT).unlink()
        self.reject('already reviewed inactive seed', trusted_base=base)
        self.write_json(CONTRACT, dict(self.deps, enabled=False), base)
        self.resolve_ok(trusted_base=base)
        self.deps['components'][0]['runtime_files'].append('src/backend/main.py')
        self.save_deps()
        self.reject('match the reviewed seed', trusted_base=base)
        self.deps['components'][0]['runtime_files'].pop()
        self.save_deps()
        seed = copy.deepcopy(self.deps)
        seed.update(enabled=False)
        seed['components'][0]['check_ids'].remove('dependency')
        self.write_json(CONTRACT, seed, base)
        self.reject('dependency check-kind coverage', trusted_base=base)

    def test_active_inheritance_rejects_removal_disablement_kind_and_reference_weakening(self):
        base = self.base()
        (self.root / CONTRACT).unlink()
        self.reject('cannot be removed or disabled', trusted_base=base)
        original = copy.deepcopy(self.deps)
        changes = [lambda d: d.update(enabled=False),
                   lambda d: d.update(components=[]),
                   lambda d: d['components'][0].update(kind='library'),
                   lambda d: d['components'][0].update(compatibility_document='src/backend/AGENTS.md'),
                   lambda d: d['components'][0].update(manifests=['src/backend/main.py']),
                   lambda d: d['components'][0].update(resolution_files=['src/backend/main.py']),
                   lambda d: d['components'][0].update(runtime_files=[]),
                   lambda d: d['components'][0].update(dockerfiles=[])]
        for change in changes:
            self.deps = copy.deepcopy(original)
            change(self.deps)
            self.save_deps()
            self.assertTrue(self.resolve(self.root, base)['errors'], self.deps)
        self.deps = copy.deepcopy(original)
        self.deps['components'][0]['check_ids'].append('lint')
        self.save_deps(base)
        self.deps['components'][0]['check_ids'].remove('lint')
        self.save_deps()
        self.reject('Inherited dependency artifacts or check bindings', trusted_base=base)

    def test_active_inheritance_allows_additive_artifacts_and_components(self):
        base = self.base()
        self.write('src/backend/extra.lock', 'reviewed additional environment\n')
        self.deps['components'][0]['resolution_files'].append('src/backend/extra.lock')
        self.save_deps()
        context = self.resolve_ok(trusted_base=base)
        self.assertIn('src/backend/extra.lock', {item['path'] for item in context['documents']})

    def test_approved_check_definition_is_the_executed_and_hashed_authority(self):
        base = self.base()
        flow = self.workflow()
        old_check = copy.deepcopy(next(item for item in flow['checks'] if item['id'] == 'dependency'))
        next(item for item in flow['checks'] if item['id'] == 'dependency').update(
            kind='lint', argv=['python', '-c', 'pass'], phases=['maintenance'])
        self.save_workflow(flow)
        context = self.resolve_ok(trusted_base=base)
        self.assertEqual(next(item for item in context['checks'] if item['id'] == 'dependency'), old_check)

    def test_candidate_kind_cannot_upgrade_an_existing_approved_check(self):
        self.deps['components'][0]['check_ids'].append('reserved')
        flow = self.workflow()
        flow['checks'].append(dict(flow['checks'][-1], id='reserved', kind='lint'))
        self.save_workflow(flow)
        self.save_deps()
        base = self.base()
        # New component needs a dependency check. Candidate tries to reclassify
        # a reserved existing lint ID; workflow preparation still executes lint.
        new = copy.deepcopy(self.deps['components'][0])
        new.update(id='windows-shell', compatibility_document='scripts/windows/compatibility.md')
        for field in ARTIFACTS:
            new[field] = []
        new.update(manifests=['scripts/windows/packages.json'],
                   resolution_files=['scripts/windows/packages.lock'],
                   check_ids=['reserved', 'build', 'test'])
        for path in (new['compatibility_document'], *new['manifests'], *new['resolution_files']):
            self.write(path, '# Reviewed input\n')
        self.deps['components'].append(new)
        next(item for item in flow['checks'] if item['id'] == 'reserved')['kind'] = 'dependency'
        self.save_workflow(flow)
        self.save_deps()
        self.reject('dependency check-kind coverage', trusted_base=base)
        # A genuinely new ID retains its candidate definition and is reviewable.
        flow['checks'].append(dict(flow['checks'][-1], id='new-dependency', kind='dependency'))
        new['check_ids'][0] = 'new-dependency'
        self.save_workflow(flow)
        self.save_deps()
        self.resolve_ok(trusted_base=base)

    def test_stale_contract_policy_and_each_artifact_receipt_is_rejected(self):
        context = self.resolve_ok()
        for name in (CONTRACT, POLICY, COMPATIBILITY, *ARTIFACTS.values()):
            with self.subTest(path=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b'\n')
                self.reject('differs from recomputed', self.request(), expected=context)
                path.write_bytes(original)
        self.resolve_ok(expected=context)

    def test_binary_resolution_bytes_can_be_bound_without_executing_or_decoding(self):
        path = self.root / ARTIFACTS['resolution_files']
        path.write_bytes(b'\x00\xff\x80lock')
        context = self.resolve_ok()
        actual = next(item['sha256'] for item in context['documents'] if item['path'] == ARTIFACTS['resolution_files'])
        self.assertEqual(actual, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
