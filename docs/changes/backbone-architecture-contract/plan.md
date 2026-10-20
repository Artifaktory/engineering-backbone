# BB-ARCH-015 implementation plan

## Authorized objective and baseline

The user requested the previously discussed architecture documents and a PR on
2026-10-20. Work starts from human-merged `main`
`ae317bf30576914d4ed53856be4ae496c6ed64b3` in a fresh isolated branch.
[Task Packet](task-packet.json) is authoritative for scope and acceptance.
This is HIGH-risk shared governance work. Prior PR18 local publication corrections
are excluded. This delivery does not redesign Artifaktory, TARS or agent-factory.

## Design and implementation

1. Add `docs/agent-governance/architecture.md` as the canonical semantic contract:
   requirement provenance/approval, architecturally significant drivers, measurable
   quality scenarios, alternatives/tradeoffs, views and correspondence, decisions,
   planned verification, independent evaluation, implementation and actual evidence.
   Define source ownership, stable IDs, many-to-many traceability, explicit treatment
   of every scoped requirement, assumptions/derived requirements, blockers,
   state/revision separation, proportional tailoring and change impact.
2. Add `docs/templates/architecture/` with an index, architecture description,
   ADR, quality scenario, requirements/design traceability, review, and project/tool
   mapping templates plus a hypothetical worked example. No fabricated product
   facts, approvals or executable PASS. Twelve arc42 content areas may be combined
   or referenced; justified non-applicability is explicit. Requirements and quality
   evidence keep one authoritative home. Existing JSON and CSV contracts remain
   unchanged; unsupported metadata lives in linked companion records.
3. Add a concise official-source provenance record for ISO 29148/42010/25010/
   42020/42030 public scopes, arc42, C4, MADR, ADD and scenario/tradeoff evaluation.
   These are organization-owned rules informed by public guidance, not clause
   conformance or full ATAM. Tool names are optional examples. No new dependency.
4. Integrate core, planning, product location READMEs, quality/testing, adoption,
   repository entrypoints and change index. Make the architecture contract required
   context for scoped requirements/architecture work by agents and human reviewers.
   Preserve existing stricter approval/gates and active navigation procedures.
5. Retain coherent legacy Copier distribution via canonical includes and rewritten
   relative links, with reusable assets under managed Backbone paths. Do not seed
   or overwrite a consumer's product architecture or requirements. Existing native
   files remain preserved; adoption explains reviewed manual context integration.
6. Add narrowly targeted compatibility checks for direct source/copied links,
   rendered canonical parity, preserved project-owned documents/native instructions,
   and meaningful negative cases (missing linked contract/template). Use existing
   guard semantics; do not pretend the validator verifies architectural fitness.

## Roles, sequence and review budget

Root owns planning/integration/publication. A separate read-only reviewer must
accept this plan before implementation. Bounded implementers may author the contract
and template files. A separate quality checker runs deterministic checks on a frozen
snapshot without repairs. Independent behavior/document and authority/security
reviewers inspect the same immutable base/head/patch after checks. Separate triage
classifies findings before author repairs. Delta reviews only confirmed IDs and
introduced regressions. Required: plan, quality, behavior and authority reviews.
Optional: remote provider advice; it never replaces these reviews. Maximum two Full
rounds and six implementation/repair iterations. No repeated unchanged-failure runs.

## Verification and acceptance

Map AC-1..AC-7 in the Task Packet to the final documents, actual check report,
independent reports/triage and publication record. Check contract/template agreement,
both directions of traceability, target versus observed state, failure and ambiguity
handling, no invented human approvals, no mandatory architecture pattern/tool,
source provenance and project tailoring. Traceability is semantic: manual review
covers matters a Markdown/link check cannot prove.

Run candidate validator, all four generated-artifact checks, source-dependency
check, targeted new compatibility tests, and the repository's required complete
unittest suite. Run the actual trusted base validator from a separate ae317bf
checkout with `--root CANDIDATE --trusted-base TRUSTED_BASE`. Preserve fresh Copier
copy/update and direct-copy positive/negative coverage. Record exact commands,
exit codes and limitations. Existing schema/catalog/tooling bytes must stay unchanged;
no fingerprint regeneration is expected. Container/provider runtime tests are not
applicable because inputs and runtimes are unchanged.

Freeze and commit implementation before formal review. Ensure final published
review subject commits are reachable; if publication changes commit identity,
record and verify exact tree/parents/patch correspondence. Never claim unreachable
local hashes as the sole remote evidence. After every final code/evidence commit,
run `git diff --check ACTUAL_BASE ACTUAL_HEAD`. Inspect actual hosted CI, and report
pending/failed checks honestly. The PR is for human review; no merge or release.

## Risks, dependencies and recovery

Risks: contradictory policy/template instructions, excessive ceremony, fake normative
claims, missing legacy links, project-file overwrite, stale source/evidence and
confusing a draft with approved/verified state. Mitigate through explicit semantic
rules, linked authority, source provenance, compatibility tests and independent
reviews. Dependencies are existing Python/Copier tooling only. Revert this scoped
PR to recover; consumer adoption is a separate reviewed PR. No automated migration,
new runtime adapter, schema extension or branch-protection enforcement is included.
