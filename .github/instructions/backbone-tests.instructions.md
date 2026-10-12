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
