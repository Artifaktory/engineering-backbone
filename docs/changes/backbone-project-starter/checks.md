# Independent deterministic checks

Independent checker: `starter_quality`. Actual base `4e74c7e5f3a07430768f670c4271c1e1a0e28f68`; frozen head `f0230d0da90b17ef52932ff027529acd23d73f51`, tree `ff9d9c860682c3ed8531a9b085f9ee75678c725d`. Base-to-head binary patch SHA-256 `ba6eeafe17d91ca46c3b8b695e7e18f4372703d1419712b4d6c9654b865e7f34`. Linux; existing hash-locked Python 3.12.14. No tracked edits or repairs.

`PY` denotes the existing isolated interpreter; `BASE` the separate actual merged-base checkout and `CANDIDATE` the frozen quality checkout. All commands ran in CANDIDATE except the actual base-owned validator, which ran from BASE. Raw command arrays/cwds/timestamps/log hashes remain in ignored `artifacts/starter-quality/` in that checkout.

| Check | Actual command | Exit | Seconds |
| --- | --- | --- | --- |
| candidate-validator | `PY .engineering-backbone/src/validate.py` | 0 | 1.071 |
| trusted-base-validator | `PY BASE/.engineering-backbone/src/validate.py --root CANDIDATE --trusted-base BASE` | 0 | 1.098 |
| source-dependencies | `PY .engineering-backbone/src/check_source_dependencies.py` | 0 | 0.347 |
| committed-whitespace | `git diff --check 4e74c7e5f3a07430768f670c4271c1e1a0e28f68 f0230d0da90b17ef52932ff027529acd23d73f51` | 0 | 0.007 |
| repair-whitespace | `git diff --check 00b758e2f30f85d3c05930d5a08ec21403bb3f75 f0230d0da90b17ef52932ff027529acd23d73f51` | 0 | 0.004 |
| protected-paths | `git diff --exit-code BASE HEAD -- PROTECTED_PATHS (listed below)` | 0 | 0.004 |
| python-version | `PY --version` | 0 | 0.002 |
| compiler-toolchain_fingerprint | `PY .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | 1.177 |
| compiler-workflow_kit | `PY .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | 0.049 |
| compiler-navigation | `PY .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | 0.083 |
| compiler-quality_framework | `PY .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | 0.09 |

The actual base validator was executed from its own separate checkout, with `--trusted-base`; it was not substituted by candidate code. The four compilers remained in check mode. Existing rendered-tooling fingerprint authority remains unchanged.

## Complete suite

```sh
PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
```

**PASS: 521 tests; zero failures, errors or skips; exit 0; 683.786 seconds unittest / 684.566 seconds wrapper.**

Full-log SHA-256 `c9d075b39e8255a9a5454880f6fc3ca1d155d22d7f78a889993d3e4bbf051d41`. The checker independently recomputed all sixteen referenced quick/full/supplement log hashes; all matched. Final HEAD/tree/base patch and clean tracked state were reconfirmed.

The complete run includes all 34 new tests: twelve environment, eleven doctor/example and eleven export cases. Coverage includes actual fresh export/verification, managed/native/provenance tampering, product/governance JSON separation, unsafe destination/link refusal, read-only update/conflict/ownership/removal behavior, real autocrlf checkouts and both poisoned helper-cache nonexecution/no-write regressions. Existing source/legacy copy/update and policy-authority tests passed.

## Supplemental observations and limits

- Actual empty source environment register and explicitly selected `.env.example`: exit 0, zero declared variables; no application credential-readiness claim.
- Actual development doctor: exit 0.
- Actual source-linux doctor: exit 1, Docker CLI/daemon missing here. This remains an operational prerequisite gap, not a passing container or runner check.
- No native Windows, Docker image, live provider, runner registration/access/isolation or remote CI result is established. A native-smoke success line in the suite is a unit fixture.

Author-side initial failures and repairs remain separate in [implementation](implementation.md) and [check triage](check-triage.md). The initial exporter run was 9/10, exit 1; the repaired author suite was 11/11, exit 0. Only the complete independent result above qualifies this frozen implementation. The early concurrent missing-guide links were incomplete construction, not final quality.

## Protected paths

The exact existing runtime/native/schema/catalog/legacy/fixture/workflow/dependency/container and previous-delivery path arguments below were unchanged. New starter/environment helpers, new tests and new kit records are separate additions.

```text
.engineering-backbone/src/check_source_dependencies.py
.engineering-backbone/src/maintenance/compile_navigation.py
.engineering-backbone/src/maintenance/compile_quality_framework.py
.engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py
.engineering-backbone/src/maintenance/compile_workflow_kit.py
.engineering-backbone/src/navigation.py
.engineering-backbone/src/opencode_native_smoke.py
.engineering-backbone/src/quality_framework.py
.engineering-backbone/src/source_layout.py
.engineering-backbone/src/validate.py
.engineering-backbone/src/workflow_kit.py
.engineering-backbone/schemas
.engineering-backbone/standards
.engineering-backbone/legacy
.engineering-backbone/tst/fixtures
.github
.codex
.opencode
opencode.json
.gitattributes
copier.yml
.engineering-backbone/core.json
.engineering-backbone/project.json
.engineering-backbone/opencode.json
.engineering-backbone/requirements.txt
.engineering-backbone/requirements.lock
infra/docker/engineering-backbone/Dockerfile
docs/changes/backbone-architecture-contract
docs/changes/backbone-bootstrap
docs/changes/backbone-ci-clone-repair
docs/changes/backbone-codex-consolidation
docs/changes/backbone-codex-security
docs/changes/backbone-copilot-development
docs/changes/backbone-dependency-compatibility
docs/changes/backbone-layout-compatibility
docs/changes/backbone-layout-corrections
docs/changes/backbone-layout-integration
docs/changes/backbone-layout
docs/changes/backbone-opencode-governance
docs/changes/backbone-planning-delivery
docs/changes/backbone-quality-framework
docs/changes/backbone-technology-navigation
docs/changes/backbone-testing-ci-contract
docs/changes/backbone-workflow-kit
```

## Later evidence and publication

Later evidence-only commits require candidate and actual base-owned validation and committed base/head plus repair-range whitespace checks again. They do not retrospectively become part of this implementation Full subject. Exact published tree/parent/patch correspondence and actual PR/remote job status belong in publication readback. Required unavailable CI/native/hosting evidence remains visible; no waiver or merge/release approval is inferred.
