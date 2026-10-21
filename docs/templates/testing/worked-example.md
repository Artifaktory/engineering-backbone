# Worked example: verify an exported collection

**Fictional teaching example, entirely unexecuted.** No product, person, project,
requirement or design below has been approved. `EX-T-SOURCE-v1` denotes an
illustrative document revision, not a real commit. No build, test or pipeline has
run; no actual PASS, accepted finding or release permission exists.

Use the [testing contract](../../quality/testing.md) and
[CI/CD contract](../../quality/ci-cd.md) to replace these drafts with actual project
sources, owners, revisions and observations.

## 1. Carry the sources into a proportionate strategy

The draft goal `EX-T-GOAL-1` is to export a selected local collection and let its
owner inspect the result. Language, UI, storage and packaging are undecided.

| Draft input | Obligation / design claim | Open source decision |
| --- | --- | --- |
| `EX-T-REQ-1` | A valid export contains exactly the authorized selected entries and preserves their specified values. | Product owner unassigned; supported value/encoding contract unresolved |
| `EX-T-REQ-2` | Invalid or unauthorized selection produces a defined rejection and does not overwrite an existing output. | Product/security owners unassigned; access and overwrite policy draft |
| `EX-T-REQ-3` | A user can open the completed output using the declared supported reader. | Supported reader/version and output format not selected |
| `EX-T-ADR-1` | An export component produces the format; an entrypoint supplies selection and authorization; a reader consumes the output. | Proposed architecture; interfaces not accepted |

Draft plan `EX-T-PLAN-1` maps these sources to the strategy below. An authorized
investigation could resolve format/access choices within its own packet. Product
implementation and verification cannot be dispatched from this incomplete example.

## 2. Select tests and define observable outcomes

| Proposed test / method | Source and risk | Planned procedure and expectation | Boundary / readiness |
| --- | --- | --- | --- |
| `EX-T-CASE-1` component test | REQ-1; missing/changed values | Generate allowed boundary values and compare parsed export with the selected input under the accepted format contract | Format/data contract unresolved |
| `EX-T-CASE-2` negative integration test | REQ-2; unauthorized read or destructive overwrite | Use actual authorization boundary and an existing output; exercise rejected selection and compare original bytes/state afterward | Identity/access fixture and output behavior unresolved |
| `EX-T-CASE-3` integration/acceptance | REQ-1/3; individually correct components disagree | Export through the real entrypoint, open with the supported reader, compare selected values and identity of the actual produced output | Reader and representative environment unresolved |
| `EX-T-CHECK-4` static review | ADR-1 and material risks | Independently inspect interface/error/data-handling design against accepted source decisions | Draft review may identify gaps; no approval implied |

Automated test code may own detailed cases and selectors. The strategy links these
identities instead of reproducing every input in a manual catalogue. Expected
outcomes are planned oracles, not observed results. Performance and large data-volume
coverage need an applicability decision once actual capacity requirements exist;
this example invents no load threshold or exemption.

A second, smaller change could be documentation-only: `EX-T-DOC-1` would require
instructions to agree with an accepted command interface and all local links to
resolve. Review plus document checks could supply the relevant evidence. It would
need no invented deployment or runtime performance test. Its sources, applicability
and actual outcomes would still have to be recorded.

## 3. Map the proposed checks to execution

| Intended obligation | Proposed route | Required actual evidence | Current state |
| --- | --- | --- | --- |
| Component and negative/integration behavior | Project-defined approved check IDs in kit phase `pr`, for PR and configured main push | Actual product/test revisions, environment, command, expected/observed comparison and report | No binding, command or run exists |
| Larger supported-reader matrix | Separately reviewed project procedure/workflow; not a generic maintenance behavior-test route | Each exercised reader/platform configuration and its limits | Not implemented; applicability unresolved |
| Packaged release, if selected later | Existing release-profile integrity/provenance/signature obligations; conditional SBOM rules still apply | Exact produced artifact and actual verification | No release profile selected or activated |

The document chooses no CI provider or runner. A real project must record its
hosting/access/evidence policy, including local-runner or no-upload constraints
where required. Optional profile or workflow presence does not activate it.

## 4. Preserve outcome meanings without fabricating a run

The run record is currently **not run; outcome not assessed; acceptance pending**.
The following are conditional illustrations of how a future observation would be
classified, not events that happened:

| Possible future observation | Meaning and required treatment |
| --- | --- |
| Actual export drops a required value | Behavioral failure; preserve evidence, triage the defect and verify a confirmed repair with regression coverage. |
| Test parser crashes before comparison | Test/tool error; no usable behavioral conclusion; diagnose and retain the failed attempt. |
| Required supported reader is unavailable | Blocked prerequisite; retain the missing coverage and its gate consequence. |
| CI matrix row is skipped or its job queued | Required behavior remains unexecuted; neither condition supplies PASS. |
| Component fixture agrees with expected bytes | Evidence limited to that fixture if it is actually run; real authorization/reader acceptance still needs its own evidence. |

The existing requirement JSON would retain `not_run` until mapped evidence supports
another permitted state. Packet acceptance remains `pending`; a quality CSV row may
record planned coverage using its existing supported status. These prose labels add
no new schema fields or enums. An exception cannot turn an absent run into PASS.

## 5. Assess closure and changed inputs

Completion is currently blocked by unresolved source decisions, missing actual
assignments/inputs, absent implementation and unexecuted checks. There is no
independent acceptance or release decision. A later completion report must account
for every scoped obligation, actual runs, open findings and residual limitations.

If a later accepted `EX-T-SOURCE-v2` changes number encoding, reassess REQ-1/3,
ADR-1, component boundary cases, reader interaction, documentation and release
compatibility. Identify which earlier results, if any later exist, still apply;
keep their original revisions and observations. Pause affected work, update its
source/packet bindings, run the required v2 checks and return their actual results
to the delivery owner. A historical v1 success would not establish v2 behavior.
