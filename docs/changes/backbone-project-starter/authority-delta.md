# Scoped authority Delta

Independent reviewer: `starter_authority_full`, with read-only environment
auxiliary. Prior Full `f0230d0da90b17ef52932ff027529acd23d73f51`; repaired head
`bb794a6b05e35f168ee90d4dcbe5055f674eeead`; tree
`b96337072a048afa37eee2135f3fafeaa76f8782`.
Full-to-repair binary patch SHA256
`1913af276440e84684ec4e7bae5787f8b46ac9687732576af684e0690894de46`;
actual base `4e74c7e5f3a07430768f670c4271c1e1a0e28f68` to repair SHA256
`fba134f81573d5100933bf63a2df6ac169c6ab8d34c90df1b86e9cd6b0abbfc9`.
Both digests, head/tree, committed whitespace and clean tracked state independently
matched. Review began after the new complete independent quality PASS.

**START-AUTH-01/02 resolved. NO CONFIRMED IN-SCOPE FINDINGS in the repairs or
their direct regressions.**

| Finding | Independent proof |
| --- | --- |
| START-AUTH-01, P2 | Source/project overlap is checked before `old_plan()` launches a descriptor. The real nested Git descriptor is refused without its marker or project writes; ordinary external trusted-source comparison passes. |
| START-AUTH-02, P2 | Starter root/ancestor/file paths reject symbolic links and junctions, with resolved containment before reads/writes. Environment roots/inputs likewise reject junctions and enforce strict resolved containment before input reads. Modeled alias/escape negatives and ordinary-path controls pass. |

Seven focused starter/integration tests passed: five tests in 4.081 seconds, then
two tests in 5.854 seconds, both exit 0. Coverage includes nested descriptor
nonexecution, junction root/read/write refusal, ordinary three-way comparison,
neutral export, overwrite/link/traversal refusal, nested/dangling governed aliases
and trusted cross-field floor integration. Commands used the existing interpreter
with `-B -m unittest` and named methods from
`tst.test_starter_export.StarterExportTests`.

The independent read-only auxiliary selected both environment junction and
physical-escape-before-read regressions from `tst.test_environment.EnvironmentTests`:
two tests, 0.009 seconds, exit 0. No broad suite rerun or edits occurred.

Reviewer read the actual final quality evidence and recomputed all sixteen log
hashes. All eleven quick gates and the 528-test complete suite passed, zero
failures/errors/skips, exit 0; 684.798 seconds unittest / 685.554 seconds wrapper.
Full-log SHA256
`5341628170577ac7a4cd78321c0da9c6add74fe0a524fa6ffdf00ac8c87a4240`.
The exact protected-path command was rerun successfully: original validators,
schemas/catalog, history, dependency inputs and active native source CI unchanged.

Junction execution was modeled on Linux; conditional native Windows branches were
not executed. Docker, actual fleet/runner access, live provider loading and remote
CI remain unqualified external gates. Unchanged areas were not reopened; later
report-only commits are outside this snapshot. This agent Delta supports separate
final triage and grants no human merge, release or deployment approval.
