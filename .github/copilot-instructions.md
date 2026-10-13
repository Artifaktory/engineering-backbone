# Copilot repository instructions

Read the [canonical policy](../policy/core.md), [repository facts](../CONTRIBUTING.md) and
[Copilot workflow](../docs/copilot/workflow.md) before non-trivial work. Discover applicable
root/path instructions; preserve stricter local policy and unrelated work. This
entry is shared context; agent profiles select responsibilities and tool budgets,
and skills supply procedures when needed.

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

Select a role from [agent profiles](agents/) and a procedure from [skills](skills/).
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
`python scripts/validate.py`,
`python scripts/compile_toolchain_fingerprint.py --check`,
`python -m unittest discover -s tests -v` and `git diff --check`.
Read [CONTRIBUTING.md](../CONTRIBUTING.md) and the active Task Packet first.
