# Technology/navigation first repair Delta

These two independent reports review the first repair snapshot at `4722d46e220ee34fb649c787d19f75f77447ca0b`.
They close the effective-check finding and preserve the remaining source-project-facts defect.
[Separate Delta triage](technology-navigation-delta-triage.md) corrects the earlier source-layout assumption.
No edits occurred between these reviewers.

---

# Independent repair Delta A — behavior and compatibility

Reviewer: `/root/tech_full_behavior` · 2026-10-14 · read-only repair Delta.

## Verdict

**CHANGES STILL REQUIRED.** `TNAV-S-2` is **FIXED** within the assessed Delta.
`TNAV-B-1` / duplicate `TNAV-S-1` is **partially fixed, still open**: consumer
project/core facts and source policy/core.json are now bound, but the source
repository's existing project.json remains omitted. No unrelated Full scope was
reopened and no other direct repair defect was confirmed.

The previous report's phrase “Human triage” was inaccurate: separate triage was
intended, as required by the existing policy. There is no human-only triage rule.
Human merge/release approval remains mandatory and separate. The prior report
need not be rewritten; this clarification and the recorded triage preserve history.

## Frozen scope and identity

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`.
- Prior Full-reviewed head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`.
- Repaired head: `4722d46e220ee34fb649c787d19f75f77447ca0b`.
- Repaired tree: `ea5e2b47728d3fea7ba4a217e3ce4ac3a16fc48b`.
- Delta SHA-256: `0081f46e538998bcafaa10ba790d63b1bab68a3cce792d6acdc3e3eb74b404f5`.
- Full patch SHA-256: `0a576467bdcd34bc9638ef3dfbe16d665297921c627006f12b014ec80775582c`.
- Packet: `artifacts/technology-navigation/delta-a-task.json`.
- Authority: the existing plan and separate
  `docs/reviews/technology-navigation-triage.md`.

Identities and clean tracked worktree were independently checked before and after
the review. No tracked files, commits, remote objects or comments were changed.
Only ignored diagnostic/report files were written.

## TNAV-B-1 / TNAV-S-1 — source project facts remain unbound

**Status: STILL OPEN, P1 retained, high confidence, context completeness.**

The consumer part is fixed. The original independent behavior probe was rerun
unchanged against this repaired guard: both mandatory JSON paths now occur in the
receipt; both mutations and both removals reject verification with exit 1; normal
resolve and unchanged verify return 0. The source `policy/core.json` inclusion and
its mutation/removal checks also pass in the focused suite.

However, `scripts/navigation.py:494–499` still places
`.engineering-backbone/project.json` only in the consumer branch. That is an
existing source file, not a proposed new source contract:

- `git ls-tree BASE .engineering-backbone/project.json` returns tracked blob
  `1de5d9f5dfb428f890896c54ce70679c0a348dca`; the same file is tracked at this head.
- Its actual facts include source base branch `main`, validation command, language
  and enabled Codex/Copilot adapters.
- Source validator `scripts/validate.py:2454–2458` loads/validates that file and
  passes its contents into adapter checks; this is not a consumer-only artifact.

The new source unit fixture deletes project.json at
`tests/test_navigation.py:329–334`, then explicitly asserts its absence. The new
guide at `docs/agent-navigation.md:108–111` likewise describes a source layout
without these JSON project facts. Those assumptions are contradicted by the
tracked source layout. The earlier bounded guidance “do not invent” a source file
does not justify omitting the file that already exists.

Independent executable reproduction uses a real Copier-rendered active fixture,
maps its actual managed catalog/core/guide files into the source layout, and copies
the repository's real source project.json bytes. The frozen approved CLI is called
with `--source`. Results in `delta-behavior-source-probe.json`:

1. Resolve exits 0; `policy/core.json` is present and project.json is absent.
2. Unchanged verify exits 0.
3. Change the existing project's branch and validation command: old receipt verify
   still exits 0.
4. Remove that project.json: old receipt verify still exits 0.

This is the remaining source branch of the same mandatory-project-facts omission,
with the same trigger and impact as the confirmed original finding. It violates
the approved complete required context / stale handoff acceptance (AC-2/AC-3).
It is not a new requirement or an assertion that separate full validation allows
these omissions. The presence of copied Task Packet/contribution facts cannot
hash-bind a distinct machine facts file used by the source validator.

