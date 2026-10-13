# Versioned agentic quality framework

## Authority and bounded delivery
Human approval 2026-10-13 authorizes the agreed shared quality framework, checks,
necessary contract/negative tests, independent review chain and a PR.
Base main: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`.
HIGH risk. This PR changes the Backbone only; no consumer adoption, permissions,
merge/release/deployment, client installation or external certification.

Canonical `policy/core.md` remains authority. Add a linked quality extension,
reviewed sources/rules/profiles, a project-owned separate quality-profile contract,
templates and concise provider/role/skill discovery and handoff instructions.
Do not change existing Task Packet role enums or closed project/workflow contracts.

## Contract and enforcement
1. New `standards/sources.json`, `rules.json`, `profiles/*.json` hold one
   versioned catalog. Norm entries describe official editions and verified public
   scope; full ISO/IEC clause adoption is NOT claimed from catalog abstracts.
   Eight baseline organization rules cover requirements, design, code, tests,
   docs, evidence, independent review and handoffs. Add bounded applicable
   software/security, Python, TypeScript, high-risk and agentic refinements.
   C++17 and IEC material stays explicitly reference-only until its necessary
   tool/profile/full-text applicability work has been reviewed.
2. Project profile lives at `.engineering-backbone/quality-profile.json`,
   schema version1, enabled boolean, catalog_version1.0.0, backbone_ref full40
   or blank for inactive seed, profiles, four project-owned document paths,
   per-rule check-ID bindings and exceptions. Commands remain in workflows.json.
   Active automatic bindings require an active complete workflow kit and actual
   referenced PR check IDs/kinds. No project command is executed by this guard.
3. Required docs: quality plan, test strategy and traceability CSV; exception doc
   required when exceptions exist. CSV has exact columns rule_id,requirement_id,
   risk,architecture,tests,check_ids,evidence,status; maps every applicable rule.
   A mapping/status is a declaration, not authenticated reviewer or runtime proof.
   Evidence verification and human acceptance continue through existing reviews.
   Required artifact absence, malformed data, invalid rule/check/path, removal or
   weakening of active inherited selection/bindings, expired/disallowed exceptions
   and candidate catalog poisoning fail structural validation.
4. A self-contained stdlib quality guard is compiled from trusted source/catalog
   into the current validator and immutable reusable governance workflow.
   The workflow independently runs it even against an approved old validator.
   Candidate scripts, schemas or catalogs never supply authority. Guard reads
   bounded regular files without symlink ancestors/duplicate keys/path traversal.
   V1 accepts only the compiler-owned current catalog. Future historical catalogs
   require an explicitly reviewed trusted-source literal allowlist; arbitrary
   coherent base-owned JSON is never authority. Legacy absence stays compatible;
   managed catalog data may not be altered by a consumer. Harmless JSON whitespace,
   key order and line-ending differences are permitted; parsed authority must
   match exactly, with duplicate keys and extra catalog/profile files rejected.
   The existing eight-file tooling attestation format is preserved, new validator
   bytes get a new current fingerprint; only merged previous identities retained.
5. Add source compiler --write/--check and source CI check. Catalog changes are
   reviewed source changes; compiling reads JSON/AST without importing candidate
   executable code. One source function/catalog compiled everywhere.
6. Copier opt-in use_quality_framework defaults false and is installation-only
   with legacy missing answer=false. Opt-in outputs an explicitly inactive
   incomplete seed and preserved project-owned docs/profile. Complete seed is
   reviewed/merged before separate activation; activation changes enabled only
   and cannot manufacture a base. Ordinary upgrades preserve profile/docs/native
   files and stricter rules; refreshed managed catalog and fragments require
   reviewed manual integration and matching workflow pin. Existing consumers
   without the profile remain valid; existing adopted profiles cannot disappear.
7. Structural PASS means contracts/links/check bindings only. Actual commands and
   fixed job gate belong to workflow kit; semantic design/test quality,
   independent reviewers, client loading and human acceptance are separate.
   No fabricated normative conformance or certification claims.

## Ownership and interface
Catalog/docs worker: standards/**, policy/quality.md, docs/quality/**.
Engine worker: scripts/quality_framework.py, schemas/quality-profile.schema.json,
tests/test_quality_framework.py. Self-contained function:
`quality_errors(root, trusted_base=None, *, source=False)` returns list[str].
Inside it one `catalog_json = '{}'` assignment is compiler-owned JSON literal.
Compiler combines catalog into keys version/sources/rules/profiles. A CLI validate
wrapper invokes the function, never application checks.
Template/adapter worker: copier.yml, templates/**, .codex/**, .github/agents/**,
.github/skills/**, .github/instructions/**, .github/copilot-instructions.md and
tests/test_quality_copier.py. Keep native identities/tool permissions unchanged.
Root: compiler, validator/workflow integration, tests of actual compiled payload,
README/CONTRIBUTING/core link, adoption docs, fingerprint, task/evidence records.
Dependencies: independent plan review first; agree catalog/profile field shapes
before workers edit; catalog -> compiler -> rendered tests -> fingerprint.
Use existing venv/Python3.12 and locked dependencies; no dependency changes.

## Verification and review
AC1: bounded truthful catalog with role/phase/source applicability and diagrams.
AC2: separate profile contract, safe guard, positive/negative enforcement and
legacy absence/inactive seed support; null never means absent.
AC3: real Copier create/update/provider matrix and preserved local rules/docs.
AC4: workflow-owned guard blocks candidate/old-validator bypass; no candidate code
executes; approved compatibility tuple and all existing checks preserved.
AC5: role/skill/task handoffs select exact profile/rule version and required evidence.
AC6: source/trusted validator, both existing compilers/new compiler, meaningful
targeted then full tests, actionlint and committed diff hygiene pass.
AC7: independent plan and two frozen Full reviews, triage then confirmed fixes and
scoped Deltas; actual published tree/CI/provider review evidenced separately.

Independent plan review precedes implementation. Full reviewers inspect same
base/head/patch digest read-only after deterministic checks. No author approval.
Triage before fixes; direct repair regressions receive Delta; widened scope a
new bounded Full. At most two Full rounds and eight repair iterations by default.
Budget/unchanged required failure/unresolved finding/scope conflict stops publication.
No merge or automatic downstream apply. Recovery is a reviewed revert or manual
consumer pin/config migration; no destructive cleanup.
