# BB-LAYOUT-012: bounded CI clone repair addendum

This addendum addresses the user's still-red Foundation check within the existing
Copilot test scope. It grants no merge, runtime, dependency, workflow or template
change. Current published head: `2ddfa803688c70b556dc83bcf07a4c3911713be5`.
The original corrective baseline and previously recorded evidence remain intact.

## Observed failure

Foundation run `39422351687`, jobs `118626214062` and the single diagnostic rerun
`118631415944`, each ran 433 tests and failed one existing historical Copilot
upgrade subtest. Git exited 128 while copying a loose object during a local clone
from the test's temporary source. The new selector regression passed. The exact
underlying filesystem/Git cause is unproven; Git 2.55.0 is the observed CI version,
not proof of a particular upstream defect. The failing method is unchanged by the
selector correction and passes locally with Git 2.51.1. The repeated remote
failure now requires a bounded fixture repair, not further unchanged retries.

## Proposed repair and retained contract

After independent triage confirms the installed Copier behavior, use the explicit
`git+file://` URL formed from the committed fixture source's resolved URI for the
initial historical `run_copy`. Copier records that source for subsequent real
`run_update` calls, selecting Git's transport instead of its local object-copy
optimization. Both pinned tags and all actual upgrade, local-policy preservation,
installation-only rejection and validation assertions remain. No hand-edited
answers file, retry loop, skipped assertion, catch-and-pass, dependency pin change
or global Git configuration is allowed. Plain `file://` is insufficient for the
installed Copier's Git-source discovery and must not be substituted blindly.

The only substantive file is
`.engineering-backbone/tst/test_copilot_distribution.py`. Supporting evidence and
current Task Packet acceptance updates stay in this corrective directory. No
legacy template, source validator, schema, native instruction or workflow change.

## Checks, review and publication

1. Independent triage records both actual failures and verifies the proposed URL
   with a real tagged Copier copy/update before implementation. Independent plan
   review precedes the repair.
2. Apply the smallest source-URL change with a short purpose comment. Preserve
   every existing assertion. Use Git trace evidence from a real targeted run to
   confirm transport selection; the actual upgrade/rejection assertions remain
   the behavior evidence.
3. A separate quality checker reruns the affected 41 Copilot tests, structural,
   compiler and dependency checks plus committed patch whitespace checks. No
   claim that local Git reproduces the hosted Git version.
4. Freeze the corrected commit/tree/binary patch. An independent bounded second
   Full review covers this newly diagnosed repair and direct regressions against
   the current published head. Triage before further repairs. The overall task's
   two-Full/six-iteration budget remains; original first Full evidence is retained.
5. Publish only to existing draft PR18. After the final evidence commit, check
   both original full-PR and corrective committed diffs, verify remote tree/patch
   correspondence and observe a new full remote Foundation run. Preserve the two
   failed attempts in the PR description; do not call prior-head tests current.

This addendum changes no actual main authority. The independent BB-LAYOUT-013
prerequisite and its human-merge-then-integrate ordering remain necessary for
PR18's separate trusted-base check.
