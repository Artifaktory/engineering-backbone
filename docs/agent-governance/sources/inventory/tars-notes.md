# Tars Codex ecosystem source inventory

Source repository: `Artifaktory/Tars`; governance source branch: `feature/frontend` (not default `master`).
Pinned HEAD: `6dc0ee4ef712f6f1b26a11f180c36d6434a759c1`.
Git tree: `b06a5facbdd763fa6d941b66e1f6682fa7ba43d2`; recursive response contains 4761 entries and `truncated=false`.
Snapshot captured 2026-10-12. Source repositories were read-only.

## Coverage and limitations

The machine-readable `tars.json` enumerates all 501 selected blobs individually with source commit, blob SHA, size, path, URL, disposition, rationale and proposed destination. It is complete **for the explicit selection rules**, not a semantic audit of the whole Tars codebase.

| Disposition | Count | Meaning |
|---|---:|---|
| integrate-common | 137 | Extract named portable behavioral sections; preserve project native files. This is a proposal, not a claim of implemented portability. |
| retain-local | 137 | Product paths, branch/runner/dependency configuration, technical/domain profiles and optional tool settings stay in Tars. |
| defer-implementation | 100 | Controllers/schemas/hooks/conformance require a separately tested project-neutral implementation; not ported by prose. |
| support-test | 127 | Historic/source-local tests, fixtures and calibration reports; do not count as current Backbone proof. |

| Inspection | Count | Meaning |
|---|---:|---|
| content-read | 160 | Retrieved complete content and examined for extraction/classification; not an independent code audit. |
| content-excerpt | 4 | Focused symbols/sections inspected; no whole-file semantic assurance. |
| tree-only | 337 | Existence, path and immutable blob metadata only; classification conservative. |

All 164 fetched source files returned blob SHAs matching the Git tree.
`tars-source-cache.json` retains the connector-returned content for the inspected files in scratch.

Selection includes all `AGENTS.md`, `.codex/**`, `.agents/skills/**`, Copilot agents/instructions/prompts/baseline, `docs/agent-governance/**`, `schemas/agent-governance/**`, `scripts/agent_governance/**`, `tst/agent_governance/**`; supporting quality docs/runner/tests/policy/CI/IDE/config files; and all `.specify/**` because Spec Kit skills reference it. No `.opencode/**`, `opencode.json*` or `.aiignore` exists in this snapshot. Product files, product tests, portals/program plans and historical `artifacts/quality-*` are not included in the completeness claim.

## Portable sections to integrate

1. **Authority/discovery** — root and nearest-path instructions, host adapters derive from canonical source, no shadow policy, unexpected overrides treated explicitly. Use trusted base policy when reviewing changes to policy itself. Actual instruction loading is host evidence, not a file existence guarantee.
2. **Role contracts** — planner, independent plan reviewer, implementer, test engineer, checker, reviewer, security reviewer, documentation/traceability, diff explorer and finding triage have separate outputs and allowed edits. Checker may write caches/artifacts but must report unchanged source. Reviewer and triage return observations/decisions rather than patches. An implementer never certifies their own work.
3. **Task scope and planning depth** — prepare the smallest sufficient run contract from the authorized request; allowed/excluded paths, objective/acceptance, base/branch, risk, required checks/reviewers, forbidden actions. Delivery complexity is independent of run risk. Direct change need not become a program. Plans refer to authoritative requirements/architecture; issue/project state and runtime evidence remain distinct.
4. **Execution budgets** — identify actual orchestration owner, limit nested delegation according to that owner, targeted test then affected suite then project-selected broader checks; no retry of unchanged deterministic failure, deliberate bounded transient retry. Scope/contract/risk change, no relevant state change, repeated failure or budget end requires reassessment. Do not hardcode AO-only orchestration.
5. **Frozen review input** — provider/role reviewers see the same immutable base, head/tree or patch identity, objective/acceptance and selected catalogs. No fixes between parallel reviews. Report instruction sources, checked/unchecked paths, commands actually executed and evidence gaps.
6. **Finding/triage contract** — ID, severity/confidence, changed location, trigger, execution path, impact, evidence, acceptance relevance, diff causation and smallest useful regression test. Preserve rejected/duplicate/debt/out-of-scope/new-requirement/needs-decision dispositions. Only confirmed IDs become a fix task.
7. **Full → triage → fix → delta** — full uses task base to frozen head; delta uses prior reviewed head to new repair head and verifies confirmed IDs plus directly introduced regressions. A changed objective/scope/risk/contract invalidates a limited delta and merits a new full review. Reviewer roles on one snapshot constitute one round. Budgets must not falsely imply open blockers are resolved.
8. **Required vs optional reviewers** — only selected required role/provider evidence is mandatory; present optional evidence still needs snapshot integrity. A general review cannot silently stand in for a security or traceability lens.
9. **Closeout/evidence** — objective/acceptance-to-real-evidence matrix, scope differences, actual command/exit/status, docs/contracts impact, rollback/cleanup where applicable, unexecuted checks and open risks. Planned/implemented/tested/manual/blocked/stale are separate. Hashes bind a snapshot; they do not authenticate a human or hostile same-user local environment.
10. **Host/remote capability limits** — config/profile existence does not establish execution, correct discovery, read-only enforcement, active hooks, provider review automation or GitHub protection. Remote review without a complete bound run context remains advisory. This does not transfer Tars's remote schedule or P0/P1-only policy as universal defaults.

