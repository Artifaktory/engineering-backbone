# Source CI: local runner and evidence contract

This is the operating contract for `Artifaktory/engineering-backbone` source CI.
It does not configure a consumer project's CI or provision a runner. The source
workflows retain their PR, main-push and manual triggers and all substantive
validation, trusted-base, container and native discovery checks.

## Allocation and trust

Source jobs in `quality.yml`, the source branch of `governance-checks.yml`, and
`opencode-native.yml` have job-level repository/event conditions. In the checked-in
workflow, a foreign repository, unsupported event or PR from a different head
repository cannot allocate a source runner. The trusted-policy job remains PR-only.
The reusable workflow independently checks the source condition; relying solely on
its caller or a shell step after allocation would not suffice.

| Job | Required local labels |
| --- | --- |
| Foundation, source dependencies/container, trusted policy | `self-hosted`, `Linux`, `X64`, `backbone-ci` |
| Linux native discovery and document portability | `self-hosted`, `Linux`, `X64`, `backbone-ci` |
| Windows native discovery and document portability | `self-hosted`, `Windows`, `X64`, `backbone-ci` |

The native matrix retains the historical `ubuntu-latest` / `windows-latest`
**display names** to preserve check identities. Allocation uses its explicit local
`labels` arrays; these names do not select GitHub-hosted images. There is no hosted
fallback for source mode. A missing matching runner leaves a job queued; it is not
passing CI and is not permission to remove a required check.

Before assigning these labels, the operator must provide isolated, preferably
ephemeral workers restricted to the reviewed source workflow through runner-group
and repository access controls. The Linux worker needs Bash, Git, Python setup
support, and Docker for the existing image job. Windows needs Git/Bash and Python
setup support. Workers must have no production credentials or access to deployment
hosts, sensitive networks or unrelated workspaces. Do not attach these labels to a
general-purpose deployment runner merely to clear a queue.

The job condition is a checked-in routing safeguard, not an authenticated security
boundary against a contributor who changes the workflow itself. Operator-controlled
runner access, appropriate workflow approval/restrictions and isolation remain
required before enabling local execution, especially in this public repository.
This change neither installs those controls nor proves any worker is available.
No `pull_request_target` or privileged fork execution route is introduced.

## Checks and evidence

The foundation job still runs the source validator, all compiler checks and the
complete unittest suite. The dependencies job still verifies tracked locked inputs,
builds the tooling image and runs its offline smoke. The trusted-policy job runs
the actual base-owned validator against the candidate. Source Python checks use
isolated environments and the existing hash-locked dependencies.

Both native platforms run direct-copy/line-ending and architecture distribution
tests before the pinned, credential-free OpenCode discovery smoke. These checks
establish their observed behavior only; they do not certify the entire Windows
suite, qualify a model or establish production agent permissions.

Source workflows do not upload GitHub artifacts. Normal Actions logs still contain
command output. The native report remains at `artifacts/opencode-native/report.json`
inside the isolated checkout. Before worker disposal, an authorized operator can
retain necessary redacted evidence through an approved local channel and bind it to
the run, job, platform, base/head and checks. Do not copy credentials or raw personal
data into logs or durable reports. After evidence handling, dispose of the ephemeral
worker or apply the reviewed workspace/environment/container cleanup procedure.
No broad host cleanup command is installed by this PR.

Missing runners, failed checks, skipped checks, unavailable Docker/native platforms
and uncollected reports remain explicit evidence gaps. Static allocation tests and
local unittest results do not replace a completed remote run or human acceptance.
Repository required-check settings and human merge/release controls are unchanged.

## Consumer boundary

Direct copies must select their workflows explicitly before the first push.
Source job guards prevent these particular source jobs from allocating in a foreign
repository; they do not establish that every copied or added workflow is safe.
Preserve the receiving project's stronger runner, evidence and publication rules.

Legacy `governance-checks.yml` calls with `source_mode: false` retain their existing
hosted Linux allocation. The separate reusable `workflow-kit-pr.yml` and
`workflow-kit-maintenance.yml` remain `workflow_call` assets with hosted-runner and
artifact-exchange assumptions. They are not called by these source entrypoints.
Projects prohibiting hosted runners or artifact uploads must not activate those
legacy workflows until a separate reviewed profile replaces those assumptions.

## Basis and limits

These are Backbone operating rules implementing the user's local-runner/no-upload
constraint. GitHub's [job condition and runner syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idif),
[expression syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#fromjson)
and [self-hosted runner security guidance](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#hardening-for-self-hosted-runners)
were inspected on 2026-10-21. They explain the mechanism and risks; they do not
require our project label names or certify this deployment. See also the
[dependency/container contract](dependency-compatibility.md),
[repository controls](repository-controls.md) and
[adoption guide](../../agent-governance/adoption.md).
