# Local runner Full review triage

Both independent Full reviewers inspected the same manifest-bound snapshots before repairs.

| Finding | Decision | Scoped repair |
| --- | --- | --- |
| LR-PLAN-001 | Confirmed, resolved in reviewed plan Delta | Original pull_request merge-result checkout retained |
| LR-AO-RUNTIME-001 | Confirmed P2 | Certify UID1001 and writable renderer mounts; actual preflight before checkout; preserve browser image and tests |
| LR-AO-RUNTIME-002 | Confirmed P2 | Explicit per-tier native tools/CGO/rebuild prerequisite catalog and activation evidence; pinned leaderboard Node setup |

Backbone has no confirmed in-scope Full finding. Its complete 239-test suite passed in 642.854s; this supplements the frozen check record. AO broad source failures remain outside this routing diff and are not certified green. No merge/activation is authorized by these reviews.

Repairs remain within the runner prerequisite/verification contract and require scoped Delta review of the two runtime IDs and directly introduced regressions. Draft activation stops remain in force.

## Remote Codex follow-up triage

`LR-BB-CODEX-001`, P1, confirmed at GitHub head `19fb75b640a470b459119f1654f5e43d3c1aef2b` (local identical-tree head `21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb`). [Remote finding](https://github.com/Artifaktory/engineering-backbone/pull/11#discussion_r4261094614). A foreign-fork source PR skips both Foundation governance and Trusted base policy. GitHub reports conditional skips as successful/nonblocking, allowing a required-check merge without either original validation. The skip is introduced by this runner migration, so the earlier clean Full/Delta conclusions do not close this newly observed defect.

Minimal scoped repair: schedule the original check names and fail in a fixed first shell step before any candidate checkout/setup. Source foreign or absent head identity fails; same-source requests and original external consumer/non-PR behavior remain intact. Add actual-script regression cases and correct the existing same-source fixture. Require independent plan follow-up, deterministic checks, two scoped Delta catalogs and remote Codex follow-up. AC2/3/4 return to pending until this evidence is complete; activation remains blocked separately.

Closure: the reviewed plan was implemented and independently checked at
`a2e9f536f589042425ebc3f248dc0bde8215a7de`: 242 local tests passed. Two independent
scoped Delta catalogs at frozen head `1d0f055d54b57011d3da200c5e037319c8cca44d`
both close `LR-BB-CODEX-001` as RESOLVED and report no confirmed direct repair
regressions. Original names/scheduling, first-action ordering, quoted event data,
caller-mode independence and external consumer/non-PR behavior are verified.
AC2/3/4 are now pass on the recorded evidence. Fresh remote advisory review remains
to be recorded on the final PR head. The actual source-runner Python-loader failure
and clean-isolation qualification remain blocked under AC5; closing this P1 does
not convert that required remote failure into success.

## Closure artifact follow-up: LR-BB-CLOSURE-001

Confirmed P2 at local closure head `14b1abc04d8328861c0b0256077a2fbeef1b025a`:
the final independent current/trusted validators both exited1, rejecting the four
raw companion `.json` records under `docs/reviews` as unsupported governance JSON
artifacts. The gate implementation and checked source files are unchanged; this
is a directly introduced evidence-packaging regression. Publication remains
stopped while this required metadata check fails.

Minimal repair: retain each raw record byte-for-byte as `.json.txt`, update only
the durable-copy mapping, and rerun both actual validators plus committed-range
whitespace/source equality checks. Do not change the validator, schemas, source,
compiled tooling, assertions or check configuration. Require scoped independent
Delta closure for this confirmed ID and direct documentary regressions. AC3/4
return to pending until repaired metadata and review pass; AC5 stays blocked.