Primary pinned references are root `AGENTS.md`, `docs/agent-governance/{00-file-layout-and-authority,05-local-agent-loop,20-role-contracts,30-task-packet-and-scope,32-task-packet-modes,40-review-policy-and-catalog,60-findings-and-triage,70-evidence-and-artifacts,80-host-tool-permission-matrix,90-conformance-test-plan,95-governance-change-policy}.md`; the planning docs and 12 native Codex roles/12 Copilot roles/18 skill bodies and their metadata were inspected.

## What must remain project-local

| Tars mechanism | Why it is not a global Backbone default |
|---|---|
| `feature/frontend`, `origin/feature/ux-&-test`, `origin/main/master` remote allowlists | These are Tars integration authority; other projects have their own branches and origin trust. |
| AO as sole outer orchestrator, no nested workers, `internal_subagents_max: 0` under AO/external | Explicit selected Tars deployment mode. Portable rule must honor an assigned owner and actual host capability. |
| `model_reasoning_effort=medium`, Plan Mode high, role-specific effort | User/host/model cost and provider capability choice; not a cross-project policy guarantee. |
| Guard, ActionIntent, Workspace, Exchange/Orders/Positions, Mainnet/Funds/Testnet | Trading product model and protected operating procedures. |
| `scripts/quality/run.py` and quick/commit/push/full concrete matrices | Project runtime/toolchain/coverage/baseline/manual triggers; Backbone should reference configured commands. |
| Single-flight integration lane, self-hosted ci-light/ci-heavy/ci-check runners | Project hosting and hardware capabilities. |
| Remote reviews consciously triggered, auto-review after every push disabled, advisory P0/P1 only | Tars current project policy conflicts with globally mandatory proactive review. User may change it later in a Tars governance PR. |
| Sphinx-Needs, LikeC4, Spec Kit selected adapter exclusions | Specific truth-owner/tool integrations; use equivalent project sources rather than mandate tools globally. |
| Risk-Control grandfathering and named plan profiles | Historical Tars exceptions are not portable. |
| Tars calibration baselines and claimed historic PASS | Evidence belongs to its recorded host/snapshot; do not reinterpret as Backbone checks. |

## Runtime implementation not ported by documentation

- `scripts/agent_governance/review_chain.py` is 52,270 characters; excerpt inspection confirms task/round identity, finding artifact seals, `.git/tars-agent-governance` anchors and structured human decision validation. These mechanisms require a dedicated migration if wanted.
- `scripts/agent_governance/pre_publish_check.py` is 66,870 characters; excerpt inspection shows fixed quality matrices, provider/role gates, publish authority markers, remote-advertised base binding and scope-class constraints. It embeds Tars-specific trust/quality choices.
- `scripts/agent_governance/codex/run_local_review.py` is 95,222 characters; excerpt inspection shows exact Tars roles/catalogs, active-packet pointer, isolated Codex invocation, trusted-base context, snapshot/secret/integrity checks. No claim that Backbone now supplies this runner.
- Native hooks are disabled by `.codex/config.toml`. `Stop` currently produces warnings, not an unconditional publish block; `PreToolUse` is a regex/tool-name defense-in-depth layer. They do not replace sandbox/authorization. Configuration requires separate host conformance before activation.
- Source schemas include Tars prefixes and identity contracts. Source schema existence is not compatible with Backbone schema IDs by construction.
- Source tests (including 92,259-byte local runner and 139,795-byte prepublish test files) remain tree-only inventories unless explicitly fetched. They were not executed in this extraction.

## Source contradictions that must not propagate

| ID | Source | Actual conflicting evidence | Extraction decision |
|---|---|---|---|
| TARS-SRC-001 | `docs/agent-governance/codex/90-codex-conformance-tests.md` blob `ba581d5e213b440d9ac5e8b12f58f102e1e32d1b`, section “Statisch”, says config enables Multi-Agent | `.codex/config.toml` blob `df331a5dc57c1d1fac358da8f9a899e3f04b71af` has agents.enabled=false and features.multi_agent=false; README/AO policy disables nested orchestration | Use actual configured capability; record stale prose and keep source remediation separate. |
| TARS-SRC-002 | `docs/agent-governance/codex/70-skills-and-invocation.md` blob `363587a954d7996ac9545d059f86874d34cec84f` says safe intake/planning/quality helpers can be implicit | All 18 inspected `agents/openai.yaml` files explicitly set `allow_implicit_invocation: false`; e.g. task-intake blob `27df880954fe11a8e9d25ea6c966df34d3ce5740` and run-quality blob `31899d6ae63cd3146e18832c96aabc5a002332ba` | Do not promise implicit loading; use configured host/skill behavior and real discovery check. |

## Minimal integration recommendation

For this PR, add the common contracts above to canonical Backbone policy/docs and generate matching Codex/Copilot instruction fragments. Keep the existing mandatory planner/implementer/reviewer provider slots compatible. Optional specialized roles can be described and selected without introducing new schema/controller/host assumptions. Add a full source file mapping and focused portable-policy/template tests. Preserve source-local enforcement and explicitly name deferred runtime migration. Do not modify Tars or claim consumer adoption has occurred.
