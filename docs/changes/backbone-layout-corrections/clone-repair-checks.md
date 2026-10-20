# BB-LAYOUT-012: independent clone-repair checks

Quality-checker session: `layout_quality`, separate from implementation and review.
Date: 2026-10-20. **Affected suite: 41 tests passed; all 11 additional commands
returned exit 0.** This report verifies the local repair and its retained
contracts. The required changed-head remote Foundation result remains separate.

## Tested snapshot

- Published repair baseline: `2ddfa803688c70b556dc83bcf07a4c3911713be5`.
- Original corrective baseline: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.
- Original PR base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Tested repaired head: `e2bd3c7dc881348967af28a6da99be992e94e122`.
- Tested tree: `f94d11c832a8f5f0d492c1b8d7b6a71a91bec5c3`.
- Binary repair-baseline-to-head patch SHA256:
  `9c5a498c61b72e2774e1fac84856e2f35423fbed5b5b4e79edcccded7efd6000`.

The checker read the [bounded plan](clone-repair-plan.md),
[independent plan review](clone-repair-plan-review.md) and
[confirmed triage](clone-repair-triage.md) before testing. The worktree was clean
at the frozen head. All **556 tracked input hashes** matched before and after
execution, with a clean worktree at completion. This report was added afterward;
the checker made no source/test repair.

## Executed checks

Commands ran from the repository root with the existing isolated Python
**3.12.14**, unchanged hash-locked dependencies and local Git **2.51.1**.
`python` below denotes that environment's interpreter. `HEAD` in the table
denotes only the tested repaired commit above.

| Command | Exit | Result |
| --- | ---: | --- |
| `PYTHONPATH=.engineering-backbone GIT_TRACE=<absolute-artifact-path> python -m unittest tst.test_copilot_distribution tst.test_copilot_validation tst.test_copilot_workflow_guard -v` | 0 | **41 tests in 78.308 seconds, OK.** |
| `python .engineering-backbone/src/validate.py` | 0 | Structural PASS; no supplied trusted-base comparison. |
| `python .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | Compiled authority matches. |
| `python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | Compiled catalog and entrypoints match. |
| `python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | Compiled workflow matches. |
| `python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | Rendered toolchain fingerprint matches. |
| `python .engineering-backbone/src/check_source_dependencies.py` | 0 | Tracked inputs and all 26 locked installed versions consistent. |
| `git diff --check` | 0 | Working diff clean. |
| `git diff --cached --check` | 0 | Staged diff clean. |
| `git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f HEAD` | 0 | Complete committed PR diff clean. |
| `git diff --check 2ddfa803688c70b556dc83bcf07a4c3911713be5 HEAD` | 0 | Committed clone-repair diff clean. |
| `git diff --check c50108773ba3195bf0f7503e5dffb2d7bfc78cd3 HEAD` | 0 | Complete committed corrective diff clean. |

The actual trace path was
`/workspace/scratch/6e019b0851cc/backbone-layout/artifacts/clone-repair-quality/git-trace.log`;
the interpreter was
`/workspace/scratch/6e019b0851cc/backbone-venv/bin/python`.
Copier's missing answers-file warning appeared for intentionally fresh fixtures;
the suite and compiler checks completed successfully. The rendered fingerprint
remains `402e3fa62d99afda07bd2929afef9237e28835b3a3a349e6ca194d01cb58343f`.

## Independently observed transport and preservation

The affected suite includes the actual
`CopilotDistributionTests.test_historical_upgrade_adds_package_without_replacing_local_authority`
method. Its Git trace contains **14 clone commands for the exact
`/upgrade-source` fixture**, all using `file:///tmp/copilot-distribution-…/upgrade-source`,
and **14 corresponding `git upload-pack` invocations**. Other unchanged tests'
source paths are outside this scoped count. This independently observes the
repaired real fixture's transport during its successful copy, rejection and
update checks; it does not rely solely on the author's earlier trace.

The actual rendered answers are asserted to retain the `git+file://` source at
both revisions and initial tag `v0.1.0`; the existing final `v0.2.0` assertion
remains. The suite executes the original installation-only rejection subtests,
actual update, local-authority byte preservation, no-rejection-file checks and
trusted consumer validation. No answers were manually rewritten by this checker.

An independent AST audit against the published baseline confirms:

- All **15 original assertion call ASTs** remain intact and ordered; three source/tag
  assertions were added, for 18 total in this method.
- Both original real `run_update` call ASTs are unchanged.
- The rest of this test module's AST is unchanged.
- The only changed substantive file is the scoped test file; all other changed
  paths are corrective evidence or the current Task Packet.
- **433 test methods** remain present. This bounded check executed 41 of them;
  no local full 433-test rerun is claimed.

The tested test-file SHA256 is
`2dc0490bf69ed5986d6379e856543958eb9904f12cafbeacf3f5d224a44c2ce1`.
No runtime authority, dependency, template, workflow or validator change is part
of this repair.

## Evidence and publication limits

Ignored raw artifacts are under `artifacts/clone-repair-quality/`:

| Artifact | SHA256 |
| --- | --- |
| `affected-suite.log` | `f46b39980b8b22c0b0bc9fc37d9c8efd40bf4e916c619a283c11ddb43a9ebb50` |
| `git-trace.log` | `a6804445f4d81c66174b5b2f664b23fc02f4b324b4ab16eeeee8037ee26846e8` |
| `commands.json` | `31d149e7f88c1fac96c8ab26be7e16388f048df91028d0f325e6687856b66a2a` |
| `preservation.json` | `01076f2ebc759729bf938e2880f693cca5b0f5ff1adb495ad8e587130b02253a` |
| `inputs-before.json` / identical `inputs-after.json` | `97f38c27065c387995ccfcd67788a1d1d88d920efd9ecbb9caa57d12ecb1ed25` |
| `transport-and-freeze.json` | `6b592e44f35cc7b91e7e2f6fb91335d67767e8b51540cfc45715b4dbfb2c9048` |

The two failed hosted Foundation attempts at the published baseline remain
failed evidence in the triage records. Their Git **2.55.0** / Python **3.12.15**
environment was not reproduced here. The exact underlying Git/filesystem cause
is unproven. The local passing tests establish retained behavior and selected
transport on Git 2.51.1; they do not yet prove the hosted failure resolved.
The actual changed-head full Foundation run must be observed after publication.

These committed whitespace checks bind only `e2bd3c7…`. After this report and
review evidence are committed, repeat the original full-PR, corrective and
repair committed-diff checks against the exact final publication head. Independent
bounded second Full review remains separate from this quality report.

No container, native client or model session was executed for this test-only
repair. The separate old-main trusted-base layout gate and BB-LAYOUT-013's human
merge prerequisite are unchanged; candidate structural PASS does not replace
that gate or authorize merge.
