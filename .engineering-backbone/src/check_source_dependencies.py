#!/usr/bin/env python3
"""Check this source repository's tracked dependency inputs and installed resolution.

This bounded check accepts the exact-pin/hash format used here. It is not a
general package resolver, vulnerability scanner or behavioral compatibility proof.
Run in a clean Python 3.12 environment installed from requirements.lock.
"""
from __future__ import annotations

import argparse
import importlib.metadata
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PATHS = (
    'AGENTS.md', 'CONTRIBUTING.md', 'docs/quality/dependencies.md',
    'docs/operations/engineering/dependency-compatibility.md', 'infra/docker/engineering-backbone/Dockerfile', '.dockerignore',
    '.engineering-backbone/requirements.txt', '.engineering-backbone/requirements.lock', '.engineering-backbone/src/check_source_dependencies.py',
    '.github/workflows/quality.yml',
)
PIN = re.compile(r'([A-Za-z0-9][A-Za-z0-9_.-]*)==([0-9][A-Za-z0-9.!+_-]*)\Z')
HASH = re.compile(r'--hash=sha256:[0-9a-f]{64}\Z')
BASE = re.compile(r'FROM python:3\.12-bookworm@sha256:[0-9a-f]{64}\Z')


class DependencyError(ValueError):
    """An input or installed dependency violates the source contract."""


def regular_file(root: Path, name: str) -> Path:
    path = root
    for part in Path(name).parts:
        path /= part
        if path.is_symlink():
            raise DependencyError(f'symlinked required input: {name}')
    if not path.is_file() or not path.read_bytes().strip():
        raise DependencyError(f'missing, empty or non-regular required input: {name}')
    return path


def parse_pins(text: str, *, hashed: bool) -> dict[str, str]:
    """Reject unsupported resolution syntax instead of interpreting it loosely."""
    records = []
    pending = ''
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            if pending:
                raise DependencyError(f'interrupted requirement continuation at line {number}')
            continue
        continued = line.endswith('\\')
        pending += (' ' if pending else '') + (line[:-1].rstrip() if continued else line)
        if not continued:
            records.append(pending)
            pending = ''
    if pending:
        raise DependencyError('unfinished requirement continuation')
    pins = {}
    for record in records:
        fields = record.split()
        if not fields:
            raise DependencyError('empty package requirement')
        match = PIN.fullmatch(fields[0])
        if not match:
            raise DependencyError(f'expected exact package pin: {fields[0]}')
        name = re.sub(r'[-_.]+', '-', match[1]).lower()
        if name in pins:
            raise DependencyError(f'duplicate package pin: {name}')
        if hashed:
            if len(fields) < 2 or any(not HASH.fullmatch(item) for item in fields[1:]):
                raise DependencyError(f'expected SHA256 hashes for locked package: {name}')
        elif len(fields) != 1:
            raise DependencyError(f'unsupported direct requirement syntax: {name}')
        pins[name] = match[2]
    if not pins:
        raise DependencyError('dependency manifest or resolution is empty')
    return pins


def check_tracking(root: Path) -> None:
    git = ['git', '-c', 'core.fsmonitor=false', '-c', 'submodule.recurse=false']
    top = subprocess.run(git + ['rev-parse', '--show-toplevel'], cwd=root,
                         capture_output=True, text=True, check=False, timeout=30)
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        raise DependencyError('source root must be the Git checkout root')
    result = subprocess.run(git + ['ls-files', '--stage', '-z', '--', *REQUIRED_PATHS],
                            cwd=root, capture_output=True, text=True,
                            check=False, timeout=30)
    if result.returncode:
        raise DependencyError('cannot inspect tracked source inputs')
    tracked = {}
    for entry in result.stdout.split('\0'):
        if not entry:
            continue
        metadata, name = entry.split('\t', 1)
        mode, _object_id, stage = metadata.split()
        if mode not in {'100644', '100755'} or stage != '0' or name in tracked:
            raise DependencyError(f'non-regular or conflicted tracked input: {name}')
        tracked[name] = mode
    missing = set(REQUIRED_PATHS) - set(tracked)
    if missing:
        raise DependencyError('required inputs are not Git-tracked: ' + ', '.join(sorted(missing)))


def check_inputs(root: Path) -> dict[str, str]:
    for name in REQUIRED_PATHS:
        regular_file(root, name)
    check_tracking(root)
    dockerfile = (root / 'infra/docker/engineering-backbone/Dockerfile').read_text(encoding='utf-8')
    from_lines = [line.strip() for line in dockerfile.splitlines()
                  if re.match(r'\s*FROM\b', line, re.I)]
    if len(from_lines) != 1 or not BASE.fullmatch(from_lines[0]):
        raise DependencyError('Dockerfile requires one immutable Python 3.12 bookworm base')
    direct = parse_pins((root / '.engineering-backbone/requirements.txt').read_text(encoding='utf-8'), hashed=False)
    locked = parse_pins((root / '.engineering-backbone/requirements.lock').read_text(encoding='utf-8'), hashed=True)
    for name, version in direct.items():
        if locked.get(name) != version:
            raise DependencyError(f'direct pin and locked resolution differ: {name}')
    return locked


def check_installed(locked: dict[str, str]) -> None:
    for name, expected in locked.items():
        try:
            actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise DependencyError(f'locked package is not installed: {name}') from exc
        if actual != expected:
            raise DependencyError(f'installed version differs from lock: {name} ({actual} != {expected})')
    result = subprocess.run([sys.executable, '-I', '-m', 'pip', 'check'],
                            capture_output=True, text=True, check=False, timeout=120)
    if result.returncode:
        raise DependencyError('installed dependency metadata is inconsistent:\n' +
                              result.stdout.strip() + '\n' + result.stderr.strip())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        if sys.version_info[:2] != (3, 12):
            raise DependencyError('source tooling requires Python 3.12')
        locked = check_inputs(args.root.resolve())
        check_installed(locked)
    except (DependencyError, OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: tracked source inputs, {len(locked)} installed locked versions and declared dependency consistency')
    print('Build, consumer tests and container execution provide separate behavioral evidence.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
