---
name: delta-review
description: Use after triaged repairs to verify confirmed finding IDs and directly introduced regressions on a frozen repair.
---

Read the [canonical policy](../../../policy/core.md) and
[Copilot workflow](../../../docs/copilot/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: prior reviewed head, repaired head, repair patch digest, original review and
triage reports, confirmed IDs, Task Packet and actual repair/check evidence. Output:
Delta report mapping each confirmed ID to repaired, unresolved or blocked evidence,
plus direct repair regressions and coverage. Use a separate read-only reviewer.

## Procedure

1. Confirm immutable revisions and compare only the repair range to the reviewed
   head. Read trusted policy and affected contracts; keep original review evidence.
2. For every confirmed ID, trace the original trigger and verify the repair and
   meaningful regression evidence. Unexecuted cases remain explicit limitations.
3. Inspect callers/consumers directly affected by each repair for new defects. Apply
   Full finding-quality fields to any directly introduced regression.
4. Return per-ID conclusions, direct regression findings and unreviewed paths to
   triage. State `NO CONFIRMED IN-SCOPE FINDINGS` only with snapshot/coverage limits.

## Stops and negative cases

Do not silently reopen unchanged areas or call a new feature a repair. Changed
objective, acceptance, contract or trust boundary needs a new scoped Full. Stop
for unresolved human decisions, unchanged failed repair, missing evidence, candidate
mutation or exhausted budget. No author self-review, edits or human approval.

## Selected quality context

If `.engineering-backbone/quality-profile.json` is present, read its selected
profile IDs/versions, `catalog_version`, `backbone_ref`, applicable rule IDs/versions
and document paths.
Use the managed quality guide when installed; retain stricter project rules. Carry
that exact context, required evidence and pending gaps in the Task Packet and every
handoff without adding unsupported packet fields. An inactive seed is not adopted;
structural validation is not semantic review, certification or human acceptance.