Bounded follow-up: bind the existing project.json in source receipts as well as
consumer receipts; keep the two core.json locations distinct. Correct the source
fixture and guide assumption. Add source-mode exact-hash, valid-change, deletion
and unchanged-restoration checks through the approved compiled CLI. Retain the
already fixed consumer and effective-check cases. Separate triage precedes repair,
then a frozen follow-up Delta can assess this remaining ID without reopening Full.

## TNAV-S-2 — effective approved check definitions

**Status: FIXED within the assessed Delta.** The new `effective_workflow` helper
at `scripts/navigation.py:198–221` substitutes the full approved check object for
an existing ID when the supplied trusted workflow is enabled, retaining genuinely
new candidate IDs. Both manifest coverage and the receipt use this same effective
view. The base manifest is evaluated with its own definitions, and candidate
workflows.json remains in the document-hash set.

Inspected this against the existing `workflow_kit.py prepared()` contract and
quality coverage substitution. Independently executed tests reject candidate
docs→migration relabeling and added candidate PR phases for approved non-PR checks;
retain all approved fields despite candidate changes; cover active inheritance
and enabled-only activation; retain new-ID behavior; and invalidate the old
receipt after a candidate declaration edit even when effective execution remains
unchanged. The installed CLI integration compares every selected complete receipt
definition to actual `workflow-kit.py prepare` output. No project check commands
were executed. No direct regression in this repair was confirmed.

## Actual commands, records and limits

| Independently executed | Exit | Result |
| --- | ---: | --- |
| `git status --porcelain`, `git rev-parse HEAD HEAD^{tree}`, both `git diff --full-index --binary … \| sha256sum` identity checks | 0 | Exact frozen identities and clean tracked tree. |
| `.venv/bin/python -m unittest tests.test_navigation tests.test_navigation_integration -v` | 0 | 35 tests in 36.849s, OK. |
| `.venv/bin/python -m artifacts.technology-navigation.review-behavior-probe` | 0 | Original consumer diagnostic rerun; four former false-success cases now reject with child CLI exit 1. Output preserved separately. |
| `.venv/bin/python -m artifacts.technology-navigation.delta-behavior-source-probe` | 0 | Diagnostic completed; child source CLI wrongly accepts both changed and removed project facts with exit 0. This is reproduction, not acceptance PASS. |
| `git diff --check PRIOR_FULL HEAD` | 0 | Delta whitespace check passed. |
| Python exact-substring comparison of both original Full reports against durable combined report | 0 | Both preserved verbatim. |

The reviewer inspected only the confirmed repairs, their canonical/generated
propagation, related fixtures/guide changes, preserved initial reports and direct
regression evidence. Read the independent repaired quality-gate report: 83 tests
in 110.900s, exit 0, plus validators, four compilers, Actionlint and diff check.
Those are attributed to the quality checker, not claimed as this reviewer's runs.
The earlier full 314-test result belongs to its prior head; no full repaired-head
suite is claimed.

Read refreshed explicit-context smoke evidence: 28 selected reads/hashes, required
consumer facts, four effective approved checks, and refusal after project-fact
tampering. That is a consumer fixture and does not cover the remaining source
omission. Native Codex/Copilot discovery, application/language runtimes, PostgreSQL,
native Windows, remote CI and publication were not executed by this reviewer.
No native discovery or human approval is inferred from these checks.

Evidence under `artifacts/technology-navigation/`:

| File | SHA-256 |
| --- | --- |
| `delta-behavior-tests.log` | `adda4630363a9b950a2ad3850cf843aafecbfa94ece83c9c0ba77bc9af11b401` |
| `delta-behavior-consumer-probe.json` | `707784390e0dbb79fd497543e27b2d0889a5be145e95c7862fc64ae00f086d9a` |
| `delta-behavior-source-probe.py` | `5fc8b131a3b917171fcf6e9457719a726609083e58dd718b5cca28d1893d188e` |
| `delta-behavior-source-probe.json` | `3d43a95e8b2f2f58a029c2e69a81c629df3263c4497f2ecaa0838eeea4bfba47` |

The original consumer probe script remains unchanged at its earlier recorded
SHA-256. All diagnostic consumers were temporary and cleaned after execution.

