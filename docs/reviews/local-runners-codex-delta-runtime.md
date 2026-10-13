# Scoped independent runtime Delta: Backbone LR-BB-CODEX-001

Date: 2026-10-13. Role: independent read-only runtime/compatibility reviewer. Scope is the triage-confirmed remote P1 `LR-BB-CODEX-001`, its repair, directly introduced regressions and the associated evidence boundaries. This is not a second Full review, a reopening of unchanged AO work, human approval, publication authorization or runtime activation clearance.

## Frozen snapshot

| Item | Independently observed value |
| --- | --- |
| Repository | `Artifaktory/engineering-backbone` |
| Trusted migration base | `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13` |
| Prior reviewed local head | `21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb` |
| Prior local tree | `46d6fb10d37fdcd9dbb43f8e1444f6a577e60460` |
| Repaired head | `1d0f055d54b57011d3da200c5e037319c8cca44d` |
| Repaired tree | `0b432e942d1508f86d0e1bf952f2625f3e83a8d2` |
| `git diff --binary PRIOR..HEAD` SHA256 | `d1a5cc1c162dfe1a72235148ed4a62d67118a6aa330afc9de92b749c034b5a32` |

The repaired head/tree/digest exactly match `codex-delta-review-manifest.json`; the tracked checkout was clean. The associated prior published head is `19fb75b640a470b459119f1654f5e43d3c1aef2b`. That Git object is absent locally: an attempted local tree lookup exited128 and was not represented as successful. The parent independently retrieved its GitHub git-commit endpoint and supplied the exact matching tree above. Thus the portable mapping is supplied official metadata, while the local snapshot/delta verification is independent. No remote mutation or fetch was performed by this reviewer.

Applicable root/core/contribution instructions remain unchanged from the earlier reviews. Read the confirmed remote triage, independently reviewed scoped plan follow-up, complete repair diff, both actual first-step scripts, added/adjusted tests and documentary quality/runtime records.

## Result

**LR-BB-CODEX-001 is RESOLVED in the scoped implementation. NO CONFIRMED IN-SCOPE DELTA FINDINGS.** This closure establishes the repaired scheduling and explicit rejection behavior, not successful remote qualification of the selected Python runtime or hosting controls.

### Finding closure and direct regression reasoning

The reusable `Validate governance and compatibility` job no longer has the migration-added source-fork job-level skip. The source `Foundation checks` caller remains scheduled under its original name. `Trusted base policy` restores `github.event_name == 'pull_request'`, so a source PR no longer skips that original check because of its head repository.

Both paths now inspect head repository data in their fixed first Bash step before any checkout/setup action. Foreign, empty or absent source-PR head identity yields a nonzero result. A missing runner leaves a check pending rather than turning refusal into a successful skip. Subsequent checkouts/setup steps retain ordinary success gating; no `always()` candidate checkout or `continue-on-error` converts the rejection into execution/success.

The reusable first step restricts the new refusal to source repository identity plus `pull_request`, independently of caller-controlled source_mode. Same-source PRs, source push/manual events and valid external-consumer PR/fork requests preserve their previous script outcomes. Forged external source_mode and unsupported events still fail through their original checks. Trusted-policy remains PR-only.

`PR_HEAD_REPO` enters through the step environment, not direct interpolation into the shell program. Quoted string comparisons keep command substitutions, newline text, spacing and other hostile head strings as data. No eval or constructed command is added. Repository controls and isolation remain separate because the workflow itself is candidate-editable; this repair does not claim an immutable untrusted-code boundary.

Parsed prior/repaired workflow comparisons verified that all original names, events, permissions, routing groups/labels, timeouts, action refs, trusted/candidate checkout refs, dependencies and subsequent command payloads remain unchanged outside the planned scheduling and first-origin-check additions. The source-positive existing workflow fixture adds only the actual same-repository head value; its existing adversarial assertions remain intact. Consumer defaults and unchanged workflow-kit aggregates were not reopened or modified.

## Independently executed bounded checks

