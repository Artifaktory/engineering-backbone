# BB-LAYOUT-013 deterministic-check failure triage

Date: 2026-10-20. Session: `correction_triage`, acting only as independent finding
triage. This is a separate delivery from BB-LAYOUT-012. This record does not supply
Full-review approval or authorize publication while required checks fail.

## Frozen subject

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Candidate: `785d4d51dec3ff8f26bf2a4322b3ffe9422ef7ff`.
- Tree: `7408b74288ec66a2e14bca77697917e5aeb3f075`.
- Binary base-to-candidate patch SHA256:
  `00274fd3e015d78c923b8c9001c187ceb25d4c38d935e0ac8750f4e0a522eaf9`.

The triage session independently resolved these identities, read the canonical
policy, reviewed plan/packet and plan review, and inspected the affected compiler,
resolver and test setup. Only this report is written by triage. The quality
checker's first complete 441-test suite finished at this frozen candidate with
exit **1**, **441 tests in 462.650 seconds**, **13 failures**. Its complete final
tracebacks were read and classified below. Subsequent implementer repairs are
outside that tested snapshot and require separately recorded verification.

## Confirmed findings

### LC-CHECK-01 — incomplete OpenCode helper call migration

**Confirmed; P2; runtime compatibility; high confidence.**

Location: `scripts/navigation.py:599-600`, with generated copies in the quality
guard, validator and workflow. The current diff changes `opencode_paths` from
`(role, native)` to `(folder, role, native)` but leaves the two inactive-to-active
seed-comparison calls using the old signature. A valid reviewed inactive OpenCode
package activated with only the enabled flag changed reaches these calls and
returns an error for missing `native`, preventing the existing valid consumer
transition. The guard fails closed; this is a compatibility regression, not
evidence of unauthorized activation succeeding.

Independent reproduction on the frozen candidate:
`tests.test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_inheritance_and_package_removal`
fails at its unchanged positive assertion on line 101 with
`opencode_paths() missing 1 required positional argument: 'native'`.
This directly violates the preserved consumer/activation contract and AC-5.

Minimal repair: pass `trusted_base` to the reviewed seed call and `root` to the
candidate call, retaining all path-set and exact-byte comparisons. Regenerate
the maintained compiled outputs and toolchain fingerprint. Do not catch-and-pass
the error, alter activation requirements or change the existing assertions.
Recheck the complete OpenCode navigation module, generated entrypoints and
required compiler checks before the final complete suite.

### LC-CHECK-02 — compiler fixture omits new reviewed input

**Confirmed; P2; integration fixture compatibility; high confidence.**

Location: `tests/test_navigation_integration.py:58-67`. The existing partial
source fixture copies standards and four generated/runtime outputs but omits
the newly required canonical `scripts/source_layout.py` input. The changed
`compile_navigation.py:160` correctly reads that input; the fixture fails before
its unchanged deterministic-compilation and candidate-module isolation assertions
can exercise their contracts.

Independent reproduction on the frozen candidate:
`tests.test_navigation_integration.NavigationCompilerIntegrationTests.test_compilation_and_all_guards_ignore_candidate_module_side_effects`
fails at line 124 with `No such file or directory` for the fixture's
`source/scripts/source_layout.py`. This is a missing fixture setup dependency,
not a reason to add a compiler fallback or import candidate Python.

Minimal repair: copy the reviewed helper into this fixture separately from
`COMPILER_FILES`, whose existing tests intentionally require every listed output
to contain the mutated technology authority. Also provide the complete canonical
old-layout policy inputs required when the same fixture is checked with
`source=True`; preserve the strict source resolver and every original assertion.
Recheck both `NavigationCompilerIntegrationTests` methods, including their
side-effect marker and poisoned-authority rejection assertions. This disposition
is within the approved fixture-setup scope and AC-5 retention requirement.

### LC-CHECK-03 — source CLI fixture retains conflicting consumer authority

**Confirmed; P2; integration fixture compatibility; high confidence.**

Location: `tests/test_navigation_integration.py:450-466`. This fixture copies
old-source policy files over an installed consumer but retains its
`.engineering-backbone/core.json` and does not install `policy/dependencies.md`.
The newly explicit source resolver therefore correctly rejects the synthetic
fixture as ambiguous before its existing source-project-fact assertions execute.
Removing ambiguity without completing the four canonical policy inputs would
still leave the fixture invalid.

