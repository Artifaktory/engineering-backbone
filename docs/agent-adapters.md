# Codex and Copilot adapters

The baseline is [policy/core.md](../policy/core.md). Both entrypoints contain its
essential rules inline. Copier renders the shared essential fragment and role
bodies into native files; provider profiles do not constitute a new orchestrator.

| Purpose | Codex | Copilot |
| --- | --- | --- |
| Standing instructions | Root `AGENTS.md` | `.github/copilot-instructions.md` |
| Planner | `.codex/agents/backbone-planner.toml` | `.github/agents/backbone-planner.agent.md` |
| Implementer | `.codex/agents/backbone-implementer.toml` | `.github/agents/backbone-implementer.agent.md` |
| Independent Full or Delta reviewer | `.codex/agents/backbone-reviewer.toml` | `.github/agents/backbone-reviewer.agent.md` |

The three Codex profiles retain their existing contract. Copilot additionally has
analyst, plan reviewer, test engineer, quality checker, security reviewer,
documentation and finding triage profiles: ten roles total. Its eight procedural
skills and core/optional path rules are defined in
[the Copilot operating guide](copilot/workflow.md). Specializations map to existing
Task Packet roles; generic schemas are not expanded. The planner returns a plan,
the implementer owns scoped changes and the reviewer reports findings read-only.
Delta is a reviewer invocation with confirmed IDs and a repair range, using its
own skill rather than an additional profile.
No model, reasoning, credential, MCP server or machine-specific settings are forced.

## Installation and updates

Select adapters with `use_codex` and `use_copilot`. Select optional technical rules
with `copilot_python_profile` and `copilot_frontend_profile` (both default false);
core governance/test/docs path rules accompany Copilot. The language and
frontend/backend answers record facts; they do not select rules implicitly or
generate application infrastructure.
The template has no tasks, migrations, custom Jinja extensions or shell hooks.

Copier creates native entrypoints and profiles only when absent. It preserves all
existing `AGENTS.md` files, Copilot instructions, profiles in both native agent
directories, Copilot skills/path instructions, and `.engineering-backbone/project.json`.
The same ownership rule applies to existing three-role consumers and new extended
installations. Copier always updates the
canonical core and `AGENTS.fragment.md` / `Copilot.fragment.md` under
`.engineering-backbone/`, plus the neutral `copilot-guide.md`. These are integration
material; neither product
loads them automatically. During initial adoption and later updates, manually
refresh the protected native files through a reviewed PR, preserving stricter
local rules. Keep project facts and Copier answers consistent when they change.

Pin the initial copy and each update to a reviewed commit or release reference.
Use Copier in a clean Git worktree; inspect conflicts, run project checks and obtain
independent review before merging. A successful template update is not proof of
runtime discovery or completed adoption. Never merge a baseline update automatically.

The answers file is intentionally namespaced. From the consumer repository use
`copier update --answers-file .engineering-backbone/copier-answers.yml --vcs-ref APPROVED_COMMIT`.
The explicit answers-file option is required for update discovery.

Adapter selection (`use_codex`, `use_copilot`) and the template-generated workflow
choice (`backbone_workflow_ref`), along with the two optional Copilot profile
choices, are installation-only. Missing profile answers in legacy bundles mean
false. Copier reads the installed
answers with its built-in external-data support and rejects changes to those choices
before rendering into the consumer. This prevents conditional selection changes
from deleting native policies despite Copier's skip-if-exists behavior. A fresh copy
may report the expected missing installed-answers warning.

Changing an adapter requires a separate reviewed migration of native files and
project facts, with deliberate handling of the saved installation choices. Do not
alter or remove the answers file merely to bypass the guard. A baseline update
keeps the current installation choices. Consumer CI also prevents a candidate's
project facts from disabling a provider enabled in the trusted base. Retiring such
a provider needs a separately approved baseline-policy migration; flipping facts
cannot hide its inherited instruction or permission checks.

