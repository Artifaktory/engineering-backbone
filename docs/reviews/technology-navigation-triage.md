# Separate Full-review finding triage

Task: `BB-TECH-NAV-008` · Triager: `/root/tech_findings_triage` · 2026-10-14.
This session performed triage only, after both independent Full reports completed.
It did not implement, act as either Full reviewer, edit tracked files or write to
GitHub. Separate triage is required by the existing policy; human approval remains
required for merge/release, not for these already authorized bounded repairs.

## Verdict and frozen identity

**CHANGES REQUIRED. Two distinct confirmed P1 findings block publication closeout.**
Repair the bounded defects below, run relevant checks, freeze the repaired snapshot
and obtain independent Delta review. No finding requires a new requirement, human
policy decision or changed trust boundary. No additional Full round is necessary
if the repairs stay within these bounds.

- Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Reviewed head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Reviewed tree: `b2bf7b72f878033eafb2d2da4eaa0425fcbdd266`
- Full patch SHA-256: `f214df661b5d168208e69a90b063cda3b07feb33591bfb71a15dfbdcd761324c`

The triager independently matched head/tree/patch and observed a clean tracked
worktree before and after inspection/probes. Both Full reports bind these same
identities. The preceding deterministic gate reports 314 tests passing; it does
not resolve either semantic defect found afterward.

## Classification

| Review IDs | Decision | Severity | Repair scope |
| --- | --- | --- | --- |
| `TNAV-B-1`, `TNAV-S-1` | Confirmed; duplicate reports of one omission, retain both IDs | P1 | Automatically include existing mandatory project/core JSON documents in the context |
| `TNAV-S-2` | Confirmed; distinct authority mismatch | P1 | Use effective approved workflow check definitions for technology coverage and receipt checks |

There are no rejected findings and no unresolved human-decision classifications.
The context omission is treated as P1 for this delivery because ordinary active
consumer handoffs can omit authoritative branch/validation facts and still verify
after those facts disappear or change. The authority reviewer assigned P2 and the
behavior reviewer P1; both reported the same reproduced defect. This classification
does not claim the full governance validator permits weakened core invariants.

## TNAV-B-1 / TNAV-S-1 — required context

Confirmed by the automatic path set at `scripts/navigation.py:460-472`, the existing
project-facts operating contract, both independent reproductions, and the triager's
own rerun of the isolated authority probe against the unchanged frozen CLI.
Resolve succeeds while project.json/core.json are absent from `documents`; project
branch/validation-command changes, core changes and removal of both files each
leave verification of the old receipt successful. This directly violates plan
design steps 4/5 and AC-2/AC-3. A separate earlier project validation cannot hash
bind otherwise valid fact changes into a later receipt.

Minimal repair:

1. Add `.engineering-backbone/project.json` and `.engineering-backbone/core.json`
   to the mandatory consumer context, using existing path, regular-file and byte
   hash validation. These files must not depend on manual manifest duplication.
2. Add the applicable source `policy/core.json`. Keep source and consumer layouts
   explicit; do not invent a source project.json. Clarify the existing source
   project-facts route in the guide if needed, using the existing Task Packet and
   contribution instructions rather than adding a new facts contract.
3. Update only directly affected fixtures/docs and regenerate the existing compiled
   guards/workflow/fingerprint through their normal compiler chain. Preserve prior
   fingerprint history and legacy/inactive navigation behavior.

Required regression bounds: an active real rendered consumer includes both JSON
paths with exact hashes without manual mapping; unchanged verify passes; mutation
of each rejects the old receipt; removal of each rejects resolution/verification.
Exercise the source core.json counterpart. Cover canonical resolver and installed
CLI through focused unit/integration checks. Retain absence/inactive compatibility.
Refresh the explicit-context smoke receipt/receiver evidence for the newly required
documents; preserve the old smoke as earlier-snapshot evidence and continue to mark
native provider discovery unverified.

## TNAV-S-2 — effective approved check definitions

Confirmed by `scripts/navigation.py:229-279,451-452,534`, the existing approved
substitution in `quality_framework.py:933-950` and `workflow_kit.py:227-237`, and the
triager's independent isolated probe rerun. The approved base contains an existing
`reserved` docs check. The candidate relabels that same ID as migration and uses it
to satisfy a new PostgreSQL rule. Resolve/verify both return 0, but approved workflow
preparation retains the docs definition and produces zero migration-kind checks.
The receipt reports the candidate migration command while execution preparation
reports the approved docs command. No application command was executed.

