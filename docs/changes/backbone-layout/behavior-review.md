# Independent behavior and compatibility Full review

Reviewer: `layout_behavior_review`, independent read-only review session.
Bounded test-retention assistance: `layout_behavior_review/layout_retention_audit`.
Round: first Full. Outcome: **changes requested**, pending independent triage of
LBEH-01 through LBEH-03. No implementation changes were made by these reviewers.

## Frozen subject

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Head tree: `09f9a2dacc7943e0e7ce18a97422f801a6f686e2`.
- SHA256 of `git diff --binary BASE HEAD`:
  `3d55fa71f514b9e39f798920188f5186db72b03ef6ea83de576e87f4e8c090bd`.

The head, tree, patch digest and clean frozen worktree were verified before review.
The [Task Packet](task-packet.json), [plan](plan.md), [mapping](mapping.md),
[check record](checks.md), current entrypoints and original trusted-base policy
were read. The full 431-test result belongs to the separately recorded tested
implementation commit; the frozen head adds its check report only.

## Findings

### LBEH-01 — Retarget the native workflow's test invocation

- Severity/category/confidence: **P2**, CI behavior, high.
- Location: `.github/workflows/opencode-native.yml:36`.
- Trigger and execution path: any native-smoke workflow job still invokes
  `python -m unittest tests.test_opencode_native_smoke -v` from the repository root.
  The refactor moves `tests/` to `.engineering-backbone/tst/`; `tests` no longer
  exists as an importable repository package.
- Impact: the Linux and Windows jobs fail in their first test step, before the
  pinned native discovery exercise. The subsequent native runner path was updated,
  but this prerequisite was left pointing at the removed layout.
- Evidence: the exact workflow command was executed on the frozen head with the
  isolated Python environment. Exit **1**, `ModuleNotFoundError: No module named
  'tests'`, `FAILED (errors=1)`. This is separate from the documented old trusted
  validator failure.
- Contract/diff relation: AC-3 and AC-7 require retargeted checks. The test-directory
  move causes a previously valid command to fail.
- Minimal correction/regression: use the new discovery directory and import top
  level, retaining all smoke failure-path tests; execute that exact workflow test
  command and ensure future command changes cannot silently reference the old
  package.

### LBEH-02 — Keep the legacy dependency document path in its adoption instructions

- Severity/category/confidence: **P3**, consumer documentation, high.
- Location: `docs/agent-governance/adoption.md:357`.
- Trigger and execution path: an existing Copier consumer follows the explicitly
  legacy adoption section to locate and complete the dependency compatibility
  document. The text says the optional package creates and preserves
  `docs/operations/engineering/dependency-compatibility.md`.
- Impact: that path describes the source reference repository, not the retained
  consumer output. The instructions direct the adopter to a file the legacy copy
  does not supply and incorrectly describe its update ownership.
- Evidence: the active legacy template filename still renders
  `docs/dependency-compatibility.md`; `copier.yml:31` preserves that same old path.
  The original base guide named the old path correctly. Only the source guide's
  literal was changed to the new source location.
- Contract/diff relation: AC-5 requires the old consumer layout and update contract
  to remain meaningful; this source/consumer distinction was lost during the move.
- Minimal correction/regression: retain `docs/dependency-compatibility.md` in the
  legacy section and distinguish source-only paths. Compare that instruction with
  the actual rendered optional-quality consumer and its preserved-file list.

### LBEH-03 — Resolve the native runner's default repository from its new depth

- Severity/category/confidence: **P2**, native-runner behavior, high.
- Location: `.engineering-backbone/src/opencode_native_smoke.py:480`.
- Trigger and execution path: the workflow and documented CLI invoke the relocated
  runner without `--repo`. Its default remains
  `Path(__file__).resolve().parents[1]`, which now selects `.engineering-backbone/`
  instead of the repository root. After archive verification, `prepare_fixture`
  opens the inactive companion `.engineering-backbone/opencode.json` as if it were
  the native root configuration.
- Impact: even after LBEH-01 is repaired, the native exercise fails with
  `source native config is outside the smoke contract`; no discovery or permission
  evidence can be obtained through the default invocation.
- Evidence: a bounded probe called actual `main()` argument parsing with no
  `--repo`, replacing only the archive/runtime wrapper with a call to actual
  `prepare_fixture()` in a temporary directory. It printed the selected
  `.engineering-backbone` directory, returned **1**, and wrote the exact error
  above. The probe did not download or execute OpenCode. The runner's default line
  is byte-identical to the original shallower `scripts/` location.
- Contract/diff relation: AC-3 requires executable paths to remain functional. The
  moved runner's unchanged parent-depth calculation creates this regression.
- Minimal correction/regression: calculate the repository root from the new
  canonical location. Add a regression for the default CLI root and real fixture
  preparation, while retaining explicit `--repo` behavior and existing failure
  checks. Native/model qualification remains a separate execution result.

## Coverage and observations

- Compared validator and compiled guard changes with their original source files:
  executing-layout selection, canonical policy/dependency/schema locations,
  historical byte checks and original-context link resolution, artifact discovery,
  compiler input/output roots and retained consumer branches.
- Inspected source CI, the trusted-base branch selection, native smoke workflow,
  dependency/Docker inputs, pinned legacy fingerprint transition, root Copier
  entrypoint, canonical template includes, copy/adoption guidance and native paths.
- The bounded retention audit compared all original 28 test modules and 418
  methods. All remain. AST assertion/rejection counts do not decrease; the Copilot
  selector split adds explicit checks while retaining the remaining parity checks.
  Existing historical fixture bytes match the base.
- The retention auditor independently regenerated the exact previous-main consumer
  using Copier in a temporary directory. All 45 files in the new predecessor
  archive matched byte-for-byte, and all eight recorded original tooling blob IDs
  matched Git. The actual old-main `run_update` evidence was read in the check
  record, not rerun or claimed as this review's own experiment.
- Reviewed new direct-copy tests for optional component pruning, project-owned root
  build files, policy/permission weakening, historical tampering and validation of
  newly added records. No additional confirmed test-retention defect was found.

## Limits and publication boundary

This review did not rerun the complete suite, build a container, execute a live
native client, qualify a model, exercise Windows, inspect remote CI results or
approve release. The actual old trusted validator's exit 1 / 34 errors remains the
explicit known migration blocker; it is not waived or reported as a new finding.
Container execution remains unproven locally. The draft publication purpose does
not make these findings PASS or authorize merge. Independent triage must classify
the three findings before repair, followed by Delta review of confirmed repairs
and their direct regressions.
