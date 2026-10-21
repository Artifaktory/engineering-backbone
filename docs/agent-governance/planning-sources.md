# Planning source provenance

The public primary references below were inspected on **2026-10-21**. They inform
[the planning and delivery contract](planning.md) and its original Backbone
prompts. They do not prescribe these templates verbatim. Links near each rule group
show the source IDs that inform it so readers can inspect its basis.

The ISO entries use published editions and publicly available descriptions of
scope. Full normative texts, complete required-field lists and clause conformance
were not assessed. A future clause-based or regulated project profile needs the
full applicable material, qualified interpretation, an applicability assessment
and its required independent evidence. Structural PASS or an agent review supplies
none of those claims. Draft/future revisions are not silently adopted.

## Reference register

| ID and primary source | Kind and material used | Backbone use and limit |
| --- | --- | --- |
| **P-S01 — [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html)** | Published software lifecycle standard; public scope includes concurrent, iterative and incremental application and agile approaches, without prescribing a lifecycle model or document format. | Supports a connected, revisable process. The particular Backbone handoff, record names and readiness rules are our implementation choices. |
| **P-S02 — [ISO/IEC/IEEE 16326:2019](https://www.iso.org/standard/75276.html)** | Published project-management standard, confirmed in 2026; public scope describes required project-management-plan content and technical management processes across sizes/methodologies. | Direct planning anchor. PLAN-03 is a Backbone content contract informed by this scope and public engineering guidance; it is not an asserted transcription of all ISO mandatory fields. |
| **P-S03 — [ISO 21511:2018](https://www.iso.org/standard/69702.html)** | Published guidance for work breakdown structures, their concepts, characteristics and relationships across project types/sizes. | Supports explicit work-scope decomposition. It does not prescribe our item types, issue hierarchy, tool or dependency schema. |
| **P-S04 — [Scrum Guide, November 2020](https://scrumguides.org/scrum-guide.html)** | Framework; Product Goal, Product Backlog/refinement, Sprint Planning, Sprint Backlog and Definition of Done sections. | Goal-led incremental delivery, continuing refinement and shared quality. Scrum does not mandate a User Story sentence, Epic hierarchy or formal Definition of Ready; Backbone readiness and independent-review gates remain local rules. |
| **P-S05 — [Bill Wake, INVEST in Good Stories and SMART Tasks, 2003](https://xp123.com/invest-in-good-stories-and-smart-tasks/)** | Original practical heuristic for valuable, negotiable, small, estimable, testable and preferably independent stories. | Prompts for useful delivery slices. Independence is desirable rather than universally attainable; INVEST is not a norm or a substitute for technical dependency analysis. |
| **P-S06 — [NASA Systems Engineering Handbook: 6.1 Technical Planning](https://www.nasa.gov/reference/6-1-technical-planning/)** | Public engineering guidance on tasks, technical effort, work breakdown, dependencies, resources, responsibilities and planned outputs. | Informs plan questions, entry/exit criteria and planning-to-work-assignment handoff. We adapt the ideas proportionately; NASA organizational approvals and mission procedures are not imposed on every project. |
| **P-S07 — [NASA Work Breakdown Structure Handbook, November 2021](https://www.nasa.gov/wp-content/uploads/2023/08/nasa-work-breakdown-structure-handbook.pdf)** | Public practice for authorized scope, work breakdown/dictionaries, requirements relationships, progressive detail and integration work. | Informs scope coverage, explicit boundaries and justified decomposition depth. The Backbone templates are original; using them does not claim NASA process compliance. |
| **P-S08 — [NASA Systems Engineering Handbook: 5.2 Product Integration](https://www.nasa.gov/reference/5-2-product-integration/)** | Public guidance on planning and verifying the assembly of interacting products. | Informs interface/configuration prerequisites, integration responsibility and assembled-system evidence. Individual component success is insufficient for combined-system acceptance. |
| **P-S09 — [NIST SP 800-218, SSDF 1.1, Final, February 2022](https://csrc.nist.gov/pubs/sp/800/218/final)** and [public text](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) | Secure-development recommendations; especially PO.1.2 security requirements, PO.4 security-check criteria, PW.1.1 risk modeling and PW.1.2 requirements/risk/design-decision records. | Informs early risk-based security planning and evidence mapping. It supplies no universal story schema. The [SSDF 1.2 initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) is not adopted as a final standard here. |
| **P-S10 — [Jeff Patton, The New User Story Backlog Is a Map](https://jpattonassociates.com/the-new-backlog/)** | Practical story-mapping method preserving user activities, context and release slices. | Optional way to expose user-flow coverage and useful increments. A user-flow sequence does not determine the technical build/dependency sequence. |
| **P-S11 — [The Kanban Guide, May 2025](https://kanbanguides.org/the-kanban-guide/2025.5/)** | Flow framework; explicit Definition of Workflow, work-in-progress control, capacity and active flow management. | Informs bounded parallel work and visible blockers. Backbone does not mandate a particular board, number of workers, WIP limit or scheduling product. |
| **P-S12 — Artifaktory and Tars planning contracts**, pinned below | Existing project conventions and repository evidence, not external norms. | Reuse the clarified distinction between work package, delivery item, issue and run-specific packet, with dependency/conflict and integration review. Do not import domain facts, tool dependencies, fixed phase counts or project-specific authorities. |

For a system that includes substantial non-software elements, the project may also
assess [ISO/IEC/IEEE 15288:2023](https://www.iso.org/standard/81702.html). It is an
optional system-lifecycle scope consideration, not an additional mandatory profile
installed by this kit. The existing architecture source register remains the
reference for requirements and architecture foundations.

## Pinned project precedents

- Artifaktory `981c9dbc68fdd44acbf25a5351208d9d467b4789`:
  [planning contract](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/agent-governance/planning/README.md),
  [implementation-plan review](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/agent-governance/review-catalogs/implementation-plan.md),
  [decomposition review](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/agent-governance/review-catalogs/delivery-decomposition.md)
  and [delivery issue form](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/.github/ISSUE_TEMPLATE/agent_delivery.yml).
- Tars `9e91f8c16d747d5a58890d0d16e4c3cf7078b942`:
  [planning entry](https://github.com/Artifaktory/Tars/blob/9e91f8c16d747d5a58890d0d16e4c3cf7078b942/docs/agent-governance/planning/README.md),
  [plan standard](https://github.com/Artifaktory/Tars/blob/9e91f8c16d747d5a58890d0d16e4c3cf7078b942/docs/agent-governance/planning/20-plan-package-standard.md),
  [decomposition standard](https://github.com/Artifaktory/Tars/blob/9e91f8c16d747d5a58890d0d16e4c3cf7078b942/docs/agent-governance/planning/30-delivery-decomposition-standard.md)
  and [story/issue/task standard](https://github.com/Artifaktory/Tars/blob/9e91f8c16d747d5a58890d0d16e4c3cf7078b942/docs/agent-governance/planning/40-story-issue-task-standard.md).

These snapshots demonstrate the precedent, not current product completion or an
installed Backbone planning engine. Their validators prove only the checks they
actually perform; structural validation cannot establish semantic completeness,
independent approval or safe parallel execution.

The installed Artifaktory [Spec-Kit task template](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/.specify/templates/tasks-template.md)
contains generic defaults about optional tests, a blanket foundation prerequisite,
file-based parallelism and final security hardening. Backbone instead applies its
existing risk-based testing policy and explicit dependency/security contract. This
is an assessment of that pinned project template, not a claim about every Spec Kit
release. The older [Business Stack package contract](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/business-stack/work-package-contract.md)
uses an issue/execution equivalence that the newer planning model separates; the
clarified semantics inform this kit. Local program engines and authenticated
publication controls are not transplanted by copying document templates.

## Rule-to-source crosswalk

| Backbone group | Main sources | What remains our own contract |
| --- | --- | --- |
| PLAN-01 | P-S01, P-S02, P-S04, P-S07 | Three delivery depths, explicit open-question gate handling and proportionate record combination. |
| PLAN-02 | P-S03, P-S04, P-S05, P-S12 | Precise local names and relationships, stable IDs and tracker/packet boundaries. |
| PLAN-03 | P-S02, P-S06, P-S07, P-S09 | The minimum question set, early quality dispositions and evidence expectations. |
| PLAN-04 | P-S03, P-S05, P-S07, P-S10, P-S12 | Coverage dispositions, split/couple criteria and review obligations. |
| PLAN-05 | P-S06, P-S08, P-S11, P-S12 | Typed dependencies, explicit conflict analysis, start criteria and integration responsibility. |
| PLAN-06 | P-S06, P-S12 | Existing Task Packet fields and linked companion records; no schema migration. |
| PLAN-07 | P-S04, P-S06, P-S09, P-S12 | Role separation, local readiness, distinct claims and Full/triage/repair/Delta gates. |
| PLAN-08 | P-S01, P-S04, P-S09, P-S12 | Impact-record content, stale-evidence handling and scoped stop/return rules. |
| PLAN-09 | P-S01, P-S06, P-S12 | Tool mapping, exact handoff content and distinction between declared and implemented enforcement. |

Source hints explain the rationale for our rules. They do not add external process
obligations, replace the core authority, require a named tool, or authorize weakening
stricter project controls. Projects can choose different representations and
implementation techniques while satisfying the adopted content and evidence duties.
