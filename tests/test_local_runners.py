"""Source runner routing is separate from the reusable consumer contract."""

import json
from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPOSITORY = 'Artifaktory/engineering-backbone'
SOURCE_RUNNER = {
    'group': 'af-ci-build-v1',
    'labels': ['self-hosted', 'linux', 'x64', 'ci-heavy'],
}


def resolve_runner(value, repository):
    """Evaluate only the explicit, repository-bound routing contract under test."""
    if isinstance(value, dict):
        return value
    pattern = (
        r"\$\{\{ fromJSON\(github\.repository == '([^']+)' "
        r"&& '([^']+)' \|\| '([^']+)'\) \}\}"
    )
    match = re.fullmatch(pattern, value)
    if not match:
        raise ValueError('Runner selection must depend only on repository identity')
    owner, source, consumer = match.groups()
    if owner != SOURCE_REPOSITORY:
        raise ValueError('Unexpected source repository')
    return json.loads(source if repository == owner else consumer)


def require_source_runner(value):
    if resolve_runner(value, SOURCE_REPOSITORY) != SOURCE_RUNNER:
        raise ValueError('Source jobs must select the verified build group and labels')


class LocalRunnerContractTests(unittest.TestCase):
    def test_every_source_job_routes_to_the_build_group(self):
        count = 0
        for path in sorted((ROOT / '.github/workflows').glob('*.yml')):
            workflow = yaml.safe_load(path.read_text())
            for name, job in workflow['jobs'].items():
                with self.subTest(workflow=path.name, job=name):
                    if 'uses' in job:
                        self.assertEqual(job['uses'], './.github/workflows/governance-checks.yml')
                    else:
                        require_source_runner(job['runs-on'])
                        count += 1
        self.assertEqual(count, 11)

    def test_reusable_external_consumers_keep_their_hosted_default(self):
        for name in ('governance-checks', 'workflow-kit-pr', 'workflow-kit-maintenance'):
            workflow = yaml.safe_load((ROOT / f'.github/workflows/{name}.yml').read_text())
            for job_name, job in workflow['jobs'].items():
                if 'runs-on' not in job:
                    continue
                for repository in ('example/consumer', 'Artifaktory/Artifaktory'):
                    with self.subTest(workflow=name, job=job_name, repository=repository):
                        self.assertEqual(resolve_runner(job['runs-on'], repository), 'ubuntu-latest')
                        self.assertNotIn('inputs.source_mode', job['runs-on'])

    def test_hosted_source_fallback_and_wrong_group_are_rejected(self):
        for value in (
            'ubuntu-latest',
            {'labels': SOURCE_RUNNER['labels']},
            {**SOURCE_RUNNER, 'group': 'af-ci-fast-v1'},
            {**SOURCE_RUNNER, 'labels': ['self-hosted', 'linux', 'ci-heavy']},
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                require_source_runner(value)

    def test_caller_controlled_routing_is_rejected(self):
        value = "${{ fromJSON(inputs.source_mode && '{}' || '\"ubuntu-latest\"') }}"
        with self.assertRaises(ValueError):
            resolve_runner(value, SOURCE_REPOSITORY)

    def test_mandatory_aggregate_gates_still_reject_skipped_results(self):
        # Execute the actual gate script rather than imitating its verdict.
        import os
        import subprocess
        for name in ('workflow-kit-pr', 'workflow-kit-maintenance'):
            workflow = yaml.safe_load((ROOT / f'.github/workflows/{name}.yml').read_text())
            gate = workflow['jobs']['gate']
            self.assertEqual(gate['if'], 'always()')
            step = next(item for item in gate['steps'] if 'NEEDS_JSON' in item.get('env', {}))
            results = {key: {'result': 'success'} for key in gate['needs']}
            for verdict in ('success', 'failure', 'skipped', 'cancelled'):
                changed = {key: dict(value) for key, value in results.items()}
                changed['configuration']['result'] = verdict
                result = subprocess.run(
                    ['bash', '-c', step['run']],
                    env={**os.environ, 'NEEDS_JSON': json.dumps(changed)},
                    text=True, capture_output=True,
                )
                with self.subTest(workflow=name, verdict=verdict):
                    self.assertEqual(result.returncode == 0, verdict == 'success', result.stderr)


if __name__ == '__main__':
    unittest.main()
