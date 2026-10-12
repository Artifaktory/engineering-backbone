# Planning, requirements and review formats

Use the smallest useful delivery depth: one direct PR plan, a feature plan for
several related stories, or a program plan only for real multi-delivery dependencies.
Requirements and architecture evidence remain in the consuming repository.

## Task Packet

[The task schema](../schemas/task-packet.schema.json) and
[pending example](../examples/task-packet.json) record objective, role, risk,
approved sources, immutable revisions when available, scope, acceptance verification,
commands/manual evidence, budget, stop conditions and forbidden actions.
Implementation can start with a known base and no head yet; formal review freezes
both revisions. Completed delivery needs actual evidence and completed acceptance.

## Requirement format

[The requirement schema](../schemas/requirement.schema.json) and
[pending example](../examples/requirement.json) distinguish approval, implementation
and verification. Select automatic, manual or hybrid verification explicitly.
A stated requirement or completed implementation is not proof of verification.
Use stable local IDs and actual acceptance-to-test/evidence references.

## Review evidence

[The review schema](../schemas/review-evidence.schema.json) and
[pending example](../examples/review-evidence.json) capture a frozen review snapshot,
independent reviewer identity, findings and triage/repair/delta records. Stable
finding IDs preserve causation through the chain. A delta checks prior confirmed
findings and direct repair regressions; expanded scope needs a new Full round.

The format is a structural contract, not a signature system. Passing schema checks
does not prove that an independent human/model inspected a snapshot. Durable
redacted review records live under `docs/reviews/`; local transcripts belong in
ignored `artifacts/`. Human GitHub approval and release approval are verified
separately.

## Direct plan checklist

- Observable objective and scope including explicit exclusions.
- Existing requirement/architecture links where applicable; no invented IDs.
- Acceptance criteria and automatic/manual/hybrid verification.
- Risks, dependencies and rollback or safe recovery.
- Task Packet, deterministic checks, immutable review snapshot and human decision.

This bootstrap uses [its direct plan](../plans/bootstrap.md). Add story/ADR templates
later when projects demonstrate a shared need; preserve their domain-specific data.
