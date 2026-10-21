# Product architecture

This is the default home for the actual project's architecture. Follow the
[requirements-to-architecture contract](../agent-governance/architecture.md) and
start with the [reusable document kit](../templates/architecture/README.md).
Existing project sources may remain authoritative elsewhere; register their paths
and tool mappings instead of copying a second specification here.

When a project starts, replace this placeholder with its scope, owners, requirement
sources and revisions, target/observed state, document index and open decisions.
The [architecture template](../templates/architecture/architecture.md) covers
stakeholders, constraints, context, strategy, building blocks, runtime, deployment,
crosscutting concepts, decisions, quality, risks and terminology. Several topics
may share a file or link existing documents; justify non-applicability.

Keep significant decisions under `decisions/` or the project's declared equivalent.
Quality scenarios may stay with requirements if that is their authoritative home.
Traceability points to requirements, decisions, views, planned checks and actual
evidence. Frozen delivery reviews belong in `docs/changes/<delivery>/`.

No product architecture, approval or implementation is asserted by this placeholder
or the hypothetical example in the document kit. Architectural elements describe
responsibilities and relationships; they are not automatically source directories.

Use the [planning contract](../agent-governance/planning.md) and
[planning kit](../templates/planning/README.md) to connect these authoritative
records to delivery outcomes, dependencies and acceptance. Planning references
source revisions; it does not create a competing requirement or design authority.
