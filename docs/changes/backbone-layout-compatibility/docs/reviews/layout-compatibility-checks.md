# BB-LAYOUT-013 deterministic compatibility checks

Quality-checker session: `layout_quality`, separate from implementation and triage.
Date: 2026-10-20. **Final repaired run: 441 tests passed; all additional commands
below returned exit 0.** This is deterministic check evidence, not formal Full
review, a merge authorization, or a claim about a later published head.

## Frozen scope

| Input | Identity |
| --- | --- |
| Actual old-main base | `212608aa50ee517b3dd3107a9480da997222fd4f` |
| Tested repaired bridge head | `aaa74e3dfc60836f8aae7c2751bc9dd889c52470` |
| Tested repaired tree | `fe6da7e734e7d6cdea508dc007649f03b903c423` |
| Binary base-to-head patch SHA256 | `8f6ca8f0f22fe3065f392aed73c194be8aeebc7e0ee7b74680c871953e671969` |

The initial bridge run at `785d4d51dec3ff8f26bf2a4322b3ffe9422ef7ff`
completed with **441 tests, 13 failures, exit 1** in 462.650 seconds. Its complete
failure inventory remains in [the failed-run record](layout-compatibility-check-failures.md).
[Independent triage](layout-compatibility-check-triage.md) classified four causes,
LC-CHECK-01 through LC-CHECK-04, before implementers repaired them. This checker
made no source or test repairs. The final run below is separate evidence on the
repaired snapshot and does not replace or relabel that failed run.

The final run began with a clean worktree. Before/after SHA256 inventories matched
for all **505 input files**, with no additions during execution. The identical
inventory JSON SHA256 is
`7a688fb7936e92766398da6618a2fb45acd3c1879116192d87efd27929e255ee`.
This report was written only after that comparison and the completed suite.

## Executed checks

Commands ran from the old-layout bridge root using isolated Python **3.12.14**
and the previously installed hash-locked source dependencies. `python` below is
that environment's interpreter. No dependencies or source inputs were changed.

| Actual command | Result |
| --- | --- |
| `python -m unittest discover -s tests -v` | Exit 0; **441 tests in 450.358 seconds, OK**. |
| `python scripts/validate.py` | Exit 0; structural validation, without a supplied trusted base. |
| `python scripts/compile_navigation.py --check` | Exit 0. |
| `python scripts/compile_quality_framework.py --check` | Exit 0. |
| `python scripts/compile_workflow_kit.py --check` | Exit 0. |
| `python scripts/compile_toolchain_fingerprint.py --check` | Exit 0. |
| `python scripts/check_source_dependencies.py` | Exit 0; **26** locked installed versions and tracked dependency inputs consistent. |
| `actionlint -shellcheck= -pyflakes=` | Exit 0; actionlint **1.7.12**. Optional shellcheck/pyflakes analyzers were not executed. |
| `git diff --check` | Exit 0. |
| `git diff --cached --check` | Exit 0. |
| `git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f aaa74e3dfc60836f8aae7c2751bc9dd889c52470` | Exit 0; actual committed PR base/head diff. |

The checked rendered current tooling fingerprint is
`a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`.
Copier emitted its missing answers-file warning for intentionally fresh render
fixtures; the full suite and compiler checks still completed successfully.

## Actual trusted-base transitions

The following are real Git checkouts, not path projections or synthesized
candidate trees. The checker independently verified each HEAD, clean worktree,
and **every actual tracked file blob** against its recorded commit, including
after the full suite.

| Alias | Commit | Tree | Verified files |
| --- | --- | --- | ---: |
| `OLD` | `212608aa50ee517b3dd3107a9480da997222fd4f` | `c31ee9b6e418325936b59e31cd7e9b9865ed0064` | 495 |
| `PR18_ORIGINAL` | `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` | `af532155a9f1196aa65e553b24b957f5f50297a3` | 542 |
| `PR18_CURRENT` | `2ddfa803688c70b556dc83bcf07a4c3911713be5` | `ae42d5f1848b65509e51813b824b7d9c2b61a6cc` | 551 |

