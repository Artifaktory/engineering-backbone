# BB-LAYOUT-012 corrective closeout

The source Copilot docs selector now covers nested Markdown while retaining root
Markdown and docs data. All 24 native Copilot files were audited; their native
locations remain required. The root `copier.yml` is the legacy Copier entrypoint
and already targets the relocated template. It is not a Copilot configuration.

The extra EOF blank line that failed Foundation CI is removed. Contributor
instructions now require both committed corrective and whole-PR diff checks after
the last evidence commit. Working-tree cleanliness alone is insufficient.

Implementation snapshot: `dbe05e14a255488e3416465971ece755fb04aba3`, tree
`1801cbc5defdf82a4c37f5ead84eea2e8ab1df4b`. Corrective base:
`c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`. Full patch SHA256:
`8957f9cea5e698daa212cdbd08c555dbdd6ea0e7222b52c1dea7e19038575ed0`.

| Acceptance | Recorded disposition |
| --- | --- |
| AC-1 selector and retained contracts | PASS: 41 affected tests and independent Full review. |
| AC-2 EOF and final committed checks | Repair and implementation-snapshot checks PASS; final evidence-commit checks remain pending here. |
| AC-3 contributor procedure | PASS: reviewed final-commit requirement. |
| AC-4 checks and independent chain | PASS: [checks](checks.md), [Full](full-review.md), [triage](triage.md); no repair Delta needed. |
| AC-5 honest CI/trust evidence | PASS: [observed prior-head CI](ci-observations.md), with failed trusted-base gate retained. |
| AC-6 publication/readback | Pending at this commit; exact published identities and current checks are recorded in the PR description. |

The final evidence-only commit is outside the frozen implementation snapshot.
Before branch publication, rerun the validator and all final committed diff
checks, then verify remote tree and binary patch correspondence. GitHub-created
commit metadata may differ; equal content trees and patches must be verified.
The PR description records those post-commit results without creating a
self-referential evidence-commit loop.

## Remaining prerequisite

The old-main trusted validator cannot interpret the relocated source layout.
BB-LAYOUT-013 separately prepares a dual-layout trusted validator on the old
layout, with positive transitions, rejection tests and independent reviews.
Only a human merge of that prerequisite can change the actual trusted main.
Afterward, integrate actual main into PR18, reconcile moved files, and rerun its
checks. This correction does not make that failed gate green or authorize merge.

No native Copilot/model qualification is claimed. The current correction was
checked with 41 affected tests; the prior full 432-test/container/native results
belong only to their recorded old head. Current-head remote results are required.
Recovery remains a normal reviewed corrective commit. No force push, merge,
release, repository-setting change or downstream application was performed.
