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

The planner returns a Task Packet/plan; the implementer owns scoped changes and
actual validation; the reviewer reports findings read-only. Quality checking and
triage remain explicitly separate stages. Delta review is a scoped reviewer
invocation with confirmed finding IDs and a repair commit range, not a fourth agent.
No model, reasoning, credential, MCP server or machine-specific settings are forced.

## Installation and updates

Select adapters with `use_codex` and `use_copilot`. The language and frontend/backend
answers record project facts; they do not generate application infrastructure.
The template has no tasks, migrations, custom Jinja extensions or shell hooks.

Copier creates native entrypoints and profiles only when absent. It preserves all
existing `AGENTS.md` files, Copilot instructions, profiles in both native agent
directories, and `.engineering-backbone/project.json`. It always updates the
canonical core and `AGENTS.fragment.md` / `Copilot.fragment.md` under
`.engineering-backbone/`. Those fragments are integration material; neither product
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
choice (`backbone_workflow_ref`) are installation-only choices. Copier reads the installed
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

Copilot roles use `.github/agents/*.agent.md`: YAML frontmatter has `description`,
`name` and explicit tools; Markdown supplies instructions. Planner/reviewer tools are
`read` and `search`; implementer adds `edit` and `execute`. Omitting `tools` enables
all available tools, so the restricted roles set it explicitly. GitHub cloud agent
does not currently use VS Code `handoffs`; this baseline does not rely on them.

Copilot support differs across GitHub, CLI and IDE features. Its native custom
reviewer is selectable; it does not automatically become the PR code-review bot.
Copilot Code Review consumes supported standing instructions and requires product
access and separate automatic-review settings/rulesets. It reads PR instructions
from the head branch, so changed instructions must be assessed against trusted base
governance. Copilot approvals can technically count with an optional preview
setting; this project's human approval requirement still applies.

Codex combines instruction files root-to-current-directory; Copilot documents
nearest `AGENTS.md` precedence for agent instructions. Use the common root baseline
and reviewed stronger local additions; do not assume identical nested resolution.

## Runtime discovery smoke check

After installation, start a new supported Codex session at the repository root and
ask it to list active instructions and available `backbone_*` roles. Start the
planner or reviewer and check that it reports its role and scoped boundaries without
writing files. Repeat from any relevant nested directory.

In Copilot, verify the repository instruction appears in response references and
the three custom agents are available for selection in the intended client. Select
the reviewer, verify it cannot access edit/execute tools, and request review of a
frozen test commit. GitHub automatic PR review is tested separately in an authorized
PR. Record product/client version, revision and observed behavior. CI parsing only
establishes file structure, not runtime loading or AI review quality.

## Official references

Verified on 2026-10-12; formats may evolve:

- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex subagents and native TOML](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Copilot custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Copilot instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review)
