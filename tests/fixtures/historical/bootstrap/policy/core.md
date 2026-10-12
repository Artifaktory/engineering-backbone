# Engineering Backbone: shared governance

This policy is language- and domain-independent. Project-specific rules, branches,
commands, deployment permissions and risk controls belong to the consuming project.
Existing stricter project rules remain binding. A profile or agent adapter may add
restrictions; it must not weaken this baseline or replace local policy silently.

## Scope and authorization

Before a non-trivial edit, check the current branch, base revision, clean/dirty
worktree and applicable instructions. Use a scoped Task Packet recording the
objective, authorized actions, base revision, included/excluded paths, role, risk,
acceptance-to-verification mapping, budgets and stop conditions. Analysis and packet
preparation may precede that packet. No unrelated cleanup or invented requirements.

Human instructions authorize the requested work. Publishing a requested PR is not
permission to merge, release, deploy, delete data or expand access. Stop when the
scope or authorization is missing, contradictory or exceeded. Never overwrite
unrelated work, force-push, perform destructive Git cleanup or commit secrets.

## Roles and planning

The planner produces a testable plan. The implementer makes the approved scoped
changes. The quality checker records actual deterministic check results. Independent
reviewers inspect a frozen snapshot read-only. Triage classifies findings before
repair. The implementer must not certify its own changes as independently reviewed.
Do not silently switch incompatible roles within a review session.

Use a direct plan for a small PR. A feature or program plan is optional when
dependencies, multiple deliveries or risks justify it. Requirement approval,
implementation and verification are separate states. Automated, manual and hybrid
verification are valid when explicitly selected and evidenced.

## Checks and evidence

Run the project's relevant deterministic checks before formal review. A bug fix
needs a meaningful regression check. Contract or workflow changes need producer /
consumer and failure-path checks proportional to risk. Preserve assertions,
coverage, timeouts and gates; do not skip checks to obtain a green result.

Record exact commands, exit codes, inspected revisions, executed and unexecuted
checks, findings, limitations and acceptance coverage. A plan, test name, generated
file, schema-valid report or model output is not a PASS or proof of runtime behavior.
Redact sensitive information. Missing tools or absent evidence remain visible.

## Full, triage, repair and delta review

Freeze the same base, head and patch digest for all reviewers in one Full round.
Do not edit that snapshot between reviewers. Findings need stable IDs, severity,
location, trigger, impact, evidence and a relation to the current diff. Exclude
style preferences, new requirements and unrelated pre-existing debt.

Triage findings as confirmed, rejected or requiring a human decision. Repair only
confirmed findings. Freeze the changed repair snapshot. Delta review checks those
finding IDs and regressions directly introduced by the repairs. Scope, contract or
trust-boundary expansion requires a new Full round. An unchanged repair snapshot,
unresolved human decision or exhausted budget stops the chain.

## Control plane and downstream safety

Changes to governance, schemas, validators, templates, agent permissions and CI are
HIGH risk by default. Review them against the trusted base policy as well as the
proposed head. Test generated consumers and upgrade behavior before distribution.
Consumers pin a reviewed release/commit and adopt changes through their own PRs.
Never automatically apply or merge downstream changes.

A human must approve merge and release. An AI review is advice, even when a provider
can technically submit an approval. Do not auto-merge governance. Release, signing,
branch protection and required-check settings are separate repository controls.
Instructions and schema checks do not enforce those controls by themselves.

## Adapter boundaries

Codex and Copilot profiles express the same roles and baseline. Read-only profiles
are restrictive defaults, not protection against elevated runtime overrides.
Native role files do not install or activate GitHub review bots. CI verifies formats
and generated artifacts; product-specific runtime discovery must be checked
separately. Preserve stricter local instructions during installation and upgrades.
