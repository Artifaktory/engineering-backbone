# Integrate the merged compatibility prerequisite into PR 18

Status: proposed for independent plan review; no implementation or verification
PASS is implied. Task: [BB-LAYOUT-014](task-packet.json).

The user reported that PR #18 now conflicts and requested continuation of its
repair. PR #19 has actually been human-merged as
`537576f658bbd79c3bc49b26ade948116c664943`; its second parent is the reviewed
prerequisite head `fc707a8d51981d52445c2176711154dfd26145aa`.
PR #18 starts at `f1c1410cff6407109f286173f1ecc980cd2a14b7` on
`refactor/direct-copy-layout`. The common ancestor is
`212608aa50ee517b3dd3107a9480da997222fd4f`.
This task integrates actual `main` into that existing PR branch and publishes its
reviewed correction. It does not authorize merging the PR, release or deployment.

## Problem and bounded outcome

The two branches changed the same validators, compiler outputs, workflows, tests
and current instruction pointers while PR #18 moved their physical locations.
A read-only merge-tree inspection reports content conflicts and new-file location
ambiguities; in particular, Git guesses that new prerequisite plans belong in an
unrelated Codex delivery. Resolve these mappings explicitly, preserving both the
new copyable structure and the trusted dual-layout behavior from merged `main`.

The separate triage has reproduced INT-ARCHIVE-01, the Codex P1 from PR #19
(`discussion_r4325322772`): the actual merged-main validator accepts deletion of
`docs/changes/backbone-bootstrap/plans/bootstrap-task.json` because archive hashes
are checked only for files returned by the walk. Include the narrowly confirmed
archive-completeness repair and meaningful negative coverage. The executing
validator owns the required archive set; candidate maps cannot weaken it.

The requested Codex review of PR #18 at `f1c1410...` was running when this plan was
prepared. Read its actual result before publication. Triage any findings before
repair, and distinguish that prior-head review from the new integration review.

### Codex follow-up addendum

The prior-head review subsequently returned three reports. Its archive-deletion
report (`discussion_r4325511332`) duplicates confirmed INT-ARCHIVE-01. The following
two reports are independently confirmed and included in this amended plan:

- **INT-ARCHIVE-02**, P1 (`discussion_r4325511354`): `.gitattributes` protects
  tooling LF bytes but omits the byte-hashed records under `docs/changes/`.
  A fresh checkout with `core.autocrlf=true` can rewrite those records to CRLF and
  make clean source validation fail. Independent triage reproduced 88 archive-hash
  errors on a fresh exact-`f1c1410...` checkout, while nested historical-fixture text
  bytes stayed unchanged. Add a narrowly scoped LF
  attribute for these archived text records and a real fresh Git checkout
  regression in `test_reference_layout.py`. Verify the same archived hashes and
  validator result after checkout; preserve nested historical-fixture attributes
  and all committed historical bytes. Do not rewrite history to accept CRLF hashes.
- **INT-NAV-01**, P2 (`discussion_r4325511366`): active root instructions still
  point at the earlier BB-LAYOUT-011 task. Triage confirmed stale active pointers
  in AGENTS, CONTRIBUTING and the change index. The current-pointer work below
  already covers correcting this to BB-LAYOUT-014 in the active instructions and
  applicable README navigation. Historical records retain their original pointers.

The `.gitattributes` repair is additional scoped implementation limited to the
confirmed finding. The amended plan requires independent review before GO.
Retain the separate triage, actual before/after evidence and dispositions in the
frozen review context; do not treat an implemented proposal as completed checking.

## Integration and file ownership

1. Verify a clean worktree, the live PR head, and actual `main`; preserve unrelated
   changes. Start a normal merge of `537576f...` into the PR branch. Keep both
   parents in the resulting merge commit and never rewrite published history.
