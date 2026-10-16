# OpenCode reconstruction: bounded repair quality checks

Date: 2026-10-16. Session: `bb_reconstruction_repair_checks`. Responsibility:
independent deterministic quality checking, with no implementation or finding-triage
authorship. This record is not a semantic Delta review, human approval or runtime
qualification.

## Frozen source and scope

- Repository: `Artifaktory/engineering-backbone`; Task `BB-OPENCODE-010`.
- Exact trusted base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Previous Full head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Tested repaired head: `0778d728a273bc6af845b18d33f96e5731df9bc9`.
- Tested repaired tree: `6527697236e82bb39e07b2237a1efafb8907de3e`.
- Binary base-to-repaired-head patch SHA-256:
  `c1db79fa470ec2bbcc2b62955cc60372683f204cdbb4b89020007741db09066b`.
- Binary previous-Full-to-repaired-head patch SHA-256:
  `bdb1111380f5145907e415b6ecbf0d2f353f50165f289f0614ad88e14876b7e4`.

Read AGENTS, CONTRIBUTING, canonical policy, the active Task Packet and approved
plan, both OpenCode contracts, prior verification evidence and the separate triage
record before checking. Triage confirmed `REC-BB-SEC-001` with duplicate alias
`REC-BB-FUNC-001`: the candidate workflow had stopped admitting the immediately
preceding approved tooling fingerprint. The bounded repair retains that exact
fingerprint and adds positive/negative predecessor-consumer regressions with a
self-contained fixture. Four repair files and three Full/triage records differ
from the previous Full snapshot. Historical fixtures and production guards are
unchanged by this repair.

The checkout was clean at the start and end of all commands; head and tree were
rechecked unchanged. The detached trusted-base checkout was independently checked
to have the exact declared base and a clean worktree. This report is written after
the tested source freeze. No implementation, workflow or test was edited by this
quality session; no compiler was run in write mode.

## Actual complete rerun

**PASS: 414 tests in 355.728 seconds, exit 0.** The process wall time was
356.321 seconds. Command:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The entire discovered suite ran without test exclusions, added skips or changed
assertions. Its final output was `OK`, with no failures or skips. This is fresh
execution of the repaired source, not reuse of the earlier 412-test result.
Full-log SHA-256:
`d568708d1a0409c7878438a60143f382c6f22239008f4fcc3d6dd7934438938f`.

The run includes the actual candidate workflow admitting unchanged immediate-
predecessor tooling and a coherent current-tooling upgrade. Its negative cases
reject an unapproved candidate, an unapproved trusted baseline and a mixed tuple
of otherwise approved tooling without executing the unapproved validator marker.
The clean single-commit and autocrlf clone checks run those cases while verifying
the predecessor Git objects are absent. Existing historical authority-set equality,
Copier upgrade, OpenCode adapter and legacy-adapter tests remain included.

## Deterministic gates

All nine commands below exited 0. Commands ran from
`/workspace/scratch/6e019b0851cc/engineering-backbone`, using its isolated
`.venv/bin/python` (Python 3.12.14) and the installed hash-locked dependencies.
`<trusted-base>` below means the exact path
`/workspace/scratch/6e019b0851cc/artifacts/backbone-trusted-base`.
The Actionlint executable was
`/workspace/scratch/6e019b0851cc/tools/actionlint/actionlint`, reporting version
1.7.12. The raw manifest records complete argv arrays, elapsed times and log hashes.

| Check | Command | Exit |
| --- | --- | ---: |
| Current validator | `.venv/bin/python scripts/validate.py --trusted-base <trusted-base>` | 0 |
| Exact predecessor validator | `.venv/bin/python <trusted-base>/scripts/validate.py --root /workspace/scratch/6e019b0851cc/engineering-backbone --trusted-base <trusted-base>` | 0 |
| Navigation compiler | `.venv/bin/python scripts/compile_navigation.py --check` | 0 |
| Quality compiler | `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 |
| Toolchain compiler | `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0 |
| Workflow compiler | `.venv/bin/python scripts/compile_workflow_kit.py --check` | 0 |
| Source dependencies | `.venv/bin/python scripts/check_source_dependencies.py` | 0 |
| Actionlint | `/workspace/scratch/6e019b0851cc/tools/actionlint/actionlint` | 0 |
| Whitespace | `git diff bf8e901ecd066e8e6d1b05f0c56a66081a473c0a HEAD --check` | 0 |