---

# Independent repair Delta B — authority and context

Reviewer: `/root/tech_full_authority`; read-only independent session; 2026-10-14.
Task: `BB-TECH-NAV-008-DELTA-B`.

## Verdict

**CHANGES REQUIRED — TNAV-B-1 / TNAV-S-1 remains partially unresolved in source
mode. TNAV-S-2 is FIXED within the bounded reviewed contract.** Consumer mandatory
project/core context and source core.json are fixed. The source repository's own
existing project.json is still omitted. This is a remaining path of the original
mandatory-context finding, not a new requirement or an expanded trust boundary.

No tracked edits, commits, publication, candidate commands or application checks
were performed. Unchanged Full-review scope was not reopened. The initial Full
reports, deterministic gate and separate triage remain preserved as earlier
snapshot evidence, including their original verdicts and severity difference.

## Identity and scope

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Prior Full head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Repair head: `4722d46e220ee34fb649c787d19f75f77447ca0b`
- Repair tree: `ea5e2b47728d3fea7ba4a217e3ce4ac3a16fc48b`
- Delta SHA-256: `0081f46e538998bcafaa10ba790d63b1bab68a3cce792d6acdc3e3eb74b404f5`
- Full patch SHA-256: `0a576467bdcd34bc9638ef3dfbe16d665297921c627006f12b014ec80775582c`

The reviewer independently verified these identities and clean worktree before
and after checks. Review covered only the two confirmed repairs, generated
propagation, directly affected tests/guide text and preserved review evidence.
The separate triage was read before assessment; the reviewer did not implement
or approve its own repairs.

## TNAV-B-1 / TNAV-S-1 — partial fix; source project facts still omitted

Severity follows separate triage: **P1**. Confidence: high. Category: incomplete
mandatory context / stale handoff.

The consumer additions at `scripts/navigation.py:496-499` correctly include
`.engineering-backbone/project.json` and `.engineering-backbone/core.json` using
existing safe document reads and exact byte hashes. The source addition of
`policy/core.json` at line 494 likewise binds its bytes. Independent probes and
real rendered CLI tests establish presence, unchanged verification, mutation
rejection and removal rejection for these fixed cases.

However, the source arm at `scripts/navigation.py:494-495` still omits the source
repository's **existing** `.engineering-backbone/project.json`. Both upstream
base and this repaired head track that file at blob
`1de5d9f5dfb428f890896c54ce70679c0a348dca`. It contains this project's actual name,
base branch and validation command. The source validator itself reads and
validates it at `scripts/validate.py:2454-2457`; it is not a proposed new consumer
file or invented source contract.

The repair guide at `docs/agent-navigation.md:108-111` and source regression test
at `tests/test_navigation.py:329-334` incorrectly assume no source project file:
the test deletes it and asserts it is absent from the receipt. That assertion
protects the remaining omission. The separate triage's instruction not to invent
a source project.json reflected the same factual layout mistake. That premise
must be corrected explicitly; the original completeness requirement is unchanged.

The root disclosed this layout correction during Delta. This reviewer separately
checked the actual Git object at base/head and the source validator, then ran an
isolated reproduction with the real source project facts copied into a source-mode
active route fixture. Resolve exited 0 while omitting project.json; modifying its
base branch and validation command then verified the old receipt with exit 0;
deleting it also verified with exit 0. Exact three CLI invocations and results
are in `delta-authority-source-project-probe.json`.

Impact remains the original one: a source-mode agent can read every resolved
file yet miss authoritative project facts, and a stale receipt still verifies
after those facts change or disappear. Prior full project validation does not
bind the later receipt to those bytes. Plan steps 4/5 and AC-2/AC-3 remain unmet
for this source path.

Required bounded completion: include the existing project.json in both layouts;
keep source core at policy/core.json and consumer core at the installed path.
Correct the guide and source test to model the actual source layout, assert exact
hash inclusion and valid modification/removal rejection, regenerate the existing
compiled artifacts/fingerprint and obtain a bounded follow-up Delta. Preserve the
current reports and append the factual correction to the triage/evidence chain.
No actual workflow authority or broader execution/authentication system is needed.

## TNAV-S-2 — FIXED

