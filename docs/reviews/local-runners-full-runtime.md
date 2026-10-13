# Independent Full review: Backbone local runners — runtime and compatibility catalog

Date: 2026-10-13. Role: independent read-only runtime/platform reviewer. This is review advice, not human approval, release approval, or runner activation evidence.

## Immutable snapshot

| Item | Observed value |
| --- | --- |
| Repository | Artifaktory/engineering-backbone |
| Base | `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13` |
| Head | `9064f09b9aff88ae8a14e359f3d6ec82457ba582` |
| Tree | `9d2fd1df089cfd46d8ed8dafbd1c4d37be4b1d5e` |
| `git diff --binary BASE..HEAD` SHA256 | `d6c3b53653c9099494dc49b09579e5917b8163c335b2bdda2119a4ba5686cb01` |

These values independently match `full-review-manifest.json`. The tracked checkout was clean when inspected. No additional ancestor or applicable nested `AGENTS.md` was found, including a hidden-file instruction search. No tracked source or test bytes were edited.

Read `AGENTS.md`, `policy/core.md`, `CONTRIBUTING.md`, the active local-runner Task Packet/plan, the independent plan review and LR-PLAN-001 Delta, new activation/check evidence, and `docs/repository-controls.md`.

## Conclusion

**NO CONFIRMED IN-SCOPE FINDINGS** in the runtime/platform/consumer-routing catalog for this frozen snapshot. This conclusion is limited to the coverage below. It does not establish actual source-repository access to the selected group or certify the host Python/tool-cache/runtime environment. Draft-only delivery and the documented activation stop remain necessary.

## Job and compatibility coverage

All four workflow files and their full current diffs were inspected. All 11 directly executed job definitions resolve the source repository to the build group with the four required labels. The two same-snapshot reusable governance callers inherit that selection. A parsed comparison against the trusted base confirms that every job step payload, event, permission block, timeout, dependency, output, native command and artifact identity is unchanged; only `runs-on` and the explicitly planned same-source-fork guards differ in these workflows.

| Workflow | Jobs inspected | Routing/runtime result |
| --- | --- | --- |
| governance-checks | validate | Source identity selects `af-ci-build-v1` plus self-hosted/linux/x64/ci-heavy. Other caller repositories retain ubuntu-latest. Python3.12, source/consumer/trusted validations and exact source command chain are retained |
| quality | foundation reusable caller; trusted-policy direct job | Caller remains same-snapshot and source_mode=true. Direct trusted-policy binds build group, preserves base/head checkout paths, base-owned dependencies/validator and bootstrap notice |
| workflow-kit-pr | configuration; governance reusable caller; quality; security; secrets; gate | Source routes locally; external consumers retain hosted default. Same-source fork guards do not change external consumer behavior. Trusted execution artifact ID/digest, prepared runtimes, explicit candidate SHA and all mandatory needs are retained |
| workflow-kit-maintenance | configuration; security; secrets; gate | Source routes locally; external consumers retain hosted default. Default-branch/event contract, prepared artifact, runtime setup and strict maintenance aggregate are retained |

The identity used for reusable routing is `github.repository`, the caller's repository context. It is not `inputs.source_mode`. The existing mode checks still reject a foreign consumer forging source_mode=true before source validation. An external consumer with either source mode value cannot gain this source-only local placement through the routing expression. Templates and compiled workflow payloads are untouched; existing consumer callers pin their reviewed workflow reference and require their own adoption.

Source identity takes the explicit JSON group/labels object; the external branch is the original string ubuntu-latest. The only fixed mapping is the source-only trusted-policy job. No source fallback to hosted jobs or label-only build-group inference is introduced.

PR/head-versus-trusted-base and maintenance/default-branch checkout contracts are unchanged from the trusted base. The deliberate Backbone head checkout is pre-existing; AO's default merge-result preservation issue is not a reason to alter Backbone's existing consumer/trust contract. Contents tokens remain read-only, checkout credentials remain disabled where originally set, and the artifact/digest checks remain unchanged.

