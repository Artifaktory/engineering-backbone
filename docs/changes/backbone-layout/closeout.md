# Draft refactoring closeout

This delivery creates a first inspectable direct-copy reference layout. It is not
merge-ready: the actual previous trusted validator still rejects the moved source
layout. No product repository, deployment, release or integration was activated.

## Outcome and evidence

- The actual repository now exposes the product, shared-document, native-tool and
  Backbone-tooling locations shown in [README](../../../README.md).
- All 495 baseline files have unique destinations in [the map](mapping.md); 152
  historical or immutable files retain exact bytes. Historical evidence remains
  about its original deliveries, never the copied project's qualification.
- The independent [check record](checks.md) reports 431 passing tests at
  `ee4f7cee7a386edfb5fb43b2763a03596b8eabf1`, all compiler/validator/dependency checks,
  direct-copy regressions and a real prior-main Copier update.
- Both Full reviews examined `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
  [Independent triage](review-triage.md) confirmed three path regressions. The
  repaired implementation is `97e68ecefbd21b0d022514f46520a75a6a025536`.
- [Repair checks](repair-checks.md) passed the exact workflow's 12 affected tests,
  including the new CLI-root regression. The full suite now contains 432 tests;
  a complete 432-test rerun was not executed after these bounded repairs.
- [Behavior Delta](behavior-delta.md) and [security Delta](security-delta.md)
  closed all three findings without confirmed direct regressions. The original
  Full reports and findings remain preserved rather than rewritten as PASS.

The [Task Packet](task-packet.json) maps AC-1 through AC-7 to these observations.
AC-6 is satisfied by honestly exercising and retaining the failed old-layout gate,
not by passing that gate. AC-8 is satisfied by [the published draft PR and recorded remote checks](publication.md).
The packet's head names the repaired implementation, while subsequent commits
contain evidence only. Exact Full and Delta patch digests are in their reports.

## Documentation and requirements impact

The root instructions, contribution guide, adoption instructions, active policy
links and native references now identify the canonical locations. The complete
migration map allows a reviewer to follow every old file to its destination.
Product component READMEs explain where source, tests, dependency manifests,
lockfiles, build configuration, containers and IDE files belong. They do not
introduce fictional product code or select Artifaktory, Tars or Mastra dependencies.
No shared policy invariant, pinned dependency or existing historical fixture
content was changed. Existing legacy consumer paths and update ownership remain.

## Residual risks and safe recovery

The previous trusted-base validator exits 1 with 34 layout/context errors. The
workflow still invokes that base-owned validator; there is no candidate fallback,
projection or bypass. A separately reviewed trust migration is needed before merge
readiness. A draft review outcome is not human approval or release permission.

Docker and Podman are unavailable locally, so a real image build and offline smoke
have not been executed here. Native Windows/OpenCode/model behavior and OS
isolation are also unqualified by these checks. Remote CI results must be read
separately from local results. Copying the reference requires project-specific
facts, task references, dependencies, build commands and CI adoption; copied history
and inactive adapter seeds confer no operational approval.

The change remains on its own unmerged branch. A human can review or close the draft
without changing main or downstream repositories. Subsequent development should
use scoped follow-up commits/PRs and preserve this reviewed history; no force push
or destructive rollback is needed.
