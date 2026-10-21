# Delivery item: TBD result

Template for PLAN-02, PLAN-06 through PLAN-09 in the
[planning contract](../../agent-governance/planning.md). Story-specific prompts are
informed by INVEST and Scrum (P-S04..P-S05); the common assignment contract and gates
are Backbone-owned. See the [source record](../../agent-governance/planning-sources.md).

## Identity, authority and outcome

| Field | Project value |
| --- | --- |
| Stable item ID / definition revision | `TBD` |
| Type | Story / technical enablement / bug / migration / investigation / other justified type |
| Parent plan and work-package references | `TBD` immutable revisions; shared work may serve several obligations |
| Product goal, requirements, architecture decisions and interface references | `TBD` |
| Accountable owner / intended implementer responsibility | `TBD`; assign actual identities before dispatch |
| Required/optional independent reviewers / acceptance decision owner | `TBD` applicable roles and authority |
| Risk classification / applicable quality profile and shared Done criteria | `TBD` source references and justified applicability |
| Observable result and reason for this work | `TBD` |
| Included / excluded work and deliverables | `TBD` |
| Definition state / readiness assessment | Draft / not assessed; use actual project state mapping |
| Tracker projection, if used | `TBD` item ID, source revision and synchronization owner |

## Type-specific clarification

Complete the relevant row; do not create fictional end users for technical work.

| Type | Additional information |
| --- | --- |
| User story | Beneficiary, need and value; relevant workflow and examples. Describe a small useful outcome across the necessary layers. A sentence format is optional. |
| Technical enablement | Capability or constraint enabled, supported delivery/requirement, and an independently assessable technical result. |
| Bug | Observed versus expected behavior, affected revision, reproducible trigger/impact and regression evidence required. |
| Migration | Old/new state, compatibility window, data/invariant ownership, transition order and failure/recovery criteria. |
| Investigation | Specific question, uncertainty to reduce, authorized scope, time/cost bound, expected evidence/decision record and return condition. It does not authorize production implementation. |

## Contracts, scope and prerequisites

| Read context / source revision | Allowed changes and concrete output | Excluded changes / reserved resources |
| --- | --- | --- |
| `TBD` | `TBD` | `TBD` |

| Prerequisite / contract version | Dependency kind and start condition | Evidence / owner | Current readiness or block |
| --- | --- | --- | --- |
| `TBD` | Contract / implementation / integrated result / shared resource | `TBD` | Not assessed |

Name relevant file/module boundaries and shared data, configuration, generated
artifacts or environments. Use [decomposition](decomposition.md) for conflict sets,
coordination and integration. A write-path list alone is not proof of independence.
Specify allowed local design choices and decisions reserved to an identified owner.

## Acceptance and verification

| Criterion ID / source | Observable expected result, including relevant adverse case | Verification method and procedure/check reference | Owner, environment and data | Actual result / revision / evidence |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | Automatic / manual / hybrid: `TBD` | `TBD` | Not run |

Select criterion-specific acceptance separately from the project's shared Definition
of Done. Reference required quality/security checks, documentation and traceability
updates. A mock or isolated component check supports only its tested claim; identify
which checks require real components or the integrated system.

## Integration, risks and stop conditions

Record the integration owner, compatible target/interface revisions, merge order,
required assembled-system checks and applicable recovery path. State material risks,
permissions/data boundaries and required decision gates. An unresolved prerequisite,
contract drift, scope expansion or missing authority must have an explicit stop or
return action. Define the recipient and information to return; do not guess missing
product decisions to finish a task.

## Bind an execution packet

Link each actual Task Packet to this item ID and definition revision through its
supported source/objective fields or a companion index. Record actual repository
base, allowed actions, role, check commands, budget and stop conditions there.
Keep any extra planning fields in linked records; do not add unsupported JSON keys.
Use distinct packet identities and evidence for separate execution attempts.

Task Packet `ready_for_review` requires an immutable review subject; it is not this
item's implementation-start decision. Before dispatch, verify the required source
context is accessible and received and that the selected host actually supports
the required permissions and handoff. Packet completion cannot broaden the item's
scope or replace independent review, integration acceptance or human merge/release.

## Closeout

Record actual delivered revision and outputs, acceptance evidence, shared Done
criteria, findings/triage/repairs, integration outcome and remaining work. Distinguish
implemented, verified, accepted and released claims. Missing required evidence stays
pending, failed or blocked under the selected schema; it is never inferred from
Issue closure, a merged PR or a worker's success message.
