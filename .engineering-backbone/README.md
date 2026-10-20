# Engineering Backbone tooling

This is a directory, not an IDE file or product runtime. Its source, tests, schemas,
standards and locked Python dependencies support the common engineering checks.
Canonical human policy is [docs/agent-governance/core.md](../docs/agent-governance/core.md).

- `src/`: validator and runtime checks; `src/maintenance/`: checked-output compilers.
- `tst/`: the existing tooling regression suite and immutable historical fixtures.
- `schemas/` and `standards/`: governance contracts and reviewed catalogs.
- `requirements.txt` and `requirements.lock`: this toolchain's dependencies.
- `core.json`: shared invariants; `project.json`: reviewed project facts.
- `opencode.json`: inactive adapter companion; copying does not activate it.
- `legacy/`: compatibility material for existing Copier consumers.

Start with the root [README](../README.md) and [adoption guide](../docs/agent-governance/adoption.md).
Keep application dependencies in their component manifests. Do not replace local
project policy or claim old Backbone evidence as evidence for a new application.
