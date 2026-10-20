# BB-ARCH-015 independent repair checks

- Checker: `/root/architecture_quality`, independent quality session; no author repair role.
- Date: 2026-10-20.
- Actual trusted base: `ae317bf30576914d4ed53856be4ae496c6ed64b3`.
- Prior failed subject: `1dbd1d68a7a23b8b38f532ed7a9dff8488642a57`.
- Repaired frozen subject: `f5860b5ec6ff31457c021c8a81cc0128f62fc468`.
- Tree: `d4aa8b2a9024a3cb26293fede0bb4e6e13add713`.
- Base-to-repaired binary patch SHA-256: `5440559beb213336e0c424cccf0b4e60ed7d48b30a789188168e27ef5996a287`.
- Prior-to-repaired binary patch SHA-256: `e557b66896c2b30e651893f94d686f91217612987b2bde4bf42f253f41f2e396`.
- Confirmed repair ID: `ARCH-CHECK-01`; independently triaged before repair.
- Candidate worktree: `/workspace/scratch/6e019b0851cc/backbone-architecture-repaired-quality`.
- Trusted checkout: `/workspace/scratch/6e019b0851cc/backbone-architecture-trusted`.
- Interpreter: `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python` (Python 3.12.14).

## Result and rerun basis

PASS for the required deterministic scope on the repaired head: complete suite ran 465 tests in 606.809 seconds, result `OK`, exit 0. Focused unchanged regression classes ran 8 tests in 18.957 seconds, result `OK`, exit 0. Candidate and actual trusted-base validation, four compiler checks, source dependencies and both committed-patch checks passed.

The prior failed run and separate triage remain preserved in `failed-checks.md` and `check-triage.md` in this delivery. The prior five failure events across four test methods are not relabeled as passing. This rerun was justified by the changed quality-policy input and removed obsolete wrapper rewrite, exactly within the confirmed repair boundary. No historical fixture, assertion, guard, schema or test was changed for the repair.

The corrected independently adoptable quality package refers to the architecture obligations of the adopted core without introducing an absent file dependency into historical consumers. Full new installations retain the mandatory core link and supplied architecture kit.

This result clears the deterministic-check prerequisite for the required independent Full reviews. It is not a semantic Full/Delta review, authenticated human approval, hosted CI result or permission to merge/release.

## Actual commands and outcomes

All commands ran in the candidate root except `focused-regressions`, which ran in its `.engineering-backbone/` directory. The absolute interpreter is recorded above; commands below are the exact argv joined for reading. Times are observed command wall time, distinct from unittest-reported execution time.

| Check | Exact command | Exit | Seconds |
| --- | --- | ---: | ---: |
| candidate-validator | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/validate.py` | 0 | 0.795 |
| toolchain-fingerprint | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | 1.25 |
| workflow-kit | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | 0.04 |
| navigation | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | 0.069 |
| quality-framework | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | 0.072 |
| source-dependencies | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python .engineering-backbone/src/check_source_dependencies.py` | 0 | 0.348 |
| focused-regressions | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest tst.test_quality_workflows.QualityWorkflowTests tst.test_architecture_documents.ArchitectureDocumentTests -v` | 0 | 19.434 |
| trusted-base-validator | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python /workspace/scratch/6e019b0851cc/backbone-architecture-trusted/.engineering-backbone/src/validate.py --root /workspace/scratch/6e019b0851cc/backbone-architecture-repaired-quality --trusted-base /workspace/scratch/6e019b0851cc/backbone-architecture-trusted` | 0 | 1.017 |
| committed-patch | `git diff --check ae317bf30576914d4ed53856be4ae496c6ed64b3 f5860b5ec6ff31457c021c8a81cc0128f62fc468` | 0 | 0.006 |
| complete-suite | `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v` | 0 | 607.542 |

Additional committed-repair check: `git diff --check 1dbd1d68a7a23b8b38f532ed7a9dff8488642a57 f5860b5ec6ff31457c021c8a81cc0128f62fc468` returned exit 0. Both patch checks were repeated after the suite without a changed input, solely to confirm final publication-patch integrity; no test was retried for a green result.

The standalone candidate validator does not perform trusted history comparison. That comparison was separately executed with the actual ae317bf validator and `--trusted-base` checkout; a candidate PASS was not substituted for it.

## Confirmed regression coverage

`QualityWorkflowTests` was unchanged and now passes all four affected methods, including both malformed/null-profile subcases. The valid inactive quality package passes without executing candidate guard code. Catalog poisoning, malformed/null profiles and manufactured first activation continue to be rejected by the intended current quality guard, while the historical-validator control behaves as expected.

`ArchitectureDocumentTests` was unchanged and passes all four methods: real off/on copy, canonical rendered parity, absence of invented product files, real update preserving project-owned architecture/requirements/native instructions, and rejection of missing required contract/template in source and installed layouts. The complete suite includes both classes again and the existing wider compatibility/security checks.

No new optional experiments or unchanged-input failure retries were added. The explicit trusted-base negative archive cases belong to the preserved prior-head report; this report does not present those historical executions as newly run tests.

## Snapshot integrity

All 619 tracked file hashes remained identical before and after execution; `git status --porcelain` was empty. Head, trusted base, tree and both patch identities were verified. A prior-to-repaired test-tree comparison returned exit 0, confirming no changed tests.
Base-to-repaired `git diff --quiet` returned exit 0 over the protected paths below, confirming no validator/guard, schema/catalog, dependency, native runtime profile/configuration, Docker, CI, product or Copier-setting changes:

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

No source repair, commit, publication or live provider operation was performed by the checker. The suite invokes fixture workflow payloads using the supplied pinned environment; observed pip output reports the installed requirements already satisfied.

## Local logs and limitations

Raw logs remain under `/tmp/backbone-architecture-repair-quality-logs/`; these transient files are not the durable record. Commands, outcomes and log digests are recorded here.

| Log | SHA-256 |
| --- | --- |
| `candidate-validator.log` | `07604dad0ce23e9a3291888da5b1f5fb1e48d63eee763a517af23015c68eb6af` |
| `toolchain-fingerprint.log` | `f4604bc86a36f36d2d4bfc6dcda266d5cc127d5c6ef65dd7e480493d4265e905` |
| `workflow-kit.log` | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| `navigation.log` | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| `quality-framework.log` | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| `source-dependencies.log` | `4c8826eb1d965d4f44ac880d328b943916f62ff61c70af306cdc80400da82ee5` |
| `focused-regressions.log` | `8e1bf926443bcc962dc0c9b26d5f36cc6568c61affc8fc27451b9a7df09f8ae7` |
| `trusted-base-validator.log` | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| `committed-patch.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `complete-suite.log` | `6d6fd6b78d5ca76f3dca801831aa37b5fea22285e7c25aa807fe5ce8db324e35` |

- Expected initial Copier missing-answers warnings occurred in fresh consumer fixtures; they were not failures.
- The source dependency check observed 26 installed locked versions and consistent tracked inputs. No new environment installation is claimed.
- Tests use isolated fixtures and controlled/stubbed runtime paths. They do not establish live client/provider loading, actual product behavior, normative conformance, human approval or repository-protection enforcement.
- No container execution or diagram-rendering run was performed by this checker; runtime/container inputs are unchanged. Architecture semantics remain the subject of the independent reviews.
- Hosted CI and any later evidence/publication head are outside this frozen local report and require their own appropriate observations.
