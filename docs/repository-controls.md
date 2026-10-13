# Repository controls and readiness

This repository distributes a control plane. Its own CI and independent review are
required before proposing downstream use. A structural validator is not a complete
security boundary. Human merge/release and GitHub enforcement are distinct controls.

## Observed baseline, 2026-10-12

| Item | Actual observation |
| --- | --- |
| Repository | `Artifaktory/engineering-backbone`, private, default branch `main` |
| Initial base | `396737eea7cc2d69b654917dfb62e39541c7ac3a`, README only |
| Auto-merge | Repository metadata reports `allow_auto_merge: false` |
| About description | Empty; recommended text below is prepared, not applied |
| Rulesets | GitHub returned 403 with “Upgrade to GitHub Pro or make this repository public to enable this feature.” |
| Branch-protection read | GitHub returned 403 “Resource not accessible by integration.” |

These failures do not establish an enforced merge gate. Changing visibility,
upgrading a subscription, installing integrations or widening access is a separate
human decision. Neither a private repository nor an agent instruction enforces
required checks or approvals on its own.

Recommended GitHub About description:

> Versioned, reusable agent governance and engineering building blocks for Codex,
> Copilot and software repositories, with validated consumer adoption and updates.

## Required operational checks before a consumable release

- Verify the available repository protection mechanism for the actual GitHub plan.
- Require PRs and actual successful Foundation / Trusted base checks; use the exact
  check names visible after the first workflow run.
- Require independent human review of control-plane changes, dismiss stale approvals
  and require review after changed commits. An AI/provider approval is not our human
  release decision. Verify eligible reviewers rather than installing fake owners.
- Restrict direct pushes, force pushes/deletion and bypass permissions appropriately.
- Keep Actions token permissions read-only by default and avoid governance auto-merge.
- Configure actual private-workflow sharing only for intended consumer repositories.
- Configure provider automatic PR reviews separately when desired/eligible; keep them
  advisory to the formal frozen review chain.
- Record the reviewed commit, actual CI results, live native-profile discovery and
  remaining limitations before a human creates a release/tag.

If those release controls are unresolved, do not classify this bootstrap as approved
for downstream distribution. CI can still provide evidence for reviewing the PR.

## CI in this PR

`quality.yml` runs on PRs, main pushes and manual dispatch. It calls the reusable
workflow to validate source policy/schemas/examples/native adapters/workflows and
run adversarial plus real consumer-generation/upgrade and actual workflow-payload
tests. Committed whitespace checks use explicit PR base/head or push before/head
revisions, not the clean checkout working tree. It uses read-only tokens, pinned
Actions and no deployment/provider secrets.

The trusted-policy job checks out explicit base/head revisions and executes the
base-owned validator/dependencies against the candidate. That protects supported
machine invariants after bootstrap without trusting a newly weakened head validator.
The README-only initial base has no validator: the job emits an explicit bootstrap
notice requiring independent human review rather than claiming a pre-existing gate.

The consumer branch of the reusable workflow also executes only the trusted
consumer revision's validator, schemas and dependency lock, with `--trusted-base`.
Before dependencies or validator execution, the pinned workflow independently
attests all eight tooling files in both snapshots against its own coherent
fingerprints and checks monotonic provider selections. Both canonical policy files
must be regular files owned by each snapshot before any tooling executes. Unknown base tooling,
poisoned candidate tooling, mixed versions and inherited-provider disablement fail
closed, including when the previous validator predates those checks. First adoption needs a
reviewed seed PR with the caller inactive, followed by a separate activation PR.
Consumer callers cannot select source mode. Manual dispatch always uses the
repository default branch's bundle as trusted tooling, even when the candidate is
an unmerged feature commit. Its whitespace check covers the selected commit's
latest patch; the trusted policy comparison uses the default branch. See
[adoption](adoption.md) for the event matrix.

The workflow itself can be changed in a PR. Protected external approval/check
settings and independent review are still needed to prevent bypass. Format/evidence
tests cannot replace semantic review, authenticated approvals or runtime discovery.

## Toolchain fingerprint maintenance

`python scripts/compile_toolchain_fingerprint.py --check` must pass in source CI.
The compiler fingerprints actual Copier-rendered working-tree output rather than
raw source bytes; it excludes policy/project data, docs and provider metadata.
A tooling change requires a reviewed `--write` refresh of the workflow current
literal and the matching consumer workflow pin. Its previous list permits only
explicit reviewed compatibility snapshots; arbitrary caller hashes are forbidden.

The initial retained entries were calculated from these actual Git trees:

| Source snapshot | Git tree | Rendered tooling SHA256 |
| --- | --- | --- |
| Bootstrap review, local `d568bf8` / published `6982e4a` | `da5e4b16db198a583ca252f109d33778de0a3f78` | `444494997fb175e75e9fe5031d02e1005db910800711116773c890ea24508566` |
| First repair review, local `6542ad3` / published `3a2e3c8` | `d28d6972fa999e785af13b315ce4daf570c73aea` | `92a5da2f8cbc81f588e231167ae5b66e5f69e255f80be1d13c80ea4152b3dffa` |
| Tooling review, local `dc1459f` / published `abb280c` | `2727bd2a2c0f7a10bca749165f29a9a50021343b` | `ef266be0f22b7e505563e408fe8b93ab6418ec1255bed6c2d6067f9e74be44c9` |

These are reviewed PR snapshots, not declarations that releases or downstream
adoption are approved. Consumer candidate tooling can stay at its approved base
or upgrade to the current literal; it cannot mix historical files or downgrade to
another retained version. A SHA or schema-valid report alone is not human approval.

## Update/release discipline

The [shared workflow kit](workflows/README.md) adds a strict aggregate with fixed
expected jobs; require its actual published final status only after the reviewed
complete seed and activation steps. Verify deliberate failure, missing-job and
green cases against hosting protections before declaring enforcement. Legacy
governance and kit execution are separate; a generic required check's skipped or
neutral GitHub conclusion is not proof that every project requirement ran.
This delivery configures no server-side protection, publishes no Backbone release
and activates no downstream caller.

Publish reviewed releases with immutable commit references. Consumers obtain
provider-selected files and their own settings; update through consumer PRs. A
central fix does not silently alter existing consumers. If a defective release is
found, stop new adoption, document the affected versions and provide a reviewed fix;
each consumer decides its rollback/update with its own required checks.

## Quality-profile gate and limits

The [quality framework](quality/README.md) adds source compilation and a
workflow-owned consumer guard. The current catalog is compiled trusted data;
consumer/base JSON cannot redefine it. The guard checks safe files, activation
against a complete reviewed seed, actual workflow check IDs/kinds, monotonic active
selection, traceability and bounded exceptions. Project commands still execute
only in the separate workflow kit. The governance guard executes no candidate
quality code.

Require the observed governance and kit statuses through independently verified
hosting controls before describing them as merge enforcement. Agent instructions
and local validation guide behavior but cannot authenticate manual approvals,
validate the meaning of an evidence file or certify software against a standard.
Public ISO/IEC abstracts are reference scope only; full normative adoption and any
certification scheme need a separately approved project contract and evidence.
