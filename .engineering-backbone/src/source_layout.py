"""Reviewed source-layout resolver, compiled into standalone trusted guards.

Maintenance extracts this function as text. Guards never import candidate code.
Consumer execution uses its existing fixed contract and does not call this helper.
"""


def source_layout(root):
    """Select one complete canonical source policy without weakening source mode.

    Candidate and trusted-base snapshots must be resolved independently. Native
    dependency files at the product root are deliberately not layout selectors.
    """
    from pathlib import Path

    root = Path(root).absolute()
    contracts = {
        'old': {
            'policy_json': 'policy/core.json',
            'policy_md': 'policy/core.md',
            'quality_policy': 'policy/quality.md',
            'dependency_policy': 'policy/dependencies.md',
            'standards': 'standards',
            'dependencies': '',
            'navigation_guide': 'docs/agent-navigation.md',
            'opencode_guide': 'docs/opencode/workflow.md',
            'opencode_runner': 'docs/opencode/opencode-runner-contract.md',
        },
        'new': {
            'policy_json': '.engineering-backbone/core.json',
            'policy_md': 'docs/agent-governance/core.md',
            'quality_policy': 'docs/quality/policy.md',
            'dependency_policy': 'docs/quality/dependencies.md',
            'standards': '.engineering-backbone/standards',
            'dependencies': '.engineering-backbone',
            'navigation_guide': 'docs/agent-governance/agent-navigation.md',
            'opencode_guide': 'docs/agent-governance/adapters/opencode/workflow.md',
            'opencode_runner': 'docs/agent-governance/adapters/opencode/opencode-runner-contract.md',
        },
    }
    canonical = ('policy_json', 'policy_md', 'quality_policy', 'dependency_policy')

    def present(relative):
        # Check aliases before existence/type filtering: a dangling alternative
        # or a symlinked parent is ambiguity, never permission to use the other.
        path = root
        if path.is_symlink():
            return True
        for part in Path(relative).parts:
            path /= part
            if path.is_symlink():
                return True
        return path.exists()

    old = present(contracts['old']['policy_json'])
    new = present(contracts['new']['policy_json'])
    if old == new:
        kind = 'ambiguous' if old else 'absent'
        raise ValueError('Source layout: ' + kind + ' canonical policy authority')
    selected, alternate = ('old', 'new') if old else ('new', 'old')
    chosen = contracts[selected]
    if any(present(contracts[alternate][key]) for key in canonical):
        raise ValueError('Source layout: mixed canonical policy authorities')
    for key in canonical:
        path = root
        components = [root]
        for part in Path(chosen[key]).parts:
            path /= part
            components.append(path)
        if any(component.is_symlink() for component in components):
            raise ValueError('Source layout: canonical policy must be a regular file; symlinked canonical policy: ' + chosen[key])
        if not path.is_file():
            raise ValueError('Source layout: missing canonical policy file: ' + chosen[key])
    return dict(chosen, layout=selected)
