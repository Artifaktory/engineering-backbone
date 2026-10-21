# BB-TEST-017 implementation plan

## Authorization and immutable baseline

On 2026-10-21 the user approved the preceding testing/quality and CI/CD proposals
as one coherent documentation delivery and explicitly requested a PR for review.
Actual merged main is `1a740604d4a6a68e500da36c4d99935d04a8ce86` (PR22); candidate
branch is `docs/testing-ci-contract`. Risk is HIGH: this is shared engineering
policy and distributed agent context. The Task Packet is `task-packet.json`.
This authorizes implementation and PR publication, not merge, release or deployment.

A separate read-only planner assesses this bounded scope; an independent reviewer
must accept this plan before implementation. Root integrates and publishes. Separate
authors own testing/provenance, CI/CD semantics and reusable templates. A separate
test implementer owns compatibility checks; independent quality and Full reviewers
do not repair their inspected snapshots. Triage remains separate from repair.

## Proposed delivery and boundaries

1. Expand existing `docs/quality/testing.md` into the canonical proportionate testing
   and verification contract. Preserve risk-based selection and existing stronger
   policies. Define scope/authority, requirements-risk-design-acceptance lineage,
   static/dynamic methods, levels/types/techniques/development approaches/phases,
   testability and design, applicability, environments/data, responsibilities,
   execution, anomalies/regression, flaky cases, changed-input validity and closure.
   Include the existing real agent-handoff-chain obligations and live/mock limits.
2. Add `docs/quality/testing-sources.md`: primary source editions, public-scope limits
   and near-rule crosswalk. Reuse existing registers. ISO29119-1:2022 and 2/3/4:2021,
   ISO25010:2023, ISO20246:2017, NASA5.3/5.4, NISTSSDF1.1, NIST800-204D and optional
   SLSA/ISTQB inform original Backbone rules; do not claim full-text conformity or
   universal required tools, test counts, coverage rates or development methodology.
3. Add `docs/quality/ci-cd.md`, linked to existing workflow documentation. Map required
   evidence to actual check IDs, triggers, revisions/builds, environment, owner,
   permissions, retention and gate decisions. Cover PR/integrated-main/periodic/
   release/deploy applicability, artifact identity and pipeline-change verification.
   Distinguish recommendations, optional adopted profiles, current inherited duties
   and Backbone-owned semantics. Preserve actual workflow-kit requirements, including
   release signatures/SBOM where selected, without weakening them to optional advice.
   Document current phase/kind support honestly: generic periodic/release behavior
   tests and arbitrary matrices require a separately reviewed implementation.
   User-selected local runners/no GitHub artifact upload remain source/project facts,
   not an external norm. Legacy optional hosted/upload workflows remain separately
   identified; no activation or runtime modification occurs here.
4. Add eight canonical templates under `docs/templates/testing/`: README, test-strategy,
   test-design, test-run, test-completion, ci-mapping, review and worked-example.
   Reuse the existing quality-plan/test-strategy seeds rather than inventing duplicate
   mandatory records. Automated test code may own detailed cases; small changes may
   combine records. Include an explicitly hypothetical example with planned checks,
   meaningful negative/integration cases, mock/live boundaries, pending execution,
   blocked/failed/error/skip meanings and no invented approvals or actual PASS.
5. Explain status dimensions and exact existing schema crosswalk in companion prose.
   Requirement verification is not_run/pass/fail/blocked; Task Packet acceptance and
   review checks pending/pass/fail/blocked; quality CSV pending/planned/verified/gap.
   Applicability, run lifecycle/outcome, evidence freshness and gate decisions remain
   distinct. N/A, missing, skipped, blocked or cancelled is not runtime PASS. Waivers
   cannot rewrite history or waive a nonwaivable rule. Do not add JSON fields/states,
   change CSV columns or pretend documentation implements a result engine.
6. Integrate core/root/quality/architecture/planning/adoption/workflow entrypoints as
   necessary. Current delivery references in AGENTS/CONTRIBUTING/changes index must
   point here and to the actual trusted base; old delivery records remain untouched.
   Always distribute the managed testing/CI guidance and templates when linked from
   core, including adapters/quality/workflow disabled. Optional guide links must not
   break those copies. Keep managed common templates separate from project-owned
   strategy/results. Existing consumer documents and native instructions are preserved;
   enrich installation seed links without falsely updating existing project content.
7. Add meaningful source/direct-copy/rendered copy/update/negative tests: guide/template
   parity and local context, optional-off/on combinations, project/native preservation,
   missing mandatory context rejection and unchanged existing schema/state boundaries.
   Existing tests may receive necessary link-rewrite expectations; no assertion is
   removed or narrowed. Schemas/catalogs/runtime/workflow YAML and frozen fixtures
   remain unchanged. Rendered toolchain tuple should remain unchanged; fingerprint
   check still runs, without an unnecessary generation/authority change.

## Acceptance and verification

- AC1: coherent requirements/architecture/planning-to-verification contract with
  proportionate methods, risk and applicability, evidence and real acceptance.
- AC2: accurate source provenance and local-rule distinction; no imposed stack,
  methodology, percentage, certification or universal CI topology.
- AC3: complete original testing kit and coherent hypothetical example; small or
  nonsoftware projects can satisfy relevant duties without fictitious runtime work.
- AC4: explicit status/evidence/gate mapping preserves existing schemas and stronger
  policy, including mandatory missing-result failure and historical results.
- AC5: CI/CD mapping connects test strategy to real check/evidence/permission/gate
  contracts, accurately states current automation and source/consumer limits.
- AC6: source and legacy copies/updates preserve context and project ownership; real
  positive/negative tests pass, with no schema/catalog/runtime/workflow/fixture edits.
- AC7: actual candidate/base-owned checks, full suite, independent reviews and triage
  qualify a frozen implementation; published PR and exact identity/readback recorded.

Run targeted distribution tests during integration, then freeze a committed subject.
A separate quality checker runs candidate validator, four compiler --check commands,
source dependency checks and the complete unittest suite with the existing locked
Python3.12 environment. Execute the actual main-base validator from a separate
checkout against the candidate using --trusted-base. Verify protected paths and
committed whitespace. Preserve failures and triage before repair; do not rerun an
unchanged failure to obtain green. No dependency/container/native adapter changes
are planned; do not claim Docker/native Windows/provider execution if unavailable.

After deterministic checks, independent behavior/traceability and authority/security/
compatibility Full reviewers inspect the same base/head/binary-patch digest read-only.
Triage concrete findings before repair; Delta covers confirmed repairs and direct
regressions. At most two Full rounds and six implementation/repair iterations.
A scope/trust-boundary change requires a new independently reviewed plan.

## Publication, limitations and recovery

Evidence commits refer to the inspected implementation; reviewers do not claim to
have reviewed their own later reports. Repeat candidate/base-owned validation for
those records and git diff --check BASE HEAD after each final commit. Publishing
through the GitHub connector may change commit IDs: preserve reachable reviewed
commits or verify exact tree, parent and binary-patch correspondence and record it.
Read back the final PR/head/changed paths and remote CI. Queued/skipped/missing checks
are not passing; do not provision runners, weaken required checks or add hosted
fallbacks to clear a queue. A draft PR is appropriate if required runtime/CI evidence
remains pending. No merge/release/deploy, automatic downstream apply, protection or
credential changes. Recovery is a reviewed revert of this scoped delivery.