| Check | Actual result |
| --- | --- |
| Local head/tree/delta digest and tracked status | Match; clean |
| Actual first scripts: both jobs, both source modes, exact/foreign/empty/unset/case/spacing/newline/command-like head strings | 30 origin cases PASS; only exact source identity passes source PR gates |
| Actual Foundation script compared with its prior script for all unchanged source/consumer modes, allowed and unsupported events | 56 equivalence cases PASS; exit/stdout/stderr unchanged |
| Event-derived command-substitution sentinel | Never created; hostile text remained data |
| Parsed scheduling/first-action/ordinary-success gating checks | PASS; original quality checks schedule and origin gates precede actions |
| All checked workflow/test/script/template/dependency bytes from independent quality sourceproof | 166 files match frozen checked blobs and SHA256 values at final repaired head; zero mismatches |
| Five copied immutable quality/runtime evidence files versus their manifest | All exact matches |
| Decoded remote Foundation log versus recorded SHA256 | Exact match; actual runner/group, prior checkout head, 239-test result, 19 loader errors and failure verified |
| Protected workflow-kit runner and requirement manifests versus trusted migration base | Byte-identical; no loader filter or dependency relaxation |

The 86 actual-script cases were run in read-only subprocesses with controlled environment values and a disposable sentinel outside source. No broad full suite or native/runtime job was rerun by this reviewer.

## Quality provenance and honest runtime limits

The separate quality role checked source commit `a2e9f536f589042425ebc3f248dc0bde8215a7de`/tree `b002b44cbcb5ebb16728635f7694dd02154fe9a6`. All 166 relevant checked source files still match at this final documentary head, allowing the recorded results to bind to the repaired implementation rather than assuming equivalence from commit names alone. Supplied quality evidence records eight focused tests, the changed positive fixture, source/trusted validators, both compilers, actionlint without shellcheck and whitespace checks passing; the complete suite passed 242 tests in 462.887s. These full checks were not independently rerun here.

All durable evidence copies match the quality manifest, including local check report/JSON, sourceproof and remote runtime report/JSON. Their PASS means local repaired-source checks. They explicitly keep the remote Foundation verdict FAILED and AC5 blocked. Historical earlier review/check conclusions remain historical and cannot close this later P1 or certify a later runner environment.

Independently read the preserved remote Foundation log for run `38427484521`, job `115400567007`, SHA256 `474e564d398467f49b9a2af43aa1b30576c479d071639da6ef87815e19a4eed7`. It names `pc2-build`/`af-ci-build-v1`, checks out the earlier published head, runs 239 tests in 470.476s and ends `FAILED (failures=19)`. Exactly 19 loader-error records identify `libpython3.12.so.1.0`; this is genuine placement/access and failed child execution evidence, not a green Foundation result. Trusted-policy success is supplied in the separate runtime metadata and does not waive the failed suite.

The newly documented Python certification environment matches the unchanged workflow-kit allowlist. Loader injection variables stay excluded. The repair does not patch the runner cache, host linker configuration, scripts, templates, assertions, selected commands or filtering to obtain green tests. It requires the exact selected interpreter to start under that minimal child environment, followed by the actual full suite on a certified runner. AC5/task status remain blocked; AC4 remains pending until review/follow-up completion. No claim is made that access on one observed build machine certifies every group member or clean isolation.

## Coverage and unreviewed areas

Covered the P1's concrete skip-to-nonblocking path, restored scheduling, both actual fixed first scripts, consumer/non-PR equivalence, hostile/missing values, subsequent checkout gating, scoped positive-fixture change, immutable checked-source correspondence, documentary acceptance honesty and the preserved remote-loader failure classification. No new confirmed direct repair regression was found.

Not exercised or approved: actual foreign-source PR scheduling/conclusion on GitHub at the repaired head; live required-check/approval settings; repository-wide runner isolation and every group member; intrinsic loader compatibility of the intended self-hosted interpreter; successful repaired-head remote Foundation execution; remote advisory Codex Delta result; human merge/release authority. The parent-supplied published/local tree mapping was not fetched independently. Unchanged AO/native/container/consumer implementation areas and earlier Full catalogs were intentionally not reopened.

Keep draft/runtime stops in force. A verified changed runtime is appropriate input for a later bounded remote qualification, but this Delta neither authorizes host/settings mutations nor converts the earlier remote failure into PASS. No source edits, commits, remote writes, dependency installs or nested agents were performed.
