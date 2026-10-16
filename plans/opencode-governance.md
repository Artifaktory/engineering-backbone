# OpenCode governance adapter and controlled AO integration

## Authority and recovery

Task BB-OPENCODE-010 implements the user's 2026-10-15 authorization to implement,
check, independently review and publish the paired Backbone/AO PRs. Base remains
`bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`. This is HIGH-risk control-plane work.
No merge, release, deployment, automatic downstream adoption or settings change.

On 2026-10-16 automated workspace maintenance removed both unpublished checkouts
and local evidence. GitHub branch, commit-object and Library recovery found no
copy of the lost implementation. This is a reconstruction, not an exact restore.
Historical tests and reviews do not certify this new code. The previous confirmed
findings are required regression cases. Obtain a fresh independent plan review,
then fresh deterministic checks and two independent Full reviews of the recovered
implementation. This relevant replacement snapshot justifies a new Full round;
do not present it as Delta-only or silently discard the historical findings.

## Implementation

1. Add optional `use_opencode`, default false and legacy absence false. It chooses
   installation only. Preserve root native JSON/JSONC, `.opencode/**`, root AGENTS
   and the adapter companion on Copier updates. Selected adapter changes during
   update remain rejected before mutation. Keep the existing exact codex/copilot
   project schema untouched for predecessor compatibility.
2. Use a separate fixed `.engineering-backbone/opencode.json` companion:
   `schema_version: "1"`, `adapter_version: "1.0.0"`, boolean `enabled`,
   `opencode_version: "1.19.0"`, `native_config: "opencode.json"`.
   Source and new installs use an inactive seed. Inactive routing does not disable
   OpenCode's direct discovery of installed files. Activation requires active
   navigation and reviewed seed; inherited package removal/disable fails closed.
3. Produce explicit root `opencode.json` local mandatory instructions and native
   primary roles planner, implementer, reviewer, quality-checker and triage.
   Task Packet roles remain the existing five, including `quality_checker`.
   All permissions deny `*`; read/glob/grep/skill may allow. Implementer edit/bash
   are ask, quality-checker bash is ask; read-only roles have no shell/edit/task/MCP.
   These defaults do not establish OS confinement. Use eight shared procedures
   from existing Copilot partials, preserving default Copilot rendering exactly.
   OpenCode reviewer explicitly supports scoped plan, Full and Delta modes;
   plan review must not demand completed implementation checks.
4. Add self-contained data-only `opencode_errors` and compile it into the trusted
   workflow guard without importing candidate modules or altering old tooling
   fingerprints/file lists. Validate exact versions/keys, duplicate JSON/YAML,
   safe regular portable paths, symlinks/case ambiguity, native instructions,
   role/skill identities, permission order and inherited no-weaker guarantees.
   Reject extra native configuration layers, JSONC collisions and executable or
   legacy aliases, including agent/skill/plugin/tool/command and mode/modes.
   Recursively allow only the exact eight canonical native SKILL.md paths;
   ordinary support resources remain valid. Inspect alternate `.agents/.claude`
   skill trees for reserved names without banning unrelated external skills.
5. Extend existing navigation without a second authority. Hash the companion,
   native config, explicit local instructions, guide, runner contract, selected
   native role and relevant procedures. Every role gets task-intake. Planner gets
   implementation-plan; implementer gets bug-reproduction/test-and-quality/
   docs-traceability; quality_checker gets test-and-quality; reviewer gets
   implementation-plan/code-review/delta-review; triage gets finding-triage.
   Do not inject incompatible role prompts. Whole-file hashes apply to anchored
   references. Changed/missing mandatory context invalidates handoffs.
6. Recreate pinned native discovery evidence and portable no-credential smoke for
   OpenCode 1.19.0 source `733b2c627e5aec39cb33cc22373bdce33053ef2c`.
   Verify downloaded archive digests before extraction/execution. Use isolated
   state and a local canned provider for actual CLI loading/tool-denial evidence.
   Root and nested cwd, exact primary roles and missing-role preflight are tested.
   A denial test must observe an actual requested tool and native refusal, not
   merely an unchanged file. Windows requires actual Windows CI. No real-model,
   OS-isolation, resume or compaction qualification is inferred from stub tests.
7. Integrate the separately reviewed AO companion through existing Instructor
   policy/admission/controller/session boundaries. Preserve absent-binding policy
   JSON/hash and unmanaged behavior. Revalidate actual workspace/context before
   inference and queued turns, fresh resume and child-role handoffs. Bind the
   actual generated AO primary rather than assuming installed backbone profiles
   are selected. Preserve existing unsupported read-only OpenCode sandbox refusal.

