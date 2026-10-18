---
name: test-and-quality
description: Use when adding scoped verification or checking deterministic results and acceptance before independent review.
---

Read the [canonical policy](../../../policy/core.md) and
[OpenCode workflow](../../../docs/opencode/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: frozen base/head, Task Packet, acceptance criteria, approved check commands,
prerequisites and test-path scope. Output: check/evidence report with commands, exit
codes, revisions, acceptance coverage, unexecuted checks and limitations. Test
engineers may edit scoped tests; quality checkers record evidence without repairs.

## Procedure

1. Confirm snapshot, prerequisites and applicable policy. Select targeted checks,
   affected suites and required broader checks proportionally to risk.
2. For fixes, require an observed failing regression and repaired run. For control
   plane/contract changes, exercise real create/update and negative input paths.
3. Run approved commands only. Keep assertions, coverage, timeouts and gates intact;
   terminal access does not authorize unrelated command-side writes.
4. Record actual results and map every acceptance item to evidence or pending,
   blocked or failed status. Hand frozen check evidence to independent review.

## Stops and negative cases

Stop on changed snapshot, unsafe command, missing prerequisite or failed required
check. Explain any retry; unchanged failures are investigated, not rerun for green.
A structural PASS proves neither Copilot discovery nor product runtime behavior.

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
guide (`docs/agent-navigation.md` in the source; `.engineering-backbone/navigation-guide.md`
when installed). After a Task Packet exists, resolve its scoped request with the
approved guard, verify received context against the current snapshot, then actually
read every resolved document before scoped work. Transfer the request, complete
context and task acceptance/check/stop/return contract at each handoff; resolve a
new request for a delegated role or narrower scope. Invalid or missing mandatory
context blocks the affected task. An inactive seed, receipt or agent reply does not
prove native instruction loading or authorize additional work.
