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
It fails before execution if that baseline is incomplete; first adoption needs a
reviewed seed PR with the caller inactive, followed by a separate activation PR.
Consumer callers cannot select source mode. Manual dispatch always uses the
repository default branch's bundle as trusted tooling, even when the candidate is
an unmerged feature commit. Its whitespace check covers the selected commit's
latest patch; the trusted policy comparison uses the default branch. See
[adoption](adoption.md) for the event matrix.

The workflow itself can be changed in a PR. Protected external approval/check
settings and independent review are still needed to prevent bypass. Format/evidence
tests cannot replace semantic review, authenticated approvals or runtime discovery.

## Update/release discipline

Publish reviewed releases with immutable commit references. Consumers obtain
provider-selected files and their own settings; update through consumer PRs. A
central fix does not silently alter existing consumers. If a defective release is
found, stop new adoption, document the affected versions and provide a reviewed fix;
each consumer decides its rollback/update with its own required checks.
