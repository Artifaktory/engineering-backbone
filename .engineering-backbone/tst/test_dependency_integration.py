"""Real rendered dependency contracts, preservation and hashed agent handoffs.

These tests exercise the installed guard and Copier, not a package resolver,
container engine or native agent client. The immediate predecessor validator is
also run separately against the delivery snapshot as a publication gate.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

from copier import run_update
from jsonschema import Draft202012Validator

from tst import test_navigation_integration as navigation_tests
from tst.test_quality_copier import commit, git, initialize
from tst.test_quality_framework import check


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = '.engineering-backbone/dependencies.json'
POLICY = '.engineering-backbone/dependency-policy.md'
SCHEMA = '.engineering-backbone/dependencies.schema.json'
PROJECT_DOCUMENT = 'docs/dependency-compatibility.md'
NAVIGATION = '.engineering-backbone/navigation.json'
WORKFLOW = '.engineering-backbone/workflows.json'
ARTIFACTS = {
    'config/compatibility.md': '# Compatibility\nPython 3.12; Linux tooling fixture.\n',
    'config/requirements.txt': 'example==1.0.0\n',
    'config/requirements.lock': 'example==1.0.0 --hash=sha256:' + 'a' * 64 + '\n',
    'config/python-version': '3.12\n',
    'config/Dockerfile': 'FROM scratch\nLABEL purpose="structural fixture only"\n',
}


class DependencyIntegrationTests(unittest.TestCase):
    # Reuse the real Copier and active-navigation setup without inheriting and
    # rerunning its unrelated TestCase methods.
    setUp = navigation_tests.NavigationCopierIntegrationTests.setUp
    copy = navigation_tests.NavigationCopierIntegrationTests.copy
    active_cli_fixture = navigation_tests.NavigationCopierIntegrationTests.active_cli_fixture

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def validate(self, target, base=None):
        argv = [sys.executable, '-I', str(target / '.engineering-backbone/quality-guard.py'),
                'validate', '--root', str(target)]
        if base is not None:
            argv.extend(['--trusted-base', str(base)])
        return subprocess.run(argv, cwd=target, capture_output=True, text=True)

    def dependency_fixture(self, *, enabled=True):
        target, command, receipt, write_json = self.active_cli_fixture()
        for relative, content in ARTIFACTS.items():
            (target / relative).write_text(content, encoding='utf-8')
        flow = json.loads((target / WORKFLOW).read_text())
        flow['checks'].extend(check(kind) for kind in ('dependency', 'build', 'test', 'container'))
        write_json(WORKFLOW, flow)
        contract = {
            'schema_version': '1', 'enabled': enabled,
            'components': [{
                'id': 'configuration', 'kind': 'tooling',
                'compatibility_document': 'config/compatibility.md',
                'manifests': ['config/requirements.txt'],
                'resolution_files': ['config/requirements.lock'],
                'runtime_files': ['config/python-version'],
                'dockerfiles': ['config/Dockerfile'],
                'check_ids': ['dependency', 'build', 'test', 'container'],
            }],
        }
        write_json(CONTRACT, contract)
        return target, command, receipt, write_json, contract

    def test_real_copy_installs_optional_seed_and_preserves_provider_choices(self):
        disabled = self.copy(use_quality_framework=False, use_codex=False, use_copilot=False)
        for relative in (CONTRACT, SCHEMA, PROJECT_DOCUMENT):
            self.assertFalse((disabled / relative).exists(), relative)
        # The shared policy is always distributed so the canonical quality policy
        # can refer to it even when optional project contracts are not installed.
        self.assertEqual((disabled / POLICY).read_text().strip(),
                         (self.source / 'docs/quality/dependencies.md').read_text().strip())
        for codex, copilot in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(codex=codex, copilot=copilot):
                target = self.copy(use_quality_framework=True, use_codex=codex, use_copilot=copilot)
                for relative in (CONTRACT, SCHEMA, POLICY, PROJECT_DOCUMENT):
                    self.assertTrue((target / relative).is_file(), relative)
                self.assertFalse((target / 'Dockerfile').exists(), 'Consumer Dockerfile was invented')
                value = json.loads((target / CONTRACT).read_text())
                self.assertEqual(value, {'schema_version': '1', 'enabled': False, 'components': []})
                schema = json.loads((target / SCHEMA).read_text())
                self.assertEqual(schema, json.loads((self.source / '.engineering-backbone/schemas/dependencies.schema.json').read_text()))
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema).validate(value)
                self.assert_success(self.validate(target))

    def test_copier_update_preserves_project_contract_document_and_dockerfile(self):
        target, _, _, _, _ = self.dependency_fixture(enabled=False)
        local_doc = '# Local compatibility\nKeep the stronger project contract and review owner.\n'
        (target / PROJECT_DOCUMENT).write_text(local_doc)
        (target / 'Dockerfile').write_text('FROM scratch\nLABEL owner="project"\n')
        protected = {relative: (target / relative).read_bytes()
                     for relative in (CONTRACT, PROJECT_DOCUMENT, 'Dockerfile', NAVIGATION)}
        initialize(target)
        commit(target, 'Reviewed project dependency seed and native container')
        policy = self.source / 'docs/quality/dependencies.md'
        policy.write_text(policy.read_text() + '\nDependency policy update fixture.\n')
        commit(self.source, 'Reviewed dependency policy fixture v0.2.0')
        git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assertIn('Dependency policy update fixture.', (target / POLICY).read_text())
        self.assert_success(self.validate(target))

    def test_active_navigation_survives_optional_extension_installation(self):
        # Model a real pre-adoption project: active navigation, no dependency
        # contract/schema/project document. This is not an old-guard identity test.
        extension_templates = [path for path in (self.source / '.engineering-backbone/legacy/templates').rglob('*')
                               if path.is_file() and any(name in path.name for name in
                                   ('dependencies.json', 'dependencies.schema.json', 'dependency-compatibility.md'))]
        self.assertEqual(len(extension_templates), 3)
        saved = {path: path.read_bytes() for path in extension_templates}
        for path in extension_templates:
            path.unlink()
        commit(self.source, 'Template before optional dependency project assets')
        git(self.source, 'tag', '-f', 'v0.1.0')
        target, command, receipt, _ = self.active_cli_fixture()
        self.assertFalse((target / CONTRACT).exists())
        before_navigation = (target / NAVIGATION).read_bytes()
        before_catalog = {path.relative_to(target): path.read_bytes()
                          for path in (target / '.engineering-backbone/standards').rglob('*.json')}
        self.assert_success(command('resolve', output=receipt))
        base = self.workspace / 'approved-no-dependency-contract'
        shutil.copytree(target, base)
        initialize(target)
        commit(target, 'Project active navigation before dependency adoption')
        for path, content in saved.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        commit(self.source, 'Install optional dependency project assets')
        git(self.source, 'tag', 'v0.2.0')
        run_update(target, answers_file='.engineering-backbone/copier-answers.yml',
                   vcs_ref='v0.2.0', defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        self.assertFalse(json.loads((target / CONTRACT).read_text())['enabled'])
        self.assertEqual((target / NAVIGATION).read_bytes(), before_navigation)
        self.assertEqual(before_catalog, {
            path.relative_to(target): path.read_bytes()
            for path in (target / '.engineering-backbone/standards').rglob('*.json')
        })
        self.assert_success(self.validate(target, base))
        self.assert_success(command('resolve', trusted_base=base))

    def test_reviewed_complete_seed_activates_only_without_contract_changes(self):
        target, command, receipt, write_json, contract = self.dependency_fixture(enabled=False)
        self.assert_success(self.validate(target))
        base = self.workspace / 'reviewed-seed'
        shutil.copytree(target, base)
        active = copy.deepcopy(contract)
        active['enabled'] = True
        write_json(CONTRACT, active)
        self.assert_success(self.validate(target, base))
        self.assert_success(command('resolve', trusted_base=base, output=receipt))
        altered = copy.deepcopy(active)
        altered['components'][0]['kind'] = 'application'
        write_json(CONTRACT, altered)
        changed = self.validate(target, base)
        self.assertNotEqual(changed.returncode, 0, changed.stdout + changed.stderr)
        write_json(CONTRACT, active)
        (base / CONTRACT).unlink()
        unreviewed = self.validate(target, base)
        self.assertNotEqual(unreviewed.returncode, 0, unreviewed.stdout + unreviewed.stderr)

    def assert_receipt_inputs(self, target, context, policy):
        documents = {item['path']: item['sha256'] for item in context['documents']}
        for relative in {CONTRACT, policy, *ARTIFACTS}:
            self.assertIn(relative, documents)
            self.assertEqual(documents[relative], hashlib.sha256((target / relative).read_bytes()).hexdigest())
        self.assertEqual({item['id'] for item in context['checks']},
                         {'docs', 'lint', 'dependency', 'build', 'test', 'container'})
        self.assertEqual(context['runtime_loading'], 'unverified')

    def test_installed_consumer_handoff_includes_dependency_inputs_and_rejects_stale_bytes(self):
        target, command, receipt, _, _ = self.dependency_fixture()
        self.assert_success(command('resolve', output=receipt))
        self.assert_receipt_inputs(target, json.loads(receipt.read_text()), POLICY)
        self.assert_success(command('verify', expected=receipt))
        for relative in ('config/requirements.txt', 'config/requirements.lock', 'config/Dockerfile'):
            path = target / relative
            original = path.read_bytes()
            with self.subTest(changed=relative):
                try:
                    path.write_bytes(original + b'# Deliberate dependency input change\n')
                    stale = command('verify', expected=receipt)
                    self.assertNotEqual(stale.returncode, 0, stale.stdout + stale.stderr)
                    self.assertIn('Handoff context differs from recomputed snapshot', stale.stdout)
                finally:
                    path.write_bytes(original)
        self.assert_success(command('verify', expected=receipt))

    def test_source_layout_resolves_dependency_policy_and_container_inputs(self):
        target, _, receipt, _, _ = self.dependency_fixture()
        for relative, installed in (
            ('docs/agent-governance/core.md', '.engineering-backbone/core.md'),
            ('docs/quality/policy.md', '.engineering-backbone/quality-policy.md'),
            ('docs/quality/dependencies.md', POLICY),
            ('docs/quality/README.md', '.engineering-backbone/quality-guide.md'),
            ('docs/quality/technology-profiles.md', '.engineering-backbone/technology-guide.md'),
            ('docs/agent-governance/agent-navigation.md', '.engineering-backbone/navigation-guide.md'),
        ):
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target / installed, path)
        result = subprocess.run([
            sys.executable, '-I', str(ROOT / '.engineering-backbone/src/quality_framework.py'),
            'resolve', '--source', '--root', str(target),
            '--request', str(target / 'plans/request.json'), '--output', str(receipt),
        ], cwd=target, capture_output=True, text=True)
        self.assert_success(result)
        self.assert_receipt_inputs(target, json.loads(receipt.read_text()), 'docs/quality/dependencies.md')


if __name__ == '__main__':
    unittest.main()
