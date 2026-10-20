# Independent corrective plan review

Reviewer session: `corrections_plan_review`. Role: independent read-only plan
reviewer. Task: [BB-LAYOUT-012](task-packet.json). This report reviews the plan
before implementation; it does not certify a repair, CI result, release or merge.

## Frozen planning subject

- Corrective baseline: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.
- Original PR base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- [Plan](plan.md) SHA256:
  `88a6a16404ace99048d59a69f5b84212fb641821e753f1776b45750dadd1d6ba`.
- [Task Packet](task-packet.json) SHA256:
  `cdc5b77667593c7950ce1afaf6ca50c6df200051186911891a21cb662058666e`.

The reviewer independently verified HEAD and both planning hashes. The planning
files were uncommitted; their exact file hashes identify this planning snapshot.
Only the planning directory was untracked when inspected. Later implementation
review must bind its own committed head and binary patch digest.

## Coverage and observations

Read the root agent instructions, canonical policy, contributor guide, plan and
packet, current source docs instruction, corresponding legacy template, and the
affected source/consumer distribution-test parity logic.

- The source instruction still has `*.md,docs/**,plans/**`. The bounded proposed
  selector includes nested Markdown while retaining all `docs/**` data paths.
  Root and nested Markdown, tooling Markdown, a docs JSON path and an unrelated
  code negative are explicitly required. The plan correctly rules out a
  whole-path matcher whose single star silently crosses directory separators.
  The test must exercise the declared slash and dot-directory behavior; it must
  not claim to prove live Copilot instruction loading.
- The legacy template retains its existing selector. Existing source/consumer
  parity checks distinguish source-only rules while preserving instruction
  bodies and other metadata. Extending that explicit distinction to the docs
  selector is a bounded correction, not a permission or policy relaxation.
- Native Copilot discovery paths remain under `.github/`. Root `copier.yml`
  remains the separate legacy Copier entrypoint. Neither file location is moved
  based on the ambiguous root-file wording.
- The reviewer independently ran the complete original-base-to-current-head
  `git diff --check`: exit **2**, identifying only the new blank EOF line at
  `docs/changes/backbone-layout/publication.md:56`. The plan's minimal removal
  and final committed-diff checks directly address the reproduced failure.
- The new publication procedure checks both the corrective diff and the full
  live PR diff after the final evidence commit. It accounts for a changed live
  base and invalidates the check after any later commit. This closes the gap
  between a clean worktree and a valid already-committed patch without weakening
  the CI gate.
- Current CI observations must remain bound to their tested head and actual
  workflow/job identities. Existing remote results are not relabeled as proof
  of an unpublished corrective head.
- The old trusted-base path failure remains explicit and unchanged in this
  packet. A separate compatibility delivery is outside BB-LAYOUT-012; this plan
  authorizes no candidate fallback, projection, waived check, main merge,
  repository-setting change or downstream application.
- Role separation, pre-implementation review, deterministic affected checks,
  frozen Full review, independent triage, necessary Delta, two-Full/six-iteration
  limits and exact remote publication readback are specified.

## Outcome

**NO CONFIRMED IN-SCOPE PLAN FINDINGS.**

The bounded plan is suitable to proceed to implementation and its recorded
verification/review chain. No changes to implementation, tests, workflow code,
legacy templates or either reviewed planning file were made by this reviewer.
The future selector regression, repaired committed diff, updated PR and new
remote results remain to be demonstrated by their assigned roles.
