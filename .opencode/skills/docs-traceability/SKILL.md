---
name: docs-traceability
description: Use when a scoped change requires documentation, workflow diagrams or acceptance-to-evidence closeout.
---

Read the [canonical policy](../../../policy/core.md) and
[OpenCode workflow](../../../docs/opencode/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: authorized documentation scope, accepted requirements, implementation and
review revisions, actual check results and intended audience. Output: scoped docs
patch and acceptance-to-evidence map with pending/blocked/failed states and gaps.
Documentation workers edit allowed docs only; a reviewer returns text read-only.

## Procedure

1. Compare the implemented behavior to existing usage, interfaces and requirements;
   identify only affected documents, diagrams and links.
2. Explain responsibilities, inputs/outputs, review transitions and safe recovery.
   Keep project commands/branches local and stricter rules intact.
3. Map each acceptance criterion to actual observed evidence and revision. Separate
   structural/scenario checks, real host smoke, provider review and human decisions.
4. Check relative links and provenance. Keep durable redacted records while raw
   transcripts/test artifacts remain outside tracked docs.
5. Return unresolved claims, runtime gaps, residual risk and a frozen patch for
   independent review; preserve prior reports and installed publication gates.

## Stops and negative cases

Stop on contradictory sources, undocumented behavior changes or missing evidence
needed for a claim. Never call a planned test PASS, invent host compatibility or
alter production code/tests as a documentation side effect.

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
