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

PR creation and actual remote-check readback are pending at this record's initial
commit. Queued, absent or skipped checks are not passing. No runner provisioning,
hosted fallback, GitHub artifact upload, protection or permission change is included.
