# Open consumer follow-up packages

These are planning records, **not executed deliveries, created tracker issues or
approved releases**. They preserve the incoming review's remaining useful work.
The user accepted retaining consumer suitability as a work package; concrete
implementation is outside BB-PLAN-016. A future scoped task identifies its owner,
base, decision authority and independent review before implementation.

## CONSUMER-EXPORT: neutral seed and reviewable updates

**Outcome:** a new project receives the same reference directory layout and current
engineering obligations without foreign active task references or mandatory
Backbone delivery history. Existing consumer-owned files and stronger policy remain
authoritative. Product tools and stack stay optional.

**Current constraint:** the source validator requires mapped historical records;
layout compatibility tests preserve 152 entries from a 495-file crosswalk. Deleting
the archive or setting a candidate-owned mode flag is not a safe implementation.

**Work and deliverables:**

1. Independently design source/tooling/consumer ownership, the export manifest and
   trust/bootstrap contract. Identify which histories and legacy maintenance assets
   a consumer can omit while preserving current obligations and source regression
   coverage. Define validation from trusted executable authority, not a consumer
   switch that disables checks.
2. Export into a new empty destination, preserving the agreed paths. Neutralize
   project metadata and active entrypoints; use pending project-owned evidence.
   Record source commit, included content identities, omissions and local decisions.
3. Omit or explicitly deactivate workflows until runner, upload, permission and
   required-check choices are reviewed. Preserve native host locations and prove
   relevant discovery separately; no automatic agent or provider activation.
4. Support a reviewable difference against a later pinned source and local edits.
   Report conflicts and obsolete managed files. No automatic downstream apply.

**Acceptance:** a clean minimal export validates under its reviewed consumer
contract without the source archive; ordinary product manifests/fixtures remain
independent; current mandatory policy cannot be removed through manifest/mode
tampering; no active foreign task/PASS/history authorizes work; excluded workflows
cannot start on first push; an update preserves project-owned work and fails visibly
on conflicting authority. Exercise fresh copy, negative bootstrap, overwrite
refusal, update conflicts and supported Linux/Windows behavior. A manifest alone
is not semantic approval or execution evidence.

**Dependencies and review:** design/trust review precedes exporter and validator
implementation; an export owner and security reviewer are required. Source and
consumer validation need distinct coverage. Recovery is discard of an unadopted
export or a reviewed revert of the consumer adoption PR.

## CONSUMER-PROFILES: optional project-specific stacks

Separate selectable items, after the generic contract can be adopted safely:

| Item | Outcome and acceptance |
| --- | --- |
| Local CI with no uploads | A project-selected runner/permission/evidence profile exercises its actual required checks on verified local hosts, with no hosted fallback or GitHub artifact storage; runner isolation and retention are reviewed. This PR's source-only configuration does not install this profile in consumers. |
| Mastra/TypeScript | A real selected application layout, native manifests/lock/build inputs, tests and documented component boundaries; verify the chosen versions rather than impose them on unrelated projects. |
| Requirements/architecture tooling | Optional Sphinx-Needs/LikeC4 or alternative mapping preserves IDs, ownership, revisions, relationships, gaps and status meanings through a real document build; rendered output is not approval or product verification. |
| Shared skill source | Reviewed canonical procedures distribute to each selected host's native discovery locations; prove loading and applicable boundaries per host. A shared directory or successful copy is insufficient. |

Profiles may depend on the neutral-export work for distribution, but their product
requirements and host choices require their own scoped decisions. None is silently
mandatory for a documentation project, desktop application or other stack.
