# BB-ARCH-015 independent deterministic checks

- Checker: `/root/architecture_quality`, separate quality session; no implementation or repair role.
- Date: 2026-10-20.
- Base: `ae317bf30576914d4ed53856be4ae496c6ed64b3`.
- Frozen head: `1dbd1d68a7a23b8b38f532ed7a9dff8488642a57`.
- Patch SHA-256 (`git diff --binary BASE HEAD`): `2bf0734cc6d4a719f21329a2086232440ed03aba8ea2949066c10adf9acb2a2a`.
- Candidate worktree: `/workspace/scratch/6e019b0851cc/backbone-architecture-quality`.
- Actual trusted-base worktree: `/workspace/scratch/6e019b0851cc/backbone-architecture-trusted`.
- Interpreter: `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python` (Python 3.12.14).
- Required context read: AGENTS, core policy, CONTRIBUTING, BB-ARCH-015 Task Packet and approved plan, architecture contract, quality policy and testing guide. No nested AGENTS files apply. The source has no active navigation seed.

## Result

FAIL / required review gate blocked: complete suite ran 465 tests in 617.400 seconds with result `FAILED (failures=5)` (process exit 1). Four targeted architecture-distribution tests, candidate and actual trusted-base checks, compiler freshness, source dependencies and committed-patch whitespace passed. The complete suite exposes one common compatibility defect across five failure events; no repair or retry was performed.

Independent triage and confirmed repair are required before qualifying a repaired snapshot. Formal Full review remains blocked on the required suite. Publication/hosted CI and human merge/release remain separate obligations. These results apply only to the frozen head above; later evidence/code commits need their own appropriate checks.

## Actual commands

All commands below ran from the candidate worktree. Exit codes are observed, not inferred from a plan. Elapsed time is wall time from the command harness.

| Check | Exact command | Exit | Seconds |
| --- | --- | ---: | ---: |
| candidate-validator | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/validate.py` | 0 | 0.825 |
| toolchain-fingerprint | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | 1.262 |
| workflow-kit | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | 0.043 |
| navigation | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | 0.076 |
| quality-framework | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | 0.079 |
| source-dependencies | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/check_source_dependencies.py` | 0 | 0.363 |
| architecture-documents | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_architecture_documents.py -v` | 0 | 14.322 |
| trusted-base-validator | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /workspace/scratch/6e019b0851cc/backbone-architecture-trusted/.engineering-backbone/src/validate.py --root /workspace/scratch/6e019b0851cc/backbone-architecture-quality --trusted-base /workspace/scratch/6e019b0851cc/backbone-architecture-trusted` | 0 | 0.949 |
| committed-patch | `git diff --check ae317bf30576914d4ed53856be4ae496c6ed64b3 1dbd1d68a7a23b8b38f532ed7a9dff8488642a57` | 0 | 0.007 |
| complete-suite | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v` | 1 | 618.267 |

The candidate validator explicitly reports that no trusted-base history comparison occurs in its standalone invocation. The separate `trusted-base-validator` command uses the executable from the actual ae317bf checkout and supplies that checkout as `--trusted-base`. The two results are distinct.

## Compatibility and negative-path evidence

- Real Copier copy exercised optional adapters/quality both disabled and enabled, including canonical rendered-content parity and absence of invented product documents/manifests.
- Real Copier update refreshed managed guides while retaining project-owned architecture, requirements, project template and native instructions byte for byte.
- Source/direct-copy and installed-consumer cases reject deletion of the linked architecture contract or decision template.
- A separate isolated Git archive of the exact frozen head was checked by the actual trusted-base validator. The intact control passed; deleting each newly linked required document produced the expected rejection. The frozen worktree was never mutated for these negative cases.

| Trusted-base case | Observed exit | Expected result |
| --- | ---: | --- |
| positive-control | 0 | 0 |
| missing-contract | 1 | nonzero and missing-file link diagnostic |
| missing-template | 1 | nonzero and missing-file link diagnostic |

Trusted negative-case runner: `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /tmp/backbone-architecture-trusted-negatives.py` (exit 0, 3.471 seconds). It exports `git archive --format=tar 1dbd1d68a7a23b8b38f532ed7a9dff8488642a57` to a fresh temporary directory and invokes:

```sh
/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /workspace/scratch/6e019b0851cc/backbone-architecture-trusted/.engineering-backbone/src/validate.py --root /tmp/backbone-arch-trusted-negative-8xc0l4ib/candidate --trusted-base /workspace/scratch/6e019b0851cc/backbone-architecture-trusted
```

For each negative case it removes only the named contract/template file, checks for nonzero exit plus the corresponding broken local Markdown link diagnostic, then restores that temporary file. Missing-document rejection proves structural link enforcement, not architectural fitness.

## Snapshot integrity and unchanged areas

Before/after SHA-256 comparison found all 617 tracked files unchanged. `git status --porcelain` was empty after execution. Head, base and patch digest were rechecked.
`git diff --quiet BASE HEAD --` over the protected paths below returned exit 0; no schema, catalog, guard/validator, runtime profile/configuration, dependency input, Dockerfile, product code, Copier settings or CI workflow changes are present:

```text
.engineering-backbone/src
.engineering-backbone/schemas
.engineering-backbone/standards
.engineering-backbone/requirements.txt
.engineering-backbone/requirements.lock
.engineering-backbone/core.json
.engineering-backbone/project.json
.engineering-backbone/opencode.json
.github/workflows
.codex
.opencode
opencode.json
infra/docker
apps
packages
config
copier.yml
```

Only documentation, canonical rendering wrappers and the new architecture-distribution test file are changed. No fingerprint regeneration, source repair, commit, branch publication or live provider operation was performed by this quality session. The suite executes fixture workflow payloads that invoke pinned pip requirements; observed output reported the existing versions already satisfied.

## Logs and limits

Raw local logs are retained under `/tmp/backbone-architecture-quality-logs/`; these transient files are not committed delivery artifacts. This durable report carries commands, outcomes and content digests so the runs can be reproduced.

| Log | SHA-256 |
| --- | --- |
| `candidate-validator.log` | `07604dad0ce23e9a3291888da5b1f5fb1e48d63eee763a517af23015c68eb6af` |
| `toolchain-fingerprint.log` | `f4604bc86a36f36d2d4bfc6dcda266d5cc127d5c6ef65dd7e480493d4265e905` |
| `workflow-kit.log` | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| `navigation.log` | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| `quality-framework.log` | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| `source-dependencies.log` | `4c8826eb1d965d4f44ac880d328b943916f62ff61c70af306cdc80400da82ee5` |
| `architecture-documents.log` | `da87254d73d23e52d5a4234a708284255a9a5698bbbc29023507ad39348f6ec4` |
| `trusted-base-validator.log` | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| `committed-patch.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `complete-suite.log` | `c7b251a910e90221c780ad3d4b4d61f3abe490b01505a173d185e6bd5b10a425` |
| `trusted-positive-control.log` | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| `trusted-missing-contract.log` | `41b7473d1d3a54ab2bbd347a29e43cbcc1180510da5c4a924d6b473c5c618d3a` |
| `trusted-missing-template.log` | `69690f18abe087569ea29033b7aa02d0cde33c82d3027958df27bf6b61bdc3b3` |

