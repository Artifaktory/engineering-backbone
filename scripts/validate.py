#!/usr/bin/env python3
"""Validate the backbone's structural contracts; never execute project commands.

Use the validator from a trusted checkout with --root pointing at a proposed
checkout and --trusted-base pointing at the trusted checkout for policy changes.
These checks cannot authenticate review evidence or enforce human decisions.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
BUNDLE = SCRIPT_DIRECTORY.parent if SCRIPT_DIRECTORY.name == "scripts" else SCRIPT_DIRECTORY
DEFAULT_MODE = "consumer" if BUNDLE.name == ".engineering-backbone" else "source"
DEFAULT_ROOT = BUNDLE.parent if DEFAULT_MODE == "consumer" else BUNDLE
POLICY_FLOOR = {
    "human_merge_required": True,
    "human_release_required": True,
    "independent_review_required": True,
    "triage_before_fix": True,
    "delta_after_fix": True,
    "local_policy_may_only_strengthen": True,
    "automatic_downstream_apply": False,
}
IGNORED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", "dist", "build"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".toml", ".py", ".jinja"}
NATIVE_ROLES = ("planner", "implementer", "reviewer")
JINJA_OPEN = "{" * 2
JINJA_BLOCK = "{" + "%"
CONFLICT = re.compile(r"^(?:<<<<<<<(?: |$)|>>>>>>>(?: |$)|\|\|\|\|\|\|\|(?: |$))", re.M)
MD_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
MD_REFERENCE = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|[^\s]+)", re.M)
MACHINE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|/(?:workspace|home|Users|root|tmp|mnt)/)")
SOURCE_LEAK = re.compile(r"(?:\bArtifaktory/|\bBinary-Refinery/|github\.com/(?:Artifaktory|Binary-Refinery)/|\btars\.trading\b)", re.I)


def read_json(path: Path):
    def unique_keys(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key: {key}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def codex_errors(root, trusted_base=None, *, source=False):
    """Inspect managed Codex identities without trusting candidate executable code.

    This function is also compiled into the pinned consumer workflow, where an
    approved historical validator cannot supply the new native identity checks.
    It checks repository layers and declared defaults, not live parent permissions.
    """
    import json
    import os
    from pathlib import Path
    import tomllib

    root = Path(root).absolute()
    base = Path(trusted_base).absolute() if trusted_base is not None else None
    roles = {f'backbone_{role}': f'.codex/agents/backbone-{role}.toml'
             for role in ('planner', 'implementer', 'reviewer')}
    errors = []
    # Rust str::trim uses Unicode White_Space. Python str.strip additionally
    # removes U+001C..U+001F, which must not change a native role's identity.
    whitespace = '\t\n\v\f\r \u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'

    def safe(path, *, directory=False):
        try:
            relative = path.relative_to(root)
        except ValueError:
            errors.append(f'{path}: Codex identity path is outside its snapshot')
            return False
        components = [root] + [root.joinpath(*relative.parts[:index])
                               for index in range(1, len(relative.parts) + 1)]
        try:
            if any(part.is_symlink() for part in components):
                errors.append(f'{relative}: Codex identity path must have no symlink ancestors')
                return False
            if not path.resolve().is_relative_to(root.resolve()):
                errors.append(f'{relative}: Codex identity path resolves outside its snapshot')
                return False
            if not (path.is_dir() if directory else path.is_file()):
                errors.append(f'missing required file: {relative}' if not directory and not path.exists()
                              else f'{relative}: Codex identity path must be a regular ' + ('directory' if directory else 'file'))
                return False
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f'{relative}: cannot inspect Codex identity path: {exc}')
            return False
        return True

    def selected(owner):
        path = owner / '.engineering-backbone/project.json'
        # A trusted base may be a different snapshot; check its own ancestry.
        relative = path.relative_to(owner)
        components = [owner] + [owner.joinpath(*relative.parts[:index])
                                for index in range(1, len(relative.parts) + 1)]
        def unique(pairs):
            out = {}
            for key, value in pairs:
                if key in out:
                    raise ValueError('duplicate project JSON key: ' + key)
                out[key] = value
            return out
        try:
            if any(part.is_symlink() for part in components) or not path.is_file():
                raise ValueError('Codex adapter facts must be regular with no symlink ancestors')
            data = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)
            agents = data.get('agents') if isinstance(data, dict) else None
            if not isinstance(agents, dict) or set(agents) != {'codex', 'copilot'} or any(type(value) is not bool for value in agents.values()):
                raise ValueError('agents require exact boolean codex/copilot facts')
            return agents['codex']
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{relative}: {exc}')
            return None

    enabled = selected(root)
    before = selected(base) if base is not None else False
    if before is True and enabled is not True:
        errors.append('adapter regression: trusted-base enabled codex must remain enabled')
    if enabled is not True and before is not True:
        return errors
    safe(root / 'AGENTS.md')

    def read_toml(path):
        if not safe(path):
            return None
        try:
            return tomllib.loads(path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{path.relative_to(root)}: invalid Codex identity TOML: {exc}')
            return None

    def identity(path, data, fallback=None):
        if data is None:
            return None
        value = data.get('name')
        if value is not None and not isinstance(value, str):
            errors.append(f'{path.relative_to(root)}: Codex role name must be a string')
            return None
        name = value.strip(whitespace) if isinstance(value, str) else ''
        if not name:
            name = fallback
        if not name:
            errors.append(f'{path.relative_to(root)}: Codex role requires a nonempty name')
        return name

    for name, relative in roles.items():
        path = root / relative
        data = read_toml(path)
        if data is None:
            continue
        allowed = {'name', 'description', 'developer_instructions', 'sandbox_mode'}
        if set(data) - allowed:
            errors.append(f'{relative}: unapproved keys (model, credentials and permission overrides are prohibited): {sorted(set(data) - allowed)}')
        for key in ('name', 'description', 'developer_instructions'):
            if not isinstance(data.get(key), str) or not data[key].strip():
                errors.append(f'{relative}: required nonempty string {key}')
        if data.get('name') != name:
            errors.append(f'{relative}: incorrect native agent name')
        mode = 'workspace-write' if name == 'backbone_implementer' else 'read-only'
        modes = {mode, 'read-only'} if not source else {mode}
        if not isinstance(data.get('sandbox_mode'), str) or data['sandbox_mode'] not in modes:
            errors.append(f'{relative}: sandbox_mode must be {mode}' + (' or the stricter read-only' if len(modes) > 1 else ''))

    def traversal_error(exc):
        errors.append(f'cannot inspect Codex identity namespace: {exc}')

    # Every repository-contained .codex folder can form a later project layer
    # when Codex starts from that working directory. Git internals are not input.
    folders = []
    for directory, subdirs, filenames in os.walk(root, followlinks=False, onerror=traversal_error):
        subdirs[:] = [name for name in subdirs if name != '.git']
        # Source run evidence can contain isolated historical checkouts. Keep
        # the existing source-only artifact exclusion; consumers have no exemption.
        if source and Path(directory) == root and 'artifacts' in subdirs:
            subdirs.remove('artifacts')
        for name in subdirs + filenames:
            if name.casefold() == '.codex' and name != '.codex':
                errors.append(f'{Path(directory).relative_to(root) / name}: case-variant Codex native path is ambiguous; use .codex')
        if '.codex' in subdirs:
            folder = Path(directory) / '.codex'
            if safe(folder, directory=True):
                folders.append(folder)

    for folder in folders:
        try:
            for path in folder.iterdir():
                canonical = path.name.casefold()
                if canonical in {'agents', 'config.toml'} and path.name != canonical:
                    errors.append(f'{path.relative_to(root)}: case-variant Codex native path is ambiguous; use {canonical}')
        except OSError as exc:
            traversal_error(exc)
        agents_dir = folder / 'agents'
        if agents_dir.exists() or agents_dir.is_symlink():
            if safe(agents_dir, directory=True):
                for directory, subdirs, filenames in os.walk(agents_dir, followlinks=False, onerror=traversal_error):
                    current = Path(directory)
                    subdirs[:] = [name for name in subdirs if safe(current / name, directory=True)]
                    for filename in filenames:
                        if Path(filename).suffix != '.toml':
                            continue
                        path = current / filename
                        name = identity(path, read_toml(path))
                        if name in roles and path != root / roles[name]:
                            errors.append(f'{path.relative_to(root)}: reserved managed Codex role name {name}')

        config = folder / 'config.toml'
        if not config.exists() and not config.is_symlink():
            continue
        data = read_toml(config)
        if data is None:
            continue
        declarations = data.get('agents', {})
        if not isinstance(declarations, dict):
            errors.append(f'{config.relative_to(root)}: Codex agents declarations must be a table')
            continue
        for declared, settings in declarations.items():
            # Scalar [agents] fields are global orchestration settings, not roles.
            if not isinstance(settings, dict):
                if declared in roles:
                    errors.append(f'{config.relative_to(root)}: reserved managed Codex declaration {declared} requires its canonical config_file')
                continue
            reference = settings.get('config_file')
            if reference is None:
                if declared in roles:
                    errors.append(f'{config.relative_to(root)}: reserved managed Codex declaration {declared} requires its canonical config_file')
                continue
            if not isinstance(reference, str) or not reference:
                errors.append(f'{config.relative_to(root)}: Codex role {declared} config_file must be a nonempty path')
                continue
            path = folder / reference
            referenced = read_toml(path)
            if referenced is None:
                continue
            name = identity(path, referenced, fallback=declared)
            if declared in roles or name in roles:
                if declared not in roles or name != declared or path.resolve() != (root / roles[declared]).resolve():
                    errors.append(f'{config.relative_to(root)}: reserved managed Codex declaration/effective name {declared} must reference its corresponding canonical role')
    return errors


def copilot_errors(root, trusted_base=None, *, source=False):
    """Self-contained Copilot checks compiled into the pinned workflow.

    Every registry and permission limit below belongs to trusted source/workflow
    bytes. This function reads candidate data only; it imports no candidate code.
    Legacy three-role consumers remain valid until the extended package is seeded.
    Native permissions express host tool budgets, not a filesystem sandbox.
    """
    import json
    import os
    from pathlib import Path
    import re
    from urllib.parse import unquote, urlsplit
    import yaml

    original = ('planner', 'implementer', 'reviewer')
    extended = ('analyst', 'plan-reviewer', 'test-engineer', 'quality-checker',
                'security-reviewer', 'documentation', 'finding-triage')
    budgets = {role: {'read', 'search'} for role in original + extended}
    budgets['implementer'] |= {'edit', 'execute'}
    budgets['test-engineer'] |= {'edit', 'execute'}
    budgets['quality-checker'] |= {'execute'}
    budgets['documentation'] |= {'edit'}
    skills = ('task-intake', 'implementation-plan', 'bug-reproduction',
              'test-and-quality', 'code-review', 'finding-triage',
              'delta-review', 'docs-traceability')
    core_rules = ('governance', 'tests', 'docs')
    rules = core_rules + ('python', 'frontend')
    role_paths = {role: f'.github/agents/backbone-{role}.agent.md' for role in budgets}
    skill_paths = {skill: f'.github/skills/{skill}/SKILL.md' for skill in skills}
    rule_paths = {rule: f'.github/instructions/backbone-{rule}.instructions.md' for rule in rules}
    managed = list(role_paths.values()) + list(skill_paths.values()) + list(rule_paths.values())
    extra = [role_paths[role] for role in extended] + list(skill_paths.values()) + list(rule_paths.values())
    mandatory = list(role_paths.values()) + list(skill_paths.values()) + [rule_paths[rule] for rule in core_rules]
    errors = []
    root = Path(root).absolute()
    base = Path(trusted_base).absolute() if trusted_base is not None else None

    def safe(path, owner):
        try:
            relative = path.relative_to(owner)
        except ValueError:
            errors.append(f'{path}: managed file is outside its snapshot')
            return False
        components = [owner] + [owner.joinpath(*relative.parts[:index]) for index in range(1, len(relative.parts) + 1)]
        if any(part.is_symlink() for part in components) or not path.is_file():
            errors.append(f'{relative}: managed Copilot file must be regular with no symlink ancestors')
            return False
        if not path.resolve().is_relative_to(owner.resolve()):
            errors.append(f'{relative}: managed Copilot file resolves outside its snapshot')
            return False
        return True

    def selected(owner):
        path = owner / '.engineering-backbone/project.json'
        if not safe(path, owner):
            return None
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('duplicate project JSON key: ' + key)
                result[key] = value
            return result
        try:
            data = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)
            value = data.get('agents') if isinstance(data, dict) else None
            if not isinstance(value, dict) or set(value) != {'codex', 'copilot'} or any(type(item) is not bool for item in value.values()):
                raise ValueError('agents require exact boolean codex/copilot facts')
            return value['copilot']
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{path.relative_to(owner)}: {exc}')
            return None

    enabled = selected(root)
    before = selected(base) if base is not None else False
    if before is True and enabled is not True:
        errors.append('adapter regression: trusted-base enabled copilot must remain enabled')
    if enabled is not True and before is not True:
        return errors
    safe(root / '.github/copilot-instructions.md', root)
    # Supported hosts may merge profiles by the header name as well as the
    # filename. Reserve both namespaces without imposing managed tool or body
    # rules on unrelated local profiles. Never rewrite or follow local aliases.
    class UniqueLoader(yaml.SafeLoader):
        pass
    def mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError('frontmatter keys must be strings')
            if key in result:
                raise ValueError('duplicate YAML key: ' + key)
            result[key] = loader.construct_object(value_node, deep=deep)
        return result
    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    def native_name(path):
        if not safe(path, root):
            return None
        try:
            # Inspect the optional header only. Unrelated tools, models, hooks,
            # metadata and body links remain outside the managed role contract.
            with path.open(encoding='utf-8') as stream:
                first = stream.readline(131073).lstrip('\ufeff')
                if first.strip() != '---':
                    return None
                lines = []
                length = 0
                for line in stream:
                    if line.strip() == '---':
                        break
                    length += len(line)
                    if length > 131072:
                        raise ValueError('native frontmatter exceeds the namespace inspection limit')
                    lines.append(line)
                else:
                    raise ValueError('unterminated YAML frontmatter')
            data = yaml.load(''.join(lines), Loader=UniqueLoader)
            if data is None:
                return None
            if not isinstance(data, dict):
                raise ValueError('native frontmatter must be a mapping')
            name = data.get('name')
            if name is not None and not isinstance(name, str):
                raise ValueError('native name must be a string when present')
            if name is None:
                # The supported native parser preserves a present empty scalar
                # as ''. PyYAML uses None instead; reserve that ambiguity
                # conservatively, while an absent name keeps service fallback.
                return '' if 'name' in data else None
            return name.strip().casefold()
        except (OSError, UnicodeError, ValueError, TypeError, RecursionError, yaml.YAMLError) as exc:
            errors.append(f'{path.relative_to(root)}: native Copilot namespace cannot be inspected; reviewed manual reconciliation required ({exc})')
            return None

    directory = root / '.github/agents'
    if not directory.is_symlink() and not directory.parent.is_symlink() and directory.is_dir():
        identities = {'backbone-' + role: Path(relative).name for role, relative in role_paths.items()}
        try:
            profiles = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            errors.append(f'.github/agents: native Copilot namespace cannot be inspected; reviewed manual reconciliation required ({exc})')
            profiles = []
        for path in profiles:
            name = path.name.casefold()
            suffix = '.agent.md' if name.endswith('.agent.md') else '.md' if name.endswith('.md') else None
            if suffix is None:
                continue
            if path.is_symlink():
                safe(path, root)
                continue
            if not path.is_file():
                continue
            identity = name[:-len(suffix)]
            if identity in identities and path.name != identities[identity]:
                errors.append(f'{path.relative_to(root)}: alternate or ambiguous managed Copilot role identity; keep the canonical {identities[identity]} and reconcile this local profile in a reviewed manual migration')
            header_name = native_name(path)
            if header_name in identities and path.name != identities[header_name]:
                errors.append(f'{path.relative_to(root)}: reserved managed Copilot header name {header_name}; keep the canonical {identities[header_name]} and reconcile this local profile in a reviewed manual migration')
            if header_name == '' and not name.endswith('.chatmode.md'):
                # The supported CLI bridge falls back only for an explicitly
                # blank name. It truncates at the first .agent.md marker before
                # trying .chatmode.md, rather than stripping the final suffix.
                # The inspected CLI bridge skips exact legacy .chatmode.md files.
                fallback = name
                for marker in ('.agent.md', '.chatmode.md'):
                    index = name.find(marker)
                    if index > 0:
                        fallback = name[:index]
                        break
                fallback = fallback.strip().casefold()
                if fallback in identities and path.name != identities[fallback]:
                    errors.append(f'{path.relative_to(root)}: reserved managed Copilot blank-name fallback {fallback}; keep the canonical {identities[fallback]} and reconcile this local profile in a reviewed manual migration')
    if base is not None and before is True:
        installed = list(managed)
        for relative in skill_paths.values():
            directory = (base / relative).parent
            # Known managed companion resources share the same preservation
            # boundary as SKILL.md. Unrelated project skill folders stay local.
            for current, subdirs, files in os.walk(directory, followlinks=False):
                for name in subdirs:
                    if (Path(current) / name).is_symlink():
                        errors.append(f'{Path(current).relative_to(base) / name}: trusted managed Copilot directory cannot be symlinked')
                installed.extend(str((Path(current) / name).relative_to(base)) for name in files)
        for relative in sorted(set(installed)):
            previous = base / relative
            if previous.exists() or previous.is_symlink():
                safe(previous, base)
                if not (root / relative).exists() and not (root / relative).is_symlink():
                    errors.append(f'{relative}: installed Copilot asset cannot disappear; removal requires a separately reviewed governance migration')
    skill_directories = [str(Path(relative).parent) for relative in skill_paths.values()]
    package = source or any((root / relative).exists() or (root / relative).is_symlink()
                            for relative in extra + skill_directories)
    required = mandatory if package else [role_paths[role] for role in original]
    for relative in required:
        if not (root / relative).exists() and not (root / relative).is_symlink():
            errors.append(f'missing required Copilot package file: {relative}')

    conflict = re.compile(r'^(?:<<<<<<<(?: |$)|>>>>>>>(?: |$)|\|\|\|\|\|\|\|(?: |$))', re.M)
    link = re.compile(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)')
    reference = re.compile(r'^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|[^\s]+)', re.M)

    def text(path):
        if not safe(path, root):
            return None
        label = str(path.relative_to(root))
        try:
            content = path.read_text(encoding='utf-8')
            if len(content) > 131072:
                raise ValueError('managed content exceeds 128 KiB')
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{label}: {exc}')
            return None
        if conflict.search(content):
            errors.append(f'{label}: unresolved merge conflict marker')
        if path.suffix == '.md':
            prose = re.sub(r'```.*?```|~~~.*?~~~', '', content, flags=re.S)
            for match in list(link.finditer(prose)) + list(reference.finditer(prose)):
                target = match.group(1).strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or target.startswith(('#', '${')):
                    continue
                relative = unquote(parsed.path)
                if not relative:
                    continue
                linked = (path.parent / relative).resolve()
                if relative.startswith('/') or not linked.is_relative_to(root.resolve()) or not linked.exists():
                    errors.append(f'{label}: broken local Markdown link {target}')
        return content

    def frontmatter(relative):
        content = text(root / relative)
        if content is None:
            return None, ''
        try:
            match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', content, re.S)
            if not match:
                raise ValueError('missing YAML frontmatter')
            data = yaml.load(match.group(1), Loader=UniqueLoader)
            body = content[match.end():].strip()
            if not isinstance(data, dict):
                raise ValueError('frontmatter must be a mapping')
            if not body:
                raise ValueError('missing agent instructions or skill/rule body')
            return data, body
        except (ValueError, TypeError, yaml.YAMLError) as exc:
            errors.append(f'{relative}: {exc}')
            return None, ''

    def string(data, key, relative, limit):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > limit or '\x00' in value:
            errors.append(f'{relative}: required nonempty string {key} (maximum {limit} characters)')
            return False
        return True

    for role, relative in role_paths.items():
        if not (root / relative).exists() and not (root / relative).is_symlink():
            continue
        data, body = frontmatter(relative)
        if data is None:
            continue
        allowed = {'name', 'description', 'tools'}
        if role in extended:
            allowed |= {'handoffs', 'user-invocable', 'disable-model-invocation'}
        if set(data) - allowed:
            errors.append(f'{relative}: unapproved frontmatter keys: {sorted(set(data) - allowed)}')
        string(data, 'name', relative, 64)
        string(data, 'description', relative, 1024)
        if data.get('name') != 'backbone-' + role:
            errors.append(f'{relative}: incorrect native agent name')
        tools = data.get('tools')
        valid = isinstance(tools, list) and bool(tools) and all(isinstance(item, str) for item in tools)
        if valid:
            valid = len(tools) == len(set(tools)) and (set(tools) == budgets[role] if source else set(tools).issubset(budgets[role]))
        if not valid:
            errors.append(f'{relative}: tools must be ' + ('exactly ' if source else 'a nonempty unique subset of ') + str(sorted(budgets[role])) + '; planner/reviewer cannot edit, execute, or delegate')
        if role in extended and len(body) < 60:
            errors.append(f'{relative}: meaningful agent instructions require at least 60 characters')
        for key in ('user-invocable', 'disable-model-invocation'):
            if key in data and type(data[key]) is not bool:
                errors.append(f'{relative}: {key} must be boolean')
        if 'handoffs' in data:
            handoffs = data['handoffs']
            if not isinstance(handoffs, list) or not handoffs or len(handoffs) > 10:
                errors.append(f'{relative}: handoffs must be a nonempty list of at most ten entries')
            else:
                for handoff in handoffs:
                    if not isinstance(handoff, dict) or set(handoff) != {'label', 'agent', 'prompt', 'send'}:
                        errors.append(f'{relative}: handoff requires only label, agent, prompt, send')
                        continue
                    string(handoff, 'label', relative, 120)
                    string(handoff, 'prompt', relative, 2048)
                    target = handoff['agent']
                    if not isinstance(target, str) or target not in {'backbone-' + item for item in budgets}:
                        errors.append(f'{relative}: handoff target must be a known backbone role')
                    if handoff['send'] is not False:
                        errors.append(f'{relative}: handoffs require send: false; automatic handoffs are prohibited')
    for skill, relative in skill_paths.items():
        if not (root / relative).exists() and not (root / relative).is_symlink():
            continue
        data, body = frontmatter(relative)
        if data is None:
            continue
        if set(data) != {'name', 'description'}:
            errors.append(f'{relative}: skill frontmatter requires only name and description')
        string(data, 'name', relative, 64)
        string(data, 'description', relative, 1024)
        if data.get('name') != skill:
            errors.append(f'{relative}: skill name must match its folder')
        if len(body) < 100 or not re.search(r'^#{1,6} ', body, re.M):
            errors.append(f'{relative}: meaningful skill body requires headings and at least 100 characters')
        # Companion resources are owned by this managed skill only. Never follow
        # directory links or exempt other files hidden under a known skill path.
        directory = (root / relative).parent
        for current, subdirs, files in os.walk(directory, followlinks=False):
            for name in subdirs:
                if (Path(current) / name).is_symlink():
                    errors.append(f'{Path(current).relative_to(root) / name}: managed Copilot directory cannot be symlinked')
            for name in files:
                path = Path(current) / name
                if path != root / relative:
                    text(path)
    for rule, relative in rule_paths.items():
        if not (root / relative).exists() and not (root / relative).is_symlink():
            continue
        data, body = frontmatter(relative)
        if data is None:
            continue
        if 'applyTo' not in data or set(data) - {'description', 'applyTo'}:
            errors.append(f'{relative}: instruction frontmatter requires applyTo and only optional description')
        if 'description' in data:
            string(data, 'description', relative, 1024)
        if string(data, 'applyTo', relative, 2048):
            patterns = [item.strip() for item in data['applyTo'].split(',')]
            invalid = any(not item or item.startswith(('/', '\\', '!')) or '\\' in item or ':' in item
                          or any(char.isspace() or ord(char) < 32 for char in item)
                          or any(part in {'.', '..'} for part in item.split('/'))
                          or any(not part for part in item.split('/'))
                          or any(char in item for char in '[]{}()')
                          or not re.search(r'[^*?/]', item)
                          for item in patterns)
            if invalid or len(patterns) != len(set(patterns)):
                errors.append(f'{relative}: applyTo must use unique scoped repository-relative glob patterns')
        if len(body) < 60:
            errors.append(f'{relative}: meaningful instruction body requires at least 60 characters')
    return errors


class RepositoryValidator:
    def __init__(self, root: Path, trusted_base: Path | None = None, *, mode: str | None = None):
        # Default identity belongs to the executing trusted bundle, never a
        # candidate-controlled filename. The explicit API mode is for trusted
        # callers and fixtures; there is deliberately no CLI mode override.
        selected_mode = DEFAULT_MODE if mode is None else mode
        if selected_mode not in {"source", "consumer"}:
            raise ValueError("validator mode must be source or consumer")
        self.source = selected_mode == "source"
        self.agents = {}
        self.root = root.resolve()
        self.trusted_base = trusted_base.resolve() if trusted_base is not None else None
        self.errors: list[str] = []
        self.schemas = {}
        # Contract schemas come from the executing validator's checkout, not
        # the candidate checkout: changing head schemas cannot bypass base CI.
        for name in ("core-policy", "project", "task-packet", "review-evidence", "requirement"):
            try:
                schema = read_json(BUNDLE / "schemas" / f"{name}.schema.json")
                Draft202012Validator.check_schema(schema)
                self.schemas[name] = Draft202012Validator(schema)
            except (OSError, ValueError, SchemaError) as exc:
                self.error(f"validator bundle schema {name}: {exc}")

    def error(self, message: str):
        self.errors.append(message)

    def label(self, path: Path):
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def load(self, path: Path):
        try:
            if not path.resolve().is_relative_to(self.root):
                self.error(f"{self.label(path)}: file resolves outside the repository")
                return None
            return read_json(path)
        except (OSError, ValueError) as exc:
            self.error(f"{self.label(path)}: {exc}")
            return None

    def validate_data(self, name: str, data, label: str):
        if name not in self.schemas:
            return
        for err in sorted(self.schemas[name].iter_errors(data), key=lambda e: str(list(e.path))):
            field = ".".join(str(x) for x in err.path) or "<root>"
            self.error(f"{label}: {field}: {err.message}")
        if not isinstance(data, dict):
            return
        if name == "review-evidence":
            reviewers = data.get("reviewers", [])
            if isinstance(reviewers, list):
                ids = [r.get("id") for r in reviewers if isinstance(r, dict) and isinstance(r.get("id"), str)]
                if data.get("implementer") in ids:
                    self.error(f"{label}: implementer cannot be their own independent reviewer")
                if len(ids) != len(set(ids)):
                    self.error(f"{label}: reviewer identities must be unique")
            findings = data.get("findings", [])
            if isinstance(findings, list):
                ids = [f.get("id") for f in findings if isinstance(f, dict) and isinstance(f.get("id"), str)]
                if len(ids) != len(set(ids)):
                    self.error(f"{label}: finding IDs must be unique")
        if name in {"task-packet", "requirement"}:
            criteria = data.get("acceptance", data.get("acceptance_criteria", []))
            if isinstance(criteria, list):
                ids = [a.get("id") for a in criteria if isinstance(a, dict) and isinstance(a.get("id"), str)]
                if len(ids) != len(set(ids)):
                    self.error(f"{label}: acceptance criterion IDs must be unique")

    def policy_path(self, root: Path):
        return root / "policy" / "core.json" if self.source else root / ".engineering-backbone" / "core.json"

    def read_policy(self, root: Path):
        path = self.policy_path(root)
        # A link that belongs to today's candidate can point into tomorrow's
        # candidate after promotion. Canonical policy must belong to its snapshot.
        if path.is_symlink() or path.parent.is_symlink():
            raise ValueError("canonical policy must be a regular file in its own repository")
        if not path.resolve().is_relative_to(root):
            raise ValueError("policy resolves outside its own repository")
        return read_json(path)

    def policy(self):
        path = self.policy_path(self.root)
        try:
            policy = self.read_policy(self.root)
        except (OSError, ValueError) as exc:
            self.error(f"{self.label(path)}: {exc}")
            return
        self.validate_data("core-policy", policy, self.label(path))
        invariants = policy.get("invariants", {}) if isinstance(policy, dict) else {}
        for key, value in POLICY_FLOOR.items():
            if not isinstance(invariants, dict) or invariants.get(key) is not value:
                self.error(f"{self.label(path)}: mandatory policy invariant {key} must be {value}")
        if self.trusted_base is not None:
            try:
                base = self.read_policy(self.trusted_base)
            except (OSError, ValueError) as exc:
                self.error(f"BOOTSTRAP: trusted base has no readable policy; explicit bootstrap review is required ({exc})")
                return
            self.validate_data("core-policy", base, "trusted-base policy")
            previous = base.get("invariants", {}) if isinstance(base, dict) else {}
            if isinstance(previous, dict) and isinstance(invariants, dict):
                for key, value in previous.items():
                    if key not in invariants or invariants[key] is not value:
                        self.error(f"policy regression: trusted-base invariant {key} was removed or weakened")

    def required_file(self, relative: str):
        path = self.root / relative
        if not path.is_file():
            self.error(f"missing required file: {relative}")
            return False
        if not path.resolve().is_relative_to(self.root):
            self.error(f"{relative}: file resolves outside the repository")
            return False
        return True

    def adapters(self, project):
        if not isinstance(project, dict) or not isinstance(project.get("agents"), dict):
            return
        agents = dict(project["agents"])
        if self.trusted_base is not None:
            base_path = self.trusted_base / ".engineering-backbone" / "project.json"
            try:
                if not base_path.resolve().is_relative_to(self.trusted_base):
                    raise ValueError("file resolves outside the trusted repository")
                base_project = read_json(base_path)
            except (OSError, ValueError) as exc:
                self.error(f"trusted-base project configuration is unreadable; installed adapter selection cannot be established ({exc})")
            else:
                self.validate_data("project", base_project, "trusted-base project configuration")
                previous = base_project.get("agents", {}) if isinstance(base_project, dict) else {}
                if isinstance(previous, dict):
                    for adapter in ("codex", "copilot"):
                        if previous.get(adapter) is True:
                            if agents.get(adapter) is not True:
                                self.error(f"adapter regression: trusted-base enabled {adapter} must remain enabled; removal requires a separately reviewed governance migration")
                            # Candidate flags cannot suppress file, permission
                            # or managed-content checks for installed providers.
                            agents[adapter] = True
        self.agents = agents
        self.errors.extend(codex_errors(self.root, self.trusted_base, source=self.source))
        self.errors.extend(copilot_errors(self.root, self.trusted_base, source=self.source))

    def walk(self):
        paths = []
        search_root = self.root if self.source else self.root / ".engineering-backbone"
        for directory, subdirs, filenames in os.walk(search_root, followlinks=False):
            subdirs[:] = [name for name in subdirs if name not in IGNORED]
            # Root artifacts/ holds ignored run evidence, which may quote
            # conflict markers and links. Do not exempt identically named
            # directories inside governed documentation or a consumer bundle.
            if self.source and Path(directory) == self.root and "artifacts" in subdirs:
                subdirs.remove("artifacts")
            paths.extend(Path(directory) / name for name in filenames)
        if not self.source:
            # Standing entrypoints are required by adapters(), but their local
            # prose is project-owned. Application files are outside this tool
            # contract; only managed bundle artifacts and selected native
            # profiles receive link/conflict/schema checks.
            if self.agents.get("codex") is True:
                paths.extend(self.root / ".codex/agents" / f"backbone-{role}.toml" for role in NATIVE_ROLES
                             if (self.root / ".codex/agents" / f"backbone-{role}.toml").is_file())
            # copilot_errors owns its exact native registry, including ancestor
            # safety, conflict and link checks; unrelated .github files stay local.
            workflow = self.root / ".github/workflows/engineering-backbone.yml"
            if workflow.is_file():
                paths.append(workflow)
        return paths

    def dependencies(self, source):
        directory = self.root if source else self.root / ".engineering-backbone"
        parsed = {}
        for filename in ("requirements.txt", "requirements.lock"):
            path = directory / filename
            if not self.required_file(str(path.relative_to(self.root))):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.error(f"{self.label(path)}: cannot read dependency manifest: {exc}")
                continue
            # The supported format is intentionally small: exact package pins,
            # comments and backslash continuations. No indexes, VCS, includes,
            # options, editable installs or environment-dependent unpinned input.
            logical = []
            current = ""
            for line in content.splitlines():
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                continues = line.endswith(chr(92))
                current += " " + (line[:-1].strip() if continues else line)
                if not continues:
                    logical.append(current.strip())
                    current = ""
            if current:
                self.error(f"{self.label(path)}: unterminated dependency continuation")
            packages = {}
            for entry in logical:
                pieces = entry.split()
                match = re.fullmatch(r"([A-Za-z0-9][A-Za-z0-9_.-]*)==([A-Za-z0-9][A-Za-z0-9.!+-]*)", pieces[0])
                hashes = pieces[1:]
                locked = filename.endswith(".lock")
                if match is None or (locked and not hashes) or any(not re.fullmatch(r"--hash=sha256:[0-9a-f]{64}", value) for value in hashes) or (not locked and hashes):
                    self.error(f"{self.label(path)}: dependency entries must use exact == pins{' with SHA256 hashes' if locked else ''}; indexes, URLs and install options are forbidden")
                    continue
                name = re.sub(r"[-_.]+", "-", match.group(1)).lower()
                if name in packages:
                    self.error(f"{self.label(path)}: duplicate dependency {name}")
                packages[name] = match.group(2)
            if not packages:
                self.error(f"{self.label(path)}: dependency manifest is empty")
            parsed[filename] = packages
        if "requirements.txt" in parsed and "requirements.lock" in parsed:
            for name, version in parsed["requirements.txt"].items():
                if parsed["requirements.lock"].get(name) != version:
                    self.error(f"dependency lock mismatch: {name}=={version} must match requirements.lock; regenerate the lock")

    def workflows(self, source):
        directory = self.root / ".github" / "workflows"
        if not directory.is_dir():
            return
        for path in sorted(directory.iterdir()):
            if path.suffix not in {".yml", ".yaml"} or (not source and path.name != "engineering-backbone.yml"):
                continue
            relative = self.label(path)
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError) as exc:
                self.error(f"{relative}: invalid workflow YAML: {exc}")
                continue
            if not isinstance(data, dict):
                self.error(f"{relative}: workflow must be a mapping")
                continue
            events = data.get("on", data.get(True))  # PyYAML YAML 1.1 treats on as a boolean.
            event_names = events.keys() if isinstance(events, dict) else events if isinstance(events, list) else [events]
            if "pull_request_target" in event_names:
                self.error(f"{relative}: pull_request_target is forbidden for backbone validation")
            permissions = data.get("permissions")
            if not isinstance(permissions, dict) or permissions.get("contents") != "read" or any(value != "read" for value in permissions.values()):
                self.error(f"{relative}: explicit read-only contents permissions are required")
            jobs = data.get("jobs", {})
            if not isinstance(jobs, dict) or not jobs:
                self.error(f"{relative}: workflow needs jobs")
                continue
            for job_id, job in jobs.items():
                if not isinstance(job, dict):
                    self.error(f"{relative}: job {job_id} must be a mapping")
                    continue
                extra = job.get("permissions", {})
                if not isinstance(extra, dict) or any(value != "read" for value in extra.values()):
                    self.error(f"{relative}: job {job_id} may not request write permissions")
                if job.get("secrets") == "inherit":
                    self.error(f"{relative}: secrets: inherit is forbidden")
                calls = [job] + (job.get("steps", []) if isinstance(job.get("steps", []), list) else [])
                for call in calls:
                    if not isinstance(call, dict) or "uses" not in call:
                        continue
                    uses = call["uses"]
                    if not isinstance(uses, str):
                        self.error(f"{relative}: uses must be a string")
                        continue
                    if not uses.startswith("./") and not re.fullmatch(r"[^\s@]+@[0-9a-f]{40}", uses):
                        self.error(f"{relative}: external actions/workflows must use a full commit SHA: {uses}")
                    if uses.startswith("actions/checkout@"):
                        with_values = call.get("with", {})
                        if not isinstance(with_values, dict) or with_values.get("persist-credentials") is not False:
                            self.error(f"{relative}: checkout requires persist-credentials: false")

    def markdown(self, path: Path, content: str):
        # Templates are checked again after rendering; source Jinja paths and
        # placeholders are not actual consumer paths.
        if "template" in path.relative_to(self.root).parts:
            return
        content = re.sub(r"```.*?```|~~~.*?~~~", "", content, flags=re.S)
        for match in list(MD_LINK.finditer(content)) + list(MD_REFERENCE.finditer(content)):
            target = match.group(1).strip("<>")
            if target.startswith(("#", JINJA_OPEN, "${", "<")):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            relative = unquote(parsed.path)
            if not relative:
                continue
            if relative.startswith("/"):
                self.error(f"{self.label(path)}: absolute Markdown link {target}")
                continue
            linked = (path.parent / relative).resolve()
            if not linked.is_relative_to(self.root) or not linked.exists():
                self.error(f"{self.label(path)}: broken local Markdown link {target}")

    def artifacts(self, paths):
        for path in paths:
            parts = path.relative_to(self.root).parts
            if path.name.endswith(".schema.json"):
                data = self.load(path)
                if data is not None:
                    try:
                        Draft202012Validator.check_schema(data)
                    except SchemaError as exc:
                        self.error(f"{self.label(path)}: invalid JSON schema: {exc}")
                continue
            if path.suffix != ".json" or not any(p in {"examples", "plans", "requirements", "reviews", "tasks"} for p in parts):
                continue
            data = self.load(path)
            if data is None:
                continue
            if isinstance(data, dict) and "scope" in data:
                kind = "task-packet"
            elif isinstance(data, dict) and "statement" in data:
                kind = "requirement"
            elif isinstance(data, dict) and "reviewers" in data:
                kind = "review-evidence"
            else:
                self.error(f"{self.label(path)}: unrecognized governance JSON artifact")
                continue
            self.validate_data(kind, data, self.label(path))

    def run(self):
        if not self.root.is_dir():
            self.error(f"repository root does not exist: {self.root}")
            return self.errors
        self.policy()
        project_path = self.root / ".engineering-backbone" / "project.json"
        project = self.load(project_path)
        if project is not None:
            self.validate_data("project", project, self.label(project_path))
            self.adapters(project)
        source = self.source
        self.required_file("policy/core.md" if source else ".engineering-backbone/core.md")
        self.workflows(source)
        self.dependencies(source)
        paths = self.walk()
        self.artifacts(paths)
        portable = {self.policy_path(self.root), project_path}
        if not source:
            portable.add(self.root / ".engineering-backbone" / "core.md")
        for path in paths:
            if path.suffix not in TEXT_SUFFIXES:
                continue
            if not path.resolve().is_relative_to(self.root):
                self.error(f"{self.label(path)}: file resolves outside the repository")
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.error(f"{self.label(path)}: cannot read text: {exc}")
                continue
            if CONFLICT.search(content):
                self.error(f"{self.label(path)}: unresolved merge conflict marker")
            if path.suffix == ".md":
                self.markdown(path, content)
            if path in portable and (MACHINE_PATH.search(content) or SOURCE_LEAK.search(content)):
                self.error(f"{self.label(path)}: project configuration/core contains an absolute machine path or source-project domain")
        return self.errors


def validate_root(root: Path | str, trusted_base: Path | str | None = None, *, mode: str | None = None):
    return RepositoryValidator(Path(root), Path(trusted_base) if trusted_base is not None else None, mode=mode).run()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--trusted-base", type=Path)
    args = parser.parse_args(argv)
    errors = validate_root(args.root, args.trusted_base)
    if args.trusted_base is None:
        print("TRUST: no trusted base supplied; policy-history comparison was not performed. Initial bootstrap requires explicit independent review.")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} structural validation error(s).", file=sys.stderr)
        return 1
    print("PASS: structural contracts validated. This does not authenticate evidence or establish human approval, agent behavior, or release authorization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
