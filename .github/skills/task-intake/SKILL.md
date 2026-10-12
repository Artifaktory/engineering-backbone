---
name: task-intake
description: Use when a new request needs bounded requirements, acceptance evidence and an authorized Task Packet.
---

Read the [canonical policy](../../../policy/core.md) and
[Copilot workflow](../../../docs/copilot/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: user request, project facts, current branch/base revision, root/path
instructions and existing requirements. Output: proposed Task Packet content,
acceptance-to-verification map, assumptions and blocking owner decisions. Analyst
or planner returns text; an authorized owner persists it.

## Procedure

1. Inspect the repository context and applicable policy; preserve unrelated work.
2. Separate requested outcomes from assumptions. Record objective, included/excluded
   paths, authorized actions, existing Task Packet role, risk, budget and stops.
3. Give each acceptance criterion observable automated/manual/hybrid evidence;
   classify control-plane edits as HIGH and include downstream effects.
4. List missing prerequisites and decisions. Give the packet/revision to the owner
   before handing a bounded accepted request to planning.

## Stops and negative cases

Stop for contradictory authority, ambiguous scope or unavailable project facts.
Do not create product requirements, schema role names or approval from assumptions.
A packet is proposed scope, not implementation or validation evidence.
