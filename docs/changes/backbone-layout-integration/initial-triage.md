# BB-LAYOUT-014 initial independent triage

Role: independent triage, read-only against repository source. No runtime, tests or task records were changed. Reproduction copies were extracted directly from immutable Git commits into temporary directories and removed on completion. This is triage evidence, not implementation or merge approval.

## INT-ARCHIVE-01 — confirmed, P1, high confidence

Source: Codex PR19 review discussion `4325322772`, reviewed `fc707a8d51981d52445c2176711154dfd26145aa`; now merged as actual main `537576f658bbd79c3bc49b26ade948116c664943`. Candidate PR18 `f1c1410cff6407109f286173f1ecc980cd2a14b7`.

Contract: reviewed historical records must remain byte-preserved in the new source layout. Executing-validator-owned `HISTORICAL_FILES` is the authority, not candidate mappings.

Execution: `RepositoryValidator.run()` walks existing files and calls `historical_bytes(path)` only inside that walk. An absent archive entry is never visited. Deleting `docs/changes/backbone-bootstrap/plans/bootstrap-task.json` therefore produces neither a hash error nor an inbound-link error. The actual trusted validator accepts the candidate after loss of reviewed history.

Reproduction commands:

```sh
/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /tmp/backbone-integration-triage.py
/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /tmp/backbone-integration-pr18-history-probe.py
```

Each script uses `git archive` at the pinned revisions; actual validator command is `python -I -B EXECUTING_VALIDATOR --root CANDIDATE --trusted-base FROZEN_BASE`.

| Executing validator | Candidate | Trusted base | Result |
| --- | --- | --- | --- |
| actual main 537576f `scripts/validate.py` | pristine PR18 f1c1410 | actual main 537576f | exit 0, structural PASS |
| actual main 537576f `scripts/validate.py` | PR18 with unlinked historical task removed | actual main 537576f | exit 0, structural PASS: defect reproduced |
| frozen PR18 f1c1410 moved validator | pristine PR18 f1c1410 | pristine PR18 f1c1410 | exit 0, structural PASS |
| frozen PR18 f1c1410 moved validator | PR18 with unlinked historical task removed | pristine PR18 f1c1410 | exit 0, structural PASS: same defect reproduced |

Running the pre-integration PR18 validator against old-layout actual main yields four existing compatibility errors both before and after deletion; those are not evidence that historical deletion was rejected. The new-to-new reproduction isolates its same missing-file defect.

Raw outcomes: `/tmp/backbone-integration-triage-results.json` and `/tmp/backbone-integration-pr18-history-results.json`.

Minimal repair: for new-layout source candidates, require every executing-validator-owned historical path independently of current walk results. Reject missing, non-regular or alias paths before the ordinary per-file hash checks. A set comparison against safely walked regular files naturally detects missing files and symlinked directory omissions; a direct check must also guard ancestors. Preserve the existing byte hashes and candidate-map non-authority. No new history exemption, schema relaxation or consumer requirement.

Meaningful regressions: complete archive succeeds; unlinked archive-file deletion fails; containing archive-directory deletion fails; candidate-map changes cannot authorize either omission; existing changed-byte rejection remains. Cover a symlinked ancestor if the chosen mechanism would otherwise follow it. Keep old-layout and consumer behavior unaffected.

## Merge conflict inventory

Read-only `git merge-tree --write-tree f1c1410cff6407109f286173f1ecc980cd2a14b7 537576f658bbd79c3bc49b26ade948116c664943` exits 1 and reports conflicts in moved runtime/compiler files, four moved test modules, workflow, root AGENTS/CONTRIBUTING, and locations of new compatibility fixture/test/plan files. It suggests `plans/layout-compatibility*` under `docs/changes/backbone-codex-consolidation/plans/`, which is semantically wrong and must not be accepted mechanically. `docs/reviews` has a split rename; choose the new compatibility delivery's explicit history location. Preserve original evidence bytes unless explicitly recorded as current operational navigation. New `scripts/source_layout.py` needs the intended new tooling source path and compiler references.

Integration constraint from independent test assessment: the existing exact c501 snapshot must remain accepted against frozen212608, and its fixture bytes must remain unchanged. If the integration introduces additional historical records from PR19, their required-presence obligations must be tied to the relevant trusted history or explicit transition, not imposed globally on all older snapshots. This must not weaken the existing 88-entry archive deletion rejection. A separately pinned exact537576 fixture can preserve the old-main-to-bridge test and support current integration coverage.

## INT-ARCHIVE-02 — confirmed, P1, high confidence

Source: Codex PR18 discussion `4325511354`, reviewed exact head `f1c1410cff6407109f286173f1ecc980cd2a14b7`.

The root attributes pin source tooling, schemas and dependency files to LF but omit the archived text under `docs/changes/`. A clean checkout with `core.autocrlf=true` converts all 88 hashed archive entries to CRLF; the validator then rejects its pristine source tree. This makes normal Windows checkouts fail and defeats byte-preserved archive claims.

