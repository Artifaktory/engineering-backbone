# Copilot repository instructions

Read the [canonical policy](../docs/agent-governance/core.md), [repository facts](../CONTRIBUTING.md) and
[Copilot workflow](../docs/agent-governance/adapters/copilot/workflow.md) before non-trivial work. Discover applicable
root/path instructions; preserve stricter local policy and unrelated work. This
entry is shared context; agent profiles select responsibilities and tool budgets,
and skills supply procedures when needed.

For scoped requirements or design work, read the
[architecture contract](../docs/agent-governance/architecture.md) and carry its
source/decision/view/verification context into planning and independent review.

- Start with an authorized Task Packet, actual branch/base/head and approved scope.
  Map acceptance to real verification; classify control-plane changes as HIGH risk.
- Use separate planning, implementation, quality, independent review and triage
  sessions. Non-trivial plans need independent review before implementation.
- Run approved checks, freeze the snapshot, then Full → Triage → Fix confirmed IDs →
  Delta of fixes/direct regressions. Wider scope/contract/trust changes need a new
  scoped Full. Keep budgets and stop conditions; no author self-approval.
- Bind reviews to revisions and patch digest; preserve findings/coverage and actual
  commands/results. Unexecuted checks remain pending/blocked, never invented PASS.
- Keep secrets out of files/logs. Do not force-push, overwrite unrelated work, merge,
  release, alter protections or apply downstream changes without separate authority.
- Human merge/release approval and installed local Publish-Go/signature/history
  gates remain required. Instructions and schema checks do not enforce these gates.

Select a role from [agent profiles](agents) and a procedure from [skills](skills).
Handoffs are optional host conveniences: transfer Task Packet, revisions and evidence
manually to a fresh session where unsupported. Role selection alone does not make
review independent; verify the intended client actually loads its files and tools.

## PR review

Prioritize concrete correctness, security, compatibility and downstream regressions.
Use stable IDs, P0-P3, exact path, trigger, impact, evidence, diff causation and a
minimal regression check; report unreviewed areas. Exclude style and unrelated debt.
Assess changed instructions against trusted-base policy. Delta binds prior reviewed
head, repaired head and confirmed IDs without reopening unchanged areas. Default
maximum is two Full rounds unless a justified policy exception permits another.

Custom roles do not activate automatic GitHub PR review. Provider advice/automatic
fixes never bypass triage, local review stops or human approval. Verify provider
settings separately and document unavailable context/runtime checks.

## Selected quality context

If `.engineering-backbone/quality-profile.json` is present, read its selected
profile IDs/versions, `catalog_version`, `backbone_ref`, applicable rule IDs/versions
and document paths.
Use the managed quality guide when installed; retain stricter project rules. Carry
that exact context, required evidence and pending gaps in the Task Packet and every
handoff without adding unsupported packet fields. An inactive seed is not adopted;
structural validation is not semantic review, certification or human acceptance.

## Repository checks

Use an isolated Python 3.12 environment with hash-locked requirements. Run
`python .engineering-backbone/src/validate.py`,
`python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check`,
`python .engineering-backbone/src/maintenance/compile_navigation.py --check`,
`python .engineering-backbone/src/maintenance/compile_quality_framework.py --check`,
`python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check`,
`python .engineering-backbone/src/check_source_dependencies.py`,
`python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v` and `git diff --check`.
Read [CONTRIBUTING.md](../CONTRIBUTING.md) and the active Task Packet first.

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
