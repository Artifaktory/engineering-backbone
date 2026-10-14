# Separate first-repair Delta triage

Task: `BB-TECH-NAV-008` · Triager: `/root/tech_findings_triage` · 2026-10-14.
Separate triage began after both first-repair Delta reports completed. No tracked
edits, implementation, Full/Delta reviewer role, commits or GitHub writes were
performed by this session. The original Full reports and triage remain preserved.

## Verdict

**TNAV-S-2 is FIXED within the reviewed scope. TNAV-B-1 / TNAV-S-1 remains OPEN,
P1, for the source layout's existing project facts file.** Its consumer project/core
and source core.json portions are fixed. Complete the bounded source-facts repair
below, verify the directly affected paths and obtain a follow-up independent Delta.
This restores the already approved complete-context contract; it does not require
a new Full round, policy file, requirement or human intermediate decision.

## Reviewed identities

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Prior Full head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- First repair head: `4722d46e220ee34fb649c787d19f75f77447ca0b`
- First repair tree: `ea5e2b47728d3fea7ba4a217e3ce4ac3a16fc48b`
- First repair delta SHA-256: `0081f46e538998bcafaa10ba790d63b1bab68a3cce792d6acdc3e3eb74b404f5`
- Full patch SHA-256: `0a576467bdcd34bc9638ef3dfbe16d665297921c627006f12b014ec80775582c`

The triager independently checked head, tree, repair delta and clean tracked
worktree; both Delta reports bind this same snapshot. Earlier complete/targeted
test results retain their own heads and are not relabeled as follow-up results.

## Explicit correction of the prior triage premise

The original triage said not to invent a source project.json and described source
facts as supplied by the Task Packet/contribution route. That direction rested on
an incorrect assumption that the source layout lacked project.json. I did not
verify that assumption before the original triage. It was wrong.

Both the original upstream base and the first repair head already track
`.engineering-backbone/project.json` at unchanged blob
`1de5d9f5dfb428f890896c54ce70679c0a348dca`. It contains the source repository's actual
name, base branch, validation command, language and adapter choices. Source
`scripts/validate.py:2454-2458` loads/validates that file and uses it for adapter
validation. It is an existing authoritative source fact file, not a new consumer
requirement. Task Packet/contribution facts cannot bind its distinct bytes.

Preserve the prior reports and triage as history, including the incorrect premise.
This report explicitly corrects it. Do not silently rewrite the original record
or present the first repair's source test as proof of complete source facts.

## Findings after both independent Deltas

| Retained IDs | Classification | Evidence and remaining scope |
| --- | --- | --- |
| `TNAV-B-1`, `TNAV-S-1` | Confirmed, partially repaired; source project facts remain open P1 | Consumer project/core files and source policy/core.json are bound. Existing source project.json is still absent from the receipt. |
| `TNAV-S-2` | Fixed within bounded reviewed contract | Both independent Deltas confirm approved definition substitution, phase/kind coverage, full prepared-definition parity, activation/inheritance, candidate hash invalidation and genuinely new IDs. |

The source resolver arm at `scripts/navigation.py:494-499` omits project.json.
The new test at `tests/test_navigation.py:319-344` deletes that existing file and
asserts omission, and the guide at `docs/agent-navigation.md:108-111` repeats the
incorrect layout premise. These are residual/direct-repair portions of the same
confirmed context finding, not new unrelated defects or expanded Full scope.

The triager independently ran the behavior reviewer's isolated source probe, using
a real Copier-rendered fixture mapped into the source layout and actual repository
project.json bytes. Source resolve and unchanged verify returned 0; policy/core.json
was present while project.json was absent. Changing source base_branch and
validation_command still verified the prior receipt with 0; deleting project.json
also verified with 0. This reproduces the remaining AC-2/AC-3 violation. It does not
claim the separate full project validator accepts deletion or that receipt hashes
authenticate Git identity.

