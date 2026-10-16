# Independent Full review: OpenCode behavior and compatibility

Date: 2026-10-16. Reviewer: `bb_reconstruction_full_behavior`, a separate
read-only Full implementation-review session with no implementation authorship.
This report is written outside the immutable reviewed worktree. It is neither
human approval nor a runtime/model qualification.

## Immutable binding

- Repository: `Artifaktory/engineering-backbone`.
- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Tree: `ce15f563e2656831b48e01cf144fa65650033d80`.
- SHA-256 of `git diff --binary <base> <head>`:
  `01334adf41279a614f05ca011c6a9777078fc7f011f7f29d2982204b7fb98523`.
- Reviewed worktree: `artifacts/backbone-full-snapshot`, detached and clean.

Head, tree, patch digest and clean status were checked before and after review;
they remained unchanged. The scope is the complete 78-file base-to-head diff,
with emphasis on installation/update compatibility, shared procedures, navigation,
data-only guards, and the meaning of native-smoke evidence.

## Conclusion

**One in-scope compatibility finding: REC-BB-FUNC-001.** It requires separate
triage before repair. The issue was raised as a lead by the parallel security
reviewer late in this review and then independently checked against the exact
base and candidate workflow by this reviewer. It is the same underlying issue as
`REC-BB-SEC-001`; triage should preserve both IDs and avoid duplicate repairs.

Apart from that predecessor-fingerprint omission, the inspected implementation
follows the approved bounded reconstruction plan.
The optional install flag defaults to false, treats an absent legacy answer as
false, and rejects ordinary changes before mutation. Native configuration and
project-owned instructions survive Copier updates. The unchanged Codex/Copilot
project-facts shape and byte-identical default shared-partial output preserve the
existing adapter contract.

The separate companion does not pretend to disable native file discovery. Its
activation/inheritance rules, exact native roles and procedures, and selected-role
receipt additions agree with the documented contract. Reviewer context now carries
the independent planning procedure and supports an explicit plan mode without
requiring completed implementation checks. The recursive skill and legacy mode
regressions are represented in both the validator and compiled trusted workflow
tests. Ordinary support resources and unrelated alternate skills remain distinct
from managed native identities.

The native smoke reports a deliberately limited observation: an instrumented
temporary source fixture, real pinned executable, localhost canned provider,
exact role discovery, instruction bytes in an actual selected-agent request,
missing-role preflight, and a native error associated with the requested write
tool-call ID. The code and documentation do not promote that result into
real-model qualification, Windows execution, operating-system confinement or a
live AO activation claim.

## Finding REC-BB-FUNC-001

- Severity: **P1**. Category: downstream upgrade compatibility. Confidence: high.
- Location: `.github/workflows/governance-checks.yml:79-80`; rejection path at
  lines 138-140.
- Trigger: an existing consumer generated from the exact immediately preceding
  trusted source `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a` adopts the candidate
  pinned workflow, either retaining its previously approved tooling or updating
  the tooling and workflow together.
- Evidence: the exact base workflow declares current tooling digest
  `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`.
  The candidate replaces CURRENT with
  `a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`
  but retains the previous list without adding that immediate predecessor.
  A read-only Python/YAML comparison of the base Git blob and candidate file
  printed `base_current_accepted_by_head False`, exit 0.
- Execution path and impact: the existing trusted consumer gate computes the
  baseline digest, then requires it to appear in CURRENT or PREVIOUS. Therefore
  the immediate predecessor is rejected with `Trusted base toolchain fingerprint
  is not approved by this pinned workflow` before native/quality checks or the
  predecessor validator can run. Updating the candidate tooling does not fix the
  baseline-side rejection. The documented normal consumer upgrade is blocked,
  including consumers that leave OpenCode unselected.
- Diff causation: the changed CURRENT literal removes the immediately preceding
  digest from the accepted set without transferring it into PREVIOUS. The earlier
  workflow accepted this digest as CURRENT. This is not pre-existing consumer debt.
- Contract relation: the approved plan requires exact predecessor compatibility
  and real update behavior; Task Packet AC-4 and AC-7 cover those paths. Running
  the predecessor validator directly does not exercise this earlier fingerprint
  gate. The new workflow tests use a selected older historical fixture rather
  than the exact immediately preceding source, so their PASS does not cover it.
- Minimal repair/regression proposal for triage: retain the independently
  verified immediate predecessor digest in the workflow-owned reviewed list.
  Exercise a real exact-base generated consumer through the candidate workflow
  with both unchanged old tooling and coherent updated tooling; retain rejection
  of unapproved fingerprints. Do not weaken or bypass the fingerprint gate.

