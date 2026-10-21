# Test strategy and scoped verification plan

Status: draft; project decisions, owners and review are not yet established.
Apply the [testing contract](../../quality/testing.md) and
[CI/CD contract](../../quality/ci-cd.md). Combine this with an existing project
strategy or delivery plan where that already owns the information.

## Scope, authority and decisions

| Field | Project value or authoritative reference |
| --- | --- |
| Strategy/plan identity and revision | Record ID, exact source revision and scope |
| Authorized objective and delivery | Requirement/architecture/plan IDs and revisions |
| Included components and changes | Product/configuration/document boundaries |
| Exclusions and applicability | Reason, owner, affected obligation and allowed disposition |
| Existing controls | Adopted core, quality/technology profiles and stricter local rules |
| Responsibilities | Planning/test-design owner, implementer, checker, independent reviewer, integration owner and decision authority |
| Open decisions | Question, owner, next action, budget and gate impact |

Do not infer requirement or design approval from this plan. Record assumptions and
source gaps explicitly. Refer to existing quality goals rather than inventing a
second requirements source. The [planning contract](../../agent-governance/planning.md)
links the required work to authorized delivery items and execution packets.

## Risk, applicability and coverage

| Requirement / acceptance / risk and revision | Quality goal or failure consequence | Selected method, level/type and reason | Test/procedure IDs and owner | Environment and evidence required | Gap or justified non-applicability |
| --- | --- | --- | --- | --- | --- |
| Project source | Observable obligation | Review/analysis/demonstration/test; appropriate scope | Authoritative definition | Planned, not observed evidence | Owner and gate effect |

Assess relevant functional, security/privacy, reliability, usability/accessibility,
performance/capacity, compatibility, maintainability and operational concerns.
Select success, rejection, boundary, state-transition and failure/recovery paths
where their risks apply. Distinguish component, integration and overall acceptance.
Use code/branch coverage only where useful, with justified local targets/exclusions;
requirement and material-risk coverage remain explicit. A percentage alone does not
establish adequacy. Test-first, example-led, exploratory or other approaches remain
project choices within the adopted obligations.

## Readiness, resources and completion

- Identify interfaces and testability hooks, observable outcomes and controlling
  configuration; resolve design obstacles before dependent implementation starts.
- Record supported platforms, actual dependencies, data versions, safe fixtures,
  isolation, access, tools and representative environments. Label mocks/simulations
  and the live behavior they cannot establish.
- State entry criteria, required permissions/capacity, sequencing, parallel resource
  conflicts, integration responsibility and bounded execution time/cost.
- Define suspension/resumption conditions and treatment of missing prerequisites.
- Define exit criteria: required coverage and results, finding resolution, accepted
  limitations and the independent/human decisions needed for the requested gate.

Use [CI mapping](ci-mapping.md) for events, actual check IDs and gates. Required
checks may be automatic, manual or hybrid, with a recorded procedure and result.
The existing workflow contract owns executable command definitions.

## Maintenance and source basis

When sources, interfaces, product/build inputs, platforms or acceptance change,
record affected tests and the validity of earlier evidence. Preserve old results;
plan focused re-verification and regression with an owner. The [run](test-run.md)
and [completion](test-completion.md) records contain actual observations later.

Source basis: original prompts informed by T-S02/T-S03, T-S05, T-S07/T-S08 and T-S12
in the [source register](../../quality/testing-sources.md#reference-register).
