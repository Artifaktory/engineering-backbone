# Backbone Codex repair: independent quality checks

Finalized 2026-10-13T16:39:12.256553+00:00. Role: quality checker only. **Local repaired-source checks PASS; remote Foundation execution remains FAILED / AC5 blocked.**

Frozen local candidate `a2e9f536f589042425ebc3f248dc0bde8215a7de`, tree `b002b44cbcb5ebb16728635f7694dd02154fe9a6`. Prior local reviewed head `21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb`; migration trusted base `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`.

After execution, 166 tracked workflow/test/script/template/dependency files still match the frozen candidate byte-for-byte (zero mismatches), combined content SHA256 `af0d13e9f05576268c3d4055e0f5fb09af231908e9af388bb97a350b3c233cce`. Root documentary/Task acceptance updates do not alter these checked bytes. Full per-file proof is in `bb-codex-repair-sourceproof.json`.

Runtime: isolated `/workspace/scratch/59eed579c382/backbone-venv/bin/python` (`Python3.12.14`), using the unchanged hash-locked dependencies. Actionlint1.7.7 uses the specified custom-label config; shellcheck is disabled, so shellcheck is not claimed executed. No source repairs, host settings, toolcache changes or remote reruns were performed.

## Exact commands and results

All commands ran from `/workspace/scratch/a674a4925ed7/runner-migration/engineering-backbone`. `$PY` below denotes the exact isolated Python executable above; `$ROOT` denotes that repository and `$TRUSTED` denotes `/workspace/scratch/a674a4925ed7/runner-migration/backbone-trusted`. Fully expanded command strings, exit codes, cwd, timing, log paths and log digests are preserved in `bb-codex-repair-quality.json`.

| Command | Exit | Seconds |
| --- | --- | --- |
| `$PY -m unittest discover -s tests -p test_local_runners.py -v` | 0 | 0.77 |
| `$PY -m unittest discover -s tests -p test_workflows.py -k source_mode_cannot_bypass_consumer_gate -v` | 0 | 1.37 |
| `$PY scripts/validate.py` | 0 | 0.77 |
| `$PY scripts/compile_toolchain_fingerprint.py --check` | 0 | 1.07 |
| `$PY scripts/compile_workflow_kit.py --check` | 0 | 0.11 |
| `$PY $TRUSTED/scripts/validate.py --root $ROOT --trusted-base $TRUSTED` | 0 | 0.87 |
| `/workspace/scratch/59eed579c382/quality-actionlint-tooling/actionlint -config-file /workspace/scratch/a674a4925ed7/runner-migration/actionlint.yaml -shellcheck=` | 0 | 0.02 |
| `git diff --check` | 0 | 0.01 |
| `$PY -m unittest discover -s tests -v` | 0 | 463.71 |
| `git diff --check 21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb a2e9f536f589042425ebc3f248dc0bde8215a7de` | 0 | 0.01 |

Focused source-runner suite: **8 tests passed**. Changed source-mode positive fixture: **1 test passed**. Full required producer/consumer/negative/upgrade suite: **242 tests passed in 462.887s**, exit0; wrapper wall time463.71s. The full suite ran once on this repaired source snapshot and was not repeated.

The focused suite executes the actual fixed Bash gates for same-source, foreign-source, absent-head and shell-like head strings; both source modes are exercised. It confirms original quality check names stay scheduled, gates precede actions, source push/dispatch and external consumer forks remain compatible, and mandatory aggregate failures/skips/cancellations are rejected. Full consumer tests, approved-base execution boundaries, token filtering, toolchain/workflow-kit generation and trusted-base validation passed.

## Log digests

| Actual evidence log | SHA256 |
| --- | --- |
| `artifacts/local-runners/codex-repair-focused-local-runners.log` | `a627edf750de8b57144b61752ad2ae1a9306cd93fe08b90d15e7cd0756938b70` |
| `artifacts/local-runners/codex-repair-affected-source-mode-fixture.log` | `21ca5c929cdd34901d938d184c7dcf37d6bfc8b3d73d741a66f0844ffe8377ec` |
| `artifacts/local-runners/codex-repair-validate.log` | `183a7aa135e384ea2f24526c9162858fc51b4af25f642b5b0d586ae37704d37f` |
| `artifacts/local-runners/codex-repair-fingerprint-check.log` | `09a87260d7008ca1d5d69dd935c7e75446d8dbfd07ac49bcc9d0b793112d3f3a` |
| `artifacts/local-runners/codex-repair-workflow-kit-check.log` | `bfc57d07c02b666cfa4a1cef8cc18e7633c4e910a9b239791f4f1846c03951c1` |
| `artifacts/local-runners/codex-repair-trusted-base-validate.log` | `00aee686ce3456fc7b3bfef3b9d05f89757bdf7bd46b3be2f09ffe2aca362be2` |
| `artifacts/local-runners/codex-repair-actionlint.log` | `4e07d9363d7c27fdb3068ce2e10b775dfa8f96a8c0d2d52498399cd9749ca72f` |
| `artifacts/local-runners/codex-repair-diff-check.log` | `b7547a3c0968af11e233aff016c247e6db3d3a592e16cf3ccad8595973958b22` |
| `artifacts/local-runners/codex-repair-full-unittest.log` | `7a72465f3b6d95bb7fa1396e555f4492d3becaaed594a0aa117868a44a304ec0` |
| `artifacts/local-runners/codex-repair-committed-range-diff-check.log` | `5af54f4b10be6039fe9cf54e7024ae06a4f2a73ca933052ed3c7aa13d19b29dc` |

The committed-range whitespace record is explicitly derived from the actual tool transcript (empty stdout, exit0), rather than rerun for logging. Other check files are captured command stdout/stderr with command/cwd headers. All logs are in ignored source `artifacts/local-runners/`.

## Remote runtime and acceptance boundary

The separate `bb-remote-runtime-quality.md` / `.json` records remote run38427484521, Foundation job115400567007, published snapshot19fb75b640a470b459119f1654f5e43d3c1aef2b. That actual run proves pc2-build / af-ci-build-v1 repository access. It ran239 tests in470.476s and failed19 assertions because child Python exited127 while loading libpython3.12.so.1.0 after the unchanged allowlist removed LD_LIBRARY_PATH. Trusted base policy passed in that run; the full Foundation suite did not.

This local PASS covers the repaired gate scheduling/origin-check regression and unchanged complete source suite in the isolated local runtime. It does not certify the self-hosted interpreter, every build-group member, repository-wide isolation/access controls, or remote success at the repaired head. AC5 stays blocked until the selected runner runtimes pass exact-allowlist interpreter certification and the required remote jobs succeed. No source/tooling/environment-filter weakening was proposed or applied to turn that remote failure green.

Independent scoped Delta review, advisory GitHub review and human merge/release authority remain separate from deterministic local check results.
