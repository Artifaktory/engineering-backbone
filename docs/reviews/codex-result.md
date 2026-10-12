# Codex finding repair verification

This record covers the four findings on PR 1 at published snapshot
`6982e4a53185b5fcba48b17db10a59a3eaca83ee`, their confirmed repairs, and the
directly related dispatch bypass found during Delta review. See
[triage](codex-triage.md) and the
[active task packet](../../plans/codex-findings-task.json).

## Frozen review subjects

| Subject | Local commit | Git tree |
| --- | --- | --- |
| Repair base, identical to the provider-reviewed published tree | `d568bf820ab9d49a9bff34edb2cab32755cfca3a` | `da5e4b16db198a583ca252f109d33778de0a3f78` |
| First repair / Delta round 1 | `91cae8957fd84dcaa96e97f6d88303d79caba03e` | `f2ce5c09a6b5ce6750b87601cc54e91f6fc108d4` |
| Dispatch follow-up / Delta round 2 | `a48f3a4a6df4127a7bd730e8304cf47b10bce0e5` | `ef08cae8395067601c0767d503cc59e3bf3fef35` |

Round 1 patch SHA256:
`0703de7120c017d522a72927b6efb6d3df0ac1ab8cb362a21331cb789733caff`.
Round 2 patch SHA256:
`aa70214d9b98b6dc0da831694cdb64488694ed65acde68d81089344f08bc3b83`.
Digests use `git diff --binary --full-index BASE HEAD` for the respective rows.
The GitHub publication may have different commit metadata; matching Git trees and
published revision mappings are recorded in the PR. This file is subsequent
documentation of the reviewed implementation, not a new implementation change.

## Independent Delta results

The reviewers were separate read-only sessions `codex_delta_correctness` and
`codex_delta_security`; neither authored the repairs. The previous Full review was
retained. Both reviewed identical frozen subjects in each round, then reconfirmed
head/tree/patch identity and clean tracked worktrees.

Round 1 was **not accepted as final**: the correctness reviewer reproduced 66
passing tests, while the security reviewer proved that manual dispatch could
select the unapproved candidate as its own trusted tooling. That P1 finding was
confirmed before a scoped follow-up. Round 2 covered only that correction and its
direct regressions; both reviewers independently passed all 14 workflow tests and
reported no new confirmed direct regression.

| Finding | Final verified outcome |
| --- | --- |
| BB-CX-01 P1 | Consumer PRs execute the previous base's validator, schemas and hash-locked dependencies in isolated Python mode with `--trusted-base`; candidate no-op/import/schema/lock attacks fail. Missing or partial bases fail before Python execution. Downstream callers cannot select source mode. |
| BB-CX-01-DELTA-01 P1 | Manual dispatch uses the repository default branch's bundle independently of the selected feature commit. An independent custom-default-branch probe using a real pre-repair consumer baseline rejects the malicious feature with exit 1 and never runs its validator. PR/push base selection remains intact. |
| BB-CX-02 P2 | Committed whitespace defects fail explicit PR base/head and push before/head ranges on clean checkouts. Dispatch checks the selected commit's latest patch; root/zero-before cases use the empty tree. |
| BB-CX-03 P2 | Ignored source-root `artifacts/` run evidence is excluded; nested governed documentation and managed consumer artifacts still reject malformed contracts, missing links and conflict markers. |
| BB-CX-04 P2 | Copier rejects invalid branch components, reserved `HEAD` and trailing/control characters before destination writes. Project/task schemas reject the same Git-invalid forms while retaining valid nested and existing metadata names. |

Independent Git/schema oracle probes and real Copier upgrades also confirmed valid
branches and preservation of a manually activated caller while its saved template
workflow choice remains empty. These are model-session observations, not human
signatures or evidence of release approval.

## Deterministic checks executed

The existing isolated Python 3.12 environment used the previously verified,
unchanged `requirements.lock`. No dependency or Action pins changed.

- `python -m unittest discover -s tests -v`: final **68 tests**, 30.059 seconds,
  exit 0; real Copier and actual reusable-workflow shell payloads are included.
- `python scripts/validate.py --trusted-base artifacts/codex-repair/trusted-source`:
  exit 0 against the extracted pre-repair source policy.
- `python artifacts/codex-repair/trusted-source/scripts/validate.py --root .
  --trusted-base artifacts/codex-repair/trusted-source`: previous source validator,
  exit 0 against the final candidate.
- Actionlint 1.7.12 on both source workflows: exit 0.
- Working/staged and explicit frozen repair-range whitespace checks: exit 0.
- Independent second-round workflow reproduction: 14 tests per reviewer, exit 0;
  additional security probe used separate reviewed default and malicious feature
  Git revisions rather than trusting the test candidate's bundle.

## Publication and operational boundaries

GitHub-hosted CI, provider re-review and publication-tree readback are recorded on
PR 1 after publication. Local checks do not establish those external outcomes.
First consumer adoption requires a reviewed seed with the caller inactive, then
a separate activation PR after the seed exists on the base/default branch.

External caller protection, repository merge controls, private workflow sharing
and native client discovery remain the separate operational boundaries described
in [repository controls](../repository-controls.md). The source PR's README-only
`main` still has no earlier trusted validator; its bootstrap notice is not proof
of an existing enforced gate. No downstream repository writes, merge, release or
deployment are authorized or performed by this repair task.
