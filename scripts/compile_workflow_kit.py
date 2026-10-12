#!/usr/bin/env python3
"""Compile the self-contained trusted workflow kit into its pinned entry points.

This maintenance tool extracts source text with AST; it never imports candidate
modules. Consumer jobs execute only the function embedded in reviewed workflows.
The existing eight-file governance fingerprint format is unchanged.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '# BEGIN COMPILED WORKFLOW KIT GUARD'
END = '# END COMPILED WORKFLOW KIT GUARD'
TARGETS = (
    ('scripts/validate.py', ''),
    ('.github/workflows/workflow-kit-pr.yml', '          '),
    ('.github/workflows/workflow-kit-maintenance.yml', '          '),
)


def kit_function(source: Path = ROOT):
    """Return one trusted function's exact source without executing its module."""
    content = (source / 'scripts/workflow_kit.py').read_text(encoding='utf-8')
    matches = [node for node in ast.parse(content).body
               if isinstance(node, ast.FunctionDef) and node.name == 'workflow_kit_main']
    if len(matches) != 1 or matches[0].decorator_list:
        raise ValueError('Expected one undecorated self-contained workflow_kit_main function')
    node = matches[0]
    return '\n'.join(content.splitlines()[node.lineno - 1:node.end_lineno])


def replace_kit_guard(content: str, function: str, indent: str):
    pattern = re.compile(r'(?m)^' + re.escape(indent + START) + r'\n.*?^'
                         + re.escape(indent + END) + r'$', re.S)
    replacement = indent + START + '\n' + '\n'.join(
        indent + line if line else '' for line in function.splitlines()) + '\n' + indent + END
    refreshed, count = pattern.subn(lambda match: replacement, content)
    if count != 1:
        raise ValueError('Expected exactly one compiled workflow kit guard block')
    return refreshed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--source', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        function = kit_function(args.source)
        changes = []
        for name, indent in TARGETS:
            path = args.source / name
            content = path.read_text(encoding='utf-8')
            refreshed = replace_kit_guard(content, function, indent)
            if refreshed != content:
                changes.append((path, refreshed))
        if args.write:
            for path, refreshed in changes:
                path.write_text(refreshed, encoding='utf-8')
            print('PASS: trusted workflow kit compiled into validator and reusable workflows')
            return 0
        if changes:
            for path, _ in changes:
                print('FAIL: stale compiled workflow kit guard: ' + str(path.relative_to(args.source)))
            return 1
        print('PASS: compiled workflow kit entry points match trusted source')
        return 0
    except (OSError, SyntaxError, ValueError) as exc:
        print('FAIL: ' + str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
