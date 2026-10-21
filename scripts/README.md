# Shared project commands

Keep small repository-wide development, build and maintenance entry commands here;
delegate product commands to the owning component's native tool. The authoritative
command map is [development](../docs/operations/development.md), not a second task
runner. Backbone's source validator and compilers remain in `.engineering-backbone/src/`.

`python scripts/runner_doctor.py --profile development` checks the current Python
3.12/venv-module, Git and Bash prerequisites without requiring Docker. Use
`source-linux` or `source-windows` for the source CI prerequisites described in the
[runner runbook](../docs/operations/engineering/source-ci.md). The source profiles
also check the observed OS/X64, plus Docker CLI/daemon on Linux or Git Bash and
PowerShell on Windows. The script uses fixed argument lists and ten-second probe
timeouts, suppresses captured output, and installs/registers nothing.

Run the doctor under the actual intended account and environment. A local PASS
does not prove GitHub runner registration, labels, repository/group availability,
isolation, network download access, successful package installation or completed
CI. The venv probe imports the standard modules; the actual setup command still
has to create the environment and install its reviewed lock.
