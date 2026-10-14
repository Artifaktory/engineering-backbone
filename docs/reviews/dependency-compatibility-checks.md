# Dependency compatibility: independent quality execution

Role: read-only quality checker. No source edits, repairs, commits, semantic approval or release authority.

- Base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
- Original frozen head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`.
- Base-to-head patch SHA256: `6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0`.
- Python: `3.12.14` from `.venv/bin/python`.

## Deterministic checks: passed

These actual commands all exited0 on the original frozen head. Each exact argv/output/exit is in its ignored `quality-*.log`; `quality-checks.json` maps the evidence.

```sh
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/compile_navigation.py --check
.venv/bin/python scripts/compile_quality_framework.py --check
.venv/bin/python scripts/compile_toolchain_fingerprint.py --check
.venv/bin/python scripts/compile_workflow_kit.py --check
.venv/bin/python scripts/check_source_dependencies.py
.venv/bin/python artifacts/dependency-compatibility/trusted-base/scripts/validate.py --root . --trusted-base artifacts/dependency-compatibility/trusted-base
artifacts/tools/actionlint
git diff 229ac884c1a2ac70f0fb5c961bd517c9eaf740af HEAD --check
```

Both catalogs and requirements manifests remained byte-unchanged in the base-to-head Git diff. Source worktree was clean at execution entry and the last observed pre-repair check.

## Full suite: failed, one underlying cause

Command: `.venv/bin/python -m unittest discover -s tests -v`.

Actual result: **362 tests,3 failures,0 errors; exit1**. Unittest elapsed1289.482 seconds; wrapper elapsed1291.44 seconds. The remaining359 tests passed. Whole log: `artifacts/dependency-compatibility/quality-unittest.log`.

Whole-log SHA256: `236ad1cb84f116dffef01133e3d308c089facd1572c7ef2b762862079e0663fe`.

**DEP-TEST-001 (P2):** `tests/test_workflows.py:281-284` keeps an exact expected set of historical toolchain fingerprints. New reviewed immediate-predecessor identity `e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450` is retained by the candidate workflow, but missing from the test expected set. The direct assertion and both clean-single-commit/autocrlf wrappers fail with the same unexpected-set-member message. This is one underlying quality failure. Independent exact-predecessor workflow execution passes, so this result does not establish an upgrade execution defect.

No unchanged retry was performed. Root separate triage confirmed DEP-TEST-001 and, after the original full run completed, committed a two-line test-only repair at `79fc21fbc5ff77938e3d2d952b90550cb36dedbd`. Quality checker executed the three affected tests on that frozen repair: **3 passed**, exit0,62.722 seconds(unittest),63.92 seconds(wrapper). Evidence: `quality-repair-targeted.log`, SHA256 `bd423e409a67199219b83a0e86a98bdebf13303faddf054904ec4d4a46188b08`.

## Clean locked environment: passed

Created fresh `artifacts/dependency-compatibility/quality-clean-venv`. Installed `requirements.lock` with `pip install --require-hashes --only-binary=:all: -r requirements.lock`. All26 locked package versions installed. In that new environment, `python -m pip check` and `python scripts/check_source_dependencies.py` exited0. Elapsed27.53 seconds. Evidence: `quality-clean-install.log`.

## Exact immediate-predecessor consumer upgrade: passed

Command: `.venv/bin/python artifacts/dependency-compatibility/quality-real-upgrade.py` (exit0). The ad hoc script exports exact base/head Git trees, creates a temporary tagged source, renders an old active-navigation consumer with both native providers, performs real Copier `run_update`, and validates it against its unchanged old baseline.

Observed: dependency extension installed inactive; active navigation preserved; eight native/project files and all41 quality/technology catalog JSON files preserved byte-for-byte; old guard resolution and new guard validation/resolution against the old consumer all exit0.

The exact candidate reusable-workflow shell payload also exits0 against those old/new consumers, including actual current/previous toolchain attestation. Current digest `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`; retained predecessor `e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450`. Payload SHA256 `a3fedf9262baae88b0e8955326457b3386fce12242edecc24c8203e619b2809e`. Evidence: `quality-real-upgrade.log` and its ad hoc script. This evidence covers actual CLI/workflow behavior, without claiming native client instruction loading.

## Explicit limits and repair verification

Docker executable is absent. Local container build/smoke was **not executed**; actual CI execution remains pending. Evidence: `quality-container-capability.log`. No Windows execution or native agent discovery claim is made. Image registry provenance is separately retained by root in `python-full-base-image.json`; the earlier slim candidate artifact is not final-image evidence.

Separate triage required a successful full suite before publication. After the targeted repair checks, the quality checker executed the complete discovered suite again on the frozen repair using four isolated module subprocesses. No tests were excluded; each worker recorded the exact started IDs. The ID multiset was compared with fresh full unittest discovery and required exact one-time coverage.

## Repaired full suite: passed

- Head: `79fc21fbc5ff77938e3d2d952b90550cb36dedbd`.
- Command: `.venv/bin/python artifacts/dependency-compatibility/quality-full-sharded.py`.
- Discovery: `unittest.defaultTestLoader.discover("tests")`,362 unique test IDs across23 modules.
- Actual execution: **362/362 tests passed**, zero failures/errors/skips/expected-failures/unexpected-successes; all23 module exits0. Four isolated subprocess workers; elapsed368.83 seconds.
- Exact discovered-versus-started ID equality passed. No exclusions or duplicate IDs. HEAD remained unchanged and worktree clean at completion.
- `quality-full-discovered.json` records every expected ID; `quality-full-sharded-results.json` records every started ID, per-module totals, exits and whole-module-log hashes. The test runner and parallel-safety read-only audit are retained in the ignored artifacts directory.

Final evidence hashes:

- `quality-full-sharded.log`: `c1b53a4998eb1d5f8f09a38b4d951f2e8291167efead5806098b520524f04508`.
- `quality-full-sharded-results.json`: `7210faf19b25cfa0f80975b62017820cd1a50491d61d39e84b44442cf142b709`.
- `quality-full-discovered.json`: `30bca99d446e7d1dd24fc1e1055f81fa0c35b9e232371c4831d2f65a28203e1e`.
- `quality-full-sharded.py`: `cc5f9fb2399ebea9f8ece21905674d5dda3d81a7d617092d3938a30c12385b1a`.
- `quality-repair-targeted.log`: `bd423e409a67199219b83a0e86a98bdebf13303faddf054904ec4d4a46188b08`.

Original failed full-suite evidence remains retained above. DEP-TEST-001 is execution-verified closed by the targeted and complete rerun; independent Delta review and separate triage remain the owner's responsibility. Container build/smoke is still explicitly pending actual CI. These results do not constitute semantic approval or native agent-loading proof.
