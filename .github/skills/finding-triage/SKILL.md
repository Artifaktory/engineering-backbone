---
name: finding-triage
description: Use after Full or Delta review to classify every finding before any repair.
---

Read the [canonical policy](../../../docs/agent-governance/core.md) and
[Copilot workflow](../../../docs/agent-governance/adapters/copilot/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: Task Packet, immutable review report, base/head/patch digest, stable IDs,
coverage and evidence. Output: triage report preserving all IDs and classifications
confirmed, rejected or requiring a human decision, with reasons and evidence. A
read-only triage session returns text to an authorized owner for persistence.

## Procedure

1. Check each claim against the actual contract, concrete trigger, execution path,
   impact and current diff; distinguish missing evidence from a proven defect.
2. Confirm in-scope defects, reject unsupported/style/unrelated claims with reasons,
   and identify owner decisions without guessing the answer.
3. For confirmed IDs, record the smallest authorized repair, regression check and
   whether scope/contract/trust changes require a separately scoped new Full.
4. Pass confirmed IDs and the prior reviewed head to a separate implementer session;
   preserve original review evidence for independent Delta.

## Stops and negative cases

Stop for unresolved owner decisions, missing snapshot/evidence or budget exhaustion.
Do not delete findings, silently mark them resolved, edit code/tests or auto-fix.
A classification does not prove a repair or grant merge/release approval.

## Selected quality context

If `.engineering-backbone/quality-profile.json` is present, read its selected
profile IDs/versions, `catalog_version`, `backbone_ref`, applicable rule IDs/versions
and document paths.
Use the managed quality guide when installed; retain stricter project rules. Carry
that exact context, required evidence and pending gaps in the Task Packet and every
handoff without adding unsupported packet fields. An inactive seed is not adopted;
structural validation is not semantic review, certification or human acceptance.

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
