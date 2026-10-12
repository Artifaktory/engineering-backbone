# Copilot-native development package plan

Active task: [BB-COPILOT-003](copilot-development-task.json). Scope is the backbone
only. The human authorized implementation and a checked, independently reviewed
PR. Merge/release/downstream activation remain separate decisions.

## Contract

- Keep the existing planner/implementer/reviewer files and their tool metadata
  backward-compatible. Add analyst, plan reviewer, test engineer, quality checker,
  security reviewer, documentation/traceability and finding triage: ten Copilot
  profiles. Map specializations onto existing Task Packet roles rather than invent
  new enum values. No changes to Codex profiles or generic schemas.
- Supply eight task skills: task-intake, implementation-plan, bug-reproduction,
  test-and-quality, code-review, finding-triage, delta-review, docs-traceability.
  Skill instructions are concise, procedural and contain required inputs/output,
  stop conditions, trusted-base authority and real evidence requirements.
- Use Copilot-native tool budgets and optional handoffs on new roles; handoffs use
  send:false and are convenience only, with manual/session-file fallback. Reviewer
  independence requires a separate session and frozen commit, not switching names.
- Add core governance/tests/docs path rules and selectable Python/frontend examples.
  Select profiles via install-time Copier answers; do not derive framework/paths
  solely from language strings. Preserve all existing native roles/skills/rules and
  always refresh a neutral Copilot integration guide; no tasks/hooks/shell installs.
- Publish a reusable role/skill package, not an enforced role filesystem sandbox.
  Quality checker has execute privileges: it must obey scope and approved commands;
  tool filtering alone does not forbid arbitrary command-side writes.
- Extend the trusted validator with an embedded Copilot role/skill registry (no
  candidate-controlled catalog authority). Validate new managed profiles if present,
  require source completeness, preserve installed native files on ordinary updates
  and distinguish legacy three-role consumers from extended consumers.
- A workflow-owned Copilot guard checks the candidate even when the trusted base
  has the old three-role validator. Compile the self-contained embedded registry /
  validation function into the immutable workflow and fail checks on drift. It uses
  hash-locked trusted-base dependencies and never executes/imports candidate code.
  Test old-base upgrades with elevated new roles/malformed skills/rules, removal of
  installed extended assets, and legacy consumers without any extended assets.
- Keep the attested tooling tuple shape unchanged; validator bytes change its digest.
  Retain reviewed previous digest and update workflow-owned current fingerprint.
  Old trusted validator still accepts the unchanged three original profiles. The
  new validator must be proven compatible with older generated bundles.
- Documentation includes source revisions/licenses/patterns, client capability and
  actual-runtime smoke tests, diagrams in README and generated guide, and separate
  GitHub PR bot setup. Live PyCharm/VS Code/CLI operation is not available here;
  structural/scenario tests must not be labelled client discovery or provider proof.

## Verification and review

Independently review this plan before implementation. Then run source/trusted-base
validation, actual Copier generation/upgrade tests, negative permissions/metadata/
link/handoff tests, the complete existing security suite, fingerprint and Actionlint.
Use two frozen-snapshot Full reviewers; triage before fixes, then independent Delta
for confirmed IDs and direct repair regressions. No artificial Delta if no repairs.
A lightweight forward test receives only raw fixtures and skill files, not the
expected result. It measures instruction usability, not actual Copilot execution.

Local base `2b48fc01d20648ffeeea94e288e1c7d511bae12b` has tree
`357d1c3caf05eed442f5b5cc74539437c36bd794`, identical to remote main
`1ffebdfff4f5cc24e7ffcfff5a4dcf88d554f4c8`. Publish from remote main with verified
reviewed tree equality; metadata differences are reported, not concealed.

## Independent plan review

`copilot_plan_review` identified PLAN-TRUST-1 (old validator lacks new-asset
validation). The workflow-owned guard amendment above resolves the design gap; its
implementation must pass the stated negative executed-upgrade tests. No other
confirmed plan blocker. Reviewer did not execute implementation tests.
