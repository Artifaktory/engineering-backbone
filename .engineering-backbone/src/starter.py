"""Export and inspect a neutral starter from an explicitly reviewed source checkout.

This is a separate structural seed contract. It never replaces source/legacy
validation, product tests, active optional contracts or human adoption review.
"""
from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
from types import ModuleType
from urllib.parse import quote, unquote, urlsplit


SOURCE = Path(__file__).absolute().parents[2]
SCRIPT = '.engineering-backbone/src/starter.py'
MANIFEST = '.engineering-backbone/starter-manifest.json'
SOURCE_URL = 'https://github.com/Artifaktory/engineering-backbone'
MANAGED_PREFIXES = (
    'docs/agent-governance/', 'docs/quality/', 'docs/templates/', 'docs/operations/',
    '.engineering-backbone/schemas/', '.engineering-backbone/standards/',
    '.codex/', '.github/agents/', '.github/skills/', '.github/instructions/',
    '.opencode/',
)
PROJECT_PREFIXES = ('apps/', 'packages/', 'contracts/', 'tst/', '.vscode/')
MANAGED_FILES = (
    '.engineering-backbone/core.json', '.engineering-backbone/opencode.json',
    '.engineering-backbone/src/environment.py', 'scripts/runner_doctor.py',
    'opencode.json',
)
PROJECT_FILES = (
    '.env.example', 'config/environment.json', 'config/README.md',
    'scripts/README.md', 'infra/README.md', 'docs/architecture/README.md',
    'docs/requirements/README.md',
)
SEEDS = {
    'README.md': 'README.md.in', 'AGENTS.md': 'AGENTS.md.in',
    'CONTRIBUTING.md': 'CONTRIBUTING.md.in', 'SECURITY.md': 'SECURITY.md.in',
    '.github/copilot-instructions.md': 'copilot-instructions.md.in',
    'docs/changes/README.md': 'changes-README.md.in',
    'docs/operations/development.md': 'development.md.in',
    'artifacts/README.md': 'artifacts-README.md.in',
}
# This profile includes all distributed native instructions. Existence is not
# evidence of host loading, model qualification or authority to launch a host.
FLOOR = {
    'human_merge_required': True, 'human_release_required': True,
    'independent_review_required': True, 'triage_before_fix': True,
    'delta_after_fix': True, 'local_policy_may_only_strengthen': True,
    'automatic_downstream_apply': False,
}
FORBIDDEN_INSTALLATION = (
    'copier.yml', '.engineering-backbone/copier-answers.yml',
    '.engineering-backbone/validate.py', '.engineering-backbone/src/validate.py',
    '.engineering-backbone/legacy', '.engineering-backbone/tst',
)
OPTIONAL_CONTRACTS = (
    '.engineering-backbone/workflows.json', '.engineering-backbone/quality-profile.json',
    '.engineering-backbone/navigation.json', '.engineering-backbone/dependencies.json',
)
ENGINEERING_ROOTS = (
    'docs/changes', 'docs/requirements', 'docs/plans', 'docs/tasks', 'docs/reviews',
)
LINK = re.compile(r'(?P<inline>\]\()(?P<target>[^\s)]+)(?P<end>\))|(?P<reference>^\s*\[[^\]\n]+\]:\s*)(?P<ref_target>\S+)', re.M)


