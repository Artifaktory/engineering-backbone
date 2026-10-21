"""Local doctor failure boundaries and inactive local-CI adoption example."""
from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

import yaml

from tst.test_source_ci import condition, event


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/runner_doctor.py'
EXAMPLE = ROOT / 'docs/templates/operations/local-ci.yml.example'
SPEC = importlib.util.spec_from_file_location('backbone_runner_doctor', SCRIPT)
doctor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = doctor
SPEC.loader.exec_module(doctor)
SENTINEL = 'FAKE_SECRET_MUST_NEVER_APPEAR_7319'


def available(command):
    return '/fixed-tools/' + Path(command).name


def successful(command, **kwargs):
    return subprocess.CompletedProcess(command, 0, b'GNU bash x86_64-pc-msys', b'')


class RunnerDoctorTests(unittest.TestCase):
    def run_main(self, profile, run=successful, which=available, system='Linux', machine='x86_64'):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(doctor.platform, 'system', return_value=system), \
                patch.object(doctor.platform, 'machine', return_value=machine), \
                patch.object(doctor.sys, 'version_info', (3, 12, 14)), \
                patch.object(doctor.shutil, 'which', side_effect=which), \
                patch.object(doctor.subprocess, 'run', side_effect=run) as calls, \
                redirect_stdout(out), redirect_stderr(err):
            code = doctor.main(['--profile', profile])
        return code, out.getvalue() + err.getvalue(), calls.call_args_list

    def test_development_uses_fixed_bounded_probes_without_docker(self):
        code, output, calls = self.run_main('development')
        self.assertEqual(code, 0)
        self.assertIn('python-3.12: ok', output)
        self.assertIn('registration, labels, repository/group access', output)
        for call in calls:
            self.assertFalse(call.kwargs['shell'])
            self.assertEqual(call.kwargs['timeout'], 10)
            self.assertEqual(call.kwargs['stdin'], subprocess.DEVNULL)
            self.assertNotIn('docker', Path(call.args[0][0]).name)
        self.assertEqual([Path(call.args[0][0]).name for call in calls][1:], ['git', 'bash'])

    def test_source_linux_requires_observed_os_and_architecture(self):
        for system, machine in [('Windows', 'AMD64'), ('Linux', 'aarch64')]:
            with self.subTest(system=system, machine=machine):
                code, output, _ = self.run_main('source-linux', system=system, machine=machine)
                self.assertEqual(code, 1)
                self.assertIn('Prerequisite checks failed.', output)
        code, output, calls = self.run_main('source-linux')
        self.assertEqual(code, 0)
        self.assertIn('docker-daemon: ok', output)
        docker = [call.args[0][1:] for call in calls if Path(call.args[0][0]).name == 'docker']
        self.assertEqual(docker, [['--version'], ['info', '--format', '{{.ServerVersion}}']])

    def test_docker_daemon_failure_returns_nonzero_without_tool_output(self):
        def run(command, **kwargs):
            if 'info' in command:
                return subprocess.CompletedProcess(command, 1, SENTINEL.encode(), SENTINEL.encode())
            return successful(command, **kwargs)
        code, output, _ = self.run_main('source-linux', run=run)
        self.assertEqual(code, 1)
        self.assertIn('docker-daemon: failed', output)
        self.assertNotIn(SENTINEL, output)

    def test_missing_executable_is_nonzero(self):
        code, output, calls = self.run_main('development', which=lambda command: None if command == 'git' else available(command))
        self.assertEqual(code, 1)
        self.assertIn('git: missing', output)
        self.assertTrue(all(Path(call.args[0][0]).name != 'git' for call in calls))

    def test_timeout_and_oserror_are_redacted(self):
        for failure, state in [
            (subprocess.TimeoutExpired(SENTINEL, 10, output=SENTINEL, stderr=SENTINEL), 'timeout'),
            (OSError(SENTINEL), 'failed'),
        ]:
            with self.subTest(state=state):
                code, output, _ = self.run_main('development', run=lambda *a, **k: (_ for _ in ()).throw(failure))
                self.assertEqual(code, 1)
                self.assertIn('git: ' + state, output)
                self.assertNotIn(SENTINEL, output)
                self.assertNotIn('Traceback', output)

    def test_nonzero_probe_output_is_never_printed(self):
        def run(command, **kwargs):
            return subprocess.CompletedProcess(command, 3, SENTINEL.encode(), SENTINEL.encode())
        code, output, _ = self.run_main('development', run=run)
        self.assertEqual(code, 1)
        self.assertNotIn(SENTINEL, output)

    def test_windows_requires_git_bash_instead_of_wsl_and_powershell(self):
        code, output, calls = self.run_main('source-windows', system='Windows', machine='AMD64')
        self.assertEqual(code, 0)
        self.assertIn('git-bash: ok', output)
        self.assertTrue(any(Path(call.args[0][0]).name == 'pwsh' for call in calls))

        def linux_bash(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, b'GNU bash x86_64-pc-linux-gnu', b'')
        code, output, _ = self.run_main('source-windows', system='Windows', machine='AMD64', run=linux_bash)
        self.assertEqual(code, 1)
        self.assertIn('git-bash: failed', output)
        code, output, _ = self.run_main(
            'source-windows', system='Windows', machine='AMD64',
            which=lambda c: None if c in {'pwsh', 'powershell'} else available(c))
        self.assertEqual(code, 1)
        self.assertIn('powershell: missing', output)

    def test_current_python_version_is_not_a_profile_claim(self):
        with patch.object(doctor.sys, 'version_info', (3, 11, 9)), \
                patch.object(doctor.shutil, 'which', side_effect=available), \
                patch.object(doctor.subprocess, 'run', side_effect=successful):
            checks = doctor.diagnose('development')
        self.assertEqual(checks[0], doctor.Check('python-3.12', 'failed'))

    def test_real_cli_help_and_invalid_options_do_not_echo_input(self):
        help_result = subprocess.run([sys.executable, str(SCRIPT), '--help'], capture_output=True, text=True, check=False)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn('source-windows', help_result.stdout)
        invalid = subprocess.run([sys.executable, str(SCRIPT), '--profile', SENTINEL], capture_output=True, text=True, check=False)
        self.assertEqual(invalid.returncode, 2)
        self.assertNotIn(SENTINEL, invalid.stdout + invalid.stderr)


