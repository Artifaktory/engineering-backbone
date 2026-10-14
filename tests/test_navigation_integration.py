"""Exercise compiled navigation authority and real optional consumer upgrades.

These checks prove installed bytes, isolated guard execution and preservation.
They do not claim native provider discovery or execution of technology toolchains.
"""
from __future__ import annotations

import ast
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

from copier import run_copy, run_update
from jsonschema import Draft202012Validator
import yaml

from tests.test_quality_copier import commit, git, initialize
from tests.test_quality_framework import HEADERS, check, quality, workflow


ROOT = Path(__file__).resolve().parents[1]
NAVIGATION = '.engineering-backbone/navigation.json'
ASSETS = (
    NAVIGATION,
    '.engineering-backbone/navigation-guide.md',
    '.engineering-backbone/navigation.schema.json',
    '.engineering-backbone/navigation-request.schema.json',
    '.engineering-backbone/technology-guide.md',
)
COMPILER_FILES = (
    'scripts/navigation.py', 'scripts/quality_framework.py', 'scripts/validate.py',
    '.github/workflows/governance-checks.yml',
)


def isolated_guard(content):
    """Load only the reviewed guard function, with no module-level execution."""
    nodes = [node for node in ast.parse(content).body
             if isinstance(node, ast.FunctionDef) and node.name == 'quality_errors']
    if len(nodes) != 1:
        raise AssertionError('Expected one compiled quality guard')
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]),
                 'reviewed-navigation-integration-guard', 'exec'), namespace)
    return namespace['quality_errors']


class NavigationCompilerIntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-navigation-compiler-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.source = self.workspace / 'source'
        shutil.copytree(ROOT / 'standards', self.source / 'standards')
        for relative in COMPILER_FILES:
            destination = self.source / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def compile(self, script, mode):
        return subprocess.run(
            [sys.executable, '-I', str(ROOT / 'scripts' / script), mode,
             '--source', str(self.source)], cwd=self.workspace,
            capture_output=True, text=True,
        )

    def assert_compile_ok(self, script, mode):
        result = self.compile(script, mode)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def guards(self):
        for relative in ('scripts/quality_framework.py', 'scripts/validate.py'):
            yield relative, isolated_guard((ROOT / relative).read_text())
        workflow = yaml.safe_load((ROOT / '.github/workflows/governance-checks.yml').read_text())
        step = next(step for step in workflow['jobs']['validate']['steps']
                    if step.get('name') == 'Validate generated consumer with trusted tooling')
        body = step['run'].split('# BEGIN COMPILED QUALITY GUARD\n', 1)[1]
        body = body.split('# END COMPILED QUALITY GUARD', 1)[0]
        yield 'trusted workflow', isolated_guard(textwrap.dedent(body))

    def test_catalog_refresh_propagates_through_both_compilers_deterministically(self):
        for script in ('compile_navigation.py', 'compile_quality_framework.py'):
            self.assert_compile_ok(script, '--check')
        path = self.source / 'standards/technologies/rules.json'
        rules = json.loads(path.read_text())
        rules['rules'][0]['statement'] += ' TECHNOLOGY-FIXTURE-REVISION'
        path.write_text(json.dumps(rules) + '\n')
        stale = self.compile('compile_navigation.py', '--check')
        self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
        for relative in ('scripts/navigation.py', 'scripts/quality_framework.py'):
            self.assertIn(relative, stale.stdout)
        self.assert_compile_ok('compile_navigation.py', '--write')
        stale = self.compile('compile_quality_framework.py', '--check')
        self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
        for relative in ('scripts/validate.py', '.github/workflows/governance-checks.yml'):
            self.assertIn(relative, stale.stdout)
        self.assert_compile_ok('compile_quality_framework.py', '--write')
        compiled = {relative: (self.source / relative).read_bytes() for relative in COMPILER_FILES}
        for relative, content in compiled.items():
            self.assertIn(b'TECHNOLOGY-FIXTURE-REVISION', content, relative)
        for script in ('compile_navigation.py', 'compile_quality_framework.py'):
            self.assert_compile_ok(script, '--check')
            self.assert_compile_ok(script, '--write')
        self.assertEqual(compiled, {relative: (self.source / relative).read_bytes()
                                    for relative in COMPILER_FILES})

    def test_compilation_and_all_guards_ignore_candidate_module_side_effects(self):
        marker = self.workspace / 'candidate-module-executed'
        injection = (f'from pathlib import Path\nPath({str(marker)!r}).touch()\n'
                     'raise RuntimeError("candidate module was imported")\n')
        for relative in ('scripts/navigation.py', 'scripts/quality_framework.py'):
            path = self.source / relative
            path.write_text(path.read_text() + '\n' + injection)
        for script in ('compile_navigation.py', 'compile_quality_framework.py'):
            self.assert_compile_ok(script, '--write')
            self.assert_compile_ok(script, '--check')
        self.assertFalse(marker.exists())
        guards = list(self.guards())
        for name, guard in guards:
            with self.subTest(entry_point=name, state='valid'):
                self.assertEqual(guard(self.source, source=True), [])
                self.assertFalse(marker.exists())
        rules_path = self.source / 'standards/technologies/rules.json'
        value = json.loads(rules_path.read_text())
        value['rules'][0]['statement'] = 'Candidate replaced trusted technology obligations.'
        rules_path.write_text(json.dumps(value) + '\n')
        for name, guard in guards:
            with self.subTest(entry_point=name, state='poisoned authority'):
                errors = guard(self.source, source=True)
                self.assertTrue(errors)
                self.assertIn('Managed technology rules differs from trusted authority', '\n'.join(errors))
                self.assertFalse(marker.exists())


class NavigationCopierIntegrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-navigation-copier-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.source = self.workspace / 'source'
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', 'artifacts', '.venv'))
        initialize(self.source)
        commit(self.source, 'Reviewed navigation fixture v0.1.0')
        git(self.source, 'tag', 'v0.1.0')
        self.counter = 0

    def copy(self, *, target=None, **data):
        if target is None:
            target = self.workspace / ('consumer-' + str(self.counter))
            self.counter += 1
        run_copy(str(self.source), target, data=data, vcs_ref='v0.1.0',
                 defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        return target

    def test_navigation_is_optional_and_installs_inactive_with_all_provider_combinations(self):
        disabled = self.copy(use_codex=False, use_copilot=False)
        for relative in ASSETS + ('.engineering-backbone/standards/technologies',):
            self.assertFalse((disabled / relative).exists(), relative)
        for codex, copilot in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(codex=codex, copilot=copilot):
                target = self.copy(use_quality_framework=True, use_codex=codex, use_copilot=copilot)
                for relative in ASSETS:
                    self.assertTrue((target / relative).is_file(), relative)
                seed = json.loads((target / NAVIGATION).read_text())
                self.assertFalse(seed['enabled'])
                self.assertEqual(seed['components'], [])
                schema = json.loads((target / ASSETS[2]).read_text())
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema).validate(seed)
                for name in ('navigation', 'navigation-request'):
                    self.assertEqual(
                        (target / '.engineering-backbone' / (name + '.schema.json')).read_text().strip(),
                        (self.source / 'schemas' / (name + '.schema.json')).read_text().strip())
                source_catalog = self.source / 'standards/technologies'
                installed_catalog = target / '.engineering-backbone/standards/technologies'
                expected = {path.relative_to(source_catalog): json.loads(path.read_text())
                            for path in source_catalog.rglob('*.json')}
                actual = {path.relative_to(installed_catalog): json.loads(path.read_text())
                          for path in installed_catalog.rglob('*.json')}
                self.assertEqual(expected, actual)
                result = subprocess.run(
                    [sys.executable, '-I', str(target / '.engineering-backbone/quality-guard.py'),
                     'validate', '--root', str(target)], cwd=target,
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('navigation.json', (target / '.engineering-backbone/AGENTS.fragment.md').read_text())
                if codex:
                    for path in (target / '.codex/agents').glob('*.toml'):
                        self.assertIn('navigation.json', path.read_text(), str(path.relative_to(target)))
                if copilot:
                    native = [target / '.github/copilot-instructions.md']
                    native.extend((target / '.github/agents').glob('*.agent.md'))
                    native.extend((target / '.github/skills').glob('*/SKILL.md'))
                    for path in native:
                        self.assertIn('navigation.json', path.read_text(), str(path.relative_to(target)))

    def test_copy_and_update_preserve_project_navigation_and_native_instructions(self):
        target = self.workspace / 'preserved'
        target.mkdir()
        seed_template = (self.source / 'templates/.engineering-backbone' /
                         '{% if use_quality_framework %}navigation.json{% endif %}.jinja')
        seed = json.loads(seed_template.read_text())
        seed['documents'] = {'project': 'docs/project-navigation.md'}
        seed['always'] = ['project']
        protected = {
            NAVIGATION: json.dumps(seed, indent=4) + '\n',
            'docs/project-navigation.md': '# Local navigation\nRetain stronger routing obligations.\n',
            'AGENTS.md': '# Local instructions\nPreserve the project authority.\n',
            '.github/agents/backbone-reviewer.agent.md': 'Preserved stronger local reviewer contract.\n',
        }
        for relative, content in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.copy(target=target, use_quality_framework=True)
        initialize(target)
        commit(target, 'Project-owned navigation and instructions')
        guide = self.source / 'docs/agent-navigation.md'
        guide.write_text(guide.read_text() + '\nReviewed navigation guide fixture update.\n')
        commit(self.source, 'Reviewed navigation fixture v0.2.0')
        git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True,
                   overwrite=True, skip_tasks=True)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_text(), content, relative)
        self.assertIn('Reviewed navigation guide fixture update.',
                      (target / '.engineering-backbone/navigation-guide.md').read_text())
        self.assertFalse(json.loads((target / NAVIGATION).read_text())['enabled'])

    def active_cli_fixture(self):
        target = self.copy(use_quality_framework=True, use_workflow_kit=True,
                           use_codex=False, use_copilot=False)
        marker = self.workspace / 'declared-check-executed'

        def write(relative, content):
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return path

        def write_json(relative, value):
            return write(relative, json.dumps(value, indent=2) + '\n')

        declarations = quality()
        write_json('.engineering-backbone/quality-profile.json', declarations)
        checks = [check('docs'), check('lint')]
        for item in checks:
            item['argv'] = [sys.executable, '-c',
                            f'from pathlib import Path; Path({str(marker)!r}).touch()']
        write_json('.engineering-backbone/workflows.json', workflow(checks=checks))
        baseline = json.loads((self.source / 'standards/profiles/baseline.json').read_text())
        rows = io.StringIO(newline='')
        writer = csv.DictWriter(rows, fieldnames=HEADERS)
        writer.writeheader()
        for rule_id in baseline['rules']:
            writer.writerow({
                'rule_id': rule_id, 'requirement_id': 'CLI-1', 'risk': 'Incomplete handoff',
                'architecture': 'Explicit routing', 'tests': 'Installed CLI structural fixture',
                'check_ids': 'docs' if rule_id == 'QUAL-TEST-001' else '',
                'evidence': '', 'status': 'planned',
            })
        write(declarations['documents']['traceability'], rows.getvalue())
        navigation = json.loads((target / NAVIGATION).read_text())
        navigation.update(enabled=True, documents={'design': 'docs/design.md#contract'},
                          always=['design'], components=[{
                              'id': 'configuration', 'paths': ['config'], 'profiles': ['json'],
                              'documents': [], 'checks': [{
                                  'rule_id': 'TECH-JSON-001', 'check_ids': ['lint']}],
                          }])
        write_json(NAVIGATION, navigation)
        write('docs/design.md', '# Design\n## Contract\nRetain the parser schema.\n')
        write('config/settings.json', '{"value": 1}\n')
        packet = json.loads((self.source / 'plans/technology-navigation-task.json').read_text())
        packet.update(id='CLI-1', role='implementer', status='active')
        packet['repository']['head_revision'] = 'c' * 40
        packet['scope'] = {'include': ['config/**'], 'exclude': []}
        write_json('plans/task.json', packet)
        request = write_json('plans/request.json', {
            'schema_version': '1', 'task_packet': 'plans/task.json', 'task_type': 'implementation',
            'paths': ['config/settings.json'], 'components': [], 'revision': 'c' * 40,
        })
        receipt = self.workspace / 'context.json'

        def command(action, request_path=request, expected=None, output=None, trusted_base=None):
            argv = [sys.executable, '-I', str(target / '.engineering-backbone/quality-guard.py'),
                    action, '--root', str(target), '--request', str(request_path)]
            if expected is not None:
                argv.extend(['--expected', str(expected)])
            if output is not None:
                argv.extend(['--output', str(output)])
            if trusted_base is not None:
                argv.extend(['--trusted-base', str(trusted_base)])
            result = subprocess.run(argv, cwd=target, capture_output=True, text=True)
            self.assertFalse(marker.exists(), 'Context routing executed a declared project check')
            return result

        return target, command, receipt, write_json

    def test_installed_cli_resolves_and_verifies_without_executing_checks(self):
        target, command, receipt, write_json = self.active_cli_fixture()
        resolved = command('resolve', output=receipt)
        self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
        context = json.loads(receipt.read_text())
        self.assertEqual(context['technology_profiles'], [{'id': 'json', 'version': '1'}])
        self.assertEqual(context['runtime_loading'], 'unverified')
        self.assertEqual({item['id'] for item in context['checks']}, {'docs', 'lint'})
        verified = command('verify', expected=receipt)
        self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
        self.assertEqual(json.loads(verified.stdout), context)
        null = write_json('plans/null.json', None)
        invalid_inputs = (
            ('resolve', {'request_path': null}, 'Navigation request must be an object'),
            ('verify', {'expected': null}, 'Expected handoff context must be an object'),
        )
        for action, arguments, message in invalid_inputs:
            with self.subTest(action=action, invalid='null'):
                rejected = command(action, **arguments)
                self.assertNotEqual(rejected.returncode, 0)
                self.assertIn(message, rejected.stdout)
        alias = self.workspace / 'linked-input-directory'
        alias.symlink_to(target / 'plans', target_is_directory=True)
        rejected = command('resolve', request_path=alias / 'request.json')
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('linked', rejected.stdout)
        design = target / 'docs/design.md'
        design.write_text(design.read_text() + 'A reviewed design change requires a new handoff.\n')
        stale = command('verify', expected=receipt)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn('Handoff context differs from recomputed snapshot', stale.stdout)

    def test_installed_cli_binds_mandatory_project_and_core_facts(self):
        target, command, receipt, write_json = self.active_cli_fixture()
        resolved = command('resolve', output=receipt)
        self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
        context = json.loads(receipt.read_text())
        documents = {item['path']: item['sha256'] for item in context['documents']}
        declared = json.loads((target / NAVIGATION).read_text())['documents'].values()
        for filename, schema_name in (('project.json', 'project.schema.json'),
                                      ('core.json', 'core-policy.schema.json')):
            relative = '.engineering-backbone/' + filename
            path = target / relative
            original = path.read_bytes()
            with self.subTest(document=relative, state='mandatory bytes'):
                self.assertNotIn(relative, declared)
                self.assertIn(relative, documents)
                self.assertEqual(documents[relative], hashlib.sha256(original).hexdigest())
            try:
                changed = json.loads(original)
                if filename == 'project.json':
                    changed['project'].update(base_branch='release',
                                              validation_command='python tools/new_validation.py')
                else:
                    changed['invariants']['security_review_required'] = True
                schema = json.loads((target / '.engineering-backbone/schemas' / schema_name).read_text())
                Draft202012Validator(schema).validate(changed)
                write_json(relative, changed)
                with self.subTest(document=relative, state='valid facts changed'):
                    stale = command('verify', expected=receipt)
                    self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
                    self.assertIn('Handoff context differs from recomputed snapshot', stale.stdout)
                path.unlink()
                for action in ('resolve', 'verify'):
                    with self.subTest(document=relative, state='removed', action=action):
                        rejected = command(action, expected=receipt if action == 'verify' else None)
                        self.assertNotEqual(rejected.returncode, 0, rejected.stdout + rejected.stderr)
                        self.assertIn('Required document or directory absent: ' + relative, rejected.stdout)
            finally:
                path.write_bytes(original)
        unchanged = command('verify', expected=receipt)
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)

    def test_installed_cli_uses_the_same_effective_checks_as_trusted_preparation(self):
        target, command, receipt, write_json = self.active_cli_fixture()
        workflow_path = '.engineering-backbone/workflows.json'
        initial_flow = json.loads((target / workflow_path).read_text())
        reserved = check('docs', check_id='reserved')
        reserved.update(argv=[sys.executable, '-c', 'raise SystemExit(97)'], timeout_seconds=17)
        initial_flow['checks'].extend([check('test'), reserved])
        write_json(workflow_path, initial_flow)
        base = self.workspace / 'approved-base'
        shutil.copytree(target, base)
        unchanged = command('resolve', trusted_base=base)
        self.assertEqual(unchanged.returncode, 0, unchanged.stdout + unchanged.stderr)
        navigation = json.loads((target / NAVIGATION).read_text())
        component = navigation['components'][0]
        component['profiles'].append('postgresql')
        component['checks'].append({'rule_id': 'TECH-POSTGRESQL-001', 'check_ids': ['test', 'reserved']})
        for base_kind, candidate_kind, binding, accepted in (
            ('docs', 'migration', 'reserved', False),
            ('migration', 'docs', 'reserved', True),
            ('docs', 'docs', 'new-migration', True),
        ):
            with self.subTest(approved=base_kind, candidate=candidate_kind, binding=binding):
                approved = copy.deepcopy(initial_flow)
                approved['checks'][-1]['kind'] = base_kind
                (base / workflow_path).write_text(json.dumps(approved) + '\n')
                candidate = copy.deepcopy(approved)
                candidate['checks'][-1].update(
                    kind=candidate_kind, argv=[sys.executable, '-c', 'raise SystemExit(98)'],
                    cwd='config', timeout_seconds=27)
                if binding == 'new-migration':
                    candidate['checks'].append(check('migration', check_id=binding))
                write_json(workflow_path, candidate)
                component['checks'][-1]['check_ids'] = ['test', binding]
                write_json(NAVIGATION, navigation)
                prepared_path = self.workspace / 'prepared-workflow.json'
                prepared = subprocess.run([
                    sys.executable, '-I', str(target / '.engineering-backbone/workflow-kit.py'),
                    'prepare', '--root', str(target), '--trusted-base', str(base),
                    '--phase', 'pr', '--output', str(prepared_path),
                ], cwd=target, capture_output=True, text=True)
                self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
                actual = {item['id']: item for item in json.loads(prepared_path.read_text())['checks']}
                self.assertEqual(actual['reserved'], approved['checks'][-1])
                resolved = command('resolve', trusted_base=base, output=receipt)
                if not accepted:
                    self.assertFalse(any(item['kind'] == 'migration' for item in actual.values()))
                    self.assertNotEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
                    self.assertIn('Required technology check-kind coverage missing', resolved.stdout)
                    continue
                self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
                context = json.loads(receipt.read_text())
                self.assertEqual({item['id'] for item in context['checks']}, {'docs', 'lint', 'test', binding})
                for item in context['checks']:
                    self.assertEqual(item, actual[item['id']])
                if binding == 'new-migration':
                    self.assertEqual(actual[binding], candidate['checks'][-1])
                verified = command('verify', trusted_base=base, expected=receipt)
                self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
                if binding == 'reserved':
                    # The approved execution stays fixed, but a changed candidate
                    # declaration still invalidates the complete handoff snapshot.
                    candidate['checks'][-1]['timeout_seconds'] += 1
                    write_json(workflow_path, candidate)
                    stale = command('verify', trusted_base=base, expected=receipt)
                    self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
                    self.assertIn('Handoff context differs from recomputed snapshot', stale.stdout)


if __name__ == '__main__':
    unittest.main()
