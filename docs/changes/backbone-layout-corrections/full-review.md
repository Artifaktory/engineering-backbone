# BB-LAYOUT-012 independent Full review

Date: 2026-10-20. Reviewer session: `correction_full_review`, separate from the
planner, implementer, quality checker and finding triage. This bounded Full review
covers behavior and governance/security as permitted by the reviewed plan.

**NO CONFIRMED IN-SCOPE FINDINGS.** No P0-P3 defect attributable to the corrective
diff was identified. This is not approval to merge or a claim that all PR checks
pass. Separate finding triage and final publication checks remain required.

## Frozen identity and scope

- Corrective base: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.
- Reviewed head: `dbe05e14a255488e3416465971ece755fb04aba3`.
- Reviewed tree: `1801cbc5defdf82a4c37f5ead84eea2e8ab1df4b`.
- Original PR base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Binary corrective patch SHA256:
  `8957f9cea5e698daa212cdbd08c555dbdd6ea0e7222b52c1dea7e19038575ed0`.

The reviewer independently resolved the frozen HEAD/tree, recomputed the binary
patch digest and confirmed that it matched the supplied patch bytes. The frozen
worktree was clean before and after review. It was not edited. The only reviewer
write is this report in the live corrective change directory.

The review read `AGENTS.md`, canonical governance, the corrective plan, Task Packet
and independent plan review; inspected all four substantive file diffs and their
relevant surrounding implementation; and read the four new planning/CI evidence
records. The broader original layout refactor was not re-reviewed. The separate
BB-LAYOUT-013 compatibility implementation was not reviewed here.

## Behavior and governance coverage

| Area | Review conclusion |
| --- | --- |
| Source Copilot docs rule | The only instruction-file change is the declared selector. Recursive Markdown coverage retains root Markdown and `docs/**` data coverage. Native location and instruction body remain unchanged. |
| Selector regression | The test uses slash-aware filesystem glob matching, demonstrates the old nested-document omission, checks nested component/tooling Markdown and docs JSON, and excludes unrelated Python source. It explicitly limits its claim to selector modeling. |
| Optional components | If the frontend is absent, the example is created in a separate temporary fixture; the copied repository component is not recreated. Mandatory tooling and docs inputs remain checked as real files. |
| Source/legacy distribution | Both source and legacy docs headers are asserted explicitly. Existing rendered body comparisons and other role/skill metadata assertions remain. The legacy template itself is unchanged. |
| Publication EOF repair | Byte comparison confirms exactly one extra final LF was removed. The publication document retains a single terminal newline and its prior historical claims. |
| Contributor procedure | The new requirement covers resolved committed PR base/head and corrective base/head after the final evidence commit. It explicitly requires rerunning those checks after later commits. |
| Trust and permissions | No validator, schema, dependency input, compiled guard, workflow, canonical policy, legacy template or native agent permission changed in this correction. No candidate-side fallback, skipped gate or automatic merge was introduced. |
| CI evidence | The observation record binds the previous results to head `c501087...` and identifies the trusted-base failure separately. It does not relabel prior-head or OpenCode results as current-head/native Copilot qualification. |

The existing validator's instruction frontmatter constraints were also inspected
for compatibility with the new selector. The change does not modify executable
validation or grant any agent additional tools or authority.

## Evidence used and limits

This reviewer performed read-only Git identity/diff checks, exact source-instruction
and publication-byte comparisons, and implementation/evidence inspection. No test
suite was rerun by this reviewer and no repair was made.

The separate quality checker's [checks.md](checks.md) was read as external evidence
added after the frozen commit, bound to the same exact head/tree/patch. It records
41 affected tests passing in 68.584 seconds; the canonical validator, all four
compiler checks and dependency check passing; both committed diff checks passing;
and reproduction of the old complete-PR EOF failure. Its pruned-copy run records
the new regression passing while the removed frontend stayed absent. Those are
quality-checker executions, not executions by this reviewer.

Native Copilot loading/model behavior and product qualification were not tested.
There was no new full 433-test run in this review. Earlier remote full-suite,
container and native Windows/Linux results apply only to their recorded old head.
The old trusted-base validator incompatibility remains a known failed gate;
candidate checks and this review do not replace it or authorize its adoption.

This report and any subsequent evidence commit are outside the frozen review
snapshot. Before publication, resolve the final head and live PR base, rerun both
committed diff checks, verify remote head/tree correspondence, and read current
check conclusions. Future substantive changes need their own applicable review.
