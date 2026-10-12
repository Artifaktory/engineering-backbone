# Codex follow-up triage: trusted tooling promotion

Codex review `5487485660` inspected published commit
`3a2e3c83954cff3f7402fad7293b58c4524ae21a`. Local commit
`6542ad3f76ae35fa5475fad998a7aa2967225496` has identical Git tree
`d28d6972fa999e785af13b315ce4daf570c73aea` and is the next repair base.
The [active packet](../../plans/codex-findings-task.json) covers these confirmed
follow-up findings under the task owner's request to repair valid findings and
review the changes before updating the same PR.

## Reproduced before repairs

| ID | Severity | Provider thread | Reproduction and triage |
| --- | --- | --- | --- |
| BB-CX-05 | P1 | [4245472719](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245472719) | Confirmed: real consumers can disable Codex, Copilot or both in candidate metadata and remove standing/native files; the unchanged trusted-base validator returns 0 because selection is candidate-owned. |
| BB-CX-06 | P2 | [4245472732](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245472732) | Confirmed: both shipped caller definitions lack `workflow_dispatch`, so the advertised manual consumer flow is unreachable without a custom caller. |
| BB-CX-07 | P1 | [4245472740](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245472740) | Confirmed: a candidate changing only its validator to a no-op and a schema to `{}` passes. After promotion to the next base, a subsequent weakened-policy candidate passes and executes the no-op. The earlier combined-corruption test did not isolate this poisoning step. |

No finding is rejected. Reproductions used temporary real generated bundles and
the actual reusable-workflow shell. The original four repair outcomes and the
dispatch correction remain recorded in [the previous result](codex-result.md).

## Scoped repair decisions

- Read and validate trusted project facts; enabled providers cannot become disabled
  in ordinary updates, and their files remain checked. Fresh provider selection and
  valid strengthening remain available. A human-reviewed removal is a distinct
  governance migration; a candidate flag is never authorization to bypass a gate.
- Ship the manual trigger in both the active caller and the manual example.
- Before dependencies or validators execute, the immutable called workflow verifies
  coherent approved identities of both base and candidate managed tooling. The
  authority is pinned workflow content, not a candidate-owned manifest or input.
  Personalized project facts, policy additions and agent prose are not toolchain
  bytes; their existing structural, monotonic and human reviews remain separate.
- An unchanged approved base or coherent current reviewed upgrade is supported;
  unknown/mixed tooling and rollback to another historical identity are rejected.
  Legitimate Copier tooling updates therefore also need a reviewed workflow pin.
  The producer checks the current identity against real rendered Copier output.
- Previously approved validators lack the new provider comparison, so the pinned
  workflow independently checks adapter selections before invoking older tooling.

No private-source checkout credential, provider key, candidate hook, arbitrary
allowlist input or automatic downstream update is added. The next frozen review
covers these repairs, their new tooling-identity contract and direct regressions;
unchanged foundation areas are not re-reviewed.
