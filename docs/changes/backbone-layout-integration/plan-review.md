# BB-LAYOUT-014 independent plan review

Decision: **APPROVED FOR THE RECORDED IMPLEMENTATION SCOPE**. No confirmed
in-scope plan blocker remains. This is independent plan advice, not implementation
verification, publication approval, human merge approval or release authorization.

Reviewer responsibility: independent plan reviewer. The reviewer did not author
the plan, implement the runtime/tests, or modify either reviewed planning file.
Only this review record was written.

## Reviewed identity and context

- Starting PR18 head: `f1c1410cff6407109f286173f1ecc980cd2a14b7`.
- Actual merged main: `537576f658bbd79c3bc49b26ade948116c664943`.
- Main parents: `212608aa50ee517b3dd3107a9480da997222fd4f` and
  `fc707a8d51981d52445c2176711154dfd26145aa`.
- Common ancestor: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Reviewed [plan](plan.md) SHA256:
  `3a865abe86c39422696c6b0b1b4006307facd14779d1e73516cc8eaeeff94cba`.
- Reviewed [Task Packet](task-packet.json) SHA256:
  `4287287df9b2b321fe2a47ddf7024fd7fb4b56b45a41605e87cab3cbdfea3e64`.

Read root AGENTS, CONTRIBUTING, the canonical governance policy, applicable
documentation/governance instructions, the Task Packet schema, the proposed plan
and packet, and the separate initial triage including all three confirmed IDs.
The triage report was read from
`/tmp/backbone-layout-integration-initial-triage.md` before its retention in this
delivery. No active source navigation seed was present. The reviewed amendment
includes the returned PR18 Codex findings; the earlier draft was not approved as
an implementation gate before this amendment.

## Assessment

The task is properly bounded to the existing PR18 conflict repair and directly
related confirmed findings. It records the real human-merged prerequisite and
requires a normal two-parent integration without force pushing or merging PR18.
The additional authority code is reviewed main code relocated to its intended
source path, not a candidate-controlled replacement for the trusted-base check.

The runtime plan preserves separate candidate/base layout selection, executable
source identity, four canonical policy files, schema and permission floors, and
old-source/consumer contracts. Regeneration uses the canonical maintenance tools.
Only the measured main current fingerprint may join the existing approved
predecessors; arbitrary intermediate identities remain excluded.

The history plan keeps the original 495-path mapping and 88-entry archive
authority unchanged. Incoming prerequisite records retain their exact bytes and
internal relative-link topology under the new compatibility delivery. Their
ordinary validation does not depend on a new candidate-only exemption. Existing
two ZIP fixtures and their manifest remain byte-identical; the new exact main
fixture uses a separate verified manifest. Existing assertion coverage and real
Copier updates are explicitly preserved.

The separately confirmed repairs have concrete behavior-level checks:

| Finding | Planned verification |
| --- | --- |
| INT-ARCHIVE-01 | Executable-owned required archive completeness; missing file/directory and linked replacements reject; intact archive succeeds; candidate map cannot waive the requirement. |
| INT-ARCHIVE-02 | Fresh real Git checkout with `core.autocrlf=true`; actual archive hashes and validator result checked; committed archive bytes and nested historical fixture attributes unchanged. |
| INT-NAV-01 | Current root instructions and navigation resolve the BB-LAYOUT-014 packet/plan; historical records keep their original task references. |

The real main validator's positive transition check and the candidate's negative
archive-completeness evidence remain separate. Main still contains the confirmed
deletion blind spot until a human merges its repair; a main PASS cannot certify
that fix. The plan states this limitation explicitly.

All eight acceptance criteria map to actual evidence or explicit pending states.
Targeted and complete deterministic checks precede frozen behavior/security Full
reviews. Separate triage, bounded repair/Delta, two Full rounds, six implementation
iterations, current-main freshness, final committed diffs after evidence commits,
remote tree/patch/parent readback, and actual current-head CI/review observation
are required. Local container/native limitations are not substituted with old-head
results. No gate, dependency version, native permission or external repository is
silently changed.

## Executed plan checks and limits

Using the unchanged isolated Python environment, JSON Schema Draft 2020-12
validation of the final packet against the tracked task schema completed with
exit 0. SHA256 calculation bound the final amended files above. Read-only
`git show`, `git merge-base`, and `git branch --show-current` completed with exit 0
and confirmed the recorded merge ancestry and existing PR branch.

No runtime tests, implementation review, repaired Windows checkout, new remote CI
or integration merge was executed by this plan reviewer. Those remain required
implementation/quality/review evidence. Any later scope or trust-boundary change
requires updated independent planning and the applicable Full review; this
decision does not waive the recorded stop conditions.
