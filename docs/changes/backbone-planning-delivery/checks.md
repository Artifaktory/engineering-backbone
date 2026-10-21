# Independent deterministic checks

Checker: separate agent `planning_quality`, read-only. Trusted base `4394763d03c1d1302b6b37cef142d0f98f848be4`; frozen candidate `6a1089aa148fabbf7c5a223a9055f2dd7b187878`. Base-to-head binary patch SHA-256 `746882d44bee3159bc83dfca1fee3a5d07e399f3ecd521a8fa791c73908d2798`.

Environment: Linux; locked isolated Python 3.12.14. `PY` below denotes that interpreter, `BASE` the separate immutable merged-base checkout, and `CANDIDATE` the frozen candidate checkout. Raw logs are local ignored artifacts; this redacted record preserves commands, results and limitations.

| Check | Command | Exit | Seconds |
| --- | --- | --- | --- |
| candidate-validator | `PY .engineering-backbone/src/validate.py` | 0 | 0.969 |
| compiler-toolchain_fingerprint | `PY .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | 1.319 |
| compiler-workflow_kit | `PY .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | 0.063 |
| compiler-navigation | `PY .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | 0.087 |
| compiler-quality_framework | `PY .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | 0.103 |
| source-dependencies | `PY .engineering-backbone/src/check_source_dependencies.py` | 0 | 0.381 |
| trusted-base-validator | `PY BASE/.engineering-backbone/src/validate.py --root CANDIDATE --trusted-base BASE` | 0 | 1.019 |
| committed-whitespace | `git diff --check 4394763d03c1d1302b6b37cef142d0f98f848be4 6a1089aa148fabbf7c5a223a9055f2dd7b187878` | 0 | 0.017 |
| protected-paths | `git diff --exit-code 4394763d03c1d1302b6b37cef142d0f98f848be4 6a1089aa148fabbf7c5a223a9055f2dd7b187878 -- .engineering-backbone/schemas .engineering-backbone/tst/fixtures .engineering-backbone/standards docs/changes/backbone-architecture-contract` | 0 | 0.004 |
| python-version | `PY --version` | 0 | 0.004 |

The actual base-owned validator ran from the trusted-base checkout. Candidate validation is recorded separately. Protected schemas, standards/catalogs, historical fixtures and the prior architecture delivery were unchanged.

## CHECK-01 regression

The explicitly pinned predecessor expectation repair passes the previously failing historical-copy test: one test, exit 0, 6.751 seconds unittest time (7.147 seconds wrapper time). See [the failed-run triage](check-triage.md) for the preserved earlier failure and incomplete run.

## Complete suite

```sh
PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
```

**PASS: 482 tests, exit 0; 629.312 seconds unittest time, 630.005 seconds wrapper time.**
The complete run covers source/rendered product-governance boundaries, malformed
managed records, five planning copy/update/context checks, all 152 preservation
entries in a real autocrlf checkout, portable path formatting, source-CI guards,
actual workflow payloads, unknown/mixed-toolchain rejection and historical clean
single-commit/autocrlf callers. The repaired predecessor assertion also passes
inside this complete run. No test was skipped to obtain this result.

A native-smoke success line in this unittest log comes from test-harness fixtures.
It is not evidence of a live provider, real Windows host or remote CI run.

## Actual predecessor upgrade

The checker freshly rendered actual merged base `4394763d03c1d1302b6b37cef142d0f98f848be4` and implementation `729531ef541720058c1984e925886dc538e7b77b`, then executed the unchanged candidate workflow shell payload against the resulting consumer. Exit 0, 2.388 seconds. Previous tooling digest: `94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`; current: `85519f27019364daf5ef22cc06ddc333811e5d5f0bc8fe3d98f77cd6c13ce152`. The checker verified source tooling and workflows are byte-identical between that snapshot and the repaired candidate. This is inherited evidence for the unchanged payload, not a claim of a fresh runtime execution on the repaired commit.

## Limits and publication checks

No native Windows, Docker image/smoke, live OpenCode/provider or GitHub runner execution was established by this local run. Real autocrlf checkouts and portable-path tests exercise their named conditions on Linux; they are not native Windows certification. Remote CI availability and results belong in the publication record. Missing required runtime/CI evidence remains a merge gate, not a waiver.

Later evidence-only commits require candidate/base-owned validation and the actual final base-to-head committed whitespace check again. Full implementation reviews bind the frozen implementation above; later reports must not claim they reviewed themselves.
