# PR 18: bounded layout corrections

Status: proposed for independent plan review; no implementation or verification is
claimed. Task: [BB-LAYOUT-012](task-packet.json). The user requested correction of
missed Copilot/root-file handling and red checks in the existing refactoring PR.

Corrective baseline: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` in the local
`backbone-layout` worktree, initially clean. The existing draft
[PR 18](https://github.com/Artifaktory/engineering-backbone/pull/18) still targets
`main`; its original layout base is
`212608aa50ee517b3dd3107a9480da997222fd4f`. These are different comparison purposes,
not interchangeable tested snapshots.

## Confirmed observations and scope

| Observation | Bounded action |
| --- | --- |
| COP-LAYOUT-01: source `backbone-docs.instructions.md` uses `*.md,docs/**,plans/**`, missing 19 new nested Markdown paths outside `docs/` | Change the source selector to `*.md,**/*.md,docs/**`; preserve the legacy generated consumer selector and native location |
| All 24 active Copilot files already have retargeted references; 67 relative links were checked without a broken link | Record the audit coverage; do not invent another relocation |
| Root `copier.yml` is Copier's legacy discovery entrypoint, not a Copilot configuration file | Preserve it and the existing `.engineering-backbone/legacy/templates` target |
| Foundation CI passed all 432 tests in 279.873 seconds, then failed the committed diff check on an extra blank EOF line at `docs/changes/backbone-layout/publication.md:56` | Remove only the extra blank EOF line and verify the committed PR diff after the final evidence commit |
| The actual old trusted-base validator reports 34 path-layout errors | Preserve that failed gate; diagnose its requirements and document a concrete separately reviewed follow-up, without bypass or trust migration in this correction |
| Docker/dependency and native Windows/Linux jobs passed at the observed remote head | Record their actual run/head identities and conclusions; do not treat them as evidence for an unpublished later head |

The selector semantics are documented by GitHub's
[repository instruction guide](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions):
`*` matches within one directory and `**` spans directories. This is a selector
coverage correction, not proof of native Copilot loading or model behavior.

The original broad frontend selector predates this refactor. Its narrowing would
be a separate product/layout decision and is excluded. Native `.github`, `.codex`
and `.opencode` locations, tool permissions, canonical policy, compiled guards,
schemas, dependency inputs, legacy generated contracts and historical bytes are
unchanged. No source-policy or trust-boundary relaxation is authorized.

## Implementation sequence

1. Obtain an independent read-only review of this plan and Task Packet before
   implementation. Root coordinates separate planner, implementer, quality
   checker, reviewer and triage sessions.
2. Reproduce COP-LAYOUT-01 with repository-path matching that preserves the
   documented slash semantics. A whole-path `fnmatch` implementation whose `*`
   crosses `/` would hide the defect and is not adequate evidence. Require the
   original selector to miss a nested component README, then require the corrected
   source selector to match root `README.md`, nested component Markdown, nested
   tooling Markdown and a JSON document under `docs/`. Assert that a TypeScript or
   Python source file outside `docs/` does not match. Keep the legacy consumer's
   established selector assertion explicit rather than weakening parity checks.
3. Apply the source selector correction and the smallest affected distribution
   test updates. Preserve all instruction bodies and legacy rendered output.
4. Remove the extra EOF blank line from the publication record. Preserve its
   earlier timestamped claims; new observations belong in this corrective change
   record, not in rewritten historical results.
5. Add the committed-diff publication requirement to the current contributor
   documentation and command list. Check unstaged and staged edits during work,
   then check both the corrective baseline-to-HEAD diff and the complete PR
   base-to-HEAD diff after the final documentation/evidence commit. A clean
   worktree-only `git diff --check` cannot validate already committed changes.
   Record exact resolved base/head IDs and exit codes; any later commit invalidates
   this final publication check until rerun.
6. Write current remote evidence and a trust-migration follow-up note under this
   corrective change directory. Bind all CI observations to their exact remote
   head and run IDs. The follow-up specifies what the trusted base must recognize,
   required policy/permission/missing-file rejection tests, independent review and
   human adoption steps. It creates no unrelated branch or new PR and implements
   no fallback, projection, exemption or workflow suppression.
7. Have a separate quality checker execute the affected suites, structural and
   compiler checks, and committed-diff checks. Use the existing full-suite CI as
   evidence only for its recorded head; require current-head remote results after
   publication. Run a fresh local full suite if targeted results identify a
   concrete wider regression risk, not to manufacture a blanket PASS claim.
8. Freeze a committed corrective snapshot with base/head and SHA256 of
   `git diff --binary <corrective-base> <head>`. Independent behavior and
   governance/security Full review may be covered by one independent reviewer
   with explicit coverage, or two parallel reviewers using the same snapshot.
   A separate triage session classifies findings before fixes. Delta covers only
   confirmed repairs and their direct regressions. At most two Full rounds and six
   implementation iterations are available for this scope.
9. Update the existing PR 18 branch and description only. Verify remote head/tree
   correspondence and read back current check conclusions. Keep the PR draft and
   distinguish the repaired Foundation issue from the unresolved trusted-base
   migration gate. No merge, release, repository settings or downstream changes.

## Verification and evidence

Use the existing isolated Python 3.12 environment and unchanged reviewed lock.
Required affected checks include `tst.test_copilot_distribution`,
`tst.test_copilot_validation` and `tst.test_copilot_workflow_guard`, with the new
selector regression included. Run from the bundle import root or set the existing
project import path explicitly. Run the canonical validator, all four compiler
`--check` commands and the source-dependency check to detect unintended drift.
The compiler outputs themselves are not expected to change.

The final publication checks are:

```sh
git diff --check
git diff --cached --check
git diff --check c50108773ba3195bf0f7503e5dffb2d7bfc78cd3 HEAD
git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f HEAD
```

Also resolve and record the live PR base. If it advances, run the full PR diff
check against that actual base as well; do not silently retain a stale identity.
The known pre-fix complete PR diff must reproduce the EOF failure, and the final
committed complete PR diff must pass. Evidence-only files are not exempt.

The trusted-base job remains a real failed gate. Report its exact observed
validator/base/head and error category without substituting candidate results.
Candidate checks do not authorize changes to trust. The concrete follow-up is a
proposal for later scoped review, not executed migration or permission to merge.

Closeout maps each acceptance criterion to exact commands/results and review
coverage, including pending or blocked states. Newly passed container/native jobs
may update the prior environmental evidence gap for the tested head, but they do
not establish native Copilot runtime discovery or product qualification. Recovery
is a normal reviewed corrective commit; no destructive Git operations are used.
