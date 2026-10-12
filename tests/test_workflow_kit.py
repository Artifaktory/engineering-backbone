"""Exercise actual isolated kit execution and its approved-base boundaries."""
import ast
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'scripts/workflow_kit.py'


def command(kind='docs', *, check_id=None, code='pass', phases=None):
    return {'id': check_id or kind, 'kind': kind,
            'argv': [sys.executable, '-c', code], 'cwd': '.',
            'timeout_seconds': 5, 'phases': phases or ['pr']}


def config(*, enabled=True, profiles=None, capabilities=None, checks=None,
           runtimes=None):
    return {'schema_version': '1', 'enabled': enabled,
            'profiles': profiles if profiles is not None else ['docs'],
            'capabilities': capabilities or [], 'runtimes': runtimes or {},
            'checks': checks if checks is not None else [command()]}


class WorkflowKitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='backbone-kit-')
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.candidate = self.workspace / 'candidate'
        self.base = self.workspace / 'base'
        self.candidate.mkdir()
        self.base.mkdir()
        self.execution = self.workspace / 'execution.json'
        # Match trusted compilation: only the exact self-contained function is
        # executed. Neither candidate Python nor ambient source imports are used.
        source = SOURCE.read_text(encoding='utf-8')
        node = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == 'workflow_kit_main')
        self.runner = self.workspace / 'trusted-runner.py'
        self.runner.write_text('\n'.join(source.splitlines()[node.lineno - 1:node.end_lineno])
                               + '\nraise SystemExit(workflow_kit_main())\n', encoding='utf-8')

    def write_config(self, root, value):
        path = root / '.engineering-backbone/workflows.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')
        return path

    def cli(self, *arguments, expected=0, env=None):
        result = subprocess.run([sys.executable, '-I', str(self.runner), *map(str, arguments)],
                                cwd=self.workspace, capture_output=True, text=True,
                                timeout=15, env=env)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def prepare(self, candidate=None, base=None, phase='pr', expected=0):
        if candidate is not None:
            self.write_config(self.candidate, candidate)
        if base is not None:
            self.write_config(self.base, base)
        return self.cli('prepare', '--root', self.candidate, '--trusted-base', self.base,
                        '--phase', phase, '--output', self.execution, expected=expected)

    def execute(self, category='quality', phase='pr', expected=0, env=None):
        return self.cli('run', '--root', self.candidate, '--config', self.execution,
                        '--phase', phase, '--category', category, expected=expected, env=env)

    def init_git(self):
        subprocess.run(['git', 'init', '-q', str(self.candidate)], check=True,
                       capture_output=True)

    def track(self, name, data):
        path = self.candidate / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        subprocess.run(['git', '-C', str(self.candidate), 'add', '--', name], check=True,
                       capture_output=True)
        return path

    def test_legacy_absence_validates_but_cannot_run_new_kit(self):
        self.assertIn('legacy', self.cli('validate', '--root', self.candidate,
                                        '--trusted-base', self.base))
        self.prepare(expected=1)

    def test_existing_candidate_json_null_is_rejected_as_malformed(self):
        path = self.write_config(self.candidate, None)
        self.assertEqual('null', path.read_text())
        self.assertIn('missing or unknown keys',
                      self.cli('validate', '--root', self.candidate, expected=1))
        self.cli('validate', '--root', self.candidate, '--trusted-base', self.base,
                 expected=1)
        self.write_config(self.base, config(enabled=False))
        self.cli('validate', '--root', self.candidate, '--trusted-base', self.base,
                 expected=1)
        self.prepare(expected=1)

    def test_existing_trusted_base_json_null_is_rejected(self):
        self.write_config(self.base, None)
        self.cli('validate', '--root', self.candidate, '--trusted-base', self.base,
                 expected=1)
        self.write_config(self.candidate, config())
        self.cli('validate', '--root', self.candidate, '--trusted-base', self.base,
                 expected=1)
        self.prepare(expected=1)

    def test_empty_inactive_seed_validates_but_cannot_execute(self):
        seed = config(enabled=False, profiles=[], checks=[])
        self.write_config(self.candidate, seed)
        self.cli('validate', '--root', self.candidate)
        self.prepare(seed, seed, expected=1)
        self.execution.write_text(json.dumps(seed), encoding='utf-8')
        self.execute(expected=1)

    def test_activation_requires_identical_complete_reviewed_seed(self):
        active = config()
        seed = dict(active, enabled=False)
        self.prepare(active, seed)
        changed = copy.deepcopy(active)
        changed['checks'][0]['argv'][-1] = 'print(1)'
        self.prepare(changed, seed, expected=1)
        self.prepare(active, config(enabled=False, profiles=[], checks=[]), expected=1)

    def test_active_without_trusted_seed_is_rejected(self):
        self.prepare(config(), expected=1)

    def test_real_successful_command_executes(self):
        value = config(checks=[command(code="from pathlib import Path; Path('executed').write_text('yes')")])
        self.prepare(value, value)
        self.execute()
        self.assertEqual('yes', (self.candidate / 'executed').read_text())

    def test_real_failure_cannot_be_overridden_by_forged_report(self):
        value = config(checks=[command(code='raise SystemExit(7)')])
        self.prepare(value, value)
        (self.candidate / 'results.json').write_text('{"result":"success"}')
        self.assertIn('exit 7', self.execute(expected=1))

    def test_command_timeout_fails(self):
        value = config(checks=[command(code='import time; time.sleep(3)')])
        value['checks'][0]['timeout_seconds'] = 1
        self.prepare(value, value)
        self.assertIn('timed out', self.execute(expected=1))

    @unittest.skipUnless(os.name == 'posix', 'Process-group cleanup is POSIX-specific')
    def test_timeout_terminates_child_process_group(self):
        # A child would write after the parent's timeout unless its process group
        # is killed. Observe it through a bounded independent waiter.
        child = "import time; from pathlib import Path; time.sleep(2); Path('survived').write_text('bad')"
        code = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",' + repr(child) + ']); time.sleep(4)'
        value = config(checks=[command(code=code)])
        value['checks'][0]['timeout_seconds'] = 1
        self.prepare(value, value)
        self.execute(expected=1)
        subprocess.run([sys.executable, '-c', 'import time; time.sleep(1.5)'], check=True)
        self.assertFalse((self.candidate / 'survived').exists())

    def test_missing_tool_fails_truthfully(self):
        value = config()
        value['checks'][0]['argv'] = ['backbone-no-such-executable-783423']
        self.prepare(value, value)
        self.assertIn('unavailable', self.execute(expected=1))

    def test_arguments_are_passed_without_shell(self):
        value = config()
        literal = '; touch shell-was-used'
        value['checks'][0]['argv'] = [sys.executable, '-c',
            "import sys; from pathlib import Path; Path('argument').write_text(sys.argv[1])", literal]
        self.prepare(value, value)
        self.execute()
        self.assertEqual(literal, (self.candidate / 'argument').read_text())
        self.assertFalse((self.candidate / 'shell-was-used').exists())

    def test_secret_environment_is_not_inherited_by_checks(self):
        value = config(checks=[command(code="import os; assert 'BACKBONE_SECRET' not in os.environ; assert 'GITHUB_TOKEN' not in os.environ")])
        self.prepare(value, value)
        self.execute(env=dict(os.environ, BACKBONE_SECRET='sensitive', GITHUB_TOKEN='sensitive'))

    def test_base_command_and_runtime_are_current_execution_authority(self):
        base = config(checks=[command(code="from pathlib import Path; Path('base-command').touch()")],
                      runtimes={'python': '3.12'})
        candidate = copy.deepcopy(base)
        candidate['checks'][0]['argv'][-1] = "from pathlib import Path; Path('candidate-command').touch()"
        candidate['runtimes']['python'] = '3.13'
        candidate['checks'].append(command(check_id='new-check', code="from pathlib import Path; Path('addition').touch()"))
        self.prepare(candidate, base)
        self.assertEqual('3.12', json.loads(self.execution.read_text())['runtimes']['python'])
        self.execute()
        self.assertTrue((self.candidate / 'base-command').exists())
        self.assertTrue((self.candidate / 'addition').exists())
        self.assertFalse((self.candidate / 'candidate-command').exists())

    def test_candidate_kind_changes_cannot_suppress_existing_failure(self):
        base = config(checks=[command(code='raise SystemExit(6)')])
        candidate = config(checks=[command('sast', check_id='docs'), command(check_id='new-docs')])
        self.prepare(candidate, base)
        self.execute(expected=1)

    def test_approved_configuration_profiles_capabilities_and_ids_cannot_disappear(self):
        base = config(capabilities=['dependencies'], checks=[command(),
                      command('dependency', phases=['pr', 'maintenance'])])
        for candidate in (None, dict(base, enabled=False), config(),
                          dict(base, checks=[command(), command('dependency', check_id='replacement', phases=['pr', 'maintenance'])])):
            with self.subTest(candidate=candidate):
                self.write_config(self.base, base)
                path = self.candidate / '.engineering-backbone/workflows.json'
                if candidate is None:
                    if path.exists():
                        path.unlink()
                else:
                    self.write_config(self.candidate, candidate)
                self.cli('validate', '--root', self.candidate, '--trusted-base', self.base,
                         expected=1)
        language = config(profiles=['docs', 'python'], runtimes={'python':'3.12'},
                          checks=[command()] + [command(kind) for kind in ['build','lint','test','sast']])
        self.prepare(config(), language, expected=1)

    def test_every_profile_and_capability_requires_real_catalog_coverage(self):
        # Documentation is an independent consumer of the executable contract:
        # its catalog must produce a complete valid configuration, and each
        # published obligation must actually be required by the trusted guard.
        catalog = json.loads((ROOT / 'docs/workflows/profiles.json').read_text())
        coverage = {}
        for profile in catalog['profiles'].values():
            for kind in profile['pr']:
                coverage.setdefault(kind, set()).add('pr')
        for capability in catalog['capabilities'].values():
            for phase in ['pr','maintenance','release','deploy']:
                for kind in capability.get(phase, []):
                    coverage.setdefault(kind, set()).add(phase)
        for kind in catalog['capabilities']['release']['conditional_release']['dependencies_or_container']:
            coverage.setdefault(kind, set()).add('release')
        all_checks = [command(kind, phases=sorted(phases)) for kind, phases in coverage.items()]
        value = config(profiles=list(catalog['profiles']),
                       capabilities=list(catalog['capabilities']),
                       runtimes={'python':'3.12','node':'24','go':'1.24','dotnet':'8.0.x'}, checks=all_checks)
        schema = json.loads((ROOT / 'schemas/workflows.schema.json').read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(value)))
        self.prepare(value, value)
        for index in range(len(all_checks)):
            missing = copy.deepcopy(value)
            del missing['checks'][index]
            self.write_config(self.candidate, missing)
            self.cli('validate', '--root', self.candidate, expected=1)

    def test_maintenance_runs_declared_checks_and_delivery_needs_capability(self):
        value = config(capabilities=['dependencies'], checks=[command(),
                       command('dependency', code="from pathlib import Path; Path('maintenance').touch()", phases=['pr','maintenance'])])
        self.prepare(value, value, phase='maintenance')
        self.execute(category='maintenance', phase='maintenance')
        self.assertTrue((self.candidate / 'maintenance').exists())
        self.prepare(value, value, phase='release', expected=1)
        self.execute(category='quality', phase='maintenance', expected=1)

    def test_docs_project_security_is_explicitly_not_applicable(self):
        self.prepare(config(), config())
        self.assertIn('NOT APPLICABLE', self.execute(category='security'))

    def test_invalid_types_unknown_keys_duplicate_ids_empty_argv_and_controls_fail(self):
        alterations = [lambda c:c.update(extra=True), lambda c:c.update(enabled=1),
                       lambda c:c.update(profiles=['docs','docs']),
                       lambda c:c.update(checks=[command(),command()]),
                       lambda c:c['checks'][0].update(argv=[]),
                       lambda c:c['checks'][0].update(argv=['']),
                       lambda c:c['checks'][0].update(argv=['python','bad\nargument']),
                       lambda c:c['checks'][0].update(argv=['python','bad\ud800argument']),
                       lambda c:c['checks'][0].update(timeout_seconds=True),
                       lambda c:c['checks'][0].update(timeout_seconds=1801),
                       lambda c:c['checks'][0].update(phases=['maintenance']),
                       lambda c:c['checks'][0].update(cwd='../outside'),
                       lambda c:c['checks'][0].update(cwd='C:\\outside'),
                       lambda c:c.update(runtimes={'python':'3.12.x'}),
                       lambda c:c.update(runtimes={'node':'$(command)'}),
                       lambda c:c.update(runtimes={'ruby':'3.3'})]
        for alteration in alterations:
            with self.subTest(alteration=alteration):
                value=config()
                alteration(value)
                self.write_config(self.candidate, value)
                self.cli('validate','--root',self.candidate,expected=1)

    def test_duplicate_json_keys_and_oversized_config_fail(self):
        path = self.write_config(self.candidate, config())
        path.write_text('{"enabled":true,"enabled":false}')
        self.assertIn('Duplicate JSON', self.cli('validate','--root',self.candidate,expected=1))
        path.write_bytes(b' ' * 262145)
        self.assertIn('size limit', self.cli('validate','--root',self.candidate,expected=1))

    def test_symlink_config_ancestor_and_symlink_cwd_fail(self):
        outside = self.workspace / 'outside'
        outside.mkdir()
        self.write_config(outside, config())
        (self.candidate / '.engineering-backbone').symlink_to(outside / '.engineering-backbone', target_is_directory=True)
        self.cli('validate','--root',self.candidate,expected=1)
        (self.candidate / '.engineering-backbone').unlink()
        value=config()
        value['checks'][0]['cwd']='alias/subdir'
        (outside / 'subdir').mkdir()
        (self.candidate / 'alias').symlink_to(outside, target_is_directory=True)
        self.prepare(value,value)
        self.execute(expected=1)

    def test_strict_gate_rejects_missing_skipped_failed_cancelled_and_extra_jobs(self):
        jobs={name:{'result':'success'} for name in ['configuration','governance','quality','security','secrets']}
        self.cli('gate','--needs-json',json.dumps(jobs))
        for state in ['skipped','neutral','cancelled','failure',None]:
            altered=copy.deepcopy(jobs)
            altered['quality']['result']=state
            self.cli('gate','--needs-json',json.dumps(altered),expected=1)
        missing=dict(jobs)
        del missing['secrets']
        self.cli('gate','--needs-json',json.dumps(missing),expected=1)
        self.cli('gate','--needs-json',json.dumps(dict(jobs,untrusted={'result':'success'})),expected=1)

    def test_secret_scanner_checks_actual_tracked_bytes_without_leaking_matches(self):
        self.init_git()
        self.track('clean.txt', b'normal project content\n')
        self.cli('secret-scan','--root',self.candidate)
        cases=[b'ghp' + b'_' + b'A'*36, b'github' + b'_pat_' + b'a'*50,
               b'AK' + b'IA' + b'A'*16, b'-----BEGIN ' + b'PRIVATE KEY-----']
        for index,secret in enumerate(cases):
            with self.subTest(index=index):
                path=self.track('secret.bin', b'\x00prefix '+secret+b' suffix')
                output=self.cli('secret-scan','--root',self.candidate,expected=1)
                self.assertIn('secret.bin',output)
                self.assertNotIn(secret.decode(),output)
                path.write_bytes(b'clean')

    def test_secret_scanner_failure_limits_missing_and_unsafe_files_fail(self):
        self.cli('secret-scan','--root',self.candidate,expected=1)
        self.init_git()
        path=self.track('tracked.txt',b'normal')
        path.unlink()
        self.cli('secret-scan','--root',self.candidate,expected=1)
        path.symlink_to(self.runner)
        self.cli('secret-scan','--root',self.candidate,expected=1)
        path.unlink()
        path.write_bytes(b'x'*2097153)
        self.assertIn('size limit',self.cli('secret-scan','--root',self.candidate,expected=1))

    def test_secret_scan_rejects_subdirectory_and_suppresses_git_fsmonitor(self):
        self.init_git()
        self.track('clean.txt',b'normal')
        subdirectory=self.candidate / 'empty'
        subdirectory.mkdir()
        self.cli('secret-scan','--root',subdirectory,expected=1)
        hook=self.workspace / 'fsmonitor'
        hook.write_text('#!/bin/sh\ntouch ' + str(self.workspace / 'unexpected-hook') + '\n')
        hook.chmod(0o755)
        subprocess.run(['git','-C',str(self.candidate),'config','core.fsmonitor',str(hook)],check=True)
        self.cli('secret-scan','--root',self.candidate)
        self.assertFalse((self.workspace / 'unexpected-hook').exists())


if __name__ == '__main__':
    unittest.main()
