# BB-PLAN-016 implementation plan

## Authorization and baseline

On 2026-10-21 the user requested the agreed planning documentation and a PR,
including earlier independent-agent review points and short, accurate references
for rules informed by standards or methods. The agreed core is the five-part
planning/decomposition kit. The separate consumer audit is included as explicit
triage: confirmed bounded defects are repaired here; a neutral export and optional
technology profiles remain separately specified work, not falsely completed.

Trusted base: human-merged `main` at
`4394763d03c1d1302b6b37cef142d0f98f848be4`. Candidate branch:
`docs/planning-delivery-contract`. Work is HIGH risk because it changes shared
governance, distributed validation and source CI. The scoped Task Packet is
`task-packet.json` in this directory. No product repository is changed.

## Delivery and responsibilities

Root owns integration, triage and publication. A separate planner inspects scope;
an independent read-only reviewer reviews this plan before implementation.
Bounded implementation responsibilities may run concurrently after that review:

1. Canonical planning contract and source provenance: update the existing
   `docs/agent-governance/planning.md`, add `planning-sources.md`, connect the
   requirement/architecture handoff, ownership, iterative delivery planning,
   decomposition, typed dependencies, integration, readiness, evidence and change
   impact. Label public standard scopes, optional methods and organization-owned
   rules distinctly. Do not claim full-text clause conformance.
2. Reusable planning kit under `docs/templates/planning/`: index, delivery plan,
   typed delivery item, decomposition/dependency map, readiness/review checklist,
   project/tool mapping and a hypothetical end-to-end example. Show a user-valued
   story with parallel technical assignments and assembled-system acceptance;
   preserve open decisions and pending evidence. Small changes may combine records.
3. Distribution and entrypoints: link canonical context from core/root/quality/
   architecture/adoption guidance and native entrypoints; distribute canonical
   guidance through the retained legacy Copier templates with correct relative
   links. Preserve project-owned records and existing native instruction files.
   Do not extend JSON schemas or reinterpret `ready_for_review` as execution-ready.
4. Consumer defects: confine automatic governance-artifact recognition to explicit
   engineering roots appropriate to the trusted source/legacy layout; ordinary
   product examples/tasks/reviews/schema files must remain product-owned. Preserve
   rejection of malformed actual governance records and historical validation.
   Fix canonical path diagnostics and LF attributes for all byte-attested assets;
   extend the real autocrlf regression to the complete preservation inventory.
   Regenerate the actual rendered-tooling fingerprint and retain the immediately
   preceding reviewed digest for upgrades. Do not change historical fixture bytes.
5. Adoption and source-CI safety: correct stale draft/merge-blocker claims and the
   claim that a copied workflow cannot start. Source-only entrypoint jobs must be
   repository-bound before runner allocation. Preserve the user's local-runner and
   no-artifact-upload constraints for this PR: source jobs select explicit local
   Linux/Windows runner labels, never a hosted fallback, and remove source native
   smoke uploads. Preserve every substantive check and trusted-base check. Keep
   reusable legacy consumer workflow behavior distinct; document that those
   optional workflows require a separately reviewed local/no-upload profile.
   Do not provision runners, alter protections, execute untrusted forks locally,
   or count queued/skipped remote jobs as successful evidence.
6. Record incoming audit findings and their disposition in this delivery. Specify
   neutral export acceptance: same reference layout, no foreign active tasks or
   required source history, reviewed tooling trust/bootstrap, explicit CI selection,
   reproducible source manifest and consumer validation. Optional Mastra,
   Sphinx-Needs/LikeC4 and shared-host skill profiles remain optional follow-ups.

Parallel implementation uses nonoverlapping ownership: contract/provenance,
planning templates, validator/portability, and source CI. Root alone integrates
entrypoints, legacy distribution, fingerprint generation and delivery records.
The final fingerprint is generated only after validator and workflow edits settle.

## Acceptance and verification

