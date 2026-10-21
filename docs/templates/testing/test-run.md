# Test or verification execution record

Status: not executed. Expected outcomes belong to the design; observed outcomes
remain absent until actual execution. Use the [testing contract](../../quality/testing.md)
and the project's existing evidence/retention rules.

## Exact execution subject

| Field | Actual value, or explicit unavailable prerequisite |
| --- | --- |
| Run identity | Unique run/attempt ID, executor and timestamp/timezone |
| Authorized scope | Packet, strategy and requested verification gate |
| Source and test revisions | Actual base/head or equivalent immutable product and procedure identities |
| Built/delivered subject | Artifact identity/hash and build-input linkage where applicable |
| Environment | Actual OS/runtime/tool versions, dependency/configuration and data identities |
| Capability boundary | Real integration/provider/platform versus fixture, mock, simulation or analysis |
| Invocation | Actual command and working directory, CI check/run/job IDs or manual procedure revision |
| Prerequisite readiness | Required inputs/access and actual readiness; unresolved blockers |
| Evidence handling | Resolvable report/log location, access, redaction and retention owner/period |

Do not copy expected versions into these fields as if observed. A build, source
checkout and delivered package can differ; record the subject actually exercised.
Never expose credentials or sensitive test data in a durable report.

## Observations

| Test/case ID and version | Execution lifecycle | Actual result | Expected versus observed | Evidence and finding IDs |
| --- | --- | --- | --- | --- |
| Required case | Not run until started | Not assessed | No observation yet | Pending |

Record actual start/end, exit code where applicable, measured values and relevant
stdout/report evidence. Separate lifecycle (not run/running/finished/cancelled)
from outcome (pass/fail/blocked/error/skipped/inconclusive where the project maps
these meanings). A failed expected behavior is different from an unusable result
caused by the test, tool or environment. A queued job is not an executed test.

These are companion-report meanings, not new JSON values. Map existing fields
through the contract; keep raw runner states and unsupported information in the
companion record. An expected result, empty report or exit zero alone does not
establish every required acceptance claim.

## Deviations, attempts and validity

- Record failures, anomalies, missing evidence and their affected scope; identify
  whether product, test/procedure, environment or unresolved analysis owns the cause.
- Preserve the first failure and each relevant attempt. Give any retry a reason,
  changed condition or bounded diagnostic question; do not repeat unchanged failures
  until one run happens to succeed.
- For flaky behavior, retain the uncertain result, owner, diagnosis/repair work,
  expiry of any permitted isolation and its visible gate effect. Required gaps stay
  blocking unless an actually allowed exception is independently established.
- Record stop/resume conditions and which partial observations remain usable.
- Assess evidence applicability to the current product/configuration. Later changes
  may invalidate a claim without changing the historical execution result.

This record supplies observations, not independent approval. Use
[test completion](test-completion.md) for the overall coverage and gate assessment.
Source basis: original prompts informed by T-S03, T-S07/T-S08 and T-S09 in the
[source register](../../quality/testing-sources.md#reference-register).
