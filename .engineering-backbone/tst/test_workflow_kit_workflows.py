"""Execute compiled workflow payloads; artifact transfer is emulated locally.

No GitHub service, runtime setup action, or application deployment is claimed by
these checks. The actual trusted shell/Python payloads run on real Git fixtures.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

from src.maintenance.compile_workflow_kit import kit_function, replace_kit_guard, TARGETS

ROOT = Path(__file__).resolve().parents[2]


def workflow(name='pr'):
    return yaml.safe_load((ROOT / f'.github/workflows/workflow-kit-{name}.yml').read_text())


def command(code):
    return [sys.executable, '-c', code]


def configuration(code='print("actual docs check")', *, enabled=True, dependencies=False):
    checks = [{'id': 'docs', 'kind': 'docs', 'argv': command(code), 'cwd': '.',
               'timeout_seconds': 10, 'phases': ['pr']}]
    if dependencies:
        checks.append({'id': 'dependency', 'kind': 'dependency',
                       'argv': command('print("actual dependency check")'), 'cwd': '.',
                       'timeout_seconds': 10, 'phases': ['pr', 'maintenance']})
    return {'schema_version': '1', 'enabled': enabled, 'profiles': ['docs'],
            'capabilities': ['dependencies'] if dependencies else [],
            'runtimes': {}, 'checks': checks}


class WorkflowKitPayloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-kit-workflow-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.candidate = self.workspace / 'candidate'
        self.trusted = self.workspace / 'trusted-base'
        self.runner_temp = self.workspace / 'runner-temp'
        self.runner_temp.mkdir()
        self.output = self.workspace / 'github-output'
        self.output.touch()
        self.candidate.mkdir()
        (self.candidate / '.engineering-backbone').mkdir()
        (self.candidate / 'README.md').write_text('A real tracked documentation fixture.\n')
        self.write_config(configuration())
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Workflow kit fixture')
        self.git('config', 'user.email', 'workflow-kit@example.invalid')
        self.git('add', '.')
        self.git('commit', '-m', 'Reviewed fixture')
        shutil.copytree(self.candidate, self.trusted)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.candidate, capture_output=True,
                              text=True, check=True).stdout.strip()

    def write_config(self, config, root=None):
        (root or self.candidate).joinpath('.engineering-backbone/workflows.json').write_text(
            json.dumps(config) + '\n')

    def shell(self, job, step, *, name='pr', **overrides):
        selected = next(item for item in workflow(name)['jobs'][job]['steps']
                        if item.get('name') == step)
        env = os.environ.copy()
        env.update({'GITHUB_WORKSPACE': str(self.workspace),
                    'GITHUB_REPOSITORY': 'example/consumer',
                    'RUNNER_TEMP': str(self.runner_temp), 'GITHUB_OUTPUT': str(self.output),
                    'SOURCE_MODE': 'false', 'EVENT_NAME': 'pull_request',
                    'BEFORE_SHA': '1' * 40,
                    'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH']})
        env.update(overrides)
        return subprocess.run(['bash', '-c', selected['run']], cwd=self.workspace,
                              env=env, capture_output=True, text=True)

    def prepare(self, name='pr', **env):
        return self.shell('configuration', 'Prepare trusted workflow runner', name=name, **env)

    def run_check(self, job, name='pr', **env):
        label = {'quality': 'project quality', 'security': 'project security',
                 'secrets': 'secret prevention'}[job]
        return self.shell(job, 'Run ' + label, name=name, **env)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_failure(self, result, message=None):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        if message:
            self.assertIn(message, result.stdout + result.stderr)

    def test_compilation_matches_all_trusted_entry_points(self):
        function = kit_function(ROOT)
        for name, indent in TARGETS:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertEqual(replace_kit_guard(text, function, indent), text)

    def test_compiler_rejects_stale_or_missing_compiled_authority(self):
        source = self.workspace / 'source'
        for name in ['.engineering-backbone/src/workflow_kit.py', *(item[0] for item in TARGETS)]:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        compiler = ROOT / '.engineering-backbone/src/maintenance/compile_workflow_kit.py'
        def check(mode):
            return subprocess.run([sys.executable, str(compiler), mode, '--source', str(source)],
                                  capture_output=True, text=True)
        self.assert_success(check('--check'))
        path = source / TARGETS[1][0]
        original = path.read_text()
        path.write_text(original.replace('def workflow_kit_main(argv=None):',
                                         'def workflow_kit_main(argv=None): # drift', 1))
        self.assert_failure(check('--check'), 'stale compiled')
        self.assert_success(check('--write'))
        self.assertEqual(path.read_text(), original)
        path.write_text(original.replace('# END COMPILED WORKFLOW KIT GUARD', '# missing end', 1))
        self.assert_failure(check('--write'), 'exactly one compiled')

    def test_actual_configuration_quality_security_and_scan_succeed(self):
        self.assert_success(self.prepare())
        self.assert_success(self.run_check('quality'))
        self.assertIn('actual docs check', self.run_check('quality').stdout)
        security = self.run_check('security')
        self.assert_success(security)
        self.assertIn('NOT APPLICABLE', security.stdout)
        self.assert_success(self.run_check('secrets'))
        self.assertIn('candidate_sha=' + self.git('rev-parse', 'HEAD'), self.output.read_text())

    def test_old_candidate_validator_and_import_poison_cannot_replace_runner(self):
        marker = self.workspace / 'candidate-code-executed'
        poison = f'from pathlib import Path\nPath({str(marker)!r}).touch()\nraise RuntimeError("poison")\n'
        for name in ('.engineering-backbone/src/workflow_kit.py', 'json.py', 'argparse.py', 'pathlib.py',
                     '.engineering-backbone/validate.py'):
            target = self.candidate / name
            target.parent.mkdir(exist_ok=True, parents=True)
            target.write_text(poison)
        self.assert_success(self.prepare(PYTHONPATH=str(self.candidate)))
        self.assert_success(self.run_check('quality', PYTHONPATH=str(self.candidate)))
        self.assertFalse(marker.exists())
        self.assertEqual((self.runner_temp / 'workflow-kit/runner.py').read_text().split(
            '# END COMPILED WORKFLOW KIT GUARD')[0].split(
            '# BEGIN COMPILED WORKFLOW KIT GUARD\n')[1].rstrip(), kit_function(ROOT))

    def test_candidate_command_weakening_executes_approved_failure(self):
        self.write_config(configuration('raise SystemExit(19)'), self.trusted)
        self.write_config(configuration('print("forged pass")'))
        self.assert_success(self.prepare())
        result = self.run_check('quality')
        self.assert_failure(result, 'exit 19')
        self.assertNotIn('forged pass', result.stdout)

    def test_actual_historical_consumer_cannot_bypass_new_compiled_checks(self):
        from copier import run_copy
        from tst.test_workflows import historical_source
        source = self.workspace / 'historical-source'
        historical_source(source, 'attested-review')
        consumer = self.workspace / 'historical-consumer'
        run_copy(str(source), consumer, defaults=True, quiet=True, skip_tasks=True)
        shutil.rmtree(self.candidate)
        shutil.rmtree(self.trusted)
        consumer.rename(self.candidate)
        self.write_config(configuration('raise SystemExit(31)'))
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Historical fixture')
        self.git('config', 'user.email', 'historical@example.invalid')
        self.git('add', '.')
        self.git('commit', '-m', 'Historical approved consumer with adopted checks')
        shutil.copytree(self.candidate, self.trusted)
        original_validator = (self.trusted / '.engineering-backbone/validate.py').read_bytes()
        self.write_config(configuration('print("candidate tries to replace failure")'))
        (self.candidate / '.engineering-backbone/validate.py').write_text('print("forged PASS")\n')
        self.assert_success(self.prepare())
        self.assert_failure(self.run_check('quality'), 'exit 31')
        self.assertEqual((self.trusted / '.engineering-backbone/validate.py').read_bytes(), original_validator)

    def test_actual_config_removal_disable_id_deletion_and_unsafe_config_fail(self):
        original = configuration()
        cases = [None, dict(original, enabled=False), dict(original, checks=[])]
        for value in cases:
            with self.subTest(value=value):
                path = self.candidate / '.engineering-backbone/workflows.json'
                if value is None:
                    path.unlink()
                else:
                    self.write_config(value)
                self.assert_failure(self.prepare())
                self.assertFalse((self.runner_temp / 'workflow-kit/execution.json').exists())
                self.write_config(original)
        path = self.candidate / '.engineering-backbone/workflows.json'
        path.unlink()
        path.symlink_to(self.trusted / '.engineering-backbone/workflows.json')
        self.assert_failure(self.prepare(), 'Symlink')

    def test_wk_s_1_compiled_guard_rejects_present_null_candidate_and_base(self):
        # Emit the actual pinned workflow runner before changing either contract.
        self.assert_success(self.prepare())
        runner = self.runner_temp / 'workflow-kit/runner.py'
        execution = self.runner_temp / 'workflow-kit/execution.json'
        cases = ((None, 'absent'), ('absent', None), (None, None),
                 (None, configuration()), (configuration(), None))
        for candidate, base in cases:
            with self.subTest(candidate=candidate, base=base):
                for root, value in ((self.candidate, candidate), (self.trusted, base)):
                    path = root / '.engineering-backbone/workflows.json'
                    if value == 'absent':
                        path.unlink(missing_ok=True)
                    else:
                        self.write_config(value, root)
                result = subprocess.run([
                    sys.executable, '-I', str(runner), 'validate',
                    '--root', str(self.candidate), '--trusted-base', str(self.trusted)],
                    cwd=self.workspace, capture_output=True, text=True)
                self.assert_failure(result, 'Configuration has missing or unknown keys')
                self.assertNotIn('PASS:', result.stdout + result.stderr)
                execution.unlink(missing_ok=True)
                result = self.prepare()
                self.assert_failure(result, 'Configuration has missing or unknown keys')
                self.assertNotIn('PASS:', result.stdout + result.stderr)
                self.assertFalse(execution.exists())

    def test_wk_s_1_compiled_guard_preserves_true_legacy_absence(self):
        self.assert_success(self.prepare())
        runner = self.runner_temp / 'workflow-kit/runner.py'
        for root in (self.candidate, self.trusted):
            (root / '.engineering-backbone/workflows.json').unlink()
        result = subprocess.run([
            sys.executable, '-I', str(runner), 'validate',
            '--root', str(self.candidate), '--trusted-base', str(self.trusted)],
            cwd=self.workspace, capture_output=True, text=True)
        self.assert_success(result)
        self.assertIn('PASS: legacy consumer has no workflow kit configuration', result.stdout)
        self.assert_failure(self.prepare(), 'requires an enabled configuration')

    def test_first_activation_requires_complete_identical_reviewed_seed(self):
        self.write_config(configuration(enabled=False), self.trusted)
        self.assert_success(self.prepare())
        self.write_config(configuration('print("unreviewed activation")'))
        self.assert_failure(self.prepare(), 'match the reviewed seed')

    def test_runtime_output_is_validated_and_not_injected(self):
        data = configuration()
        data['runtimes'] = {'python': '3.12', 'node': '24', 'go': '1.24', 'dotnet': '8.0.x'}
        self.write_config(data)
        self.write_config(data, self.trusted)
        self.assert_success(self.prepare())
        self.assertIn('dotnet=8.0.x\n', self.output.read_text())
        data['runtimes']['node'] = '24\nmalicious=true'
        self.write_config(data)
        self.assert_failure(self.prepare(), 'Invalid runtime')

    def test_secrets_are_scanned_independently_of_application_execution(self):
        self.assert_success(self.prepare())
        value = 'gh' + 'p_' + 'A' * 36
        (self.candidate / 'leaked.txt').write_text(value + '\n')
        self.git('add', 'leaked.txt')
        result = self.run_check('secrets')
        self.assert_failure(result)
        self.assertNotIn(value, result.stdout + result.stderr)
        self.assertIn('leaked.txt', result.stdout + result.stderr)

    def test_security_dependency_failure_is_not_report_only(self):
        data = configuration(dependencies=True)
        data['checks'][1]['argv'] = command('raise SystemExit(23)')
        self.write_config(data)
        self.write_config(data, self.trusted)
        self.assert_success(self.prepare())
        self.assert_failure(self.run_check('security'), 'exit 23')

    def test_actual_prepared_artifact_runs_in_fresh_job_and_filters_tokens(self):
        data = configuration('import os; assert "GITHUB_TOKEN" not in os.environ; print("fresh check")')
        self.write_config(data)
        self.write_config(data, self.trusted)
        self.assert_success(self.prepare())
        original_workspace, original_temp = self.workspace, self.runner_temp
        fresh = original_workspace / 'fresh-job'
        fresh.mkdir()
        shutil.copytree(self.candidate, fresh / 'candidate')
        (fresh / 'runner-temp').mkdir()
        shutil.copytree(original_temp / 'workflow-kit', fresh / 'runner-temp/workflow-kit')
        self.workspace, self.runner_temp = fresh, fresh / 'runner-temp'
        result = self.run_check('quality', GITHUB_TOKEN='not-a-real-token')
        self.assert_success(result)
        self.assertIn('fresh check', result.stdout)
        self.assertFalse((fresh / 'candidate/runner.py').exists())

    def test_maintenance_executes_approved_default_branch_security_and_secrets(self):
        data = configuration(dependencies=True)
        self.write_config(data)
        self.assert_success(self.prepare('maintenance'))
        result = self.run_check('security', 'maintenance')
        self.assert_success(result)
        self.assertIn('actual dependency check', result.stdout)
        self.assertNotIn('actual docs check', result.stdout)
        self.assert_success(self.run_check('secrets', 'maintenance'))
        data['checks'][1]['argv'] = command('raise SystemExit(29)')
        self.write_config(data)
        self.assert_success(self.prepare('maintenance'))
        self.assert_failure(self.run_check('security', 'maintenance'), 'exit 29')

    def test_event_and_source_mode_guards_execute(self):
        step = 'Check workflow event and mode'
        self.assert_success(self.shell('configuration', step))
        self.assert_failure(self.shell('configuration', step, SOURCE_MODE='true'), 'restricted')
        self.assert_success(self.shell('configuration', step, SOURCE_MODE='true',
                                      GITHUB_REPOSITORY='Artifaktory/engineering-backbone'))
        for event in ('pull_request_target', 'schedule', 'merge_group'):
            self.assert_failure(self.shell('configuration', step, EVENT_NAME=event), 'Unsupported')
        self.assert_failure(self.shell('configuration', step, EVENT_NAME='push',
                                       BEFORE_SHA='0' * 40), 'trusted snapshot')
        for event in ('schedule', 'workflow_dispatch'):
            self.assert_success(self.shell('configuration', step, name='maintenance', EVENT_NAME=event))
        self.assert_failure(self.shell('configuration', step, name='maintenance', EVENT_NAME='pull_request'))

    def test_actual_aggregate_rejects_every_non_success_missing_and_extra_job(self):
        for name in ('pr', 'maintenance'):
            expected = workflow(name)['jobs']['gate']['needs']
            needs = {job: {'result': 'success', 'outputs': {'report': 'forged PASS'}} for job in expected}
            def aggregate(value):
                return self.shell('gate', 'Require every mandatory job to succeed',
                                  name=name, NEEDS_JSON=json.dumps(value))
            self.assert_success(aggregate(needs))
            for job in expected:
                for status in ('failure', 'cancelled', 'skipped', 'neutral', '', None):
                    with self.subTest(workflow=name, job=job, status=status):
                        bad = copy.deepcopy(needs)
                        bad[job]['result'] = status
                        self.assert_failure(aggregate(bad), 'Mandatory jobs did not succeed')
                missing = copy.deepcopy(needs)
                missing.pop(job)
                self.assert_failure(aggregate(missing), 'Missing or unexpected')
            self.assert_failure(aggregate(dict(needs, forged={'result': 'success'})), 'Missing or unexpected')

    def test_jobs_bind_one_current_run_artifact_and_no_privileged_actions(self):
        for name in ('pr', 'maintenance'):
            data = workflow(name)
            self.assertEqual(data['permissions'], {'contents': 'read'})
            self.assertEqual(data['jobs']['gate']['if'], 'always()')
            for job_name, job in data['jobs'].items():
                if 'uses' in job:
                    self.assertEqual(job['uses'], './.github/workflows/governance-checks.yml')
                    self.assertNotIn('secrets', job)
                    continue
                self.assertEqual(job['runs-on'], 'ubuntu-latest')
                self.assertNotIn('continue-on-error', job)
                for step in job['steps']:
                    self.assertNotIn('continue-on-error', step)
                    if 'uses' in step:
                        self.assertRegex(step['uses'], r'@(?:[0-9a-f]{40})$')
                    if step.get('uses', '').startswith('actions/checkout@'):
                        self.assertIs(step['with']['persist-credentials'], False)
                        self.assertEqual(step['with']['path'], 'candidate' if job_name != 'configuration'
                                         else ('trusted-base' if 'trusted' in step['name'] else 'candidate'))
                    if step.get('uses', '').startswith('actions/download-artifact@'):
                        self.assertEqual(step['with']['artifact-ids'], '${{ needs.configuration.outputs.artifact_id }}')
                        self.assertNotIn('github-token', step['with'])
                        self.assertNotIn('run-id', step['with'])
                        self.assertEqual(step['with']['path'], '${{ runner.temp }}/workflow-kit')
                        self.assertEqual(step['with']['digest-mismatch'], 'error')
                    if step.get('uses', '').startswith('actions/setup-node@'):
                        self.assertNotIn('cache', step['with'])
                        self.assertIs(step['with']['package-manager-cache'], False)
            if name == 'maintenance':
                checkout_step = next(step for step in data['jobs']['configuration']['steps']
                                     if step.get('uses', '').startswith('actions/checkout@'))
                self.assertEqual(checkout_step['with']['ref'], 'refs/heads/${{ github.event.repository.default_branch }}')


if __name__ == '__main__':
    unittest.main()