- AC-1: Canonical vision/requirements/architecture-to-planning-to-delivery handoff
  is explicit, proportional, iterative and tool-agnostic, with stable identities,
  many-to-many coverage, owners and decision authority.
- AC-2: Complete reusable kit and coherent hypothetical example cover stories,
  technical work, bugs, migrations and investigations; no invented approval/PASS.
- AC-3: Source notes near rule groups map to verified primary references; public
  scope, method and Backbone rule authority remain distinguishable.
- AC-4: Source/direct-copy and legacy Copier copy/update preserve valid links,
  canonical guidance and project-owned/native files; missing required context is
  detected. Existing JSON/CSV contracts and stronger controls are preserved.
- AC-5: Ordinary product JSON/schema fixtures are accepted; malformed in-scope
  governance is rejected. All byte-attested entries survive real autocrlf checkout;
  diagnostics use portable paths. Historical identities remain unchanged.
- AC-6: Source CI has no hosted fallback or artifact upload; foreign copies/forks
  cannot allocate source jobs. Checks/trusted-base policy remain intact. Queued,
  missing native Windows/container/runtime evidence remains explicit.
- AC-7: Every incoming audit point has evidence, disposition and completion boundary;
  neutral-export/profile follow-ups have concrete scope and acceptance.
- AC-8: Required local checks, independent reviews, triage and any needed Delta are
  recorded against frozen revisions. Publish the authorized PR without merge.

Required checks: candidate validator; all four compiler checks; source dependency
check; targeted product-governance positive/negative cases; source and rendered
planning distribution and update tests; full 152-entry byte-preservation autocrlf
check; source-CI event/runner/upload contract tests; the repository's full unittest
suite; previous trusted validator from the separate merged-base checkout against
the candidate; actual base/head committed-patch whitespace check after each final
commit. Where relevant, test the previous rendered tooling upgrade fingerprint.
Use the existing isolated locked Python 3.12 environment; no dependency changes.

New checks must exercise meaningful behavior/compatibility boundaries, not merely
assert headings. The source semantic contract is independently reviewed; a link
test does not establish correct architecture, safe parallel execution or client
instruction loading. Container/provider and native Windows execution depend on
available actual hosts; record limitations rather than simulate an acceptance.

## Review and publication

After implementation, commit a fixed snapshot and record base/head/patch digest.
A separate quality checker runs deterministic checks without repairs. Independent
behavior/traceability and authority/security reviewers inspect the same frozen
snapshot after checks. Triage findings before confirmed repairs; Delta covers
confirmed IDs and directly introduced regressions. A changed scope or trust boundary
requires another scoped Full. Budget: two Full rounds, six implementation/repair
iterations. Do not retry unchanged failures to obtain green results.

Final evidence commits identify the previously inspected implementation snapshot
and publication diff; do not claim reviewers inspected their own later report.
Ensure reviewed commits are reachable in the PR history, or verify and record exact
tree/parent/patch correspondence if the publication transport changes identity.
Read back the PR and remote checks. Human merge/release decisions remain separate.

## Risk, exclusion and recovery

Primary risks: lost context during decomposition, fake normative authority,
overprescriptive templates, undocumented dependency/conflict hazards, a reduced
artifact scan hiding malformed governance, changed rendered fingerprints, broken
legacy links, and CI execution on unsuitable local hosts. Review and targeted
negative/upgrade tests address those risks. Local runner provisioning is external
to this PR and must not be inferred from a label. Preserve existing required-check
settings; unavailable CI remains an unresolved gate, never an automatic waiver.

Excluded: product architecture/implementation, new task schema/state machine,
semantic planning engine, tracker/orchestrator automation, neutral exporter runtime,
mandatory stack profiles, historical-record rewrites, repository administration,
merge/release/deployment, automatic downstream application. Recovery is reverting
this scoped change; downstream adoption remains a separately reviewed project PR.
