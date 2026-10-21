# Test completion and verification assessment

Status: pending assessment; no completion, acceptance or release is established.
Apply the [testing contract](../../quality/testing.md),
[quality policy](../../quality/policy.md) and the requested project gate.

## Subject and assessment scope

Record assessment ID/revision, responsible checker and independent reviewer,
strategy/design revisions, actual tested product/build/platform identities and
included run IDs. State the gate being assessed and its decision authority.
A partial delivery assessment must identify its boundaries and outstanding work.

## Planned versus actual coverage

| Requirement / acceptance / material risk | Required method and test IDs | Actual run/evidence and applicable revision | Result / coverage gap | Owner and gate consequence |
| --- | --- | --- | --- | --- |
| Source identity | Reviewed verification intent | Executed evidence, or explicitly absent | Not assessed until reviewed | Responsible decision/work owner |

Account for the complete planned scope, including negative paths, integration,
supported environments and manual checks. Explain omissions, exclusions and
changes from the strategy. Distinguish requirement/risk coverage from code/branch
measurements; report denominators, thresholds, exclusions and measurement limits
where numerical coverage is used.

## Open findings and residual uncertainty

| Finding or limitation | Impact / affected obligation | Triage and corrective/re-verification work | Authority, deadline and current disposition |
| --- | --- | --- | --- |
| Actual finding ID or explicit absence after assessment | Concrete consequence | Linked records and actual results | Owner; unresolved items remain visible |

Include blocked/error/skipped/cancelled runs, flaky cases, unavailable live/platform
checks and stale evidence. Do not convert these to pass through aggregation. State
whether actual required findings are closed, deferred under an allowed mechanism,
or still blocking. Preserve original results and decisions.

A permitted exception needs its actual scope, human authority, expiry, compensating
checks and evidence under the existing policy. Nonwaivable rules stay nonwaivable;
this assessment cannot authorize an exception or authenticate a referenced approval.

## Exit criteria and return

| Requested criterion | Evidence and independent assessment | State and authorized decision |
| --- | --- | --- |
| Project exit criterion | Actual current evidence, or identified missing work | Open/fulfilled/blocked; decision owner and evidence |

Conclude only for the recorded scope: what is established, what remains unknown,
who must act next and whether the affected gate can proceed. All required results,
review/triage and applicable human decisions remain necessary. A finished run is
not automatically an accepted item, satisfied Definition of Done or released product.

For changed inputs, identify renewed checks and which earlier evidence remains
applicable. Return the result and limitations to the delivery owner/orchestrator
with exact IDs and revisions. Source basis: original prompts informed by T-S03,
T-S07/T-S08 and T-S12 in the
[source register](../../quality/testing-sources.md#reference-register).
