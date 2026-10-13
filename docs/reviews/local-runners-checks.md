# Local runner validation evidence

Base: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`. Isolated Python3.12.14; the pinned lock was checked with `pip install --require-hashes -r requirements.lock` (exit 0).

- Targeted `test_local_runners.py`: PASS, five tests, including both actual aggregate gate scripts for success/failure/skipped/cancelled dependencies.
- `python scripts/validate.py`: PASS.
- `python scripts/compile_toolchain_fingerprint.py --check`: PASS; current rendered fingerprint remains `7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb`.
- `python scripts/compile_workflow_kit.py --check`: PASS.
- Previous trusted-base validator against candidate with `--trusted-base`: PASS.
- Actionlint1.7.7 with explicit `ci-heavy` labels, shellcheck disabled: PASS. This is not runtime activation proof.
- `git diff --check`: PASS.
- Full unittest suite was initiated before Full review; final result will be recorded before PR delivery.
- Group repository access/isolation and actual source-job execution remain unverified. No settings/registration/merge/release/deployment writes are part of this scoped change.
