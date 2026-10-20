# First direct-copy reference-layout refactor

Status: proposed for independent read-only plan review. This plan is not execution
or review evidence. The human requested a first refactoring PR on 2026-10-20 so the
structure can be inspected and improved incrementally.

Base: `212608aa50ee517b3dd3107a9480da997222fd4f` on `main` in
`Artifaktory/engineering-backbone`. Task: [BB-LAYOUT-011](task-packet.json).
The root agent coordinates separate planner, implementation, quality-checker,
independent review and triage sessions. The complete file inventory is
[layout-map.json](layout-map.json), explained in [mapping.md](mapping.md).

## Outcome and boundary

The Backbone repository itself becomes the reference directory layout. A new
project can copy the actual files to their final paths without running a generator.
The existing canonical governance, documentation, validators, schemas, tests,
native adapters and tooling remain represented. This PR does not build an example
product, port product code, introduce a second editable policy, remove established
negative checks, activate integrations or promise that copying config completes
project adoption.

The first PR will be a **draft with a visible blocked legacy trusted-base gate**.
The previous validator expects the previous source paths. Running it against the
new layout must report that real incompatibility. The PR will not replace that
failure with a candidate validator or a path projection and call the result
trusted. A later explicitly reviewed adoption of the new trusted layout is needed
before merge readiness can be claimed. The new candidate checks and legacy
consumer compatibility suite must still pass; the draft label is not an excuse to
hide defects in the candidate.

No changes are authorized in Artifaktory, Tars, an upcoming Mastra application or
Agent Orchestrator. No merge, release, deployment, repository-control change,
downstream update or runtime/model qualification is included.

## Reference structure and file ownership

```text
engineering-backbone/
├─ apps/
│  ├─ frontend/{src/,tst/}
│  ├─ backend/{src/,tst/}
│  └─ automation/{src/,tst/}
├─ packages/
├─ contracts/
├─ tst/
├─ infra/docker/engineering-backbone/Dockerfile
├─ config/
├─ scripts/
├─ docs/
│  ├─ agent-governance/
│  │  ├─ core.md
│  │  ├─ adapters/
│  │  └─ sources/
│  ├─ templates/examples/
│  ├─ requirements/
│  ├─ architecture/
│  ├─ changes/backbone-<delivery>/
│  ├─ quality/
│  └─ operations/engineering/
├─ .engineering-backbone/
│  ├─ src/maintenance/
│  ├─ tst/fixtures/
│  ├─ schemas/
│  ├─ standards/
│  ├─ legacy/templates/
│  ├─ requirements.txt
│  ├─ requirements.lock
│  ├─ core.json
│  ├─ project.json
│  └─ opencode.json
├─ .github/
├─ .vscode/
├─ .codex/
├─ .opencode/
├─ AGENTS.md
├─ CONTRIBUTING.md
├─ README.md
├─ SECURITY.md
├─ copier.yml
└─ opencode.json
```

Empty product directories receive concise explanatory files, not fabricated code
or manifests. Components keep their real dependency manifests, lock files and
build configuration at the native component root (`apps/frontend/package.json`,
`apps/backend/pyproject.toml`, `apps/automation/package.json`, for example).
Repository-wide workspace files remain at the root only when the adopted build
system needs them. UI belongs in the relevant app's `src/`; component tests use
`tst/`; cross-component tests use root `tst/`. Product packages and contracts are
separate from Backbone tooling. Infrastructure and product configuration belong in
`infra/` and `config/`; tool-specific discovery files retain their native locations.
The tooling dependencies and Dockerfile are explicitly labelled as Backbone's,
not product prerequisites. Generic VS Code settings may be added without machine
paths, automatic commands or unapproved extensions. No technology is selected for
an otherwise empty product component.

## Canonical and legacy paths

1. Apply the 495-file bijective mapping. The central move is coordinated before
   parallel content edits so workers cannot race file renames.
2. The prose authority is `docs/agent-governance/core.md`; invariants are
   `.engineering-backbone/core.json`. No editable old-path duplicate remains.
   Native adapter references and current guides point to those actual paths.
3. Runtime code lives in `.engineering-backbone/src/`; compiler maintenance lives
   in its `maintenance/` directory. Schemas and standards stay adjacent in the
   bundle. Root `scripts/` is reserved for shared/product entry commands.
4. Keep root `copier.yml` exclusively as the legacy discovery entrypoint. Its
   `_subdirectory` points to `.engineering-backbone/legacy/templates`. Existing
   generated consumers retain their historical installed layout and update
   choices. Legacy templates include current canonical source files with updated
   include paths; they do not become a new reference-product generator layer.
   Generated consumer facts, adapter opt-ins and local-policy protection remain.
5. The same validator may distinguish execution from the new `src/` reference
   layout from the historical installed `.engineering-backbone/validate.py`
   consumer layout. Source-only path branches change; consumer paths and trust
   semantics do not. Reject ambiguous modes or missing mandatory files rather
   than guessing a weaker validation mode.
6. Update compiler inputs and output locations together. Preserve compiled native
   permission guards, catalog literals, workflow policy checks and checked
   fingerprints. The legacy rendered bundle fingerprint remains explicit legacy
   compatibility evidence, separate from verification of directly copied files.
7. Keep project schema version 1 and its existing supported fields. Do not add
   unvalidated component/build metadata or change the policy invariant bytes.

## Historical records and navigation

The old plans and reviews move into `docs/changes/backbone-<delivery>/plans/` and
`reviews/` with **identical bytes**. Historical fixtures move only as a containing
directory: internal paths, manifest identities, archived consumers and bytes stay
unchanged. Pinned source-inventory JSON also remains unchanged. The crosswalk
records original Git blob identities and destinations.

