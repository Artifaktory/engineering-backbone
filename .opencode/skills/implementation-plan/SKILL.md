---
name: implementation-plan
description: Use when preparing or independently reviewing a non-trivial implementation plan before coding.
---

Read the [canonical policy](../../../docs/agent-governance/core.md) and
[OpenCode workflow](../../../docs/agent-governance/adapters/opencode/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: authorized Task Packet, base revision, local contracts, dependencies and
available validation commands. Output in planning mode: bounded plan and acceptance
map. Output in independent review mode: stable plan findings, coverage and unresolved
decisions. Record the mode and session identity; the author is not the reviewer.

## Procedure

1. Read affected paths and current behavior. Select project commands from its facts,
   not a reference repository. Keep the smallest useful delivery.
2. Map each step to acceptance, paths, risk, prerequisites, validation and recovery;
   add negative/consumer-upgrade cases for contracts, permissions or generators.
3. Record required/optional reviewers, budgets and stop conditions. Identify the
   actual orchestration owner and host capabilities; do not invent an orchestrator.
4. In review mode, independently test feasibility and missing risk/acceptance paths;
   return evidence-backed defects/decisions without rewriting the plan.
5. Hand the accepted plan plus its actual independent review to implementation.

## Stops and negative cases

Non-trivial implementation waits for required plan review and accepted scope. Stop
on changed objective, unknown dependencies or unresolved owner decisions. A plan or
review conclusion is not runtime PASS, implementation evidence or human merge approval.

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
