# Planning, requirements and review formats

Use the smallest useful delivery depth: one direct PR plan, a feature plan for
several related stories, or a program plan only for real multi-delivery dependencies.
Requirements and architecture evidence remain in the consuming repository.

## Task Packet

[The task schema](../../.engineering-backbone/schemas/task-packet.schema.json) and
[pending example](../templates/examples/task-packet.json) record objective, role, risk,
approved sources, immutable revisions when available, scope, acceptance verification,
commands/manual evidence, budget, stop conditions and forbidden actions.
Implementation can start with a known base and no head yet; formal review freezes
both revisions. Completed delivery needs actual evidence and completed acceptance.
Review-ready packets and active reviewer packets require both immutable revisions;
an active implementation packet can still have an unfinished head.

## Requirement format

[The requirement schema](../../.engineering-backbone/schemas/requirement.schema.json) and
[pending example](../templates/examples/requirement.json) distinguish approval, implementation
and verification. Select automatic, manual or hybrid verification explicitly.
A stated requirement or completed implementation is not proof of verification.
Use stable local IDs and actual acceptance-to-test/evidence references.

The [architecture contract](architecture.md) defines the required derivation from
requirements to drivers, decisions, views and planned/actual verification. Use the
[document kit](../templates/architecture/README.md) for the corresponding records.
Preserve existing requirement JSON fields and states; provenance, ownership,
architecture disposition and tool mapping can live in linked companion records.
Do not add unsupported keys or create a competing requirements specification.

## Review evidence

[The review schema](../../.engineering-backbone/schemas/review-evidence.schema.json) and
[pending example](../templates/examples/review-evidence.json) capture a frozen review snapshot,
independent reviewer identity, findings and triage/repair/delta records. Stable
finding IDs preserve causation through the chain. A delta checks prior confirmed
findings and direct repair regressions; expanded scope needs a new Full round.

The format is a structural contract, not a signature system. Passing schema checks
does not prove that an independent human/model inspected a snapshot. Durable
redacted review records live under `docs/changes/<delivery>/reviews/`; local transcripts belong in
ignored `artifacts/`. Human GitHub approval and release approval are verified
separately.

## Direct plan checklist

- Observable objective and scope including explicit exclusions.
- Existing requirement/architecture links where applicable; no invented IDs.
- Acceptance criteria and automatic/manual/hybrid verification.
- Risks, dependencies and rollback or safe recovery.
- Task Packet, deterministic checks, immutable review snapshot and human decision.

The original bootstrap is recorded in [its historical plan](../changes/backbone-bootstrap/plans/bootstrap.md).
Use the shared [decision record](../templates/architecture/decision.md) for material
architecture decisions; story formats remain project-owned. Preserve domain-specific
data and link existing authoritative architecture instead of duplicating it.

## Imported planning and review discipline

For non-trivial implementation plans, use a separate read-only plan review before
implementation. Record dependencies, required/optional reviewers, budgets and
coverage in the plan or companion report. Only the existing schema roles/fields are
accepted; the source projects' micro/standard/critical packet contracts and their
program/architecture/issue-projection engines are not installed here.

Review companion reports bind the patch digest and, for Delta, the prior reviewed
head alongside the existing base/head fields. Additional finding details (category,
confidence, execution path, acceptance relation and regression check) belong in
claim/evidence or a companion report. Existing local schemas and authenticated
review/publish controls remain authoritative. See [the section map](adapters/codex-consolidation.md).

## Copilot procedures

The [permanent Copilot operating guide](adapters/copilot/workflow.md) shows the complete
plan/check/Full/triage/fix/Delta/human decision loop and the role-to-schema mapping.
Its analyst and planner use `planner`; plan/code/security reviewers use `reviewer`;
test/documentation profiles use `implementer`; quality and triage keep their current
schema values. Seven added profiles do not change generic schemas.

Supply actual project file locations through the packet and recorded handoff.
Read-only roles return reports for an authorized writer to persist. Every repair
round starts with triage of stable finding IDs. Independent Delta receives prior
reviewed and repaired heads, confirmed IDs and patch evidence; it examines fixes
and directly introduced regressions. Missing required inputs stop that phase;
an exhausted budget or unresolved decision records a blocker for the owner.

The eight skills are procedural context. An installed file, passed parser or
simulated exercise does not prove runtime discovery; see
[Copilot acceptance](adapters/copilot/smoke-tests.md). Merge/release and local authenticated
gates remain human/project decisions.
