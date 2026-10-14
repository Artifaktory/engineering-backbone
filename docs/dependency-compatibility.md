# Source dependency and container compatibility

Read the [shared dependency policy](../policy/dependencies.md) before changing
dependencies, runtimes or container inputs. This document records the source
repository's tooling environment. Consuming projects declare their own supported
combinations and keep their application Dockerfiles under their own control.

## Authoritative inputs

| Input | Responsibility |
| --- | --- |
| [requirements.txt](../requirements.txt) | Reviewed direct tooling pins. |
| [requirements.lock](../requirements.lock) | Exact direct/transitive resolution and accepted SHA256 distribution hashes. |
| [Dockerfile](../Dockerfile) | Immutable official Python base and actual tooling-image build. |
| [.dockerignore](../.dockerignore) | Build-context exclusions, including Git history, local environments and artifacts. |
| [quality workflow](../.github/workflows/quality.yml) | Clean installation, tracked-input check, image build and offline behavior smoke. |

The supported source tooling line is Python 3.12. The reference container is
Debian bookworm/Linux; source CI runs on the existing Ubuntu runner selection.
The base image includes Git, which Copier and consumer tests require. Its index
digest was retrieved from the official Docker Hub registry on 2026-10-14: the
registry digest header matched a SHA256 of the manifest response. The inspected
Linux/amd64 image configuration reports Python 3.12.15 and includes Git in its
build history. The immutable base reference lives only in the Dockerfile; changing
it requires a reviewed update and another build/smoke result.

The image supports local use from Linux or a Windows host running Linux containers.
Native Windows execution of the full suite is not attested by the Linux job;
several workflow tests execute Bash. The project's Windows-related fixtures and
line-ending checks provide their specifically recorded evidence, not a blanket
native-Windows certification. Other Python lines, image platforms or operating
systems need their own evidence before expanding the supported combination.

## Checks

Create a clean Python 3.12 environment and install the existing resolution:

```sh
python -m venv .venv
# Use the environment's Python through activation or its platform-specific path.
python -m pip install --require-hashes --only-binary=:all: -r requirements.lock
python scripts/check_source_dependencies.py
```

The source check requires the listed inputs, the shared policy and agent entrypoint
documents to be nonempty, regular, Git-tracked files. New files therefore need to
be staged before running it. It checks the source's deliberately narrow exact-pin/
SHA256 format, matching direct pins, installed locked versions, `pip check`, and
an immutable Python 3.12 bookworm base. It fails for missing, untracked, symlinked
or conflicting inputs. Run it from a real source checkout; there is no option to
silently waive Git tracking. It does not replace clean resolution, image execution,
behavior tests or security scans. The Docker build and CI clean installation use
binary distributions, so missing platform wheels fail explicitly rather than
introducing unreviewed build dependencies from source distributions.

Build the actual tracked Dockerfile and run the same offline smoke as CI:

```sh
docker build --pull --tag backbone-tooling:check --file Dockerfile .
docker run --rm --network none backbone-tooling:check
docker run --rm --network none backbone-tooling:check python scripts/compile_toolchain_fingerprint.py --check
docker run --rm --network none backbone-tooling:check python -m unittest tests.test_copier -v
```

The image runs as an unprivileged account with its own home and writable temporary storage.
It contains no Git history; the tracked-input check runs in the CI checkout before
the build. Real Copier tests initialize temporary Git repositories inside the
container. CI additionally checks all generated compiler outputs in the image.
Builds need registry/package-index access; smoke execution has networking disabled.
If Docker is unavailable locally, record that result as unexecuted and obtain the
actual CI container result before claiming container compatibility.

## Updates and evidence

Keep direct pins and the resolved lock coherent. Regenerate the lock with the
existing [maintenance procedure](../CONTRIBUTING.md), review direct and transitive
changes, and run source checks, compilers, the full unit/consumer suite and the
container job. A lock update or successful `pip check` alone does not establish
behavioral compatibility. Record commands, revisions, tested platforms and any
unexecuted checks through the existing review chain.

This source repository has no active consumer navigation/workflow-kit contract.
Its direct [agent entrypoint](../AGENTS.md), [contributor guide](../CONTRIBUTING.md)
and source CI make these actual files reachable and checked. Installing the shared
policy in a consumer does not create its application Dockerfile or activate an
incomplete dependency contract; follow [the navigation guide](agent-navigation.md)
for the consumer's reviewed adoption and handoff path.
