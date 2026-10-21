# Test or verification design

Status: draft; no procedure is approved or executed by this template.
Use the [testing contract](../../quality/testing.md). A stable executable test,
parameterized case or versioned manual procedure may supply the detail; reference
that authority instead of maintaining a conflicting duplicate case catalogue.

## Identity, purpose and inputs

| Field | Value or authoritative reference |
| --- | --- |
| Test/procedure identity and revision | Stable ID; source location, test selector and immutable version |
| Strategy and authorized scope | Parent strategy/delivery and relevant packet |
| Source obligations | Requirement/acceptance, quality scenario, risk and design IDs/revisions |
| Purpose | Observable claim; relevant failure consequence |
| Selection | Verification method, test level/type, design technique and applicability rationale |
| Ownership | Design/implementation owner, executor and independent reviewer |
| Prerequisites | Approved contract, component/build inputs, access and readiness criteria |
| Environment and data | Platforms/dependencies/configuration; fixture identity, origin and safe handling |
| Control and observation | Initial state, setup, controllable inputs and measurable outputs |

## Procedure and decision criteria

| Case / parameter class | Input, action or referenced executable procedure | Expected observation and decision criterion | Source/risk coverage |
| --- | --- | --- | --- |
| Required scenario | Reproducible steps or exact versioned test selector | Specific result, threshold/tolerance and observation point | Source IDs |

Include relevant valid, invalid, boundary and state-transition cases, concurrency,
permissions, timeout and recovery behavior according to actual risk. Identify the
expected behavior for each; executing a command without an oracle is insufficient.
For exploratory work record the charter, scope, timebox, observations and assessment
method rather than pretending every action was scripted in advance.

Record setup/cleanup, isolation and side effects. Identify stop conditions, resource
limits and required recovery. Identify any destructive or privileged action and its
actual authorization; a test definition does not grant access or deployment rights.

## Adequacy, limitations and changes

- Explain why the selected cases expose the material obligation and failure paths.
- State unsupported platforms, mocked boundaries, unavailable observations and
  remaining coverage gaps with an owner and effect on the affected gate.
- For a defect regression, reference the observed defect, failing condition and
  expected repaired behavior; preserve the original reproduction evidence.
- A changed requirement/interface/data assumption triggers impact assessment and
  review of the affected design. Keep prior versions and result bindings intact.

Assign the actual workflow check or manual route in [CI mapping](ci-mapping.md).
Record execution only in a [run](test-run.md) or equivalent tool result.
Source basis: original prompts informed by T-S03/T-S04, T-S07 and T-S12 in the
[source register](../../quality/testing-sources.md#reference-register).
