# Dependency compatibility: publication and remote evidence

Task BB-DEPENDENCIES-009 is delivered as [PR #15](https://github.com/Artifaktory/engineering-backbone/pull/15), open and unmerged. Merge and release remain human decisions.

## Fixed published snapshot

- Base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
- Tested and Codex-reviewed public head: `fd751944bb13d5abd17e0033ec28bfa798d3ed33`.
- Exact tree: `5b523c7a4e6dcc891444e9560c46df77362448bb`.
- Matching local publication head: `101b3b5f8b2b16618cb11e80e723c03a3b846456`.
- Base-to-head patch SHA256: `d018aa70b25c5d7d12c499c4363bedf93142acb92818d1ad63d9f87f25547db1`.

GitHub Git-object readback confirmed this exact tree. Raw remote reads of Dockerfile, policy/dependencies.md, docs/dependency-compatibility.md and AGENTS.md matched the reviewed local bytes exactly. The complete tree match covers the remaining tracked inputs, including .dockerignore, manifests, source check, CI and review records. These are real files in the PR, reachable through agent entrypoints and the Task Packet.

## Actual GitHub execution

[Backbone quality run 38558220207](https://github.com/Artifaktory/engineering-backbone/actions/runs/38558220207) completed **successfully** on the fixed published snapshot.

| Job | Result | Executed evidence |
| --- | --- | --- |
| Source dependencies and container, 115832546789 | PASS | Clean hash-verified installation, tracked inputs and all 26 locked versions; actual tracked Dockerfile build; offline image validation, all four compiler checks, pip check and 13 real Copier tests in 31.936 seconds. |
| Trusted base policy, 115832546991 | PASS | Base-owned validator against candidate. |
| Foundation checks / Validate governance and compatibility, 115832547118 | PASS | Source validator, compiler/fingerprint checks, complete serial unittest discovery: 362 tests in 317.558 seconds, OK; committed patch whitespace. |

Downloaded job-log SHA256 values (redacted execution artifacts remain outside Git):

- Container log: `74705db8b2cb0dceeafe0becdbbfb7d1b6fb4a9892085936e2d276270af49f80`.
- Foundation log: `82475764ce38dcca69b555ab3bb5d7e08fd2f66aad0fb0a56b5b80cf39a18b6c`.

The earlier local 362/362 isolated-module rerun and the original failed run remain accurately recorded in the [independent checks report](dependency-compatibility-checks.md). The remote serial run is additional actual evidence; no prior failure is relabeled PASS.

## Codex and independent disposition

The [visible manual request](https://github.com/Artifaktory/engineering-backbone/pull/15#issuecomment-6167493275) supplies Task Packet, trusted base/head, tree, patch digest, Full advisory mode and local evidence. The bot summary records manual review completion at 2026-10-14T11:44:01.769243Z. Its [result](https://github.com/Artifaktory/engineering-backbone/pull/15#issuecomment-6167549793) identifies the correct commit and reports no major issues. Inline threads and submitted-review lists were empty when checked; this is an advisory issue-comment result, not a GitHub approval or human merge authorization.

[Independent remote triage](dependency-compatibility-remote-triage.md) directly verified the response and execution evidence: **NO CONFIRMED IN-SCOPE REMOTE FINDINGS**, no further repairs. Foundation was still running during that triage; the subsequent successful final result is recorded above. The local plan/Full/triage/repair/Delta chain and DEP-TEST-001 closure remain linked from the [original closeout](dependency-compatibility-closeout.md).

## Acceptance and remaining boundaries

All seven scoped acceptance criteria now have execution/review evidence: AC-1/2/3/5/6 are recorded in the original closeout and independent reports; the actual image build/offline smoke closes AC-4; exact remote readback, visible completed Codex request and successful CI close AC-7. The Task Packet points to the fixed tested public head.

This publication follow-up changes only evidence documents and Task Packet statuses. Executable code, Docker inputs, policies, schemas, catalogs, manifests and tests remain identical to the tested/Codex-reviewed snapshot. The original reports preserve their pending-at-observation states; this record supplies the later results. CI on any later evidence-only commit is a distinct run and must not be inferred from the run above.

Native Windows execution, arbitrary consumer runtime/PostgreSQL combinations and native agent discovery remain outside this source evidence. No merge, release, deployment, repository-setting change or downstream write occurred. The PR is ready for the human's review and merge decision.

The [independent publication-evidence review](dependency-compatibility-publication-review.md) verified the preceding four-file closeout snapshot, live GitHub results and recorded log hashes without findings. Its verbatim record and this link are the final evidence additions.
