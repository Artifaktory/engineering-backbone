# Publication identity and remaining gates

The user authorized a PR, not merge or release. Publication uses the authenticated
GitHub connector because local Git has no push credentials. This transport creates
new commit identities. The original reviewed local commits remain accurately named
in the reports; the table maps them to reachable published equivalents.

| Subject | Reviewed local commit | Published equivalent | Identical tree |
| --- | --- | --- | --- |
| Independently reviewed plan | `6dc0cd666ef20bd5049121a143aa238cc84548d0` | `673c2e4964649380ff543540b8592bdafda27e5d` | `c0d2806bb964087cbabcd3ea813421fb2d326542` |
| Initial implementation | `729531ef541720058c1984e925886dc538e7b77b` | `b5e2d0bb7e9220be675ab3e81650a3764210ad52` | `46bb7e8b396d3cf337bd9fbdf0165030f6d2c909` |
| Quality-checked and Full-reviewed repair | `6a1089aa148fabbf7c5a223a9055f2dd7b187878` | `3badd4a15da5c2fb0a5136d234d2475702bb1a75` | `7506a34fef2b14cf5ce93c0bcc6f28afc725ac36` |

After creating and fetching the published branch, root compared all three actual
Git trees, each parent correspondence and each complete binary patch: all matched,
exit 0. Both chains start at actual merged base
`4394763d03c1d1302b6b37cef142d0f98f848be4`. The full reviewed base-to-head patch is
identical, SHA-256 `746882d44bee3159bc83dfca1fee3a5d07e399f3ecd521a8fa791c73908d2798`.
This is verified content/parent correspondence, not a claim that local commit IDs
were pushed unchanged. The source tooling and workflows have no post-review edits.

Later commits add only this delivery's evidence, acceptance bookkeeping and
publication readback. They are outside the earlier Full subject. Candidate and
actual base-owned validation and the final committed base-to-published-head
whitespace check are required again. The PR description records the final published
head and patch identity so this document need not claim to contain its own commit SHA.

## PR and runtime evidence

PR creation/readback is pending at this record's initial revision. The intended
target is `main`, branch `docs/planning-delivery-contract`, as a draft because native
Windows, Docker and actual local-runner CI evidence remain unresolved. The PR body
and subsequent readback record must use observed identities/statuses, not infer PASS
from job labels or local fixture-based tests.

No runner provisioning, repository protection change, hosted fallback, GitHub artifact
upload, automatic downstream application, merge, release or deployment is authorized
by this record. Legacy optional consumer workflows keep their documented separate
assumptions and are not activated by this source PR.
