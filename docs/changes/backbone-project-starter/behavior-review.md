# Independent behavior and traceability Full-1

Reviewer `starter_behavior_full`; read-only, separate from all authors/checker.
Three confirmed findings, for independent triage; no edits or repairs.

| Subject | Identity |
| --- | --- |
| Base | `4e74c7e5f3a07430768f670c4271c1e1a0e28f68` |
| Head | `f0230d0da90b17ef52932ff027529acd23d73f51` |
| Tree | `ff9d9c860682c3ed8531a9b085f9ee75678c725d` |
| Binary patch SHA-256 | `ba6eeafe17d91ca46c3b8b695e7e18f4372703d1419712b4d6c9654b865e7f34` |

## Findings

**START-BEH-01 — P3, high confidence, literal-file grammar.**
`environment.py:107–111` skips comment lines before checking NUL, while the new
configuration guide says NUL fails. Auxiliary actual TEMP CLI proof with empty
valid register and explicit bytes `b'# ignored\x00comment\n'` returned exit 0/PASS.
No leakage/execution demonstrated. Minimal repair: reject NUL before comment/blank
handling and add a comment-line regression. Introduced in the new parser; AC1/6.

**START-BEH-02 — P2, high confidence, deterministic record independence.**
`starter.py:359–363`, called at 431, only applies JSON Schema. It omits trusted
`RepositoryValidator.validate_data()` cross-field checks in unchanged
`validate.py:4317–4337`: implementer/reviewer separation, reviewer/finding identity
uniqueness and acceptance-ID uniqueness. In a real TEMP export, a copied valid
review-evidence example with `implementer = reviewers[0].id` passed seed verify,
returning 166 managed files. The same data through the trusted existing method
produced `implementer cannot be their own independent reviewer`.
This is a mechanically checkable identity floor, not authenticated human approval
or a request to run the full source/history engine. The seed retains independent
review as a core invariant. Minimal repair: apply equivalent trusted deterministic
checks in the bounded seed route; regress self-review and duplicate IDs with a
valid independent positive record. New seed omission; START-03/AC3/6.

**START-BEH-03 — P2, high confidence, governed directory traversal.**
`starter.py:413–419` checks only each explicit root for a symlink and then uses
`rglob`. A fresh TEMP export with `docs/changes/linked` pointing to a sibling
directory containing malformed `task-packet.json` (`{"scope": {}}`) passed verify,
returning 166. Recursive glob skipped that linked directory, so safe-file validation
never saw the record. No outside read/execution observed. This violates the new
plan's fail-closed alias rule. Minimal repair: explicitly reject every linked
governance subdirectory, including dangling links, before descent without following
them; retain ordinary nested-record validation. Distinct from Windows junction
recognition in AUTH02. START-03/AC3/6; own native Linux TEMP proof.

## Coverage and actual evidence

Read all supplied instructions/plan/packet/review/implementation/triage context and
the complete relevant patch. Covered all five foundations: env metadata/grammar/
contexts/redaction/access claims; Git-bound export and neutral identities; omission
of history/workflows/secrets; managed/project ownership; schema/native/helper trust;
source/legacy/optional-contract refusal; link closure; read-only comparison and
ownership/removal/conflict/provenance; development command map and actual CI limits;
all lifecycle templates/source hints; root/adoption/config/scripts integration;
meaningful positive/negative tests and prior CHECK01/02/03 repairs. Preserved source
and legacy engines, schema/catalog/workflows/native/dependency/history were checked.
No additional confirmed findings; no broad test-suite rerun.

Actual commands: `git rev-parse HEAD HEAD^{tree}`, `git status --short`, binary diff
with SHA256, `git diff --check BASE HEAD` (exit 0); read-only `git diff`, `cat`,
`sed`, `nl`, `rg`; Python `-I -B` TEMP exports/negative probes, automatically cleaned.
Identity/patch and clean frozen worktree matched. All sixteen indexed quality logs
were independently hash-checked: no mismatch. Eleven quick gates exit 0; full log
records 521 tests, zero failures/errors/skips, exit 0, 683.786 seconds; SHA-256
`c9d075b39e8255a9a5454880f6fc3ca1d155d22d7f78a889993d3e4bbf051d41`.
The passing suite did not cover the new confirmed cases; it is not defect absence.

Limits: no native Windows, Docker image/daemon, fleet/registration, remote CI,
live host/provider or full-text standards audit. Source-linux doctor's missing
Docker exit 1 remains explicit; development exit 0 is only prerequisite evidence.
Later reports are outside this Full subject. Agent advice, not human merge/release/
deployment approval. Findings require triage before repair and scoped Delta.
