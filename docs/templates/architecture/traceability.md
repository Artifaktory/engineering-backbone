# Requirements-to-architecture traceability

Template under the [architecture contract](../../agent-governance/architecture.md).
This is a semantic record shape, not a new JSON/CSV schema. Use equivalent relations
in an existing project system if identity, authority, state and coverage remain
inspectable in both directions.

| Record control | Project value |
| --- | --- |
| Scope and owner | `TBD` |
| Complete scoped requirement set / authoritative query or list | `TBD` |
| Requirement source revision / immutable export | `TBD` |
| Architecture source revision and represented state | `TBD`; target or observed, explicitly identified |
| Relation authority / tool mapping | `TBD`; see [project mapping](project-mapping.md) |
| Last impact assessment and reviewer reference | None yet |

## Requirement disposition

Account for every requirement in the declared scope, including nontechnical ones.
Use a design link, justified existing coverage, justified no architecture impact,
or an explicit open/deferred item. Deferral needs the applicable authorized scope
decision; it does not turn missing required coverage into completion.

| Requirement ID and authoritative locator | Approval state / source revision | Architecture treatment and rationale | Driver/scenario, decision, element/interface/view references | Open action, owner and gate effect |
| --- | --- | --- | --- | --- |
| `TBD` | Draft / `TBD` | Open | None yet | `TBD`; blocks the affected completion claim |

"No architecture impact" requires a reason and appropriate non-architecture
fulfillment/verification route. Existing coverage identifies the actual design
and why it suffices. A missing row is a gap, not implicit non-applicability.

## Relations and verification

| Source ID | Relation meaning | Target ID / authoritative locator | Source and target revisions | Basis / current applicability |
| --- | --- | --- | --- | --- |
| `TBD` | Drives, refines, addressed by, realized by, checked by, supersedes, or another declared meaning | `TBD` | `TBD` | `TBD` |

Relationships are many-to-many. One decision may address several requirements; one
requirement may depend on several elements, scenarios and checks. Not every
requirement needs its own ADR. Every significant design addition needs a requirement,
constraint, risk or justified enabling responsibility as its basis.

| Requirement / criterion / scenario | Planned verification and owner | Actual implementation reference | Execution state and result | Evidence identity, tested revision and limits |
| --- | --- | --- | --- | --- |
| `TBD` | `TBD` | Not established | Not run | None |

Preserve separate requirement approval, implementation and verification states.
Link a test specification as a plan; link an executed report as evidence only after
execution. If a source changes, assess affected relations and results before using
them for the new claim. Existing results remain historical evidence, with their
original revision and scope.

## Impact and consistency assessment

Record the changed source IDs and versions, affected decisions/views/interfaces,
planned or actual checks, responsible owners and outcome of reassessment. Inspect
both forward coverage and reverse justification. Resolve dangling references,
inconsistent aliases, stale exports and conflicting source authority. Check that
runtime interactions, data ownership, deployment and static boundaries agree.

## Existing Backbone machine contracts

If a project uses Backbone requirement JSON, use its existing schema fields and
values unchanged. Put provenance, owner, hierarchy, relation and architecture
metadata in linked companion records keyed by the stable requirement ID unless a
separately reviewed schema migration supplies them. Do not add unsupported keys.

If the optional quality framework is adopted, its existing CSV header remains:

```text
rule_id,requirement_id,risk,architecture,tests,check_ids,evidence,status
```

Its statuses remain `pending`, `planned`, `verified`, `gap`; multiple references
use `;` as the existing contract defines. Reference the authoritative architecture
and requirement sources from that matrix. Do not replace it with this Markdown
table or interpret `verified` as design approval. Required executed evidence and
the quality framework's own checks remain binding. A populated relation, nonempty
file or schema-valid row cannot establish semantic fitness or test success.
