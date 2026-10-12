# Artifaktory Codex and engineering inventory

Repository: `Artifaktory/Artifaktory`. Observed: 2026-10-12. This is a read-only source analysis; no source repository was modified.

## Frozen source identity and coverage

- Primary development branch: `staging@7ed20cd7853d7e19eb55e37f31fa6c6214952b1d`; Git tree `08e6aeb3174e39e5efd3b5979744e68b63b0d475`.
- Previous comparison branch: `main@0307348366e900605b66f442e2075901e979ddb1`; tree `479956fe5406cfe53beff351c39e0354332b5a5a`.
- Complete recursive tree returned 1,530 entries with `truncated=false`.
- Bounded agent/governance/engineering ecosystem: **418 blob paths** individually classified with commit, blob SHA, size, source URL, main comparison, and inspection scope in `artifaktory.json`.
- Inspection: **120 full-content, 5 selected-sections, 293 tree-only**. The latter are inventory/support/deferred implementation, never represented as code audited or imported.
- Retrieved contents for 131 files are in `artifaktory-source-contents.json`; six retrieved-only references are explicitly still tree-only.
- Classification counts: **85 integrate-common; 112 retain-local; 95 defer-implementation; 126 support-test**.
- All 405 selected paths shared with main have identical blob SHAs. Staging adds 13 runner-operation/setup/test paths. Core Codex/governance references have not changed since the earlier main inspection.

The JSON selection rule lists every prefix. It includes root/nested AGENTS, .codex, .agents/skills, all Copilot agents/instructions/prompts, templates and workflows, all agent-governance documents/schemas/scripts/tests, quality runner, runner setup, legacy ai-agents, .specify plus Spec-Kit support, specs, and the directly related AFES engineering package. It does not claim to inventory all business requirements or application source.

## Reusable sections and source anchors

| Source | Common section to integrate | Keep local / caution |
| --- | --- | --- |
| `AGENTS.md` §§1,3,4,6–11 | Instruction authority, scoped packets, session separation, safe Git, deterministic-first checks, frozen reviews, honest evidence, trusted-base control-plane review | §2/§5 business domains, staging/main promotion, concrete commands, ART/AF IDs, signing requirements |
| `05-local-agent-loop.md` | One accountable orchestration owner; bounded affected-test → suite → quality → frozen review; no unchanged deterministic retry; explicit stops | Source restricts normal workers to no internal hierarchies; do not silently enable agents or import its exact runtime |
| `20-role-contracts.md` and native roles/skills | Planner, developer, test-only worker, quality checker, plan reviewer, general/specialist/test-traceability reviewer and triage responsibilities | Model/reasoning/sandbox/tool settings are host adapters; source native roles remain stronger and no self-review is allowed |
| `30-task-packet-and-scope.md`, `32-task-packet-modes.md` | Include allowlist; exclude wins; approved source versus run contract; budgets/stop conditions; no scope/risk downgrade to continue | Signed continuation and host paths are not ported; do not add unsupported keys to current backbone schemas |
| `planning/README.md`, implementation-plan and delivery-decomposition catalogs | Durable requirements and architecture → coherent PR-sized delivery → issue projection → exact run; independent plan review, dependencies/conflict sets, DoR and acceptance evidence | No business-stack sources, numbered programs, project IDs, tool installation or new orchestration runtime |
| `40-review-policy-and-catalog.md`, `45-review-chain.md` | Full-first, identical snapshot for reviewers, no fixes mid-round, confirmed IDs only; Delta verifies fixes and direct regressions; changed packet/scope/risk/contract/architecture requires Full; preserve predecessor evidence | Hash seals, Git-local anchors, signed restoration/continuation/history reconciliation, source bundles and controllers are separate deferred work |
| `60-findings-and-triage.md`, finding/output schemas | Exact location, severity/confidence, trigger/path/impact/evidence/AC/diff causation/regression; coverage and blockers; distinct confirmed/rejected/duplicate/debt/out-of-scope/new-requirement/human-decision reasons | Existing backbone schema is authoritative: preserve extended narrative in supported fields/companion reports instead of importing AF-specific JSON |
| `70-evidence-and-artifacts.md`, closeout skill/template | Actual commands, exit codes, omissions, immutable original output; redaction; per-AC automatic/manual/open results; residual risks/rollback; readiness is not approval | Host signer roots/ACLs, detached signatures, namespaces and evidence-path enforcement remain source requirements and are not provided by the backbone |
| `80-host-tool-permission-matrix.md`, Codex README | Least-privilege roles, concrete host/runtime discovery proof; format/profile presence is not enforcement | Do not copy broad command allow rules or source runtime settings |
| `95-governance-change-policy.md`, governance catalog | Dedicated HIGH-risk governance PR; trusted base; schemas/validators/consumer regression tests; no auto-merge | Historical branch-specific bootstrap exception is retired and must not be reintroduced |
| Quality strategy/manual duties | Risk-driven positive, negative, recovery, permission, migration and producer/consumer checks; real status; manual evidence triggers | Source commands, Next.js/Django/Playwright lanes, runner labels and online audit policy remain local |
| Root Copilot instructions and common path instructions/prompts | Same common baseline and bounded roles; no suggested repair before triage; remote reviews explicitly advisory | Native applyTo paths, terminal names, staging promotion and business restrictions are not universal |
| Governance workflow | Additive deterministic gate, current-diff hygiene and CI evidence | No recursive sudo workspace repair, `git clean -ffdx`, special branch-name trust exceptions or self-hosted label transplantation |

