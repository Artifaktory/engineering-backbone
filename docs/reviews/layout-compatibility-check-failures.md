# BB-LAYOUT-013 initial deterministic check failures

Quality-checker session: `layout_quality`, separate from implementation and triage.
Date: 2026-10-20. This is failed-run evidence, not approval or a passing gate.

## Snapshot and result

- Actual old-main base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Initial tested bridge head: `785d4d51dec3ff8f26bf2a4322b3ffe9422ef7ff`.
- Initial tested tree: `7408b74288ec66a2e14bca77697917e5aeb3f075`.
- Binary patch SHA256: `00274fd3e015d78c923b8c9001c187ceb25d4c38d935e0ac8750f4e0a522eaf9`.

Executed in isolated Python 3.12.14 from the bridge repository root:

```sh
python -m unittest discover -s tests -v
```

**Exit 1: 441 tests in 462.650 seconds, FAILED (failures=13).** No test error or
skip was reported. The count includes two instruction-list subtest failures;
nested clone output repeats its underlying failure but is not an extra top-level
failure. The full run completed once; no source/test repair was made by this
quality-checker session. Formal Full review must wait for triage, repairs and
passing deterministic evidence.

The initial source inventory contained 503 files. An independent triage evidence
document was added during execution. After completion, implementers began repair
writes before the final file-hash collection; their first observed source writes
were 41 seconds after the completed log's last write. Therefore this report does
not claim an unchanged post-run worktree or that later repaired source passed this
run. Final repair checks require their own frozen snapshot.

## Complete top-level failure inventory

| Test identifier | Failures | Observed traceback result |
| --- | ---: | --- |
| `test_dependency_integration.DependencyIntegrationTests.test_source_layout_resolves_dependency_policy_and_container_inputs` | 1 | `Source layout: ambiguous canonical policy authority` during a positive source-fixture resolution. |
| `test_navigation_integration.NavigationCompilerIntegrationTests.test_catalog_refresh_propagates_through_both_compilers_deterministically` | 1 | Compiler fixture lacks `scripts/source_layout.py`. |
| `test_navigation_integration.NavigationCompilerIntegrationTests.test_compilation_and_all_guards_ignore_candidate_module_side_effects` | 1 | Compiler fixture lacks `scripts/source_layout.py`. |
| `test_navigation_integration.NavigationCopierIntegrationTests.test_source_cli_binds_existing_project_facts` | 1 | `Source layout: ambiguous canonical policy authority` during a positive source-fixture resolution. |
| `test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_binds_every_reviewed_package_input` | 1 | `opencode_paths()` missing required positional argument `native`. |
| `test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_inheritance_and_package_removal` | 1 | Same missing `native` argument. |
| `test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_rejects_added_or_removed_instruction_paths` | 2 | Both changed-instruction subtests encounter the missing `native` argument before the intended rejection message. |
| `test_opencode_navigation.OpenCodeNavigationTests.test_opencode_seed_preparation_active_updates_and_unrelated_activation_edits_remain_valid` | 1 | Same missing `native` argument. |
| `test_opencode_workflow_guard.OpenCodeActivationWorkflowTests.test_compiled_workflow_binds_activation_before_approved_old_validator` | 1 | Compiled workflow guard reports the same missing `native` argument. |
| `test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable` | 1 | Expected historical fingerprint-set comparison does not account for former current identity `35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`. |
| `test_workflows.WorkflowTests.test_historical_compatibility_survives_autocrlf_source_checkout` | 1 | Nested clone reproduces the same historical fingerprint-set failure. |
| `test_workflows.WorkflowTests.test_historical_compatibility_survives_clean_single_commit_clone` | 1 | Nested clone reproduces the same historical fingerprint-set failure. |

The table reports observations, not permission to alter tests or weaken checks.
Independent classification and bounded repair instructions belong to
[the check triage](layout-compatibility-check-triage.md).

## Checks that passed on the initial bridge

The following individual commands returned exit 0, despite the failed full suite:

- `python scripts/validate.py` (without a trusted-base argument).
- All four `python scripts/compile_*.py --check` commands: navigation, quality
  framework, workflow kit and toolchain fingerprint.
- `python scripts/check_source_dependencies.py`: all 26 locked installed versions
  and tracked dependency inputs were consistent.
- Actionlint 1.7.12 with `-shellcheck= -pyflakes=`; optional analyzers unexecuted.
- Working and staged `git diff --check`, and committed
  `git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f 785d4d51dec3ff8f26bf2a4322b3ffe9422ef7ff`.
- The actual old-main validator against the old-layout bridge, supplying the actual
  old-main checkout as `--trusted-base`.
- The bridge-owned validator against the exact frozen PR 18 `c501087…` checkout,
  supplying the actual old-main checkout as `--trusted-base`.
- The bridge-owned validator against its own old-layout source with that old base.

The quality checker independently verified every actual file blob of both
transition inputs: **495** old-main files at tree
`c31ee9b6e418325936b59e31cd7e9b9865ed0064`, and **542** PR 18 files at
`c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`, tree
`af532155a9f1196aa65e553b24b957f5f50297a3`. No path projection, candidate-validator
execution or waived exit code was used.

A supplementary transition used the actually published corrected PR 18 head
`2ddfa803688c70b556dc83bcf07a4c3911713be5`, tree
`ae42d5f1848b65509e51813b824b7d9c2b61a6cc`. All **551** file blobs matched that Git
snapshot. The same bridge-owned validator checked it against the actual old base
and returned exit **0**. This is local transition evidence, not a merge of the
prerequisite or proof that PR 18 already has a compatible trusted `main`.

## Preservation audit and limits

Before repairs, all **418** original test methods were present. Every original
top-level test statement and assertion AST remained intact and ordered; two test
methods had additive fixture preparation. Total methods present: **441**.
**413** existing protected Git blobs were byte-identical to the base, including
all **59** existing fixture blobs, core policy/invariants, schemas, standards,
dependency/container inputs, native adapter files, legacy templates and existing
plans/review records. Three fixture-construction helpers/contexts had bounded
changes; this audit does not claim every test-file byte was unchanged.

The full-suite failure log SHA256 is
`71753fee77b76ec77bfa58be86b58dd13ce32130b4b1ae881889e0f59c9a052c`.
Individual command-result record SHA256:
`dfe78883d178ce5b04136bf2861ca75f749b1423a22cfe91398dfed8224b4fc7`.
Preservation audit SHA256:
`0985de0338a95e368c0bd4f0d40e34af678a78fbc1437d8b52ec0c126b4e4873`.
Raw logs remain ignored run artifacts.

Docker/Podman are unavailable locally. No bridge-specific container or actual
native Linux/Windows execution was performed by this checker. Previous PR 18 CI
results do not certify this bridge head. Failed full-suite evidence remains
visible and cannot be replaced by the passing structural/transition checks above.
