# Source CI on local runners

The 11 directly executed source job definitions select the organization group
`af-ci-build-v1` and all labels `self-hosted`, `linux`, `x64`, `ci-heavy`. The two
governance callers inherit the same selection from the reusable workflow.
Group binding is necessary: observed `ci-heavy` jobs also ran on the separate
`af-ci-fast-v1` group. Labels alone do not select only the build machines.

Reusable workflows choose this runner configuration only when `github.repository`
is `Artifaktory/engineering-backbone`. External consuming repositories retain their
existing `ubuntu-latest` default. Caller-controlled `source_mode` does not control
runner placement; templates, compiled tooling, permissions, events and validation
commands are unchanged. This PR does not distribute a new consumer bundle.

## Evidence and activation

- `Artifaktory/Artifaktory` run `37198308243` used `pc1-build` and `pc2-build` in
  `af-ci-build-v1`. Run `38379065325` confirms local operation and the overlapping
  fast-group label. These observations do **not** prove Backbone repository access.
- Granting runner-group access, registering runners or changing repository settings
  is outside this workflow PR. Keep it draft until access, isolation and actual
  source-job runner names/groups are independently verified.
- Use isolated CI machines/users and clean workspaces, separate from developer
  data, credentials and unrelated repositories. Same-repository PR guards are
  candidate-editable mitigation, not immutable protection. Repository-wide runner
  access/approval restrictions need independent verification before activation.
- Preserve Python3.12 and the existing pinned setup actions. No native Windows/macOS
  jobs exist in the Backbone source, so its source routing needs only Linux x64.
- A missing runner leaves jobs queued; the source branch has no hosted fallback.
  Mandatory aggregate gates still reject failed, skipped or cancelled dependencies.

## Verification and recovery

Run the commands in `CONTRIBUTING.md`, including the complete unittest suite and
the previous trusted base's validator. `tests/test_local_runners.py` checks source
and external consumer routing, rejects hosted/missing-group/caller-controlled
selection, and executes both aggregate gate scripts with success/failure/skipped/
cancelled inputs. These checks prove the static contract and actual gate logic;
only GitHub job records prove runner access and execution.

Until merge the default branch is unchanged. A human decides merge after activation
evidence; release and downstream adoption remain separate. Recovery is a reviewed
revert PR, without silently restoring hosted source routing or weakening gates.

GitHub references: [runner labels and groups](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow),
[untrusted checkout boundaries](https://docs.github.com/en/actions/reference/security/secure-use).
