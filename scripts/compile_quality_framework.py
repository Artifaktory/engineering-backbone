#!/usr/bin/env python3
"""Compile reviewed quality catalog/guard without importing candidate code."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '# BEGIN COMPILED QUALITY GUARD'
END = '# END COMPILED QUALITY GUARD'


def read_catalog_json(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 262144:
        raise ValueError('Absent, linked or oversized catalog file: ' + str(path))
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate catalog key')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON number')))


def catalog(source):
    directory = source / 'standards'
    if directory.is_symlink() or (directory / 'profiles').is_symlink():
        raise ValueError('Linked catalog directory')
    sections = {}
    for name in ('sources', 'rules'):
        data = read_catalog_json(directory / (name + '.json'))
        if (not isinstance(data, dict) or set(data) != {'schema_version', 'version', name}
                or data['schema_version'] != '1' or not isinstance(data[name], list)):
            raise ValueError('Invalid catalog wrapper: ' + name)
        sections[name] = data
    if sections['sources']['version'] != sections['rules']['version']:
        raise ValueError('Mixed catalog versions')
    profiles = []
    for path in sorted((directory / 'profiles').iterdir()):
        if path.suffix != '.json':
            raise ValueError('Unexpected profile catalog entry: ' + str(path))
        profile = read_catalog_json(path)
        if not isinstance(profile, dict) or profile.get('id') != path.stem:
            raise ValueError('Profile identity differs from filename')
        profiles.append(profile)
    if not profiles:
        raise ValueError('No quality catalog profiles')
    return {'version': sections['rules']['version'],
            'sources': sections['sources']['sources'],
            'rules': sections['rules']['rules'], 'profiles': profiles}


def compiled_engine(content, reviewed_catalog):
    tree = ast.parse(content)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == 'quality_errors']
    if len(functions) != 1 or functions[0].decorator_list:
        raise ValueError('Expected one undecorated self-contained quality_errors')
    assignments = [node for node in functions[0].body if isinstance(node, ast.Assign)
                   and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                   and node.targets[0].id == 'catalog_json']
    if len(assignments) != 1:
        raise ValueError('Expected one compiler-owned catalog_json assignment')
    node = assignments[0]
    if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
        raise ValueError('Catalog authority must be a literal string')
    data = json.dumps(reviewed_catalog, ensure_ascii=False, separators=(',', ':'))
    lines = content.splitlines(keepends=True)
    indent = lines[node.lineno - 1][:node.col_offset]
    lines[node.lineno - 1:node.end_lineno] = [indent + 'catalog_json = ' + repr(data) + '\n']
    return ''.join(lines)


def function_text(content):
    nodes = [node for node in ast.parse(content).body
             if isinstance(node, ast.FunctionDef) and node.name == 'quality_errors']
    if len(nodes) != 1:
        raise ValueError('Expected one quality guard function')
    node = nodes[0]
    return '\n'.join(content.splitlines()[node.lineno - 1:node.end_lineno])


def replace_guard(content, function, indent):
    pattern = re.compile(r'(?m)^(' + re.escape(indent + START) + r'\n).*?(^'
                         + re.escape(indent + END) + r'$)', re.S)
    body = '\n'.join(indent + line if line else '' for line in function.splitlines())
    updated, count = pattern.subn(lambda match: match.group(1) + body + '\n' + match.group(2), content)
    if count != 1:
        raise ValueError('Expected exactly one compiled quality guard block')
    return updated


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    parser.add_argument('--source', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    source = args.source.resolve()
    try:
        path = source / 'scripts/quality_framework.py'
        original = path.read_text(encoding='utf-8')
        expected = compiled_engine(original, catalog(source))
        function = function_text(expected)
        replacements = [(path, original, expected)]
        for relative, indent in (('scripts/validate.py', ''),
                                 ('.github/workflows/governance-checks.yml', '          ')):
            target = source / relative
            current = target.read_text(encoding='utf-8')
            replacements.append((target, current, replace_guard(current, function, indent)))
        if args.write:
            for target, current, updated in replacements:
                if current != updated:
                    target.write_text(updated, encoding='utf-8')
            print('PASS: reviewed quality catalog and guard compiled into trusted entry points')
        else:
            stale = [str(target.relative_to(source)) for target, current, updated in replacements
                     if current != updated]
            if stale:
                print('FAIL: stale compiled quality authority: ' + ', '.join(stale))
                return 1
            print('PASS: compiled quality catalog and entry points match trusted source')
        return 0
    except (OSError, UnicodeError, ValueError, SyntaxError) as exc:
        print('FAIL: ' + str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
