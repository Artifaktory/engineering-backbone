# Local runner validation evidence

Base: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`. Isolated Python3.12.14; the pinned lock was checked with `pip install --require-hashes -r requirements.lock` (exit 0).

- Targeted `test_local_runners.py`: PASS, five tests, including both actual aggregate gate scripts for success/failure/skipped/cancelled dependencies.
- `python scripts/validate.py`: PASS.
- `python scripts/compile_toolchain_fingerprint.py --check`: PASS; current rendered fingerprint remains `7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb`.
- `python scripts/compile_workflow_kit.py --check`: PASS.
- Previous trusted-base validator against candidate with `--trusted-base`: PASS.
- Actionlint1.7.7 with explicit `ci-heavy` labels, shellcheck disabled: PASS. This is not runtime activation proof.
- `git diff --check`: PASS.
- `python -m unittest discover -s tests -v`: PASS, all 239 tests, 642.854s. Full suite includes producer/consumer upgrade and negative tests.
- Group repository access/isolation and actual source-job execution remain unverified. No settings/registration/merge/release/deployment writes are part of this scoped change.

## LR-BB-CODEX-001 repair qualification

The independent quality checker executed the repaired source at local commit
`a2e9f536f589042425ebc3f248dc0bde8215a7de`, tree
`b002b44cbcb5ebb16728635f7694dd02154fe9a6`: all **242 tests passed in 462.887s**.
The eight routing/gate regressions and the changed source-positive consumer
fixture also passed. Source and trusted validators, fingerprint/workflow-kit
compilation, actionlint (shellcheck unavailable), and committed-range whitespace
checks exited0. See [exact independent commands and log digests](local-runners-codex-checks.md).

Runtime acceptance remains separate: [remote evidence](local-runners-remote-runtime.md)
proves both quality jobs reached `pc2-build` in `af-ci-build-v1` at the earlier
published head `19fb75b640a470b459119f1654f5e43d3c1aef2b`. Trusted policy passed;
Foundation's 239-test run failed with 19 child Python-loader errors. The local
242-test result is not a pass of that remote run or runner certification. AC5
remains blocked for loader compatibility, completed runtime acceptance and clean
isolation evidence. No host/settings mutation or environment-filter weakening
has occurred.