`effective_workflow` uses the full approved definition for existing IDs when an
enabled trusted workflow base applies, retaining candidate definitions for new
IDs. Manifest kind/PR-phase coverage and selected receipt checks now use that same
map. The base manifest validates against its own definitions; enabled-only
activation and active inheritance remain intact. Raw candidate workflows.json
is still included in the document hashes, so a candidate edit invalidates the old
receipt even when effective execution stays unchanged.

Independent isolated CLI probes established:

1. An approved docs ID relabeled migration cannot satisfy PostgreSQL migration
   coverage; an approved maintenance-only dependency ID cannot acquire PR coverage
   from a candidate relabel/phase edit. Both reject with exit 1.
2. Existing approved complete definitions survive candidate changes to kind,
   phases, argv, cwd and timeout. Resolve/verify pass for both an active inherited
   manifest and complete inactive-seed activation, and every selected receipt check
   equals the full definition emitted by actual workflow-kit `prepare`.
3. Changing only a candidate timeout afterward rejects the previous receipt even
   though the effective approved check stays fixed.
4. A genuinely new migration check ID retains its complete candidate definition
   and permits valid resolve/verify under the existing contract.

Preparation was executed to compare definitions; no prepared project check was
run. The fix restores the existing authority rule without changing workflow
preparation, runner ownership or the core catalogs. No direct regression in this
fix was confirmed within the recorded coverage.

## Actual checks and evidence

| Independently executed command/check | Result |
| --- | --- |
| Git head/tree/full/delta identity and status | Exact requested values; clean |
| `.venv/bin/python artifacts/technology-navigation/delta-authority-probes.py` | Exit 0; 24 child CLI calls cover consumer/source-core facts and check authority, including intended rejection exits |
| `.venv/bin/python artifacts/technology-navigation/delta-authority-source-project-probe.py` | Exit 0 means the remaining source omission reproduced; three child resolve/verify calls incorrectly return 0 |
| Seven selected repair unittest methods (exact list in log) | Exit 0; 7 tests in 8.094s, OK |
| `.venv/bin/python scripts/compile_navigation.py --check` | Exit 0 |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | Exit 0 |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | Exit 0; `a64a6c70e9ac9949322ca46a67401d45b9a1486c8f056b80447de5f277e4c9d1` |
| `git diff --check PRIOR_FULL_HEAD HEAD` | Exit 0 |

The initial 24-call script encoded the supplied source-layout assumption and
checked only source core.json. Its positive outcome must not be interpreted as
source project completeness; the separate actual-layout probe above corrects
that limitation. Likewise, the passing source unittest is insufficient while it
asserts omission of an existing authoritative file.

The seven unittest methods exercised five canonical navigation repair cases and
two real Copier/installed CLI cases, including actual workflow preparation parity.
The separate quality-checker report records 83 targeted tests in 110.900s, actual
exit 0, current/predecessor validation, four compilers, Actionlint and diff hygiene.
Those are attributed checker results, not duplicated executions by this reviewer.
The 314-test full result remains attributable only to prior head 6e5758d.

The repaired smoke report records a fresh explicit-context receiver reading all
28 consumer documents, matching all hashes, observing project/core facts and four
approved checks, and rejecting project-fact tampering. It supports the consumer
fix; it does not exercise source project facts. Native provider loading remains
unverified. No new native client, platform, database or application runs, external
publisher re-fetch, remote CI or GitHub operation were performed by this reviewer.

## Probe/log SHA-256

All paths below are relative to `artifacts/technology-navigation/`.

| File | SHA-256 |
| --- | --- |
| `delta-authority-probes.py` | `c761010c12a436f7d142533bdc791009d925e1f27bcd1998e7a4dd1ac52d3a7c` |
| `delta-authority-probes.json` | `11c7cec6d644b83a499c0e0749bf155f08e8a45c6241a412336fd40ca056d8bf` |
| `delta-authority-targeted.log` | `ab681e3be62f08788593e98ac024d78f8d5ec1c7d458753c5797834942311460` |
| `delta-authority-source-project-probe.py` | `deb5aa1d1474a218b64c665f007c50cf9e36c0df269927aca26f32c8b3e01a2f` |
| `delta-authority-source-project-probe.json` | `1e72dad0e7258d4fb7bc60b7234788288614bbdf3c22930a5ccf43f4fa379d8d` |
