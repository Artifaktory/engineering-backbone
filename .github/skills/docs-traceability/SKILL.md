---
name: docs-traceability
description: Use when a scoped change requires documentation, workflow diagrams or acceptance-to-evidence closeout.
---

Read the [canonical policy](../../../policy/core.md) and
[Copilot workflow](../../../docs/copilot/workflow.md). This skill supplies a procedure, not additional
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
