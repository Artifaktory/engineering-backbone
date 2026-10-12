# Codex review triage: bootstrap PR 1

The task owner requested triage, repairs of confirmed findings, independent Delta
review of those repairs and direct regressions, and an update/re-review on the same
PR on 2026-10-12. The active packet is
[codex-findings-task.json](../../plans/codex-findings-task.json).

## Reviewed baseline

- Provider review: `5487154028` on published commit
  `6982e4a53185b5fcba48b17db10a59a3eaca83ee`.
- Local repair base: `d568bf820ab9d49a9bff34edb2cab32755cfca3a`.
- Both have Git tree `da5e4b16db198a583ca252f109d33778de0a3f78`.
- PR base remains `main`; repairs are limited to the four findings and their
  necessary tests/documentation. There is no downstream rollout or merge authority.

## Triage before repairs

Separate workflow and validator investigators reproduced the findings on temporary
fixtures before implementation. All four are confirmed; no finding was rejected.

| ID | Severity | Provider thread | Observation | Required repair |
| --- | --- | --- | --- | --- |
| BB-CX-01 | P1 | [4245198976](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245198976) | The existing consumer commands exit 0 after replacing the candidate validator with a no-op, emptying its lock and weakening the human-merge invariant. | Execute only the previously trusted consumer validator and dependency manifest against the candidate with trusted-base comparison. Fail closed if the base bundle is absent. |
| BB-CX-02 | P2 | [4245198981](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245198981) | On a clean checkout with committed trailing whitespace, plain `git diff --check` exits 0 while explicit base/head inspection exits 2. | Inspect the committed event-specific patch; cover PR, push and manual/root cases. |
| BB-CX-03 | P2 | [4245198990](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245198990) | Ignored root `artifacts/` transcripts with captured conflict markers and missing links produce false source errors. | Exclude that designated root evidence directory while retaining managed and nested governed-path checks. |
| BB-CX-04 | P2 | [4245198996](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245198996) | Actual Copier generation and consumer validation accept `feature/.hidden` and `release.lock/next`; Git rejects both with exit 128. | Reject invalid branch components before rendering, and validate project/task metadata consistently with meaningful downstream-negative tests. |

## Bootstrap and review scope

The P1 repair restores the already documented trusted-base boundary. First adoption
has no previous consumer validator, so it cannot receive a trusted CI PASS from a
candidate-owned validator. Seed the reviewed bundle with the caller inactive,
perform explicit local/bootstrap review and human merge, then activate the pinned
caller in a separate reviewed project PR. No permissive bootstrap switch or new
private-source credential is added.

The original Full review is retained. The next independent review covers these
finding IDs, the repair diff and directly introduced regressions; it does not
repeat the entire bootstrap review. Repair completion and actual validation results
will be recorded separately after execution.

## First Delta round: remaining dispatch bypass

Both independent reviewers inspected local repair commit
`91cae8957fd84dcaa96e97f6d88303d79caba03e`, tree
`f2ce5c09a6b5ce6750b87601cc54e91f6fc108d4`, with repair patch SHA256
`0703de7120c017d522a72927b6efb6d3df0ac1ab8cb362a21331cb789733caff`.
The correctness reviewer reproduced 66 passing tests and found no confirmed
regression. The security reviewer reproduced an additional event-specific bypass;
the first repair snapshot is therefore not accepted as final.

**BB-CX-01-DELTA-01 (P1), confirmed:** consumer manual dispatch selected
`github.sha` for the trusted checkout. An unapproved selected PR snapshot could
therefore become both candidate and trusted tooling. The actual workflow shell
returned 0, executed its no-op validator and printed a forged PASS despite a
weakened human-merge invariant. Using the real prior reviewed bundle rejected that
candidate with exit 1 and did not execute its validator. Instructions asking the
operator to select an approved snapshot do not enforce this boundary.

The scoped follow-up uses the repository's default branch as independently selected
consumer dispatch tooling, never the dispatched candidate. PR base/push-before
selection remains unchanged. An absent or incomplete default-branch bundle still
fails closed. Git fixtures, event documentation and a narrow second Delta review
must verify this correction and its direct regressions; the existing Full review
is retained.
