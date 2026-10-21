# Reproducible development start

This guide separates the **Backbone source tooling** commands below from a
receiving project's own application commands. Product directories are placeholders;
copying them does not install a runtime, application, build or test suite. Use the
[adoption guide](../agent-governance/adoption.md) for the selected starter route and
[configuration guide](configuration.md) for environment values and credential access.

## Project command map

During adoption, keep one authoritative map of the project's actual commands.
Reference native manifests, lockfiles and tool configuration instead of maintaining
another version list. Equivalent records in an existing contributor guide are valid.

| Operation | Record for each applicable component |
| --- | --- |
| Prerequisites | Supported OS/architecture, runtime/tool versions and their authoritative files; required external services and access. |
| Setup | Working directory, reproducible native install command and reviewed lock/resolution; local configuration steps without secret values. |
| Run | Working directory, command, readiness observation and safe stop procedure. |
| Build/package | Command, expected artifact identity/location and supported target. |
| Test | Command, covered scope/environment and where actual results are retained. |
| Check | Lint/type/security/document checks and their existing workflow check IDs. |

For every command, state its expected observable result, required permissions,
network/service assumptions and responsible owner. Mark a missing command
**unconfigured**, with an owner and next action. Justified non-applicability is
different from successful execution. For example, a source library may have no
standalone run command; a documentation project may use a document build.

Use the same native commands locally and in CI where they establish the same
claim. Keep the [workflow contract](engineering/workflows/README.md) authoritative
for adopted executable check IDs and gates; this map does not introduce another
task runner. Test data, mocks and real external services must have explicit limits
under the [testing contract](../quality/testing.md). Record a failed or unexecuted
step before handing work to another person or agent.

## Backbone source tooling: actual setup

These commands are for this repository's Python tooling. They are not a default
application stack. Use Python 3.12 and Git; the full source suite also exercises
Bash and real temporary Git/Copier repositories. Read the supported combinations
and container limits in [dependency compatibility](engineering/dependency-compatibility.md).
Run commands from the repository root.

Linux or another supported POSIX shell with the selected interpreter:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r .engineering-backbone/requirements.lock
.venv/bin/python scripts/runner_doctor.py --profile development
```

Windows PowerShell with the Python launcher and Python 3.12 installed:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes --only-binary=:all: -r .engineering-backbone/requirements.lock
.\.venv\Scripts\python.exe scripts/runner_doctor.py --profile development
```

If the launcher or named interpreter is unavailable, select and verify an actual
Python 3.12 executable first. The explicit environment paths avoid activation and
PowerShell execution-policy assumptions. Installation needs access to the reviewed
package distributions; an unavailable wheel is a failure, not permission to loosen
the lock. Do not install application dependencies into this tooling environment.

## Backbone source tooling: actual checks

Use the environment's interpreter for every `python` command in this list:
`.venv/bin/python` on Linux or `.\.venv\Scripts\python.exe` on Windows.

```sh
python .engineering-backbone/src/validate.py
python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check
python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check
python .engineering-backbone/src/maintenance/compile_navigation.py --check
python .engineering-backbone/src/maintenance/compile_quality_framework.py --check
python .engineering-backbone/src/check_source_dependencies.py
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
```

Follow [CONTRIBUTING](../../CONTRIBUTING.md) for the actual base-owned validator,
independent reviews and final committed base/head whitespace check. The full
suite's Windows execution needs its own actual evidence; a Linux run or a
Windows-related fixture does not qualify every native Windows path. The source
container build/smoke commands are in the compatibility guide. Docker is required
for that selected check, not for every development task.

The [local runner doctor and onboarding](engineering/source-ci.md) distinguish
machine prerequisites from runner registration/access and completed CI. A local
doctor success is not an application test, a connected runner or a release gate.

Source note: these are original project instructions implementing reproducible
setup and check traceability. [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)
informs toolchain and verification discipline; it does not prescribe these commands,
Python, directory names or a universal development method.