2. Runtime implementer reconciles the reviewed helper at
   `.engineering-backbone/src/source_layout.py`, the validator, navigation and
   quality guards, and the navigation compiler at its `maintenance/` path.
   Preserve source-versus-consumer identity owned by the executing code, separate
   candidate/base resolution, complete canonical policy requirements, symlink and
   mixed-layout rejection, trusted schemas, permission floors, and legacy paths.
   Retarget maintenance inputs/outputs without changing the meaning of the old
   source contract. Do not import candidate code or manufacture an old-path view.
3. Repair INT-ARCHIVE-01 after the separate triage record is retained. Compare the
   complete executable-owned required history set with actual candidate files in
   new-source mode before per-file checks. Absent files, an absent archive parent,
   and linked replacements must not disappear from validation. Preserve old-source
   and consumer behavior; do not redefine historical authority from candidate data.
4. Test implementer reconciles the seven existing suites changed on `main`, moves
   its new transition suite and three fixture files into `.engineering-backbone/tst`,
   and adapts current checkout/compiler paths. Preserve all prior assertions,
   exact snapshot provenance, both frozen ZIP bytes, their original manifest, and
   original fixture bytes. Add an exact deterministic merged-main snapshot ZIP and
   separate manifest with commit/tree/mode/blob/hash verification before extraction
   or execution. Preserve the existing old-source prerequisite acceptance test
   using this verified old-layout main snapshot; add actual-main validator to
   integrated-candidate coverage without manufacturing an old-path projection.
   Do not remove the new-source `.engineering-backbone/core.json` while clearing
   stale consumer markers in test fixture setup. The added prerequisite records
   do not become global archive obligations for earlier frozen candidate trees.
   Retain PR #18's Copilot nested-document regression and its real `git+file://`
   Copier upgrade repair. Add observable archive-deletion rejection and intact
   archive positive coverage, including rejection when the candidate map is forged.
5. Root coordinator relocates the prerequisite's eleven plan/review records with
   identical bytes and records their exact old/new paths and Git blob identities:

   | Main path | New location |
   | --- | --- |
   | `plans/layout-compatibility*` | `docs/changes/backbone-layout-compatibility/plans/` |
   | `docs/reviews/layout-compatibility-*` | `docs/changes/backbone-layout-compatibility/docs/reviews/` |

   Keeping this original internal topology preserves same-directory and
   `../../plans` Markdown links. These records receive ordinary link/schema checks
   from actual `main`; no candidate-only historical exception is introduced.
   Explain the nested preserved `docs/reviews` directory in the change index.
   Do not edit the existing 495-entry original crosswalk or its archived bytes;
   add a separate integration inventory for newly introduced prerequisite files.
6. Root coordinator updates active task pointers and the now-obsolete migration
   blocker prose in `AGENTS.md`, `CONTRIBUTING.md` and the change index. Existing
   historical reports retain their snapshot-specific claims. The README may receive
   only an accurate pointer to the completed integration and new record inventory.
7. Regenerate maintained compiled outputs through their canonical compilers,
   including source workflow guard/fingerprint sections. Preserve workflow events,
   permissions, job gates, pinned actions, the actual trusted-base execution path,
   dependency inputs and committed-whitespace check. Retain only measured,
   previously reviewed bundle identities required for compatibility; no arbitrary
   intermediate candidate fingerprint is approved. The actual merged-main current
   digest `a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`
   may become an approved previous identity; preserve the previously approved list.

No product code, scaffold redesign, dependency version change, policy/schema
weakening, native permission change, repository setting or external-repository
change belongs to this task. `main` remains the actual trusted base; its validator's
known archive-deletion blind spot is retained in the defect evidence and is not
misrepresented as independently verifying the new repair.

## Verification and acceptance

