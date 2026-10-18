#!/usr/bin/env python3
"""Compile the pinned workflow's authority from actual Copier-rendered tooling.

This is a source maintenance command, never part of consumer execution. Historical
fingerprints are explicit reviewed workflow literals, not consumer-supplied input.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

from copier import run_copy
import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'validate.py', 'requirements.txt', 'requirements.lock',
    'schemas/core-policy.schema.json', 'schemas/project.schema.json',
    'schemas/task-packet.schema.json', 'schemas/review-evidence.schema.json',
    'schemas/requirement.schema.json',
)
FORMAT = 'engineering-backbone-toolchain-v1'

COPILOT_START = '# BEGIN COMPILED COPILOT GUARD'
COPILOT_END = '# END COMPILED COPILOT GUARD'
CODEX_START = '# BEGIN COMPILED CODEX GUARD'
CODEX_END = '# END COMPILED CODEX GUARD'
OPENCODE_START = '# BEGIN COMPILED OPENCODE GUARD'
OPENCODE_END = '# END COMPILED OPENCODE GUARD'


def guard_function(name: str, source: Path = ROOT):
    """Extract trusted source text without importing or executing its module."""
    content = (source / 'scripts/validate.py').read_text(encoding='utf-8')
    tree = ast.parse(content)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError(f'Expected exactly one self-contained {name} guard function')
    node = matches[0]
    return '\n'.join(content.splitlines()[node.lineno - 1:node.end_lineno])


def copilot_function(source: Path = ROOT):
    return guard_function('copilot_errors', source)


def compiled_copilot_guard(source: Path = ROOT):
    function = copilot_function(source)
    return '\n'.join('          ' + line if line else '' for line in function.splitlines())


def replace_copilot_guard(workflow: str, source: Path = ROOT):
    pattern = re.compile(r'(?m)^(          ' + re.escape(COPILOT_START) + r'\n).*?(^          ' + re.escape(COPILOT_END) + r'$)', re.S)
    compiled = compiled_copilot_guard(source)
    refreshed, count = pattern.subn(lambda match: match.group(1) + compiled + '\n' + match.group(2), workflow)
    if count != 1:
        raise ValueError('Expected exactly one compiled Copilot workflow guard block')
    return refreshed


def replace_codex_guard(workflow: str, source: Path = ROOT):
    pattern = re.compile(r'(?m)^(          ' + re.escape(CODEX_START) + r'\n).*?(^          ' + re.escape(CODEX_END) + r'$)', re.S)
    compiled = '\n'.join('          ' + line if line else ''
                         for line in guard_function('codex_errors', source).splitlines())
    refreshed, count = pattern.subn(lambda match: match.group(1) + compiled + '\n' + match.group(2), workflow)
    if count != 1:
        raise ValueError('Expected exactly one compiled Codex workflow guard block')
    return refreshed



def replace_opencode_guard(workflow: str, source: Path = ROOT):
    pattern = re.compile(r'(?m)^(          ' + re.escape(OPENCODE_START) + r'\n).*?(^          ' + re.escape(OPENCODE_END) + r'$)', re.S)
    compiled = '\n'.join('          ' + line if line else ''
                         for line in guard_function('opencode_errors', source).splitlines())
    refreshed, count = pattern.subn(lambda match: match.group(1) + compiled + '\n' + match.group(2), workflow)
    if count != 1:
        raise ValueError('Expected exactly one compiled OpenCode workflow guard block')
    return refreshed


def bundle_digest(root: Path):
    bundle = root / '.engineering-backbone'
    hashes = {}
    for name in FILES:
        path = bundle / name
        components = [bundle, path]
        if '/' in name:
            components.append(path.parent)
        if any(component.is_symlink() for component in components) or not path.is_file():
            raise ValueError(f'Absent or symlinked toolchain file: {name}')
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    canonical = json.dumps({'format': FORMAT, 'files': hashes}, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(canonical).hexdigest()


def rendered_digest(source: Path = ROOT):
    # Copier must read current working-tree bytes, including uncommitted repairs.
    # A direct run_copy(live_git, vcs_ref=HEAD) would use a different snapshot.
    with tempfile.TemporaryDirectory(prefix='backbone-fingerprint-') as temp:
        workspace = Path(temp)
        plain = workspace / 'source'
        shutil.copytree(source, plain, ignore=shutil.ignore_patterns(
            '.git', 'artifacts', '.venv', 'venv', 'node_modules', '__pycache__'))
        # Git cannot distribute empty directories. Ignore leftover local empty
        # template scaffolding without modifying the actual source checkout.
        for directory in sorted((path for path in plain.rglob('*') if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        consumer = workspace / 'consumer'
        run_copy(str(plain), consumer, defaults=True, quiet=True, skip_tasks=True)
        return bundle_digest(consumer)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='Check the workflow current literal against rendered source')
    mode.add_argument('--write', action='store_true', help='Refresh the current literal; review the resulting diff')
    parser.add_argument('--source', type=Path, default=ROOT, help='Trusted source directory to render')
    args = parser.parse_args(argv)
    digest = rendered_digest(args.source.resolve())
    workflow_path = args.source / '.github/workflows/governance-checks.yml'
    if args.write:
        text = workflow_path.read_text(encoding='utf-8')
        text, count = re.subn(r"CURRENT_TOOLCHAIN_SHA256: '[0-9a-f]{64}'", f"CURRENT_TOOLCHAIN_SHA256: '{digest}'", text)
        if count != 1:
            parser.error('Expected exactly one current workflow fingerprint literal')
        text = replace_copilot_guard(text, args.source.resolve())
        text = replace_codex_guard(text, args.source.resolve())
        text = replace_opencode_guard(text, args.source.resolve())
        workflow_path.write_text(text, encoding='utf-8')
    if args.check:
        text = workflow_path.read_text(encoding='utf-8')
        if replace_copilot_guard(text, args.source.resolve()) != text:
            print('FAIL: compiled Copilot workflow guard is stale; regenerate trusted source guard')
            return 1
        if replace_codex_guard(text, args.source.resolve()) != text:
            print('FAIL: compiled Codex workflow guard is stale; regenerate trusted source guard')
            return 1
        if replace_opencode_guard(text, args.source.resolve()) != text:
            print('FAIL: compiled OpenCode workflow guard is stale; regenerate trusted source guard')
            return 1
        workflow = yaml.safe_load(text)
        step = next(step for step in workflow['jobs']['validate']['steps']
                    if step.get('name') == 'Validate generated consumer with trusted tooling')
        if step['env']['CURRENT_TOOLCHAIN_SHA256'] != digest:
            print(f'FAIL: workflow toolchain fingerprint is stale; rendered source is {digest}')
            return 1
        print(f'PASS: pinned workflow current fingerprint matches actual rendered tooling: {digest}')
    else:
        print(digest)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
