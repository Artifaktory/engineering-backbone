# Full-1 triage and authorized repair

Both required Full reviews finished on the same immutable subject:
base `4e74c7e5f3a07430768f670c4271c1e1a0e28f68`,
head `f0230d0da90b17ef52932ff027529acd23d73f51`,
tree `ff9d9c860682c3ed8531a9b085f9ee75678c725d`, binary patch SHA256
`ba6eeafe17d91ca46c3b8b695e7e18f4372703d1419712b4d6c9654b865e7f34`.
See [behavior](behavior-review.md), [authority](authority-review.md) and the
original [independent checks](checks.md). Those checks qualify that head only.

Separate read-only agent `starter_check_triage` independently confirmed identity,
clean tracked state and all five findings after both Full reports were final.
Canonical IDs below retain their original spelling; the triage message omitted
the final hyphen in its shorthand IDs. Auxiliary NUL/junction findings are
corroborations of these IDs, not additional findings.

| ID | Severity / disposition | Authorized minimal repair and regression |
| --- | --- | --- |
| START-AUTH-01 | P2, confirmed | Reject project/source overlap before executing any OLD descriptor. A real nested Git descriptor must be refused without its marker executing; distinct trusted OLD/NEW sources still compare. |
| START-AUTH-02 | P2, confirmed | Reject directory junctions at roots/ancestors and enforce resolved containment before environment/starter reads and writes. Preserve ordinary paths; test modeled semantics and conditional native Windows cases. |
| START-BEH-01 | P3, confirmed | Reject NUL before skipping blank/comment lines, without disclosing input lines or values; normal comments still pass. |
| START-BEH-02 | P2, confirmed | Reuse existing trusted `RepositoryValidator.validate_data` cross-field floors with Git-owned schemas, without full source/history validation or new rules. Reject self-review and duplicate reviewer, finding, Task Packet acceptance and requirement acceptance IDs; retain valid controls and generic errors. |
| START-BEH-03 | P2, confirmed | Inspect governed directory entries recursively without following links; reject nested and dangling links/junctions before JSON selection. Ordinary nested records remain validated and product JSON remains independent. |

The triager reproduced AUTH-01/02, BEH-01 and self-review with bounded temporary
probes (0.635 seconds combined); separately reproduced BEH-03 and the four
duplicate-ID cases. No implementation edits or broad suite rerun were performed
by triage. AUTH-02 and BEH-03 can share a path helper but have distinct causes:
alias/containment versus skipped traversal. Junction evidence is an API-backed
Linux simulation, not a native Windows result. No OS race-free sandbox is required.

One bounded second implementation iteration is authorized for these five IDs.
The export author owns `starter.py` and its tests; the environment author owns
`environment.py` and its tests. No schema, catalog, original validator, source
workflow, historical evidence or unrelated requirement changes are authorized.
New failures require separate triage before further repair.

After focused regressions, freeze a new committed subject. Independent checks
must rerun all required gates and the complete suite. Both reviewers then perform
Delta reviews bound to the Full head, repair head and binary patch digest,
covering these IDs and direct regressions. Separate final triage records closure.
No second Full is needed for this scope. Original 521 PASS and eleven quick gates
remain preserved; they are not evidence for later code changes. Native Windows,
Docker, actual runner fleet and remote CI remain unqualified external gates.

This is agent triage and repair authorization within the user-approved PR scope,
not human merge, release, deployment or runner-administration approval.
