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
| Review and acceptance evidence | `df0460199ecf8a3918728e350f2b8d0c5afac56a` | `e24d8f656b52641440b753f19eb3790560128b9a` | `02a2442a6ea902d92af33ab1f21eff8033a37033` |

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

[Draft PR #22](https://github.com/Artifaktory/engineering-backbone/pull/22) was created
on 2026-10-21, targeting `main` from `docs/planning-delivery-contract`. Its observed
base was `4394763d03c1d1302b6b37cef142d0f98f848be4` and initial head
`e24d8f656b52641440b753f19eb3790560128b9a`; open, draft and not merged. All 61 changed
filenames matched the local reviewed/evidence patch exactly. The published evidence
tree and mapped parent matched; final initial-publication committed whitespace
exited 0. Its base-to-head patch SHA-256 was
`079d0aa739c0471aee2e0239d67653d050e9e6ea7392dea65f515db118d5c40c`.

Actual readback at approximately 07:00 UTC, before this readback-only update:

| Run | Observed jobs | Status |
| --- | --- | --- |
| [Backbone quality 39558918554](https://github.com/Artifaktory/engineering-backbone/actions/runs/39558918554) | Trusted base policy; Foundation validation; Source dependencies/container | All queued; no conclusions or executed steps. |
| [OpenCode native discovery 39558918673](https://github.com/Artifaktory/engineering-backbone/actions/runs/39558918673) | Linux and Windows native checks | Both queued; no conclusions or executed steps. |

These observations establish neither a matching runner nor passing remote checks.
The historical native display names do not override their configured local labels.
No completed hosted execution or source artifact upload was observed. Native Windows,
Docker and actual local-runner CI evidence therefore remain unresolved. This
readback-only commit may supersede these queued runs; the final PR description
records the final head and its actual latest readback rather than treating the
earlier queue as current evidence.

No runner provisioning, repository protection change, hosted fallback, GitHub artifact
upload, automatic downstream application, merge, release or deployment is authorized
by this record. Legacy optional consumer workflows keep their documented separate
assumptions and are not activated by this source PR.
