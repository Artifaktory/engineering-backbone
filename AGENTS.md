# Engineering Backbone agent instructions

Read [the canonical policy](docs/agent-governance/core.md), [CONTRIBUTING.md](CONTRIBUTING.md), the active
Task Packet and project instructions before non-trivial work. The current delivery is
[BB-ARCH-015](docs/changes/backbone-architecture-contract/task-packet.json), with
[its independently reviewed plan](docs/changes/backbone-architecture-contract/plan.md). This repository is
the shared agent/engineering control plane: its changes are HIGH risk by default.

- Work within an explicitly authorized, scoped Task Packet. Inspect the branch,
  base revision and worktree; preserve unrelated changes and stricter local rules.
- Keep planner, implementer, quality checker, independent reviewer and triage roles
  separate. Reviewers inspect an immutable snapshot read-only; authors do not
  approve their own implementation.
- Run relevant deterministic checks before Full review. Triage before repairs;
  repair confirmed findings only; Delta review covers those fixes and directly
  introduced regressions. Expanded scope or trust boundaries need a new Full.
- Record actual commands, exit codes and acceptance evidence. Unexecuted checks,
  runtime limitations and missing permissions are explicit; never invent PASS.
- Governance, agent permissions, templates, schema and CI changes need downstream
  compatibility and negative tests against the trusted base. Never weaken gates.
- Never commit secrets, overwrite unrelated work, force-push or use destructive
  Git cleanup. A requested PR does not authorize merge, release or deployment.
- Human merge and release approval is mandatory. No automatic downstream apply.

## Repository commands

Install `.engineering-backbone/requirements.lock` with `--require-hashes` in an isolated Python 3.12 environment. Run:

```sh
python .engineering-backbone/src/validate.py
python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check
python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check
python .engineering-backbone/src/maintenance/compile_navigation.py --check
python .engineering-backbone/src/maintenance/compile_quality_framework.py --check
python .engineering-backbone/src/check_source_dependencies.py
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
git diff --check
```

After the final evidence/code commit, also run `git diff --check BASE_SHA HEAD_SHA`
with the actual resolved PR base/head commits and record both identities. A clean
working-tree diff does not validate a committed PR patch. Any later commit requires
this publication check again.

Changes target the project-configured base branch (`main` for this repository).
Run evidence belongs in ignored `artifacts/` directories; durable redacted review
records belong in `docs/changes/<delivery>/`. Earlier Backbone records are historical
only. The human requested the architecture documents and a PR for review; this authorizes
publication, not merge or release. The actual trusted base is human-merged `main`
`ae317bf30576914d4ed53856be4ae496c6ed64b3`. Run its
`.engineering-backbone/src/validate.py --root CANDIDATE --trusted-base TRUSTED_BASE`
from that separate base checkout. Keep the trusted-base result distinct from
candidate checks; previous delivery results do not qualify this change. See the
[architecture delivery plan](docs/changes/backbone-architecture-contract/plan.md).

When copying this reference tree into another project, replace these source-specific
task references and commands with that project's reviewed facts. Follow the
[adoption guide](docs/agent-governance/adoption.md); copied history does not authorize
new work or establish that project's evidence.

## Shared source-project operating contract

Discover root and applicable path instructions; adapters and skills follow the
canonical policy. Resolve unexpected repository overrides. Independently review
non-trivial implementation plans before implementation. Record required/optional
reviewers, budgets and stop conditions without broadening authorized scope.

Reviews bind base/head revisions and a patch digest, report coverage/unreviewed
areas, and require concrete execution paths, impact, evidence and diff causation.
Delta uses the prior reviewed head, repaired head and confirmed IDs. Do not reopen
unchanged areas; use at most two Full rounds unless a confirmed blocker, relevant
new changes or a documented human exception justify another. Remote reviews remain
advisory without a separately approved formal project contract; automatic reviews
or fixes never bypass local stops and triage.

Closeout maps acceptance to actual evidence or pending/blocked/failed states.
Preserve installed local Publish-Go, signatures and history gates; the backbone
does not implement or authenticate them. Structural PASS is not semantic review.

## Active document navigation

When `.engineering-backbone/navigation.json` is enabled, follow the navigation
guide (`docs/agent-governance/agent-navigation.md` in the source; `.engineering-backbone/navigation-guide.md`
when installed). After a Task Packet exists, resolve its scoped request with the
approved guard, verify received context against the current snapshot, then actually
read every resolved document before scoped work. Transfer the request, complete
context and task acceptance/check/stop/return contract at each handoff; resolve a
new request for a delegated role or narrower scope. Invalid or missing mandatory
context blocks the affected task. An inactive seed, receipt or agent reply does not
prove native instruction loading or authorize additional work.

## Dependency and container inputs

For dependency, runtime or container work, read [the shared dependency policy](docs/quality/dependencies.md)
and [this repository's compatibility contract](docs/operations/engineering/dependency-compatibility.md).
Use the actual tracked [Dockerfile](infra/docker/engineering-backbone/Dockerfile), [direct manifest](.engineering-backbone/requirements.txt)
and [reviewed resolution](.engineering-backbone/requirements.lock). Run the declared source checks and
container build/smoke; record missing execution evidence explicitly. Source CI
checks these inputs directly because this repository has no active navigation seed.
The Dockerfile belongs to Backbone tooling and is not a consumer application's
container definition. Preserve authoritative version files and scoped review.

## OpenCode adapter

Read [the OpenCode operating contract](docs/agent-governance/adapters/opencode/workflow.md) and
[controlled runner contract](docs/agent-governance/adapters/opencode/opencode-runner-contract.md) before
OpenCode work. Its inactive companion is not a native discovery switch. Validate
the exact primary, current scoped receipt and effective permissions before runtime
use; tool defaults do not establish OS isolation or model qualification.
