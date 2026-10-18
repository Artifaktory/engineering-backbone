# OpenCode remote-finding repair: independent quality checks

Date: 2026-10-16. Session: `bb_reconstruction_repair_checks`. Responsibility:
independent deterministic quality execution for separately confirmed
`REC-BB-REMOTE-001`, with no implementation or triage authorship. This is not a
semantic Delta review, human approval or runtime qualification.

**PASS: the complete repaired-source suite ran 418 tests in 364.422 seconds,
exit 0, and all nine additional required gates exited 0.** No tests were
excluded, skipped or changed by this quality session.

## Exact tested source

- Repository: `Artifaktory/engineering-backbone`; Task: `BB-OPENCODE-010`.
- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Prior remote-reviewed head: `f22ef07ef018f41f487450465b757b658da6b396`.
- Equivalent prior local head: `a821da64c3468ebafe0e8586fc669b062b408907`.
- Prior identical tree: `ee1db8863633bc54765b32aa15e0a03a0452f57b`.
- Tested repair head: `4a0a4310dc54aba062654ab889ac16f8ac42558c`.
- Tested repair tree: `4f573d91ff80039f789866f776d6d4f44bbec1e6`.
- Binary base-to-repair patch SHA-256:
  `b1e4eeb7b0477b40c4ccad6456103237a7f8826cfb9b075a75bfe819c1f34a16`.
- Binary prior-reviewed-local-to-repair patch SHA-256:
  `d0822498a021c948f3dfee1a42475b1940d003419a1576f8f048eef3ffdf64d1`.

Read the current AGENTS, active Task Packet and remote-finding triage, alongside
the previously read canonical policy, contribution rules and approved OpenCode
contracts. The confirmed obligation restores full reviewed-seed input equality
at inactive-to-active admission. It preserves the companion's intentional flag
exception and legitimate non-activation behavior. The previous predecessor-
fingerprint finding remains closed; its regressions are still included.

All execution used a detached worktree at the tested repair commit:
`/workspace/scratch/6e019b0851cc/artifacts/backbone-remote-repair-checks-snapshot`.
This kept the tested snapshot immutable while the orchestration owner committed
the separate author report in the main checkout. The detached worktree was clean
before and after execution; its head/tree and both patch hashes were verified.
The exact trusted-base checkout was also verified clean at the declared base.
The two prior local/remote commit trees were independently checked equal.

At report preparation, the main checkout's `1cd42dc88888404af28fb821dce9cf88579c61f0`
differed from the tested repair only by adding the author report
`docs/reviews/opencode-remote-activation-repair.md`. This quality report is written
after all execution. No source, test, workflow, generated guard or dependency was
changed by this session, and no compiler was run with `--write`.

## Complete suite and required commands

The entire discovered suite finished with `OK`: **418 tests, 364.422 seconds**;
process wall time **365.181 seconds**, exit **0**. Full-log SHA-256:
`2af14ce059ae3ee2f1d792e85abfcc263488594762650156188ec4a24f3e5d17`.
This is fresh execution of the second repair, not reuse of either 414-test run.

For the following exact command forms, `PYTHON` is
`/workspace/scratch/6e019b0851cc/engineering-backbone/.venv/bin/python`,
`SNAPSHOT` is the detached worktree path above, and `TRUSTED` is
`/workspace/scratch/6e019b0851cc/artifacts/backbone-trusted-base`.
Every command ran with working directory `SNAPSHOT`. The interpreter reports
Python 3.12.14 and uses the previously hash-locked environment; the independent
source-dependency check passed. Actionlint reports version 1.7.12. The raw manifest
records complete argv arrays, actual exits, elapsed times and log hashes.

| Gate | Command | Exit |
| --- | --- | ---: |
| Complete unittest suite | `"$PYTHON" -m unittest discover -s tests -v` | 0 |
| Current validator | `"$PYTHON" scripts/validate.py --trusted-base "$TRUSTED"` | 0 |
| Exact predecessor validator | `"$PYTHON" "$TRUSTED/scripts/validate.py" --root "$SNAPSHOT" --trusted-base "$TRUSTED"` | 0 |
| Navigation compiler | `"$PYTHON" scripts/compile_navigation.py --check` | 0 |
| Quality compiler | `"$PYTHON" scripts/compile_quality_framework.py --check` | 0 |
| Toolchain compiler | `"$PYTHON" scripts/compile_toolchain_fingerprint.py --check` | 0 |
| Workflow compiler | `"$PYTHON" scripts/compile_workflow_kit.py --check` | 0 |
| Source dependencies | `"$PYTHON" scripts/check_source_dependencies.py` | 0 |
| Actionlint | `/workspace/scratch/6e019b0851cc/tools/actionlint/actionlint` | 0 |
| Whitespace | `git diff bf8e901ecd066e8e6d1b05f0c56a66081a473c0a HEAD --check` | 0 |

