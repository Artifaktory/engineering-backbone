# Project planning source and tool mapping

Template for PLAN-01, PLAN-02, PLAN-08 and PLAN-09 in the
[planning contract](../../agent-governance/planning.md). Complete this in the
project's planning index or link equivalent existing information. The contract is
semantic and tool agnostic; this record does not install adapters or authenticate
approvals. Source/application limits are in the
[source record](../../agent-governance/planning-sources.md).

## Authority and responsibilities

| Field | Project value |
| --- | --- |
| Project boundary / mapping owner / adopted Backbone revision | `TBD` |
| Authoritative local policy and existing stricter controls | `TBD` |
| Product/scope and requirement decision owner | `TBD` |
| Architecture/contract decision owner | `TBD` |
| Planning/decomposition owner | `TBD` |
| Implementation, integration, quality and independent review responsibilities | `TBD` |
| Actual delegation, approval, merge and release authority | `TBD` |
| Actual tracker, execution hosts and supported capabilities | `TBD`; presence of a file does not prove loading or support |

Record who may make routine choices inside scope and who decides changed product
behavior, contracts, risks or scope. Preserve existing human gates without inventing
an approval for every routine step. Use a bounded planning/investigation Task Packet
when planning itself is delegated; its result can then define later execution items.

## One authoritative source per information item

| Information | Authoritative location / owner | Stable identity and immutable revision binding | Derived view / synchronization rule |
| --- | --- | --- | --- |
| Product goals, requirements and acceptance | `TBD` | `TBD` | `TBD` |
| Architecture, decisions and interface contracts | `TBD` | `TBD` | `TBD` |
| Delivery plans, work packages and item definitions | `TBD` | `TBD` | `TBD` |
| Dependencies, conflicts and coverage relationships | `TBD` | `TBD` | `TBD` |
| Issue/work-board tracking | `TBD` authoritative fields versus projections | `TBD` | `TBD` |
| Task Packets and execution attempts | `TBD` | `TBD` | `TBD` |
| Quality criteria, reviews, decisions and actual evidence | `TBD` | `TBD` | `TBD` |
| Generated tool/run outputs | `TBD` ignored root and tool/run subdirectory | `TBD` | `TBD` contents ignored, tracked README, not plans, evidence or approval |

Use existing project locations; they need not follow these template filenames.
For external systems, bind a frozen accessible export or versioned record rather
than a mutable URL alone. Define where edits occur, how derived views are refreshed,
who resolves conflicting versions and what happens when required context is stale
or inaccessible. Do not create a second independent copy of a requirement or plan.

## Identity, relations and states

| Concept | Project representation and meaning |
| --- | --- |
| Stable IDs and aliases | `TBD` goal, requirement, decision/interface, plan, package, item, issue, packet, check and evidence namespaces; preserve identity across tool changes |
| Traceability | `TBD` forward/reverse lookup; many-to-many source coverage and item purpose |
| Dependency kinds | `TBD` contract, implementation, integrated result and shared-resource conditions with version and evidence owner |
| Scope and changes | `TBD` read/write/exclude ownership, change decision and affected-item/evidence reassessment |
| Start readiness | `TBD` local start criteria and actual responsible decision; not a native Task Packet enum |
| Plan/item/tracker state | `TBD` drafts, accepted definitions, blocked work and actual execution tracking remain distinguishable |
| Verification and closeout | `TBD` planned/not-run versus observed results, actual revisions and limitations |

Retain native Backbone JSON enums and the existing quality CSV format when used.
Task Packet `ready_for_review` means a frozen review subject, not implementation
readiness. The current schema has no generic parent-item, dependency or integration
fields: store those relationships in companion records keyed by ID and link them
through supported source fields. Do not add unknown JSON keys or silently map an
unknown/blocked state to success. Repeated execution attempts have distinct identities.

## Optional tools and enforcement

| Arrangement | What the project must supply |
| --- | --- |
| Markdown or another document format | Stable IDs, inspectable links, revision binding, ownership, explicit gates and evidence records |
| Requirements/model tools such as Sphinx-Needs or LikeC4 | Reviewed source/derived mapping and stable requirement/design references; readable frozen inputs for reviewers |
| Spec Kit or another planning assistant | Mapping of generated drafts to the same authority, risk-based checks and item contracts; generic defaults cannot weaken project controls |
| GitHub Issues or another tracker | Defined authoritative fields, source item ID/revision, drift detection and synchronization owner; tracker state does not prove acceptance |
| AO or another execution host | Actual dispatch/receipt/result interfaces, supported roles/permissions, packet binding, failure/stop propagation and independent evidence |

These are conceptual mappings, not configuration syntax or installed integrations.
Choose only tools the project needs. Record actual implemented automatic checks,
manual review responsibilities and unavailable capabilities. The Backbone structural
validator does not prove planning completeness, semantic independence or safe live
parallel execution. When navigation is active, register required project context
under its existing reviewed routes and verify receipt at each scoped handoff.
Keep credentials and sensitive operational data out of public exports and evidence.
