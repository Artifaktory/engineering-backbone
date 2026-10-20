# Architecture document kit

Use this kit with the [architecture contract](../../agent-governance/architecture.md).
It supplies questions and record shapes, not a preselected application architecture.
The [source record](../../agent-governance/architecture-sources.md) explains which
public standards and methods informed the Backbone rules and their adoption limits.

## Start here

1. Declare the project's authoritative sources, responsibilities, ID conventions and
   tool mapping using [project mapping](project-mapping.md).
2. Take the scoped requirements from their existing authoritative home. Record their
   architecture treatment in [traceability](traceability.md); identify the drivers
   and unresolved decisions before selecting a solution.
3. Write the smallest useful [architecture description](architecture.md), with
   [quality scenarios](quality-scenario.md) and [significant decisions](decision.md)
   where needed. Reference existing information instead of copying it.
4. Plan verification while designing. Use [review](review.md) to assess the actual
   frozen inputs and the requested gate. Update implementation and result evidence
   only when the corresponding work has occurred.

The [worked example](worked-example.md) illustrates a complete derivation with open
questions. It is fictional, draft, unimplemented and unverified; copying it does
not create product requirements or evidence.

## Choose locations without duplicating authority

| Logical information | Suggested project location when none exists |
| --- | --- |
| Source ownership, revision, index and tool mapping | `docs/architecture/README.md` |
| Architecture description and view index | `docs/architecture/architecture.md` |
| Significant decision history | `docs/architecture/decisions/` |
| Quality scenarios | Existing requirement source; otherwise an identified project record linked from the architecture |
| Requirement/design relationships | Existing traceability source; otherwise `docs/architecture/traceability.md` |
| Frozen review, findings, triage and results | `docs/changes/<delivery>/` |

These are placement defaults, not mandatory filenames or tools. Requirements stay
in their authoritative source, commonly `docs/requirements/`; project quality
documents remain authoritative for their rule/test/evidence records. An architecture
building block need not correspond to a directory. Code and test locations follow
the project's repository conventions and are linked when implementation exists.

Blank common templates remain Backbone-owned. Copy selected templates into
project-owned records and repair their relative links, or map equivalent information
in another format. Legacy Copier installs the common kit under
`.engineering-backbone/architecture-templates/`; do not write live project design
inside that managed directory.

## Tailoring and completion

The twelve content areas in the architecture template may be combined in one short
document, split, or satisfied by links to existing sources. For a non-applicable
area give a reason and owner; an empty heading or `N/A` alone is insufficient.
Use additional views where project risks need them. No framework, component count,
diagram tool or fixed number of alternatives is prescribed.

Replace every `TBD` in the scope of a requested gate with an actual value or an
explicit open item, owner and effect on that gate. Templates begin as drafts.
Do not infer requirement approval, design acceptance, implementation or verification
from the existence of a file, a filled table, a diagram build or a structural PASS.
Existing JSON schemas are unchanged; keep additional metadata in linked companion
records rather than adding unsupported keys. This kit is a semantic review aid,
not an installed architecture validator or authenticated approval system.
