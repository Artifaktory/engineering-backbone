# Delivery decomposition and parallel-work map: TBD scope

Template for PLAN-04 and PLAN-05 in the
[planning contract](../../agent-governance/planning.md). Backbone combines WBS-style
scope accounting (P-S03, P-S07), NASA dependency/integration planning (P-S06, P-S08)
and capacity-aware flow (P-S11). These are adapted engineering rules; see the
[source record](../../agent-governance/planning-sources.md).

## Subject and boundaries

Record the plan ID/revision, source requirement/architecture revisions, author,
decomposition owner, requested review gate and current state. Explain the selected
depth. Work packages describe grouped scope; delivery items describe assessable
results. Issues and execution packets are linked representations, not automatic
one-to-one substitutes for every work-package or implementation step.

## Work coverage: what belongs to the delivery?

| Work package | Result / inclusion / exclusion | Delivery items and relation | Requirement / architecture / acceptance basis | Owner |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

| Scoped obligation or planned outcome | Item(s) or justified existing coverage | Planned verification / evidence owner | Gap, deferral or decision reference |
| --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` |

Check both directions: every scoped obligation has a treatment, and every proposed
item has an authorized purpose. Include integration, documentation, quality,
security, migration and operational work where applicable. Shared work may address
several requirements; a single requirement may need several items and checks.

## Explain split and grouping decisions

Split where outcomes can be reviewed, integrated or recovered independently, or
where risk and required expertise justify distinct responsibility. Group work when
there is no valid intermediate state, a contract transition must be atomic, or
separate delivery would create an unsafe migration/recovery sequence. Record the
reason and planned integration, including any provisional interface assumption.

Small PRs and vertical user-value slices are useful goals, not arbitrary universal
quotas. Technical subassignments within one story need not be independently usable
user stories. Avoid dividing work solely by files, layers or available agent count.

## Dependency graph: what can start when?

| Prerequisite result / source item | Dependent item | Kind | Exact version and satisfied-when condition | Evidence / decision owner | Current state |
| --- | --- | --- | --- | --- | --- |
| `TBD` | `TBD` | Contract / implementation / integrated result / shared resource | `TBD` | `TBD` | Not assessed |

Define edge direction as prerequisite to dependent. Contract availability can permit
parallel producer/consumer implementation; integration still waits for both actual
results. An implementation dependency may require a built library or executable
fixture; an integrated dependency requires evidence on the specified target.
Shared resources need an explicit coordination rule, not a false claim that one
feature semantically depends on another. Resolve cycles by redesigning/grouping work
or recording a bounded exploratory step before execution; do not silently drop edges.

## Conflicts and available capacity

| Shared resource / conflict set | Affected items and read/write ownership | Coordination or serialization rule | Owner / release condition |
| --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` |

Consider interface definitions, database schemas, shared state, generated outputs,
dependency locks, routing, test environments and deployment targets as well as files.
State available implementation/review/integration capacity and the work-in-progress
limit or selection rule. Separate branches do not isolate shared runtime resources.

## Integration and failure response

| Integrated outcome / item | Integration owner and target | Required inputs / compatible versions | Merge and test order | Acceptance / recovery evidence |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | `TBD` | `TBD` | Not run |

Define compatibility/default-state assumptions, assembled-system verification,
documentation updates and any rollout/migration/recovery sequence. Record who stops
affected assignments when a contract changes, how already completed work is checked
for impact and which checks must be repeated on the assembled revision. Preserve
earlier results with their original scope. A successful isolated test does not close
an integration edge.

## Review conclusion and dispatch boundary

Use [review](review.md) to record actual coverage, blockers and the appropriate
owner's decision for this revision. List executable items separately from planned
or blocked items. Before dispatch, bind the accepted definition and required context
to each Task Packet. Record later changes in this map and synchronize derived Issues;
never treat a stale tracker label as satisfying a prerequisite.
