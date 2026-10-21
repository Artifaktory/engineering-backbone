# Planning and delivery contract

This is the shared semantic contract for turning product goals, requirements and
architecture into reviewable plans and executable work. Agents and human reviewers
apply it with the [core policy](core.md) and [architecture contract](architecture.md).
Use the [planning document kit](../templates/planning/README.md) to record the
required information in the project's chosen tools and authoritative locations.
The contract does not install a planning engine, tracker integration or orchestrator.

**Authority:** MUST describes a Backbone-owned obligation under the adopted core,
not a quotation from an external standard. Source notes identify the guidance that
informs each group; [the source register](planning-sources.md) distinguishes public
normative scopes, optional methods and local precedents. No full-text ISO clause
conformance, certification or performance of a complete named method is claimed.

## PLAN-01: Proportionate planning and authority

Use the smallest useful delivery depth: a direct PR plan for a small change, a
feature plan for related deliveries, or a program plan for actual multi-delivery
coordination. A direct change may combine plan, item and review records in one
short document. Project size, risk, uncertainty and dependencies determine detail;
a fixed hierarchy, document count, story-point scale or timebox is not required.

The project MUST identify the authorized objective, scope, decision owners and
applicable stronger controls. Plan the overall delivery sufficiently to expose
material gaps; refine near-term work into startable items while later work can
remain coarser. Stories and design experiments can inform this planning. Review the
necessary delivery strategy before dispatching dependent implementation; do not
require a complete detailed backlog before learning or incremental delivery.

Unanswered questions MUST have an owner, next action and gate impact. If a required
product or design decision is unresolved, either block affected work or authorize
a bounded investigation with a question, budget and expected decision evidence.
Do not turn an assumption into an approved requirement or approval into test proof.
A scoped planning Task Packet can authorize that investigation before a delivery
plan exists. Routine choices within an accepted scope do not require extra human
approval solely because this contract asks that they be documented.

