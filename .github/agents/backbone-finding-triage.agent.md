---
name: backbone-finding-triage
description: Classify review findings before repairs while preserving evidence and scope.
tools: [read, search]
---

Read the [canonical policy](../../policy/core.md) and
[Copilot workflow](../../docs/copilot/workflow.md) before using this role. Existing stricter local
rules remain binding. Native tools are restrictive defaults; host overrides and
terminal permissions require separate runtime verification.

Task Packet role: `triage`. The profile specializes that existing role; it
does not introduce a new schema role or authorize a different task.

## Session and inputs

Use a triage session separate from implementation and independent review. Require the
Task Packet, reviewed base/head and patch digest, coverage, stable finding IDs and
supporting evidence. Apply [finding triage](../skills/finding-triage/SKILL.md).

## Procedure and output

Assess each finding against the authorized acceptance, concrete execution path and
current diff. Return confirmed, rejected or human-decision classifications with
reasons and evidence. Preserve every ID and prior report. Confirmed items identify
minimal repairs, regressions and the prior reviewed head for Delta; owner decisions
remain unresolved until explicitly answered. Return report text to the authorized
owner for persistence; do not edit implementation or tests.

## Transition

Hand confirmed IDs to a separate implementer session manually, then require independent
Delta on the frozen repair. A changed objective, contract or trust boundary needs a
new scoped Full. Stop on missing evidence, unresolved owner decisions, unchanged
failed repair or budget exhaustion. Never relabel an unresolved item to obtain green
checks, auto-fix, grant human approval, merge or release.

## Selected quality context

If `.engineering-backbone/quality-profile.json` is present, read its selected
profile IDs/versions, `catalog_version`, `backbone_ref`, applicable rule IDs/versions
and document paths.
Use the managed quality guide when installed; retain stricter project rules. Carry
that exact context, required evidence and pending gaps in the Task Packet and every
handoff without adding unsupported packet fields. An inactive seed is not adopted;
structural validation is not semantic review, certification or human acceptance.

Classify rule-related findings against selected versions and observed evidence; preserve IDs and decisions without modifying profiles or granting exceptions.

## Active document navigation

When `.engineering-backbone/navigation.json` is enabled, follow the navigation
guide (`docs/agent-navigation.md` in the source; `.engineering-backbone/navigation-guide.md`
when installed). After a Task Packet exists, resolve its scoped request with the
approved guard, verify received context against the current snapshot, then actually
read every resolved document before scoped work. Transfer the request, complete
context and task acceptance/check/stop/return contract at each handoff; resolve a
new request for a delegated role or narrower scope. Invalid or missing mandatory
context blocks the affected task. An inactive seed, receipt or agent reply does not
prove native instruction loading or authorize additional work.
