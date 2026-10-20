# BB-LAYOUT-012 deterministic correction checks

Quality-checker session: `layout_quality`, separate from implementation and review.
Date: 2026-10-20. This report records actual local checks and their limits; it does
not constitute native Copilot qualification, independent semantic review, human
approval or merge readiness.

## Tested snapshot

- Corrective base: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.
- Original and observed live PR base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Tested head: `dbe05e14a255488e3416465971ece755fb04aba3`.
- Tested tree: `1801cbc5defdf82a4c37f5ead84eea2e8ab1df4b`.
- Corrective binary patch SHA256: `8957f9cea5e698daa212cdbd08c555dbdd6ea0e7222b52c1dea7e19038575ed0`.

The worktree was clean before checks. All **546** source-file hashes matched before
and after the affected module run; no source input changed during execution.
The quality checker edited no source or tests, and added only this report afterward.

## Executed checks

Commands ran from the repository root using the existing isolated Python 3.12.14
environment and unchanged locked dependencies. Each exit code was captured
individually. `HEAD` in the table means the exact tested head above, not a future
publication commit.

| Command | Exit | Actual result |
| --- | ---: | --- |
| `PYTHONPATH=.engineering-backbone python -m unittest tst.test_copilot_distribution tst.test_copilot_validation tst.test_copilot_workflow_guard -v` | 0 | **41 tests in 68.584 seconds, OK.** |
| `python .engineering-backbone/src/validate.py` | 0 | Structural PASS; no supplied trusted-base comparison. |
| `python .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | Compiled navigation/technology authority matches. |
| `python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | Compiled quality catalog and entrypoints match. |
| `python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | Compiled workflow entrypoints match. |
| `python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | Reviewed legacy rendered toolchain fingerprint matches. |
| `python .engineering-backbone/src/check_source_dependencies.py` | 0 | Tracked inputs, all 26 installed locked versions and dependency consistency. |
| `git diff --check` | 0 | No unstaged whitespace errors. |
| `git diff --cached --check` | 0 | No staged whitespace errors. |
| `git diff --check c50108773ba3195bf0f7503e5dffb2d7bfc78cd3 HEAD` | 0 | Committed corrective diff is clean. |
| `git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f HEAD` | 0 | Complete committed PR diff is clean. |
| `git diff --check 212608aa50ee517b3dd3107a9480da997222fd4f c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` | 2 | Pre-fix failure reproduced: `publication.md:56: new blank line at EOF`. |

The three affected modules retain positive and adversarial adapter/legacy checks.
The new slash-aware glob regression proves that the prior selector misses nested
component/tooling Markdown, that the corrected selector includes root and nested
Markdown plus JSON under `docs/`, and that unrelated Python source is excluded.
Source/legacy parity continues to assert the legacy docs selector explicitly and
compare instruction bodies and other metadata. This checks the declared selector
contract, not loading in an actual Copilot client.

An additional bounded copy check exercises the new optional-component branch:
copy the frozen repository to a temporary product, remove only `apps/frontend`,
and run `tst.test_copilot_distribution.CopilotDistributionTests.test_source_docs_rule_covers_nested_markdown_and_docs_data`
with the copied bundle on `PYTHONPATH`. **Exit 0: one test in 0.552 seconds, OK.**
The removed component remained absent afterward. This is a repeat of the same
regression in a pruned copy, not a new complete test-suite run.

Compiler toolchain fingerprint remained
`402e3fa62d99afda07bd2929afef9237e28835b3a3a349e6ca194d01cb58343f`.
Affected-suite log SHA256:
`0c65baea895b61bf868118cc154ae1db89b0a3c3c4cc450b2dc24cb63500fccc`.
Individual command-result record SHA256:
`a0b1f96c222584f481e81364e6e2d89b1931d4f330fa147358e396c7a7b1a3cc`.
Pruned-copy test log SHA256:
`66e0209d0595ee38a45056900b4e4e64588934488220170ccc34a19369efa20e`.
Raw logs remain ignored run artifacts.

## Publication boundary and retained limitations

The quality checker independently reread PR 18 metadata during these checks:
it remained open and draft, base branch `main` at
`212608aa50ee517b3dd3107a9480da997222fd4f`, remote head
`c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`. Thus the complete PR comparison above
used the live base observed at check time; the tested corrective head had not yet
been published.

**These committed-diff results bind only `dbe05e14a255488e3416465971ece755fb04aba3`.**
This report and later review/publication evidence are not yet part of that tested
commit. After the final evidence commit, the coordinator must resolve the exact
final HEAD and current live PR base and rerun both committed-diff checks, in
addition to worktree/staged checks. Any later commit invalidates that final
publication result until the checks run again. No evidence-file exemption applies.

There are now **433** test methods present. No full local 433-test run was
performed for this bounded selector/documentation correction. The earlier remote
432-test, Docker and native Linux/Windows results in
[ci-observations.md](ci-observations.md) belong to their recorded old head; they are
not current-head PASS evidence. Native Copilot behavior, model reasoning and
product qualification were not exercised. Current-head remote checks must be
read after publication.

The disclosed legacy trusted-base incompatibility remains a failed merge gate.
This correction changes no validator, schema, compiled guard, dependency pin,
legacy template or workflow gate, and these candidate-side checks do not replace
trusted-base validation. Its separate compatibility follow-up needs its own
reviewed implementation and human adoption; no bypass or merge is authorized here.
