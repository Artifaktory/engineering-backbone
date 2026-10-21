# Independent deterministic checks

Checker: separate read-only session `testing_quality`. Actual trusted base `1a740604d4a6a68e500da36c4d99935d04a8ce86`; frozen implementation `daa85bfd64467da798c57cef2894292c646e2750`. Base-to-head binary patch SHA-256 `c0f1cb18497072a46abe767fae67211d9db3f4543b0f26d1776b1cde9f3b0756`.

Environment: Linux, existing hash-locked isolated Python 3.12.14. `PY` denotes that interpreter; `BASE` is the separate immutable merged-base checkout and `CANDIDATE` the frozen candidate. Raw logs remain ignored local artifacts; this redacted report preserves execution and scope.

| Check | Actual command | Exit | Seconds |
| --- | --- | --- | --- |
| candidate-validator | `PY .engineering-backbone/src/validate.py` | 0 | 1.277 |
| compiler-toolchain_fingerprint | `PY .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | 1.679 |
| compiler-workflow_kit | `PY .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | 0.057 |
| compiler-navigation | `PY .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | 0.087 |
| compiler-quality_framework | `PY .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | 0.1 |
| source-dependencies | `PY .engineering-backbone/src/check_source_dependencies.py` | 0 | 0.393 |
| trusted-base-validator | `PY BASE/.engineering-backbone/src/validate.py --root CANDIDATE --trusted-base BASE` | 0 | 1.191 |
| committed-whitespace | `git diff --check 1a740604d4a6a68e500da36c4d99935d04a8ce86 daa85bfd64467da798c57cef2894292c646e2750` | 0 | 0.01 |
| protected-paths | `git diff --exit-code 1a740604d4a6a68e500da36c4d99935d04a8ce86 daa85bfd64467da798c57cef2894292c646e2750 -- .engineering-backbone/src .engineering-backbone/schemas .engineering-backbone/standards .engineering-backbone/tst/fixtures .github/workflows .engineering-backbone/requirements.txt .engineering-backbone/requirements.lock infra/docker/engineering-backbone/Dockerfile docs/changes/backbone-architecture-contract docs/changes/backbone-bootstrap docs/changes/backbone-ci-clone-repair docs/changes/backbone-codex-consolidation docs/changes/backbone-codex-security docs/changes/backbone-copilot-development docs/changes/backbone-dependency-compatibility docs/changes/backbone-layout-compatibility docs/changes/backbone-layout-corrections docs/changes/backbone-layout-integration docs/changes/backbone-layout docs/changes/backbone-opencode-governance docs/changes/backbone-planning-delivery docs/changes/backbone-quality-framework docs/changes/backbone-technology-navigation docs/changes/backbone-workflow-kit` | 0 | 0.003 |
| python-version | `PY --version` | 0 | 0.002 |

The trusted-base command executed the actual base-owned validator from the separate checkout. Candidate validation is a distinct result. Protected runtime, schemas, catalogs, workflow YAML, dependency/container inputs, fixtures and previous delivery records remain unchanged. The rendered tooling digest remains `85519f27019364daf5ef22cc06ddc333811e5d5f0bc8fe3d98f77cd6c13ce152`; no fingerprint regeneration or predecessor-authority change was needed.

## Focused distribution and repaired diagnostic

The test author executed the five new real distribution tests: initial run 4 passes/1 failure, exit 1, 23.600 seconds. Independent TEST-CHECK-01 triage confirmed a test-only diagnostic expectation defect. The authorized minimal correction then passed the affected case (one test, exit 0, 3.831 seconds; wrapper 4.290) and all five tests (exit 0, 25.617 seconds; wrapper 25.938). Initial and repaired results are separate; see [check triage](check-triage.md). These runs belong to `testing_distribution_tests`, not the independent checker.

## Historical-consumer context repair

The earlier independent full run on `47cec1a72dbed195cbeb3534f83a80696061e2ff`
was stopped after confirmed fixture failures and is explicitly incomplete. The
bounded one-test reproduction failed, exit 1, 3.401 seconds (wrapper 3.874). Separate
TEST-CHECK-02 triage identified missing transitive managed document context in a
selective historical-consumer fixture; runtime/schema/workflow code was unchanged.
The tracked minimal repair adds only that context and an explicit historical-core
preservation assertion. Root's seven-test module preflight then passed, exit 0,
7.181 seconds. Initial, TEMP-only triage and repaired author-side results remain
distinct from the final independent execution below; see [check triage](check-triage.md).

## Full suite

```sh
PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
```

**PASS: 487 tests, no failures/errors/skips, exit 0; 658.503 seconds unittest time,
659.177 seconds wrapper time.** The independent checker reconfirmed the immutable
head, base-to-head patch hash and clean tracked state after execution.

The full run includes all five new source/rendered copy/update/missing-context/
closed-boundary tests and all seven historical quality-workflow tests. Both
TEST-CHECK repairs are covered inside this final complete run. Old-validator
acceptance, current authority rejection, poisoned candidate-guard nonexecution,
eight historical tooling identities and historical core preservation all remain
checked. Existing clean-clone, autocrlf, unknown/mixed tooling and direct-copy
regressions also passed. No test was skipped to obtain this result.

A native-smoke success line in the log comes from a unit-test fixture; it is not a
live provider or native Windows execution.

## Limits and later evidence

No native Windows, Docker/container, live provider or remote CI execution is established by these local checks. Unit fixtures that exercise a native-smoke harness do not establish a live native/provider run. This delivery changes no runtime/container/native adapter and does not simulate those claims. Required remote source checks and observed job statuses belong in publication readback.

Later commits limited to this delivery's evidence/acceptance records require candidate and actual base-owned validation plus final committed base-to-published-head whitespace checks. They do not retrospectively enter the earlier implementation Full subject.
