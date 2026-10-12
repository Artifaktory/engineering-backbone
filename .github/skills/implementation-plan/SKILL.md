---
name: implementation-plan
description: Use when preparing or independently reviewing a non-trivial implementation plan before coding.
---

Read the [canonical policy](../../../policy/core.md) and
[Copilot workflow](../../../docs/copilot/workflow.md). This skill supplies a procedure, not additional
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