class StarterError(ValueError):
    """Safe diagnostic: never include candidate file contents or tool output."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args, data=None):
    try:
        result = subprocess.run(['git', '-C', str(root), *args], input=data,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise StarterError('trusted Git operation unavailable') from exc
    if result.returncode:
        raise StarterError('trusted Git operation failed')
    return result.stdout


def safe_relative(value):
    if (not isinstance(value, str) or not value or '\\' in value or '\x00' in value
            or '\n' in value or '\r' in value or ':' in value
            or value.startswith('/') or any(p in ('', '.', '..') for p in value.split('/'))):
        raise StarterError('unsafe repository-relative path')
    return value


def is_alias(path):
    # Windows directory junctions are distinct from symbolic links.
    return path.is_symlink() or path.is_junction()


def reject_alias_ancestors(path):
    if any(is_alias(component) for component in (path, *path.parents)):
        raise StarterError('linked or junctioned root/path ancestor is not accepted')


def contained_path(root, path):
    reject_alias_ancestors(path)
    try:
        if not path.resolve().is_relative_to(root.resolve()):
            raise StarterError('path resolves outside its project root')
    except RuntimeError as exc:
        raise StarterError('path cannot be resolved safely') from exc
    return path


def safe_root(value, *, must_exist=True):
    path = Path(value)
    if '..' in path.parts:
        raise StarterError('parent traversal is not accepted')
    path = path.absolute()
    reject_alias_ancestors(path)
    # Retain a physical check even if a platform does not classify an alias.
    if os.path.normcase(str(path.resolve())) != os.path.normcase(str(path)):
        raise StarterError('root resolves through an unexpected physical alias')
    if must_exist and not path.is_dir():
        raise StarterError('expected an existing directory')
    return path


def safe_file(root, relative):
    relative = safe_relative(relative)
    path = root.joinpath(*relative.split('/'))
    contained_path(root, path)
    current = root
    for part in relative.split('/'):
        current /= part
        if current.parent.is_dir():
            matches = [p.name for p in current.parent.iterdir() if p.name.casefold() == part.casefold()]
            if any(name != part for name in matches):
                raise StarterError('case-colliding managed/project path: ' + relative)
    if not path.is_file():
        raise StarterError('missing required regular file: ' + relative)
    return path


def read_json_bytes(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise StarterError('duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(data, object_pairs_hook=pairs)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise StarterError('invalid JSON document') from exc


class TrustedSource:
    def __init__(self, root, ref, *, attest_script=True):
        self.root = safe_root(root)
        if not re.fullmatch('[0-9a-f]{40}', ref or ''):
            raise StarterError('source ref must be a full immutable Git commit')
        if git(self.root, 'rev-parse', 'HEAD').decode().strip() != ref:
            raise StarterError('trusted checkout HEAD must equal source ref')
        self.ref = ref
        records = git(self.root, 'ls-tree', '-rz', '--full-tree', ref).split(b'\0')
        self.entries = {}
        for record in records:
            if not record:
                continue
            header, raw_path = record.split(b'\t', 1)
            mode, kind, sha = header.decode().split()
            path = safe_relative(raw_path.decode('utf-8'))
            self.entries[path] = (mode, kind, sha)
        if attest_script:
            path = safe_file(self.root, SCRIPT)
            if path.read_bytes() != self.blobs([SCRIPT])[SCRIPT]:
                raise StarterError('executing starter differs from its trusted Git blob')

    def blobs(self, paths):
        ordered = sorted(set(paths))
        for path in ordered:
            safe_relative(path)
            if path not in self.entries or self.entries[path][:2] != ('100644', 'blob'):
                raise StarterError('expected a tracked regular source file: ' + path)
        raw = git(self.root, 'cat-file', '--batch', data=''.join(self.ref + ':' + p + '\n' for p in ordered).encode())
        position = 0
        result = {}
        for path in ordered:
            end = raw.index(b'\n', position)
            sha, kind, size = raw[position:end].split()
            if kind != b'blob':
                raise StarterError('unexpected trusted Git object')
            position = end + 1
            length = int(size)
            result[path] = raw[position:position + length]
            position += length + 1
        return result


@dataclass(frozen=True)
class Entry:
    owner: str
    data: bytes


def excluded(path):
    name = PurePosixPath(path).name.lower()
    return (path.startswith('docs/agent-governance/sources/inventory/')
            or name.startswith('.env') and path != '.env.example'
            or name.endswith(('.pem', '.key', '.p12', '.pfx'))
            or name in ('.netrc', '.npmrc', '.pypirc', 'credentials.json'))


def exists_in_plan(path, paths):
    return path in paths or any(name.startswith(path.rstrip('/') + '/') for name in paths)


def markdown_targets(text, transform):
    # Preserve fenced examples; they are explanatory code rather than links.
    chunks = re.split(r'(```.*?```|~~~.*?~~~)', text, flags=re.S)
    for index in range(0, len(chunks), 2):
        def replace(match):
            target = match.group('target') or match.group('ref_target')
            changed = transform(target)
            if match.group('inline'):
                return match.group('inline') + changed + match.group('end')
            return match.group('reference') + changed
        chunks[index] = LINK.sub(replace, chunks[index])
    return ''.join(chunks)


def rewrite_links(relative, data, paths, source):
    if not relative.endswith('.md'):
        return data
    def target(value):
        parsed = urlsplit(value.strip('<>'))
        if parsed.scheme or parsed.netloc or not parsed.path or value.startswith(('#', '${', '<')):
            return value
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative), unquote(parsed.path)))
        safe_relative(resolved)
        if exists_in_plan(resolved, paths):
            return value
        kind = 'tree' if resolved not in source.entries else 'blob'
        url = SOURCE_URL + '/' + kind + '/' + source.ref + '/' + quote(resolved, safe='/')
        return url + ('#' + parsed.fragment if parsed.fragment else '')
    return markdown_targets(data.decode('utf-8'), target).encode()


def build_plan(source, project_name='new-project'):
    if not re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]*', project_name):
        raise StarterError('invalid project name')
    selected = {}
    for path in source.entries:
        if excluded(path):
            continue
        if any(path.startswith(prefix) for prefix in MANAGED_PREFIXES) or path in MANAGED_FILES:
            selected[path] = 'managed'
        if any(path.startswith(prefix) for prefix in PROJECT_PREFIXES) or path in PROJECT_FILES:
            selected[path] = 'project'
    for path in MANAGED_FILES + PROJECT_FILES:
        if path not in source.entries:
            raise StarterError('required starter input absent from trusted source: ' + path)
    inputs = set(selected) | {'.engineering-backbone/starter/' + value for value in SEEDS.values()}
    blobs = source.blobs(inputs)
    plan = {path: Entry(owner, blobs[path]) for path, owner in selected.items()}
    for path, filename in SEEDS.items():
        text = blobs['.engineering-backbone/starter/' + filename].decode('utf-8')
        plan[path] = Entry('project', text.replace('{{PROJECT_NAME}}', project_name).encode())
    project = {
        'schema_version': '1',
        'project': {'name': project_name, 'base_branch': 'main',
                    'language': 'Select project runtimes during adoption',
                    'has_frontend': False, 'has_backend': False,
                    'validation_command': 'Use the reviewed external starter verifier and project-owned native checks'},
        'agents': {'codex': True, 'copilot': True},
    }
    plan['.engineering-backbone/project.json'] = Entry('project', (json.dumps(project, indent=2) + '\n').encode())
    plan['.gitignore'] = Entry('project', b'.env\n.env.*\n!.env.example\n.venv/\nnode_modules/\nartifacts/*\n!artifacts/README.md\ndist/\nbuild/\n__pycache__/\n*.py[cod]\n')
    plan['.gitattributes'] = Entry('managed', b'# Keep managed starter bytes stable under core.autocrlf.\ndocs/** text eol=lf -filter -working-tree-encoding\n.engineering-backbone/** text eol=lf -filter -working-tree-encoding\n.codex/** text eol=lf -filter -working-tree-encoding\n.github/** text eol=lf -filter -working-tree-encoding\n.opencode/** text eol=lf -filter -working-tree-encoding\nscripts/runner_doctor.py text eol=lf -filter -working-tree-encoding\nopencode.json text eol=lf -filter -working-tree-encoding\n.gitattributes text eol=lf -filter -working-tree-encoding\n')
    paths = set(plan)
    if len({p.casefold() for p in paths}) != len(paths):
        raise StarterError('case-colliding trusted starter paths')
    return {path: Entry(entry.owner, rewrite_links(path, entry.data, paths, source)) for path, entry in sorted(plan.items())}


def manifest_for(source, plan):
    return {'version': 1, 'source_ref': source.ref,
            'files': [{'path': path, 'owner': entry.owner, 'sha256': digest(entry.data)} for path, entry in sorted(plan.items())],
            'omitted': ['source history', 'source tests/maintenance', 'legacy Copier assets', 'active source workflows', 'real environment files']}


def write_export(source, destination, project_name):
    root = safe_root(destination, must_exist=False)
    if root.resolve() == source.root.resolve() or root.resolve().is_relative_to(source.root.resolve()):
        raise StarterError('export destination must be outside the trusted source')
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise StarterError('export destination must be new or empty')
    plan = build_plan(source, project_name)
    records = dict(plan)
    records[MANIFEST] = Entry('provenance', (json.dumps(manifest_for(source, plan), indent=2) + '\n').encode())
    # All content and paths are computed before the first write. Exclusive writes
    # never replace a file that appeared after this preflight.
    root.mkdir(parents=True, exist_ok=True)
    for path, entry in records.items():
        destination_path = contained_path(root, root.joinpath(*path.split('/')))
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        contained_path(root, destination_path)
        with destination_path.open('xb') as output:
            output.write(entry.data)
    return len(plan)


def reject_other_installation(root):
    for path in FORBIDDEN_INSTALLATION:
        if (root / path).exists() or (root / path).is_symlink():
            raise StarterError('existing source/legacy installation requires its original gates')
    for path in OPTIONAL_CONTRACTS:
        if (root / path).exists() or (root / path).is_symlink():
            raise StarterError('optional contract requires a separately reviewed integration: ' + path)
    workflows = root / '.github/workflows'
    if workflows.exists() and (workflows.is_symlink() or any(workflows.glob('*.y*ml'))):
        raise StarterError('active CI requires a separately reviewed integration')


def provenance(root, source, plan):
    observed = read_json_bytes(safe_file(root, MANIFEST).read_bytes())
    if (not isinstance(observed, dict) or set(observed) != {'version', 'source_ref', 'files', 'omitted'}
            or type(observed['version']) is not int or observed['version'] != 1
            or observed['source_ref'] != source.ref
            or not isinstance(observed['files'], list) or not isinstance(observed['omitted'], list)):
        raise StarterError('invalid starter provenance; it cannot select validation authority')
    entries = {}
    for row in observed['files']:
        if (not isinstance(row, dict) or set(row) != {'path', 'owner', 'sha256'}
                or not isinstance(row['path'], str) or row['path'] in entries
                or row['owner'] not in {'managed', 'project'}
                or not isinstance(row['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', row['sha256'])):
            raise StarterError('invalid starter provenance entries')
        safe_relative(row['path'])
        entries[row['path']] = row
    if set(entries) != set(plan):
        raise StarterError('provenance path inventory differs from trusted plan')
    for path, entry in plan.items():
        if entries[path]['owner'] != entry.owner or (entry.owner == 'managed' and entries[path]['sha256'] != digest(entry.data)):
            raise StarterError('provenance cannot alter trusted ownership/content: ' + path)



def compile_trusted_module(data, filename, name):
    # Compile precisely the approved Git blob. SourceFileLoader could execute an
    # unrelated timestamp/size-valid __pycache__ entry despite matching .py bytes.
    # This path neither reads nor rewrites local bytecode caches.
    module = ModuleType(name)
    module.__file__ = str(filename)
    exec(compile(data, str(filename), 'exec'), module.__dict__)
    return module


def trusted_validator(source):
    relative = '.engineering-backbone/src/validate.py'
    path = safe_file(source.root, relative)
    if path.read_bytes() != source.blobs([relative])[relative]:
        raise StarterError('trusted validation helper differs from Git')
    return compile_trusted_module(source.blobs([relative])[relative], path,
                                  '_trusted_starter_validation')


def schema_check(module, source, name, data, label):
    raw = source.blobs(['.engineering-backbone/schemas/' + name + '.schema.json'])
    schema = read_json_bytes(next(iter(raw.values())))
    # Reuse the unchanged trusted method's schema AND deterministic cross-field
    # floors, without its constructor (which reads on-disk bundle schemas) or run().
    checker = module.RepositoryValidator.__new__(module.RepositoryValidator)
    checker.schemas = {name: module.Draft202012Validator(schema)}
    checker.errors = []
    checker.validate_data(name, data, label)
    if checker.errors:
        # Detailed trusted diagnostics can include candidate field values; expose
        # only the fixed record type/path, never those internal messages.
        raise StarterError('invalid ' + name + ' record: ' + label)



def environment_structure(source, root):
    relative = '.engineering-backbone/src/environment.py'
    path = safe_file(source.root, relative)
    if path.read_bytes() != source.blobs([relative])[relative]:
        raise StarterError('trusted environment helper differs from Git')
    module = compile_trusted_module(source.blobs([relative])[relative], path,
                                    '_trusted_starter_environment')
    try:
        module.load_contract(safe_file(root, 'config/environment.json'))
    except module.EnvironmentError as exc:
        raise StarterError('invalid environment metadata contract') from exc


def verify_project(source, root):
    root = safe_root(root)
    reject_other_installation(root)
    facts = read_json_bytes(safe_file(root, '.engineering-backbone/project.json').read_bytes())
    module = trusted_validator(source)
    schema_check(module, source, 'project', facts, '.engineering-backbone/project.json')
    plan = build_plan(source, facts['project']['name'])
    provenance(root, source, plan)
    for path, entry in plan.items():
        # Product placeholders may be dropped/replaced as the project evolves.
        if entry.owner == 'project' and path not in SEEDS and path not in {'.engineering-backbone/project.json', 'config/environment.json', '.env.example', '.gitignore'}:
            continue
        file = safe_file(root, path)
        if entry.owner == 'managed' and file.read_bytes() != entry.data:
            raise StarterError('managed baseline differs from trusted source: ' + path)
    policy = read_json_bytes(safe_file(root, '.engineering-backbone/core.json').read_bytes())
    if policy.get('invariants') != FLOOR:
        raise StarterError('mandatory core invariants changed')
    if facts['agents'] != {'codex': True, 'copilot': True}:
        raise StarterError('distributed native baseline selection cannot be disabled under the seed gate')
    for relative in ('AGENTS.md', 'CONTRIBUTING.md', '.github/copilot-instructions.md'):
        text = safe_file(root, relative).read_text(encoding='utf-8')
        for required in ('docs/agent-governance/core.md', 'docs/agent-governance/architecture.md',
                         'docs/agent-governance/planning.md', 'docs/quality/testing.md',
                         'docs/operations/configuration.md'):
            if required not in text:
                raise StarterError('project entrypoint omits canonical context: ' + relative)
    native = (module.codex_errors(root, source=True) + module.copilot_errors(root, source=True)
              + module.opencode_errors(root, source=True))
    if native:
        raise StarterError('native instruction baseline failed trusted checks')
    environment_structure(source, root)
    check_documentation(root, plan)
    for directory in ENGINEERING_ROOTS:
        for file in governance_json_files(root, directory):
            relative = file.relative_to(root).as_posix()
            safe_file(root, relative)
            data = read_json_bytes(file.read_bytes())
            if isinstance(data, dict) and 'scope' in data:
                kind = 'task-packet'
            elif isinstance(data, dict) and 'statement' in data:
                kind = 'requirement'
            elif isinstance(data, dict) and 'reviewers' in data:
                kind = 'review-evidence'
            else:
                raise StarterError('unrecognized governance JSON record: ' + relative)
            schema_check(module, source, kind, data, relative)
    return len([entry for entry in plan.values() if entry.owner == 'managed'])



def governance_json_files(root, directory):
    folder = root / directory
    # Inspect aliases before existence filtering, including dangling links.
    contained_path(root, folder)
    if not folder.exists():
        return
    if not folder.is_dir():
        raise StarterError('governance root must be a regular directory')
    pending = [folder]
    while pending:
        current = contained_path(root, pending.pop())
        with os.scandir(current) as entries:
            for entry in entries:
                path = contained_path(root, Path(entry.path))
                # Do not let recursive glob silently skip linked subdirectories.
                # Every entry is checked before JSON filename selection/descent.
                if entry.is_dir(follow_symlinks=False):
                    pending.append(path)
                elif not entry.is_file(follow_symlinks=False):
                    raise StarterError('governance entry must be a regular file/directory')
                elif path.suffix == '.json':
                    yield path


def check_documentation(root, plan):
    paths = set(plan) | {MANIFEST}
    for relative, entry in plan.items():
        if not relative.endswith('.md'):
            continue
        file = root / relative
        if entry.owner == 'project' and not file.exists():
            continue
        safe_file(root, relative)
        def target(value):
            parsed = urlsplit(value.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path or value.startswith(('#', '${', '<')):
                return value
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative), unquote(parsed.path)))
            safe_relative(resolved)
            linked = root.joinpath(*resolved.split('/'))
            contained_path(root, linked)
            if not linked.exists():
                raise StarterError('broken/escaping local Markdown reference: ' + relative)
            return value
        markdown_targets(file.read_text(encoding='utf-8'), target)


def descriptor(source, project_name):
    return {path: {'owner': entry.owner, 'data': base64.b64encode(entry.data).decode()}
            for path, entry in build_plan(source, project_name).items()}


def old_plan(source_root, source_ref, project_name):
    old = TrustedSource(source_root, source_ref)
    # Only the caller-selected, Git-attested OLD SOURCE executable is run. No
    # executable/module in the project checkout is imported or launched.
    try:
        result = subprocess.run([sys.executable, '-I', str(old.root / SCRIPT), '_describe',
                                 '--source-ref', source_ref, '--project-name', project_name],
                                cwd=old.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise StarterError('old trusted export descriptor unavailable') from exc
    if result.returncode:
        raise StarterError('old trusted export descriptor failed; reviewed migration required')
    data = read_json_bytes(result.stdout)
    if not isinstance(data, dict):
        raise StarterError('invalid old trusted descriptor')
    plan = {}
    for path, entry in data.items():
        safe_relative(path)
        if not isinstance(entry, dict) or set(entry) != {'owner', 'data'} or entry['owner'] not in {'managed', 'project'}:
            raise StarterError('invalid old trusted ownership descriptor')
        try:
            content = base64.b64decode(entry['data'], validate=True)
        except (ValueError, TypeError) as exc:
            raise StarterError('invalid old trusted content descriptor') from exc
        plan[path] = Entry(entry['owner'], content)
    return old, plan


def compare_project(source, previous_root, previous_ref, root):
    root = safe_root(root)
    previous_root = safe_root(previous_root)
    # Reject every overlap BEFORE Git-attested OLD code is launched. An exact
    # ref attests bytes, but does not make a project-contained source acceptable.
    for trusted_root in (source.root, previous_root):
        physical_source, physical_project = trusted_root.resolve(), root.resolve()
        if (physical_source == physical_project
                or physical_source.is_relative_to(physical_project)
                or physical_project.is_relative_to(physical_source)):
            raise StarterError('trusted source checkouts must be outside the project')
    reject_other_installation(root)
    facts = read_json_bytes(safe_file(root, '.engineering-backbone/project.json').read_bytes())
    module = trusted_validator(source)
    schema_check(module, source, 'project', facts, '.engineering-backbone/project.json')
    old, before = old_plan(previous_root, previous_ref, facts['project']['name'])
    after = build_plan(source, facts['project']['name'])
    provenance(root, old, before)
    result = []
    for path in sorted(set(before) | set(after)):
        previous, current = before.get(path), after.get(path)
        local_path = root / path
        local = None
        if local_path.exists() or local_path.is_symlink():
            # Never read real environment files: none may enter either plan.
            if excluded(path):
                raise StarterError('secret-like path in trusted export plan')
            local = safe_file(root, path).read_bytes()
        if previous is not None and current is not None and previous.owner != current.owner:
            status = 'ownership-change'
        elif previous is None:
            status = 'new-upstream' if local is None else ('already-current' if local == current.data else 'conflict')
        elif current is None:
            status = 'removed-upstream' if local is None or local == previous.data else 'conflict-removed'
        elif previous.data == current.data:
            status = 'unchanged' if local == previous.data else 'local-modification'
        elif local == previous.data:
            status = 'upstream-only'
        elif local == current.data:
            status = 'already-current'
        else:
            status = 'conflict'
        result.append({'path': path, 'owner': current.owner if current else previous.owner,
                       'status': status, 'action': 'preserve-project-owned' if (previous and previous.owner == 'project') else 'manual-review'})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('export', 'verify', 'compare', '_describe'):
        sub = commands.add_parser(name)
        sub.add_argument('--source-ref', required=True)
        if name in ('export', '_describe'):
            sub.add_argument('--project-name', default='new-project')
        if name == 'export':
            sub.add_argument('--destination', required=True, type=Path)
        if name in ('verify', 'compare'):
            sub.add_argument('--root', required=True, type=Path)
        if name == 'compare':
            sub.add_argument('--old-source', required=True, type=Path)
            sub.add_argument('--old-ref', required=True)
    args = parser.parse_args(argv)
    try:
        source = TrustedSource(SOURCE, args.source_ref)
        if args.command == 'export':
            count = write_export(source, args.destination, args.project_name)
            print(f'Exported {count} starter files. Project adoption and execution evidence remain pending.')
        elif args.command == 'verify':
            count = verify_project(source, args.root)
            print(f'PASS: {count} managed starter files and supported structural records. No product/runtime/human approval claim.')
        elif args.command == 'compare':
            rows = compare_project(source, args.old_source, args.old_ref, args.root)
            print(json.dumps({'old_ref': args.old_ref, 'new_ref': args.source_ref, 'files': rows, 'applied': False}, indent=2))
        else:
            print(json.dumps(descriptor(source, args.project_name)))
    except (StarterError, OSError, UnicodeError, KeyError, TypeError) as exc:
        # Known diagnostics are constructed from names/paths, never document or
        # subprocess contents. Unexpected library details remain suppressed.
        print('ERROR: ' + (str(exc) if isinstance(exc, StarterError) else 'starter operation failed safely'), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
