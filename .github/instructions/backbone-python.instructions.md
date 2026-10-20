---
applyTo: "**/*.py"
---

Follow the [canonical policy](../../docs/agent-governance/core.md) and
[Copilot workflow](../../docs/agent-governance/adapters/copilot/workflow.md) together with applicable project instructions.

This optional profile adds Python-specific guidance without selecting a framework.
Read project package/runtime configuration, path instructions and approved commands.
Preserve public contracts and typed boundaries; cover error paths and resource
cleanup proportionally to the change. Follow the installed formatter, linter,
type-checker and test conventions. Do not add dependencies, rewrite packaging or
run reference-project commands unless the Task Packet authorizes that scope.

Read the optional `.engineering-backbone/quality-profile.json` when present and
apply its exact profile/catalog versions and relevant rule IDs/versions to this path's
work. Carry required evidence and gaps in the Task Packet/handoffs; retain
stricter local rules and do not infer adoption, execution or certification.