For initial adoption, leave `backbone_workflow_ref` empty, merge a reviewed seed
bundle, then manually add the pinned caller in a separate activation PR as described
in [adoption](adoption.md). The empty saved answer records what Copier generated;
it does not prohibit a separately maintained caller. Activating, removing or
repinning that caller is a reviewed manual workflow migration and does not require
changing the installation-only answer. Existing callers are preserved by Copier.
Case-only workflow SHA input is normalized to lowercase in generated callers;
the template never changes an existing workflow's reviewed pin automatically.
Tooling updates must include the matching reviewed workflow pin: that workflow
attests the complete validator/schema/dependency tuple before trusting either
snapshot, while project-specific facts and stronger local rules remain outside the
fingerprint. See [adoption](adoption.md) for the update procedure.

The consumer receives the centrally compiled `requirements.lock` with exact direct
and transitive versions and hashes. In an isolated Python 3.12 environment, install
with `python -m pip install --require-hashes -r .engineering-backbone/requirements.lock`,
then run `python .engineering-backbone/validate.py --root .`. The companion
`requirements.txt` retains direct dependency metadata. Compile/update the lock
centrally during dependency maintenance; Copier never runs that compiler or hooks.

## Native formats and limits

Codex roles use standalone TOML under `.codex/agents/` with required `name`,
`description` and `developer_instructions`. Planner/reviewer default to
`sandbox_mode = "read-only"`; implementer defaults to `workspace-write`. Current
local Codex clients load these profiles for spawned sessions. Older clients and
Codex GitHub review integration require separate verification/setup. Parent live
permission overrides can supersede a child's read-only default. Do not use elevated
runtime permissions as a substitute for a controlled independent review.

Copilot profiles use `.github/agents/*.agent.md`; skills use
`.github/skills/<name>/SKILL.md`; path rules use
`.github/instructions/*.instructions.md` with `applyTo`. Explicit tools limit
available operations; they are not a filesystem sandbox. In particular a quality
checker with `execute` can write through commands and must obey its approved scope.
The existing three profiles remain compatible; additional roles use deliberate
manual transitions and optional `send: false` handoffs, with fresh reviewer sessions.

Copilot support differs across hosts and versions. Use
[the client matrix](copilot/clients.md) for PyCharm/JetBrains, VS Code Local versus
Agent Host, CLI, cloud agent and PR review. A native reviewer does not automatically
become the PR bot; product access and review settings are separate. Assess changed
instructions against trusted-base policy, and retain human merge approval.

Codex combines instruction files root-to-current-directory; Copilot documents
nearest `AGENTS.md` precedence for agent instructions. Use the common root baseline
and reviewed stronger local additions; do not assume identical nested resolution.

## Runtime discovery smoke check

After installation, start a new supported Codex session at the repository root and
ask it to list active instructions and available `backbone_*` roles. Start the
planner or reviewer and check that it reports its role and scoped boundaries without
writing files. Repeat from any relevant nested directory.

For Copilot follow [the runtime smoke checklist](copilot/smoke-tests.md): verify
all ten selected profiles, eight skill procedures, applicable rules and real tool
calls in the intended client. Capture actual versions and observations. GitHub
automatic PR review is tested separately in an authorized PR. CI parsing and
instruction simulations do not establish runtime loading or review quality.

## Official references

Verified on 2026-10-12; formats may evolve:

- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex subagents and native TOML](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Copilot custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Copilot instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review)

## Consolidated source-project contract

[The consolidation map](codex-consolidation.md) identifies the shared sections now
present in native profiles and generated fragments, and the controls retained in
each project. Codex keeps its three profiles; Copilot's ten native profiles map
specialized responsibilities to a narrowed Task Packet using existing schema role
values. Do not invent role values or unknown evidence fields. Keep richer
review metadata in existing claim/evidence fields or a companion report.

Native files remain protected on update. Refreshing `.engineering-backbone/core.md`
and instruction fragments does not refresh protected native role bodies. Reconcile
approved common changes manually in the consumer PR, preserving stricter rules.
