# Contributing to Engineering Backbone

Read [AGENTS.md](AGENTS.md), [the common policy](policy/core.md) and the active
Task Packet. The active Codex identity-security repair uses
[its Task Packet](plans/codex-security-task.json) and [its plan](plans/codex-security.md).
The preceding Copilot delivery uses [its Task Packet](plans/copilot-development-task.json)
and [its plan](plans/copilot-development.md). The earlier Codex consolidation is
recorded in [its plan](plans/codex-consolidation.md). The original bootstrap remains recorded
in [plans/bootstrap-task.json](plans/bootstrap-task.json) and [plans/bootstrap.md](plans/bootstrap.md). Keep shared policy distinct from
project-specific branches, domain rules, commands and permissions.

## Local validation

Use an isolated Python 3.12 environment. Install the reviewed tooling dependencies,
then run the same structural and consumer-compatibility checks as CI:

```sh
python -m venv .venv
# Activate the environment using your platform's normal command.
python -m pip install --require-hashes -r requirements.lock
python scripts/validate.py
python scripts/compile_toolchain_fingerprint.py --check
python -m unittest discover -s tests -v
git diff --check
```

For a subsequent policy update, run the previous trusted revision's validator
against the candidate and supply `--trusted-base` with that previous checkout.
The initial README-only base has no validator: independent bootstrap review and
explicit human repository-control setup are required before release.

## Change and review process

1. Record a bounded task/plan and acceptance-to-verification mapping.
2. Implement only the approved scope. Add meaningful positive/negative and upgrade
   checks for any changed contract, permission or generated artifact.
3. Run deterministic checks, then freeze base/head/patch for independent Full review.
4. Triage before edits. Repair confirmed findings and request Delta review of those
   IDs and direct repair regressions; expanded scope needs another Full round.
5. Publish a PR when explicitly authorized. A human decides merge and, separately,
   release. Do not auto-merge governance or automatically apply downstream changes.

Review records report actual observations, not an authenticated human signature.
AI/provider review integration and native runtime discovery are separate from
syntax checks. Keep generated consumer facts and stronger local policy intact.

## Maintenance

Dependabot proposes Action/tool dependency updates. Review dependency changes and
regenerate the locked tooling set with `uv pip compile requirements.txt --generate-hashes
--python-version 3.12 --output-file requirements.lock`, then run all checks and
compatibility tests. Source and template changes must be reviewed together. Do not manually edit
Copier's answers file; use Copier's update options. Avoid arbitrary template tasks.

Changes to the copied validator, schemas or dependency manifests also require
`python scripts/compile_toolchain_fingerprint.py --write`, followed by `--check`.
Review the resulting workflow-owned current digest and retain only explicitly
reviewed previous tooling identities needed for consumer compatibility. The check
fingerprints actual Copier-rendered bytes; it does not attest semantic correctness.
Consumers update copied tooling and its reviewed workflow pin together. Independent
source review and human release approval remain mandatory before distribution.

Use [docs/repository-controls.md](docs/repository-controls.md) for required protected
settings and [docs/adoption.md](docs/adoption.md) for the consumer workflow.
