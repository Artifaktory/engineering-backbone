# Dependency compatibility and tracked container inputs

## Authority and scope
Task BB-DEPENDENCIES-009 is authorized by the user's 2026-10-14 request to implement
shared dependency/version compatibility governance, real Git-tracked discoverable
Dockerfile/documentation, checks, independent review, PR and visible Codex review.
Base main: 229ac884c1a2ac70f0fb5c961bd517c9eaf740af. HIGH-risk control-plane work.
No merge, release, deployment, downstream writes, runner migration or repository
settings changes. Preserve all existing stronger local gates.

## Design
1. Add canonical policy/dependencies.md, referenced from quality policy and agent
   entrypoints, distributed as .engineering-backbone/dependency-policy.md. Define
   reproducible reviewed resolution, compatible runtime/platform combinations,
   apps versus libraries, explicit update scope, no silent conflict bypass, actual
   behavior tests, and independent review. Native manifests/lockfiles remain the
   version authority; do not duplicate package version lists in prose.
2. Preserve both existing catalog identities byte-for-byte: their trusted guards
   intentionally reject catalog replacement. This delivery extends the existing
   navigation/quality guard with an optional project-owned dependencies.json and
   its schema. No new check kind, parallel rule catalog or runtime upgrade.
3. Consumer contract v1: enabled flag and components containing id (existing
   navigation component), kind (application/library/tooling), compatibility_document,
   manifests, resolution_files, runtime_files, dockerfiles and check_ids. Application
   and tooling need concrete resolution; published libraries may use supported
   ranges with a documented/tested compatibility matrix. All kinds describe their
   reproducible test environment. Require dependency, build, test PR check coverage,
   plus container for declared Dockerfiles, using effective approved check definitions.
4. Active contract requires active navigation, quality and workflow configuration.
   Validate safe exact nonempty regular repository-local files; dependency artifacts
   must be covered by their navigation component's literal paths. Always include
   the policy and contract in active dependency contexts; include every selected
   component's referenced files, with hashes, in implementer/reviewer handoffs.
   Missing files, missing/invalid bindings and stale handoffs fail closed. Do not
   execute candidate commands in structural validation or claim semantic proof.
5. Keep legacy absence/inactive seeds supported. Adoption requires a complete
   reviewed inactive seed followed by enabled-only activation. Reject removal,
   disablement or weakening of an inherited active dependency contract. Copier
   preserves project-owned config/docs and installs managed policy/schema. Matching
   reviewed guard/workflow pins are required; an old guard cannot attest new duties.
6. Source repository currently has no active navigation/workflow kit. Add real
   root Dockerfile and .dockerignore for the existing Python tooling, plus an actual
   docs/dependency-compatibility.md naming requirements.txt/requirements.lock,
   supported tooling environment and build/test commands. Source CI executes a
   bounded source dependency check (tracked required inputs, direct pins versus
   resolution, installed declared dependency consistency), and a Docker build/smoke
   check. Root AGENTS/CONTRIBUTING link these actual files. Do not activate a fake
   source navigation contract or overwrite consumers' application Dockerfiles.
   Container base is immutable and verified from registry evidence; no invented
   digest. No broad tooling upgrades. Report unavailable local Docker honestly.
7. Compile through existing navigation -> quality -> toolchain fingerprint chain;
   keep trusted predecessor/source validation and consumer-upgrade checks intact.

## Acceptance and verification
- Shared policy and actual source Dockerfile/compatibility files are tracked and
  reachable from agent entrypoints; remote PR tree readback verifies their bytes.
- Positive and negative dependency config/routing checks: missing/empty/unsafe
  artifact, missing check kind, approved-versus-candidate check definition, all
  task roles/types, stale manifest/lock/Dockerfile receipts, inherited weakening
  and invalid activation. Test relevant component coverage, not unrelated scans.
- Real Copier create/update with quality on/off/provider combinations; local files
  preserved; legacy active navigation survives optional extension installation.
- Source lock/metadata validation and container smoke (local if engine available,
  otherwise actual GitHub CI with explicit pending/blocked evidence).
- Current and trusted-base validators, all compilers, full unittest suite,
  Actionlint, diff whitespace and meaningful new negative/upgrade tests.
- Independent plan review before implementation. Quality checker executes checks.
  Two independent read-only Full reviewers on identical frozen base/head/patch:
  behavior/compatibility and authority/security. Separate triage before confirmed
  repairs; targeted checks and Delta on fixes/direct regressions. Two Full rounds
  max without justified expanded scope; eight repair iterations max.
- Publish PR at verified tree, inspect CI, trigger Codex visibly with fixed review
  context. Triage any available remote findings; no automatic merge.

## Ownership and stop conditions
Root plans/integrates/publishes. Guard worker owns resolver/schema/unit tests;
policy worker owns shared policy/templates/guides; container worker owns source
Dockerfile/check/CI with focused tests. Independent quality and reviewer roles do
not repair their reviewed snapshot. Missing required evidence, confirmed unresolved
findings, authorization conflict or weakened local gates block the affected step.
