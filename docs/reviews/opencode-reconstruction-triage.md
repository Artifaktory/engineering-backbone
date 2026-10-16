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

## Closure addendum — 2026-10-16

**REC-BB-SEC-001 and its duplicate REC-BB-FUNC-001 are closed as repaired and
verified on the frozen repair snapshot below. The Backbone local publication
gate is satisfied.** This dated addendum supersedes the earlier open-finding
publication block; the original finding, severity, repair scope and evidence
above remain preserved. It does not change the separate AO or remote/platform
acceptance states and does not provide human merge/release approval.

### Closure binding and evidence

- Prior Full head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Quality-tested repair head: `0778d728a273bc6af845b18d33f96e5731df9bc9`.
- Delta-reviewed repair head: `c2c31eed661714c0d8bc2245ff8505ac01a60c9a`.
- Delta-reviewed tree: `15bf96a0d003cc6b9d20dc1482d250b35dbbb44b`.
- Prior-Full-to-repair binary patch SHA-256:
  `574e5505fb0765a0bae674a3eb1d51419c64218a1b8f37a0233fb55db04d7279`.
- Base-to-repair binary patch SHA-256:
  `d34ceb2a0aee308a460f43e0da0ad4efea9cf3955f56cc27651f1f31a071cb92`.
- Independent quality record: `opencode-reconstruction-repair-checks.md`, SHA-256
  `4dfe1e02cbbd47e8eb8fba042c434bab6e98794abe661547bd87fd010a6e49c7`.
- Completed independent Delta: `opencode-reconstruction-delta-security.md`,
  SHA-256 `77f79038348b2e8cc52815d132d7e36d0f90e5db47be984fc918a4fbfa12c6f2`.

Read both completed records and independently confirmed the Delta snapshot's
head, tree, patch hashes and clean worktree. The quality-tested and Delta-reviewed
heads differ only by the added quality record; there is no intervening product or
test change. The repair consists of the approved workflow authority addition,
test changes and two separate predecessor-fixture files. Existing historical
fixtures and production guard payloads remain unchanged. Other additions since
Full are the review, triage and quality evidence records.

Triage verified all ten raw command-log hashes against the repair manifest, whose
SHA-256 is `031e64636fa4bb0f119adccdf943cf21d091524eb524cab13840dc85c00d7eb4`.
The actual full-suite log ends with **414 tests in 355.728 seconds, OK**; its
SHA-256 is `d568708d1a0409c7878438a60143f382c6f22239008f4fcc3d6dd7934438938f`.
The complete suite and all nine deterministic gates recorded exit 0. These are
the independent quality session's executions, not reruns claimed by triage.

The independent Delta reviewer confirmed that the authority list adds exactly
the approved predecessor digest and that the executable workflow payload is
byte-identical. The reviewer freshly rendered the exact trusted base, checked all
eight source-tooling blobs, and established that all 45 fixture files match that
rendering byte for byte; only documented installation-path answers metadata is
omitted. The ZIP and complete rendered-tooling digests match the recorded values.
This establishes provenance independently of the fixture's own manifest claims.

The Delta reviewer also executed five focused regression tests: unchanged
predecessor tooling and coherent current-tooling adoption pass; unknown baseline,
unknown candidate and mixed tooling remain rejected; exact historical authority
and clean single-commit/autocrlf behavior remain intact. All five passed in
31.497 seconds, exit 0. The review reports no confirmed repair defect or direct
regression. This closes the original workflow-envelope failure without weakening
membership, coherence or predecessor execution checks.

### Final classifications and next step

| ID or gate | Final triage disposition |
| --- | --- |
| REC-BB-SEC-001, original triaged P1 | Closed: the exact approved predecessor is retained and its original rejection path is repaired and independently verified. |
| REC-BB-FUNC-001 | Closed by the same verified repair; duplicate alias remains preserved. |
| New repair findings or human-decision items | None submitted by the completed Delta; no additional repair is authorized. |
| Local Backbone check/review chain | Complete: two Full reviews, separate triage, one bounded repair, fresh complete quality checks and independent Delta. No further Full or repeat testing is required for unchanged implementation. |
| AC-4 immediate-predecessor regression | Closed by actual positive/negative workflow execution and independently verified fixture provenance. |
| Native Windows and Docker build/smoke | Still pending actual PR CI execution. Local Linux smoke evidence remains limited to its unchanged recorded inputs and canned-provider observations. |
| AO implementation and full gates / paired delivery | Separate and pending; this Backbone closure does not certify AO or complete the paired delivery. |
| Remote identity, visible Codex request and actual CI/review outcomes / AC-8 | Pending publication-phase work. Record observed results and triage any remote findings before repairs. |

The root may now finish the explicit acceptance mapping, persist the final review
and closure records, and publish the already authorized Backbone PR. Verify the
actual remote tree against the intended local tree, provide the frozen review
bindings with a visible Codex request, and inspect actual CI/review outcomes.
State the pending Windows/container and separate AO gates in the PR; publication
does not turn those states into PASS. Evidence-only closeout records do not
reopen the unchanged implementation review.

No qualified runtime/model default, OS confinement, native compaction/resume/
delegation qualification, activation, merge, release, deployment, settings change
or automatic downstream adoption is authorized by this closure. This session
appended only this addendum to its existing triage record; it made no product,
test, immutable-snapshot or remote changes.
