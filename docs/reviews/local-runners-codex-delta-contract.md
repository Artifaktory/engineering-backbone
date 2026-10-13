# Independent scoped Delta: LR-BB-CODEX-001

Date: 2026-10-13. Role: independent read-only trust/governance/test-contract reviewer. Scope: the confirmed Backbone P1 origin/scheduling repair and direct repair regressions, plus changed acceptance/evidence records. Unchanged AO and prior Full scope were not reopened. This report is not human merge/release approval or runtime activation evidence.

## Frozen scope and identity

- Repository: `Artifaktory/engineering-backbone`.
- Trusted migration base: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`.
- Prior reviewed local head: `21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb`, tree `46d6fb10d37fdcd9dbb43f8e1444f6a577e60460`.
- Associated published head: `19fb75b640a470b459119f1654f5e43d3c1aef2b`.
- Repair head: `1d0f055d54b57011d3da200c5e037319c8cca44d`, tree `0b432e942d1508f86d0e1bf952f2625f3e83a8d2`.
- Delta binary-patch SHA256: `d1a5cc1c162dfe1a72235148ed4a62d67118a6aa330afc9de92b749c034b5a32`.
- Manifest: `codex-delta-review-manifest.json` outside the repository.
- Confirmed finding: `LR-BB-CODEX-001` only.

Current head/tree, prior local tree and recomputed Delta digest independently match the manifest, and the tracked worktree matches the frozen repair head. The published GitHub commit object is not installed in this local repository. The parent separately reports verifying its tree through the official GitHub commit API as `46d6fb10d37fdcd9dbb43f8e1444f6a577e60460`, equal to the independently inspected prior local tree. This reviewer did not fetch or change remote state; the published-to-local association is explicitly supplied evidence.

## Conclusion and closure

`LR-BB-CODEX-001` is **RESOLVED in the scoped implementation contract**. There are `NO CONFIRMED IN-SCOPE DELTA FINDINGS`.

Both original quality checks remain scheduled for source pull requests and reject foreign or absent head identity with a nonzero first-step result before checkout/setup. The fix removes the specific migration-induced successful-skip path. It does not establish immutable runner protection: these workflow guards remain candidate-editable, and independent repository access/approval/isolation controls remain required.

No additional repair is requested by this reviewer. The recorded remote Foundation failure remains real and unresolved runtime-qualification evidence under AC5, which stays blocked. Local test success and closure of this P1 do not convert that failure into PASS or authorize activation, merge, release or deployment.

## Repair and regression observations

- `.github/workflows/governance-checks.yml` removes the source-fork job-level skip while retaining the job ID and `Validate governance and compatibility` name. Its existing first Bash step adds a source-repository/PR-event origin refusal before the original mode/event restrictions. The quality caller still uses the original `Foundation checks` name. The job therefore executes the refusal rather than returning a conditionally skipped check.
- `.github/workflows/quality.yml` restores the original `github.event_name == 'pull_request'` scheduling condition for `Trusted base policy`. Its new unconditional first Bash step rejects foreign or missing `PR_HEAD_REPO` before any checkout or setup action. An unavailable self-hosted runner may leave it queued; it cannot produce a successful skipped rejection.
- Both head values enter through `env` and are compared as quoted data in fixed Bash programs. There is no event expression interpolation into `run`, evaluation of head text, dynamic command construction or source-mode authorization bypass. Actual-script cases reject foreign, empty and shell-like head values under both `source_mode` values, while same-source identity passes the origin check.
- Reusable consumer behavior is retained: external consumer PR origins do not enter the source refusal; forged consumer `source_mode: true` remains rejected by the unchanged existing restriction. Source push/manual events and unsupported-event rejection retain their original behavior. Hosted defaults for external consumers and repository-identity-bound local source routing are unchanged.
- Base-to-repair structural comparison of the two changed workflows confirms preserved events, names, permissions, concurrency, runner group/labels, job identities, dependencies/timeouts/strategy, existing checkout references/action pins and all subsequent original step dictionaries. The original governance mode/event payload remains intact following the inserted refusal. No workflow-kit aggregate, trusted base-owned validator, environment filter, compiler, schema, template, dependency or consumer fingerprint is modified by this repair.
- The independently reviewed follow-up plan scopes `tests/test_workflows.py` solely to the positive source fixture. The actual edit supplies a valid same-repository head to that existing fixture without dropping its forged-mode or unsupported-event assertions. New tests inspect scheduling, old names, first-step placement and the actual gate scripts, rather than substituting a model of their verdicts.
- Task/evidence updates distinguish original historical Full/Delta conclusions from the subsequently confirmed P1. AC4 remains pending while the present review chain closes; AC5 explicitly remains blocked. The updated AC2/AC3 local check results are supported by the repaired-source evidence, not the earlier clean review conclusions.

## Evidence identity and honesty

All seven copied plan/quality/sourceproof/final-manifest/remote-runtime files are byte-identical to the independent originals outside the repository. Their final-manifest SHA256 entries also match the copied bytes.

The checker executed source head `a2e9f536f589042425ebc3f248dc0bde8215a7de`. All 166 sourceproof workflow/test/script/template/dependency file SHA256 and Git blob identities independently match the frozen repair head; the relevant tracked source paths have no diff from that checked head. Documentary acceptance updates therefore do not substitute untested source for the checked candidate.

All ten saved quality-log hashes match their recorded SHA256 identities and actual exit/status fields. The complete-suite log contains `Ran 242 tests in 462.887s` and `OK`. The recorded wrapper exit is 0. These are observed saved execution records, not a newly repeated full suite.

The saved remote log hash matches `474e564d398467f49b9a2af43aa1b30576c479d071639da6ef87815e19a4eed7`. It names `pc2-build`/`af-ci-build-v1`, contains `Ran 239 tests in 470.476s` and `FAILED (failures=19)`, with exactly 19 recorded `libpython3.12.so.1.0` loader errors. The associated independent metadata reports child exit127, Foundation failure, and Trusted base policy success at the earlier published head. Documentation correctly treats this as placement/access evidence and failed runtime acceptance, rather than proof of clean isolation or repaired-head remote success.

The documented Python child-certification example uses exactly the unchanged 16-key workflow-kit allowlist. It excludes loader/injection variables and does not widen the filter, alter host loader settings or patch a shared cache. It remains a future runtime prerequisite; it was not executed on the user's selected runner by this reviewer.

## Actual bounded reviewer checks

- Manifest/current head/tree/prior local tree/Delta SHA256 and `git diff --exit-code <repair-head>`: exit0, exact matches.
- `/workspace/scratch/59eed579c382/backbone-venv/bin/python -B -m unittest discover -s tests -p test_local_runners.py -v`: exit0, 8 tests passed. Includes actual first-step gates, retained consumer behavior, source routing and aggregate failure cases.
- The same isolated Python with `-B -m unittest discover -s tests -p test_workflows.py -k source_mode_cannot_bypass_consumer_gate -v`: exit0, 1 affected fixture test passed. The pre-existing Copier missing-answers warning is recorded in the output and is not a failure.
- Read-only sourceproof/log/manifest hash checks, scoped workflow structural comparison and exact allowlist comparison: exit0.
- `git diff --check 21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb 1d0f055d54b57011d3da200c5e037319c8cca44d`: exit0.
- Inspected the complete-suite saved conclusion; the suite was not rerun. Source/trusted validators, compiled tooling/workflow-kit and actionlint successes are independently saved quality-owner records. Shellcheck was not executed or claimed.

## Coverage and remaining limits

Covered the confirmed P1 gate/scheduling repair, first-action ordering, unchanged check names and trust contracts, head-value treatment, caller-mode boundaries, source/non-PR/consumer compatibility, affected fixture, repaired-source provenance, immutable saved check records and acceptance/report updates. Earlier unchanged review scope and AO code were not reopened.

Not exercised here: GitHub scheduling/conclusions at the repaired head; actual branch protection and repository-wide approval/access controls; all build-group members or clean runner isolation; a loader-compatible remote child interpreter and successful remote Foundation suite; remote Codex Delta follow-up. The earlier decoded log is saved supplied remote evidence, not a new service observation. No settings, host/shared-cache changes, environment-filter changes, remote actions, source edits, commits, releases, deployment or nested agents were performed. The only write is this report outside the repository.
