# File relocation crosswalk

Baseline: `212608aa50ee517b3dd3107a9480da997222fd4f`. The [machine-readable map](layout-map.json) accounts for all 495 tracked baseline blobs exactly once. Each entry records old path, destination, baseline Git blob, byte size, disposition and whether contents must remain identical. It is a migration inventory, not an executable source of authority. No baseline file is silently discarded. New reference-directory READMEs, current change records and regression checks are additional files.

| Existing location | Reference location | Treatment |
| --- | --- | --- |
| `policy/core.md` | `docs/agent-governance/core.md` | Canonical prose authority; update relative links only as required |
| `policy/{quality,dependencies}.md` | `docs/quality/{policy,dependencies}.md` | Shared quality/dependency authority |
| `policy/core.json` | `.engineering-backbone/core.json` | Exact invariant bytes preserved |
| `schemas/`, `standards/` | `.engineering-backbone/{schemas,standards}/` | Tool contracts/catalogs; no new schema fields or rule weakening |
| Runtime `scripts/*.py` | `.engineering-backbone/src/` | Runtime and checks |
| `scripts/compile_*.py` | `.engineering-backbone/src/maintenance/` | Integrity maintenance, still required |
| `tests/` | `.engineering-backbone/tst/` | Tests move; fixture bytes and internal identities stay intact |
| Root `requirements.txt`, `requirements.lock` | `.engineering-backbone/` | Exact tooling dependencies; no product dependency claim |
| Root `Dockerfile` | `infra/docker/engineering-backbone/Dockerfile` | Backbone tooling image; root build context retained |
| `templates/` | `.engineering-backbone/legacy/templates/` | Legacy Copier compatibility only; includes read canonical sources |
| `copier.yml` | `copier.yml` | Root discovery entry remains for existing Copier users; not the direct-copy route |
| `docs/{agent-adapters,agent-navigation,planning}.md` | `docs/agent-governance/` | Current agent procedures |
| `docs/{copilot,opencode}/` | `docs/agent-governance/adapters/{copilot,opencode}/` | Current native-client contracts |
| `docs/codex-consolidation.md` | `docs/agent-governance/adapters/codex-consolidation.md` | Current consolidation/provenance guide |
| `docs/source-{inventory,provenance}` | `docs/agent-governance/sources/` | Pinned inventory JSON bytes preserved; current navigation links may be repaired |
| `docs/workflows/` | `docs/operations/engineering/workflows/` | Existing engineering operations/catalog |
| `docs/{dependency-compatibility,repository-controls}.md` | `docs/operations/engineering/` | Tooling operations and repository controls |
| `docs/adoption.md` | `docs/agent-governance/adoption.md` | Direct-copy instructions plus explicit legacy compatibility |
| `examples/` | `docs/templates/examples/` | Document/data examples |
| `plans/`, `docs/reviews/` | `docs/changes/backbone-<delivery>/{plans,reviews}/` | Historical files unchanged, associated by delivery |
| `.github/`, `.codex/`, `.opencode/`, `opencode.json` | Same native locations | Discovery paths stay native; canonical references updated |
| Root entrypoints and ignore files | Root | Human/tool entrypoints; clarify project-owned settings |

Historical delivery groups: bootstrap, ci-clone-repair, codex-consolidation, codex-security, copilot-development, dependency-compatibility, opencode-governance, quality-framework, technology-navigation and workflow-kit. The archive index maps old links to source commit and destination; old commands and PASS claims remain historical observations.
