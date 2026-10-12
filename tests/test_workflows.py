"""Execute the actual reusable-workflow shell payloads against real Git consumers."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy
import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = yaml.safe_load((ROOT / '.github/workflows/governance-checks.yml').read_text())
STEPS = {step['name']: step for step in WORKFLOW['jobs']['validate']['steps']}


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def initialize(root):
    git(root, '-c', 'init.defaultBranch=main', 'init')
    git(root, 'config', 'user.email', 'workflow-tests@example.invalid')
    git(root, 'config', 'user.name', 'Workflow fixture')


def commit(root, message):
    git(root, 'add', '.')
    git(root, 'commit', '-m', message)
    return git(root, 'rev-parse', 'HEAD')


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='backbone-workflow-source-')
        cls.addClassCleanup(cls.fixture.cleanup)
        cls.source = Path(cls.fixture.name) / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns('.git', '__pycache__', 'artifacts', '.venv'))
        initialize(cls.source)
        commit(cls.source, 'Reviewed template fixture')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-workflow-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.candidate = self.workspace / 'candidate'
        run_copy(str(self.source), self.candidate, defaults=True, quiet=True, skip_tasks=True, vcs_ref='HEAD')
        self.trusted = self.workspace / 'trusted-base'
        shutil.copytree(self.candidate, self.trusted)

    def shell(self, step, **overrides):
        env = os.environ.copy()
        env.update({
            'GITHUB_WORKSPACE': str(self.workspace),
            'GITHUB_REPOSITORY': 'example/consumer',
            'EVENT_NAME': 'pull_request',
            'SOURCE_MODE': 'false',
            'PATH': str(Path(sys.executable).parent) + os.pathsep + env['PATH'],
        })
        env.update(overrides)
        return subprocess.run(['bash', '-c', STEPS[step]['run']], cwd=self.workspace,
                              env=env, capture_output=True, text=True)

    def validate(self, **env):
        return self.shell('Validate generated consumer with trusted tooling', **env)

    def mutate(self, path, fn, root=None):
        file = (root or self.candidate) / path
        data = json.loads(file.read_text())
        fn(data)
        file.write_text(json.dumps(data) + '\n')

    def test_valid_consumer_uses_prior_bundle(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('no trusted base supplied', result.stdout)

    def test_candidate_noop_validator_and_empty_lock_cannot_bypass_policy(self):
        marker = self.workspace / 'candidate-validator-executed'
        (self.candidate / '.engineering-backbone/validate.py').write_text(
            f'from pathlib import Path\nPath({str(marker)!r}).touch()\nprint("forged PASS")\n')
        (self.candidate / '.engineering-backbone/requirements.lock').write_text('# empty malicious lock\n')
        self.mutate('.engineering-backbone/core.json', lambda d: d['invariants'].update(human_merge_required=False))
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('human_merge_required', result.stdout + result.stderr)
        self.assertIn('dependency manifest is empty', result.stdout + result.stderr)
        self.assertFalse(marker.exists())
        self.assertNotIn('forged PASS', result.stdout)

    def test_trusted_extra_invariant_cannot_be_removed(self):
        self.mutate('.engineering-backbone/core.json', lambda d: d['invariants'].update(security_review_required=True), self.trusted)
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('trusted-base invariant security_review_required', result.stdout + result.stderr)

    def test_candidate_import_paths_and_schema_cannot_replace_trusted_tooling(self):
        (self.candidate / 'yaml.py').write_text('raise RuntimeError("candidate import executed")\n')
        (self.candidate / 'jsonschema.py').write_text('raise RuntimeError("candidate import executed")\n')
        (self.candidate / '.engineering-backbone/schemas/core-policy.schema.json').write_text('{}\n')
        self.mutate('.engineering-backbone/core.json', lambda d: d.update(version='invalid'))
        result = self.validate(PYTHONPATH=str(self.candidate))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('version', result.stdout + result.stderr)
        self.assertNotIn('candidate import executed', result.stdout + result.stderr)

    def test_absent_or_partial_base_fails_before_python_execution(self):
        python_marker = self.workspace / 'python-executed'
        fake_bin = self.workspace / 'fake-bin'
        fake_bin.mkdir()
        fake_python = fake_bin / 'python'
        fake_python.write_text(f'#!/bin/bash\ntouch "{python_marker}"\nexit 0\n')
        fake_python.chmod(0o755)
        original_path = os.environ['PATH']
        for missing in ('validate.py', 'requirements.lock', 'schemas/project.schema.json'):
            with self.subTest(missing=missing):
                file = self.trusted / '.engineering-backbone' / missing
                original = file.read_bytes()
                file.unlink()
                result = self.validate(PATH=str(fake_bin) + os.pathsep + original_path)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('No complete trusted consumer baseline', result.stdout)
                self.assertFalse(python_marker.exists())
                file.write_bytes(original)
        shutil.rmtree(self.trusted)
        result = self.validate(PATH=str(fake_bin) + os.pathsep + original_path)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('workflow inactive', result.stdout)
        self.assertFalse(python_marker.exists())

    def test_source_mode_cannot_bypass_consumer_gate(self):
        step = 'Check workflow mode and event'
        self.assertNotEqual(self.shell(step, SOURCE_MODE='true').returncode, 0)
        self.assertEqual(self.shell(step, SOURCE_MODE='true', GITHUB_REPOSITORY='Artifaktory/engineering-backbone').returncode, 0)
        self.assertEqual(self.shell(step).returncode, 0)
        self.assertNotEqual(self.shell(step, EVENT_NAME='pull_request_target').returncode, 0)

    def test_checkout_uses_explicit_revisions_and_no_credentials(self):
        head = STEPS['Checkout candidate snapshot']['with']
        base = STEPS['Checkout trusted consumer snapshot']['with']
        self.assertEqual(head['ref'], '${{ github.event.pull_request.head.sha || github.sha }}')
        self.assertEqual(head['fetch-depth'], 0)
        self.assertEqual(base['ref'], '${{ github.event.pull_request.base.sha || github.event.before || github.sha }}')
        self.assertFalse(head['persist-credentials'])
        self.assertFalse(base['persist-credentials'])
        self.assertIn("github.event_name == 'workflow_dispatch'", STEPS['Checkout trusted consumer snapshot']['if'])

    def whitespace_fixture(self, *, first_commit=False, bad=True):
        shutil.rmtree(self.candidate)
        self.candidate.mkdir()
        initialize(self.candidate)
        file = self.candidate / 'text.txt'
        file.write_text('valid\n')
        base = None if first_commit else commit(self.candidate, 'Base')
        file.write_text('valid\n' + ('trailing whitespace  \n' if bad else 'clean patch\n'))
        head = commit(self.candidate, 'Candidate')
        self.assertEqual(git(self.candidate, 'diff', '--check'), '')
        return base, head

    def test_committed_whitespace_fails_pr_and_push_on_clean_checkout(self):
        base, head = self.whitespace_fixture()
        for event in ('pull_request', 'push'):
            with self.subTest(event=event):
                result = self.shell('Check committed patch whitespace', EVENT_NAME=event, BASE_SHA=base, HEAD_SHA=head)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('trailing whitespace', result.stdout)

    def test_clean_committed_patch_passes_pr_and_push(self):
        base, head = self.whitespace_fixture(bad=False)
        for event in ('pull_request', 'push'):
            result = self.shell('Check committed patch whitespace', EVENT_NAME=event, BASE_SHA=base, HEAD_SHA=head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dispatch_checks_selected_commits_latest_patch(self):
        _, head = self.whitespace_fixture()
        result = self.shell('Check committed patch whitespace', EVENT_NAME='workflow_dispatch', BASE_SHA='', HEAD_SHA=head)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('trailing whitespace', result.stdout)

    def test_first_commit_whitespace_is_checked_for_push_and_dispatch(self):
        for bad in (False, True):
            _, head = self.whitespace_fixture(first_commit=True, bad=bad)
            for event in ('push', 'workflow_dispatch'):
                with self.subTest(event=event, bad=bad):
                    result = self.shell('Check committed patch whitespace', EVENT_NAME=event,
                                        BASE_SHA='0' * 40 if event == 'push' else '', HEAD_SHA=head)
                    self.assertEqual(result.returncode == 0, not bad, result.stdout + result.stderr)

    def test_whitespace_guard_rejects_invalid_context_and_events(self):
        base, head = self.whitespace_fixture(bad=False)
        for env in ({'HEAD_SHA': 'main'}, {'BASE_SHA': 'main'}, {'BASE_SHA': '0' * 40},
                    {'HEAD_SHA': 'f' * 40}, {'EVENT_NAME': 'schedule'}):
            with self.subTest(env=env):
                values = {'BASE_SHA': base, 'HEAD_SHA': head}
                values.update(env)
                result = self.shell('Check committed patch whitespace', **values)
                self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
