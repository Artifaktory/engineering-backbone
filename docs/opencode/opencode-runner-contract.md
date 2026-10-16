# Controlled OpenCode runner contract

Contract identifier: `ao-opencode-backbone-v1`. This describes the paired AO
integration; documentation or a copied adapter does not establish runtime support.
The existing Instructor policy digest is the adoption authority. A project operator
must review the complete data binding and qualification before governed execution.
No installer seeds a qualified default or silently repins changed context.

## Policy and context

Optional `InstructorPolicy.backbone` has `schemaVersion: 1`, `adapterSha256` for
raw `.engineering-backbone/opencode.json` bytes and contexts keyed by existing
Instructor role. Each context records the mapped existing Task Packet role,
explicit repository-relative `taskPacket` and the full approved resolver context.
An absent binding preserves the existing policy serialization/hash and unmanaged
behavior. The verifier executes no candidate Python, plugin, shell or receipt code.

Require actual Git HEAD equal to receipt revision; Task Packet ID/role must agree.
A nonnull packet head must equal that revision; null is allowed only by the existing
Task Packet grammar, including active implementer/planner, never as a fabricated
reviewer snapshot. Validate exact fields, duplicates, bounded JSON/document counts
and bytes, aggregate prompt size, UTF-8, portable exact-case regular paths and all
whole-file hashes. Reject symlinks/reparse paths and invalid anchors. Include the
explicit Task Packet, companion, config, required instructions, selected role and
procedures. Recompute the canonical context digest without its context_sha256 key.

The receipt deliberately includes selected procedures only. Native OpenCode also
enumerates every canonical skill. For each nonselected skill, compare current raw
bytes to the exact raw Git blob at the already-approved receipt commit using only
the eight fixed canonical paths. Disable Git replacement objects and lazy fetching;
neutralize inherited Git repository/object overrides, bound time/output and use no
fetch, filters, smudge or candidate command. Receipt hashes and approved-tree blobs
are distinct evidence sources. Reject extra recursive SKILL.md, external/global/
ancestor skill sources and implicit or explicit instructions outside the binding.

## Qualification

A governed OpenCode context also requires operator qualification with these fields:
`schemaVersion: 1`, `harness: opencode`, exact `runtimeVersion: 1.19.0`, exact `model`,
optional immutable `modelSnapshot`, mapped `role`, `platform` (linux/windows/darwin),
`interface` (chat/tui), `configurationContract: ao-opencode-backbone-v1`, RFC3339
`observedAt`, `status: qualified`, `evidenceRef`, SHA256 `evidenceSha256` and `cases`.
Every required case is `pass` with its evidenceRef: context_loading, stale_context,
tool_boundaries, failed_check_reporting, delegation_context, resume_context.
Missing, unknown or mismatched qualification blocks admission. This is an explicit
operator attestation of completeness/binding, not an authenticated human signature,
a fetched URL, verified evidence truth or model-quality certification. Synthetic
fixtures test admission; they are never production qualification.

## Admission and lifecycle

The initial supported governed combination is a **fresh ACP/chat process,
implementer, default permission mode**. Governed TUI start/restore and Chat-to-TUI
remain blocked even with a TUI attestation because live native changes are outside
AO interception. Existing unsupported read-only OpenCode sandbox refusals remain.
Do not adopt a live ACP controller. Restore/resume must establish a fresh controlled
process; retained reconnection cannot inherit stale approval. Role/model/config/
interface/binding changes require replacement rather than live mutation.

Verify the real workspace before sync or async launch and before each queued turn
at the existing actual dispatch-generation boundary. Keep existing work ownership,
session incarnation and before-send admission checks. Revalidate narrowed/child
role context, without introducing a second queue, database schema or state machine.

Bind verified instruction bytes into AO's actual generated primary agent and check
that selected agent; installing backbone-implementer alone does not select it.
Project the approved implementer edit/bash asks onto that actual primary while
preserving explicit stronger denies; fail if ordered effective permissions permit
allow. Deny native internal delegation, unqualified MCP/tools/plugins and bypass.
Only a separately verified AO-owned hook may be admitted. Static approved-input
checks must precede even native version/config/agent probes because bootstrap may
initialize plugins. Probe the exact launch binary/workspace/environment with bounded
time/output and sanitized errors; never return credentials or raw provider config.

## Evidence and stops

The implementation must test actual producer-generated receipts, stale/missing/
changed inputs, model/settings rejection before native calls, queue/restore boundaries,
nonselected skill changes and Git environment/replacement isolation. Preserve all
unbound behavior. Full native model/tool/compaction/resume behavior and Windows need
actual independent execution evidence. A local canned provider proves only observed
native CLI paths. Missing evidence remains pending/blocked and no qualification is
inferred. No automatic merge, release, deployment or downstream activation occurs.
