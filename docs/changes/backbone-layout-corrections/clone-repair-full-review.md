# BB-LAYOUT-012: second Full review of COP-CI-02 repair

Date: 2026-10-20. Independent reviewer: `correction_full_review`. This is the
bounded second and final Full round within BB-LAYOUT-012's two-Full budget. It
covers the newly diagnosed clone repair and its direct regressions; the original
selector/EOF Full review remains historical evidence and is not reopened.

**NO CONFIRMED IN-SCOPE FINDINGS.** No P0-P3 defect attributable to this repair
was identified. Separate finding triage follows this report. Local verification
does not establish that the hosted Git 2.55 failure is resolved or permit merge.

## Frozen identity

- Published repair baseline: `2ddfa803688c70b556dc83bcf07a4c3911713be5`.
- Reviewed head: `e2bd3c7dc881348967af28a6da99be992e94e122`.
- Reviewed tree: `f94d11c832a8f5f0d492c1b8d7b6a71a91bec5c3`.
- Binary repair patch SHA256:
  `9c5a498c61b72e2774e1fac84856e2f35423fbed5b5b4e79edcccded7efd6000`.
- Reviewed test-file SHA256:
  `2dc0490bf69ed5986d6379e856543958eb9904f12cafbeacf3f5d224a44c2ce1`.

The reviewer independently resolved HEAD/tree, recomputed the patch digest and
confirmed exact equality with the supplied binary patch. The frozen worktree
remained clean and unmodified. This live report is the only reviewer write.

## Coverage and conclusions

The approved addendum, independent plan review and confirmed triage were read
before implementation review. Formal implementation review began only after the
separate quality checker completed the required checks. Read the complete test
diff and historical method, Task Packet changes, initial and confirmed failure
records, author evidence, and the installed Copier source-selection, clone and
answer-persistence implementation.

| Area | Review conclusion |
| --- | --- |
| Local transport | The resolved `git+file://` URI refers to the same temporary fixture. Installed Copier recognizes the `git+` prefix, removes it for Git and clones through the file URL. No network service or global Git configuration is introduced. |
| Versioned copy/update | Initial copy still uses `v0.1.0`; actual update and both installation-only rejection subtests still request `v0.2.0`. Each source revision is committed and tagged before its relevant use. The test does not depend on dirty-local-HEAD inclusion. |
| Persisted source binding | Added assertions inspect actual rendered answers after initial copy and upgrade. They require the selected URI and initial tag; the existing final-tag assertion remains. No answers file is manually rewritten. |
| Existing protection checks | Independent AST comparison confirms all 15 original assertion calls remain, with three additions and no removed/modified assertion. Both original real `run_update` call ASTs are unchanged. Local-policy byte preservation, negative installation-only cases, absence of rejection files and trusted consumer validation still execute. |
| Error handling | There is no added retry, skip, exception suppression, substituted update, or weakened expected failure. The existing negative cases still require their specific `ValueError` and unchanged target snapshot. |
| Trust and scope | Only the historical test method changes substantively. Supporting changes are corrective evidence and current Task Packet status. No runtime authority, native permission, workflow gate, dependency, schema, validator or legacy template changes. |
| Evidence honesty | Both failed remote attempts remain recorded. Reports distinguish observed Git 2.55 local-copy failures from an unproven underlying cause and keep changed-head hosted qualification pending. |

## Independent quality evidence and limits

The separate checker's [clone-repair-checks.md](clone-repair-checks.md) was read
as external evidence added after the freeze and bound to this exact head/tree and
patch. It records **41 affected tests passing in 78.308 seconds**, all 11 additional
structural/compiler/dependency/whitespace commands returning zero, and all 556
tracked input hashes unchanged. Its actual suite trace records 14 clones of the
historical fixture using `file://` and 14 corresponding upload-pack invocations.
That independently observed transport supports the proposed mechanism without
claiming an upstream Git defect was diagnosed.

This reviewer performed read-only source inspection, Git/byte identity checks
and the assertion/update AST comparison. No test suite was rerun by the reviewer;
the execution results above belong to the separate quality checker. No local
full 433-test, native client, container or model-session qualification is claimed.

The quality environment used Git 2.51.1 and Python 3.12.14. The two hosted
failures used Git 2.55.0 and Python 3.12.15. The required new full Foundation
result at the changed publication head remains pending. Another unchanged retry
is not authorized by this review if that changed-head run fails; its actual
failure requires diagnosis under the remaining task budget.

This report and subsequent evidence commits are outside the frozen snapshot.
After the final evidence commit, repeat full-PR, original-corrective and repair
committed-diff checks, verify remote head/tree correspondence, and observe current
checks. The separate old-main trusted-base layout gate and BB-LAYOUT-013 human
merge prerequisite remain unchanged. This review neither replaces that gate nor
reviews or adopts the separate compatibility implementation.
