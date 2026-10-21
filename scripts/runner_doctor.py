"""Check local prerequisites without installing or registering a CI runner.

Only fixed probes execute. Captured tool output and environment values are never
printed. A successful result does not attest GitHub access, labels or isolation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import platform
import shutil
import subprocess
import sys


PROFILES = ("development", "source-linux", "source-windows")
TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class Check:
    name: str
    status: str


def probe(name: str, executable: str, arguments: tuple[str, ...], *,
          resolve: bool = True, required_output: bytes | None = None) -> Check:
    """Run a fixed local capability probe; never surface child output/errors."""
    command = shutil.which(executable) if resolve else executable
    if not command:
        return Check(name, "missing")
    try:
        result = subprocess.run(
            [command, *arguments], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS, check=False, shell=False)
    except subprocess.TimeoutExpired:
        return Check(name, "timeout")
    except OSError:
        return Check(name, "failed")
    if result.returncode != 0:
        return Check(name, "failed")
    if required_output is not None and required_output not in result.stdout.lower():
        return Check(name, "failed")
    return Check(name, "ok")


def diagnose(profile: str) -> list[Check]:
    """Observe this process/platform; a selected profile is not platform proof."""
    if profile not in PROFILES:
        raise ValueError("unsupported doctor profile")
    results = [Check("python-3.12", "ok" if sys.version_info[:2] == (3, 12) else "failed")]
    if profile.startswith("source-"):
        expected = "Linux" if profile == "source-linux" else "Windows"
        results.extend([
            Check("operating-system", "ok" if platform.system() == expected else "failed"),
            Check("x64-architecture", "ok" if platform.machine().casefold()
                  in {"x86_64", "amd64"} else "failed"),
        ])
    results.append(probe("python-venv-modules", sys.executable,
                         ("-I", "-c", "import venv, ensurepip"), resolve=False))
    results.append(probe("git", "git", ("--version",)))
    if profile == "source-windows":
        # Git for Windows Bash identifies its MSYS build in --version output.
        # A WSL bash.exe on PATH is not the Git Bash required by these jobs.
        results.append(probe("git-bash", "bash", ("--version",), required_output=b"msys"))
        powershell = "pwsh" if shutil.which("pwsh") else "powershell"
        results.append(probe("powershell", powershell,
                             ("-NoLogo", "-NoProfile", "-NonInteractive", "-Command", "exit 0")))
    else:
        results.append(probe("bash", "bash", ("--version",)))
    if profile == "source-linux":
        results.append(probe("docker-cli", "docker", ("--version",)))
        results.append(probe("docker-daemon", "docker", ("info", "--format", "{{.ServerVersion}}")))
    return results


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "ERROR: invalid doctor options; use --help.\n")


def main(argv=None) -> int:
    parser = SafeParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILES, default="development",
                        help="development excludes Docker; source profiles require the observed OS/X64")
    args = parser.parse_args(argv)
    checks = diagnose(args.profile)
    for check in checks:
        print(f"{check.name}: {check.status}")
    passed = all(check.status == "ok" for check in checks)
    print("Prerequisite checks passed." if passed else "Prerequisite checks failed.")
    print("Runner registration, labels, repository/group access, isolation and completed CI are not verified.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
