# Independent authority, security and compatibility Full-1

Reviewer `starter_authority_full`; separate read-only session. Two confirmed
findings for independent triage; no tracked edits, repairs or publication.

| Subject | Identity |
| --- | --- |
| Base | `4e74c7e5f3a07430768f670c4271c1e1a0e28f68` |
| Head | `f0230d0da90b17ef52932ff027529acd23d73f51` |
| Tree | `ff9d9c860682c3ed8531a9b085f9ee75678c725d` |
| Binary patch SHA-256 | `ba6eeafe17d91ca46c3b8b695e7e18f4372703d1419712b4d6c9654b865e7f34` |

## Findings

**START-AUTH-01 — P2, high confidence, source/project overlap checked too late.**
`starter.py:491–499` invokes `old_plan()` (descriptor subprocess at 467–470) before
rejecting an old trusted checkout inside the target project. TEMP proof exported
a genuine project, created committed `project/vendor/old-source` with a descriptor
that wrote a marker and returned `{}`, and passed its exact full Git ref. Comparison
rejected `trusted source checkouts must be outside the project`, but the marker
already existed. Thus disallowed project-contained code executed before rejection.
The caller must explicitly select that repository/ref: this is not automatic
execution from ordinary project metadata with correct outside trusted sources.
Minimal repair: normalize and reject all source/project overlap before descriptor
launch; prove a nested source produces no marker and normal distinct sources still
compare. New comparison path; START-03/04, AC3/4/6.

**START-AUTH-02 — P2, high confidence, Windows junction/physical containment.**
New `environment.py:148–154,171–173` and `starter.py:102–129,281–300` use lexical
containment and `is_symlink`, missing distinct Windows directory junction aliases.
An input lexically under root can resolve outside; env reads and starter reads/
writes can traverse that alias. Python 3.12 official docs distinguish
[is_junction](https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.is_junction),
describe [is_relative_to](https://docs.python.org/3.12/library/pathlib.html#pathlib.PurePath.is_relative_to)
as string based, and document junction resolution in
[realpath](https://docs.python.org/3.12/library/os.path.html#os.path.realpath).
Local Python implementation inspection corroborated separate reparse-tag handling.

TEMP Linux probes modeled these semantics by suppressing `is_symlink` only for
one directory alias. Export wrote through it; safe-file accepted a lexical path
whose resolved file lay outside root; env input was similarly accepted. **This is
documented-semantics simulation, not native NTFS execution.** Minimal repair:
reject directory-junction aliases in roots/ancestors and enforce resolved containment
before reads/writes; add modeled and conditional native regressions. No race-free
OS sandbox is demanded. New helper boundary; START-01/03, AC1/3/6.

Auxiliary NUL-comment reproduction corroborates BEH01; no duplicate authority ID.
The schema-only versus trusted cross-field-floor probe belongs to BEH02.

## Coverage and actual evidence

Read role packet, AGENTS/core/CONTRIBUTING, complete plan/task packet, plan review,
implementation and check triage. Inspected complete new starter executable, seven
neutral seeds, integration tests, root/adoption/project guide and lifecycle kit.
Bounded read-only auxiliary coverage inspected env/doctor implementations/tests,
configuration, source-CI runbook and inactive local example.

Coverage included Git ref/blob/script attestation; exact managed bytes; compiled
Git helpers and poison-cache regression; provenance non-authority; core/provider
floor and optional refusal; source/legacy preservation; product JSON independence;
secret/destination/path exclusions; read-only ownership/conflict/removal; environment
precedence/redaction/access claims; fixed doctor argv/timeouts/suppression and actual
prerequisite-versus-fleet limits. No additional confirmed findings from this scope.

Actual checks: `git status --short --untracked-files=no`, `git rev-parse HEAD
HEAD^{tree}`, `git diff --check BASE HEAD` (exit 0), binary diff SHA256 and protected
path `git diff --exit-code` using the exact quality argument list (exit 0), read-only
source inspection and bounded TEMP probes. Final identity/patch/worktree matched.
All sixteen quality-log hashes independently matched; eleven quick gates exit 0;
full 521-test log: zero errors/failures/skips, exit 0, 683.786 seconds unittest /
684.566 wrapper; SHA-256
`c9d075b39e8255a9a5454880f6fc3ca1d155d22d7f78a889993d3e4bbf051d41`.
No broad suite rerun. Existing protected engines/schema/catalog/history/dependency/
workflow files remain unchanged.

Limits: no native Windows execution, Docker image, live-provider qualification,
runner fleet/registration/isolation or remote CI. Queued jobs establish no PASS.
Later reports are outside this frozen Full. Agent advice is not human merge,
release or deployment approval; confirmed findings need triage and scoped Delta.