For TNAV-S-2, the triager inspected `effective_workflow`, its candidate/base manifest
call sites and receipt selection, and read both independent executed Delta evidence
sets. Full approved objects replace existing IDs; base validation uses its own
definitions; complete-seed and inherited-active cases are covered. The repair
preserves the candidate workflow document hash. No conflicting result or remaining
direct defect was found in the recorded scope. Its tests need not be repeatedly
rerun for an unchanged helper during a source-path-only follow-up.

## Authorized bounded completion

1. Include existing `.engineering-backbone/project.json` in both source and consumer
   mandatory contexts using the existing safe document/hash mechanism. Keep source
   core at `policy/core.json` and consumer core at `.engineering-backbone/core.json`.
   Do not create or change the existing project facts/policy files themselves.
2. Correct the source test to model the actual tracked layout. Assert exact hashes
   for source project.json and policy/core.json, normal unchanged verification,
   rejection after valid fact changes, rejection after deletion, and restored-byte
   success. The consumer core.json path need not be invented in the source layout.
3. Add or extend one compiled CLI/source integration regression using real source
   project.json bytes. It must establish inclusion, exact hash, unchanged success,
   valid branch/validation-command mutation rejection and removal rejection.
4. Correct the source/consumer mapping in the shared guide and any generated copy.
   Regenerate the existing navigation/quality/fingerprint artifacts in normal order;
   preserve original catalog identity, previous fingerprints and existing gates.
5. Preserve both first-repair Delta reports and append this factual correction to
   durable review evidence. Do not rewrite historical PASS results or initial claims.

## Narrow verification and follow-up Delta

Required executable coverage is the corrected source unit, new source compiled-CLI
case, and the already-fixed consumer mandatory-facts case to guard common path-set
regression. Existing source core mutation/removal and legacy/inactive checks should
remain valid. Prefer named relevant methods or the small affected navigation module
where convenient; do not mechanically rerun all 83 prior repair tests or the full
suite for this one added mandatory source path.

Run compiler equality checks and current/predecessor validation after regeneration,
plus workflow syntax and diff hygiene for the generated workflow/fingerprint delta.
Check source/template guide propagation. Reuse prior effective-check and consumer
smoke evidence where the follow-up leaves those semantic paths unchanged, clearly
attributing it to the earlier head/guard. Do not claim a new native-client or fresh
smoke execution unless it actually occurs. Broaden checks only if the actual repair
introduces another concrete risk or an existing gate requires it.

Freeze the follow-up head and delta from `4722d46e220ee34fb649c787d19f75f77447ca0b`.
Independent Delta should assess closure of TNAV-B-1/TNAV-S-1 on the source path and
directly introduced regressions. TNAV-S-2 stays closed unless the follow-up touches
its effective-check behavior. No unchanged Full areas should be reopened. The
corrected factual premise does not change the existing plan or trust boundary.

Publication closeout remains blocked by the source-facts residual until its repair,
relevant checks and independent follow-up Delta pass. Human merge/release remains
separate; native discovery remains explicitly unverified. No human policy decision
is outstanding for this bounded completion.

## Actual triage evidence

Read both completed first-repair Delta reports, checked the tracked base/head
project blob and source validator, inspected the corrected resolver/helper/test/
guide delta, and independently executed:

```sh
.venv/bin/python -m artifacts.technology-navigation.delta-behavior-source-probe \
  > artifacts/technology-navigation/delta-triage-source-probe.json
```

Exit 0 means the diagnostic completed; its four child CLI operations expose the
remaining false-success behavior. The expected temporary Copier warning reported
an absent fixture answers file; the probe still produced the complete results.
No application checks, full suite, native client or remote operation was executed.

| Evidence file | SHA-256 |
| --- | --- |
| `delta-review-behavior.md` | `76aabeba47e82ab3baec8afe0c10dc39e79b0a4119f8704bbb7a310523d89641` |
| `delta-review-authority.md` | `3355749adadb93dbff393ff81db093257110e2cc3a2cd2d25ab8944753b1390d` |
| `delta-triage-source-probe.json` | `3d43a95e8b2f2f58a029c2e69a81c629df3263c4497f2ecaa0838eeea4bfba47` |

Evidence paths are relative to `artifacts/technology-navigation/`. Only this
ignored report and the ignored triage probe result were written by this session.
