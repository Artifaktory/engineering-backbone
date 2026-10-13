# Quality framework Full finding triage

Independent read-only triage: `quality_check_triage`. Both Full reviewers finished
before triage. Base `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`, head
`b22fd3e2f60d93ea6053f1df09bd6d079ce8c69f`, tree
`572e9fe1099da111fa040b94ee5a8aca08db1f3f`, full-index binary patch SHA256
`a693e7d51193bd822538905676ba352b9acaec52d3f383651d2b18a177421c49`.
The review checkout stayed clean.

Q-B-1: **confirmed**, P2, high confidence, before any source repair. The quality
guard invents a plural `dependencies` check kind from the capability. The existing
workflow contract requires singular `dependency` checks for PR and maintenance.
The independently observed rejection agrees with the source mapping and affects
AC-2/4. Security Full reported no additional confirmed in-scope findings.

Authorized repair is bounded to an explicit capability/kind mapping for dependency
and container, a regression for valid coverage and each missing required phase,
compiled propagation and the current fingerprint. Preserve every merged previous
fingerprint and all existing gates. Do not retain interim unmerged tooling.

This restores the existing contract without expanding scope or authority. A scoped
Delta of Q-B-1, compilation/fingerprint and direct regressions is sufficient. Wider
changes would require a new Full. Relevant checks and the required full suite must
pass before declaring the repair/review chain complete. The triage session made no
edits or repeated tests.

Repair evidence before independent Delta: the new six-case regression ran against
the original guard first and failed the two valid coverage cases (active profile
and inactive seed), exit 1. Missing PR and maintenance coverage remained rejected
by both guards. After the explicit mapping repair, all 31 engine tests passed in
1.843 seconds, exit 0. The guard was recompiled into both entrypoints and the
current rendered fingerprint became
`88d2d1e89cbff9fd925cac1a235de60867ae90a9ae231cde6cbc0a5eed8ee9b2`.
Neither interim unmerged fingerprint was added to retained authority. The complete
repaired suite and independent Delta conclusions are still pending at this record.

Subsequently the independent complete repaired run passed 278 tests in 655.696s.
[Both scoped Deltas](quality-delta-review.md) confirm Q-B-1 fixed with no additional
confirmed in-scope findings. The local finding is closed.
