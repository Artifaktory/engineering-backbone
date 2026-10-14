# Technology/navigation final functional Delta closure

Both independent reviewers close the remaining required-context finding on the same
frozen source-completion snapshot. The effective-check finding remains closed.
The initial Full reviews, first repair Delta and separate triages are preserved
in their original records; this is the subsequent bounded closure.

---

# Independent source-completion Delta A

Reviewer: `/root/tech_full_behavior` · 2026-10-14 · read-only follow-up Delta.

## Verdict

**TNAV-B-1 / TNAV-S-1: FIXED within the bounded reviewed scope.** The remaining
source project facts now occur automatically in the receipt, and both mutation
and removal reject the old receipt. Consumer behavior remains correct.

**NO CONFIRMED IN-SCOPE FINDINGS** remain in this source-completion Delta.
TNAV-S-2 remains closed: its effective-check helper is unchanged, verified by exact
source comparison. No unchanged Full-review area was reopened. This is a scoped
review conclusion, not human merge/release approval or universal correctness.

## Frozen identities and authority

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`.
- Prior Delta-reviewed head: `4722d46e220ee34fb649c787d19f75f77447ca0b`.
- Source-completion head: `64133a73668a60cd113e7088925542176d6f6a13`.
- Tree: `dd4be86ee35baaaac3162b3a191db0c2ba5b0976`.
- SHA-256 of full-index binary prior-head→head delta:
  `2769a01518fe05412585e37525a3048d7f7074f4a039910a92a4733defdef938`.
- SHA-256 of full-index binary upstream-base→head patch:
  `75215898fe780137f1724fa17497cbd0a4789b1c5bf9c7e8e1f3602b5b2c402d`.
- Packet: `artifacts/technology-navigation/source-delta-a-task.json`.
- Separate triage: `docs/reviews/technology-navigation-delta-triage.md`.

The reviewer independently matched these identities and observed a clean tracked
worktree before and after probes. No tracked files, commits, branch/reference
updates, remote comments or publication actions were performed. Only ignored
review evidence was written.

## Repair assessment

`scripts/navigation.py` now adds the existing
`.engineering-backbone/project.json` to the common required path set before the
source/consumer split. Source core remains `policy/core.json`; consumer core
remains `.engineering-backbone/core.json`. The existing safe-file and exact-byte
hashing machinery applies to all three required paths. The source project facts
themselves are byte-identical to the original upstream base.

The corrected source unit fixture retains the actual project.json and removes
only the consumer-specific core.json. It checks exact hashes, unchanged success,
fact-change rejection, missing-file rejection for resolve and verify, and restored
success for source project/core facts. The new source CLI integration uses actual
repository project.json bytes, verifies inclusion without manifest duplication,
and tests schema-valid branch/validation-command changes and deletion. The shared
guide now describes the actual two layouts without the prior false premise.

The reviewer's unchanged earlier source diagnostic was rerun against this frozen
guard. It now reports project.json and policy/core.json present, resolve/unchanged
verify exit 0, changed-source-facts verify exit 1, and removed-source-facts verify
exit 1. This directly closes the previously reproduced source false successes.

The unchanged original consumer diagnostic was also rerun. Project/core JSON
remain included; ordinary resolve/verify exit 0; both fact mutations and both
file removals reject verification with exit 1. Its result JSON is byte-identical
to the previous successful consumer repair diagnostic, confirming the common
path movement did not alter that observed behavior.

The effective-workflow helper's exact source segment matches the previous head.
Both prior Delta reports are preserved verbatim inside the durable
`technology-navigation-delta-round1.md` record. Separate triage explicitly corrects
the earlier mistaken source-layout premise; historical evidence was not rewritten.

## Independently executed evidence

Five named tests ran with `.venv/bin/python -m unittest … -v`:

1. `tests.test_navigation.NavigationTests.test_source_core_and_existing_project_facts_are_required`
2. `tests.test_navigation.NavigationTests.test_required_consumer_core_and_project_facts_bind_exact_bytes`
3. `tests.test_navigation.NavigationTests.test_legacy_absence_and_inactive_seed`
4. `tests.test_navigation_integration.NavigationCopierIntegrationTests.test_source_cli_binds_existing_project_facts`
5. `tests.test_navigation_integration.NavigationCopierIntegrationTests.test_installed_cli_binds_mandatory_project_and_core_facts`

**Result: 5 tests in 8.701s, OK, actual exit 0.** No project check commands were
executed. These are the directly affected source/consumer and compatibility cases;
the unchanged 83-test repair suite and whole suite were not repeated by this reviewer.

Other actual commands/checks:

| Command/check | Result |
| --- | --- |
| `git status --porcelain`, `git rev-parse HEAD HEAD^{tree}`, both full-index binary diff digests | Exit 0; exact frozen identity and clean tracked tree. |
| `.venv/bin/python -m artifacts.technology-navigation.delta-behavior-source-probe` | Exit 0; diagnostic completed, relevant negative child verifications exit 1 as required. |
| `.venv/bin/python -m artifacts.technology-navigation.review-behavior-probe` | Exit 0; consumer diagnostic completed with all four negative child verifications rejecting. |
| AST source-segment equality for `effective_workflow` vs prior head | Exact equality. |
| Upstream-base project.json bytes vs current file | Exact equality. |
| Both prior Delta report texts vs durable combined report | Both preserved verbatim. |
| `git diff --check PRIOR_DELTA HEAD` | Exit 0. |

An initial record-preservation inspection used the wrong proposed report filename
and raised FileNotFoundError after the helper/facts equality assertions. After
listing actual review filenames, the corrected standalone inspection completed
successfully against `technology-navigation-delta-round1.md`. This was an evidence
lookup error, not a product failure; no failed inspection is represented as PASS.

## Coverage, provenance and limits

Reviewed the bounded canonical change, corrected source fixture and guide, new
compiled CLI regression and directly related generated propagation. The supplied
independent quality-checker result reports 36 affected tests in 65.483s with exit 0,
current/predecessor validation, four compiler checks, Actionlint and diff hygiene.
Those gate executions belong to the quality checker; the independent executions
above are this reviewer's evidence. Earlier Full and first-Delta results retain
their original snapshots; this is not a claim of a whole-suite run at this head.

Read `artifacts/navigation-source-followup-smoke/report.md`. It explicitly records
a continuation by the prior fresh receiver: 28 hash checks, 27 prior full reads
reused only after byte equality, and a full reread of the changed guide. Updated
receipt verification succeeds and the old receipt rejects. This is a consumer
guide-propagation continuation, not a new fresh 28-document smoke or source-layout
execution. The source behavior is established by the bounded executable probes
and tests above. Native Codex/Copilot discovery remains unverified.

No application language/runtime matrix, PostgreSQL server, native Windows,
remote CI, PR publication, merge, release or downstream adoption was executed in
this reviewer session. No new human-only intermediate gate is introduced.

Evidence under `artifacts/technology-navigation/`:

| File | SHA-256 |
| --- | --- |
| `source-delta-behavior-tests.log` | `a4e86b6f58e63a2f889913aad45db28f4fb021bb7b1789475452ed1d82392d9d` |
| `source-delta-behavior-source-probe.json` | `eb50694fad0e21cb5cf6fcc8976ade252bbd30a863e3c419b69cd08983aeb0f9` |
| `source-delta-behavior-consumer-probe.json` | `707784390e0dbb79fd497543e27b2d0889a5be145e95c7862fc64ae00f086d9a` |

Both probe scripts were reused unchanged from their earlier recorded versions.
Temporary diagnostic consumers were cleaned after use; prior probe results remain
preserved separately.

---

# Independent source-completion Delta B

Reviewer: `/root/tech_full_authority`; read-only independent session; 2026-10-14.
Task: `BB-TECH-NAV-008-SOURCE-DELTA-B`.

## Verdict

**FIXED — remaining TNAV-B-1 / TNAV-S-1 source project-facts omission is closed
within the bounded reviewed scope. NO CONFIRMED IN-SCOPE FINDINGS.** The earlier
consumer/core portions remain fixed. TNAV-S-2 stays closed: its effective-check
helper is byte-identical to the prior independently reviewed repair, and this
follow-up does not alter its execution authority.

This is a scoped independent Delta conclusion, not human merge/release approval,
universal correctness, native-provider discovery or certification. No tracked
edits, commits, publication or project check execution were performed. Unchanged
Full-review areas were not reopened.

## Frozen identity

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Prior Delta head: `4722d46e220ee34fb649c787d19f75f77447ca0b`
- Source-completion head: `64133a73668a60cd113e7088925542176d6f6a13`
- Tree: `dd4be86ee35baaaac3162b3a191db0c2ba5b0976`
- Delta SHA-256: `2769a01518fe05412585e37525a3048d7f7074f4a039910a92a4733defdef938`
- Full patch SHA-256: `75215898fe780137f1724fa17497cbd0a4789b1c5bf9c7e8e1f3602b5b2c402d`

All identities and the clean tracked worktree were independently checked. The
separate first-repair Delta triage and this scoped reviewer packet were read before
assessment. Earlier Full/Delta reports and their factual error are retained; the
new triage explicitly corrects the source-layout premise instead of rewriting it.

## Finding closure and direct regression assessment

The existing `.engineering-backbone/project.json` is now in the common mandatory
path set for both layouts. Source mode additionally binds `policy/core.json`;
consumer mode retains `.engineering-backbone/core.json`. Existing safe document
reads and exact byte hashing apply uniformly. No new policy/facts file was invented
or modified: Git comparison confirms source project.json, policy/core.json and
policy/core.md are unchanged from the previous reviewed head.

The guide now states the actual layout. The source unit fixture retains existing
project facts, removes only consumer core.json, and checks both required source
JSON hashes, valid changes, deletion through resolve/verify and restored-byte
success. The new compiled source CLI test uses the actual repository project.json
bytes, with no manual route duplication. The already-fixed consumer case remains
covered after moving project.json into the common set.

An independent isolated probe constructed a source-layout route using the actual
repository project facts and the frozen compiled CLI. Seven child CLI calls proved:

1. Resolve succeeds with the exact source project and core hashes, without the
   consumer core.json path in the source receipt.
2. Unchanged receipt verification succeeds.
3. Changing only base_branch rejects the old receipt with exit 1.
4. Changing only validation_command rejects the old receipt with exit 1.
5. Deleting project.json rejects both resolve and verify with exit 1.
6. Restoring its original bytes restores successful verification.

The probe separately compared the exact `effective_workflow` function source span
with the prior Delta head and found it byte-identical. The canonical diff contains
only the required common-path move; no check-definition, activation, inheritance,
execution or runner behavior was changed. Generated compiler checks confirm that
the same bounded repair propagates through quality guard, validator and workflow.
No direct regression was confirmed.

## Independently executed checks

| Command/check | Actual result |
| --- | --- |
| Git head/tree/delta/full-patch identity, protected source facts comparison and worktree status | Exit 0; exact frozen identities, unchanged facts/policy and clean tree |
| `.venv/bin/python artifacts/technology-navigation/source-delta-authority-probe.py` | Exit 0; seven CLI assertions, exact hashes and unchanged effective helper |
| Four named source/consumer unit and installed CLI tests | Exit 0; 4 tests in 6.194s, OK |
| `.venv/bin/python scripts/compile_navigation.py --check` | Exit 0 |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | Exit 0 |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | Exit 0; `e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450` |
| `git diff --check PRIOR_DELTA_HEAD HEAD` | Exit 0 |

Named tests: `test_source_core_and_existing_project_facts_are_required`,
`test_required_consumer_core_and_project_facts_bind_exact_bytes`,
`test_source_cli_binds_existing_project_facts`, and
`test_installed_cli_binds_mandatory_project_and_core_facts`. Their complete module
and class names appear in `source-delta-authority-targeted.log`.

The independent quality-gate report was read and is separate evidence: 36 affected
tests in 65.483s, actual exit 0; current/predecessor validators; four compilers;
Actionlint and diff hygiene. Those broader executions are attributed to the quality
checker, not claimed as duplicated reviewer runs. Prior 314-test and 83-test runs
retain their earlier snapshots and are not relabeled as final-head full-suite runs.

## Boundaries and preserved evidence

The follow-up consumer smoke report was read. It accurately records the same
receiver verifying 28 current hashes, retaining 27 prior reads after byte equality,
and rereading the changed guide. Positive verification and stale-receipt rejection
are recorded separately. It is not a new fresh 28-document run or source-layout
execution proof; the independent source CLI probe/tests above cover the source path.
Native Codex/Copilot discovery remains unverified.

No complete suite, repeated S2 authority matrix, application/database/platform
runtime, native client, external publisher re-fetch, remote CI or GitHub operation
was performed in this Delta. Its scope is the confirmed residual and its direct
regressions. Publication identity, remote CI and requested Codex review remain
subsequent task steps; human merge/release authorization remains separate.

## Evidence SHA-256

All paths below are relative to `artifacts/technology-navigation/`.

| File | SHA-256 |
| --- | --- |
| `source-delta-authority-probe.py` | `9b6fbbf29040366bdbca3a96416086023bfe0e56286a00264b959a1f90e7b96b` |
| `source-delta-authority-probe.json` | `2c8dd97ed09a57f86cacd9eeac1962bec40fda3cfbd0153bf9bd90f89dd1eec6` |
| `source-delta-authority-targeted.log` | `bf69ff85cce6a423292442101375f27bf3e8eceae37004b995b9cf825c4021a1` |
