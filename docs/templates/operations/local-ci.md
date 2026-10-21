# Local CI adoption and observed execution

Project-owned record template; complete the applicable fields with actual facts.
Planned configuration, local prerequisite results, GitHub availability and completed
execution are different evidence. Empty fields and placeholders are not approval.

## Selected boundary

| Fact | Project decision / evidence |
| --- | --- |
| Repository, base branch and reviewed workflow revision | Pending |
| Owner/operator and independent reviewer | Pending |
| Runner group and repository/workflow access | Pending; include reusable job-defining workflows |
| OS/architecture and complete labels | Pending |
| Service account and allowed tool/network access | Pending |
| Isolation from production, credentials and other workspaces | Pending |
| Workspace/worker disposal or reviewed cleanup | Pending |
| Redacted local evidence storage, access and retention | Pending; no GitHub artifact upload |
| Existing stronger quality/workflow/hosting gates | Pending; preserve them |

Use a dedicated project label with `self-hosted`, the actual OS and architecture.
The Backbone source label `backbone-ci` is not a default grant to another project.
All required labels and group restrictions must match. The checked-in
[local CI example](local-ci.yml.example) is inactive outside `.github/workflows/`.
Select the actual repository/branch/labels and real native build/test/check commands
in a reviewed adoption PR before activating it. It intentionally fails when those
commands or the repository assertion are unconfigured.

This example is an adoption aid, not a replacement for an installed workflow kit's
trusted configuration/execution separation, strict aggregate, activation history,
attestation or quality duties. Replacing its artifact transport needs a separately
reviewed integration. Do not remove stronger gates to use this simpler example.

## Observations

| Layer | Actual identity / command / timestamp | Result and remaining gaps |
| --- | --- | --- |
| Local prerequisites under service account | Doctor profile and reviewed tool revision | Pending |
| GitHub availability | Repository runner view: name, full labels, Idle/Active/Offline, group access | Pending |
| Actual job allocation | Run/job URL, exact candidate SHA, assigned runner | Pending |
| Required checks | Actual command/check IDs, exit codes and scope | Pending |
| Deliberate negative gate | Invalid required input/check and observed blocking behavior | Pending |
| Evidence retention and cleanup | Actual action and responsible operator | Pending |
| Independent acceptance/human gate | Review identities, applicable decision and unresolved gates | Pending |

A local prerequisite PASS does not prove registration, label access, isolation or
completed CI. A queued/skipped job has not passed its required checks. No fleet
availability follows from this template; absence of inventory/access evidence
stays visible. Record the owner and next action for each pending/blocked item.

Source hints: original Backbone record informed by GitHub's
[runner routing](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow),
[group access](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)
and [security guidance](https://docs.github.com/en/actions/reference/security/secure-use),
inspected 2026-10-21. These sources explain mechanisms/risks; they do not require
our label names or certify a worker. No credential or registration token belongs
in this record.
