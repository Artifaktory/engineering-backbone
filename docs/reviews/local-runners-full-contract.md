# Independent Full review: Backbone runner contract

Date: 2026-10-13. Reviewer role: independent read-only Full reviewer, trust/governance/test contract catalog. This report is separate from the runtime review. It is neither a human approval nor evidence of runner activation.

## Frozen snapshot

- Repository: `Artifaktory/engineering-backbone`.
- Base: `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`.
- Head: `9064f09b9aff88ae8a14e359f3d6ec82457ba582`.
- Head tree: `9d2fd1df089cfd46d8ed8dafbd1c4d37be4b1d5e`.
- Binary patch SHA256: `d6c3b53653c9099494dc49b09579e5917b8163c335b2bdda2119a4ba5686cb01`.
- Reviewed manifest: `full-review-manifest.json` outside both repositories.

Actual HEAD, tree and recomputed binary patch digest match the manifest. The tracked worktree is unchanged from the reviewed head. Base `AGENTS.md`, `policy/core.md` and `CONTRIBUTING.md` were read through `git show`; candidate Task Packet, plan, instructions, repository-controls and documentation were also inspected. No ancestor or additional changed-path `AGENTS.md` was found.

## Conclusion

`NO CONFIRMED IN-SCOPE FINDINGS`.

The conclusion is limited to this frozen migration diff and the coverage below. No defect ID is opened and no repair is requested by this reviewer. It does not attest complete CI, independent hosting controls, isolated execution, runner access or approval to merge/release. The full source suite and final acceptance mapping remain required closeout evidence; there is no silent waiver of a failing or unexecuted required check.

## Contract observations

- The four workflow files contain 11 directly executing source job definitions and two local governance callers. Every direct source job resolves to `af-ci-build-v1` with cumulative `self-hosted`, `linux`, `x64`, `ci-heavy` labels. The local calls use the same reusable governance selection. A missing group registration/access remains queued/blocked rather than triggering a hosted source fallback.
- Reusable workflows choose runner placement from `github.repository`. `inputs.source_mode` is not an authority for placement. An external consumer, including `Artifaktory/Artifaktory`, retains its prior `ubuntu-latest` default even if it attempts source mode; the unchanged shell event/mode checks separately reject forged source mode. Source versus consumer behavior is intentionally scoped to the source repository rather than changing downstream projects without their PRs.
- Base/head structural comparison found unchanged events, job IDs, concurrency, workflow/job permissions, environments, dependencies, timeouts and all existing step dictionaries across all workflows. This includes trusted-base and candidate SHA checkouts, `persist-credentials: false`, pinned action IDs, workflow-owned fingerprints, artifact identity/digest checks, compiled guard payloads and native validation commands. New guards limit ordinary external-fork source dispatch; they do not change consumer guards or replace the base-owned validation contract.
- The two mandatory aggregate jobs retain `always()` and the complete fixed dependency sets. Their actual shell/Python payloads still require every expected result to equal `success` and reject missing or additional jobs; neither source nor consumer routing introduces a bypass.
- No change touches `policy/`, schemas, templates, tooling scripts, dependency manifests or historical fixtures. Consumer bundle bytes and the compiled tooling/fingerprint authority are outside the patch. The older workflow test's literal hosted assertion was updated for identity routing, while the new test suite independently parses the exact selection and requires the correct source group/labels and consumer default. This does not relax the actual trust payload or gate tests.
- New routing tests cover all source jobs, two external identities, rejected hosted source fallback, absent group, wrong group, missing architecture and caller-controlled routing. They execute both actual aggregate payloads with success/failure/skipped/cancelled dependencies. Retained existing workflow tests additionally exercise every job result, missing/extra dependency sets and forged source mode on real fixtures.
- The HIGH-risk Task Packet, revised plan and independent plan-review/Delta record preserve distinct planning, implementation, quality, Full/triage/repair/Delta roles and human merge/release gates. Both revised plan files have identical SHA256 `ed544a34a1e3e12ed351a8927033ebff47d80d2968c1b203f86db2fb24774d13`; both plan-review documents are identical. No pending acceptance criterion is represented as runtime PASS.
- Documentation limits observed build-group evidence to the repository in which it was observed. Backbone repository access, isolation, approval restrictions and actual source-job runner records remain independently unverified, so activation remains blocked and the PR stays draft. Candidate-editable guards are described as mitigation, never immutable security proof. Existing source policy makes repository settings a separate control, which this PR does not implement or authenticate.

## Independent check evidence

Python runtime used for the review experiments: 3.12.14.

- `git rev-parse HEAD`; `git rev-parse <head>^{tree}`; `git diff <base> <head> --binary | sha256sum`: all matched the frozen identity, exit 0.
- `git diff --exit-code <head>`: exit 0.
- Read-only Python base/head structural comparison across all four workflow files and 13 job definitions: unchanged contracts and all original steps; exit 0. Confirmed no modified toolkit/template/policy/schema/manifest/fixture paths.
- `python -B -m unittest discover -s tests -p test_local_runners.py -v`: exit 0; 5 tests passed.
- Additional independent execution of each actual aggregate payload: PR 22 cases and maintenance 14 cases passed. For every required job, tested `failure`, `skipped`, `cancelled` and a missing job; also tested all-success and an extra job. Every invalid input failed, and all-success alone passed. No GitHub service, scheduler or registration was exercised.
- Read the unchanged actual source-mode/event restriction and existing fixture tests covering forged source mode, trusted configuration, complete aggregate inputs and consumer upgrades.

The candidate check document reports source validator, compiled-toolchain and workflow-kit compilation, previous trusted-base validator and actionlint successes; its complete unittest suite was still running at snapshot time. Those wider check reports were inspected but not independently rerun here. No complete suite or runner activation PASS is inferred from targeted contract checks.

## Coverage and unreviewed areas

Inspected every tracked change, trusted-base instructions and policy, candidate Task Packet/plan/review/Delta/activation/check documents, relevant repository-controls text, the full workflow inventory and all changed tests. Reviewed identity routing, consumer defaults, source-mode/event restrictions, candidate/trusted checkout authority, pinned compiled payload preservation, negative gate logic and test evidence claims.

Unreviewed or unexecuted here: real GitHub expression evaluation/scheduling; live group access and public-repository/approval settings; isolated/ephemeral runner behavior; fresh runner Python/setup/action execution; the complete source/consumer/Copier unittest suite and final trusted-validator/compilation logs; actual remote job records, required-check settings and Codex review results. Deployment, release, downstream installation and broader security redesign are outside this task and were not executed or approved.

No source edits, commits, pushes, remotes, settings writes, release/deployment actions or nested agents were performed. The only write is this redacted report outside the repository.
