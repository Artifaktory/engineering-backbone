# PR 18 CI observations and confirmed corrections

Observed on 2026-10-20 through GitHub workflow/job metadata and failed-job logs.
These results belong to head `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` and base
`212608aa50ee517b3dd3107a9480da997222fd4f`; they do not certify later commits.

| Workflow/job | Run / job | Actual result |
| --- | --- | --- |
| Backbone quality / Source dependencies and container | 39418277824 / 118612658352 | PASS, including clean locked dependencies, real Docker build and offline validation/Copier smoke |
| Backbone quality / Foundation | 39418277824 / 118612658877 | Source validation and all **432 tests passed in 279.873 seconds**; the later committed-patch whitespace step failed |
| Backbone quality / Trusted base policy | 39418277824 / 118612658915 | FAIL: the actual base-owned old validator reports 34 layout/context errors |
| OpenCode native discovery / Windows | 39418277928 / 118612549794 | PASS, including native discovery/read-only exercise and evidence upload |
| OpenCode native discovery / Ubuntu | 39418277928 / 118612550144 | PASS, including native discovery/read-only exercise and evidence upload |

See the [quality run](https://github.com/Artifaktory/engineering-backbone/actions/runs/39418277824)
and [native run](https://github.com/Artifaktory/engineering-backbone/actions/runs/39418277928).
The native exercise does not qualify model reasoning, all operating-system paths
or a product deployment. Native Copilot behavior was not exercised by these jobs.

## Confirmed Foundation defect

The job's final command is `git diff --check "$BASE_SHA" "$HEAD_SHA"`. It exits 2:
`docs/changes/backbone-layout/publication.md:56: new blank line at EOF.`
The same complete base-to-head diff was reproduced locally with exit 2. Earlier
working-tree-only checks missed this committed evidence-file defect. This delivery
removes only the final extra blank line and requires a committed complete PR diff
check after the final publication/evidence commit. The workflow gate stays intact.

## Copilot audit

The read-only `correction_copilot_assess` session checked 24 active Copilot files
and 67 relative links: native/canonical references were already retargeted and no
broken relative link was found. The source docs selector was still
`*.md,docs/**,plans/**`; it missed newly nested Markdown outside `docs/`.
COP-LAYOUT-01 adds recursive Markdown coverage in the source and removes obsolete
source `plans/**`, while retaining `docs/**` for non-Markdown documentation data.
The legacy generated consumer selector remains unchanged.

GitHub documents native discovery and glob semantics in its
[repository instruction guide](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions).
Root `copier.yml` is the legacy Copier entrypoint, not a Copilot file. Copilot's
repository entry and path rules remain in their native `.github` locations.

## Trusted-base transition

The old trusted validator requires old policy/dependency/native instruction paths
and interprets moved historical Markdown in its new location. These checks cannot
be satisfied merely by editing a candidate-side validator. Symlinks are rejected;
duplicating old policy files would undermine the single canonical reference.

A separately scoped compatibility delivery, BB-LAYOUT-013, is being prepared on
the unchanged main layout. It must preserve the old validator's checks while
supporting both source layouts, resolve candidate and trusted-base paths
separately, and retain trusted historical mappings and hashes. It needs positive
transition coverage and negative policy/schema/adapter/permission/archive tests.
After independent checks/reviews, a human must merge that prerequisite before
PR18 can use the updated base-owned validator. No fallback, projection, skipped
gate or automatic merge is part of this correction.
