# CI local-clone transport repair

## Scope and evidence
Task BB-CI-CLONE-006, HIGH by repository default. Human request on 2026-10-13
authorizes repairing the failed post-merge run, checks, independent review and PR.
Base: `465d11c31c82e0beae1ddcd54b8eb325ce94c1f3`.

Run 38291266449, job 114951680854 failed in the historical Copier upgrade nested
under the autocrlf checkout test. Git 2.55.0 local object copying returned ENOENT
before template/validator assertions. The unchanged targeted test passed locally
on Git 2.51.1; this is intermittent, not proof of a CRLF or consumer defect.
A controlled object-removal experiment reproduces the exact local-copy failure
while the repository remains valid and file transport succeeds. The original
hosted process that removed/moved the object is not identified; automatic
maintenance is only a hypothesis.

## Proposed repair
Use an explicit `git+` file URI for the committed historical source at first
Copier adoption in the existing real-upgrade test. Copier persists that supported
source URL and uses Git transport again for subsequent tagged updates. This
avoids Git's loose-object filesystem-copy optimization without changing pinned
versions, update behavior or any existing preservation/security assertions.

Extract only the existing upgrade scenario into a reusable test method and add
one behavioral regression. In its disposable source repository, relocate the
object directory and use a relative symlink. Verify native raw local cloning is
rejected and the repository is valid, then run the real Copier copy/update with
all existing local-facts, stricter-policy and coherent-tooling assertions. Native
Git transport supports this valid repository; reverting the URI repair must make
this regression fail. This synthetic negative case tests transport selection; it
does not claim to recreate the original runner's timing.

Only tests/test_workflows.py, this task/plan, CONTRIBUTING's active-task pointer
and scoped docs/reviews/ci-clone-* evidence may change. No workflows, validators,
templates, schemas, dependencies, fingerprints, historical fixtures or downstream
repositories change. No global Git configuration, maintenance disabling, retries,
test skipping or reduced gates.

## Sequence and acceptance
1. Independent read-only plan review before test/code edits.
2. Add the negative behavioral regression first, run against the old raw source
   path and retain the observed failure. Apply the URI repair and rerun.
3. Run both clean/squashed and autocrlf compatibility checks and the real upgrade.
4. Run the full suite, source validator, both compiler checks, trusted-base
   validator and committed diff whitespace checks. Record commands/exits.
5. Freeze base/head/full patch digest for independent behavior and test/coverage
   Full reviews. Triage before repairs. Only confirmed findings receive fixes;
   scoped Delta reviews follow each repair. At most two Full rounds and six total
   repair iterations, unless new evidence justifies an explicit scoped revision.
6. Publish the same reviewed tree as a PR, verify GitHub CI and advisory review,
   and provide a commit-bound closeout. Publication evidence remains pending until
   actually observed. Human merge is separate; post-merge CI can only be verified
   after the human merges the repair.

## Recovery and limitations
The change is confined to disposable test fixture transport. Reverting the PR
restores the old test behavior. Real consumer execution and released artifacts
are unchanged. The original hosted race writer remains unknown. No claims of
GitHub push success before a repair merge, downstream activation or host-setting
enforcement are made.
