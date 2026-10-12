# Codex policy ownership and compatibility Delta

This result covers BB-CX-07-DELTA-02 and BB-CX-08/09 confirmed in
[follow-up triage](codex-followup-triage.md). The last two came from Codex review
`5488022625` of published `abb280ca0334264ddf1d8fc6b67ce5b9bfea203e`.
The [task packet](../../plans/codex-findings-task.json) authorizes scoped repair,
independent Delta review and publication on PR 1. Earlier results remain in
[the first repair](codex-result.md) and [the follow-up](codex-followup-result.md).

## Frozen subject

| Subject | Local commit | Git tree |
| --- | --- | --- |
| Previous snapshot, identical to published `abb280c` | `dc1459fe44499e2f72b9cedde74884cd5a17eeb9` | `2727bd2a2c0f7a10bca749165f29a9a50021343b` |
| Final implementation | `cf042a4e424d933421501a6d6196af9d0adfc71c` | `ad4f4dd090debddae16ba795514acfb163ca72ca` |

Patch SHA256 from `git diff --binary --full-index BASE HEAD`:
`fef33d5765afe7d92ba4db5dc7679d846fd77bbf694267d7ebd83a4fc0585576`.
Remote commits may differ in metadata; publication must preserve reviewed trees.
This subsequent evidence/packet update changes no implementation.

## Independent results

Separate read-only reviewers `codex_delta_correctness` and `codex_delta_security`
confirmed all three repairs resolved, with no confirmed new direct regression.
Neither authored these repairs. Both verified the frozen identities and clean
tracked worktree before and after review. Scope was the three corrections and
their direct regressions; unchanged foundation areas were not re-reviewed.

| ID | Verified result |
| --- | --- |
| BB-CX-07-DELTA-02 P1 | Both canonical policy files are regular in each snapshot before dependencies or validators execute. The pinned workflow rejects first-stage and promoted-base aliases with current and approved historical tooling; plain stronger policy passes and removal of its custom invariant fails. Current CLI also rejects policy and directory aliases. |
| BB-CX-08 P1 | Committed historical source fixtures reconstruct real Copier inputs and preserve all three exact approved tooling identities. Actual generation and upgrade pass in a clean single-commit clone with all original tree objects absent. Historical vulnerable code is explicitly test input, never current tooling authority. |
| BB-CX-09 P2 | Exactly eight attested paths unset inherited filters and working-tree encoding. Real checkouts preserve their bytes while application transformations and inherited diff drivers remain active. |

Both reviewers independently compared **121 reconstructed historical input files**
against actual original Git trees and blob IDs: 40 bootstrap, 40 pre-attestation,
41 attested-review. All match. Original source provenance and rendered identities
are recorded in [the fixture README](../../tests/fixtures/historical/README.md).

## Checks actually executed

- Root integration: **93 tests**, 67.605 seconds, exit 0: 50 validator, 13 Copier,
  28 workflow/compiler/compatibility and two attribute tests.
- Correctness reviewer: **34 focused tests**, 27.938 seconds, exit 0, covering
  workflow, attributes and four policy-ownership/stronger-policy cases.
- Security reviewer: **11 focused tests**, exit 0, plus independent instrumented
  current/historical two-stage alias and strict-policy control probes.
- Current and preceding published source validators, explicit trusted-base
  comparison, fingerprint compiler, Actionlint 1.7.12 and frozen-range whitespace
  checks: exit 0. Dependency and Action pins remain unchanged.

Current actual rendered tooling SHA256:
`5bca19e704f2e6ca5744cfccb10e52b862dc7b9d4c18ed5f5cb3a6db8aadab4a`.
The previous `ef266...` identity joins the two already reviewed historical entries;
its actual rendered fixture is checked independently against the workflow authority.

These are observed local/model-session results. Publication, GitHub-hosted CI and
final provider re-review are verified separately on PR 1 after publication. Human
merge/release approval, external protection settings and client discovery remain
separate operational controls. No downstream write, merge or release was performed.
