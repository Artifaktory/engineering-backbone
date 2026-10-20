# BB-LAYOUT-014 test implementation

Test implementer delivery on 2026-10-20, after the approved plan review. This is
implementation evidence, not independent quality or Full review. Work was confined
to the moved tests, their new immutable fixture and this report; no commit was
created by the test implementer.

## Integration and retained contracts

Resolved test conflicts using PR18's new paths and PR19's strict source fixture
requirements. New-source fixtures retain `.engineering-backbone/core.json` and
provide the complete canonical prose policies. Compiler fixtures copy the moved
resolver separately from the generated-output list. The unit validator fixture
now includes the independently verified 88 historical records and minimal ordinary
reference targets; the exact source transition fixtures remain unmodified trees.

All 433 PR18 test methods and their 1,120 original assertion ASTs remain unchanged
from `f1c1410cff6407109f286173f1ecc980cd2a14b7`. PR19's 23 transition methods remain,
with execution/fixture paths adapted to their new location. Its prior-main-to-old-
bridge positive now targets the frozen actual merged-main snapshot because the
working repository has the new layout. The original positive assertion remains a
real subprocess validation; no path projection or candidate executable fallback
was added. The current main validator also validates the integrated candidate.

The historical workflow test retains real rendering of `212608...`, independently
measures the fixed `35678afb...` identity, and adds actual merged main with the
fixed `a9355b8...` identity. Both real rendered consumers run through the current
trusted workflow before their measured digests enter the existing exact-set
assertion. PR18's real Copier `git+file://` transport repair and nested Copilot
selector assertions remain intact.

## Immutable input identities

The incoming original manifest and both ZIPs are byte-identical to merged main:

| File | SHA256 |
| --- | --- |
| `manifest.json` | `f60ff52c76a640c0ca180a18fb2fc9350c37f1b1862365c7c6075ac9e59c14d8` |
| `old-source.zip` | `bae53791b381301b52a072bc474816db4337251da1650af8e80bc44b9a12c421` |
| `pr18-source.zip` | `59a9f43073125650c6cace730946415e72b3ee6ff781ae8ebb79debc1d8daecc` |

The additional `merged-main.zip` and separate `merged-main.manifest.json` bind
actual main commit `537576f658bbd79c3bc49b26ade948116c664943`, tree
`10f7147ce5f4c2438cf4e016598a3a05be2c71f8`, and all 511 tracked regular files.
Archive SHA256 is
`7ba99d70d4a345623bbb30e95e632fceb904927688953dd0a031b7dea92e5a9f`.
The fixture verifier checks archive hashes, every Git blob/hash/mode, exact path
sets and reconstructed Git tree before extraction or trusted-main execution.
CI does not require those original Git objects or network access.

## Added regression coverage

INT-ARCHIVE-01 has candidate-validator rejection cases for deleting a required
record while forging its candidate map, removing the archive parent, and replacing
its file or ancestor with a symlink. Intact frozen history still passes. The actual
main positive transition is separate evidence: main's known deletion blind spot
does not prove the candidate repair.

INT-ARCHIVE-02 uses a new real Git seed and fresh checkout with repository-local
`core.autocrlf=true`; it verifies all 88 archived hashes, LF bytes, every nested
historical fixture byte, applicable attributes, and successful source validation.
It changes no global Git settings or original fixture attributes.

## Targeted execution

Python: unchanged locked environment `backbone-venv/bin/python`, Python 3.12.
Commands ran from the repository with `PYTHONPATH=.engineering-backbone`.

- `python -m unittest tst.test_source_layout_compatibility tst.test_validation tst.test_navigation_integration.NavigationCompilerIntegrationTests tst.test_navigation_integration.NavigationCopierIntegrationTests.test_source_cli_binds_existing_project_facts tst.test_dependency_integration.DependencyIntegrationTests.test_source_layout_resolves_dependency_policy_and_container_inputs tst.test_reference_layout.ReferenceCheckoutTests -v`: 83 tests, 102.241 seconds, exit 1. All 82 other cases passed; the checkout case verified its archive/attribute assertions, then exposed transient task status `in_progress`, rejected by the schema. Root corrected this separately triaged INT-CHECK-01 input to `active`; no runtime or assertion was changed for that failure. Failed log retained at `/tmp/backbone-integration-targeted-tests.log`.
- `python -m unittest tst.test_reference_layout.ReferenceCheckoutTests -v` after the corrected task input: 1 test, 2.558 seconds, exit 0. Log: `/tmp/backbone-integration-checkout-recheck.log`.
- `python -m unittest tst.test_navigation tst.test_quality_framework tst.test_opencode_validation tst.test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable tst.test_workflows.WorkflowTests.test_real_copier_upgrade_without_local_object_copy tst.test_workflows.WorkflowTests.test_historical_compatibility_survives_clean_single_commit_clone tst.test_workflows.WorkflowTests.test_historical_compatibility_survives_autocrlf_source_checkout -v`: 82 tests, 75.014 seconds, exit 0. Log: `/tmp/backbone-integration-guard-workflow-tests.log`.
- `git diff --check --cached -- .engineering-backbone/tst`: exit 0.

These are targeted working-tree results. The coordinator must freeze the resulting
merge and obtain independent complete-suite, compiler, dependency, remote-runtime
and Full-review evidence before readiness or publication claims.
