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

## Connect an actual worker

The label arrays describe required workers; they do not register a machine. When
jobs are queued with no assigned runner and no executed steps, first establish
allocation. That observation does not identify whether a label is missing, the
service is offline, capacity is busy or repository/group access is unavailable.

1. An authorized operator selects a dedicated isolated worker and reviews its
   account, network reach, cleanup and access boundaries. Do not repurpose a
   deployment host or attach production credentials to make this queue move.
2. In GitHub's actual repository/organization runner setup, register the selected
   worker and grant the intended repository access. Supply registration tokens
   through that setup channel; never paste them into chat, Git, scripts or evidence.
   Follow the current [platform service setup](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application)
   after registration. Service installation and account selection are operator
   actions, not commands performed by this kit.
3. Assign the complete labels above. All labels are cumulative. For a restricted
   runner group, also permit the actual job-defining workflow: Foundation jobs
   are defined in `governance-checks.yml`, not only in the calling `quality.yml`.
   Follow [runner-group access](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)
   for the actual immutable workflow/branch policy. A correct label cannot bypass
   a group restriction.
4. Under the same account/environment as the service, run the matching local check:

   ```sh
   python scripts/runner_doctor.py --profile source-linux
   # On the Windows worker, instead:
   python scripts/runner_doctor.py --profile source-windows
   ```

   The doctor checks the observed OS/X64, current Python 3.12 and venv modules,
   Git/Bash, Linux Docker CLI/daemon or Windows Git Bash/PowerShell. Fixed probes
   have ten-second timeouts and suppress tool output. It installs/registers
   nothing and does not verify GitHub labels, group access or host isolation.
   Verify download access for Actions, locked packages, images and the pinned
   native smoke separately; no successful network or package-install claim follows
   from the doctor. A missing prerequisite returns nonzero.
5. In Settings → Actions → Runners, confirm this repository can see the worker and
   its full labels. `Idle` means connected/ready, `Active` means executing, and
   `Offline` needs service/machine/network investigation. A local process or tool
   PASS alone is not this GitHub observation. Inspect existing queued jobs before
   creating additional runs.
6. Observe a real job receiving that runner and completing the required checks.
   Record repository, run/job URL, exact head, worker OS/labels, observed account
   boundary, result and limits using the [local CI record](../../templates/operations/local-ci.md).
   Test an intentional required-check failure during reviewed adoption. Preserve
   unexecuted Windows, Docker or other required evidence as pending/blocked.

The operator controls runner registration, services and GitHub access. This PR
does not perform those actions or prove an available fleet. For a consuming
project, start from the inactive [local example](../../templates/operations/local-ci.yml.example)
and its explicit limitations; do not activate legacy hosted/upload workflows.

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
[label routing](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow)
and [monitoring/troubleshooting](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot)
guidance inspected on the same date. See the
[dependency/container contract](dependency-compatibility.md),
[repository controls](repository-controls.md) and
[adoption guide](../../agent-governance/adoption.md).
