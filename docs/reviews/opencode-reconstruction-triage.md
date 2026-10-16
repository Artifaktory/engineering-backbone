# OpenCode reconstruction: separate Full-review triage

Date: 2026-10-16. Session: `bb_reconstruction_triage`. Responsibility: separate
finding triage, with no implementation or Full-review authorship. Both Full
reviewers had completed before this disposition was written. This report is not
human approval, a new Full review, a repair, or runtime qualification.

## Immutable inputs and authority

- Repository: `Artifaktory/engineering-backbone`.
- Task: `BB-OPENCODE-010`, `plans/opencode-governance-task.json`.
- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Reviewed head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Reviewed tree: `ce15f563e2656831b48e01cf144fa65650033d80`.
- Binary base-to-head patch SHA-256:
  `01334adf41279a614f05ca011c6a9777078fc7f011f7f29d2982204b7fb98523`.
- Behavior Full report: `opencode-reconstruction-full-behavior.md`, SHA-256
  `c84c9837ea0fa19802b03b4fa72fc4348323dcd4fcfff07a42411d1b076ed9c8`.
- Authority/security Full report: `opencode-reconstruction-full-security.md`,
  SHA-256 `fa02d9419bc533ef21c63cfe639d9c3eaa490f6824b2042366fa7ae361c999da`.

Read the repository instructions, contribution rules, canonical policy, approved
plan and Task Packet, plan review, verification record, OpenCode workflow and
runner contract, and finding-triage procedure. The base-to-head policy changes
only add OpenCode to the existing adapter lists; trusted-base review, triage,
evidence and human merge/release requirements remain binding. No active source
navigation or quality-profile file is installed.

Independently verified the detached Full snapshot's head, tree, patch digest and
clean state. Both reports identify that exact snapshot. The successful tested
implementation `fb5732d7d07d8247ab49ea9905d614064728a9cf` differs from the Full
head only by the added reconstruction-checks report. Hashes and completion text
of the original failed suite, final 412-test passing suite and native Linux report
match the durable verification record. These are supplied execution results,
not suites rerun by this triage session.

## Finding disposition

**One confirmed defect; publication is blocked pending a bounded repair,
required checks and independent Delta review.**

| Submitted ID | Reported severity | Classification | Canonical handling |
| --- | --- | --- | --- |
| REC-BB-SEC-001 | P2 | Confirmed | Canonical finding, triaged P1: immediate-predecessor consumer upgrade admission fails. |
| REC-BB-FUNC-001 | P1 | Confirmed duplicate | Same trigger, location, failure path and repair as REC-BB-SEC-001; preserve this alias in repair and Delta records. |

No findings are rejected and none require a new human decision. This is one
repair obligation, not two. The behavior reviewer transparently attributes the
initial lead to the security reviewer and independently verifies the static
rejection. The real Copier/workflow reproduction is the security reviewer's
execution evidence; it is not presented as two independent dynamic reproductions.

### REC-BB-SEC-001 / REC-BB-FUNC-001

- Category: downstream compatibility / trusted-tooling admission.
- Confidence: high.
- Location: `.github/workflows/governance-checks.yml:79-80`; trusted-baseline
  membership check at lines 138-142. The explicit test authority set in
  `tests/test_workflows.py:273-286` also requires synchronization with the repair.
- Trigger: a consumer generated from the exact immediately preceding approved
  source adopts this candidate workflow, retaining the old tooling or updating
  candidate tooling coherently with the workflow.
- Cause: the diff replaces current fingerprint
  `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615` with
  `a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`
  without retaining the predecessor in `PREVIOUS_TOOLCHAIN_SHA256`.
- Execution path: the workflow hashes the installed trusted base and requires
  membership in its own current/previous authority before it runs compiled guards
  or the previous validator. The exact predecessor fails that membership check.
  Updating only candidate tooling cannot repair a baseline-side rejection.
- Impact: the documented normal upgrade from the immediate predecessor is
  blocked, including consumers that do not select OpenCode. It fails closed;
  this evidence does not demonstrate arbitrary-tooling admission or privilege
  escalation.
- Diff causation: the base workflow admitted this exact digest as current; this
  change removes its only entry. It is not pre-existing consumer debt.
- Acceptance relation: AC-4 consumer/update compatibility and AC-7 required
  predecessor verification. Directly running the predecessor validator bypasses
  this earlier fingerprint gate and therefore does not close the finding.
- Severity decision: P1 reflects the deterministic blockage of every normal
  workflow adoption from the immediate predecessor, rather than a security
  exploit claim. The two reviewers' original severity labels remain preserved.

The security reviewer executed actual Copier rendering of both pinned source
snapshots and the exact candidate workflow payload. The original authority exited
1 with `Trusted base toolchain fingerprint is not approved by this pinned workflow`.
Appending only the exact predecessor digest to a temporary in-memory authority
list made the same diagnostic exit 0. That diagnostic is cause isolation, not an
implemented or reviewed fix.