## Fixed AO contract

Optional `InstructorPolicy.backbone` (omitempty) has schemaVersion1,
adapterSha256 and role-keyed contexts. Each context carries mapped Task Packet
role, explicit repository-relative taskPacket, and full approved resolver context
inline. The existing policy digest is authority. No candidate Python execution,
auto-repin, tracked self-referential receipt or new persistence/state machine.
Verify real Git HEAD against receipt revision; nonnull packet head must agree,
while null remains valid under the existing active implementer/planner grammar.
Bound JSON depth/size, duplicate/exact field names, UTF8, path traversal,
symlinks/reparse/case, document count/bytes and aggregate prompt size.

Governed OpenCode requires an explicit pinned operator qualification attestation:
schemaVersion1, harness opencode, exact runtime/model/optional modelSnapshot,
mapped role/platform/interface, configurationContract ao-opencode-backbone-v1,
observedAt RFC3339, status qualified, evidenceRef/evidenceSha256, and passing
context_loading, stale_context, tool_boundaries, failed_check_reporting,
delegation_context and resume_context cases. No qualified default is seeded.
This validates operator-record completeness/binding, not human signature or
truth of evidence. Missing/unknown/mismatched qualification blocks execution.

Initial supported governed interface is fresh ACP/chat, implementer only, default
permission mode. Governed TUI start/restore/Chat-to-TUI remains blocked even with
qualification because AO cannot intercept live native model/config changes.
Already running native controllers cannot be adopted. Model/role/config/interface
or binding changes require a fresh controlled process; retained reconnect fails
closed unless the boundary is re-established. Unbound behavior stays unchanged.
Native internal delegation, unqualified MCP/tools/plugins and bypass are denied;
only a verified AO-owned hook may be permitted. Static approved input checks must
precede native probing because discovery can initialize plugins. Read back the
actual version/config/selected primary/prompt/model/effective permissions with
bounded sanitized probes. Project approved implementer asks onto the actual AO
agent while preserving explicit stronger denies; do not permit effective allow.

Native discovery includes all canonical skills, while the receipt intentionally
contains selected procedures only. AO additionally compares nonselected canonical
skill bytes to raw blobs at the already-pinned receipt commit. Use only eight
fixed exact paths, disable replacement objects and lazy fetching, neutralize
inherited Git repository/object overrides and bound runtime/output. No fetch,
filter/smudge, candidate command or mutable repin. Document receipt-hash and
pinned-tree evidence separately. Reject additional recursive, external/global/
ancestor skill sources and unbound implicit/explicit instruction sources. Test
with actual Backbone-produced receipts, not only handcrafted fixtures.

## Verification and review

Required cases: opt-in matrix/legacy/update preservation, stricter local files,
native aliases and nested skill identities, reviewer plan-procedure staleness,
permissions/duplicates/path bounds, inherited activation, all five document
roles and technology routes. Compile navigation, quality and toolchain in order.
Run current and exact predecessor validators, four compiler checks, locked
dependency check, complete unittest suite, Actionlint and whitespace checks.

AO runs focused boundaries then complete CI commands: Go build/vet/race/lint,
API/sqlc drift, relevant frontend/package checks and native platform jobs. Record
missing platform/Docker/credentials honestly. Stubbed lifecycle checks do not
prove the complete native model chain. Never exclude failures to produce PASS.

After checks freeze base/head/tree/patch. Two separate read-only Full reviewers
cover behavior/compatibility and authority/security, followed by separate triage,
confirmed repairs and scoped Delta. Maximum eight repair iterations and normally
two Full rounds unless policy's relevant-change/blocker exception applies.
Publish paired PRs only with explicit acceptance states, verify remote tree bytes,
request visible @codex review and inspect actual CI/review results. No auto-merge.
An ordinary workbranch checkpoint may preserve in-progress code with its pending
state; it is not PR acceptance, release or downstream activation. Root owns remote
writes; no worker publishes independently.

## Historical findings carried forward

BB-FUNC-001/BB-SEC-001 (duplicate): nested native skill identities evade canonical
guard/receipt. BB-FUNC-002: reviewer omits independent plan-review procedure and
mode. BB-SEC-002: legacy native mode/modes aliases evade permission validation.
All three must have fresh regressions. The interrupted historical security
execution is not evidence; bounded static review remains acceptable coverage,
explicitly labelled. No unsafe or blocked reproduction needs to be retried.
