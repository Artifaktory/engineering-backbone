# Codex follow-up repair verification

This result covers confirmed BB-CX-05, BB-CX-06 and BB-CX-07 from Codex review
`5487485660` at published `3a2e3c83954cff3f7402fad7293b58c4524ae21a`.
See [follow-up triage](codex-followup-triage.md), the
[task packet](../../plans/codex-findings-task.json), and
[earlier repair results](codex-result.md).

## Frozen subject

| Subject | Local commit | Git tree |
| --- | --- | --- |
| Previous published repair, identical to `3a2e3c8` | `6542ad3f76ae35fa5475fad998a7aa2967225496` | `d28d6972fa999e785af13b315ce4daf570c73aea` |
| Follow-up implementation | `9663d5cc97a9768b0952b302620eb0716c5f92c1` | `cdb1f4473ee313fd4b91421d120e8650dce9991f` |

Patch SHA256 using `git diff --binary --full-index BASE HEAD`:
`fcdecafa950f2b337f9cd70f174379989cf02fa7795ab39274fccf1de354b71e`.
Publication may have different commit metadata; matching remote trees are recorded
on the PR. This subsequent result file changes no implementation.

## Independent results

Separate read-only sessions `codex_delta_correctness` and `codex_delta_security`
reviewed the same immutable repair snapshot. Neither authored these repairs. Both
confirmed all three findings resolved, reported no new confirmed direct regression,
and reconfirmed clean tracked worktrees and the assigned head/tree/patch identities.
The review covered the three changed repairs, the complete new tooling-identity
contract and direct regressions. Unchanged foundation areas were not re-reviewed.

| ID | Verified repair |
| --- | --- |
| BB-CX-05 P1 | Current CLI validates trusted project facts and retains the effective union of enabled providers. The pinned workflow independently rejects disablement even when executing an older approved validator. Initial opt-out, valid strengthening and ordinary project-fact changes remain supported. |
| BB-CX-06 P2 | Both the generated active caller and supplied manual example expose `workflow_dispatch`; its candidate/default-base mapping remains intact. Existing callers require a reviewed manual refresh. |
| BB-CX-07 P1 | Workflow-owned coherent fingerprints check both base and candidate tooling before pip or validators execute. Isolated script/schema/lock poisoning, simulated poisoned next-base, mixed versions, downgrade and managed symlink aliases fail. Known previous tooling and coherent updates remain usable. |

The current actual rendered tooling identity is
`ef266be0f22b7e505563e408fe8b93ab6418ec1255bed6c2d6067f9e74be44c9`.
The two retained identities and their actual source trees are documented in
[repository controls](../repository-controls.md). Authority comes from the pinned
workflow's literals, not candidate-supplied hashes. A digest is not a human signature
or proof of semantic correctness.

## Checks actually executed

- Root integration: **84 tests**, 46.345 seconds, exit 0: 46 validator, 13 Copier,
  25 workflow/compiler/compatibility tests. No dependency or Action pin changed.
- Correctness reviewer: the same 84 tests, 45.187 seconds, exit 0; plus independent
  working-tree/template-only compiler probes, project/provider variation and a real
  frozen previous-to-current Copier upgrade with explicit caller repinning.
- Security reviewer: 25 workflow tests and five focused validator tests passed;
  independent candidate `sitecustomize`, fake-authority and next-base probes never
  executed poisoned candidate code and returned exit 1.
- `python scripts/compile_toolchain_fingerprint.py --check`: exit 0 against actual
  working-tree Copier output, not raw source bytes or a stale Git checkout.
- Current and preceding published source validators with explicit trusted-base
  comparison: exit 0. The original trusted source comparison also passed.
- Actionlint 1.7.12 and working/staged/frozen-range whitespace checks: exit 0.
- Real Git `core.autocrlf=true` checkout preserves the eight attested tooling files
  at LF while application text retains its own conversion behavior.

These are observed model-session and deterministic-check results. GitHub CI,
provider re-review and publication readback are recorded separately on PR 1 after
publication. External caller protection, human merge/release approval, workflow
sharing and native-client discovery remain separate operational controls.
No downstream write, merge, release or deployment was performed.

A later focused ownership probe and Codex review `5488022625` identified a
remaining canonical-policy alias and two compatibility regressions at the
subsequently published snapshot. They were separately confirmed, corrected and
independently checked in [the final Delta result](codex-final-delta-result.md).
The results above describe their original frozen subject, not the later repair.
