# Copilot clients and GitHub review

Checked against the official sources on **2026-10-12**. Capabilities depend on the
installed client, session harness, organization policy and available tools. This
repository prepares files; it has not run a signed-in PyCharm, VS Code, CLI or
GitHub Copilot task. Follow [runtime acceptance](smoke-tests.md) before declaring
a host ready.

## Client matrix

| Surface | How to use this package | Host-specific boundary |
| --- | --- | --- |
| PyCharm / JetBrains Copilot | Open the project, select a repository custom agent and verify instructions/skills in that plugin | GitHub currently documents custom agents as public preview. Record IDE, plugin and Local/Copilot-session type; test actual discovery rather than extrapolating from VS Code |
| VS Code Local agent | Select a `.github/agents` profile and use its repository skills and applicable path rules | Local prompt files remain supported and can override agent tool selection. Inspect effective tools; this package does not distribute prompt files |
| VS Code Copilot Agent Host | Choose the Copilot session target, then select the custom agent and verify repository skill discovery | Agent Host does not load `.prompt.md` files; use skills. Host-side customizations and hook behavior differ from Local settings |
| GitHub Copilot CLI | Start at repository root and select the intended agent with `/agent` or the supported CLI agent option | Verify aliases with real file/search calls in the installed version. Missing tools are a blocker, not authority to enable all tools |
| GitHub cloud agent | Select the repository profile for the intended task and explicitly supply its packet and files | GitHub ignores IDE `handoffs`; select each next profile manually. This package does not rely on a cloud agent to create reviewer independence |
| GitHub PR code review | Separately enable/request the product review and test on an authorized PR | A selected custom reviewer is a different surface. PR bot guidance and skills come from PR head; trusted CI and human approval remain separate |

JetBrains plugin **1.18.0** added organization/enterprise skills and managed
instructions, according to the
[2026-09-22 GitHub changelog](https://github.blog/changelog/2026-09-22-new-features-and-improvements-in-copilot-for-jetbrains/).
Those wider installation options are not configured by this PR. Repository-level
files keep the first adoption local and reviewable.

For VS Code use the
[custom-agent documentation](https://code.visualstudio.com/docs/agent-customization/custom-agents),
[skills documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills)
and [prompt-file boundary](https://code.visualstudio.com/docs/agent-customization/prompt-files).
The [migration guide](https://code.visualstudio.com/docs/agent-customization/migrate-customizations)
documents separate customization locations and no automatic hook migration.
Do not transplant Local settings or hook scripts into Agent Host without a scoped
runtime change; no hooks or machine configuration are installed here.

## Tools and role changes

Every profile declares a tool list. GitHub documents omitted lists as allowing
all tools and unrecognized names as ignored; actual binding must be observed in
the target runtime. This package uses portable aliases and explicit budgets,
not broad wildcard MCP access. A tool name in a report proves nothing until a
matching operation succeeds.

Reviewer independence means a separate session and frozen snapshot. A handoff
button within an author's session can help navigate, but does not create
independence. New handoffs use `send: false`; verify the target role before
submitting. Return reports read-only and have an authorized writer persist them.
The quality checker has command execution, which can also perform writes; it
must still follow the packet's approved commands and scope.

See [GitHub's agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
for aliases and the cloud handoff restriction, and
[custom instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support)
for surface-specific instruction support.

## User reports converted into acceptance probes

These are version-specific user observations, not proof that every current client
has the defect. We use them to choose useful tests and preserve a manual fallback.

| Report checked on 2026-10-12 | Reported environment | Our acceptance probe |
| --- | --- | --- |
| [github/copilot-cli #4594](https://github.com/github/copilot-cli/issues/4594) | Windows headless CLI `1.0.81-9`: `search`/`web` aliases reportedly bind no tools; later comments describe further versions | Run a real known-file search, record tool/output, and stop if unavailable. An explicitly reviewed literal-tool migration is possible; removing the budget is not the fallback |
| [microsoft/vscode #336666](https://github.com/microsoft/vscode/issues/336666) | VS Code Insiders, Agents Window and Copilot CLI Agent Host, observed 2026-09-17: peer-chat result truncated | Transfer the full report through a shared, authorized artifact path and verify its final section; do not rely on a clipped transcript |
| [microsoft/vscode #311420](https://github.com/microsoft/vscode/issues/311420) | VS Code `1.117.0-insider`, Copilot Chat `0.45.2026042001`, macOS: handoff reportedly leaves planner active | Verify target identity and tools; if wrong, stop and select a fresh session manually. Never grant edit access to the planner to bypass the failure |

This package does not enable web tools solely to work around the CLI report.
Authority-bearing Task Packets and finding records live in project files; no
external report grants permission to change this project's guardrails.

## Configure GitHub PR code review separately

The human/operator enables Copilot product access and the desired automatic-review
setting or ruleset after checking the account/repository's available controls.
This implementation neither changes those settings nor creates downstream PRs.
See [automatic review configuration](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review).

Keep bot-facing repository and path guidance short and concrete. GitHub's
[review customization tutorial](https://docs.github.com/en/copilot/tutorials/customize-code-review)
supports focused criteria and documents reading instructions and skills from PR
head. Put relevant criteria inline: external links, desired comment formatting
and prose requests to block merge are not enforcement mechanisms. The detailed
Full/triage/fix/Delta report contract belongs to the selected reviewer procedure.

For each authorized test PR, record the exact reviewed head, provider result and
coverage. Capture a bot finding into our finding record, triage it, repair confirmed
IDs and independently Delta-review the repair. Do not assume thread replies become
context for the next bot review; supply the evidence through the supported review
inputs and recorded files. A clean bot summary does not replace required checks,
independent reviews or the human merge decision.
