# Engineering Backbone

A reusable repository structure with shared engineering policy, agent instructions,
documentation and validation tools. The files in this repository already occupy
the paths used by a copied project. New projects start by copying the reviewed tree
and filling in their own product facts; they do not need to render a template.

The direct-copy layout was human-merged in PR #18. The current
[architecture-contract delivery](docs/changes/backbone-architecture-contract/plan.md)
adds the shared route from requirements to justified design and verification.
A merged layout, a draft document or a previous-head PASS does not establish an
approved release, product readiness or adoption in another repository.

## Where files belong

```text
engineering-backbone/                 # becomes your project's repository root
├─ apps/
│  ├─ frontend/
│  │  ├─ src/                         # web UI and its application code
│  │  └─ tst/                         # frontend tests
│  ├─ backend/
│  │  ├─ src/                         # API, services and domain code
│  │  └─ tst/                         # backend tests
│  └─ automation/
│     ├─ src/                         # agents, workflows or automation code
│     └─ tst/                         # automation tests
├─ packages/                          # shared product libraries; each has src/ and tst/
├─ contracts/                         # shared API/data contracts
├─ tst/                               # tests across product components
├─ infra/
│  └─ docker/engineering-backbone/
│     └─ Dockerfile                   # image for Backbone tooling only
├─ config/                            # shared product runtime configuration
├─ scripts/                           # shared product/repository commands
├─ docs/
│  ├─ agent-governance/               # shared policy, procedures and adapter guides
│  ├─ templates/                     # reusable engineering document kits
│  │  ├─ examples/                   # task, requirement and review JSON examples
│  │  └─ architecture/               # architecture, decisions, scenarios and reviews
│  ├─ requirements/                   # product requirements
│  ├─ architecture/                   # product design and decisions
│  ├─ changes/                        # plans, reviews and evidence by delivery
│  ├─ quality/                        # policy and project quality documentation
│  └─ operations/engineering/         # tooling, workflow and repository operations
├─ .engineering-backbone/             # a directory containing the engineering tools
│  ├─ src/
│  │  └─ maintenance/                 # compilers for reviewed guards and fingerprints
│  ├─ tst/                            # tests of Backbone itself
│  ├─ schemas/                        # engineering data contracts
│  ├─ standards/                      # reviewed rule catalogs and profiles
│  ├─ legacy/templates/               # existing Copier users' compatibility assets
│  ├─ requirements.txt                # direct Python tooling dependencies
│  ├─ requirements.lock               # exact tooling resolution and hashes
│  ├─ core.json                       # mandatory governance invariants
│  ├─ project.json                    # this project's name, branch and check command
│  └─ opencode.json                   # inactive OpenCode companion configuration
├─ .github/                           # native GitHub workflows and Copilot files
├─ .vscode/                           # shared, portable VS Code configuration
├─ .codex/                            # native Codex profiles
├─ .opencode/                         # native OpenCode profiles and skills
├─ AGENTS.md                          # project agent entrypoint
├─ CONTRIBUTING.md                    # project work and verification commands
├─ SECURITY.md
├─ copier.yml                         # legacy Copier discovery entrypoint only
└─ opencode.json                      # native OpenCode configuration
```

The product folders contain explanatory placeholders. They are not working web,
backend or automation applications. Keep the components a project needs; add a
component such as `apps/desktop/` with its own `src/` and `tst/` when that project
requires it. A Mastra application can put `mastra/agents`, `mastra/tools` and
`mastra/workflows` inside `apps/automation/src/` when its stack is selected.
Artifaktory and Tars are not moved or configured by this PR.

Dependency and build files stay beside the component they describe, in the
locations its tools require. They are not collected into a generic dependencies
folder. The following are placement examples, not files already supplied here:

