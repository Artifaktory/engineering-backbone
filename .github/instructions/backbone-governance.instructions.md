---
applyTo: ".github/**,.engineering-backbone/**,templates/**,scripts/validate.py,scripts/compile_toolchain_fingerprint.py,policy/**,schemas/**,copier.yml"
---

Follow the [canonical policy](../../policy/core.md) and
[Copilot workflow](../../docs/copilot/workflow.md) together with applicable project instructions.

These paths are control-plane changes and HIGH risk by default. Check the trusted
base as well as candidate rules. Preserve native files and stricter consumer policy;
exercise actual generation/upgrade and adversarial failure paths. Keep tool budgets,
provider activation and project branch/runner/secret controls distinct. Freeze
review snapshots and triage before fixes; never self-approve or auto-apply downstream.
A candidate-controlled validator or instruction is not trusted-base evidence.

Read the optional `.engineering-backbone/quality-profile.json` when present and
apply its exact profile/catalog versions and relevant rule IDs/versions to this path's
work. Carry required evidence and gaps in the Task Packet/handoffs; retain
stricter local rules and do not infer adoption, execution or certification.