Actual reproduction:

```sh
/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /tmp/backbone-integration-crlf-triage.py
```

The script performs `git -c core.autocrlf=true clone --no-local --no-checkout SOURCE TEMP`, then `git -C TEMP -c core.autocrlf=true checkout --detach f1c1410cff6407109f286173f1ecc980cd2a14b7` (both exit 0), and runs the checked-out validator via Python `-I -B --root TEMP` (exit 1, exactly 88 historical-byte errors). No global Git configuration was changed. The absence of trusted-base comparison is explicitly reported and does not affect this checkout-byte reproduction.

Observed bytes: bootstrap archived task contains 35 CRLFs, archived result 60 CRLFs. Canonical validator remains LF (0 CRLFs), and immutable historical bootstrap fixture core remains LF (0 CRLFs). `git check-attr` reports archive text/eol/filter/encoding unspecified, source text set/eol lf/filter unset/encoding unset, and historical fixture text/filter/encoding unset under its existing nested `.gitattributes`.

Raw outcomes: `/tmp/backbone-integration-crlf-triage-results.json`.

Minimal repair: add an appropriately scoped root attribute such as `docs/changes/** text eol=lf -filter -working-tree-encoding`. Keep `.engineering-backbone/tst/fixtures/historical/.gitattributes` byte-identical; its `* -text -filter -working-tree-encoding` contract protects immutable fixture Git blobs. Do not normalize fixture files or change their expected hashes.

Meaningful regression: create a fresh isolated local clone/checkout with `core.autocrlf=true`, assert actual archive hashes equal the committed/owned authority and source validation succeeds, and assert all preserved historical fixture bytes/attributes remain unchanged. A text-only assertion that the attribute line exists would not reproduce the failure.

## INT-NAV-01 — confirmed, P2, high confidence

Source: Codex PR18 discussion `4325511366`, reviewed exact head `f1c1410cff6407109f286173f1ecc980cd2a14b7`.

At that head, `AGENTS.md` lines 3–7, `CONTRIBUTING.md` opening and `docs/changes/README.md` active-delivery paragraph point to BB-LAYOUT-011. The linked task packet has `status: completed`, while the latest correction packet is BB-LAYOUT-012 and points to the actual clone-repair review snapshot. Agents following mandatory current-task navigation therefore load a completed scope rather than the active correction, obscuring current authorization, exclusions and remaining checks.

Confirmed by reading those exact Git paths (working tree still at f1, plus `git show f1:...` for packet state). This is an operational navigation defect, not a request to rewrite historical records.

Minimal integration repair: update current entrypoints to the new independently reviewed BB-LAYOUT-014 task/plan, while retaining links to BB-LAYOUT-011/012/013 as explicitly historical or prerequisite context. Keep historical packet bytes unchanged. Verify linked paths exist and the current packet ID matches the integration delivery. Update statements claiming that main still lacks the bridge now that actual main537576 contains it; distinguish that from newly observed current-head checks.

The duplicate archived-deletion finding from PR18 discussion `4325511332` is covered by confirmed INT-ARCHIVE-01; it does not require a second independent repair.

## INT-CHECK-01 — confirmed task-metadata error, corrected before freeze

The first targeted integration run (`/tmp/backbone-integration-targeted-tests.log`) executed 83 tests in 102.241 s: 82 passed and one failed. The failing test was `ReferenceCheckoutTests.test_fresh_autocrlf_checkout_preserves_archives_and_nested_fixture_contract`; its final real source-validator assertion returned one schema error:

```text
docs/changes/backbone-layout-integration/task-packet.json: status: 'in_progress' is not one of ['planned', 'active', 'blocked', 'ready_for_review', 'completed']
FAIL: 1 structural validation error(s).
```

This is a real rejected invalid task status, not an archive-byte or attribute failure. Inspection of the test confirms that its 88 archive-hash/LF checks, nested historical-fixture byte comparisons, and effective attribute checks precede the failing final validator assertion. The log contains no additional failures. The checkout test copies the live tree into its temporary seed; that copied tree retained the transient invalid metadata even after the root owner corrected the working tree.

The root owner reports observing and correcting this metadata error immediately, before the test agent's failure report. Independent triage now read the current task packet: `status: active`. A direct `Draft202012Validator` check against the unchanged `.engineering-backbone/schemas/task-packet.schema.json` returned `SCHEMA_ERROR_COUNT 0`, exit 0. This establishes the current metadata correction; it does not retroactively turn the first failed run green.

Disposition: confirmed INT-CHECK-01, corrected in task metadata; no runtime, test, fixture, schema, assertion or timeout change justified. One focused rerun of the affected checkout test is justified because its actual copied input changed from invalid `in_progress` to valid `active`. Preserve the initial failed run and report the focused rerun separately. Freeze the candidate before independent quality checks and formal reviews to avoid live metadata changes during snapshotting. The planned frozen full-suite check remains required and is not a retry of unchanged failed input.