| Raw check log | SHA-256 |
| --- | --- |
| current-validator.log | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| predecessor-validator.log | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| navigation-compiler.log | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| quality-compiler.log | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| toolchain-compiler.log | `f28d12e31a7d926bac40e96c0f3b61d23d15f738c9fc83f02e9db3d4e38d0ea4` |
| workflow-compiler.log | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| source-dependencies.log | `4c8826eb1d965d4f44ac880d328b943916f62ff61c70af306cdc80400da82ee5` |
| actionlint.log; whitespace.log, each empty | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The current generated tooling digest remains
`a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`.
The repair adds only the exact immediate-predecessor identity
`dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`
to the previous authority list. Structural checks do not independently certify
the semantic appropriateness of that authority; that remains Delta-review scope.

## Earlier regression evidence inspected

The author's retained pre-repair log reports one failing test in 0.962 seconds,
at the exact rejection `Trusted base toolchain fingerprint is not approved by
this pinned workflow`. Its subsequent focused log reports all five tests passing
in 32.695 seconds. These are inspected supplied results, not commands rerun by
this quality session. The complete fresh suite above includes the repaired cases.

| Supplied artifact | SHA-256 |
| --- | --- |
| `artifacts/opencode/predecessor-before-repair.log` | `584245c7fc44bb97c286b018555cb255d3f215058cb18e1abe28169527a838d1` |
| `artifacts/opencode/predecessor-repair-focused.log` | `7bc748c13daf6cb75f9c73efbc4cff0b863406014db3edd5c98f555a836a4685` |
| `tests/fixtures/opencode-predecessor/manifest.json` | `6d0a9112e739554c89f7530a74c530ba6416bf8f037be3de8f5d5f9f4fe36c46` |
| `tests/fixtures/opencode-predecessor/consumer.zip` | `bc94bbb16d5fbeaa3e8bc41f49e0c1f8518d79617b6b05a0cfa6354eb4349d70` |

## Native evidence continuity and remaining gates

The repair does not change native adapter or smoke implementation. Independently
recomputed all 22 source-input SHA-256 values recorded by the prior actual Linux
smoke and the runner hash; all match the repaired checkout. The original native
report hash is
`94bf9ce0835c3c216ea3522e93f4316b850b92fff4cd46a7506bd8fc2a1d1b30`;
the unchanged runner hash is
`e48b6f3bbb51e489151764e5dec49eff0d7128d2f496f92e40c9edd365220376`.
No native smoke was unnecessarily rerun and no blocked adversarial reproduction
was attempted. This equality check preserves only the earlier recorded Linux
canned-provider observation; it adds no runtime behavior evidence.

The repaired-source local deterministic gate is complete. Independent Delta for
both confirmed finding IDs remains required before publication. Actual Windows
native execution and the locally unavailable Docker build/smoke remain remote CI
gaps. The paired AO implementation and its independent gates are separate. No
real-model qualification, OS confinement, native compaction/resume/delegation
qualification or governed activation is established by this report. Remote PR
identity, visible Codex request and actual CI/review outcomes remain pending.
Human merge/release approval and the prohibition on automatic downstream
activation remain unchanged.

Raw evidence is under ignored `artifacts/reconstruction-repair-checks/`:

| Evidence file | SHA-256 |
| --- | --- |
| manifest.json | `031e64636fa4bb0f119adccdf943cf21d091524eb524cab13840dc85c00d7eb4` |
| provenance.json | `d6916855137a8f3b411f14d4a583ffc3b0165b6d73014d183fccf05d2b423fda` |
| final-state.json | `fb7218100385b1efa3890be896668a70af8fa55f5fed799a7b962593f659bfe1` |
| native-input-equality.json | `10069241b5c5759accb6673bd673ca9b50144ecb2b3489298f289794aada129c` |
| run_checks.py | `2bba0cc7b7ad9ee00bdba50f6da44c2cbee2c98a509bb78a7d7356ac05e6c7fd` |

No commits or remote writes were made by this quality session.