## Aggregate failure-path evidence independently executed

Executed the actual `Require every mandatory job to succeed` Bash/Python snippets from both frozen workflows in read-only subprocesses. Inputs used the actual declared dependency names; no alternative implementation of the verdict was substituted.

| Workflow gate | Cases | Actual result |
| --- | --- | --- |
| workflow-kit-pr | All-success; each of five dependencies changed separately to failure/skipped/cancelled; each dependency missing | 21 cases PASS: only complete all-success exited zero |
| workflow-kit-maintenance | All-success; each of three dependencies changed separately to failure/skipped/cancelled; each dependency missing | 13 cases PASS: only complete all-success exited zero |

The aggregate `if: always()` and fixed dependency sets remain present. A same-source foreign-fork guard skips required dependencies, but the workflow-kit aggregate still rejects those skipped results. Missing/failed/cancelled jobs do not become aggregate success. This execution verifies the gate code, not GitHub job scheduling or external branch-protection enforcement.

New routing tests were read in full: all-source selection, retained external defaults, hosted/wrong-group/missing-label rejection, caller-controlled selection rejection and actual aggregate snippet execution. The modified pre-existing workflow-kit assertion preserves the hosted external branch and verifies the group/source-expression contract. No check assertion, time budget or production payload was removed to get green CI.

## Quality evidence and host prerequisites

The frozen check record and parent supplied Python3.12.14 locked-dependency installation, five targeted runner tests, source validator, toolchain fingerprint/compiler, workflow-kit compiler, previous trusted-base validator, actionlint 1.7.7 with labels, and whitespace PASS. The frozen record showed the full unittest suite running; before this review concluded, the parent separately reported all 239 tests PASS in 642.854 seconds. This remains supplied quality-role evidence, not a suite independently rerun by this reviewer.

The source jobs retain pinned setup-python and the prepared project runtime setup actions. Those actions still require a compatible Linux distribution and writable tool cache/PATH; the actual AF host distribution/cache/dependency inventory was not supplied. Official [setup-python self-hosted guidance](https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#using-setup-python-with-a-self-hosted-runner) describes distribution compatibility and cache-write needs. No particular pc1/pc2 OS version, Python artifact compatibility or tool inventory was independently observed here, so these are outstanding activation evidence, not a confirmed implementation defect. Git/Bash and the configured validation runtime/tools must work under the actual isolated runner account.

The observed AF build-group job names/labels supplied by the parent support selecting the known group, but do not prove engineering-backbone repository group access. The new documents make that limitation explicit. Candidate-editable guards are documented as mitigation; independent repository approval/access/isolation verification remains a prerequisite in this repo as well as AO.

## Commands, limits and handoff

Independent read-only commands included instruction/file reads with `rg`, base/head/tree/diff digest verification, complete workflow diffs, current job/bootstrap/gate reads, parsed comparisons of all job fields against base, and the 34-case actual aggregate snippet execution. Successful commands exited zero. No broad production suites, dependency installs, publishing/deploying jobs, local commits, pushes, remote reviews or settings mutations were performed.

Unreviewed/unexecuted: real group/repository access; actual Linux distribution and pinned Python download/native dependency behavior; tool-cache/workspace ownership; isolated clean runner lifecycle and cross-job cleanup; live Actions approval/repository enforcement; native action-version support on the installed runner; actual source runner/group records; independent reproduction of the quality role's complete suite result; remote advisory Codex findings. Private raw logs, credentials and unrelated local state are not included in this report.

Keep this review bound to the exact recorded source snapshot. If the author repairs AO-only defects, do not reopen unchanged Backbone implementation areas as a Delta. Any new Backbone change must be frozen and reviewed with its direct regressions before delivery. Live source execution remains BLOCKED until independent access/runtime/isolation evidence is obtained; this no-finding result does not override that stop.