Independent reproduction on the frozen candidate:
`tests.test_navigation_integration.NavigationCopierIntegrationTests.test_source_cli_binds_existing_project_facts`
fails at its unchanged positive assertion on line 480 with
`Quality framework: Source layout: ambiguous canonical policy authority`.
The isolated single-test run exits **1**, **1 test in 1.269 seconds**.

Minimal repair: complete the fixture's intended old-source conversion before the
existing assertions, removing the leftover consumer canonical JSON after its
source copy and providing the reviewed dependency-policy input. Keep all original
source path, project-byte, stale-receipt and schema assertions unchanged. This is
fixture correction under AC-5, not permission to accept mixed canonical source
authorities or to weaken the resolver.

The final suite exposes the same leftover consumer canonical JSON in
`tests/test_dependency_integration.py:208-228`, specifically
`test_source_layout_resolves_dependency_policy_and_container_inputs`. Its
unchanged assertion fails with the same ambiguous-authority diagnostic. That
fixture already installs `policy/dependencies.md`; only its stale canonical
consumer JSON needs removal after copying the source policy. Retain its actual
dependency/container receipt assertions.

### LC-CHECK-04 — newly approved previous-main identity lacks observed fixture evidence

**Confirmed; P2; historical compatibility test data; high confidence.**

Location: `tests/test_workflows.py:353-381`. The approved prerequisite retains the
former current rendered toolchain fingerprint
`35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`
in the previous allowlist. Independent reading of the workflow at actual base
`212608aa50ee517b3dd3107a9480da997222fd4f` confirms that exact prior current value.
The existing test's observed rendered historical fixtures and static expected
identities do not yet include this newly previous version. Its exact allowset
assertion therefore reports this one additional item. The clean single-commit and
autocrlf clone checks repeat the same failure, accounting for three suite failures.

The implementation's preservation of the approved prior identity is intentional
and required by the plan. Removing it to satisfy the old expectation would break
the transition contract. Broadening the assertion without actual fixture evidence
would not establish compatibility.

Minimal repair: reuse the new immutable old-main source fixture only after its
pinned Git tree/blob/archive verification; render its actual consumer, verify the
computed rendered digest against the explicit reviewed literal above, and execute
the real trusted consumer validation before appending that observed digest. Keep
the original exact-set assertion, all prior assertions and historical fixture
bytes unchanged. Do not derive expected authority from the candidate workflow's
allowlist. Recheck the historical test and both clone variants to prove the added
evidence works without original Git history and with autocrlf.

## Complete failure disposition and required rechecks

The LC-CHECK-01 and LC-CHECK-02 methods ran together under the existing isolated Python 3.12
environment using `python -m unittest ... -v`: exit **1**, **2 tests in 0.219
seconds**, both failing with the exact causes recorded above. These are
independent diagnostic reproductions, not a repeat or result of the full suite.
No source/test repair was made by triage.

All 13 final suite failures have a confirmed disposition:

| Finding | Failure coverage |
| --- | --- |
| LC-CHECK-01 | Six failure records: four OpenCode navigation activation methods, including the two instruction-path subtests, plus the compiled workflow activation test. |
| LC-CHECK-02 | Both navigation compiler integration methods. |
| LC-CHECK-03 | Source CLI project facts and source dependency/container receipt integration methods. |
| LC-CHECK-04 | Direct historical allowset test and its clean single-commit/autocrlf clone checks. |

Nested clone output repeats the underlying historical traceback; it does not
introduce another cause. The final full-suite log SHA256 is
`71753fee77b76ec77bfa58be86b58dd13ce32130b4b1ae881889e0f59c9a052c`.
Raw output remains an ignored run artifact; the quality checker records the
complete command/result separately. No additional unexplained failure remains
in this run. This classifies the failures; it does not mark their repairs passed.

Implementers may repair only these confirmed causes. Required affected checks,
compiler synchronization, original assertion/fixture retention, actual transition
checks and the full suite must run on a newly identified repaired snapshot before
the two independent Full reviews. No failing test, assertion, authority check or
gate may be removed. Neither these findings nor successful local transition
checks establish PR 18's eventual trusted-main acceptance or authorize either
PR's merge.
