# Architecture description: TBD project or scoped change

Template under the [architecture contract](../../agent-governance/architecture.md).
Use actual references or visible open items; do not turn prompts into factual claims.

| Record control | Project value |
| --- | --- |
| Description ID and accountable owner | `TBD` |
| Scope, exclusions and delivery/Task Packet | `TBD` |
| Authoritative source index and tool mapping | `TBD`; see [project mapping](project-mapping.md) |
| Requirement baseline | `TBD` source locations and immutable revision/export identity |
| Architecture source revision | `TBD`; record a frozen identity at review |
| Description status | Draft; replace only with a supported project state and decision record |
| Represented state | Target, observed implementation, or explicitly separated portions of each |
| Observed implementation revision | Not established; supply only when inspected |
| Review/evidence index | None yet; see [review](review.md) |

## 1. Purpose, stakeholders and goals

Describe the system's purpose and the outcomes in this scope. Identify stakeholders
and the questions they need the architecture to answer, including users, maintainers,
operators and affected external parties where applicable.

| Stakeholder/decision owner | Concern or goal | Requirement/source reference | Priority and reason |
| --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` |

## 2. Constraints and assumptions

Reference actual business, technical, organizational, regulatory and operational
constraints that materially restrict the design. Separate required constraints
from preferences and assumptions. A selected tool is not automatically a requirement.

| ID | Constraint or assumption | Source and approval state | Owner | Consequence if false / clarification needed |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

## 3. System boundary and context

Identify what is inside and outside the system, users/external systems, exchanged
information and relevant trust boundaries. State where responsibility ends. Link
the context view and authoritative external contracts. Do not include credentials
or sensitive production data in diagrams or examples.

## 4. Solution strategy and derivation

Name the architecturally significant requirements, quality scenarios and constraints.
Explain how the proposed strategy addresses them, why its complexity is justified,
and which uncertainties need early analysis or a prototype. Link the relevant
[traceability](traceability.md), [scenarios](quality-scenario.md) and
[decisions](decision.md). Record meaningful alternatives without manufacturing a quota.

| Driver/source | Design response | Decision/view reference | Main tradeoff or unresolved risk |
| --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` |

## 5. Building blocks and interfaces

Describe responsibilities, boundaries, dependency direction and interfaces at the
level needed to explain the scoped behavior. Identify owners of data and contracts.
Distinguish conceptual elements from actual modules/processes and implementation
locations. Document versions and compatibility assumptions for material interfaces.

| Element ID | Responsibility / exclusions | Interface and dependency references | Requirement/decision references | Actual code location, if implemented |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | Not established |

## 6. Runtime behavior

Show the critical interactions and state transitions. Include relevant failure,
retry, concurrency, cancellation and recovery paths, with responsibility for each
response. Link interface and quality-scenario IDs; a static component picture alone
does not describe these behaviors. State which paths remain unknown or unexamined.

## 7. Deployment and operation

Map the required runtime elements to actual or proposed environments, platforms and
trust zones. Explain configuration, secrets handling, observation, scaling, upgrade,
rollback and recovery responsibilities where relevant. Distinguish development,
test and production assumptions. Reference existing operational documents instead
of duplicating commands or creating fictional deployment infrastructure.

## 8. Crosscutting concepts

Explain applicable shared decisions such as data lifecycle and migration, security
and privacy boundaries, authorization, consistency, errors, logging, observability,
dependency compatibility, UI/accessibility and testing. Select by requirement/risk;
record justified exclusions. For agentic behavior, cover delegated authority,
handoff state and failure/evidence propagation when part of the actual scope.

## 9. Decisions and rationale

Index significant decisions and their current state, including superseded decisions.
Routine local choices need no separate ADR unless they materially affect requirements,
quality, constraints, interfaces, reversibility or cost. Link the source decision
record; do not repeat a competing version of its rationale.

| Decision ID / authoritative reference | State | Drivers | Reconsideration trigger / replacement |
| --- | --- | --- | --- |
| `TBD` | Proposed | `TBD` | `TBD` |

## 10. Quality goals and evaluation

Link prioritized measurable scenarios and the proposed evaluation method for each
material goal. Show important tradeoffs and sensitive assumptions. Thresholds need
their source/approval state; a new proposed value is an open decision, not approved
acceptance. Keep analysis/prototype evidence distinct from production behavior.

| Scenario / goal source | Planned analysis, test or manual assessment | Owner and environment | Actual result/evidence and revision |
| --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | Not run |

## 11. Risks, debt and open questions

| ID | Risk, unresolved question or deliberate debt | Affected requirements/views | Owner / next action and review trigger | Gate effect and decision reference |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | Open; specify the affected gate |

Do not silently accept a material risk or defer required coverage. Record the
project-authorized decision and compensating measures where permitted. Preserve
nonwaivable and stricter project obligations.

## 12. Vocabulary

Define ambiguous domain terms and ID meanings; link an existing glossary when it
is authoritative. A C4 container describes an application or data store at an
architectural level, not a requirement to use Docker. Avoid using one term for different elements
across requirement, diagram and code sources.

## View index and consistency

A viewpoint describes the questions and conventions for a kind of view; a view
answers them for this system and revision. Any notation is acceptable if readable
and mapped to the declared semantics.

| View ID / source | Audience and concerns | Viewpoint / notation and legend | Source revision and target/observed state | Correspondence checks |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD`: shared IDs, interfaces, data ownership, runtime/deployment agreement |

Record inconsistencies and their owners explicitly. Generated diagrams identify
their source and revision; they are not a second authority. C4 levels are optional:
include only useful detail and add behavior/data/deployment views when needed.

## Coverage, tailoring and change impact

Map all scoped requirements to the [traceability record](traceability.md), including
existing coverage, justified no architecture impact and open work. List which of
the twelve areas are satisfied here, by another source or by a justified exclusion.
For an update, record changed sources and the affected decisions, views, tests and
evidence. Mark stale claims for reassessment; unchanged areas need no gratuitous
redesign. Record actual implementation deviations and their disposition separately
from the target description.
