# BB-START-018 implementation and integration

The independently accepted plan at `3982016b6aad28271b524fd0fa68be20f390e1f2`
targets actual main `4e74c7e5f3a07430768f670c4271c1e1a0e28f68`. Root integrates
separate environment, runner, export and lifecycle authors. This record initially
describes an implementation with pending check triage, not a passing final gate.

| Requirement | Delivered implementation | Author |
| --- | --- | --- |
| START-01 | Harmless root `.env.example`, empty project variable register, stdlib metadata/value checker, configuration/credential guide | `starter_environment_impl` |
| START-02 | Fixed-probe local doctor, source runner onboarding, local-CI evidence template and inactive fail-closed no-upload example | `starter_runner_impl` |
| START-03 | Git-ref-bound neutral export, managed-byte/structural verification, neutral entrypoint seeds, trusted schema/native checks | `starter_export_impl` |
| START-04 | Read-only trusted old/new/local comparison, neutral project development map, actual source setup/check instructions | export and lifecycle authors |
| START-05 | Threat, runbook, incident, restore and release/support templates with applicability and official source hints | `starter_lifecycle_impl` |

The exporter owns selection and transformations in its reviewed executable. It
reads immutable Git blobs, omits source history/tests/maintenance/legacy/active CI,
and keeps shared canonical paths. Project facts and instructions are project-owned;
managed policy/schema/catalog/native baselines are checked against trusted source.
Provenance cannot select a weaker mode. The separate seed gate refuses existing
source/legacy and unsupported optional contracts. It does not replace their gates.
Update comparison runs only the explicitly selected old trusted source descriptor,
never project code, and writes no project changes. Real credentials are excluded.

Environment input is literal and explicitly selected; process values take priority.
The checker never evaluates shell syntax or prints supplied values. Empty metadata
does not establish application readiness. Git ignore is not an access boundary.
Doctor probes use fixed argument arrays/timeouts, suppress tool output and perform
no installation/registration. Native application commands remain project choices;
no universal task runner or installed application stack is introduced.

## Author-side checks before the frozen quality gate

- Environment: 12 tests passed, exit 0, 1.213 seconds unittest / 1.285 wrapper;
  fake secret redaction, missing/type/duplicate/input-bound/precedence and shell
  nonexecution cases. Actual empty-register local and explicit example runs exit 0.
  Raw evidence: ignored `artifacts/starter-environment/`.
- Runner: 11 new tests passed (0.097 / 0.190 seconds), six existing source-CI
  tests passed (0.561 / 0.622 seconds), exit 0. Real development doctor exit 0.
  Real source-linux doctor exit 1: Docker CLI/daemon unavailable here. This is
  preserved as an actual prerequisite gap, not converted into passing CI.
  Raw evidence: ignored `artifacts/starter-runner/`.
- Lifecycle author: owned-document local links/whitespace passed. An early source
  validator run during concurrent construction exited 1 for four links to the
  export guide that had not yet been created. No owned-template links failed.
  This incomplete-worktree result was not final quality evidence. After the guide
  existed, root's integrated candidate validator, actual base-owned validator and
  tracked whitespace preflight all passed, exit 0.
- Export: initial ten-test run had nine passes and one failure, exit 1, 4.485
  seconds. The comparison test expected a local-only Markdown change but received
  a conflict. Immutable source-URL rewriting is the suspected reason; independent
  START-CHECK-01 triage is pending. Raw log: `artifacts/starter-export/initial-tests.log`.
- The author separately raised START-CHECK-02: Python's cached module loader might
  execute unattested bytecode despite checking the `.py` Git bytes. Independent
  reproduction/triage is pending; no repair is represented as complete yet.

Both pending items require separate triage before repair. Deterministic final
checks and both Full reviews follow a new frozen subject after confirmed fixes.
No source/legacy validator, schemas, catalog, active workflow, dependency/container
inputs, historical fixture or old delivery record has been changed. Protected-path
preflight passed. No final Full, native Windows, Docker image, actual runner fleet
or completed remote CI result is established by these author checks.

## Pre-Full repair completion

Independent [check triage](check-triage.md) confirmed START-CHECK-01/-03 as narrow
test-fixture expectations and START-CHECK-02 as a P1 cache-versus-source attestation
defect. The authorized single repair iteration compiles the actual trusted Git
blobs directly, adds both-helper poisoned-cache nonexecution/no-write coverage,
and corrects only the two precise comparison expectations. All eleven repaired
export tests pass, exit 0, 6.251 seconds. Initial evidence is preserved. The source
and legacy engines remain unchanged. A fresh committed snapshot is now required
for independent deterministic checks and both first Full reviews; author results
do not replace those gates.
