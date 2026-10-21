# Testing and verification contract

This is the shared semantic contract for planning, designing, conducting and
reviewing verification under the project's adopted [core policy](../agent-governance/core.md).
Use it with the [architecture contract](../agent-governance/architecture.md),
[planning contract](../agent-governance/planning.md), [testing document kit](../templates/testing/README.md)
and [CI/CD evidence contract](ci-cd.md). It applies to the authorized change scope;
it does not require unrelated systems to be redesigned or retested without cause.

**Authority:** MUST denotes an original Backbone obligation. The
[source register](testing-sources.md) identifies public standard scopes, engineering
guidance and optional methods that informed these rules. No full-text ISO clause
conformance, certification, universal tool, test count or coverage percentage is
claimed. `TST-*` IDs are document references, not new catalog rules or JSON fields.

Adopting this contract through the core does not activate optional quality,
navigation or workflow packages. Their existing activation, profile, check-binding
and exception contracts remain unchanged. Where adopted, the [quality policy](policy.md)
and stricter project controls add binding duties; this document cannot subtract them.
It installs no test runner, result-state engine, tracker or deployment permission.

## TST-01: Scope, authority and traceability

The project MUST identify the verification scope, authoritative requirement/design
revisions, quality goals, material risks, acceptance criteria and decision owners.
Carry these inputs from architecture and delivery planning into test work. Preserve
stable IDs and bidirectional links among requirements/risks, design claims,
delivery items, tests/checks and actual evidence. Relationships may be many-to-many.
Do not copy requirements into a competing test specification or infer approval
from a link, prototype or completed template.

For every scoped obligation, record planned verification, applicable existing
evidence, an authorized scope/deferral decision, or a visible gap with owner and
next action. A deferral does not satisfy acceptance that still requires the result.
Resolve an ambiguous expected behavior with its decision owner; a test author
must not silently choose a product requirement to make a test pass.

Records MAY be combined for a small change or represented by existing project
tools with reviewable revisions. Use the smallest sufficient record set. Routine
tool and implementation choices remain within the already authorized decision space.