Add an archive index that explains the delivery grouping, old-path lookup and
immutable base revision. Historic commands, filenames, authorizations and PASS
claims describe the original delivery; they are never current product evidence.
Do not repair historical prose in place. For checking historic Markdown, resolve
its links in its recorded original path context using the bounded old-to-new
crosswalk, then confirm mapped targets exist; verify archived bytes first. The
archive identity, expected hashes and mapping used for this exception come from
the executing trusted bundle or an equivalently compiled reviewed literal, never
from the candidate-controlled `layout-map.json`. A negative regression must mutate
the candidate map to relabel a current document as historical and alter expected
hashes, and prove that neither action bypasses normal validation or byte checks.
This must not become a broad skip for all `docs/changes/` content. New change records,
new task packets and current evidence continue to receive normal link and schema
validation. Fixture exclusion remains limited to the existing fixture semantics.
Meaningful regression cases must catch a changed historical byte, a missing mapped
file and a broken new task/evidence record.

## Copy/adoption contract

Document and execute a copy of the tracked reference tree into a temporary,
differently named directory, excluding Git metadata, caches, installed dependencies
and run artifacts. Include dotfolders. The copied canonical validator and required
checks run from the copied tree without Jinja rendering or reliance on the source
checkout. A direct-copy check must detect missing required governance files and a
weakened policy/permission mutation; copying a layout alone is not qualification.

The README and adoption guide explicitly list project-owned changes:

- Review `.engineering-backbone/project.json` name, base branch, language, component
  flags and validation command; only supported schema fields are used.
- Replace current Backbone task references and repository-specific operating facts
  in root entrypoints with the new project's reviewed task and commands.
- Decide how to retain or omit Backbone history and maintenance-only legacy assets;
  inherited review records never satisfy the new project's evidence gates.
- Configure project CI and runner permissions separately. Existing source-only CI
  identity restrictions intentionally remain restricted to engineering-backbone;
  copying source CI does not establish downstream CI readiness.
- Preserve native client locations and stricter instructions. OpenCode's inactive
  companion and deny defaults remain inactive; no provider/model or OS-isolation
  claim is inherited. Current native smoke qualification remains distinct.
- Add real component manifests, locks, build configs, Docker definitions and
  environmental examples only when that project's technology is selected. Never
  copy secrets, machine-local IDE settings or a source project's deployment access.

This PR establishes an inspectable base layout and a verified local copy path.
Automatic updates of copied projects and retirement of all legacy templates are
follow-up work, not hidden promises of this refactor.

## Implementation sequence and ownership

1. Planner writes this plan, Task Packet and complete mapping; an independent
   reviewer inspects scope, migration boundaries, tests and stop conditions.
2. Coordinator verifies baseline and records available Python/container tooling.
   An implementer performs the deterministic file moves and mapping validation.
3. After moves, use nonoverlapping implementation scopes: runtime/validators;
   maintenance compilers and CI; active docs/native adapters/reference READMEs;
   test path updates and migration regression cases. Coordinate generated guard
   changes after runtime edits; do not edit frozen historical records.
4. Retarget tests while retaining the existing positive, negative, initial-copy,
   upgrade and historical cases. Add direct-copy and mapping assertions that test
   the changed contract rather than just mirroring the implementation.
5. Regenerate checked compiler outputs, stage required tracked inputs, and have a
   separate quality checker execute the recorded commands and report exit codes.
6. Freeze a committed candidate with base/head and `git diff --binary` SHA256.
   Independent behavior/compatibility and security/governance reviewers inspect
   the same immutable snapshot read-only, state coverage and unreviewed areas.
7. A separate triage session classifies findings before edits. Implementers repair
   confirmed findings only; freeze again and request Delta over those IDs and
   direct regressions. Maximum two Full rounds for unchanged scope; Task Packet
   iteration and stop limits also apply.
8. Publish the explicitly authorized draft PR. Verify remote head/tree and report
   actual CI state, including the intentionally unbypassed legacy trusted-base
   incompatibility and unavailable container/native evidence. Human inspection
   determines later scope; this PR does not claim merge readiness.

## Required verification and acceptance

Use isolated Python 3.12 with `pip install --require-hashes` from the unchanged
moved lock. Run the validator, all four compiler `--check` commands, the tracked
source-dependency check, the full unittest suite and `git diff --check` at their
new paths. Run available workflow syntax checks. Build and smoke the tracked
Dockerfile with repository-root context if Docker is available; otherwise record
the exact unavailable status and leave container compatibility unproven.

Additional contract checks:

- Every baseline blob is accounted for once, destinations are collision-free,
  required moves are present, and all `preserve_bytes` records match base hashes.
- Active references, new task packets and new evidence schema-check at new paths;
  historical links use exact original context and immutable byte verification.
- Local direct-copy checks run from a separate root and preserve negative-policy,
  native-permission and missing-file failures.
- Real Copier initial/update flows retain local project choices and legacy output
  layout, with historical fixture identities verified unchanged.
- Generated guard and fingerprint checks retain their prior rejection coverage.
- Invoke the **actual previous trusted validator** directly against the candidate.
  Record expected path incompatibility distinctly from candidate tests; no
  candidate fallback, catch-and-pass, projection or unconditional suppression.
  CI may select a new validator path only when that file belongs to the trusted
  base itself. Failed required remote gates remain visible and prevent a readiness
  claim, while the requested draft is still publishable for review.

Acceptance IDs and their initial pending states are in the Task Packet. Closeout
links each status to real evidence. AC-6 may be satisfied by the honest recorded
failure and preserved gate; that does not mean the gate passed or the repository
is merge-ready. Any runtime or container test not executed stays unexecuted.
