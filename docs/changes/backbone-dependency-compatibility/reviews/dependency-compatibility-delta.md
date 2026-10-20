# Dependency compatibility — bounded authority Delta

Reviewer: independent read-only authority/security session.
Task: BB-DEPS-009-DELTA.
Prior Full head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`.
Repaired head: `79fc21fbc5ff77938e3d2d952b90550cb36dedbd`.
Repair patch SHA256: `c695e338d61b3d3ce182269f3d1217418fd5b28d747e3012e6c094f5a4a840e5`.
Confirmed finding: `DEP-TEST-001`.

## Disposition

**DEP-TEST-001: CLOSED. NO CONFIRMED DIRECT REPAIR REGRESSIONS.**

This bounded Delta does not reopen unchanged Full-review areas or replace the
required full-suite, container, publication or human-approval gates.

## Inspection and provenance

Read the Delta Task Packet, triage follow-up, exact repair patch and neighboring
historical-authority test. Independently verified the patch digest, frozen repaired
HEAD and clean worktree. The entire repair changes only `tests/test_workflows.py`
with two inserted lines and one deleted line.

The repair adds the named `merged_technology_navigation` predecessor constant to
the existing explicit expected-set union. Exact `assertEqual(set(previous), ...)`
remains in force. Every prior authority literal, historical fixture assertion,
actual historical-consumer validation and current rendered-fingerprint assertion
is preserved. No workflow authority, runtime code, historical fixture, test skip,
subset acceptance or failure masking changes occur.

Independently exported the exact trusted base commit
`229ac884c1a2ac70f0fb5c961bd517c9eaf740af` using `git archive` into a temporary
read-only review input and ran `rendered_digest` on those bytes with the unchanged
compiler helper. Compared the result to both the base workflow's current literal
and the repair's newly named constant. Command exit 0:

```text
PASS exact trusted-base Git archive rendered digest and workflow literal:
e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450
```

Thus the added expectation identifies the actual already reviewed predecessor;
it does not approve an invented or arbitrary historical identity.

## Verification and limits

Inspected `quality-repair-targeted.log`: all three originally failing entrypoints
passed, 3 tests in 62.722 seconds, exit 0. This is independent quality-checker
execution evidence, not claimed as rerun by this reviewer. Their clean-clone and
autocrlf wrappers also exercise the nested existing checks.

The first full-suite run remains a failed historical result. The repaired-head
full-suite rerun is separately pending and remains required by the approved plan;
359 prior passes plus three targeted passes are not labeled a successful full
suite on this revision. Docker build/smoke and remote publication evidence retain
their previously documented pending/unexecuted status.

No source, tests, tracked files, workflow settings or external state were modified.
Only this ignored review report was written; temporary provenance files were
cleaned. This conclusion is independent advice, not human merge/release approval.
