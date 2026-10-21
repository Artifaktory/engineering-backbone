# Test strategy selection

Project test strategy connects requirements and material risks to observable
behavior. Start during planning; update it when design, contracts or risk change.
Assign a responsible owner, environments, data/fixtures, execution commands,
thresholds, evidence location and unresolved limitations for each required area.

Use the [architecture contract](../agent-governance/architecture.md) to derive
verification from requirement acceptance, quality scenarios, design claims and
material risks. Select the method during design; add actual results only after
execution on a recorded revision. A prototype supports only its tested assumptions,
and a reviewed target architecture does not establish implemented behavior.

| Area | Minimum selection criterion | Evidence purpose |
|---|---|---|
| Unit/component | Own logic, validation, calculations or state transitions | Isolate relevant success, boundary and failure behavior quickly |
| Integration/contract | Module, service, database or external interface | Verify actual interaction and version/contract expectations |
| Acceptance/end-to-end | Identified critical user/business flows | Establish the intended outcome in the supported assembled system |
| Negative/security | Material inputs, privilege, trust boundaries and errors | Verify rejection, safe failure and authority boundaries |
| Regression | Reproducible confirmed defects | Show the defect is detected and the repair satisfies the contract |
| Performance | Measurable latency, throughput or capacity requirement | Compare actual behavior with the project's stated target |
| Migration/recovery | Persisted data or availability obligations | Verify compatibility, integrity, restore and supported recovery |
| Platform/runtime | Supported environment or version differences | Exercise the declared support matrix proportionally to risk |

Record applicability and justified exclusions instead of accumulating irrelevant
test suites. A documentation-only project may use content/link/structural tests.
The `software`, `high-risk` and `agentic` refinements require actual test bindings.

## Coverage and quality

Measure requirement/acceptance coverage, material-risk coverage, critical behavior
and relevant success/failure/state-transition paths. Use line and branch coverage
where it helps expose code gaps, with justified component targets and exclusions.
There is no universal coverage percentage. Mutation/property/fuzz techniques may
add useful evidence for suitable logic and input surfaces; select them explicitly
with a bounded budget and failure interpretation.

Keep tests deterministic where practical. Control time, randomness and external
dependencies; separate fixtures from production credentials/data. Stubbed contracts
are useful but do not establish live provider, network or deployment behavior.
Record unexecuted live checks and manual acceptance instead of claiming equivalent
coverage. Diagnose flaky required checks; do not weaken assertions or repeat an
unchanged failure solely to obtain a green result.

## Agentic systems

Map the actual supported chain from instructor/task owner through orchestration,
dispatch, worker results, independent review, gates and final return. Verify:

- Exact task/profile/rule context, authorized scope and acceptance are preserved.
- Roles remain separated; implementers cannot approve their own work.
- Missing, failed, stale or conflicting evidence reaches the appropriate gate and
  return state; it is not reported as complete.
- Confirmed review findings follow triage, repair and Delta review correctly.
- Cancellation, timeout, partial failure, pause/resume and duplicate delivery are
  exercised where the actual host supports them.
- Returned results update the orchestration/task-owner state with correct evidence
  and stop conditions, without unauthorized publishing, merge or deployment.

Name the interfaces and supported transitions in the project strategy. Use
deterministic integration tests for the chain and bounded live verification for
provider-dependent behavior. The `agentic` profile is a test obligation; it does
not install AO, invent transitions, certify a harness or execute a live multi-agent
system merely by validating configuration.

## Execution phases

| Phase | Project-selected coverage |
|---|---|
| PR | Fast targeted checks, affected integration, critical acceptance, security and declared coverage gates |
| After merge | Required verification of the actual merged revision |
| Scheduled | Longer matrices, broad system/security, selected performance and recovery runs |
| Release/deployment | Built-artifact verification and applicable smoke/migration/recovery evidence |

Executable commands and phase assignments remain in the workflow kit. Quality
rule bindings identify PR check IDs; additional phase requirements are documented
and reviewed, not automatically installed by the quality guard. Required repository
settings enforce merge gates separately. Attach actual reports to the inspected
revision and preserve limitations in traceability/review closeout.

## Planning and integration handoff

Use the planning contract referenced by the adopted core to map each scoped
requirement/risk and acceptance criterion to its delivery item, verification method,
environment, responsible role and expected evidence. Plan integration and negative
paths alongside implementation. Prepared tests and mocks do not establish assembled
system behavior; record actual execution on the integrated revision separately.
An optional testing-package update does not silently adopt a newer core contract.