Source note: Backbone rule informed by [P-S01, P-S02, P-S04 and P-S07](planning-sources.md#reference-register).

## PLAN-02: Terms, lineage and source ownership

| Record | Meaning and boundary |
| --- | --- |
| Product goal / vision | Desired stakeholder outcome and reason to invest; its owner sets value and priority. |
| Requirements / architecture | Authoritative obligations, acceptance, significant decisions, interfaces and verification intent; retain their existing sources and revisions. |
| Delivery plan | How the authorized outcome will be reached through useful increments, responsibilities, dependencies, risk treatment and evidence. |
| Work package | A coherent portion of planned scope; it may contain several delivery items and is not automatically one issue. |
| Delivery item | A bounded, observable result: user story, technical enabling work, bug repair, migration or investigation. |
| User story | One kind of delivery item expressing stakeholder value. Use a meaningful vertical slice where practicable; a technical layer is not automatically an independently useful story. |
| Task | An execution step within an item. Give it a separate tracked item only where independent result, review, ownership or coordination warrants it. |
| Issue | A tracker representation of reviewed work, with a link to its authoritative content and revision. |
| Task Packet | A particular authorized planning, implementation, check or review assignment with execution scope, actual revisions, budget and stop conditions. |

Relationships MAY be many-to-many. An item can address several requirements; one
requirement may need several items and integration evidence. Record stable IDs and
resolvable source revisions; do not invent missing requirements or infer approval
from a reference. Preserve the architecture contract's requirement dispositions.
Plans and issues MUST link authoritative requirements/design rather than maintain
contradictory copies. A tracker may itself be authoritative if the project declares
its revision, edit ownership and export/traceability mechanism.

Issue count, work-package count and PR count need not match. Select a coherent,
reviewable change size that leaves a valid intermediate state. A project may adopt
one-item/one-PR guidance, but that is a local convention, not a universal standard.

Source note: Backbone terms informed by [P-S03, P-S04, P-S05 and P-S12](planning-sources.md#reference-register).

## PLAN-03: Delivery-plan content

The plan MUST address the following, directly or through precise existing links.
Mark genuine non-applicability with a reason; do not silently omit required work.

| Question | Required information for the planned scope |
| --- | --- |
| Why and what? | Observable goal/benefit, current state, intended result, included scope and explicit exclusions. |
| From which inputs? | Requirement, architecture/decision, quality-scenario and constraint IDs/revisions; owners, assumptions, open questions and their disposition. |
| Which deliveries? | Useful increments, work packages/items at appropriate detail, priorities, entry/exit conditions and coverage of the authorized scope. |
| Is it feasible? | Dependencies and external inputs, required skills/access/environments, capacity and effort/time/cost assumptions with uncertainty; avoid unsupported precision. |
| Who decides and integrates? | Delivery and integration owners, implementation responsibilities, required/optional independent reviewers and applicable human decisions. |
| Which risks and qualities? | Relevant security/privacy, reliability, performance, usability/accessibility, operability, compatibility and maintainability concerns; mitigation or justified non-applicability. |
| How is success established? | Acceptance-to-verification mapping, methods, environments/data, responsible checkers, thresholds where needed and expected evidence locations. |
| How is it delivered safely? | Integration sequence/configurations, rollout, migration and recovery where applicable, documentation/operational impact and completion conditions. |
| How is change controlled? | Source revision, review state, open blockers, stop/return conditions and the process for scoped replanning. |

Use the [delivery-plan template](../templates/planning/delivery-plan.md). Select
required verification during planning under [the quality policy](../quality/policy.md)
and the project's adopted test strategy.
Tests are not generally optional merely because a prompt did not explicitly ask
for them. Required coverage follows behavior and risk; documentation-only changes
can use suitable document checks. Include security work throughout relevant design,
implementation and verification, not solely as an optional final polishing phase.

Source note: Backbone minimum content informed by [P-S02, P-S06, P-S07 and P-S09](planning-sources.md#reference-register); these fields are not asserted to reproduce an ISO mandatory-field list.

## PLAN-04: Decomposition and coverage

Review decomposition before treating its dependent items as ready to execute.
Every in-scope requirement, material risk, design obligation and planned delivery
MUST have an explicit disposition: mapped work/verification, existing verified
coverage with justified applicability, approved deferral, or a visible gap/blocker.
Trace from sources to items and from items back to authorized sources or approved
risk/maintenance rationale. Integration, tests, documentation, deployment preparation
and recovery work count as real scope where needed; do not leave them ownerless.

Split work when separate results can be implemented and reviewed coherently, when
risk or ownership requires different gates, or when a smaller increment provides
useful feedback. Keep work together when it shares an indivisible contract change,
requires one atomic migration/recovery operation, has no valid intermediate state,
or would otherwise duplicate unresolved decisions. Document the reason for a
material split or coupling. Do not require all stories to wait behind a generic
foundation phase; identify the actual prerequisites for each item.

For user-facing work, use INVEST as a quality prompt and optional story mapping to
keep the overall user outcome visible. Full independence is not always attainable.
Technical work and investigations need explicit outcomes and acceptance without a
fictional user persona. An investigation ends in findings/decision evidence, not an
unfounded promise of a production feature.

Use the [decomposition record](../templates/planning/decomposition.md) for coverage,
boundaries and dependency links. A coverage matrix establishes declared relationships;
independent review still assesses whether the work and proposed checks are adequate.

Source note: Backbone rule informed by [P-S03, P-S05, P-S07, P-S10 and P-S12](planning-sources.md#reference-register).

## PLAN-05: Dependency and parallel-work contract

Work breakdown answers **what belongs to the delivery**. A dependency graph answers
**what may start when**. Record both where coordination needs them; a small direct
change can use a short table. Directed prerequisite edges MUST be acyclic. Resolve
cycles through changed decomposition, a prior contract/decision or an explicit
joint atomic delivery; do not hide the cycle by deleting a real dependency.

| Dependency kind | Start condition to record |
| --- | --- |
| Contract available | Required approved interface/data/state/error/security contract and its revision are available; a producer implementation may still be pending. |
| Implementation available | Required producer result exists at an identified revision/configuration and meets the stated input acceptance. |
| Integrated prerequisite | Required combined behavior is integrated and has the specified actual evidence. |
| Shared resource / conflict | Identify overlapping writes, mutable contracts, generated outputs, databases, environments, capacity or authority; assign sequencing, exclusive ownership or isolation. |

Every parallel group MUST state the input/output contracts, read/write/exclude
boundaries, unresolved conflicts, start criteria and integration responsibility.
Different files or branches alone do not prove independence. Consider shared APIs,
types, schema migrations, lockfiles, generated code and external state. Starting a
consumer against a stable contract or mock can be valid; that evidence remains
limited to that contract/mock until the real interaction is checked.

Plan the integration order, target configuration, compatibility strategy and
assembled-system acceptance. Designate who coordinates integration and handles
conflicting changes. Before each start, confirm its actual prerequisites still
hold. Limit work in progress to available implementation, review and integration
capacity; a greater number of active workers is not itself a delivery goal.

A contract change MUST trigger PLAN-08 impact assessment before dependent work
continues under outdated assumptions. Pause affected assignments, revalidate their
contracts/inputs and arrange the needed renewed checks. Independent unaffected
work may continue within its authorization. Item-level checks do not establish
whole-system acceptance; include actual integration and critical end-to-end evidence.

Source note: Backbone engineering contract informed by [P-S06, P-S08, P-S11 and P-S12](planning-sources.md#reference-register). These dependency kinds are our explicit adaptation, not a prescribed external schema.

## PLAN-06: Delivery items and execution packets

Each executable item MUST identify its ID/type/revision, parent plan or objective,
source requirements/design, observable result, authorized scope/exclusions,
responsible owner, interfaces, prerequisite conditions and relevant conflicts.
Record its risk, acceptance criteria, required automatic/manual/hybrid checks,
environment/data/access needs, evidence expectations, review responsibilities,
integration/recovery obligations and stop/return conditions. Use the
[delivery-item template](../templates/planning/delivery-item.md); type-specific
prompts cover stories, technical work, bugs, migrations and investigations.

Before dispatch, bind this work to a [Task Packet](../../.engineering-backbone/schemas/task-packet.schema.json)
and provide the actual approved content, not only a title or inaccessible issue URL.
The [pending example](../templates/examples/task-packet.json) illustrates supported
fields. The packet MAY narrow a reviewed item; it MUST NOT silently broaden its
objective, permissions or scope. A different run/review assignment has a distinct
identity or explicitly versioned record; retain previous evidence and outcomes.

Ownership, parent-item, dependency, interface and integration metadata do not have
dedicated fields in the existing Task Packet schema. Record them in referenced
companion documents, using existing `approved_sources`, objective/scope and evidence
fields as appropriate. The schema has `additionalProperties: false`; this contract
does not authorize arbitrary added keys, roles or states. A later machine-readable
extension requires its own reviewed versioned migration.

The [requirement schema](../../.engineering-backbone/schemas/requirement.schema.json)
and [pending example](../templates/examples/requirement.json) keep approval,
implementation and verification separate. Preserve their states and authoritative
source. Use the [architecture decision record](../templates/architecture/decision.md)
for material design choices; local routine implementation decisions need only the
level of recording proportionate to their impact.

Source note: Backbone execution contract; [P-S06 and P-S12](planning-sources.md#reference-register) inform the planning-to-assignment distinction. Existing schemas, not external methods, define supported JSON fields.

## PLAN-07: Responsibilities, readiness and review

Identify the actual product/requirement decision authority, design authority,
planning owner, item owners, integration owner, quality checker and independent
reviewers. One person can hold compatible responsibilities where appropriate;
implementation and independent approval remain separate under the core policy.
Existing Task Packet roles apply: planner, implementer, quality_checker, reviewer
and triage. Specialized responsibilities do not create new schema roles.

| Claim or gate | Evidence needed for that claim |
| --- | --- |
| Plan/decomposition reviewable | Inputs/revisions, scope, proposed work, risks, coverage and open questions are visible; a draft can be reviewed with known gaps. |
| Item ready to start | Required source decisions are authorized, prerequisites/access are available, boundaries and acceptance/checks are defined, blocking questions are resolved or explicitly handled by an allowed project mechanism, and required plan/design/decomposition review and triage are complete. |
| Item accepted | The item's observable acceptance criteria have actual results on the recorded revision/environment, with required findings resolved. |
| Definition of Done satisfied | The adopted common quality obligations for the change are met, including relevant integration, documentation, tests and required review evidence. |
| Task Packet `ready_for_review` | The packet binds immutable base and head for review. This state is not a declaration of readiness to begin implementation. |
| Delivery complete / release permitted | Required item and integration acceptance, quality and review evidence exist; completion and separately required human merge/release decisions retain their own project gates. |

Startability is a Backbone/project readiness policy, not a Scrum-mandated artifact.
A ready implementation packet may be `active` with a known base and no final head;
review-ready and active reviewer packets require both immutable revisions. A packet
cannot be `completed` while required acceptance remains pending, failed or blocked.
Mapping words to a board column never changes these claim meanings.

Non-trivial plans need independent read-only review before implementation. Review
plan content and decomposition with [the checklist](../templates/planning/review.md),
including coverage, feasible contracts, semantic conflicts and the integration path.
Record required/optional reviewers, actual methods/coverage, limitations, budgets
and findings. Required unresolved findings or missing mandatory evidence block the
affected gate; review advice does not supply a missing product decision.

After implementation, obtain required deterministic results, freeze the same
base/head/patch digest for Full review, then triage before confirmed repairs and
bounded Delta. The [review schema](../../.engineering-backbone/schemas/review-evidence.schema.json)
and [pending example](../templates/examples/review-evidence.json) retain finding IDs
and the existing supported evidence fields. Companion reports carry additional
coverage, execution-path and patch details. A new scope or trust boundary requires
a new scoped Full under the core policy. Human merge/release and stricter local
publication controls remain separate; a schema-valid report authenticates none of them.

Source note: Backbone gates and role separation, informed by [P-S04, P-S06, P-S09 and P-S12](planning-sources.md#reference-register); the exact states and review chain are local governance obligations.

## PLAN-08: Changed inputs and stale evidence

A material change to goals, requirements, assumptions, architecture, interfaces,
risk, dependencies or acceptance MUST trigger a recorded impact assessment.
Identify old/new revisions, affected plans/items/packets, decision authority,
required reassessment and whether work must pause. Apply the architecture contract's
change process where design is affected. Reprioritization may change future scope;
it cannot silently erase required acceptance for work claimed complete.

Preserve historical decisions, review findings and results with their original
identities. Mark applicability of older evidence explicitly in the companion record
or arrange renewed checks. Do not relabel planned verification as actual evidence,
rewrite prior results, or invent unsupported JSON statuses. Closeout maps each
required acceptance and integration claim to current evidence or a visible gap.

Source note: Backbone change/evidence contract informed by [P-S01, P-S04, P-S09 and P-S12](planning-sources.md#reference-register).

## PLAN-09: Tool mapping and handoff

Declare authoritative record locations, stable IDs/revisions, editable versus
derived representations, relationships, state meanings, owners and actual gates
using the [project-mapping template](../templates/planning/project-mapping.md).
Markdown, a requirements tool, an architecture tool, a tracker or a combination can
represent this contract. Tool migrations preserve meaning/history or provide a
reviewed crosswalk; no project must adopt Sphinx-Needs, LikeC4, Spec Kit or AO.

Every human/agent handoff MUST carry the scoped Task Packet, authoritative plan/item
revision, requirement/design context, applicable rules, resolved documents,
prerequisites/conflicts, acceptance/checks, pending questions, permissions/budget
and stop/return conditions. Verify that the receiving role has and has read the
required context; use the adopted navigation procedure where active. A native
instruction file, receipt or agent reply alone proves neither client loading nor
successful execution. The orchestration owner coordinates work; it cannot invent
missing approvals or widen a worker's scope.

Document which checks are structural, which require semantic review, and which need
actual runtime evidence. This kit supplies shared content and review questions;
it does not implement semantic validation, automatic issue projection, scheduler
safety or a provider integration. The source projects' micro/standard/critical
packet engines and authenticated publication mechanisms remain project-local.
Use available native procedures with the existing role mapping and current project
facts; preserve their independent review, triage, budget and human-decision rules.

Source note: Backbone interoperability and handoff contract informed by [P-S01, P-S06 and P-S12](planning-sources.md#reference-register).

## Verification evidence handoff

Use the [testing contract](../quality/testing.md) and
[CI/CD mapping](../quality/ci-cd.md) to carry planned verification into reproducible
procedures, actual revision/environment-bound results and completion assessment.
Keep requirement/design acceptance, execution outcomes and delivery gates distinct;
a prepared test or workflow binding is not evidence that it ran.
