# Dependency compatibility — independent triage

**Current disposition:** follow-up triage below confirms `DEP-TEST-001` after the
full-suite result arrived. Publication is blocked pending its bounded repair,
verification and Delta review. The original no-finding disposition is retained
below as historical evidence and is superseded by that new executed result.

- Role: `/root/dependency_triage`, separate read-only triage session.
- Task Packet: `artifacts/dependency-compatibility/triage-task.json` (`BB-DEPS-009-TRIAGE`).
- Base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
- Reviewed head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`.
- Patch SHA256: `6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0`.

## Inputs and scope

Read `AGENTS.md`, `CONTRIBUTING.md`, `policy/core.md`, `policy/quality.md`,
`plans/dependency-compatibility.md`, the assigned Task Packet, both independent
Full reports (`full-behavior-review.md` and `full-authority-review.md`) and the
current `quality-results.json`. Independently confirmed HEAD, patch digest and
absence of tracked worktree changes. The output path is ignored by Git.

This role classifies the supplied review conclusions and outstanding evidence;
it does not perform another Full review, rerun the quality suite, edit source or
tests, approve its own implementation, or authenticate a human merge decision.

## Finding disposition

Both required Full reviewers inspected the same frozen base/head/patch and report
**NO CONFIRMED IN-SCOPE FINDINGS**. Neither supplies an actionable finding ID.

- Confirmed findings: none.
- Rejected findings: none; no finding was submitted for rejection.
- Findings requiring a human decision: none.
- Authorized implementation repairs from this triage: none.
- Repair Delta review: not applicable while there are no confirmed repairs.

The reported limits do not establish implementation defects or fabricated PASS
claims: the reviewers and quality checker explicitly preserve pending and
unexecuted states. This conclusion is bounded to their documented coverage and
the immutable snapshot above; it is not universal compatibility certification.

## Evidence disposition and gates

| Evidence | Observed state | Triage disposition |
| --- | --- | --- |
| Validators, four compiler checks, source dependency check, Actionlint and diff whitespace | All nine recorded commands exited 0 in the independent quality record. | Accepted as supplied execution evidence, not claimed as rerun by triage. |
| Clean locked installation and immediate-predecessor Copier upgrade/attestation | Recorded PASS with command/log references and upgrade coverage. | Accepted as supplied evidence within its stated scope. |
| Full regression suite | `full_suite.result` remains `running`; the inspected log has no final completion summary. | Required local publication evidence remains pending. Do not publish as locally checked/complete until actual successful completion is recorded. A failure requires diagnosis and appropriate triage before repair. |
| Local Docker build and image smoke | `not_executed`; Docker executable unavailable. | Environmental execution gap, not a confirmed source defect. The approved plan explicitly allows actual GitHub CI execution after PR publication. Keep AC-4 container execution pending until the real CI job succeeds on the published snapshot. Do not claim container compatibility from static review or base-image metadata. |
| Remote PR tree identity, CI status and visible Codex request/result | Not yet executed at triage time. | Publication-phase obligations under AC-7; require actual remote tree readback and visible review request. Preserve pending/blocked/failed CI states and triage any remote findings before repairs. |
| Native Windows, downstream PostgreSQL/application combinations and native agent loading | Outside the reviewers' executed coverage. | Explicit limits, not evidence of universal support; do not infer PASS for these paths. |

The local review chain can proceed without repairs, conditional on the required
local checks actually finishing successfully. Publishing an authorized PR for
remote CI does not complete the container acceptance criterion or authorize merge,
release, deployment or downstream adoption. Human merge/release gates and any
stronger installed project controls remain binding.

## Return decision

**NO CONFIRMED IN-SCOPE FINDINGS; NO REPAIRS AUTHORIZED.** The next step is to
collect the final full-suite result, then publish only if the local publication
gate is satisfied, verify the actual remote tree, run CI and request Codex review
with the frozen review context. Actual successful container build/smoke is required
before claiming container compatibility. No source, test or tracked file was
changed by this triage; only this ignored report was written.

## Follow-up: completed full-suite failure

The independent quality run subsequently completed on the same frozen head:

```text
.venv/bin/python -m unittest discover -s tests -v
Ran 362 tests in 1289.482s
FAILED (failures=3)
exit=1 elapsed=1291.44s
```

Evidence: `quality-unittest.log`, final summary and three reported failures.
The previously inspected `quality-results.json` still had its older `running`
state during follow-up inspection; the completed raw command log is authoritative
for the result and the quality checker must reconcile that record. No earlier
report's explicit pending state is retrospectively called a fabricated PASS.

### DEP-TEST-001 — confirmed P2 test-contract regression

- Category: compatibility/regression test synchronization.
- Confidence: high.
- Location: `tests/test_workflows.py:281-284`, expected historical authority set;
  related current-diff change: `.github/workflows/governance-checks.yml:79-80`.
- Trigger: the current delivery moves the trusted merged main toolchain digest
  `e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450`
  from `CURRENT_TOOLCHAIN_SHA256` into `PREVIOUS_TOOLCHAIN_SHA256`, preserving
  immediate-predecessor adoption. The strict explicit test expectation omits it.
- Execution path: `test_approved_historical_copies_match_authority_and_remain_usable`
  fails its set equality; the clean single-commit clone and autocrlf checkout
  tests invoke that same test and consequently fail as well.
- Impact: the required full regression suite and its CI gate fail. This evidence
  does not show a bad authority digest or broken predecessor compatibility.
- Diff causation: the workflow authority set changed in this delivery; its
  explicit expected-set test was not updated for the retained reviewed identity.
- Acceptance relation: AC-3 predecessor compatibility and AC-5 deterministic
  checks; the existing full-suite publication gate remains failed.
- Reproduction: the completed independent suite reports only this extra-set item
  in all three failures. The exact predecessor upgrade/attestation log separately
  records successful execution against the old/new copied toolchains.

Additional independent provenance check by triage, exit 0:

```text
.venv/bin/python - <<'PY'
from pathlib import Path
from scripts.compile_toolchain_fingerprint import rendered_digest
print(rendered_digest(Path('artifacts/dependency-compatibility/trusted-base').resolve()))
PY
e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450
```

The base/head workflow diff also shows this exact value was the trusted base's
current digest. It is not an invented newly approved historic identity.

### Authorized bounded repair

Add a clearly named constant for the merged technology/navigation predecessor
digest to the explicit union in `test_approved_historical_copies_match_authority_and_remain_usable`,
and update its neighboring explanatory comment if needed. Preserve exact set
equality, all existing identities, immutable historical fixtures, workflow
authority and runtime implementation. Do not remove the valid predecessor digest,
accept arbitrary extra digests, use subset containment, or skip any failed test.

### Verification and gate handling

1. An independent quality checker must rerun all three failing test entrypoints
   on the frozen repaired snapshot: the direct historical test and both clean
   clone/autocrlf wrappers. The wrappers also exercise their nested real Copier
   upgrade test. Run diff-whitespace and retain actual exit codes/logs.
2. Independent Delta review must verify `DEP-TEST-001`, its exact trusted-base
   digest provenance, preservation of the strict authority assertion and absence
   of direct repair regressions. Wider changes would require rescoping.
3. The original suite supplied 359 passing tests and three failing tests. Those
   original results plus three successful targeted reruns provide strong bounded
   repair evidence if the implementation and unrelated tests remain byte-identical.
   They do **not** turn the original full-suite command into PASS or constitute
   a full-suite execution on the repaired revision.
4. The approved plan explicitly requires the full unittest suite and AC-5 records
   required deterministic checks passing. To satisfy that gate as written, run
   the full suite successfully on the repaired snapshot before publication. Do
   not silently replace it with a composite `359 + 3` PASS. A targeted repair
   check may finish earlier, but the full-suite gate remains pending until the
   actual required result is available.

Updated disposition: **one confirmed finding (`DEP-TEST-001`); bounded test repair
authorized; publication blocked until its required verification and Delta review
close it.** Docker and remote publication evidence retain their previously
documented pending/unexecuted dispositions. Triage changed only this ignored report.