This is introduced by the new navigation coverage/receipt path and conflicts with
the existing trusted workflow authority. It is not a demand to determine semantic
test adequacy or a new prohibition on candidate-owned, genuinely new check IDs.

Minimal repair:

1. When a trusted workflow base applies, construct effective definitions according
   to the existing execution contract: existing IDs use the complete approved base
   definition; genuinely new IDs retain the established candidate behavior.
2. Use the same effective definitions for technology binding existence, PR-phase
   and required-kind coverage, and the receipt's selected `checks`. Do not inspect
   candidate command text as proof of coverage and do not execute it.
3. Validate the trusted base's own manifest against its own definitions and retain
   complete inactive-seed/enabled-only activation and active inheritance checks.
   Preserve full candidate configuration/document hashing, so candidate edits still
   invalidate a prior receipt even when they do not change effective execution.
4. Update directly related guide text/tests and regenerate through the existing
   compiler chain. Do not change workflow preparation, runner authority, old core
   catalogs or required gates to accommodate the candidate definitions.

Required regression bounds:

- Existing approved docs ID relabeled migration cannot satisfy a new PostgreSQL
  migration requirement; similarly, candidate PR-phase additions cannot grant an
  approved non-PR check PR coverage.
- Approved coverage remains valid if a candidate changes the existing check's kind,
  phase or command; the emitted definition must equal the approved prepared one.
  Include complete definition fields, not only kind/argv.
- A genuinely new check ID follows the existing workflow contract; normal unchanged
  trusted-base resolution and enabled-only activation still work.
- Exercise canonical navigation, the compiled guard and an installed CLI. Compare
  selected receipt definitions with `workflow_kit.py prepare` output without running
  project commands. Cover both an already active inherited manifest and activation.

## Verification and Delta boundary

After the repairs, run the affected navigation/catalog/integration and quality
authority/workflow checks, current and predecessor validation, all compiler checks,
workflow syntax and diff hygiene. Check the generated consumer propagation and
upgrade/activation paths touched by the fixes. The prior full 314-test result is
valid evidence for its frozen head; do not relabel it as a repaired-head full run.
Use meaningful targeted repaired-head evidence and any broader run required by the
existing project gate. No unchanged whole-suite rerun is demanded merely to repeat
the old evidence; broaden testing when the actual repaired delta creates a concrete
remaining regression risk.

Delta must bind the prior reviewed head above, repaired head, exact delta digest,
and all three retained IDs. It must check both confirmed repairs and directly
introduced regressions. Adding existing mandatory files and applying already
approved execution definitions restores the approved contract, so this is a bounded
Delta rather than a new trust-boundary design. New requirements or changes to the
actual workflow execution authority would instead require a newly scoped Full.

Outstanding blockers: both findings remain unfixed at this triage snapshot; their
repair checks and independent Delta remain pending. Native discovery remains an
explicit limitation, not a newly raised blocking finding. PR/CI/Codex review remain
later authorized steps. Triage is not merge, release or downstream-adoption approval.

## Actual triage evidence

Read AGENTS.md, both core policy files, CONTRIBUTING.md, approved plan/task, quality
gate and both Full reports. Inspected the bounded canonical code and guide paths
above, then independently reran the authority diagnostic in temporary directories.
The script source was executed unchanged except its evidence output filename was
redirected to `full-triage-probes.json`, preserving the reviewer evidence. Probe
exit 0 means both defect assertions reproduced, not a repaired behavior PASS.
Its eight child CLI operations all exited 0; the last prepared configuration and
receipt have the asserted docs/migration mismatch. No tracked files were changed.

| Evidence file | SHA-256 |
| --- | --- |
| `full-review-behavior.md` | `6b33c42f3a59478d840cf9a5a981ab0cfa1b1102c85c842f6ac61c8766dd7d82` |
| `full-review-authority.md` | `eaa4d83f67b724cdaf1d75a9844644d0b0f7dd68d5870c2ea2d2bfa8c30d76ce` |
| `full-triage-probes.json` | `01d81b6b02ce3af92c6e65c90d374afe72f00efd3ca1e9864390c4ebbf5baa93` |

All paths in this evidence table are relative to
`artifacts/technology-navigation/`. No full suite, native client, remote CI or
external publisher re-fetch was performed by this triage session.
