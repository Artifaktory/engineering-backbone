# Independent behavior Delta review

Reviewer: `layout_behavior_review`, the independent behavior Full reviewer.
Mode: bounded Delta for confirmed **LBEH-01, LBEH-02 and LBEH-03**, including direct
repair regressions. Outcome: **all three findings resolved; NO CONFIRMED IN-SCOPE
FINDINGS** in this Delta. This is not human merge or release approval.

## Frozen subject

- Original base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Prior Full-review head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Repaired head: `97e68ecefbd21b0d022514f46520a75a6a025536`.
- Repaired tree: `c3ef52a5eaecff857f66ec1599257c2656cc1474`.
- SHA256 of `git diff --binary PRIOR_FULL REPAIRED`:
  `19f36e00426e33d9b1e02f82324ad998cf1b9da1e36b4a7faac490e6c3bb6512`.

The repaired head, tree, patch digest and clean frozen worktree were verified.
Read the preserved [Full report](behavior-review.md), independent
[triage](review-triage.md) and separate [targeted repair checks](repair-checks.md).
The last report was written after the frozen commit and is execution evidence
bound explicitly to the same repaired head/tree/patch; it was not represented as
part of that committed snapshot.

## Finding dispositions

| Finding | Delta disposition | Evidence and direct-regression assessment |
| --- | --- | --- |
| LBEH-01 | Resolved | The workflow now discovers `.engineering-backbone/tst` with `.engineering-backbone` as the import top level and selects `test_opencode_native_smoke.py`. The checker extracted and executed the actual workflow command: 12 tests passed, exit 0. Matrix, permissions, pinned actions, subsequent native command and artifact handling are unchanged. |
| LBEH-02 | Resolved | The legacy adoption paragraph again names `docs/dependency-compatibility.md`. It agrees with the actual conditional legacy template path and `copier.yml` preservation list. No template, preservation rule or direct-copy source path changed. |
| LBEH-03 | Resolved | The runner's default uses `parents[2]`, selecting the repository root from `.engineering-backbone/src/`. Explicit `--repo` parsing and resolution remain unchanged. The added regression invokes actual `main()` from another working directory, performs actual fixture preparation, verifies all 22 inputs and root native configuration, and passes in the affected module. Only the download/native-execution wrapper is substituted. |

Compared all changed executable, test, workflow and adoption lines in the Delta;
the other added files preserve Full-review, triage and structured evidence. The
new default-root test exercises the failure path identified in Full rather than
only comparing a constructed path. Native fixture validation, archive checks,
permission handling and existing failure assertions remain unchanged. The narrow
repairs introduce no additional confirmed behavior or compatibility defect in the
reviewed paths. No broader contract or trust-boundary change requires another Full
round for these repairs.

## Evidence limits

The independent checker, not this review session, executed the 12-test command,
canonical validator, actionlint and whitespace checks recorded in
[repair-checks.md](repair-checks.md). This Delta inspected that evidence and the
actual frozen diff; it did not rerun the complete suite or claim a new 432-test
full-suite result. The previous 431-test full result retains its original revision.

Unchanged Full-review areas were not reopened. Actual OpenCode native execution,
Windows behavior, model qualification and container execution remain outside this
Delta's demonstrated coverage. The old trusted validator's disclosed 34
path-related errors remain the separate draft migration blocker. Resolving these
three defects neither passes that gate nor makes the PR merge-ready.
