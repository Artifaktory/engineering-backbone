# OpenCode reconstruction verification

Date: 2026-10-16. Root orchestration records actual execution; this is not an independent semantic review or human approval. Historical lost results are not reused.

## Tested implementation

- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Tested head: `fb5732d7d07d8247ab49ea9905d614064728a9cf`.
- Tree: `5697c9a6d90bf6cb71024cff98e903c120b34765`.
- Binary base-to-head patch SHA-256: `c5bbd869fe002184e2f7c1a099cd6c83112d936f6e3bf435760a84a8b1de3f65`.
- Python 3.12.14; hash-locked requirements installed in a fresh isolated environment. Actionlint 1.7.12 archive digest checked before execution.
- Worktree was clean after the test-only fixture repair. This evidence record is added after the tested implementation.

## Complete suite

`.venv/bin/python -m unittest discover -s tests -v`: **412 tests passed**, exit 0, 375.266 seconds. No test exclusions or added skips.
Full-log SHA-256: `2ebc088305f1627873beaf9c9f7d0b909ef66e20584a8bc7deb4f62ac10bb82c`.

The first reconstructed run executed 410 tests and failed 22 assertions in the shared validator source fixture. It omitted the newly required native source package. Root diagnosis and a bounded test-only repair added complete minimal source data, preserved legacy consumer opt-out, and added the missing-AGENTS source negative case. Production guards were unchanged. The focused validator suite passed 51 tests in 42.713 seconds, then the entire discovered suite above was rerun.
Initial failed-log SHA-256: `019def2950b54e170d6ba598349e335b52cbe483a7d1fe323880b56feab758bb`.

## Deterministic gates

All commands below exited 0 on the final tested implementation. The trusted base is the exact detached baseline above; the predecessor validator is run from that checkout, never candidate code.

| Check | Command | Exit |
| --- | --- | ---: |
| current-validator | `.venv/bin/python scripts/validate.py --trusted-base <trusted-base>` | 0 |
| predecessor-validator | `.venv/bin/python <trusted-base>/scripts/validate.py --root . --trusted-base <trusted-base>` | 0 |
| navigation-compiler | `.venv/bin/python scripts/compile_navigation.py --check` | 0 |
| quality-compiler | `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 |
| toolchain-compiler | `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0 |
| workflow-compiler | `.venv/bin/python scripts/compile_workflow_kit.py --check` | 0 |
| source-dependencies | `.venv/bin/python scripts/check_source_dependencies.py` | 0 |
| actionlint | `actionlint` | 0 |
| whitespace | `git diff bf8e901ecd066e8e6d1b05f0c56a66081a473c0a HEAD --check` | 0 |

The full suite includes real Copier provider/opt-in/update/legacy cases, unchanged Copilot default body checks, previous-validator workflow execution, selected-role navigation and stale receipt cases, and negative native namespace/permission/path cases. The historical nested skill, reviewer-plan procedure and legacy mode findings have fresh regressions. No interrupted native adversarial reproduction was retried.

## Actual native Linux observation

The pinned OpenCode 1.19.0 smoke passed in 16.642 seconds with a localhost canned provider and no model/host credentials. It recorded 11 native/Git commands and 4 provider requests. The missing-role exit 1 is the expected negative case.
- Archive SHA-256: `7bb9e61ad6feacf2e89c10a6a2c1840e3de4220bb50ba1fc7110f31806076aec`.
- Executable SHA-256: `135ac3f86c43f2a22328a3554fec5f0bc57d71576077902661bc38dac34871fd`.
- Smoke runner SHA-256: `e48b6f3bbb51e489151764e5dec49eff0d7128d2f496f92e40c9edd365220376`.
- Complete local report SHA-256: `94bf9ce0835c3c216ea3522e93f4316b850b92fff4cd46a7506bd8fc2a1d1b30`.

Observed all five primary roles, full explicit instruction input in actual root and nested provider requests, and the selected reviewer marker. The provider requested an unadvertised write tool; the subsequent native error referenced its exact tool-call ID and the protected file remained unchanged. An unchanged file alone was not accepted. All 22 recorded source input hashes were rechecked against the tested tree and matched.

## Remaining gates and scope limits

Two independent Full implementation reviews, separate triage, any confirmed repairs/Delta and remote PR checks are pending at this record. Windows native execution awaits its real CI runner. Docker is unavailable locally; container validation remains a remote CI gap.

This smoke proves the recorded native discovery and narrow tool refusal only. It is not real-model qualification, OS confinement, native compaction/resume/delegation acceptance, or live AO activation. AO has its own scoped implementation/check/review record; no qualified tuple is seeded. No merge, release, deployment, settings change or automatic downstream activation was performed.

Ignored raw evidence: `artifacts/reconstruction-final-checks/manifest.json`, `artifacts/reconstruction-full-unittest-rerun.log`, `artifacts/opencode-native/reconstruction-final.json`. Their limits are retained here even if local raw logs later expire.
