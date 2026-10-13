---
applyTo: "tests/**,**/test_*.py,**/*.test.*,**/*.spec.*"
---

Follow the [canonical policy](../../policy/core.md) and
[Copilot workflow](../../docs/copilot/workflow.md) together with applicable project instructions.

Read the project's test conventions and commands first. Use smallest meaningful
fixtures and assert observable contract behavior. For fixes, record the actual
failure and repaired run; do not lower assertions, coverage, timeouts or gates for
green. Contract/control-plane changes require producer/consumer and failure-path
checks. Keep local test artifacts redacted and outside tracked evidence. A test name,
mock outcome or structural PASS does not prove host discovery or runtime behavior.

Read the optional `.engineering-backbone/quality-profile.json` when present and
apply its exact profile/catalog versions and relevant rule IDs/versions to this path's
work. Carry required evidence and gaps in the Task Packet/handoffs; retain
stricter local rules and do not infer adoption, execution or certification.