The existing backbone now already expresses many of these common additions. Integration should use the current three native roles with packet-scoped responsibilities rather than create a large role registry or additional controllers. Document which source concept is covered and which machinery is intentionally deferred.

## Source-specific warnings and stale references

These are source observations, not new formal findings in the backbone implementation:

1. `AGENTS.md` requires ordinary PRs to target staging, but generic task-packet and governance PR examples still use origin/main. Treat examples as historical/local examples, never target-branch authority.
2. `HOST_CALIBRATION_RUNBOOK.md` says formal Full/Delta chaining is deferred to #140, whereas the current `45-review-chain.md` describes an implemented tamper-bound chain. This runbook belongs to an earlier calibration rollout. It also references `Binary-Refinery/Artifaktory` rather than current `Artifaktory/Artifaktory`.
3. `GITHUB_ENFORCEMENT.md` is main/bootstrap-focused. Its documented check name and target must be verified against live workflows/settings before claiming protection. Branch API reports protected=false for both fetched branches; no settings mutation was performed.
4. `100-test-and-calibration-plan.md` uses CRITICAL_PRODUCTION in one calibration bullet while current risk/packet contracts use CRITICAL. Normalize generic concepts, not this stale enum.
5. `.specify/memory/constitution.md` contains unfilled project/principle/version placeholders. Its presence is not an approved project constitution.
6. `.specify/commands/speckit.implement.md` and `speckit.converge.md` explicitly refuse execution; the workflow has no implementation step. Spec-Kit is only a planning adapter and cannot replace approved packets and AO/IDE delivery.
7. `ai-agents/README.md` explicitly makes both old prompts non-authoritative. The code-review prompt includes style/naming/DRY suggestions that conflict with the current concrete-diff-only formal finding policy. Do not promote legacy prompts to active governance.
8. Source .codex and .github each have **10 native role files**, including business-safety and overlapping business-security reviewer profiles. Ten skills exist, including local issue creation. A documentation/traceability responsibility appears in the role contract without a corresponding standalone native profile. Do not claim a native implementation exists for every named responsibility.
9. Source command rules include duplicate network/business families and broad pytest/npm-run allows. Their presence is defense in depth, not evidence of complete host command or scope enforcement; copy no blanket permissions.
10. The source explicitly distinguishes repository tests, dry runs, real model review, provider remote advice, host calibration, GitHub settings, and human approval. Preserve these boundaries in the PR evidence.

## Minimum integration and verification

1. Commit complete bounded inventory and semantic crosswalk, with tree-only markers visible.
2. Strengthen shared policy/inline fragments and planner/implementer/reviewer instructions with the portable responsibilities, evidence quality, plan review, and bounded Full/Triage/Fix/Delta semantics.
3. Record neutral planning/decomposition, general correctness, governance, tests/traceability and evidence checklists in docs/codex-consolidation.md, docs/planning.md and docs/agent-adapters.md; strengthen templates/_partials and the existing native profiles. Existing consumer schema compatibility is preserved. Do not create an additional catalog or role runtime.
4. Test generated Codex/Copilot material, preservation of stronger native policies, consumer creation and upgrades, and no accidental introduction of source project branch/domain/host rules.
5. Perform independent Full review, triage, confirmed fixes, targeted checks and Delta review; do not claim controller/signature/host/remote-bot activation.
6. Preserve stronger source controls at downstream adoption. This PR centralizes common sections and records deferred machinery; it does not replace source governance or migrate the two source repositories.