class InactiveLocalCIExampleTests(unittest.TestCase):
    def setUp(self):
        self.example = yaml.safe_load(EXAMPLE.read_text(encoding='utf-8'))
        self.job = self.example['jobs']['checks']

    def test_example_is_inactive_and_allocation_is_local_with_fork_admission(self):
        self.assertFalse(EXAMPLE.is_relative_to(ROOT / '.github/workflows'))
        self.assertEqual(self.job['runs-on'], ['self-hosted', 'Linux', 'X64', 'project-ci'])
        self.assertFalse(condition(self.job['if'], event(head='outside/fork')))
        self.assertFalse(condition(self.job['if'], event(name='pull_request_target')))
        self.assertFalse(condition(self.job['if'], event(name='schedule')))
        self.assertTrue(condition(self.job['if'], event()))
        self.assertTrue(condition(self.job['if'], event(name='push')))
        self.assertEqual(self.example['permissions'], {'contents': 'read'})
        self.assertNotIn('secrets', self.job)
        for step in self.job['steps']:
            self.assertNotIn('continue-on-error', step)
            if 'uses' in step:
                self.assertRegex(step['uses'], r'^[^@]+@[0-9a-f]{40}$')
                self.assertNotIn('artifact', step['uses'])
            if step.get('uses', '').startswith('actions/checkout@'):
                self.assertIs(step['with']['persist-credentials'], False)

    def test_unconfigured_repository_and_commands_really_fail(self):
        before_checkout = self.job['steps'][0]
        actual_env = dict(os.environ, GITHUB_REPOSITORY='example/product', **before_checkout['env'])
        rejected = subprocess.run(['bash', '--noprofile', '--norc', '-c', before_checkout['run']],
                                  env=actual_env, capture_output=True, text=True, check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('Configure and review', rejected.stdout)
        actual_env['EXPECTED_REPOSITORY'] = 'example/product'
        configured_repo = subprocess.run(['bash', '--noprofile', '--norc', '-c', before_checkout['run']],
                                        env=actual_env, capture_output=True, text=True, check=False)
        self.assertEqual(configured_repo.returncode, 0)
        check = self.job['steps'][-1]
        unconfigured = subprocess.run(['bash', '--noprofile', '--norc', '-c', check['run']],
                                     env=actual_env, capture_output=True, text=True, check=False)
        self.assertNotEqual(unconfigured.returncode, 0)
        self.assertIn('commands are not configured', unconfigured.stdout)


if __name__ == '__main__':
    unittest.main()