Triage independently read the workflow transition and rejection path, verified
the trusted checkout is the declared base, and rendered its digest using the
existing `rendered_digest` helper with the locked Python environment. The command
exited 0, reported the exact `dddb8af...` digest above and
`admitted_by_current_snapshot False`. Copier emitted its expected fresh-fixture
missing-answers warning. No native OpenCode, adversarial runtime configuration,
candidate validator execution or remote write was required for this check.

## Authorized bounded repair and verification

The separate implementer may make the following repair within the approved task:

1. Add only the independently verified exact predecessor fingerprint above to
   the workflow-owned previous list. Preserve every existing approved identity,
   current digest, file membership, ordering semantics and rejection checks.
   Do not accept a candidate-selected digest, arbitrary historical identities or
   relaxed membership conditions.
2. Update the explicit authority-set expectation and its explanatory comment.
   Keep exact set equality and the clean single-commit/autocrlf checks intact.
3. Add meaningful regression coverage for an exact predecessor consumer against
   the candidate workflow: unchanged approved predecessor tooling and a coherent
   upgrade to current tooling must pass; unapproved or mixed tooling must remain
   rejected. Use verified exact-base bytes with preserved provenance. Keep the
   test self-contained where it is part of the ordinary suite; do not introduce
   a hidden dependency on local historical Git objects or network availability.
   The task excludes `tests/fixtures/historical/**`, so those immutable fixtures
   must not be edited. A narrowly scoped separate fixture is permissible if
   needed; record its provenance and preserve existing hermetic tests.
4. Record the actual failed-before/passed-after workflow regression evidence and
   run affected workflow/clone/autocrlf cases. Then rerun the complete required
   unittest suite on the repaired snapshot, current and exact predecessor
   validators, four compiler checks, source-dependency check, Actionlint and
   whitespace check. Do not reinterpret the original 412-test PASS as execution
   of the repaired source, remove assertions, add exclusions or weaken gates.

Freeze the repair head/tree and patch digests after successful verification.
Independent Delta review must use prior reviewed head
`d6a4af73ed39273383457669d498d9e2d4c3f22a`, both preserved finding IDs and the
repaired head. It covers verified digest provenance, exact authority retention,
the real predecessor transition, negative admission coverage, fixture/test
portability and direct repair regressions. This bounded compatibility repair
does not expand the contract or trust boundary, so a third Full review is not
required. Wider changes would need fresh scope assessment under the existing
policy. This is the first confirmed repair obligation in this reconstructed
Full round; the task's eight-iteration budget remains binding.

Unchanged native adapter/smoke implementation need not be re-executed merely to
repair the fingerprint list. Its prior evidence remains limited to unchanged
source bytes and the observed Linux/canned-provider paths. A relevant native
change would require reassessing that evidence.

## Evidence and publication gates

| Gate or evidence | State and required handling |
| --- | --- |
| Original complete suite and nine deterministic gates | Recorded PASS on the pre-repair implementation, with hashes checked. They remain valid historical execution results but do not detect or close the newly confirmed missing-predecessor defect. |
| Two independent Full reviews | Complete on the same immutable snapshot; one deduplicated confirmed finding. Full-review completion is not clean-review acceptance. |
| Separate triage | Complete in this report. Repair, repaired-source checks and Delta remain pending. |
| Backbone acceptance AC-1 through AC-4 | Existing adapter, navigation, guard and distribution evidence remains recorded; AC-4 has the confirmed immediate-predecessor failure until repaired and verified. |
| AO integration / AC-5 | Separate repository implementation and full gates remain pending. Backbone documentation or this review cannot certify AO lifecycle, native-input closure or delegation behavior. |
| Native evidence / AC-6 | Actual benign Linux CLI smoke passed within its declared limits. Windows awaits actual Windows CI. No real-model qualification, OS confinement, native resume/compaction/delegation qualification or governed activation is established. |
| Local Docker | Not executed because Docker is unavailable, as the check record states. Preserve the gap until the actual remote container build/smoke succeeds. |
| Review/check chain / AC-7 | Blocked by the confirmed finding until the repair, all required repaired-source checks and independent Delta are complete. |
| Publication / AC-8 | Pending: final remote tree identity, visible Codex request and actual CI/review outcomes have not been established. Remote findings require separate triage before repairs. |

After the bounded local repair/check/Delta chain is complete, the existing user
authorization permits publishing the Backbone PR with explicit pending Windows,
container and remote-review states so its actual CI can supply that evidence.
Those pending platform jobs do not authorize a claim of compatibility or a
completed acceptance criterion before they execute. The paired delivery remains
incomplete while AO's independent implementation/check/review gates are pending;
an individual Backbone PR must describe that state accurately.

No additional implementation repair is authorized by this report. In particular,
absent native/model evidence is not permission to activate a qualified default,
broaden the runner contract or repeat the previously blocked malicious native
reproduction. Human merge/release approval, stronger project controls and the
prohibitions on deployment, settings changes and automatic downstream adoption
remain unchanged.

## Return

**Confirmed: REC-BB-SEC-001, with duplicate REC-BB-FUNC-001; triaged P1.** Hand
this bounded repair to a separate implementer, then obtain actual required checks
and independent Delta before PR publication. Only this report was written by the
triage session; no implementation, tests, immutable snapshot or remote state was
changed.
