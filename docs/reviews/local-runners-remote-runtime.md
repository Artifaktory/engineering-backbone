# Backbone remote runtime: independent quality evidence

Read-only remote diagnosis for run [38427484521](https://github.com/Artifaktory/engineering-backbone/actions/runs/38427484521) / [job 115400567007](https://github.com/Artifaktory/engineering-backbone/actions/runs/38427484521/job/115400567007). This is distinct from local quality checks of the later Codex repair `a2e9f536f589042425ebc3f248dc0bde8215a7de`.

## Actual remote observations

| Observation | Evidence |
| --- | --- |
| Runner/access | The Foundation log names `pc2-build`, group `af-ci-build-v1`; source-repository access and one real execution are proven. |
| Remote source snapshot | Checkout/log reports `19fb75b640a470b459119f1654f5e43d3c1aef2b`. |
| Python setup | `Successfully set up CPython (3.12.14)`; toolcache `/home/vboxuser/actions-runner/_work/_tool/Python/3.12.14/x64`. |
| Parent environment | `LD_LIBRARY_PATH` points at that toolcache's `lib` directory. |
| Full suite | `Ran 239 tests in 470.476s`, `FAILED (failures=19)`, step exit1. |
| Child interpreter | All19 failure records contain `libpython3.12.so.1.0: cannot open shared object file`; configured checks exit127 before fixture Python code executes. |
| Other run job | `Trusted base policy` returned success; this does not certify the Foundation child runtime. |

Decoded GitHub job log is retained in ignored `artifacts/local-runners/bb-remote-foundation-38427484521-115400567007.log`; SHA256 `474e564d398467f49b9a2af43aa1b30576c479d071639da6ef87815e19a4eed7`. Metadata and exact counts are in `bb-remote-runtime-quality.json`.

## Execution path and classification

Tests configure commands with `sys.executable`. `scripts/workflow_kit.py:273-282` creates a fixed allowlisted environment and starts the approved argument vector without a shell. Dynamic-loader variables, including `LD_LIBRARY_PATH`, are deliberately absent. The parent Python can run with setup-python's exported loader path, while this exact executable cannot load libpython after that path is removed. The log directly demonstrates the resulting child startup failure; no inference of a check implementation failure is needed.

Read-only `git diff --exit-code 2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13 -- scripts templates requirements.lock requirements.txt tests/fixtures` exited0. `scripts/workflow_kit.py` SHA256 is `5737db1f426271722fb9dc60a12daf6e76b1433215dc643bd3b3b6b03185c357`. The protected runner and consumer tooling are unchanged from trusted base.

Classification: **unfulfilled local-runner runtime prerequisite / migration qualification gap**. It is a real required remote check failure. It is not evidence that the runner-group access is absent, or that the shared kit's environment filtering regressed in the migration diff. The observed runner exposes an interpreter requiring ambient loader configuration; prior hosted behavior for this exact patch interpreter is not independently established here.

## Affected remote test failures

| Test family | Failed records | Common cause |
| --- | --- | --- |
| `WorkflowKitTests` | 7 | Direct command success, argv/no-shell, approved-base authority, timeout, maintenance, declared failure and token-filter tests receive child exit127. |
| `WorkflowKitCopierTests.test_every_profile_can_render_then_run_actual_local_fixture_checks` | 5 profile subtests | docs/python/typescript/go/dotnet fixture commands cannot start the same Python executable. |
| `WorkflowKitPayloadTests` | 7 | Configuration, prepared fresh-job artifact, historical consumer, immutable approved failure, maintenance/security and import-poison tests encounter the identical loader failure. |

Some negative assertions expected an approved failure code7/19/23/31 or a timeout and instead receive127. Those differences do not justify weakening the assertions: the intended command was never started.

## Safest scoped response

Keep the confirmed Codex origin-gate repair minimal. Preserve all checks, events, consumer defaults, approved command vectors, environment filtering, templates, scripts and fingerprints. Keep AC5 blocked until the selected runners satisfy the actual execution prerequisites.

Retain the documented certification command in `docs/local-runners.md`: launch the exact selected interpreter as a child under **the existing full allowlist**, checking its real exit and supported version. A parent-only `python --version` or successful setup action is insufficient. The selected CPython3.12 runtime and required libraries must be resolvable intrinsically in that minimal environment, without `LD_LIBRARY_PATH`, `LD_PRELOAD` or equivalent overrides. Certification must cover the actual selected build machines; one Foundation access result does not certify every group member or reusable delivery path.

Do not fix this by expanding the environment allowlist, exporting loader paths through the kit, skipping tests, modifying host ldconfig/system files, patching the shared setup-python cache, or changing consumer/toolchain policy. A job-owned runtime/container or additional fixed preflight would need its own scoped plan and evidence; neither is implemented or certified here. The current documented prerequisite is honest about the unfulfilled host/runtime condition.

A changed, certified runtime is a justified input for one later remote retry. No remote rerun, settings change, host mutation, consumer change, source repair, release or deployment was executed in this quality role. The local repaired-snapshot suite is reported separately and cannot turn the failed remote run green.
