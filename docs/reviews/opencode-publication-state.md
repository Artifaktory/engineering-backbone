# OpenCode publication and acceptance state

Date: 2026-10-16. Task BB-OPENCODE-010. This records the local publication gate;
it does not approve merge, release, activation or a production model tuple.

The reconstruction's complete repaired-source suite passed 414 tests in
355.728 seconds, with all nine deterministic gates passing. Two independent Full
reviews identified one immediate-predecessor upgrade regression. Separate triage
confirmed it; the bounded repair, independent quality rerun, independent Delta
and final triage closed REC-BB-SEC-001 and its duplicate REC-BB-FUNC-001.

| Acceptance | State at publication preparation | Evidence |
| --- | --- | --- |
| AC-1: opt-in adapter and shared procedures | PASS | Complete suite; behavior/security Full reports; unchanged default Copilot rendering |
| AC-2: strict native guards and override regressions | PASS | Complete suite; security Full; current and exact-predecessor validators |
| AC-3: scoped navigation and plan-review procedures | PASS | Navigation/receipt regressions and both Full reviews |
| AC-4: installation, preservation and upgrades | PASS | Actual Copier tests; exact-predecessor old-to-old/old-to-current workflow cases; independent fixture regeneration and Delta |
| AC-5: paired AO admission/lifecycle contract | PENDING | Backbone contract reviewed; paired AO implementation is on its work branch and still completing its separate full gates |
| AC-6: native platform and qualification states | PENDING | Actual Linux OpenCode 1.19.0 smoke passed; its 22 input hashes and runner remain unchanged. Actual Windows CI is pending. No real-model tuple is qualified or installed by default |
| AC-7: complete checks and independent review chain | PASS | 414-test repair-quality record, nine gates, two Fulls, separate triage and independent Delta |
| AC-8: published PR and actual remote outcomes | PENDING | PR creation, visible Codex request and remote check/review inspection follow this record |

The active Task Packet retains pending states for the remaining paired/remote
evidence. A passing local publication gate is not an all-platform acceptance.
Docker is unavailable locally; its existing CI job remains a remote requirement.
The native canned-provider smoke does not establish model compliance, operating
system confinement or native compaction/resume/delegation qualification.

## Snapshot correspondence

GitHub's commit API creates a different commit identity while preserving the
exact tree. These fetched remote correspondences were verified:

| Stage | Local commit | Remote commit | Identical tree |
| --- | --- | --- | --- |
| Full snapshot | d6a4af73ed39273383457669d498d9e2d4c3f22a | a9262b6abc4c7bbc012830cc9f4e28df05a900a7 | ce15f563e2656831b48e01cf144fa65650033d80 |
| Tested repair | 0778d728a273bc6af845b18d33f96e5731df9bc9 | 8bb1e27d4c1fbc9e70ece29a0f3c0763fb64caa9 | 6527697236e82bb39e07b2237a1efafb8907de3e |
| Delta snapshot | c2c31eed661714c0d8bc2245ff8505ac01a60c9a | 85091ca74321668a3eb151ee2652ece7982fd8fc | 15bf96a0d003cc6b9d20dc1482d250b35dbbb44b |

The source base remains bf8e901ecd066e8e6d1b05f0c56a66081a473c0a.
The reviewed Delta base-to-head binary patch SHA-256 is
d34ceb2a0aee308a460f43e0da0ad4efea9cf3955f56cc27651f1f31a071cb92.
Subsequent publication bookkeeping consists of review/acceptance records only;
it does not change the tested implementation, workflow, native inputs or fixtures.
The final published head/tree must be checked again after upload.

Records: [Full behavior](opencode-reconstruction-full-behavior.md),
[Full security](opencode-reconstruction-full-security.md),
[repair checks](opencode-reconstruction-repair-checks.md),
[Delta](opencode-reconstruction-delta-security.md), and
[triage including closure](opencode-reconstruction-triage.md).

The paired AO work is tracked on
[its scoped work branch](https://github.com/Binary-Refinery/agent-orchestrator/tree/feat/opencode-backbone-governance).
Its tests and reviews are separate evidence; this record does not certify them.
