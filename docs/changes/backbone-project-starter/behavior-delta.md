# Scoped behavior Delta

Independent reviewer: `starter_behavior_full`. Prior Full
`f0230d0da90b17ef52932ff027529acd23d73f51`; repair
`bb794a6b05e35f168ee90d4dcbe5055f674eeead`; tree
`b96337072a048afa37eee2135f3fafeaa76f8782`.
Full-to-repair binary patch SHA256
`1913af276440e84684ec4e7bae5787f8b46ac9687732576af684e0690894de46`;
actual base `4e74c7e5f3a07430768f670c4271c1e1a0e28f68` to repair SHA256
`fba134f81573d5100933bf63a2df6ac169c6ab8d34c90df1b86e9cd6b0abbfc9`.
Identity, clean tracked state and both committed whitespace ranges independently
matched. Review started only after the new complete independent checks passed.

**START-BEH-01/02/03 resolved. NO CONFIRMED IN-SCOPE FINDINGS in these repairs or
their direct regressions.**

| Finding | Independent Delta proof |
| --- | --- |
| START-BEH-01 | Actual CLI rejects ordinary and indented NUL-bearing comments with exit 1 and redacted output; ordinary comments pass with exit 0. NUL checking precedes comment skipping. |
| START-BEH-02 | Fresh exports reject all five schema-valid violations: self-review, duplicate reviewer IDs, duplicate finding IDs, duplicate Task Packet acceptance IDs and duplicate requirement acceptance IDs. Valid records pass; private sentinel identity is absent from exposed errors. Actual unchanged Git-attested `validate_data` and Git-owned schemas are reused without the constructor/full source-history run. |
| START-BEH-03 | Fresh exports reject nested and dangling governed directory links. Ordinary nested valid records pass; nested malformed records fail; product JSON fixtures still pass. Nonfollowing entry inspection precedes JSON selection and traversal. |

Reviewer read the complete repair diff, added regressions, independent triage and
repair records. Shared containment/alias helpers support BEH-03; the separate
AUTH-01/02 closure belongs to the authority reviewer. No unchanged area was
reopened and no new Full was performed.

Bounded independent TEMP probes used Python 3.12 `-I -B`, actual export/verifier
and environment CLI calls; 5.299 seconds, exit 0. A fresh export still verified
166 managed files. No tracked writes; final read-only snapshot stayed clean.
Commands also included Git head/tree/status, both binary patch digests and
`git diff --check` for base/repair and Full/repair.

The reviewer read the actual final quality metadata and independently recomputed
all sixteen indexed log hashes: no mismatch. All eleven quick gates passed; the
complete independent run recorded 528 tests, zero failures/errors/skips, exit 0,
684.798 seconds unittest / 685.554 seconds wrapper. Full-log SHA256
`5341628170577ac7a4cd78321c0da9c6add74fe0a524fa6ffdf00ac8c87a4240`.

No scoped Delta area remains unreviewed. Native Windows junction branches were
not executed on Linux. Docker, actual fleet/runner access, live provider and remote
CI remain unqualified. Later report-only commits are outside this frozen subject.
These dispositions support separate final triage; they are agent advice, not
human merge, release or deployment approval.
