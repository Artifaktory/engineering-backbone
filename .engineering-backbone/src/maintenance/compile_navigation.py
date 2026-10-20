#!/usr/bin/env python3
"""Compile reviewed technology authority and navigation into the quality guard.

Source maintenance only: inspect text/AST, never import a candidate resolver.
Run before compile_quality_framework and compile_toolchain_fingerprint.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
START = '    # BEGIN COMPILED NAVIGATION GUARD'
END = '    # END COMPILED NAVIGATION GUARD'


def read_json(path):
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file() or path.stat().st_size > 262144:
        raise ValueError('Absent, linked or oversized technology authority: ' + str(path))
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate technology authority key')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON number')))


def technology_catalog(source):
    directory = source / '.engineering-backbone/standards/technologies'
    sections = {}
    for name in ('sources', 'rules'):
        data = read_json(directory / (name + '.json'))
        if (not isinstance(data, dict) or set(data) != {'schema_version', 'version', name}
                or data['schema_version'] != '1' or not isinstance(data[name], list)):
            raise ValueError('Invalid technology catalog wrapper: ' + name)
        sections[name] = data
    if sections['sources']['version'] != sections['rules']['version']:
        raise ValueError('Mixed technology catalog versions')
    profile_dir = directory / 'profiles'
    if profile_dir.is_symlink() or not profile_dir.is_dir():
        raise ValueError('Absent or linked technology profiles')
    profiles = []
    for path in sorted(profile_dir.iterdir()):
        if path.suffix != '.json':
            raise ValueError('Unexpected technology profile entry')
        profile = read_json(path)
        if not isinstance(profile, dict) or profile.get('id') != path.stem:
            raise ValueError('Technology profile identity differs from filename')
        profiles.append(profile)
    if not profiles:
        raise ValueError('Empty technology catalog')
    catalog = {'version': sections['rules']['version'], 'sources': sections['sources']['sources'],
               'rules': sections['rules']['rules'], 'profiles': profiles}
    validate_catalog(catalog, source)
    return catalog


def validate_catalog(catalog, source):
    """Reject malformed reviewed inputs before producing any trusted executable."""
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def text(value):
        return isinstance(value, str) and bool(value.strip()) and len(value) <= 16384

    def strings(value, *, nonempty=True):
        return (isinstance(value, list) and len(value) <= 256 and
                (bool(value) or not nonempty) and all(text(item) for item in value)
                and len(value) == len(set(value)))

    require(isinstance(catalog['version'], str) and
            re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', catalog['version']),
            'Invalid technology catalog version')
    identities = {}
    for section in ('sources', 'rules', 'profiles'):
        records = catalog[section]
        require(isinstance(records, list) and 1 <= len(records) <= 256,
                'Empty or oversized technology section: ' + section)
        ids = []
        for record in records:
            require(isinstance(record, dict) and isinstance(record.get('id'), str)
                    and re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,63}', record['id']),
                    'Invalid technology identity')
            ids.append(record['id'])
        require(len(ids) == len(set(ids)), 'Duplicate technology identity')
        identities[section] = set(ids)
    for item in catalog['sources']:
        require(set(item) == {'id', 'title', 'edition', 'url', 'status', 'access',
                             'adoption', 'verified_sections'}, 'Invalid technology source shape')
        require(all(text(item[key]) for key in item if key != 'verified_sections')
                and item['url'].startswith('https://') and strings(item['verified_sections']),
                'Invalid technology source provenance')
    kinds = {'docs', 'build', 'lint', 'test', 'typecheck', 'browser', 'api', 'migration',
             'sast', 'dependency', 'container', 'iac', 'release-integrity', 'provenance',
             'signature', 'sbom', 'deployment-smoke', 'rollback', 'monitoring'}
    for item in catalog['rules']:
        require(set(item) == {'id', 'version', 'statement', 'source_ids', 'source_alignment',
                             'check_kind_groups'}, 'Invalid technology rule shape')
        require(item['id'].startswith('TECH-') and item['version'] == '1'
                and text(item['statement']) and text(item['source_alignment'])
                and strings(item['source_ids'])
                and not set(item['source_ids']) - identities['sources'],
                'Invalid technology rule version or source reference')
        groups = item['check_kind_groups']
        require(isinstance(groups, list) and 1 <= len(groups) <= 32 and
                all(strings(group) and not set(group) - kinds for group in groups),
                'Invalid technology check-kind groups')
    core_profiles = {path.stem: read_json(path) for path in (source / '.engineering-backbone/standards/profiles').glob('*.json')}
    for item in catalog['profiles']:
        require(set(item) == {'id', 'version', 'category', 'description', 'rules',
                             'quality_profiles', 'recommendations', 'free_choices'},
                'Invalid technology profile shape')
        require(item['version'] == '1' and text(item['category']) and text(item['description'])
                and strings(item['rules']) and not set(item['rules']) - identities['rules']
                and strings(item['quality_profiles'], nonempty=False) and strings(item['recommendations'])
                and strings(item['free_choices']), 'Invalid technology profile fields or rule reference')
        require(all(key in core_profiles and core_profiles[key].get('enabled') is True
                    for key in item['quality_profiles']),
                'Unknown or inactive core quality prerequisite')


def compiled_resolver(content, authority):
    functions = [node for node in ast.parse(content).body
                 if isinstance(node, ast.FunctionDef) and node.name == 'navigation_context']
    if len(functions) != 1 or functions[0].decorator_list:
        raise ValueError('Expected one undecorated self-contained navigation_context')
    assignments = [node for node in functions[0].body if isinstance(node, ast.Assign)
                   and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                   and node.targets[0].id == 'technology_catalog_json']
    if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Constant):
        raise ValueError('Expected literal compiler-owned technology_catalog_json')
    node = assignments[0]
    if not isinstance(node.value.value, str):
        raise ValueError('Technology authority must be a string literal')
    lines = content.splitlines(keepends=True)
    indent = lines[node.lineno - 1][:node.col_offset]
    encoded = json.dumps(authority, ensure_ascii=False, separators=(',', ':'))
    lines[node.lineno - 1:node.end_lineno] = [indent + 'technology_catalog_json = ' + repr(encoded) + '\n']
    return ''.join(lines)


def function_text(content):
    nodes = [node for node in ast.parse(content).body
             if isinstance(node, ast.FunctionDef) and node.name == 'navigation_context']
    if len(nodes) != 1:
        raise ValueError('Expected one navigation function')
    node = nodes[0]
    return '\n'.join(content.splitlines()[node.lineno - 1:node.end_lineno])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--source', type=Path, default=ROOT)
    args = parser.parse_args(argv)
    source = args.source.resolve()
    try:
        path = source / '.engineering-backbone/src/navigation.py'
        current = path.read_text(encoding='utf-8')
        expected = compiled_resolver(current, technology_catalog(source))
        target = source / '.engineering-backbone/src/quality_framework.py'
        original = target.read_text(encoding='utf-8')
        body = '\n'.join('    ' + line if line else '' for line in function_text(expected).splitlines())
        pattern = re.compile(r'(?m)^(' + re.escape(START) + r'\n).*?(^' + re.escape(END) + r'$)', re.S)
        updated, count = pattern.subn(lambda match: match.group(1) + body + '\n' + match.group(2), original)
        if count != 1:
            raise ValueError('Expected one nested navigation guard block')
        changes = [(path, current, expected), (target, original, updated)]
        if args.write:
            for file, old, new in changes:
                if old != new:
                    file.write_text(new, encoding='utf-8')
            print('PASS: reviewed technology authority and navigation compiled')
        else:
            stale = [str(file.relative_to(source)) for file, old, new in changes if old != new]
            if stale:
                raise ValueError('Stale navigation authority: ' + ', '.join(stale))
            print('PASS: compiled technology and navigation authority match source')
        return 0
    except (OSError, UnicodeError, ValueError, SyntaxError) as exc:
        print('FAIL: ' + str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
