# OpenCode source provenance

The adapter and controlled-runner contract target the reviewed fixed version
**1.19.0**, source commit `733b2c627e5aec39cb33cc22373bdce33053ef2c` in
[anomalyco/opencode](https://github.com/anomalyco/opencode/tree/733b2c627e5aec39cb33cc22373bdce33053ef2c).
This is a compatibility pin, not a claim about the latest version. A version change
requires its own source/discovery review and actual runtime qualification.

Primary source inspection targets:

- [Configuration discovery](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/config/config.ts): local/global/ancestor inputs, environment settings and native instruction merge.
- [Agent configuration](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/config/agent.ts): native agent/mode discovery and legacy mode override order.
- [Skill discovery](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/skill/index.ts): recursive canonical/alternate roots, symlink traversal and name-keyed replacement.
- [Run command](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/cli/cmd/run.ts): primary selection and missing/subagent fallback.
- [Release assets](https://github.com/anomalyco/opencode/releases/tag/v1.19.0): native distribution, independently digest-checked before execution.

The controlled package therefore denies additional executable/configuration layers,
legacy mode/modes and extra recursive native SKILL.md paths, and checks exact primary
selection before inference. Environment permission overrides, global instructions,
plugins and live native changes remain runner concerns. The pinned
[native npm bootstrap](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/core/src/npm.ts)
uses `ignoreScripts: true`, while configuration still processes package/npm inputs.
Those host/global/bootstrap inputs remain runner boundaries; this observation is
neither an arbitrary install-script execution claim nor OS-isolation evidence.
Plugin initialization errors
or skipped hooks are not fail-closed governance evidence. Ordered permission defaults
are not OS isolation; permissive runtime switches cannot qualify a governed launch.

Pinned archive SHA256 values used by the portable smoke:

| Platform archive | SHA256 |
| --- | --- |
| Linux x64 | `7bb9e61ad6feacf2e89c10a6a2c1840e3de4220bb50ba1fc7110f31806076aec` |
| Windows x64 | `17108e9448c4fdad48eb8714c4ed6f5dfc9cf86c2eb8f2ce5d02043fef806eb5` |

Current reconstructed-source checks and actual runtime observations are recorded
separately in `smoke-tests.md` and the review records. Historical lost check logs do
not certify this replacement snapshot. No dynamic reproduction interrupted by an
automatic safety check is reused as successful evidence; bounded static inspection
and data-only regressions document that coverage limitation.
