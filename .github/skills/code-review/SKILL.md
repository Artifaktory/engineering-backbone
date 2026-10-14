---
name: code-review
description: Use for an independent Full review of a frozen scoped change after deterministic checks.
---

Read the [canonical policy](../../../policy/core.md) and
[Copilot workflow](../../../docs/copilot/workflow.md). This skill supplies a procedure, not additional
permissions, authority or independent approval. Preserve stricter project rules.

## Inputs and output

Inputs: authorized Task Packet, trusted-base policy, fixed base/head commits, patch
digest, check evidence, required reviewer catalog and budget. Output: review report
with snapshot, coverage/unreviewed areas and stable findings. Use a separate read-only
review session; authors never certify their own changes as independently reviewed.

## Procedure

1. Confirm the snapshot and Full mode. Read root/path instructions and affected
   contracts; compare changed instructions against trusted-base authority.
2. Orient on the diff, then trace changed execution paths and callers/consumers.
   Prioritize correctness, security, compatibility and downstream impact.
3. Challenge each suspected defect with a concrete trigger, reachable path and
   evidence. Use observed checks or label unexecuted reproduction; do not invent PASS.
4. Report stable ID, P0-P3, category/confidence, exact location, trigger, impact,
   evidence, acceptance/contract relation, diff causation and minimal regression.
   Preserve extra detail in supported schema fields/companion text, not unknown keys.
5. Exclude style, equivalent alternatives, new requirements and unrelated existing
   debt. Report `NO CONFIRMED IN-SCOPE FINDINGS` when applicable, bounded by coverage.
6. Give findings to triage. Preserve the report and immutable reviewed head.

## Stops and negative cases

Stop on changing snapshot, missing required context or exhausted budget. Do not edit,
auto-fix or provide human approval. Default maximum is two Full rounds unless a
confirmed blocker, relevant change or documented human exception justifies more.
Remote provider advice cannot bypass local gates or strengthen itself into approval.

## Selected quality context

If `.engineering-backbone/quality-profile.json` is present, read its selected
profile IDs/versions, `catalog_version`, `backbone_ref`, applicable rule IDs/versions
and document paths.
Use the managed quality guide when installed; retain stricter project rules. Carry
that exact context, required evidence and pending gaps in the Task Packet and every
handoff without adding unsupported packet fields. An inactive seed is not adopted;
structural validation is not semantic review, certification or human acceptance.
