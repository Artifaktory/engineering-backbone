# Testing and verification document kit

Use this kit with the [testing contract](../../quality/testing.md),
[CI/CD evidence contract](../../quality/ci-cd.md) and
[source register](../../quality/testing-sources.md). These are original Backbone
record shapes informed by the cited guidance; they do not copy normative templates,
claim certification or install a test runner, result engine or pipeline.

## Choose the smallest useful record

| Need | Record or equivalent authoritative information |
| --- | --- |
| Decide what, why, how and when to verify | [Test strategy/plan](test-strategy.md) |
| Describe an observable test or verification procedure | [Test design](test-design.md), or identified executable tests |
| Record an actual execution and its limitations | [Test run](test-run.md) |
| Assess coverage, findings and exit criteria | [Test completion](test-completion.md) |
| Connect evidence obligations to actual workflow checks | [CI mapping](ci-mapping.md) |
| Independently review the requested plan or result gate | [Review checklist](review.md) |

The [worked example](worked-example.md) follows draft requirements through planned
component/integration checks and CI mapping. It has no executed results or approvals.

A small change may combine applicable questions in one short document. A larger
project may use existing tools and linked records. No fixed file count, test count,
coverage percentage, tool, development method or pipeline topology is prescribed.
Existing stronger controls and adopted profile duties still apply. Record genuine
non-applicability with a reason and responsible owner; unresolved decisions retain
an owner, next action and effect on the requested gate.

## Ownership, placement and update

| Information | Suggested home when no established authority exists |
| --- | --- |
| Project quality goals and overall test strategy | Existing quality plan and `docs/quality/test-strategy.md` |
| Detailed automated tests | The project's native test sources and discoverable IDs |
| Manual procedures or test-design index | Existing test management tool or `docs/quality/` |
| Scoped runs, completion and independent review | `docs/changes/<delivery>/` |
| Raw logs and reports | Approved evidence storage, with access and retention rules |
| Actual commands and check bindings | Existing project workflow contract and CI configuration |

Keep one authority for each fact. The optional quality package already provides
project-owned quality-plan, test-strategy, traceability and exception seeds; use or
extend those records through the project's reviewed adoption. This kit does not
create another mandatory strategy or activate an inactive profile.

Common blank templates remain Backbone-owned. Legacy Copier distributes them under
`.engineering-backbone/testing-templates/`; live project results do not belong in
that managed directory. Copy selected templates into project-owned records and
repair relative links, or map equivalent tool fields. Existing project strategies,
results and native instructions require reviewed manual integration when guidance
changes; successful copying does not approve their content.

## Claims and state boundaries

Separate applicability, execution lifecycle, result, evidence validity and gate
assessment. Use the testing contract's crosswalk to existing requirement, Task
Packet, review and quality-CSV states; these Markdown prompts add no JSON fields,
roles, enums or CSV columns. An exception does not rewrite an earlier result.
A filled record, generated report, schema-valid mapping or model reply establishes
neither actual execution nor independent approval. Missing required evidence remains
visible and blocks the affected gate under the adopted policy.
