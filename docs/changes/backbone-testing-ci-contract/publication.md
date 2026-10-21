# Publication identity and readback

Repository: `Artifaktory/engineering-backbone`; branch `docs/testing-ci-contract`;
target `main`. Actual main was read back as
`1a740604d4a6a68e500da36c4d99935d04a8ce86` before publication. Publication uses
the authenticated GitHub connector. Its commit metadata differs from local Git,
so commit IDs differ while exact trees and ordered ancestry are preserved.
No main update, merge, release or deployment is authorized or performed.

| Stage | Local commit | Published equivalent | Exact tree |
| --- | --- | --- | --- |
| Plan | `519db0c68e235356fef015f3a05c139f4339afec` | `fa64dbbf5478f656bf4c4d8f8e88f75afa67ad75` | `ce9f3b3e8fc719f16fcf5bef167d602ef3984865` |
| Initial implementation | `6037d92570d1a22e7c297b9240b295537d5da0b1` | `8364ce6b9e904a972e09b00bd49fb5d7485d36d1` | `c14a68b13248301e161a8da8299f8cb33bbdb24b` |
| TEST-CHECK-01 repair | `47cec1a72dbed195cbeb3534f83a80696061e2ff` | `e98db79ab5799ab8ddcbbb4dc2941807f2846ab1` | `a8a58636308da81c153c8655f837a488f19ad50f` |
| TEST-CHECK-02 repair / reviewed subject | `daa85bfd64467da798c57cef2894292c646e2750` | `9972cd8d47079fb8726f4d79edb75f5f1b36cb2d` | `24ba4293cfdff2003af2f0686bcc93597773a27d` |

Each API-created tree matched the corresponding local tree before commit creation.
After branch creation, `git fetch origin docs/testing-ci-contract` retrieved the
actual objects. A read-only Python/subprocess comparison checked all four pairs:
exact tree equality, parent correspondence (first parent actual main; subsequent
parents previous mapped commit), and byte-for-byte equality of
`git diff --binary BASE LOCAL` and `git diff --binary BASE PUBLISHED`. Exit 0.
Reviewed implementation patch SHA-256 on both histories is
`c0f1cb18497072a46abe767fae67211d9db3f4543b0f26d1776b1cde9f3b0756`.
The initially failing implementation and both narrow repairs remain distinct.

## Evidence-only closeout

Later commits add quality/review/triage/acceptance/publication records only. They
describe the earlier frozen subject; neither Full claims to review its own report.
Candidate and actual base-owned validators and committed whitespace checks are
repeated for those commits. Their published trees/parents/patches are compared
again; the final identity/check result belongs in actual PR readback, avoiding
a self-referential commit hash.

The first evidence-only local commit `8b15b6669bc5fbbe30caed74cc97f40625a0dc8f`
maps to published `98ca049ef4b0d1c6f53075ce960f9c34b543e21c`, exact tree
`7b37a0a7c9c0be9242757cdbaa075dc74dcf0e08`. Its published parent is the mapped
reviewed implementation. Candidate and actual base-owned validation passed, exit 0.
After this commit, `git diff --check BASE LOCAL_HEAD` and
`git diff --check REVIEWED_LOCAL_HEAD LOCAL_HEAD` passed, exit 0. After fetch,
exact tree/parent/base-to-head binary-patch correspondence and both corresponding
published whitespace checks passed, exit 0. Base-to-evidence patch SHA-256:
`ff2484f7b37983c82490ce7b5227f201a6432dd56e5ff1fd075c031221557007`.

## Actual PR and first CI readback

[Draft PR #23](https://github.com/Artifaktory/engineering-backbone/pull/23) was
created on 2026-10-21 at 10:01:31 UTC. Actual REST readback confirmed open, draft,
unmerged, base `1a740604d4a6a68e500da36c4d99935d04a8ce86`, head
`98ca049ef4b0d1c6f53075ce960f9c34b543e21c`, mergeable true with state `unstable`.
All 61 changed paths from the paginated PR listing exactly matched local Git.
The combined status API returned no legacy statuses; this is not CI success.

| Actual workflow run | Jobs observed | State |
| --- | --- | --- |
| [39581489182: Backbone quality](https://github.com/Artifaktory/engineering-backbone/actions/runs/39581489182) | Trusted base policy; Foundation checks / Validate governance and compatibility; Source dependencies and container | all queued; no conclusion |
| [39581489034: OpenCode native discovery](https://github.com/Artifaktory/engineering-backbone/actions/runs/39581489034) | Native smoke (ubuntu-latest); Native smoke (windows-latest) | both queued; no conclusion |

Raw job readback showed `self-hosted`, `Linux`/`Windows`, `X64`, `backbone-ci`
labels; no assigned runner. Display names containing `ubuntu-latest` or
`windows-latest` do not establish hosted execution. The five jobs have not passed.
No runner provisioning, hosted fallback, GitHub artifact upload, protection or
permission change was made. Existing CI YAML remains untouched.

This readback-only record is followed by another evidence commit. Repeat validators,
local/published committed whitespace and exact tree/parent/patch correspondence for
that final commit, then read back its actual head and new workflow runs. Final
identities/statuses are recorded in the PR body, without claiming this file can
contain its own final commit hash. Pending CI remains a merge/release gate.