| ID | Required result | Evidence |
| --- | --- | --- |
| AC-1 | Conflict-free merge preserves the PR starting head and actual merged main as ancestry; every incoming file has an explicit destination. | Parent identities, merge/conflict inventory, no unmerged entries, blob-based relocation audit. |
| AC-2 | The new physical layout preserves dual-layout trust, stricter policies, native permissions and source/consumer separation. | Source-layout positives/negatives, candidate validator, actual main validator against the exact candidate and main checkout. |
| AC-3 | INT-ARCHIVE-01 is reproduced before repair and absent/malformed required history is rejected afterward. | Separate triage, before/after CLI results, regression assertions independent of candidate map data; intact history accepted. |
| AC-4 | Both branches' reviewed behavior and immutable inputs are preserved. | Complete suite, prior test/assertion audit, immutable ZIP/fixture and historical blob checks, real Copier updates and Copilot selector checks. |
| AC-5 | Compilers, dependencies, workflows, links and full committed diffs pass at the final snapshot. | All four compiler checks, source dependencies, Actionlint, actual commands/exit codes and final base/head/digest. |
| AC-6 | Independent review chain has no unresolved confirmed in-scope blockers. | Plan review; independent quality; frozen behavior and security Full reviews; separate triage and any required Delta. |
| AC-7 | Existing PR #18 is updated without force push and its exact current remote state is reported. | Remote parent/tree/patch readback, conflict status, all current-head CI jobs, visible requested Codex review, accurate outstanding findings. |
| AC-8 | Confirmed INT-ARCHIVE-02 and INT-NAV-01 are resolved without altering historical bytes or nested fixture attributes. | Real fresh `core.autocrlf=true` Git checkout preserves archive hashes and validates; active pointers consistently name BB-LAYOUT-014; separate triage dispositions. |

Use the unchanged hash-locked Python 3.12 environment. Targeted checks precede the
complete `python -m unittest discover -s .engineering-backbone/tst -t
.engineering-backbone -v` suite. Run all declared compiler checks, source dependency
checks, candidate validation, and actual merged-main `scripts/validate.py` with
`--root` pointing at the candidate and `--trusted-base` at that immutable main
checkout. A candidate validator is additional evidence, never a replacement.

Run `git diff --check` and committed diffs from both `537576f...` and `f1c1410...`
to the final candidate after the last code or evidence commit. Record full SHA
identities and exact exit codes. Stage the new tracked inputs before dependency
checks, without treating staging as evidence. Preserve failed logs and diagnose
their concrete causes before repairs; do not retry unchanged failures for green.

Local missing Docker/native hosts remain explicit limitations. Actual current-head
remote container and Windows/Linux jobs establish that evidence when they finish;
prior PR18/PR19 runs do not qualify this changed tree. No model qualification or OS
isolation follows from structural checks.

## Review chain, budgets and publication

The root agent coordinates separate planner, runtime/test implementers, quality
checker, independent plan reviewer, independent behavior and security reviewers,
and triage sessions. Plan review precedes non-trivial implementation. All Full
reviewers receive the same frozen base/head/tree and binary patch SHA256, relevant
instructions, task contract, completed check evidence and confirmed defect IDs.
They report actual coverage and limitations without self-approval. At most two
Full rounds and six implementation iterations apply to this scoped delivery.

Triage confirms, rejects or escalates each finding before repairs. Delta reviews
bind the prior reviewed head and repaired head and cover confirmed IDs plus direct
regressions. New scope/trust boundaries require updated independent plan/Full
review. Unresolved blockers or exhausted budgets stop publication readiness.

Before publication re-read live branch/main identities. If either moved, inspect
the new change instead of overwriting it or claiming the old base remains current.
Publish the exact reviewed tree to the existing branch with an expected-head lease
and no force push. Verify published parent ancestry, tree and binary patch. Update
the PR body to actual merged-base and current-head status; request/observe the
authorized Codex review with immutable context. Preserve existing remote findings
and separately report what is fixed, pending, failed or outside coverage. Human
review and merge remain separate. Recovery is a reviewed follow-up change or
revert, never destructive cleanup of the existing published history.
