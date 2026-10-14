# Technology/navigation local closeout

The functional implementation, deterministic checks and independent review chain
are complete. No confirmed findings remain open within the reviewed scope.
Publication, observed GitHub CI and the requested advisory Codex review are pending
at this prepublication evidence snapshot. Their actual identities/statuses will be
recorded in the PR discussion; no local result predicts an external outcome.

Functional reviewed head: `64133a73668a60cd113e7088925542176d6f6a13`, tree
`dd4be86ee35baaaac3162b3a191db0c2ba5b0976`; upstream base
`edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`; full-index binary patch SHA-256
`75215898fe780137f1724fa17497cbd0a4789b1c5bf9c7e8e1f3602b5b2c402d`.
The Task Packet points to that functional reviewed head. The final commit adds
only closeout evidence and Task Packet status; it receives a separate bounded
read-only evidence Delta before publication. Actual final commit/tree/patch and
that evidence Delta belong in the PR record, avoiding self-referential commit IDs.

## Acceptance and evidence

| Acceptance | Result and evidence |
| --- | --- |
| AC-1 | PASS: 28 technology profiles, 28 organization-owned mandatory rules and 38 source entries; [guidance](../quality/technology-profiles.md), [bounded provenance](../quality/technology-source-provenance.md) and [Full review](technology-navigation-full-review.md). PowerShell, Bash and PostgreSQL are included; MUST, SHOULD and free decisions are distinct. |
| AC-2 | PASS: role/task/component routes, complete mandatory source/consumer facts, safe document paths and actual effective check definitions; [final checks](technology-navigation-final-checks.md) and [independent closure](technology-navigation-delta-review.md). |
| AC-3 | PASS: stale/incomplete/altered context rejection, inherited restrictions, source/consumer facts and check-definition authority; [initial receiver smoke](technology-navigation-smoke.md), [final continuation](technology-navigation-smoke-followup.md) and [Delta closure](technology-navigation-delta-review.md). |
| AC-4 | PASS: real Copier provider combinations, optional inactive/legacy compatibility, local-file preservation and actual upgrades; [initial](technology-navigation-checks.md), [repair](technology-navigation-repair-checks.md) and [final checks](technology-navigation-final-checks.md). Native client discovery remains separately unverified. |
| AC-5 | PASS within the recorded staged verification: full 314-test run on the initial Full head, 83 affected tests after the first repair, then 36 tests after the bounded source completion. Validators, four compilers, Actionlint and diff hygiene passed at the final functional head. Counts are separate runs, not a combined unique-test claim or a final-head full-suite claim. |
| AC-6 | PASS: [independent plan](technology-navigation-plan-review.md), two [Full reviews](technology-navigation-full-review.md), [separate triage](technology-navigation-triage.md), two [first repair Deltas](technology-navigation-delta-round1.md), [corrected Delta triage](technology-navigation-delta-triage.md) and two [closure Deltas](technology-navigation-delta-review.md). |
| AC-7 | PENDING here: publish the exact final identity, inspect actual CI, request Codex review and record visible trigger/result and any pending external status in the PR. |

## Findings and preserved history

The preparatory workflow-test harness exceeded the host's single-argument limit
after the trusted payload grew. It now executes the same payload from a temporary
script instead of `bash -c`; assertions and gates remain intact. The known merged
predecessor fingerprint was added to the expected set, without admitting interim
unreleased fingerprints. The complete suite subsequently exercised these paths.

QG-001 / TQ-1 was a source fixture missing the new extension. Its minimal repair
retained missing-extension and original-authority poisoning rejection; the first
complete failing run and later passing result remain separately recorded.

Full findings TNAV-B-1 / TNAV-S-1 described the same required-project/core omission;
TNAV-S-2 described candidate check definitions diverging from approved workflow
preparation. Separate triage preceded both repairs. First repair Deltas closed
TNAV-S-2 but found that the source repository already had project.json, contrary
to the earlier layout assumption. The corrected triage owns that error, preserves
the prior records and authorizes the bounded source counterpart fix. Both final
Delta reviewers close TNAV-B-1 / TNAV-S-1; the effective-check helper is unchanged.

The original core catalogs, source project/core facts, dependency locks and
historical fixtures remain unchanged. Projects select relevant components and
profiles explicitly; this change does not install every language toolchain or
activate navigation in downstream projects automatically.

## Practical limits and recovery

Receipts provide structural integrity and explicit context, not authenticated Git
identity, semantic approval or proof that a native provider loaded instructions.
The fresh receiver actually read 28 documents; the final continuation verified
all 28 hashes, reused 27 unchanged prior reads and reread the changed guide.
Native Codex startup produced no model events before timeout; nested native and
Copilot discovery were not executed. No application runtime matrix, real PostgreSQL
server, native Windows or downstream deployment is claimed by these fixture tests.
Source editions are bounded references, not blanket standard adoption/certification.
Actionlint's optional external ShellCheck/Pyflakes integrations were not executed.

No hosting protection, human approval, release, deployment or downstream adoption
is established here. Human merge/release approval and stronger local controls
remain binding. Recovery is a reviewed revert or explicit project pin/configuration
migration; no automatic downstream application is introduced.
