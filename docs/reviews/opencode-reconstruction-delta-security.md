# OpenCode reconstruction: independent authority/security Delta review

Date: 2026-10-16. Reviewer: `bb_reconstruction_full_security`.
Mode: **Delta**, limited to the confirmed immediate-predecessor admission finding
and regressions directly introduced by its bounded repair. This session authored
the prior security Full report but did not implement the repair, perform its
separate triage, or author its independent quality-check report.

## Immutable review binding

- Repository: `Artifaktory/engineering-backbone`; Task `BB-OPENCODE-010`.
- Trusted base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Prior Full head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Repaired head: `c2c31eed661714c0d8bc2245ff8505ac01a60c9a`.
- Repaired tree: `15bf96a0d003cc6b9d20dc1482d250b35dbbb44b`.
- Prior-Full-to-repair binary patch SHA-256:
  `574e5505fb0765a0bae674a3eb1d51419c64218a1b8f37a0233fb55db04d7279`.
- Base-to-repair binary patch SHA-256:
  `d34ceb2a0aee308a460f43e0da0ad4efea9cf3955f56cc27651f1f31a071cb92`.

Reviewed the detached, clean `artifacts/backbone-delta-snapshot` checkout. Verified
the head, tree, both patch hashes and clean state at entry and close. Read the
separate Full-review triage and independent repair-check report against the
previously inspected repository policy, approved plan, Task Packet and Full
finding. This report is written outside that immutable checkout.

## Disposition

| Finding | Delta result |
| --- | --- |
| REC-BB-SEC-001, triaged P1 | **Repaired and verified.** The exact approved immediate-predecessor digest is retained, and its unchanged/coherent-upgrade workflow paths pass. |
| REC-BB-FUNC-001 | **Same verified repair; duplicate alias preserved.** No second repair obligation. |

**NO CONFIRMED IN-SCOPE FINDINGS in the repair or its directly affected paths.**
The original trigger is closed at this frozen repair snapshot. Return this result
to separate triage for the final disposition; it is not human merge/release
approval or evidence that the paired AO and pending platform gates are complete.

## Repair and authority assessment

The four product/test repair files are the reusable workflow,
`tests/test_workflows.py`, and the separate predecessor fixture's manifest and
ZIP. Other changes since Full are the two Full reports, separate triage and
independent repair-check record. The existing historical fixture directory is
unchanged. The quality-tested head
`0778d728a273bc6af845b18d33f96e5731df9bc9` differs from the reviewed head only by
the added repair-check report, so no product/test change intervened after those
recorded checks.

Independently compared parsed workflow authority and executable payload against
the prior Full snapshot:

- The previous list is exactly the old ordered list plus
  `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`.
- The current identity remains
  `a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`.
- The actual validation shell payload is byte-identical. Fingerprint membership,
  coherent-tuple requirements, isolated compiled guards and trusted predecessor
  validator execution were not relaxed or replaced.

This restores a specifically verified previously approved identity; it does not
grant the candidate authority to choose a digest or admit unknown tooling.
The original Full failure occurred before validator execution. The new regression
uses that actual workflow envelope rather than only calling a validator directly.

## Independent fixture provenance verification

Verified the trusted checkout is clean at exact commit `bf8e901...`, with tree
`7e4bc46ec7d4ca4805bcd9f03d49c05d662ebd31`. Independently compared all eight
`source_tooling_blobs` entries to `git rev-parse HEAD:<path>` in that checkout.
Each matches the manifest.

Copied that exact source to a temporary plain source directory, excluding Git
metadata, environments and ignored artifacts, then performed a fresh actual
Copier `run_copy` with `defaults=True`, `quiet=True`, and `skip_tasks=True` using
the locked project environment. Compared the rendered path set and every raw
file against the manifest and ZIP:

| Provenance check | Actual result |
| --- | --- |
| Exact source commit/tree and eight source tooling blobs | PASS |
| Fresh exact-base rendering versus archived fixture | All **45 files byte-identical**, with identical path membership |
| Omitted path | Only `.engineering-backbone/copier-answers.yml`, as documented; installation-path metadata is not part of tooling authority |
| ZIP SHA-256 | `bc94bbb16d5fbeaa3e8bc41f49e0c1f8518d79617b6b05a0cfa6354eb4349d70`, matches |
| Actual rendered tooling digest | `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`, matches |

The provenance command exited 0. No project hooks or native OpenCode process ran.
The test fixture loader verifies exact commit/tree/digest identifiers, ZIP hash,
unique expected paths, regular-file mode, path/size bounds, every file hash and
the complete tooling digest. It writes only into the tests' newly created or
reset temporary consumer directories. The fixture has no network or historical
Git-object dependency. The immutable source provenance was independently checked
here rather than inferred merely from the manifest's self-description.

## Independent regression execution

From the immutable repair checkout, using Python 3.12 and the hash-locked
`engineering-backbone/.venv/bin/python`, executed:

```sh
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python -m unittest \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unchanged_and_coherent_current_tooling_pass \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unknown_and_mixed_tooling_stay_rejected \
  tests.test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable \
  tests.test_workflows.WorkflowTests.test_historical_compatibility_survives_clean_single_commit_clone \
  tests.test_workflows.WorkflowTests.test_historical_compatibility_survives_autocrlf_source_checkout -v
```

**PASS: five tests, 31.497 seconds, exit 0.** No exclusions or assertion changes.
The positive test executes the actual candidate workflow with old-to-old tooling
and then old-to-current coherent tooling. Negative paths reject an unknown
candidate, an unknown trusted baseline and a mixed tuple of otherwise approved
versions; the unapproved validator execution marker stays absent. The exact
historical identity-set equality remains enforced. Clean single-commit and
autocrlf checkout cases also execute the predecessor positive/negative cases
while asserting the original predecessor commit/tree objects are unavailable.

The earlier Full reproduction established the unchanged missing-authority failure
and isolated its cause. These newly executed repaired tests, plus the independent
fresh fixture rendering, close that original trigger without relying on the
author's temporary diagnostic or a weakened test expectation alone.

## Supplied quality evidence and remaining limits

Read the independent repair-check report and verified all ten supplied command
logs against the manifest hashes: nine deterministic gates and the complete
suite, each recorded exit 0. The full log SHA-256 is
`d568708d1a0409c7878438a60143f382c6f22239008f4fcc3d6dd7934438938f`;
its final output records **414 tests passed in 355.728 seconds**. These full-gate
executions belong to the separate quality session; this Delta reviewer ran only
the focused commands and provenance comparison above.

The four-file repair does not change native adapter inputs or the smoke runner.
The independent quality report records equality for all 22 prior Linux-smoke
inputs and its runner. No native execution was repeated and no previously blocked
malicious native reproduction was attempted. This Delta does not reopen unchanged
Full-review scope or establish new native/model behavior.

Native Windows and container execution, real-model qualification, OS confinement,
native compaction/resume/delegation qualification, the paired AO implementation,
and remote PR/CI/review outcomes remain outside this repair review. Their existing
pending or blocked states remain explicit. No code/test repairs, commits, remote
writes, activation, merge, release or settings changes were made by this session.
