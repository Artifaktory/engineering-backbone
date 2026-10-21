# Project CI/CD and evidence mapping

Status: draft mapping; no workflow, profile, runner or deployment is activated.
Use the [CI/CD contract](../../quality/ci-cd.md), [testing contract](../../quality/testing.md)
and the project's existing command/check authority.

## Authority and execution boundaries

Record mapping ID/revision, delivery/test strategy references, actual workflow
configuration source/pin, owners and selected profiles/capabilities. Identify
editable versus derived representations. Existing adopted obligations remain
binding; a mapping cannot make required checks optional or replace approved commands.

| Obligation / risk | Actual check ID or manual procedure | Trigger / target revision | Supported execution route / phase | Required evidence and gate | Owner |
| --- | --- | --- | --- | --- | --- |
| Project source ID | Declared approved binding | Actual event, inputs and commit/build | Existing implementation or explicit gap | Result subject, location and decision rule | Responsible owner |

Reference command definitions rather than creating a second executable authority.
For each row record environment/platform, data and prerequisites, timeout/budget,
minimum permissions/secrets, untrusted-input boundary, isolation and failure owner.
Identify access-controlled evidence storage, redaction, retention and availability
for reviewers. Apply this project's runner and upload constraints; defaults from
another repository do not authorize hosting or evidence transfer.

## Match events to actual supported implementation

| Intended occasion | Current Backbone workflow-kit support | Project mapping to complete |
| --- | --- | --- |
| PR and configured target-branch push | `pr` phase for applicable declared quality/security checks | Actual event/ref semantics, affected scope and required check IDs |
| Periodic/manual maintenance | `maintenance` for selected dependency/container checks | Schedule, approved configuration and failure response |
| General large periodic behavior or platform suites | No general maintenance test/matrix route in this kit | Separately reviewed project workflow/manual procedure or explicit gap |
| Release | `release` integrity, provenance and signature; SBOM when selected dependencies/container require it | Actual produced artifact, verification and applicable human release gate |
| General release behavior regression | Not a generic `release` test kind in this kit | Reviewed project preflight/extension and actual evidence |
| Deployment | `deploy` smoke, rollback and monitoring for adopted deployment capability | Reviewed environment, permissions, artifact and human decision |

Events and kit phases are different dimensions. Do not add phase names such as
`nightly` or `post_merge` to the closed workflow schema. Preserve existing profile
requirements, including release signature and conditional SBOM checks. Optional
release/deploy examples remain inert until their real project integration is reviewed.

## Gate and delivered-subject assessment

- Define expected mandatory jobs/results and required manual evidence. Missing,
  queued, cancelled, skipped or failed required checks do not satisfy the gate.
- Verify that evidence applies to the actual integration/release/deployment subject;
  link source revision, build inputs and delivered artifact identity where relevant.
- Establish appropriate trust/permission separation for untrusted changes and live
  operations. Pipeline/permission changes need relevant negative checks and independent
  review; a YAML parse or runner label alone does not establish isolation or enforcement.
- Record non-applicability through the adopted mechanism, never as a fictional PASS.
  An allowed exception changes a bounded decision, not the historical result.
- Identify required repository/environment controls and observed readback separately
  from checked-in configuration; no template supplies authenticated approval.

Source basis: original mapping informed by T-S02/T-S03 and T-S09/T-S10/T-S11 in the
[source register](../../quality/testing-sources.md#reference-register). Tools,
workflow file count and topology remain project choices within adopted controls.