- Copier emitted expected initial missing-answers warnings in fresh consumer fixtures. They did not represent failures or skipped tests.
- The source dependency check observed 26 installed locked versions and consistent tracked inputs; this session reused the supplied isolated environment rather than claiming a new installation.
- Container execution, native client/provider loading, real application behavior, external tool integrations, normative clause conformance and repository protection/authenticated human approval were not tested. The unchanged runtime/container inputs and this documentation scope do not justify claiming those results.
- Markdown links and rendered bundle parity are checked; diagram rendering and semantic quality of the design remain independent review concerns.
- Hosted CI and the final published head are not covered by this local snapshot report.

## ARCH-CHECK-01: standalone quality package gains an absent architecture dependency

- Severity: P2; category: downstream compatibility; confidence: high.
- Location introduced by this diff: `docs/quality/policy.md:94` and its rendered
  link in `.engineering-backbone/legacy/templates/.engineering-backbone/quality-policy.md.jinja`.
- Trigger/path: the supported quality-package upgrade scenario adds the optional
  managed quality policy to a historical consumer while retaining its original
  eight-file tooling bundle. `QualityWorkflowTests.setUp` copies only that package
  and its project declarations. The new link resolves to
  `.engineering-backbone/architecture.md`, which this independent package route
  does not contain.
- Observed impact: the historical validator rejects a previously valid inactive
  quality seed with `broken local Markdown link architecture.md`. The current
  workflow also fails before its intended quality gate can be assessed. Fresh full
  Copier installs pass because they contain the new architecture bundle, so the
  targeted new copy/update tests alone did not expose this partial-upgrade case.
- Contract relation: AC-5 consumer compatibility and AC-6 required deterministic
  checks; preserve the established old-validator/current-workflow compatibility
  and distinct package activation boundaries.
- Diff causation: the unconditional link and wrapper replacement are new in the
  inspected patch; the historical fixture's copy boundary and assertions are
  unchanged. This is not a finding against historical fixture code.
- Minimal regression: the four unchanged affected test methods below must pass on
  the repair while still rejecting poisoned catalogs, malformed/null profiles and
  manufactured activation at the intended quality guard. Do not weaken those
  assertions or silently broaden the old tooling bundle.
- Disposition: returned for separate triage; no author repair, claim of approval
  or repeated unchanged-input test run by this quality session.

The five failure events in the complete suite were:

| Method in `tst.test_quality_workflows.QualityWorkflowTests` | Subcase / observed failure |
| --- | --- |
| `test_current_workflow_rejects_consumer_catalog_poisoning_old_validator_accepts` | Expected old-validator exit 0; got 1 for missing `architecture.md` |
| `test_current_workflow_rejects_null_and_malformed_profile_old_validator_accepts` | `content='null\n'`: expected old-validator exit 0; got 1 for missing `architecture.md` |
| `test_current_workflow_rejects_null_and_malformed_profile_old_validator_accepts` | `content='{"schema_version": "1",'`: same missing-file rejection |
| `test_first_activation_cannot_manufacture_a_reviewed_quality_seed` | Expected old-validator exit 0; got 1 for missing `architecture.md` |
| `test_valid_inactive_package_passes_without_executing_candidate_guard` | Expected current-workflow exit 0; got 1 for missing `architecture.md` |

Representative exact diagnostic:

```text
ERROR: .engineering-backbone/quality-policy.md: broken local Markdown link architecture.md
FAIL: 1 structural validation error(s).
```
