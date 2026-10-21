# Planning and delivery document kit

Use this kit with the [planning contract](../../agent-governance/planning.md).
It supplies original Backbone questions and record shapes for people and agents.
The [source record](../../agent-governance/planning-sources.md) distinguishes public
standard scopes, methods and the Backbone-owned rules they inform. These templates
do not certify norm compliance or install a planning, tracker or orchestration engine.

## Start with the next useful delivery

1. Declare source authority, responsibility, identities and tool/status mappings in
   [project mapping](project-mapping.md), or link an existing equivalent record.
2. Carry the scoped requirements and architecture handoff into a
   [delivery plan](delivery-plan.md). Keep established requirements and decisions
   in their authoritative homes; identify open questions before promising results.
3. Use [decomposition](decomposition.md) to account for the work, meaningful delivery
   slices, dependencies, shared resources and integration. Refine near work enough
   to execute; later work may remain coarse with visible uncertainty.
4. Describe each independently assignable result with [delivery item](delivery-item.md).
   Use its appropriate type; a user story is one option. Project Issues refer to
   these reviewed items. Bind each actual execution through the existing Task Packet.
5. Apply [review](review.md) to the requested plan, decomposition or start gate.
   Preserve the existing independent Full, triage, confirmed repair and Delta chain.
   Add actual implementation and verification evidence only after execution.

The [worked example](worked-example.md) follows one fictional user outcome through
architecture inputs, a plan and parallel technical assignments to integration.
All approvals, implementation and tests remain absent. It demonstrates decisions
and dependencies, not a ready-to-dispatch product backlog.

## Choose proportional records

| Scope | Minimum useful arrangement |
| --- | --- |
| Direct change | A short combined plan/item can answer the applicable questions and link its execution packet; do not manufacture an Epic or program. |
| Feature | A delivery plan and related items, with dependency/integration information where needed. |
| Program | Coordinated plans or work packages, shared interfaces, resources and cross-delivery decisions only when the scope actually requires them. |

The same questions may be satisfied by existing records, tables or another tool.
No fixed number of files, hierarchy depth, story points, sprint duration or PRs per
story is imposed. A project may adopt stricter delivery conventions explicitly.
Document justified non-applicability with a reason and owner. For unresolved inputs,
record the owner, next decision and affected gate rather than leaving an unexplained
`TBD` or inventing approval. Routine implementation choices stay within the agreed
decision space.

## Ownership and placement

| Information | Suggested home when the project has no existing authority |
| --- | --- |
| Source mapping and planning conventions | Project planning index, such as `docs/planning/README.md` |
| Delivery plan, item definitions and decomposition | `docs/changes/<delivery>/`, or the project's established planning source |
| Product requirements and architecture | Their existing authoritative locations, commonly `docs/requirements/` and `docs/architecture/` |
| Operational tracking | The chosen tracker, with stable links to reviewed item revisions |
| Execution packets, reviews, triage and evidence | The delivery's project-owned record directory |

These are placement suggestions, not paths created by this kit. Keep one authority
per information item and identify derived tracker/rendered views. Copy selected
blank templates into project-owned records and repair relative links there. Common
templates stay Backbone-owned; legacy Copier installs them under
`.engineering-backbone/planning-templates/`. Do not place live project plans in that
managed directory.

Existing Task Packet, requirement, review JSON and optional quality CSV schemas
remain unchanged. Additional planning relationships belong in linked companion
records. In particular, Task Packet `ready_for_review` binds a review snapshot; it
does not mean implementation may start. A filled template, successful documentation
build, valid schema or agent reply does not establish semantic fitness, loaded
instructions, human approval or executed behavior.