The source-level rejection above was independently established; the parallel
security reviewer is separately recording the actual Copier/workflow reproduction.
No source repair has been made by this reviewer.

## Coverage

Read the candidate and trusted-base `AGENTS.md`, `policy/core.md` and
`CONTRIBUTING.md`; the approved plan, Task Packet, independent plan review and
reconstruction check record; and the changed adapter, navigation and runner guides.
Compared the small policy changes to the unchanged trusted authority, including
separate review/triage, truthful evidence and human merge/release requirements.

Inspected:

- Copier installation selection, preservation patterns, both AGENTS template
  conditions, the new native templates and installed guidance/schema includes.
  The two AGENTS source templates are currently byte-identical; real matrix and
  update checks cover their overlapping Codex case.
- All five generated native role bodies and all eight generated procedure bodies,
  their permissions/metadata and their shared Copilot partials. Reviewed the
  optional reviewer plan-mode branch separately from default Copilot rendering.
- `opencode_errors`, its call from repository validation, the compiler extraction
  and trusted workflow inclusion, exact companion/native formats, duplicate
  fields, permission ceilings/order, inherited restrictions, namespace scans,
  recursive canonical skill paths, alternate reserved identities and path checks.
- Navigation's new companion validation, activation prerequisites, role/procedure
  path selection and receipt integration, together with the compiled quality and
  workflow copies and existing receipt verification call paths.
- Native download verification/extraction, isolated environment, command/output
  bounds, fixture provenance, provider exchange, complete-request loading checks,
  linked tool-error checks and Linux/Windows workflow wiring.
- All new test modules and the existing validator-fixture repair. The repair adds
  required source assets while keeping legacy consumer opt-out explicit; it does
  not remove production checks or existing failure assertions.

## Independent execution and inspected evidence

Commands ran from the immutable snapshot with Python bytecode writes disabled,
using the original checkout's hash-locked Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/6e019b0851cc/engineering-backbone/.venv/bin/python -B -m unittest tests.test_opencode_validation tests.test_opencode_navigation tests.test_opencode_workflow_guard tests.test_opencode_native_smoke -v
PYTHONDONTWRITEBYTECODE=1 /workspace/scratch/6e019b0851cc/engineering-backbone/.venv/bin/python -B -m unittest tests.test_opencode_distribution -v
```

The first command passed **44 tests in 13.130 seconds**, exit 0. The second passed
**5 real Copier distribution tests in 15.578 seconds**, exit 0. These exercise the
eight-way provider matrix, source/generated procedure equality, local-file
preservation, installation-choice rejection and an actual historical update.
Copier's expected missing-answers warnings on fresh fixtures were visible.

A separate read-only Jinja comparison rendered each of the 13 changed Copilot
partials from both the exact base blob and candidate with the ordinary core/guide
variables and default optional settings: all outputs were byte-identical, exit 0.

The root's full-suite evidence is external execution evidence, not an independently
rerun full suite by this reviewer. Its log hash was checked against the durable
record: `2ebc088305f1627873beaf9c9f7d0b909ef66e20584a8bc7deb4f62ac10bb82c`.
The existing native report hash also matched the durable record:
`94bf9ce0835c3c216ea3522e93f4316b850b92fff4cd46a7506bd8fc2a1d1b30`.
Its status is passed on Linux, with four provider requests and six passed case
groups. All 22 recorded source-input hashes independently matched this reviewed
snapshot. The report's instrumented fixture hashes are kept distinct from source
hashes.

## Limits and handoff

No native adversarial skill/mode reproduction was attempted or retried. The
historical override classes were reviewed statically and through data-only
regressions. This session did not rerun the native executable, full 412-test suite,
all compiler/dependency gates, or Docker build; their supplied execution records
retain their original authorship and limits.

Actual Windows native execution, remote CI/provider review outcomes, real-model
qualification, and full AO lifecycle/runtime behavior are unreviewed by this
Backbone behavior review. The AO contract was assessed as this PR's documented
interface, not as certification of a separate repository's implementation. No
qualified tuple, deployment or downstream activation is inferred.

Return this report to a separate triage session together with the independent
authority/security review. REC-BB-FUNC-001 remains open for that classification;
the passing checks do not close it. Pending acceptance evidence, the paired AO
gates, human decisions and repository publication controls remain binding. No
implementation/test edits or remote writes were made by this reviewer.
