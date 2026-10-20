# BB-ARCH-015 check-failure triage

- Triage owner: `/root/architecture_check_triage`, separate read-only repository session.
- Date: 2026-10-20.
- Actual base: `ae317bf30576914d4ed53856be4ae496c6ed64b3`.
- Failed frozen head: `1dbd1d68a7a23b8b38f532ed7a9dff8488642a57`.
- Base-to-head binary patch SHA-256: `2bf0734cc6d4a719f21329a2086232440ed03aba8ea2949066c10adf9acb2a2a`.
- Input: the independent quality report originally returned as
  `/tmp/backbone-architecture-failed-checks.md`, plus the actual complete-suite log
  and unchanged historical-consumer fixture implementation.
- Quality report SHA-256: `f02d5b2cc9f9b5ef8ae1ad3317e6a17a3d2f86cba4b82bda9dd0b1cd624affea`.
- Phase: pre-Full deterministic-check failure. No formal Full round has started.

## Decision

`ARCH-CHECK-01` is **CONFIRMED**, severity **P2**, category downstream compatibility,
high confidence. The five failure events have one common cause. There are no
rejected findings or unresolved human decisions in this triage. Author repair of
this confirmed defect may proceed within the approved plan and Task Packet.
The failed head is not qualified for Full review or a passing delivery claim.
The confirmed disposition and permitted narrow repair were sent to the root before
author edits; this durable report was finalized after that message. Root subsequently
reported starting the two-file repair and focused checks in its separate worktree.
Those later checks are not results of this triage session.

## Evidence and causation

The independent checker ran all 465 tests: `FAILED (failures=5)` after 617.400
seconds, process exit 1. Triage read the actual failure output at the frozen head.
All five events report the same missing-link diagnostic:

```text
ERROR: .engineering-backbone/quality-policy.md: broken local Markdown link architecture.md
FAIL: 1 structural validation error(s).
```

`docs/quality/policy.md:94` adds an unconditional Markdown link to the architecture
contract. The changed legacy `quality-policy.md.jinja` rewrites that link to the
installed basename `architecture.md`. This works in a complete fresh installation,
but it adds a new file dependency to the independently adopted optional quality
package.

The unchanged `QualityWorkflowTests.setUp` at lines 73–84 deliberately adds only
the optional quality package and declarations to a historical consumer. It retains
the historical core, validator, schemas and dependency manifests. That supported
partial-adoption route has not adopted the new core or architecture kit. The old
validator correctly rejects the dangling Markdown link before the intended current
quality guard can be exercised. This is a defect introduced by the new link, not
an error in the existing fixture or a reason to weaken its assertions.

Four unchanged test methods produce the five events:

| Method in `tst.test_quality_workflows.QualityWorkflowTests` | Failure events |
| --- | ---: |
| `test_valid_inactive_package_passes_without_executing_candidate_guard` | 1 |
| `test_current_workflow_rejects_null_and_malformed_profile_old_validator_accepts` | 2: null and malformed JSON |
| `test_current_workflow_rejects_consumer_catalog_poisoning_old_validator_accepts` | 1 |
| `test_first_activation_cannot_manufacture_a_reviewed_quality_seed` | 1 |

The defect violates AC-5 consumer compatibility and AC-6 required checks. It blocks
a valid inactive quality-only adoption and obscures the intended distinction between
an old validator's blind spot and the current workflow-owned quality authority.
The source and new full-copy tests passing does not establish this partial route.

## Confirmed repair boundary

Use the proposed policy wording, or equivalent meaning:

> For architecture-specific obligations, follow the architecture contract referenced
> by the project's adopted canonical core. Updating the optional quality package
> alone does not adopt a newer core policy.

Keep this reference as prose rather than an unconditional local Markdown link in
the independently distributed quality policy. Preserve the statement that document
rule IDs do not change quality catalog/schema authority or install automatic checks.
Revert the now-unneeded legacy quality-policy wrapper transformation to its canonical
include. Both paths are already in the approved Task Packet scope.

The new canonical core's mandatory `(architecture.md)` link must remain. Complete
new source/direct-copy and legacy installations still supply the contract and kit;
missing required contract/template files must still fail their link checks. The
repair preserves the boundary between adopting a new core and updating an optional
package; it does not make the new core's architecture obligations optional.

Do not change the historical fixtures, assertions, package selection, old tooling,
quality guard, catalogs, schemas, runtime, workflow or permissions. Do not add the
architecture package to the partial-upgrade fixture merely to bypass the failure.
No plan extension or new requirement is needed: this is a narrow correction within
the approved documentation/distribution compatibility work. Count it as a repair
iteration within the existing six-iteration budget.

## Required verification after changed input

1. Run all tests in `tst.test_quality_workflows.QualityWorkflowTests` unchanged.
   These must again permit the valid inactive package, retain old-validator control
   results, and reject poisoned/malformed/manufactured state at the intended quality
   boundary without executing candidate guard code.
2. Run `tst.test_architecture_documents.ArchitectureDocumentTests` unchanged to
   preserve full copy/update parity, project-owned records/native instructions and
   missing required guide/template rejection in both layouts.
3. On the new frozen repaired head run the candidate and actual ae317bf trusted-base
   validators, the declared generated-artifact/source checks, committed-patch check
   and the required full unittest suite. Preserve this failed report rather than
   replacing it with a later PASS. A rerun is justified by the changed link input.
4. Only after required checks pass may the two independent Full reviewers assess the
   repaired immutable base/head/patch. Full budget remains zero of two at this point;
   this triage is not a Full review or a Delta approval. Subsequent review findings
   still require separate triage before repair.

Example focused command from `.engineering-backbone/` with the approved interpreter:

```sh
/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest tst.test_quality_workflows.QualityWorkflowTests tst.test_architecture_documents.ArchitectureDocumentTests -v
```

## Actual triage actions and limits

Read AGENTS, core, CONTRIBUTING, the approved plan/Task Packet, the changed policy
and wrapper diff, historical-consumer setup/tests, actual full-suite failure output
and the independent quality report. Reconfirmed HEAD and the binary patch digest.
`git status --short` was empty in the frozen worktree. No repository file was edited;
no repair, test rerun, publication or merge was performed. This report evaluates the
observed failure and repair scope; it does not claim that an unexecuted repair works.
