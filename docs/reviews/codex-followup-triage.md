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

## Direct regression: policy ownership after promotion

BB-CX-07-DELTA-02 is a confirmed P1 discovered during the final ownership probe
and independently reproduced by `codex_delta_security` before repair. The base is
local `dc1459fe44499e2f72b9cedde74884cd5a17eeb9`, tree
`2727bd2a2c0f7a10bca749165f29a9a50021343b`, identical to published `abb280c`.

A candidate canonical `core.json` symlink to `../../candidate/strict-core.json`
initially resolves inside the candidate and contains the strict base policy. The
actual workflow returns 0. After promotion preserving that symlink into
`trusted-base`, it points into the next candidate. Removing a custom true invariant
from the target also returns 0: the supposedly trusted comparison now reads the
candidate's rules. Current and previously approved tooling both reproduce this;
an independently owned regular strict base rejects the same removal with exit 1.

This is a direct gap in BB-CX-07's protected promotion contract. Repair requires
regular canonical policy files in both snapshots before dependency or validator
execution, plus current-validator policy ownership and containment checks. Policy
values remain project-specific and unhashed; ordinary stronger JSON policies stay
supported. Refresh the current tooling identity, retain the previously reviewed
coherent identity, and independently Delta-review the correction and its direct
regressions. No new trust boundary or unrelated foundation work is introduced.

## Subsequent provider compatibility findings

Codex review `5488022625` inspected published `abb280c` and reported two direct
regressions in the follow-up compatibility mechanism.

| ID | Severity | Provider thread | Trigger and triage |
| --- | --- | --- | --- |
| BB-CX-08 | P1 | [4245880365](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245880365) | Historical test sources are loaded with `git archive` from development-tree objects. A clean squash checkout lacks those objects; tests fail despite valid tooling. Confirm by isolating a single-commit checkout before replacing the dependency with durable historical fixtures. |
| BB-CX-09 | P2 | [4245880378](https://github.com/Artifaktory/engineering-backbone/pull/1#discussion_r4245880378) | Bundle attributes set text/eol but inherit independent parent content filters and working-tree encodings. Confirm the actual transformed checkout before clearing those attributes only on the eight attested files. |

Both repair decisions remain within BB-CX-07's existing compatibility contract.
Preserve exact historical tooling identities and real Copier upgrade coverage;
protect managed bytes while retaining application-owned attributes. Reproduction
results and the immutable review snapshot are recorded with the next Delta result.

Both subsequent provider findings were confirmed before their repairs. BB-CX-08:
a fresh one-commit source repository had none of the three historical trees; the
actual historical compatibility test failed with `git archive` exit 128. BB-CX-09:
real Git checkouts with an inherited content filter or UTF-16LE encoding changed
the managed toolchain digest; application files also received their intended
transformations. The fixes package unchanged historical source blobs with verified
provenance and unset only content-transform attributes on attested file paths.