`BRIDGE` denotes the tested repaired bridge root identified above. With these
aliases standing for the corresponding checkout paths, the executed commands
were:

```sh
python "$OLD/scripts/validate.py" --root "$BRIDGE" --trusted-base "$OLD"
python scripts/validate.py --root "$PR18_ORIGINAL" --trusted-base "$OLD"
python scripts/validate.py --trusted-base "$OLD"
python scripts/validate.py --root "$PR18_CURRENT" --trusted-base "$OLD"
```

**All four returned exit 0.** The first executes the actual old-main validator
against the old-layout bridge. The remaining commands execute the bridge-owned
validator against the exact original PR 18, its own old-layout source, and the
actually published corrected PR 18, respectively. They all supply the actual
old-main checkout as trusted base. No candidate-owned validator, fallback,
candidate path transformation, or waived exit code was used.

The original `c501087…` transition remains the primary frozen-fixture evidence.
The `2ddfa803…` transition supplements it for the corrected selector and added
task/review records. These local transitions do not mean that the prerequisite
has merged or that PR 18 already has a compatible trusted `main`.

## Preservation and coverage

The independent Git-blob audit found **413 existing protected blobs byte-identical
to the old base**, including **all 59 original fixture blobs**. The protected set
contains original policy, schemas, standards, legacy templates, native adapter
files, dependency/container inputs, existing plans and existing review records.
New fixture and report files are not counted as existing preserved blobs.

All **418 original test methods** remain present, and every original assertion
AST remains intact and in order. Total methods are **441**, adding 23 cases.
Five original method bodies gained fixture preparation or additional observed
previous-main consumer coverage:

- `DependencyIntegrationTests.test_source_layout_resolves_dependency_policy_and_container_inputs`
- `NavigationTests.test_source_core_and_existing_project_facts_are_required`
- `NavigationCopierIntegrationTests.test_source_cli_binds_existing_project_facts`
- `QualityFrameworkTests.test_real_current_source_catalog_is_checked_without_project_profile`
- `WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable`

This is method/assertion retention, not a claim that all original test-file bytes
are unchanged. The previous-main consumer test measures and runs the actual old
consumer before adding its observed identity; the allowlist is not the source of
its expected fingerprint. Negative authority, project-fact, inactive-module,
dependency, historical-copy and clone regression coverage ran in the full suite.

## Run artifacts and limits

Raw logs remain ignored under `artifacts/layout-compatibility-quality/final/`.

| Artifact | SHA256 |
| --- | --- |
| `full-suite.log` | `344c6703fdbe879e87b81192530ded48bc61e49cc4f23d8ca12a2db3a54cd207` |
| `commands.json` | `aea737ecdb86a3a246749891dd2074d16cac2373c7da75d6fd0dbc8d0e774192` |
| `preservation.json` | `5760a14a6922a4fcd51e9de7f65e9880857b10e79e81a97f3aeb01a714967718` |

`commands.json` records exact interpreter/executable paths, arguments, exit codes,
durations and hashes for the 14 non-suite commands. Transition input identities
and full before/after inventories are recorded alongside it. Initial failed-run
artifacts remain separate in the parent artifact directory and are identified in
the failed-run record.

Docker and Podman are unavailable locally. This checker did not execute actual
bridge-specific containers, native Linux/Windows clients, model sessions or
native Copilot loading. Prior PR 18 CI results do not certify this bridge head;
any remote bridge results must identify their own exact commit. Formal Full
reviews and subsequent triage/Delta review remain separate from these checks.

The committed whitespace check above binds **only the tested head `aaa74e3…`**.
After report/review commits, publication must repeat the committed base-to-final
head diff check. The source/test freeze and passing suite do not automatically
certify later source changes.
