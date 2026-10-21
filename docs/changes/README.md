# Change records and Backbone history

Keep each project's delivery plan, Task Packet, checks, independent reviews, triage
and repair evidence together under `docs/changes/<delivery>/`. New records report
actual revisions and results. A copied plan, an old PASS statement or a valid schema
is not evidence that the receiving project was checked or approved.

The active delivery is [BB-PLAN-016](backbone-planning-delivery/task-packet.json),
with its [independently reviewed plan](backbone-planning-delivery/plan.md),
[incoming review disposition](backbone-planning-delivery/incoming-review.md) and
[open consumer follow-ups](backbone-planning-delivery/follow-up-packages.md).
The merged [BB-ARCH-015 architecture delivery](backbone-architecture-contract/plan.md)
retains its original scope and evidence.
The merged [BB-LAYOUT-014 integration](backbone-layout-integration/task-packet.json),
its [incoming-file map](backbone-layout-integration/incoming-map.json), the original
[BB-LAYOUT-011 refactor](backbone-layout/task-packet.json),
[BB-LAYOUT-012 corrections](backbone-layout-corrections/task-packet.json) and
[original relocation crosswalk](backbone-layout/mapping.md) retain their recorded scope.

## Preserved earlier deliveries

The `backbone-<delivery>/plans/` and `reviews/` directories preserve earlier Backbone
records byte for byte. They describe their original snapshots, paths, commands,
authorizations and observed results. They do not authorize current work or establish
current implementation, CI, runtime qualification or release readiness.

| Delivery | Original plan at its preserved location |
| --- | --- |
| Foundation | [Bootstrap](backbone-bootstrap/plans/bootstrap.md) |
| Codex reference consolidation | [Consolidation](backbone-codex-consolidation/plans/codex-consolidation.md) |
| Codex identity security | [Security](backbone-codex-security/plans/codex-security.md) |
| Copilot development workflow | [Copilot](backbone-copilot-development/plans/copilot-development.md) |
| Shared workflow kit | [Workflow kit](backbone-workflow-kit/plans/workflow-kit.md) |
| CI clone repair | [CI repair](backbone-ci-clone-repair/plans/ci-clone-repair.md) |
| Quality framework | [Quality](backbone-quality-framework/plans/quality-framework.md) |
| Technology profiles and navigation | [Navigation](backbone-technology-navigation/plans/technology-navigation.md) |
| Dependency compatibility | [Dependencies](backbone-dependency-compatibility/plans/dependency-compatibility.md) |
| OpenCode governance | [OpenCode](backbone-opencode-governance/plans/opencode-governance.md) |
| Trusted-layout prerequisite (PR #19) | [Compatibility](backbone-layout-compatibility/plans/layout-compatibility.md) |

The compatibility delivery retains `plans/` and `docs/reviews/` beneath its own
directory so its original relative links work without rewriting recorded evidence.
All eleven records retain their exact bytes from merged main `537576f...`; the
integration map records each original Git blob and destination.

Use [layout-map.json](backbone-layout/layout-map.json) to look up an `old_path` and
its `new_path`. Each entry includes the original Git blob and byte size from base
`212608aa50ee517b3dd3107a9480da997222fd4f`. The map is a review inventory, not permission
to weaken validation or to redefine which files are historical.

Relative links inside preserved files retain their original context and may not
navigate correctly in a normal Markdown viewer. Look up their old destination in
the crosswalk or view the file at the recorded base commit. The validator resolves
these known archived links using its trusted historical mapping and verifies the
archived bytes; new files receive normal link and schema validation.

In this first refactor, keep the mapped archive together with its tooling during a
copy. Omitting or changing required archived files needs an explicit, reviewed
adoption/migration of that contract. Store the receiving project's new evidence in
its own delivery directory and replace Backbone-specific active task references in
root instructions. Never relabel inherited records as that project's results.
