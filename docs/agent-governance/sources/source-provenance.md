# Source provenance and adaptation

This bootstrap adapts existing engineering and agent-governance concepts from
two private repositories. It is a new, smaller implementation, not an import of
their complete control planes. Source revisions are fixed for review; later
changes in those projects do not automatically change this repository.

## Pinned source revisions

| Source | Inspected branch | Commit |
|---|---|---|
| `Artifaktory/Artifaktory` | `main` | `0307348366e900605b66f442e2075901e979ddb1` |
| `Artifaktory/Tars` | `feature/frontend` | `6dc0ee4ef712f6f1b26a11f180c36d6434a759c1` |

Both recursive Git trees were inventoried without truncation. Tars governance
was read on `feature/frontend`; its default `master` branch was not used as the
governance source. The identifiers below are Git blob SHA-1 values, not content
SHA-256 digests or attestations of review completion.

## Relevant inspected Artifaktory files

All paths below refer to the pinned Artifaktory commit above.

| Path | Git blob SHA-1 |
|---|---|
| `AGENTS.md` | `1fd081376fd577f5d485e2f35c1e2e4bada514fd` |
| `docs/agent-governance/20-role-contracts.md` | `8cc7ca2a2a8d7adf60ff48d72e96c950b72d0b7e` |
| `docs/agent-governance/30-task-packet-and-scope.md` | `8cf97728c1f3bd4b02870fc33b23fcd0a5e20e89` |
| `docs/agent-governance/45-review-chain.md` | `b0a14a0d3d5b631411c4772539dd941b65f24d18` |
| `docs/agent-governance/60-findings-and-triage.md` | `17ee13924e509ff1713ee81cca5d13f07bf5b87d` |
| `docs/agent-governance/95-governance-change-policy.md` | `b923b2b55a82f84eabf3d7ef96c1b44ee299fb5b` |
| `docs/agent-governance/templates/task-packet.yaml` | `f853d7295c18db549aef1290658bc4e4b3a814f0` |
| `docs/agent-governance/templates/review-finding.json` | `b3d50728a02ccc683ae17b411fd757cc20a5d3f0` |
| `.github/workflows/governance-quality.yml` | `4d9b8603b0376503f667f1b30ee391bd11108764` |
| `.codex/agents/artifaktory-general-reviewer.toml` | `42cf901528811df96bf0675cb16c38386be84ac5` |
| `.github/agents/artifaktory-general-reviewer.agent.md` | `23a5826dcd4a666a843b08a5ba560d1cac60fe5b` |
| `docs/agent-governance/migration/tars-to-artifaktory-crosswalk.md` | `e781a1bbaa2fb2581acee42e4a6a47f15acca774` |

## Relevant inspected Tars files

All paths below refer to the pinned Tars commit above.

| Path | Git blob SHA-1 |
|---|---|
| `AGENTS.md` | `5d3476a073a791c113336c98df9ff4774e781bbc` |
| `docs/agent-governance/00-file-layout-and-authority.md` | `ae8f261a86d6a39374f0988d35c39bd2a32eac93` |
| `docs/agent-governance/05-local-agent-loop.md` | `f1c8c03a91f084c7cfc03751ad9ac3260dbc9125` |
| `docs/agent-governance/planning/10-delivery-modes-and-plan-triggers.md` | `175d767dd295fd0d008a435c51962429956d4777` |
| `docs/agent-governance/planning/40-story-issue-task-standard.md` | `62927c8b7a8eb1b621069cab47dbdfa526927c0a` |
| `docs/agent-governance/planning/templates/github-issue.md` | `d2bf67a56f7b5e5f68f38a092edb79987de48c0b` |
| `docs/agent-governance/planning/templates/phase-plan.md` | `8605eb9d5672ce91058fc02e553ef77a07e46422` |
| `docs/agent-governance/requirements/templates/requirement.md` | `379e54e0530e6d6b97f98bcad6e75cb807238c4a` |
| `docs/agent-governance/requirements/templates/verification.md` | `b5b803bfacd9f6b4969dc9fc9b93f13074b39cb2` |
| `docs/agent-governance/templates/task-packet.yaml` | `ced246c62d3f740e43ab77974950aa8bf76076f8` |
| `docs/agent-governance/templates/triage-report.md` | `6d3fa093a2a06343533df7585cc9cf010d12f9f5` |
| `docs/agent-governance/templates/closeout-report.md` | `c92677b600602332f764aec8ef784761b18bed67` |
| `.codex/agents/tars-general-reviewer.toml` | `c2a239d30d6be9be410b68b62d8d92a6f4b8aa80` |
| `.github/agents/tars-reviewer.agent.md` | `7d399efd2c129184defa01799c5641974c96901d` |

## Retained semantics and project boundaries

- Retain bounded scope, separate worker/reviewer/triage sessions, deterministic
  checks, immutable review snapshots, Full → Triage → Fix → Delta, truthful
  acceptance evidence, human merge/release and trusted-base governance review.
- Use neutral formats and role names. Planning depth is proportional to delivery
  complexity. Requirement approval, implementation and verification remain
  distinct; automated, manual and hybrid verification are supported.
- Source code, business/trading safeguards, architecture, source-of-truth paths,
  branch strategy, runtime commands, runner labels, deployment and local approval
  authorities stay in each project. Stricter local policy remains binding.

## Concrete adaptation hazards

- Artifaktory's Task Packet example uses `origin/main`, while its root policy
  requires ordinary PRs target `staging`. Resolve the actual project policy;
  never adopt an example branch blindly.
- Tars's example binds `origin/feature/frontend`, AO ownership, trading-specific
  forbidden actions and `tars.agent.task.v1`. These are not universal defaults.
- Artifaktory's workflow binds `ci-heavy` self-hosted runners, privileged workspace
  repair, aggressive Git cleanup and project-specific Python scripts. Its checks
  inform this bootstrap; that workflow is not copied as a portable implementation.
- Source agent files refer to project-specific skills and catalogs. Neutral
  adapters must reference available local contracts and declare restricted tools.

## Enforcement limits

The source repositories contain signed Publish-Go, finding seals, local history
anchors and extended review-chain validators. Those implementations are **not
ported** here. Their review semantics inform the policy; this bootstrap does not
claim their signatures, history retention, publish gates or agent runtime controls
are installed or enforced. Structural/consumer tests do not prove a semantic
review occurred. Human decisions and repository controls remain separate from
schema validation; actual bootstrap checks and reviews must be reported separately.

## Follow-up complete ecosystem mapping

The bootstrap's 26-file reference table above remains its historical extraction
record. The follow-up [complete bounded inventories](inventory/README.md)
map 501 Tars and 418 Artifaktory source files individually, including current
Artifaktory staging and its comparison to main. The [section consolidation map](../adapters/codex-consolidation.md)
records what is actually integrated and what remains local or deferred. Inspection
coverage and source contradictions are explicit; tree inventory is not code review.
