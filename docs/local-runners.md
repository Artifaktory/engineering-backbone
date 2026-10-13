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
- Backbone [run 38427484521](https://github.com/Artifaktory/engineering-backbone/actions/runs/38427484521)
  at published head `19fb75b640a470b459119f1654f5e43d3c1aef2b` now proves repository
  access: both quality jobs ran on `pc2-build` in `af-ci-build-v1`. Trusted base
  policy succeeded; Foundation's 239-test run failed with 19 Python-loader errors.
  This proves placement, not completed runtime acceptance or clean isolation.
- Granting runner-group access, registering runners or changing repository settings
  is outside this workflow PR. Keep it draft until access, isolation and actual
  source-job runner names/groups are independently verified.
- Use isolated CI machines/users and clean workspaces, separate from developer
  data, credentials and unrelated repositories. Same-repository PR guards are
  candidate-editable mitigation, not immutable protection. Repository-wide runner
  access/approval restrictions need independent verification before activation.
- Preserve Python3.12 and the existing pinned setup actions. No native Windows/macOS
  jobs exist in the Backbone source, so its source routing needs only Linux x64.
- The selected Python3.12 interpreter must also start in the workflow kit's
  deliberately filtered child environment, without `LD_LIBRARY_PATH`, `PYTHONPATH`
  or other parent injection variables. The observed self-hosted tool-cache Python
  cannot locate `libpython3.12.so.1.0` in that environment. Certify a runner-owned
  loader-compatible installation/tool cache and repeat the actual suite before
  activation. Do not broaden the trusted environment allowlist, bypass tests,
  patch a shared tool cache in a PR job or mutate host loader configuration from
  candidate CI. Runner provisioning is outside this workflow PR.
- A missing runner leaves jobs queued; the source branch has no hosted fallback.
  Mandatory aggregate gates still reject failed, skipped or cancelled dependencies.

## Verification and recovery

Source pull requests with a foreign or absent head repository fail in the first
fixed step of both existing quality checks, before checkout/setup. The original
check names remain scheduled, so conditional skips cannot turn that refusal into
a successful required check. The reusable governance branch retains external
consumer behavior; repository identity, not source_mode, selects source refusal.
These workflow guards remain candidate-editable mitigation and require the
independently verified repository controls described above.

Run the commands in `CONTRIBUTING.md`, including the complete unittest suite and
the previous trusted base's validator. `tests/test_local_runners.py` checks source
and external consumer routing, rejects hosted/missing-group/caller-controlled
selection, and executes both aggregate gate scripts with success/failure/skipped/
cancelled inputs. These checks prove the static contract and actual gate logic;
only GitHub job records prove runner access and execution.

For Python certification, execute the selected interpreter in a minimal child
environment matching the relevant allowlist, then run the full suite on the same
runner. A normal parent-shell `python --version` does not prove this condition:

```python
import os
import subprocess
import sys

allowed = {'PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR', 'TEMP', 'TMP',
           'SystemRoot', 'COMSPEC', 'PATHEXT', 'DOTNET_ROOT',
           'DOTNET_ROOT_X64', 'DOTNET_CLI_TELEMETRY_OPTOUT',
           'DOTNET_NOLOGO', 'PYTHONUTF8', 'PYTHONIOENCODING'}
environment = {key: value for key, value in os.environ.items() if key in allowed}
subprocess.run([sys.executable, '-c', 'import sys; print(sys.version)'],
               env=environment, check=True)
```

Until merge the default branch is unchanged. A human decides merge after activation
evidence; release and downstream adoption remain separate. Recovery is a reviewed
revert PR, without silently restoring hosted source routing or weakening gates.

GitHub references: [runner labels and groups](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow),
[untrusted checkout boundaries](https://docs.github.com/en/actions/reference/security/secure-use).
