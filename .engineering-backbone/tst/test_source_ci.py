"""Check source runner allocation boundaries from the actual workflow conditions.

These are static contract checks, not a GitHub scheduler/runner attestation.
The evaluator deliberately supports only the boolean expression subset used here.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'Artifaktory/engineering-backbone'
LOCAL_LINUX = ['self-hosted', 'Linux', 'X64', 'backbone-ci']
TOKEN = re.compile(r"'(?:[^']|'')*'|&&|\|\||!=|==|[!()]|[A-Za-z_][A-Za-z0-9_.]*")


def workflow(name):
    return yaml.safe_load((ROOT / '.github/workflows' / name).read_text())


def condition(expression, context):
    """Evaluate real job conditions for concrete boolean/string event fixtures."""
    expression = expression.removeprefix('${{').removesuffix('}}').strip()
    parts, previous = [], 0
    for match in TOKEN.finditer(expression):
        if expression[previous:match.start()].strip():
            raise ValueError('Unsupported workflow condition syntax')
        token = match.group()
        if token.startswith("'"):
            parts.append(repr(token[1:-1].replace("''", "'")))
        elif token in {'&&', '||', '!'}:
            parts.append({'&&': 'and', '||': 'or', '!': 'not'}[token])
        elif token in {'(', ')', '==', '!='}:
            parts.append(token)
        else:
            if token not in context:
                raise ValueError('Unmodelled context: ' + token)
            parts.append(repr(context[token]))
        previous = match.end()
    if expression[previous:].strip():
        raise ValueError('Unsupported trailing condition syntax')

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not evaluate(node.operand)
        if isinstance(node, ast.BoolOp):
            values = [bool(evaluate(value)) for value in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            left, right = evaluate(node.left), evaluate(node.comparators[0])
            if isinstance(left, str) and isinstance(right, str):
                left, right = left.casefold(), right.casefold()
            if isinstance(node.ops[0], ast.Eq):
                return left == right
            if isinstance(node.ops[0], ast.NotEq):
                return left != right
        raise ValueError('Unsupported condition AST')

    return bool(evaluate(ast.parse(' '.join(parts), mode='eval')))


def event(name='pull_request', repository=SOURCE, head=SOURCE, source=True):
    return {
        'github.repository': repository,
        'github.event_name': name,
        'github.event.pull_request.head.repo.full_name': head,
        'inputs.source_mode': source,
    }


class SourceCIContractTests(unittest.TestCase):
    def source_jobs(self):
        for filename in ('quality.yml', 'opencode-native.yml'):
            for name, job in workflow(filename)['jobs'].items():
                yield filename, name, job
        yield 'governance-checks.yml', 'validate', workflow('governance-checks.yml')['jobs']['validate']

    def test_source_guards_reject_foreign_copy_fork_missing_head_and_wrong_events(self):
        rejected = [
            event(repository='example/product', head='example/product'),
            event(name='push', repository='example/product', head=None),
            event(name='workflow_dispatch', repository='example/product', head=None),
            event(head='outside/fork'),
            event(head=None),
            event(name='pull_request_target'),
            event(name='issue_comment'),
            event(name='schedule'),
        ]
        for filename, name, job in self.source_jobs():
            self.assertIn('if', job, (filename, name))
            for context in rejected:
                with self.subTest(workflow=filename, job=name, context=context):
                    self.assertFalse(condition(job['if'], context))

    def test_source_guards_allow_intended_source_checks(self):
        for filename, name, job in self.source_jobs():
            for trigger in ('pull_request', 'push', 'workflow_dispatch'):
                with self.subTest(workflow=filename, job=name, event=trigger):
                    expected = name != 'trusted-policy' or trigger == 'pull_request'
                    self.assertEqual(condition(job['if'], event(name=trigger)), expected)

    def test_legacy_consumer_mode_retains_its_existing_allocation_behavior(self):
        job = workflow('governance-checks.yml')['jobs']['validate']
        self.assertTrue(condition(job['if'], event(repository='example/product',
                                                  head='example/product', source=False)))
        # The legacy branch is intentionally retained; source mode must select
        # the complete fixed local label set, with no user-supplied fallback.
        match = re.fullmatch(
            r"\$\{\{ inputs\.source_mode && fromJSON\('([^']+)'\) \|\| 'ubuntu-latest' \}\}",
            job['runs-on'])
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1)), LOCAL_LINUX)

    def test_all_source_allocations_require_dedicated_local_labels(self):
        quality = workflow('quality.yml')['jobs']
        self.assertEqual(quality['foundation']['uses'], './.github/workflows/governance-checks.yml')
        self.assertIs(quality['foundation']['with']['source_mode'], True)
        for name in ('source-dependencies', 'trusted-policy'):
            self.assertEqual(quality[name]['runs-on'], LOCAL_LINUX)
        native = workflow('opencode-native.yml')['jobs']['native-smoke']
        self.assertEqual(native['runs-on'], '${{ matrix.labels }}')
        matrix = native['strategy']['matrix']['include']
        self.assertEqual({entry['os'] for entry in matrix}, {'ubuntu-latest', 'windows-latest'})
        by_name = {entry['os']: entry['labels'] for entry in matrix}
        self.assertEqual(by_name['ubuntu-latest'], LOCAL_LINUX)
        self.assertEqual(by_name['windows-latest'], ['self-hosted', 'Windows', 'X64', 'backbone-ci'])

    def test_source_jobs_do_not_upload_or_bypass_failed_checks(self):
        for filename, name, job in self.source_jobs():
            with self.subTest(workflow=filename, job=name):
                self.assertNotIn('continue-on-error', job)
                self.assertNotIn('secrets', job)
                for step in job.get('steps', []):
                    self.assertNotIn('continue-on-error', step)
                    self.assertNotIn('upload-artifact', step.get('uses', ''))
                    if step.get('uses', '').startswith('actions/checkout@'):
                        self.assertIs(step['with']['persist-credentials'], False)
                self.assertNotIn('pull_request_target', workflow(filename).get('on',
                                 workflow(filename).get(True, {})))

    def test_portability_native_and_trusted_policy_checks_remain_mandatory(self):
        native = workflow('opencode-native.yml')['jobs']['native-smoke']
        scripts = '\n'.join(step.get('run', '') for step in native['steps'])
        for required in ('--require-hashes --only-binary=:all:', 'test_reference_layout.py',
                         'test_architecture_documents.py', 'test_opencode_native_smoke.py',
                         'opencode_native_smoke.py --report artifacts/opencode-native/report.json'):
            self.assertIn(required, scripts)
        self.assertTrue(all('if' not in step for step in native['steps']))
        trusted = workflow('quality.yml')['jobs']['trusted-policy']
        commands = '\n'.join(step.get('run', '') for step in trusted['steps'])
        self.assertIn('trusted-base/.engineering-backbone/src/validate.py --root candidate --trusted-base trusted-base', commands)
        self.assertIn("exit 1", commands)
        foundation = workflow('governance-checks.yml')['jobs']['validate']
        check = next(step for step in foundation['steps'] if step['name'] == 'Validate backbone source')
        self.assertEqual(check['if'], 'inputs.source_mode')
        self.assertIn('python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v', check['run'])
        self.assertIn('compile_toolchain_fingerprint.py --check', check['run'])


if __name__ == '__main__':
    unittest.main()