Source note: Backbone rule informed by [T-S02, T-S03, T-S05, T-S07 and T-S08](testing-sources.md#reference-register).

## TST-02: Distinguish methods, levels and phases

Here, **verification** assesses the specified obligations; **validation** assesses
fitness for the intended stakeholder use and operating context. Select suitable
inspection/review, analysis, demonstration, executed test or a justified combination.
Document reviews and static checks can establish their particular claims before
executable software exists; runtime behavior still needs its required runtime evidence.

| Dimension | Examples and boundary |
| --- | --- |
| Test level | Component/unit, integration, system and acceptance; names and boundaries follow the actual product. |
| Test type or objective | Functional, security, performance, compatibility or recovery; these can span several levels. |
| Design technique | Boundary values, equivalence classes, decision tables, state transitions, exploratory, property-based or fuzz techniques where useful. |
| Development approach | TDD, BDD, examples-first or another suitable practice; no single approach is imposed by this contract. |
| Execution occasion | PR, integrated main, scheduled maintenance, release or deployment; an occasion is not proof of coverage. |

Automated, manual and hybrid methods are valid when their procedures, coverage,
results and responsibility are explicit. A simulator, fixture or mock establishes
only its exercised assumptions, not live provider, native platform or deployment
behavior. A successful document build establishes neither design approval nor
implemented product acceptance.

Source note: Backbone terminology informed by [T-S01, T-S04, T-S06, T-S07, T-S08 and T-S12](testing-sources.md#reference-register).

## TST-03: Select coverage from obligations and risks

The project MUST assess applicability, required depth and evidence for relevant
verification areas, including the following. This is an assessment matrix, not a
requirement to execute every technique on every project.

| Area | Selection trigger and evidence purpose |
| --- | --- |
| Static/document quality | Relevant requirements, architecture, code, configuration, documentation or build inputs; assess content and appropriate syntax/type/lint/structure claims. |
| Component/unit | Own logic, validation, calculations or state changes; exercise meaningful success, rejection, boundary and failure behavior. |
| Integration/contract | Interacting modules, databases, services or external interfaces; establish actual compatibility and error behavior. |
| System/acceptance | Critical stakeholder outcomes; exercise the assembled supported configuration and intended use. |
| Security/privacy | Material inputs, privilege, trust boundaries and data protection; verify relevant controls and safe failure. |
| Regression | A reproducible defect or changed behavior; show that the check detects the defect and qualifies its repair. |
| Performance/capacity | Authorized latency, throughput, resource or scale targets; select representative load, stress, endurance or data-volume scenarios as needed. |
| Migration/recovery/operations | Persisted data, delivery or availability obligations; verify relevant upgrade, integrity, startup, rollback/restore and operating behavior. |
| Platform/runtime/dependencies | Promised environments or coupled versions; exercise a justified support matrix and actual affected inputs. |

Assess other material qualities, such as usability/accessibility, maintainability,
data quality or physical safety, where the product's quality model and risks require
them. The table does not exhaust the project's possible verification objectives.

Record required/optional status or justified non-applicability, with scope, reason,
owner and affected gate. Omission, an empty heading or unexplained `N/A` is not a
disposition. Apply existing profile duties: for example, an adopted software
profile's build/lint/test/security bindings cannot be replaced by documentation checks.
Documentation-only work may use content, review and structural checks suitable to
its actual claims. Use the applicable quality model to expose missed concerns;
do not invent quality targets or assume that all products share the same thresholds.

Measure requirement/acceptance, material-risk and critical-behavior coverage. Use
code/branch measures where useful, with justified targets and exclusions. A high
percentage, large test count or green scan does not establish adequate coverage.

Source note: Backbone selection rule informed by [T-S02, T-S05, T-S07, T-S09 and T-S12](testing-sources.md#reference-register).

## TST-04: Plan testability and readiness early

During architecture and delivery planning, the responsible roles MUST select
verification methods and address observability, controllable inputs, interfaces,
environments, data, access and uncertainty. Identify required skills/resources,
time/cost assumptions, check and integration owners, independent reviewers and
explicit entry/exit criteria. Record unresolved inputs with their next action and
gate impact. A bounded investigation may produce decision evidence without claiming
that the eventual feature is verified.

The [test strategy](../templates/testing/test-strategy.md) records the applicable
coverage, methods, responsibilities, environments, evidence expectations and timing.
Reference the existing quality plan and delivery plan instead of duplicating their
authoritative scope, risk decisions or commands. Connect planned checks to their
actual execution routes using [CI mapping](../templates/testing/ci-mapping.md).

Start a required run only when its procedure, target inputs, expected outcomes,
environment and permissions are sufficiently ready. An unavailable prerequisite
blocks the affected run or supports an explicitly bounded alternative investigation;
it does not authorize weakened acceptance. Do not defer security or integration
planning to an unspecified final polishing phase.

Source note: Backbone planning rule informed by [T-S02, T-S03, T-S07 and T-S09](testing-sources.md#reference-register).

## TST-05: Specify meaningful checks

For each required check or coherent group, the project MUST identify its source
obligation/risk and stable test or procedure reference, prerequisites, inputs/data,
actions or command, expected result and decision criterion. Include required
cleanup, side effects and stopping conditions. Choose representative normal,
negative, boundary, state-transition and failure cases according to the risk.
Compare observations with the authorized expectation rather than with an unreviewed
output generated by the same implementation.

Use [test design](../templates/testing/test-design.md), or reference executable tests
that carry these details. A separate prose case for every automated test is not
required. Manual and exploratory checks need reproducible scope, procedure/charter,
observations and result interpretation proportionate to the claim. Test changes
receive semantic review; changing an assertion or reference output requires an
explanation of the underlying requirement or defect.

For a reproducible bug repair, preserve the observed failing condition and show
that the regression check detects it before accepting the repaired result. Do not
reintroduce unsafe effects merely to reproduce a live failure; use a controlled,
representative reproduction and state its limitations.

Source note: Backbone design rule informed by [T-S03, T-S04, T-S07 and T-S12](testing-sources.md#reference-register).

## TST-06: Control environments and data

Record the actual source/build/artifact identity, test-code or procedure revision,
platform/runtime, relevant tool/dependency versions, configuration and test-data
identity for each claim. Protect credentials and personal data; use isolated,
redacted or synthetic fixtures where suitable and document necessary live access.
Control time, randomness, concurrency and external dependencies where practical.
Avoid cross-run mutable state and document cleanup or recovery needed after a run.

The environment MUST support the claimed behavior. Mocks cannot establish actual
database migration or external-service compatibility; Linux checks cannot establish
native Windows behavior. Representative substitutes and reduced matrices may be
useful, but their scope and remaining required evidence must be visible. The
project's existing dependency and supported-platform contracts remain binding.

Source note: Backbone environment rule informed by [T-S03, T-S07, T-S09 and T-S12](testing-sources.md#reference-register).

## TST-07: Execute, investigate and preserve results

The quality checker or assigned executor MUST record actual commands or manual
procedures, target/configuration identity, time, observed results, relevant exit
codes and accessible evidence. Use a [test-run record](../templates/testing/test-run.md)
or an equivalent report; redact sensitive output and preserve enough information
for independent assessment. Planned checks, generated receipts and fixture-based
smoke messages are not live execution evidence.

When an anomaly occurs, preserve the failure and its inputs. Triage product defects,
test defects and environment/tool failures before repair. Link findings, decisions,
changed inputs, focused rechecks and relevant regression. Stop affected work when
continuing would be unsafe or invalidate the evidence; retain partial results and
state the conditions for a valid resume or fresh run.

Do not retry an unchanged failure merely to obtain green. A rerun needs a stated
diagnostic purpose or evidenced transient cause; keep all attempts and their
interpretation. A flaky check remains uncertain after a lucky success. Any temporary
quarantine must expose the lost coverage, owner, repair action, expiry and gate
impact under the project's permitted exception rules. Quarantine cannot silently
waive a required check or a nonwaivable obligation.

Source note: Backbone execution rule informed by [T-S02, T-S03, T-S07, T-S09 and T-S12](testing-sources.md#reference-register).

## TST-08: Keep claim states separate

The following vocabulary defines semantic distinctions for companion records and
tool mappings; it does not extend existing JSON/CSV schemas. Equivalent project
terms are permitted if their meaning and allowed gate conclusions remain explicit.

| Dimension | Meaning to preserve |
| --- | --- |
| Applicability | Required, optional or justified not applicable for the stated scope. |
| Run lifecycle | Not run, running, finished or cancelled. A queued run has not executed. |
| Check outcome | Not assessed; pass; fail; blocked; error; inconclusive; or skipped, with the actual reason. |
| Evidence applicability | Applicable to the current claim, applicable with stated limits, or stale/requiring reassessment after changes. |
| Acceptance/gate decision | Open, satisfied or blocked; a permitted explicit exception is a separate decision with its original authority and bounds. |

`pass` means that an actually completed check met its defined criterion for its
recorded target and environment. `fail` means that an observation did not meet the
criterion. `error` means that a test/tool/environment failure prevented a usable
test decision; `inconclusive` means the collected evidence cannot decide the claim.
`blocked` identifies an unmet prerequisite or required unresolved issue; `skipped`
records an intentionally omitted execution. Record which cases actually ran when
a suite was partial or cancelled. None of missing, not run, queued, blocked, error,
inconclusive, skipped, cancelled or not applicable establishes a passing runtime check.

Preserve the supported schemas exactly:

| Existing representation | Supported states and interpretation |
| --- | --- |
| Requirement verification | `not_run`, `pass`, `fail`, `blocked`; assess the full scoped requirement, not merely one passing child test. |
| Task Packet acceptance and review check | `pending`, `pass`, `fail`, `blocked`; use companion details for run/error/applicability distinctions. |
| Quality traceability CSV | `pending`, `planned`, `verified`, `gap`; `verified` is a declaration with evidence, not a validator-authenticated runtime PASS. |
| Task Packet lifecycle | `planned`, `active`, `blocked`, `ready_for_review`, `completed`; these describe the assignment, not the result of a test. |
| Workflow result | Preserve the actual executor's result and its mapping; required missing/failed/cancelled/skipped jobs cannot satisfy the existing strict aggregate. |

Do not serialize these explanatory labels as unsupported schema values. A failure
or stale report keeps its original result; append a new assessment/run at the new
revision. An exception never rewrites a historical test into PASS. Apply stronger
installed gate and exception rules; updating a board column supplies no evidence.

Source note: the exact vocabulary/crosswalk is Backbone-owned. [T-S03, T-S07 and T-S12](testing-sources.md#reference-register) inform record separation; existing schemas define machine-supported states.

## TST-09: Assess completion and acceptance

Before claiming verification complete, the responsible roles MUST compare planned
and actual coverage, results, anomalies and environments against the scope and exit
criteria. Use the [completion record](../templates/testing/test-completion.md) and
[review checklist](../templates/testing/review.md), or equivalent project records.
Account for every required result, missing/omitted case, open defect, limitation
and remaining risk, with its owner and gate effect. Distinguish item-level checks
from assembled-system and intended-use acceptance.

Independent review assesses whether the selected checks and evidence are adequate,
not just whether a command exited zero. Missing, failed, stale or unexecuted
mandatory evidence blocks the affected completion claim unless an existing project
mechanism permits a specifically authorized exception to that obligation. Baseline
nonwaivable duties and stricter controls remain binding. Human merge/release and
deployment decisions retain their separate required gates.

Source note: Backbone completion rule informed by [T-S02, T-S03, T-S06, T-S07 and T-S08](testing-sources.md#reference-register).

## TST-10: Reassess changes and verify handoffs

A relevant change to requirements, design, interfaces, implementation, test logic,
build inputs, data, environment or platform MUST trigger an evidence-impact
assessment. Identify affected claims, old/new revisions, evidence that remains
applicable, necessary new checks and blocked gates. Preserve historical results;
do not relabel old evidence as execution on a new configuration. Recheck affected
behavior and direct regressions proportionately, without restarting unrelated work.

Every agent/human handoff carries the scoped Task Packet, authoritative sources,
acceptance IDs, applicable rules, check definitions, environment/access needs,
required evidence and stop/return contract. Existing Task Packet roles apply;
specialized test responsibility does not add new schema roles or permissions.

For systems with agent delegation/orchestration, plan and verify the actual supported
chain from task owner/instructor through dispatch, workers, independent review,
triage, gates and return. Cover context/role boundaries, rejected or missing evidence,
partial failure, cancellation, timeout, duplicate delivery, pause/resume and correct
owner/orchestrator state updates where supported. Worker-only tests do not establish
whole-chain behavior. Combine deterministic integration checks with bounded real
host/provider checks when required; label their distinct claims and unexecuted paths.
Neither a profile nor a receipt installs or qualifies an orchestrator.

Map execution occasions and their real check/evidence/gate routes under
[the CI/CD contract](ci-cd.md). General scheduled or release behavior-test automation
requires the actual project implementation; documenting a phase installs none.
An optional package update does not silently adopt a newer core or activate checks.

Source note: Backbone change/handoff rule informed by [T-S02, T-S03, T-S07, T-S09 and T-S12](testing-sources.md#reference-register). The concrete agent-chain duties are our risk-based adaptation, not a claimed external agent-testing standard.