| Files or settings | Location in a future project |
| --- | --- |
| Frontend `package.json`, component build configuration | `apps/frontend/` |
| Python `pyproject.toml`, requirements or constraints files | `apps/backend/` or the relevant Python component |
| Automation `package.json` and `tsconfig.json` | `apps/automation/` |
| Component-owned lockfile | Beside its native dependency manifest |
| Workspace manifest, shared lockfile, workspace build configuration | Repository root when the selected workspace tooling requires it |
| Shared library manifest and code/tests | `packages/<name>/`, with `src/` and `tst/` |
| Product Dockerfiles and deployment configuration | `infra/`, with build contexts documented for each component |
| Runtime configuration examples | `config/`; secrets and local environment values stay untracked |
| Tool/IDE discovery configuration | Its native location, such as `.github/`, `.vscode/` or a root configuration file |

`.engineering-backbone/` is an ordinary directory, not an IDE file or an application
framework. Its dependencies and tests belong to engineering tooling. Product
languages, frameworks, dependencies and build systems remain project decisions.

## Existing files and first adoption

The [complete relocation map](docs/changes/backbone-layout/mapping.md) accounts for
all 495 existing files. Policies and guides move to their final documentation
locations; validators, schemas and tests move into the tooling directory. Native
agent files stay in their tool's discovery paths. Earlier plans and reviews are
preserved under [change history](docs/changes/README.md), with their original bytes
and claims; they are not evidence that a copied product has passed its checks.

Follow the [direct-copy adoption guide](docs/agent-governance/adoption.md). It lists
what must be changed for a project: project facts, root instructions, active task,
actual build/test commands, CI and runner settings. Copy dotfolders, exclude Git
metadata and local output, and preserve existing stricter project instructions.
The source-only CI identity restriction remains intentional; copying these files
does not create ready-to-run downstream CI or authorize provider activation.

The retained Copier compatibility assets serve existing generated consumers at
their previous paths. Their initial-copy/update tests and protection of local
instructions remain required. They are not the starting path for the new reference
layout. Automatic updates of directly copied repositories are future work.

## Validate this repository

Use Python 3.12 in an isolated environment and the reviewed lockfile:

```sh
python -m venv .venv
# Activate the environment using your platform's normal command.
python -m pip install --require-hashes -r .engineering-backbone/requirements.lock
python .engineering-backbone/src/validate.py
python .engineering-backbone/src/maintenance/compile_navigation.py --check
python .engineering-backbone/src/maintenance/compile_quality_framework.py --check
python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check
python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check
python .engineering-backbone/src/check_source_dependencies.py
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
git diff --check
```

The dependency check requires the actual inputs to be Git-tracked. Container build
and smoke commands are in the [tooling compatibility contract](docs/operations/engineering/dependency-compatibility.md).
Structural checks do not establish native agent discovery, model behavior, human
approval, repository protections or product compatibility. Missing evidence and
failed gates stay visible.

## Shared engineering documents

- [Core policy](docs/agent-governance/core.md) and [quality policy](docs/quality/policy.md)
- [Agent adapters](docs/agent-governance/agent-adapters.md), [Copilot workflow](docs/agent-governance/adapters/copilot/workflow.md) and [OpenCode contract](docs/agent-governance/adapters/opencode/workflow.md)
- [Planning and evidence formats](docs/agent-governance/planning.md) and [document navigation](docs/agent-governance/agent-navigation.md)
- [Requirements-to-architecture contract](docs/agent-governance/architecture.md), [document kit](docs/templates/architecture/README.md) and [worked example](docs/templates/architecture/worked-example.md)
- [Quality framework](docs/quality/README.md), [testing](docs/quality/testing.md) and [dependency policy](docs/quality/dependencies.md)
- [Engineering workflows](docs/operations/engineering/workflows/README.md) and [repository controls](docs/operations/engineering/repository-controls.md)
- [Contribution process](CONTRIBUTING.md), [source provenance](docs/agent-governance/sources/source-provenance.md) and [security reporting](SECURITY.md)

Changes follow scoped planning, independent plan review, implementation and checks,
frozen Full review, triage, confirmed repairs and Delta review. Human merge and
release decisions remain separate; no downstream update or activation is automatic.
