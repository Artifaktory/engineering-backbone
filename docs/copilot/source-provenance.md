# Copilot source provenance and adaptation

Checked on **2026-10-12**. These pinned practical examples informed the package's
design; upstream branches remain free to evolve. Our role and skill text is
authored for this backbone's existing policy and schema, rather than importing an
upstream agent library. No upstream installation script, plugin, hook or executable
integration is installed. Upstream assumptions never override local governance.

## Practical examples inspected

| Source at immutable commit | File and Git blob | Pattern used and boundary |
| --- | --- | --- |
| `microsoft/vscode@3b486b1ff92ac032974c6f589e7d5a46fe486067` | [`.github/skills/code-review/SKILL.md`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/.github/skills/code-review/SKILL.md), `2c703c7e652aa1c925605e7176fa6e37ae405028` | Review trigger, complete diff coverage and concrete defect causation; combine with our immutable snapshot and Full/Delta contracts |
| Same VS Code revision | [`.github/skills/unit-tests/SKILL.md`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/.github/skills/unit-tests/SKILL.md), `bfadcdf8da2225ca33e5b2409ad50a191f354b56` | Capability-aware test procedure and explicit environment prerequisites; do not copy Electron/Mocha/build commands into unrelated projects |
| Same VS Code revision | [`extensions/copilot/src/extension/chatSessions/copilotcli/node/copilotCli.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/extensions/copilot/src/extension/chatSessions/copilotcli/node/copilotCli.ts), `7b767d48b1a47f6f43195f9f29d186308058a14c` | Primary host evidence: the CLI bridge resolves and merges agents by header name, case-insensitively, and absent tools become an unrestricted default. Reserve managed header identities as well as filenames; do not infer every client's duplicate-file precedence |
| Same VS Code revision | [`promptsServiceImpl.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/workbench/contrib/chat/common/promptSyntax/service/promptsServiceImpl.ts), `338149b1a56ea1f50be73e19244023398f530d12`; [`yaml.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/base/common/yaml.ts), `64679352573b69990a3996802f2f24c81c0ae561` | An explicitly empty name survives into the CLI filename fallback; the lightweight parser also treats a present missing scalar as empty. Check reserved fallback names and handle the trusted parser difference conservatively, without claiming absent-name or universal-client precedence |
| `microsoft/skills@d5741a1e9325adead3a28d1d203bb69283907e06` | [`.github/agents/planner.agent.md`](https://github.com/microsoft/skills/blob/d5741a1e9325adead3a28d1d203bb69283907e06/.github/agents/planner.agent.md), `bc29ea60192d67de4878d8ca1bb18f1fe67a22f7` | Explicit read-only planner, plan sections and deliberate handoffs; omit CoreAI DIY paths, Azure, Zustand, React and Pydantic assumptions |
| `github/awesome-copilot@70ddff7fab9d4d49743d221b56d761cff58048d0` | [`agents/planner.agent.md`](https://github.com/github/awesome-copilot/blob/70ddff7fab9d4d49743d221b56d761cff58048d0/agents/planner.agent.md), `cb1518a913319d4ccd3723f116ad598e43204e2a` | Small purpose-specific plan profile; adapt its IDE-specific tool names into explicitly tested portable budgets |
| Same Awesome Copilot revision | [`agents/agent-governance-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/70ddff7fab9d4d49743d221b56d761cff58048d0/agents/agent-governance-reviewer.agent.md), `1d3d80676271c53ad192e0c7205aec82f7f2a176` | Inspect existing controls and delegation boundaries. Do not copy its fixed model, terminal-capable reviewer or speculative trust-scoring/intent-classifier architecture |
| `github/spec-kit@03de661789b74405ae93b8b532d52d2cf8af422e` | [`design/integration.md`](https://github.com/github/spec-kit/blob/03de661789b74405ae93b8b532d52d2cf8af422e/design/integration.md), `b110bbafca7eaa3cecd95a2307255fc11d62b7df` | Separate common process from native adapters and make generated-file ownership explicit; retain Copier and our reviewed trust boundary, without Spec Kit's package runtime/lifecycle |

The VS Code unit-test skill is the actual inspected testing source; there is no
assumption that a `writing-tests` skill exists at that pin. The Awesome Copilot
[README](https://github.com/github/awesome-copilot/blob/70ddff7fab9d4d49743d221b56d761cff58048d0/README.md)
(`a8fc4a9664d2c7115d9560c3de6a44ad68af6b4d`) was inspected for its distinction
between agents, instructions and skills, not as an instruction to install everything.

## Licenses checked at the same pins

All four inspected projects declare the MIT License. The following license files
were fetched and read; they remain the upstream notices. This package reuses design
patterns, with independently authored procedural text, and does not vendor their
files or substantive passages. Future direct copying needs the applicable notices
included in the copied deliverable and review of the specific file's license.

| Source | License file and blob |
| --- | --- |
| Microsoft VS Code | [LICENSE.txt](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/LICENSE.txt), `0ac28ee234d232ac0691f39cebf95bf6b2a763a5` |
| Microsoft Skills | [LICENSE](https://github.com/microsoft/skills/blob/d5741a1e9325adead3a28d1d203bb69283907e06/LICENSE), `79656060de00aa4659ad2c276d5be8830664d544` |
| Awesome Copilot | [LICENSE](https://github.com/github/awesome-copilot/blob/70ddff7fab9d4d49743d221b56d761cff58048d0/LICENSE), `89bc5e962c9944cdb050887062afdaaf89be504a` |
| Spec Kit | [LICENSE](https://github.com/github/spec-kit/blob/03de661789b74405ae93b8b532d52d2cf8af422e/LICENSE), `28a50fa22639e32febe14e4ffc7a732b0ba8c90a` |

## Official capability references

- [GitHub custom-agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration): native profile metadata, explicit tool budgets, aliases and ignored cloud handoffs.
- [Creating custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents) and [about custom agents](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents): profile selection and documented JetBrains preview boundary.
- [GitHub agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills): procedures loaded for relevant tasks, including supported code-review/CLI/IDE surfaces.
- [Custom instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support): verify the intended host before claiming file discovery.
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents) and [skills](https://code.visualstudio.com/docs/agent-customization/agent-skills): role/skill composition and selected harness behavior.
- [VS Code prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files) and [migration](https://code.visualstudio.com/docs/agent-customization/migrate-customizations): Local versus Agent Host and customization migration boundaries.
- [GitHub PR review guidance](https://docs.github.com/en/copilot/tutorials/customize-code-review): focused inline review criteria and PR-head instruction/skill inputs.
- [JetBrains 1.18.0 changelog](https://github.blog/changelog/2026-09-22-new-features-and-improvements-in-copilot-for-jetbrains/): organization skill/instruction support added in that release.

These are capability observations, not runtime results for this repository. User
reports and their exact environment boundaries are recorded in
[clients.md](clients.md). [Smoke tests](smoke-tests.md) turn those observations into
actual client checks. [workflow.md](workflow.md) remains the operating contract,
also included verbatim in every generated neutral Copilot guide.