The full log includes passing resolver regressions for changes across all native
roles/procedures and other package inputs, including nonselected roles, added or
removed explicit-instruction references, and positive inactive-preparation,
already-active-update and unrelated-edit controls. The compiled-workflow case
passes with its approved-old-validator scenario. Historical authority equality,
the immediate-predecessor/coherent upgrade positives, mixed/unknown-tooling
negatives, clean single-commit clone and autocrlf clone cases all remain included.

The generated current tooling fingerprint is
`35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`.
The explicit previous-authority set retains the reviewed former current
`a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`
and immediate merged predecessor
`dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`.
These check results do not replace independent semantic review of the repair.

| Raw check log | SHA-256 |
| --- | --- |
| current-validator.log | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| predecessor-validator.log | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| navigation-compiler.log | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| quality-compiler.log | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| toolchain-compiler.log | `020abedd3802183fe911ec3f3e565d2ae8df9c7059c46b60ace8b173c3b2a60a` |
| workflow-compiler.log | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| source-dependencies.log | `4c8826eb1d965d4f44ac880d328b943916f62ff61c70af306cdc80400da82ee5` |
| actionlint.log; whitespace.log, each empty | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The separate author report records the failing-before and focused passing-after
executions. This quality session read that report and the retained logs; it does
not claim their executions as its own. The complete fresh rerun above independently
includes the affected cases. No repair was needed during quality execution.

## Unchanged actual native evidence

Read the retained original Linux and Windows ZIP artifacts from the initial
published head, as documented in `opencode-remote-initial-checks.md`. Recomputed
each ZIP hash and its original `report.json` entry hash; all match that record:

| Evidence | Linux | Windows |
| --- | --- | --- |
| ZIP SHA-256 | `29a98e19dfdf7b21b70164a8bd33c1dd8580afb09e90268ae8b09d1aaceca24d` | `140b1dcedcda964002fb0a8a7d0f94fda989e11eb863a0553cd2b5fea24efd17` |
| Original report SHA-256 | `a69f3ca8d4db181455d628b9bcad4e69941dcd84ff583dbf60132fb4d1484ffd` | `8d6368e9ed2f227164124b28b1a730e4027c46cbfb49012d813cbf37c0bcbc66` |
| Matched source inputs | 22 / 22 | 22 / 22 |
| Matched runner hash | `e48b6f3bbb51e489151764e5dec49eff0d7128d2f496f92e40c9edd365220376` | `d8dbee7a710b1e7ecfa7c6a396bc6404c6070aaba3f818755a89791c27ef82c0` |

For each platform, compared every reported source-input hash and the runner hash
with the repaired commit's raw Git blobs. Linux matches those raw bytes; Windows
matches their ordinary LF-to-CRLF checkout transformation. Each underlying raw Git
blob is also identical between the prior remote head and repaired head. Thus the
Windows check establishes source correspondence, not raw cross-platform byte
identity. All comparisons passed; the per-file evidence is retained.

This is a fresh input-continuity check against existing actual native reports.
No native runtime was rerun, and no blocked adversarial reproduction was attempted.
The earlier Linux/Windows observations remain limited to their pinned native
version, temporary instrumented fixture and canned provider. They do not establish
real-model qualification, OS confinement, native compaction/resume/delegation
qualification, host configuration adoption or AO lifecycle correctness.

## Handoff and evidence

The required local deterministic gate for `REC-BB-REMOTE-001` is complete.
Independent Delta and separate closure remain necessary; this report does not
close the finding or change Task acceptance states. Updated remote-tree identity,
actual refreshed PR CI and remote-review outcomes remain publication-phase work.
The earlier five successful CI jobs and Docker execution remain evidence only for
their original published head. No new local Docker execution is claimed; Docker
is unavailable in this environment. AO's separate checks and reviews are not
certified here. No activation, merge, release, deployment, settings change or
automatic downstream adoption was performed or authorized by these results.

Raw logs and reproducible runner remain under ignored
`artifacts/remote-activation-repair-checks/`:

| Evidence file | SHA-256 |
| --- | --- |
| manifest.json | `62ec19574a1f4b720b71cad2588d1beb6a5a7a400efe904ecf2d33e2cf95334b` |
| provenance.json | `048751db92248fc2c5747f5e3962ae58ed066bb233d597f49b6b327f142c7fc9` |
| final-state.json | `5df6ed9b4252296210150c8dbbb7e1d24d5269e9e041db733286cf0cb84a4ee0` |
| native-input-equality.json | `cf40f6c62597cb6dd2b39c26a8f39a961a771f8e55935193a50ba9e53bd1f8ac` |
| run_checks.py | `55d96637bbfbd7ed1ee6d3c92d3351d558cf1db5c2abd8bd347d54756c7aaa52` |

Only this new durable quality report and ignored execution evidence were written
by this session. No commits or remote writes were made.
