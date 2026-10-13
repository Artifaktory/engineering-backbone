# Independent scoped plan follow-up: LR-BB-CODEX-001

Role: independent read-only reviewer. Repository: `Artifaktory/engineering-backbone`. Scope: the new confirmed remote finding repair section of `plans/local-runners.md`, the directly required Task Packet update, and the proposed early rejection gates. Previously unchanged implementation and Full-review scope were not reopened.

## Exact reviewed snapshot

| Item | Revision or SHA256 |
| --- | --- |
| Prior published identical-tree local HEAD | `21e633fd98dc86fc0f50d2d6f1c99414fafcb6bb` |
| Local HEAD tree | `46d6fb10d37fdcd9dbb43f8e1444f6a577e60460` |
| Associated GitHub head, supplied by parent | `19fb75b640a470b459119f1654f5e43d3c1aef2b` |
| Exact revised `plans/local-runners.md` | `69b1d0d2aa406b7aadaee45a977dcf67cadc0265ccf3de687f44caf0edc39ca7` |
| Exact revised `plans/local-runners-task.json` | `3e56b90c7384de303f44f4886e63fecd169dca025d07f5062a1d8044f9ab726c` |
| Binary diff of these two plan/task files | `13f7c2b94d0fe194fa1b2e0412e1aba6cf47b35509560b4a38c5de0f63362c08` |

The working tree has only the plan, Task Packet, and triage report changed. Workflow/test implementation is still the previously published snapshot. The two reviewed file digests were rechecked before this report and remained identical.

## Conclusion

**NO CONFIRMED IN-SCOPE FINDINGS** in the proposed scoped repair plan. No plan-review blocker remains for implementing this bounded repair. `LR-BB-CODEX-001` itself remains an unresolved implementation defect until the actual gates, regressions, checks, independent Delta reviews, and remote follow-up are complete. This report is neither implementation approval nor activation evidence.

## Reviewed reasoning and boundaries

- The existing source `quality.yml` has a `foundation` reusable caller named `Foundation checks`, with the reusable `validate` job source-fork condition; `trusted-policy`, named `Trusted base policy`, also has a source-fork job condition. Thus a source foreign-fork PR can skip both validation paths. The new plan correctly restores scheduling rather than replacing one skip with another successful or neutral result.
- The proposed fixed first Bash rejection in both validation jobs occurs before checkout and setup. A foreign or missing source head identity must produce a nonzero result under the existing check names. Neither a notice nor an `exit 0` is sufficient. Unavailable local runner access may leave the check queued, but it cannot be reported as successful rejection or runtime proof.
- Source rejection is based on source repository and PR event identity, not on caller-controlled `source_mode`. Same-source PRs, source push/manual events, and valid external-consumer PRs keep their existing subsequent behavior and routing. The reusable governance script's original forged-source-mode and event checks remain intact.
- The plan explicitly passes the PR head repository through an environment value and compares quoted shell variables. This avoids placing event-derived text inside the shell program. Implementation review should reject direct `${{ ... }}` interpolation into `run` and any `eval`, command construction, or unquoted expansion. Missing values need an explicit empty/default handling that fails source PRs without treating missing identity as same-source authorization.
- Required check names, runner group/labels, events, permissions, trusted base and candidate checkouts, and existing validation commands remain outside the repair. Workflow-kit aggregate behavior is unchanged; its existing failed/skipped/missing-result defenses are not reopened or replaced by this narrow source quality fix.
- Planned regression tests execute the actual two early gate scripts and cover same-source, foreign-source, absent-head, non-PR source events and external consumer fork behavior. Tests also check original scheduling/names and placement before actions. A hostile environment value containing shell metacharacters can be included in those rejection cases to demonstrate that it remains data. Source identity tests must not use `source_mode` as authorization.
- Adding `tests/test_workflows.py` to the Task Packet is directly necessary: its existing positive source test calls `Check workflow mode and event` with source repository/mode but no PR head fixture. Supplying the real same-repository head preserves that positive assertion under the new fail-closed contract. The plan restricts this file's edit to that fixture; existing adversarial assertions are retained.
- AC2, AC3 and AC4 return to pending while repair evidence is outstanding. AC5 remains blocked for group-access/isolation/actual source-runner evidence. Prior reports remain historical observations and cannot close the newly confirmed finding.
- Two independent scoped Delta catalogs must bind the prior reviewed/published local head, repaired head and binary patch digest. This restores the approved scheduling/gate contract without changing trust authority, so a second Full round is not required for the stated scope. Any implementation that broadens events, privileges, access, or consumer behavior would require renewed scope/review.
- Candidate-editable mitigation remains explicitly documented. The repair does not authorize repository settings, runner registration, merge, release, deployment, or activation and does not claim immutable protection.

## Evidence and limitations

Read the new plan section (`plans/local-runners.md:27-33`), Task Packet diff, remote triage addition, current `quality.yml`, the first reusable governance steps, `tests/test_local_runners.py`, and the relevant source-positive fixture at `tests/test_workflows.py:172-177`. Applicable root instructions and Backbone core/contribution policy from the earlier review remain binding and unchanged in this repair scope.

Read-only commands included `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git status --short`, `git diff --name-only`, plan/task diffs, `sha256sum`, targeted file reads, and `git diff --binary -- <plan> <task> | sha256sum`. These completed successfully. No tests, dependency installation, GitHub dispatch, source edits, commits, pushes, setting writes, or nested agents were performed by this reviewer. The only write is this report outside the repository.

The supplied [remote finding](https://github.com/Artifaktory/engineering-backbone/pull/11#discussion_r4261094614) was not retrievable through the public web reader; its identity and triage are supplied by the parent and tracked triage document. The reviewer independently inspected the implicated job conditions rather than assuming the comment proves runtime behavior. [GitHub's primary branch-protection documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging) confirms that required checks can satisfy the status condition with skipped or neutral outcomes; actual repository protection configuration was not inspected.

Unreviewed: the yet-unwritten gate implementation and tests, full/consumer/trusted/compiled check results for that repair, real GitHub scheduling/check conclusions, native hosting/runtime/runner access and isolation, actual required-check settings, and new remote Codex results. All remain required evidence or explicit blocked states, not PASS inferred from this plan.
