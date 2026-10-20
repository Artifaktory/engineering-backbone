# Contributing to Engineering Backbone

Read [AGENTS.md](AGENTS.md), [the common policy](docs/agent-governance/core.md),
the active [BB-LAYOUT-011 Task Packet](docs/changes/backbone-layout/task-packet.json)
and [its plan](docs/changes/backbone-layout/plan.md). Prior delivery plans and reviews
are preserved in [change history](docs/changes/README.md). Their claims refer to their
original snapshots and do not authorize or certify this refactor.

This repository is also the copyable reference layout. Shared policy stays distinct
from project-owned branches, domain rules, commands and permissions. Follow the
[adoption guide](docs/agent-governance/adoption.md) before using a copy for a product.

## Local validation

Use an isolated Python 3.12 environment. Install the reviewed tooling dependencies,
then run the same structural and consumer-compatibility checks as CI:

```sh
python -m venv .venv
# Activate the environment using your platform's normal command.
python -m pip install --require-hashes -r .engineering-backbone/requirements.lock
python .engineering-backbone/src/validate.py
python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check
python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check
python .engineering-backbone/src/maintenance/compile_navigation.py --check
python .engineering-backbone/src/maintenance/compile_quality_framework.py --check
python .engineering-backbone/src/check_source_dependencies.py
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
git diff --check
```

For a subsequent policy update, run the previous trusted revision's validator
against the candidate and supply `--trusted-base` with that previous checkout.
For this path refactor, the previous validator still expects the previous source
layout. Its actual failure remains visible and blocks merge readiness. Never retry
with candidate code and describe that as trusted-base PASS. The draft PR provides
a reviewable migration; resolving the trust transition requires separate explicit
review. In later deliveries, use the new path only when the validator belongs to
the already trusted base itself.

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

Read [the dependency policy](docs/quality/dependencies.md) and the actual
[source compatibility contract](docs/operations/engineering/dependency-compatibility.md) before changing
dependencies, runtime or container inputs. The tracked [Dockerfile](infra/docker/engineering-backbone/Dockerfile)
builds this repository's Python tooling; follow the contract's build/smoke commands
and report their actual results. Commit required inputs and documentation together.
The source dependency check validates tracked files, direct/resolved pins and
installed requirements; behavior and container checks remain additional evidence.

Dependabot proposes Action/tool dependency updates. Review dependency changes and
regenerate the locked tooling set with `uv pip compile .engineering-backbone/requirements.txt --generate-hashes
--python-version 3.12 --output-file .engineering-backbone/requirements.lock`, then run all checks and
compatibility tests. Canonical source and retained legacy template changes must
be reviewed together. The root `copier.yml` and `.engineering-backbone/legacy/`
serve existing consumers; direct copies do not require rendering. Do not manually
edit a legacy consumer's Copier answers file; use Copier's update options. Avoid
arbitrary template tasks.

Technology catalog or resolver changes require `python .engineering-backbone/src/maintenance/compile_navigation.py
--write`, then `python .engineering-backbone/src/maintenance/compile_quality_framework.py --write`, followed by
their `--check` commands. These compile reviewed literals into the self-contained
trusted guards. Keep the original quality catalog authority unchanged unless a
separately reviewed migration authorizes it. Run routing/receipt failure cases,
real Copier consumer updates and previous-validator checks. Use
[the navigation guide](docs/agent-governance/agent-navigation.md) to distinguish static, explicit
agent-context and actual native-client evidence.

Changes to the copied validator, schemas or dependency manifests also require
`python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --write`, followed by `--check`.
Review the resulting workflow-owned current digest and retain only explicitly
reviewed previous tooling identities needed for consumer compatibility. The check
fingerprints actual Copier-rendered bytes; it does not attest semantic correctness.
Consumers update copied tooling and its reviewed workflow pin together. Independent
source review and human release approval remain mandatory before distribution.

Use [repository controls](docs/operations/engineering/repository-controls.md) for required protected
settings and [the adoption guide](docs/agent-governance/adoption.md) for the consumer workflow.
