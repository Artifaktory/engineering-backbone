"""Exercise the trusted quality guard's real declarations and base boundary."""
import ast
import contextlib
import copy
import csv
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'scripts/quality_framework.py'
HEADERS = ('rule_id', 'requirement_id', 'risk', 'architecture', 'tests',
           'check_ids', 'evidence', 'status')


def check(kind='docs', check_id=None, phases=None):
    return {'id': check_id or kind, 'kind': kind,
            'argv': [sys.executable, '-c', 'raise SystemExit(31)'],
            'cwd': '.', 'timeout_seconds': 5, 'phases': phases or ['pr']}


def workflow(profiles=None, checks=None, runtimes=None):
    return {'schema_version': '1', 'enabled': True,
            'profiles': profiles or ['docs'], 'capabilities': [],
            'runtimes': runtimes or {}, 'checks': checks if checks is not None else [check()]}


def quality(*, enabled=True, profiles=None, checks=None, exceptions=None):
    return {'schema_version': '1', 'enabled': enabled, 'catalog_version': '1.0.0',
            'backbone_ref': 'a' * 40, 'profiles': profiles if profiles is not None else ['baseline'],
            'documents': {'quality_plan': 'docs/quality/quality-plan.md',
                          'test_strategy': 'docs/quality/test-strategy.md',
                          'traceability': 'docs/quality/traceability.csv',
                          'exceptions': 'docs/quality/exceptions.md'},
            'checks': checks if checks is not None else [{'rule_id': 'QUAL-TEST-001', 'check_ids': ['docs']}],
            'exceptions': exceptions or []}


class QualityFrameworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = SOURCE.read_text(encoding='utf-8')
        node = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == 'quality_errors')
        # Match the pinned compiler: execute only the trusted self-contained
        # function, never candidate imports or its guard/schema/catalog source.
        namespace = {}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), namespace)
        cls.guard = staticmethod(namespace['quality_errors'])
        kit_source = ROOT / 'scripts/workflow_kit.py'
        kit_node = next(node for node in ast.parse(kit_source.read_text()).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'workflow_kit_main')
        kit_namespace = {}
        exec(compile(ast.Module(body=[kit_node], type_ignores=[]), str(kit_source), 'exec'), kit_namespace)
        cls.workflow_guard = staticmethod(kit_namespace['workflow_kit_main'])
        cls.sources = json.loads((ROOT / 'standards/sources.json').read_text())
        cls.rules_wrapper = json.loads((ROOT / 'standards/rules.json').read_text())
        cls.rules = {entry['id']: entry for entry in cls.rules_wrapper['rules']}
        cls.catalog_profiles = {entry['id']: entry for entry in
                                [json.loads(path.read_text()) for path in
                                 sorted((ROOT / 'standards/profiles').glob('*.json'))]}
        cls.schema = json.loads((ROOT / 'schemas/quality-profile.schema.json').read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.schema_validator = Draft202012Validator(cls.schema)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='backbone-quality-')
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.candidate = self.workspace / 'candidate'
        self.base = self.workspace / 'base'
        self.candidate.mkdir()
        self.base.mkdir()

    def write_json(self, folder, relative, value):
        path = folder / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
        return path

    def package(self, folder, *, central=False):
        prefix = 'standards' if central else '.engineering-backbone/standards'
        self.write_json(folder, prefix + '/sources.json', self.sources)
        self.write_json(folder, prefix + '/rules.json', self.rules_wrapper)
        for name, value in self.catalog_profiles.items():
            self.write_json(folder, prefix + '/profiles/' + name + '.json', value)

    def trace(self, value):
        bindings = {entry['rule_id']: entry['check_ids'] for entry in value['checks']}
        exceptions = {entry['rule_id']: entry for entry in value['exceptions']}
        rules = sorted({rule_id for profile in value['profiles']
                        for rule_id in self.catalog_profiles[profile]['rules']})
        rows = []
        for rule_id in rules:
            check_ids = bindings.get(rule_id, exceptions.get(rule_id, {}).get('compensating_check_ids', []))
            rows.append(dict(rule_id=rule_id, requirement_id='REQ-1', risk='Incorrect behavior',
                             architecture='ADR-1', tests='Selected project verification',
                             check_ids=';'.join(check_ids), evidence='', status='planned'))
        return rows

    def write_trace(self, folder, rows):
        buffer = io.StringIO(newline='')
        writer = csv.DictWriter(buffer, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
        path = folder / 'docs/quality/traceability.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(buffer.getvalue(), encoding='utf-8')
        return path

    def install(self, folder, value=None, *, flow=None):
        value = quality() if value is None else value
        self.package(folder)
        self.write_json(folder, '.engineering-backbone/quality-profile.json', value)
        if flow is not False:
            self.write_json(folder, '.engineering-backbone/workflows.json', flow or workflow())
        documents = folder / 'docs/quality'
        documents.mkdir(parents=True, exist_ok=True)
        for name in ('quality-plan.md', 'test-strategy.md', 'exceptions.md'):
            (documents / name).write_text('Project-owned quality declaration.\n', encoding='utf-8')
        self.write_trace(folder, self.trace(value))
        for exception in value['exceptions']:
            path = folder / exception['evidence_path']
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Recorded exception review; identity not authenticated.\n', encoding='utf-8')
        return value

    def assert_ok(self, folder=None, base=None, *, source=False):
        self.assertEqual([], self.guard(folder or self.candidate, base, source=source))

    def assert_rejected(self, phrase=None, folder=None, base=None, *, source=False):
        errors = self.guard(folder or self.candidate, base, source=source)
        self.assertTrue(errors)
        if phrase:
            self.assertIn(phrase, '\n'.join(errors))
        return errors

    def software(self, *, enabled=True, waive=False):
        bindings = [{'rule_id': 'QUAL-TEST-001', 'check_ids': ['docs']},
                    {'rule_id': 'QUAL-SEC-001', 'check_ids': ['sast']}]
        if not waive:
            bindings.append({'rule_id': 'QUAL-SW-001', 'check_ids': ['build', 'lint', 'test', 'sast']})
        exceptions = []
        if waive:
            exceptions = [{'rule_id': 'QUAL-SW-001', 'scope': 'Recorded limited pilot component',
                           'reason': 'Reviewed compensating verification during bounded migration',
                           'owner': 'Project quality owner', 'approved_by': 'Human project owner',
                           'expires_on': '2099-12-31', 'compensating_check_ids': ['docs'],
                           'evidence_path': 'docs/reviews/exception.md'}]
        return quality(enabled=enabled, profiles=['baseline', 'software'], checks=bindings,
                       exceptions=exceptions)

    def software_flow(self):
        return workflow(checks=[check(kind) for kind in ('docs', 'build', 'lint', 'test', 'sast')])

    def test_legacy_absence_and_empty_inactive_seed_remain_compatible(self):
        self.assert_ok(base=self.base)
        seed = quality(enabled=False, profiles=[], checks=[])
        seed['backbone_ref'] = ''
        self.install(self.candidate, seed, flow=False)
        self.assert_ok(base=self.base)
        self.schema_validator.validate(seed)

    def test_existing_candidate_and_base_json_null_are_not_absence(self):
        self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', None)
        self.assert_rejected('missing or unknown keys')
        (self.candidate / '.engineering-backbone/quality-profile.json').unlink()
        self.write_json(self.base, '.engineering-backbone/quality-profile.json', None)
        self.assert_rejected('missing or unknown keys', base=self.base)

    def test_real_current_source_catalog_is_checked_without_project_profile(self):
        self.assert_ok(ROOT, source=True)
        self.package(self.candidate, central=True)
        (self.candidate / 'policy').mkdir()
        for name in ('core.json', 'core.md', 'quality.md', 'dependencies.md'):
            shutil.copyfile(ROOT / 'policy' / name, self.candidate / 'policy' / name)
        self.assert_rejected('Required document or directory absent: standards/technologies/sources.json',
                             source=True)
        shutil.copytree(ROOT / 'standards/technologies',
                        self.candidate / 'standards/technologies')
        self.assert_ok(source=True)
        path = self.candidate / 'standards/rules.json'
        value = json.loads(path.read_text())
        value['rules'][0]['statement'] = 'Candidate-owned rule override'
        path.write_text(json.dumps(value))
        self.assert_rejected('differs from trusted authority', source=True)

    def test_complete_profile_and_schema_validate_without_executing_commands(self):
        value = self.install(self.candidate)
        self.schema_validator.validate(value)
        marker = self.workspace / 'executed'
        flow = workflow()
        flow['checks'][0]['argv'] = [sys.executable, '-c',
                                   'from pathlib import Path; Path(' + repr(str(marker)) + ').touch()']
        self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
        self.assert_ok()
        self.assertFalse(marker.exists())

    def test_activation_requires_identical_complete_reviewed_inactive_seed(self):
        value = quality()
        seed = dict(value, enabled=False)
        self.install(self.base, seed)
        self.install(self.candidate, value)
        self.assert_ok(base=self.base)
        changed = copy.deepcopy(value)
        changed['backbone_ref'] = 'b' * 40
        self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', changed)
        self.assert_rejected('except enabled', base=self.base)
        self.install(self.candidate, value)
        seed['profiles'] = []
        seed['checks'] = []
        self.install(self.base, seed)
        self.assert_rejected('requires baseline', base=self.base)

    def test_activation_cannot_manufacture_a_trusted_base(self):
        self.install(self.candidate)
        self.assert_rejected('already reviewed inactive seed', base=self.base)

    def test_active_adoption_cannot_be_removed_disabled_or_downgraded(self):
        value = self.software()
        self.install(self.base, value, flow=self.software_flow())
        for mode in ('removed', 'disabled', 'profile', 'binding'):
            with self.subTest(mode=mode):
                self.install(self.candidate, value, flow=self.software_flow())
                candidate = copy.deepcopy(value)
                if mode == 'removed':
                    (self.candidate / '.engineering-backbone/quality-profile.json').unlink()
                elif mode == 'disabled':
                    candidate['enabled'] = False
                    self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', candidate)
                elif mode == 'profile':
                    self.install(self.candidate, quality(), flow=self.software_flow())
                else:
                    candidate['checks'][-1]['check_ids'].remove('lint')
                    self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', candidate)
                self.assert_rejected(base=self.base)

    def test_reviewed_base_check_kinds_remain_current_execution_authority(self):
        value = self.software()
        self.install(self.base, value, flow=self.software_flow())
        flow = self.software_flow()
        flow['checks'][2]['kind'] = 'test'  # ID lint changed at candidate only.
        flow['checks'].append(check('lint', check_id='replacement-lint'))
        self.install(self.candidate, value, flow=flow)
        # Without a base, the bound lint ID has no lint kind and is rejected.
        self.assert_rejected('check-kind coverage')
        # In this PR the approved old lint definition remains authoritative.
        self.assert_ok(base=self.base)

    def test_managed_catalog_poisoning_in_candidate_or_coherent_base_is_rejected(self):
        value = self.install(self.candidate)
        self.install(self.base, value)
        for folder in (self.candidate, self.base):
            with self.subTest(folder=folder.name):
                self.package(self.candidate)
                self.package(self.base)
                path = folder / '.engineering-backbone/standards/rules.json'
                modified = json.loads(path.read_text())
                modified['rules'][3]['check_kind_groups'] = []
                path.write_text(json.dumps(modified))
                self.assert_rejected('differs from trusted authority', base=self.base)

    def test_catalog_formatting_is_not_rule_authority(self):
        self.install(self.candidate)
        for path in (self.candidate / '.engineering-backbone/standards').rglob('*.json'):
            value = json.loads(path.read_text())
            value = dict(reversed(list(value.items())))
            path.write_text(json.dumps(value, separators=(',', ':')) + '\r\n')
        self.assert_ok()

    def test_catalog_bundle_must_be_complete_without_extra_profiles(self):
        self.install(self.candidate)
        path = self.candidate / '.engineering-backbone/standards/profiles/baseline.json'
        path.unlink()
        self.assert_rejected('profile files differ')
        self.package(self.candidate)
        self.write_json(self.candidate, '.engineering-backbone/standards/profiles/unknown.json', {})
        self.assert_rejected('profile files differ')

    def test_reference_only_profiles_and_unknown_versions_cannot_activate(self):
        for profile in ('cpp17', 'iec61508', 'iec62304'):
            with self.subTest(profile=profile):
                value = quality(profiles=['baseline', profile])
                self.install(self.candidate, value)
                self.assert_rejected('Reference-only')
                self.assertTrue(list(self.schema_validator.iter_errors(value)))
        value = quality()
        value['catalog_version'] = '2.0.0'
        self.install(self.candidate, value)
        self.assert_rejected('not trusted')

    def test_active_profile_requires_baseline_full_pin_and_documents(self):
        for mutation in ('baseline', 'pin', 'document', 'empty', 'absent'):
            with self.subTest(mutation=mutation):
                value = self.install(self.candidate)
                if mutation == 'baseline':
                    value['profiles'] = []
                    value['checks'] = []
                elif mutation == 'pin':
                    value['backbone_ref'] = ''
                elif mutation == 'document':
                    value['documents']['test_strategy'] = ''
                elif mutation == 'empty':
                    (self.candidate / value['documents']['quality_plan']).write_text('  \n')
                else:
                    (self.candidate / value['documents']['quality_plan']).unlink()
                self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                self.assert_rejected()

    def test_binding_requires_real_active_complete_pr_workflow(self):
        for mutation in ('absent', 'null', 'disabled', 'incomplete', 'unknown', 'maintenance'):
            with self.subTest(mutation=mutation):
                value = self.install(self.candidate)
                flow = workflow()
                if mutation == 'absent':
                    (self.candidate / '.engineering-backbone/workflows.json').unlink()
                elif mutation == 'null':
                    self.write_json(self.candidate, '.engineering-backbone/workflows.json', None)
                elif mutation == 'disabled':
                    flow['enabled'] = False
                    self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
                elif mutation == 'incomplete':
                    flow['checks'] = []
                    self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
                elif mutation == 'unknown':
                    value['checks'][0]['check_ids'] = ['invented']
                    self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                else:
                    flow['checks'].append(check('dependency', check_id='nightly', phases=['maintenance']))
                    self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
                    value['checks'][0]['check_ids'] = ['nightly']
                    self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                self.assert_rejected()

    def test_dependency_capability_matches_existing_workflow_kit_contract(self):
        # The capability is plural, but the executable check kind is singular.
        # Compare actual independently compiled guards, including both required
        # phases, for active quality profiles and otherwise-valid inactive seeds.
        for enabled in (False, True):
            for phases in (['pr', 'maintenance'], ['pr'], ['maintenance']):
                with self.subTest(enabled=enabled, dependency_phases=phases):
                    flow = workflow(checks=[check(), check('dependency', phases=phases)])
                    flow['capabilities'] = ['dependencies']
                    self.install(self.candidate, quality(enabled=enabled), flow=flow)
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        kit_result = self.workflow_guard(['validate', '--root', str(self.candidate)])
                    expected = 0 if set(phases) == {'pr', 'maintenance'} else 1
                    self.assertEqual(expected, kit_result, output.getvalue())
                    errors = self.guard(self.candidate)
                    if expected == 0:
                        self.assertEqual([], errors)
                    else:
                        self.assertTrue(errors)
                        self.assertIn('Required workflow checks are missing', '\n'.join(errors))

    def test_python_and_typescript_profiles_require_matching_real_workflow_profiles(self):
        for language, kinds, runtimes in [('python', ['build', 'lint', 'test', 'sast'], {'python': '3.12'}),
                                           ('typescript', ['build', 'lint', 'test', 'sast', 'typecheck'], {'node': '24'})]:
            with self.subTest(language=language):
                rule_id = 'QUAL-PY-001' if language == 'python' else 'QUAL-TS-001'
                required = ['lint', 'test'] + (['typecheck'] if language == 'typescript' else [])
                value = quality(profiles=['baseline', language], checks=[
                    {'rule_id': 'QUAL-TEST-001', 'check_ids': ['test']},
                    {'rule_id': rule_id, 'check_ids': required}])
                flow = workflow(profiles=[language], checks=[check(kind) for kind in kinds], runtimes=runtimes)
                self.install(self.candidate, value, flow=flow)
                self.assert_ok()
                flow['profiles'] = ['docs']
                flow['checks'].append(check())
                self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
                self.assert_rejected('language workflow profile')

    def test_traceability_requires_exact_columns_and_every_selected_rule(self):
        value = self.install(self.candidate)
        path = self.write_trace(self.candidate, self.trace(value)[:-1])
        self.assert_rejected('every selected rule')
        path.write_text(','.join(HEADERS) + '\n')
        self.assert_rejected('every selected rule')
        path.write_text(','.join(reversed(HEADERS)) + '\n')
        self.assert_rejected('columns')
        path.write_text(','.join(HEADERS) + ',claim\n')
        self.assert_rejected('columns')

    def test_traceability_cannot_invent_rule_check_or_verification_status(self):
        value = self.install(self.candidate)
        for mutation in ('rule', 'check', 'status', 'missing-check', 'unbound-check'):
            with self.subTest(mutation=mutation):
                rows = self.trace(value)
                row = next(row for row in rows if row['rule_id'] == 'QUAL-TEST-001')
                if mutation == 'rule':
                    row['rule_id'] = 'QUAL-NONE-001'
                elif mutation == 'check':
                    row['check_ids'] = 'invented'
                elif mutation == 'status':
                    row['status'] = 'certified'
                elif mutation == 'missing-check':
                    row['check_ids'] = ''
                else:
                    rows[0]['check_ids'] = 'docs'
                self.write_trace(self.candidate, rows)
                self.assert_rejected()

    def test_planned_and_gap_rows_are_declarations_not_fabricated_semantic_pass(self):
        value = self.install(self.candidate)
        rows = self.trace(value)
        rows[0]['status'] = 'gap'
        rows[0]['evidence'] = 'artifacts/not-yet-executed.txt'
        self.write_trace(self.candidate, rows)
        self.assert_ok()

    def test_verified_rows_require_existing_nonempty_regular_safe_evidence(self):
        value = self.install(self.candidate)
        rows = self.trace(value)
        rows[0]['status'] = 'verified'
        self.write_trace(self.candidate, rows)
        self.assert_rejected('evidence file')
        rows[0]['evidence'] = 'docs/reviews/result.txt'
        self.write_trace(self.candidate, rows)
        self.assert_rejected('absent')
        result = self.candidate / 'docs/reviews/result.txt'
        result.parent.mkdir(parents=True)
        result.write_text('')
        self.assert_rejected('empty')
        result.write_text('Actual reviewer must independently assess this evidence.')
        self.assert_ok()
        result.unlink()
        result.mkdir()
        self.assert_rejected('regular file')

    def test_binary_regular_evidence_and_short_document_names_are_valid(self):
        value = self.install(self.candidate)
        value['documents']['quality_plan'] = 'a'
        (self.candidate / 'a').write_text('Project quality plan')
        self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
        self.schema_validator.validate(value)
        rows = self.trace(value)
        rows[0].update(status='verified', evidence='docs/reviews/result.png')
        path = self.candidate / 'docs/reviews/result.png'
        path.parent.mkdir(parents=True)
        path.write_bytes(b'\x89PNG\r\n\x00binary evidence')
        self.write_trace(self.candidate, rows)
        self.assert_ok()
        path.write_bytes(b'')
        self.assert_rejected('empty')

    def test_json_duplicate_keys_unknown_fields_and_size_are_rejected(self):
        value = self.install(self.candidate)
        path = self.candidate / '.engineering-backbone/quality-profile.json'
        path.write_text(json.dumps(value)[:-1] + ',"enabled":true}')
        self.assert_rejected('Duplicate JSON')
        self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', dict(value, claim='certified'))
        self.assert_rejected('unknown keys')
        path.write_text(' ' * 262145)
        self.assert_rejected('size limit')
        self.install(self.candidate)
        path = self.candidate / '.engineering-backbone/standards/sources.json'
        path.write_text('{"schema_version":"1","schema_version":"1"}')
        self.assert_rejected('Duplicate JSON')

    def test_document_paths_reject_traversal_absolute_machine_and_control_paths(self):
        for path in ('../escape.md', '/tmp/file.md', 'C:/file.md', 'docs\\file.md',
                     'docs/./file.md', 'docs//file.md', 'docs/../file.md', 'docs/file\x00.md'):
            with self.subTest(path=repr(path)):
                value = self.install(self.candidate)
                value['documents']['quality_plan'] = path
                self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                self.assert_rejected()

    @unittest.skipUnless(hasattr(os, 'symlink'), 'Filesystem lacks symlinks')
    def test_symlink_root_ancestors_catalog_documents_and_evidence_are_rejected(self):
        value = self.install(self.candidate)
        root_alias = self.workspace / 'alias'
        root_alias.symlink_to(self.candidate, target_is_directory=True)
        self.assert_rejected('Symlink', folder=root_alias)
        document = self.candidate / value['documents']['quality_plan']
        target = self.workspace / 'external.txt'
        target.write_text('External')
        document.unlink()
        document.symlink_to(target)
        self.assert_rejected('Symlink')
        document.unlink()
        document.write_text('Restored')
        catalog = self.candidate / '.engineering-backbone/standards/rules.json'
        external_catalog = self.workspace / 'catalog.json'
        external_catalog.write_bytes(catalog.read_bytes())
        catalog.unlink()
        catalog.symlink_to(external_catalog)
        self.assert_rejected('Symlink')
        catalog.unlink()
        self.package(self.candidate)
        rows = self.trace(value)
        rows[0].update(status='verified', evidence='evidence/result.txt')
        external = self.workspace / 'evidence'
        external.mkdir()
        (external / 'result.txt').write_text('External evidence')
        (self.candidate / 'evidence').symlink_to(external, target_is_directory=True)
        self.write_trace(self.candidate, rows)
        self.assert_rejected('Symlink')

    def test_malformed_workflow_values_cannot_crash_or_supply_bindings(self):
        for key, wrong in [('kind', []), ('argv', None), ('phases', ['pr', 'pr']),
                           ('timeout_seconds', True), ('cwd', {'path': '.'})]:
            with self.subTest(key=key):
                self.install(self.candidate)
                flow = workflow()
                flow['checks'][0][key] = wrong
                self.write_json(self.candidate, '.engineering-backbone/workflows.json', flow)
                self.assert_rejected()

    def test_reference_duplicate_selections_and_binding_ids_are_rejected(self):
        for mutate in ('pin', 'profile', 'rule', 'check'):
            with self.subTest(mutate=mutate):
                value = self.install(self.candidate)
                if mutate == 'pin':
                    value['backbone_ref'] = 'main'
                elif mutate == 'profile':
                    value['profiles'].append('baseline')
                elif mutate == 'rule':
                    value['checks'].append(value['checks'][0])
                else:
                    value['checks'][0]['check_ids'].append('docs')
                self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                self.assert_rejected()

    def test_reviewed_exception_seed_activates_and_preserves_compensating_checks(self):
        value = self.software(waive=True)
        self.install(self.base, dict(value, enabled=False), flow=self.software_flow())
        self.install(self.candidate, value, flow=self.software_flow())
        self.assert_ok(base=self.base)
        self.schema_validator.validate(value)
        value['exceptions'][0]['compensating_check_ids'] = ['invented']
        self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
        self.assert_rejected(base=self.base)

    def test_baseline_exceptions_empty_metadata_expiry_and_evidence_are_rejected(self):
        for mutation in ('baseline', 'owner', 'expired', 'date', 'document', 'evidence', 'check'):
            with self.subTest(mutation=mutation):
                value = self.software(waive=True)
                self.install(self.candidate, value, flow=self.software_flow())
                exception = value['exceptions'][0]
                if mutation == 'baseline':
                    exception['rule_id'] = 'QUAL-TEST-001'
                elif mutation == 'owner':
                    exception['owner'] = ''
                elif mutation == 'expired':
                    exception['expires_on'] = '2000-01-01'
                elif mutation == 'date':
                    exception['expires_on'] = '2099-02-30'
                elif mutation == 'document':
                    value['documents']['exceptions'] = ''
                elif mutation == 'evidence':
                    (self.candidate / exception['evidence_path']).unlink()
                else:
                    exception['compensating_check_ids'] = ['invented']
                self.write_json(self.candidate, '.engineering-backbone/quality-profile.json', value)
                self.assert_rejected()

    def test_active_base_cannot_introduce_or_relax_exception_but_can_remove_it(self):
        value = self.software()
        self.install(self.base, value, flow=self.software_flow())
        candidate = copy.deepcopy(value)
        candidate['exceptions'] = self.software(waive=True)['exceptions']
        self.install(self.candidate, candidate, flow=self.software_flow())
        self.assert_rejected('cannot introduce', base=self.base)
        self.install(self.base, candidate, flow=self.software_flow())
        self.install(self.candidate, value, flow=self.software_flow())
        self.assert_ok(base=self.base)
        candidate['exceptions'][0]['expires_on'] = '2099-12-30'
        self.install(self.candidate, candidate, flow=self.software_flow())
        self.assert_rejected('cannot introduce', base=self.base)

    def test_expired_base_exception_can_be_repaired_by_removal_not_carried_forward(self):
        value = self.software()
        expired = copy.deepcopy(value)
        expired['exceptions'] = self.software(waive=True)['exceptions']
        expired['exceptions'][0]['expires_on'] = '2000-01-01'
        self.install(self.base, expired, flow=self.software_flow())
        self.install(self.candidate, expired, flow=self.software_flow())
        self.assert_rejected('expired', base=self.base)
        self.install(self.candidate, value, flow=self.software_flow())
        self.assert_ok(base=self.base)

    def test_trace_csv_malformed_rows_controls_and_oversized_docs_are_rejected(self):
        value = self.install(self.candidate)
        path = self.candidate / value['documents']['traceability']
        path.write_text(','.join(HEADERS) + '\nQUAL-TEST-001,too,few\n')
        self.assert_rejected('malformed')
        rows = self.trace(value)
        rows[0]['risk'] = 'risk\x00value'
        self.write_trace(self.candidate, rows)
        self.assert_rejected('NUL')
        self.install(self.candidate)
        (self.candidate / value['documents']['test_strategy']).write_bytes(b'x' * 1048577)
        self.assert_rejected('size limit')


if __name__ == '__main__':
    unittest.main()
