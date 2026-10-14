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


# BEGIN COMPILED WORKFLOW KIT GUARD
def workflow_kit_main(argv=None):
    """Validate, prepare approved commands, execute checks, and enforce gates."""
    import argparse
    import json
    import os
    from pathlib import Path
    import re
    import signal
    import stat
    import subprocess
    import tempfile

    config_relative = '.engineering-backbone/workflows.json'
    profiles = {'docs', 'python', 'typescript', 'go', 'dotnet'}
    capabilities = {'dependencies', 'web', 'api', 'database', 'container',
                    'iac', 'release', 'deploy'}
    runtime_for = {'python': 'python', 'typescript': 'node', 'go': 'go',
                   'dotnet': 'dotnet'}
    quality = {'docs', 'build', 'lint', 'test', 'typecheck', 'browser', 'api',
               'migration'}
    security = {'sast', 'dependency', 'container', 'iac'}
    release = {'release-integrity', 'provenance', 'signature', 'sbom'}
    deploy = {'deployment-smoke', 'rollback', 'monitoring'}
    phases = {'pr', 'maintenance', 'release', 'deploy'}
    kinds = quality | security | release | deploy
    identifier = re.compile(r'[A-Za-z][A-Za-z0-9_.-]{0,63}\Z')
    config_limit = 262144
    missing_config = object()

    def fail(message):
        raise ValueError(message)

    def safe_text(value, label, *, nonempty=True, limit=4096):
        if (not isinstance(value, str) or len(value) > limit
                or (nonempty and not value.strip())
                or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value)):
            fail('Invalid ' + label)
        try:
            value.encode('utf-8')
        except UnicodeError:
            fail('Invalid UTF-8 ' + label)
        return value

    def safe_path(path, *, directory=False, missing=False):
        path = Path(path)
        if '..' in path.parts:
            fail('Parent traversal in filesystem path')
        path = Path(os.path.abspath(path))
        current = Path(path.anchor)
        for part in path.parts[1:]:
            current = current / part
            try:
                mode = current.lstat().st_mode
            except FileNotFoundError:
                if missing:
                    return path
                fail('Required filesystem path is absent')
            if stat.S_ISLNK(mode):
                fail('Symlink in filesystem path')
            if current != path and not stat.S_ISDIR(mode):
                fail('Non-directory filesystem ancestor')
        mode = path.stat().st_mode
        if directory and not stat.S_ISDIR(mode):
            fail('Working directory is not a directory')
        if not directory and not stat.S_ISREG(mode):
            fail('Input is not a regular file')
        return path

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('Duplicate JSON object key')
            result[key] = value
        return result

    def read_json(path, *, absent=False):
        path = safe_path(path, missing=absent)
        if absent and not path.exists():
            return missing_config
        if path.stat().st_size > config_limit:
            fail('Configuration exceeds size limit')
        with path.open('rb') as handle:
            data = handle.read(config_limit + 1)
        if len(data) > config_limit:
            fail('Configuration exceeds size limit')
        try:
            return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                              parse_constant=lambda value: fail('Invalid JSON number'))
        except (UnicodeError, json.JSONDecodeError):
            fail('Invalid UTF-8 JSON configuration')

    def unique_strings(value, allowed, label, limit=100):
        if (not isinstance(value, list) or len(value) > limit
                or any(not isinstance(item, str) or item not in allowed for item in value)
                or len(value) != len(set(value))):
            fail('Invalid or duplicate ' + label)
        return set(value)

    def required(config):
        needed = set()
        for profile in config['profiles']:
            if profile == 'docs':
                needed.add(('docs', 'pr'))
            else:
                needed.update((kind, 'pr') for kind in ('build', 'lint', 'test', 'sast'))
                if profile == 'typescript':
                    needed.add(('typecheck', 'pr'))
        selected = set(config['capabilities'])
        for capability, kind in (('web', 'browser'), ('api', 'api'),
                                 ('database', 'migration'), ('iac', 'iac')):
            if capability in selected:
                needed.add((kind, 'pr'))
        for capability, kind in (('dependencies', 'dependency'), ('container', 'container')):
            if capability in selected:
                needed.update((kind, phase) for phase in ('pr', 'maintenance'))
        if 'release' in selected:
            needed.update((kind, 'release') for kind in ('release-integrity', 'provenance', 'signature'))
            if selected & {'dependencies', 'container'}:
                needed.add(('sbom', 'release'))
        if 'deploy' in selected:
            needed.update((kind, 'deploy') for kind in deploy)
        return needed

    def validate(config, *, complete=False):
        expected = {'schema_version', 'enabled', 'profiles', 'capabilities',
                    'runtimes', 'checks'}
        if not isinstance(config, dict) or set(config) != expected:
            fail('Configuration has missing or unknown keys')
        if config['schema_version'] != '1' or type(config['enabled']) is not bool:
            fail('Invalid configuration version or enabled flag')
        selected_profiles = unique_strings(config['profiles'], profiles, 'profiles', 5)
        unique_strings(config['capabilities'], capabilities, 'capabilities', 8)
        versions = config['runtimes']
        if not isinstance(versions, dict) or set(versions) - set(runtime_for.values()):
            fail('Invalid runtime mapping')
        for name, version in versions.items():
            safe_text(version, 'runtime version', limit=32)
            pattern = r'[0-9]{1,3}(?:\.[0-9]{1,3}){0,2}'
            if name == 'dotnet':
                pattern += r'(?:\.x)?'
            if re.fullmatch(pattern, version) is None:
                fail('Runtime version must be numeric or a terminal .x for dotnet')
        checks = config['checks']
        if not isinstance(checks, list) or len(checks) > 100:
            fail('Invalid checks array')
        ids = set()
        coverage = set()
        for check in checks:
            keys = {'id', 'kind', 'argv', 'cwd', 'timeout_seconds', 'phases'}
            if not isinstance(check, dict) or set(check) != keys:
                fail('Check has missing or unknown keys')
            if not isinstance(check['id'], str) or identifier.fullmatch(check['id']) is None:
                fail('Invalid check ID')
            if check['id'] in ids:
                fail('Duplicate check ID')
            ids.add(check['id'])
            if not isinstance(check['kind'], str) or check['kind'] not in kinds:
                fail('Unknown check kind')
            arguments = check['argv']
            if not isinstance(arguments, list) or not 1 <= len(arguments) <= 64:
                fail('Check argv must contain an executable')
            for argument in arguments:
                safe_text(argument, 'command argument', nonempty=False)
            if not arguments[0].strip():
                fail('Check argv must contain an executable')
            cwd = safe_text(check['cwd'], 'working directory', limit=512)
            if (cwd != '.' and (cwd.startswith('/') or '\\' in cwd
                    or ':' in cwd or any(part in ('', '.', '..') for part in cwd.split('/')))):
                fail('Working directory must be a safe relative path')
            timeout = check['timeout_seconds']
            if type(timeout) is not int or not 1 <= timeout <= 1800:
                fail('Timeout must be between 1 and 1800 seconds')
            selected_phases = unique_strings(check['phases'], phases, 'check phases', 4)
            if not selected_phases:
                fail('Check must select a phase')
            allowed_phases = ({'release'} if check['kind'] in release else
                              {'deploy'} if check['kind'] in deploy else
                              {'pr', 'maintenance'} if check['kind'] in {'dependency', 'container'} else {'pr'})
            if selected_phases - allowed_phases:
                fail('Check kind does not support selected phases')
            coverage.update((check['kind'], phase) for phase in selected_phases)
        if config['enabled'] or complete:
            if not selected_profiles:
                fail('Active configuration must select a profile')
            if any(runtime_for[profile] not in versions
                   for profile in selected_profiles if profile in runtime_for):
                fail('Required profile runtime is missing')
            if required(config) - coverage:
                fail('Required profile or capability checks are missing')
        return config

    def configuration(root):
        root = safe_path(root, directory=True)
        value = read_json(root / config_relative, absent=True)
        return None if value is missing_config else validate(value)

    def compare(candidate, base):
        if base is not None:
            if candidate is None:
                fail('Existing workflow configuration cannot be removed')
            if base['enabled'] and not candidate['enabled']:
                fail('Enabled workflow configuration cannot be disabled')
            for key in ('profiles', 'capabilities'):
                if set(base[key]) - set(candidate[key]):
                    fail('Approved profiles or capabilities cannot be removed')
            base_ids = {check['id'] for check in base['checks']}
            if base_ids - {check['id'] for check in candidate['checks']}:
                fail('Approved check IDs cannot be removed')
        if candidate is not None and candidate['enabled'] and (base is None or not base['enabled']):
            if base is None:
                fail('Activation requires an already reviewed inactive seed')
            validate(base, complete=True)
            activated = dict(base, enabled=True)
            if candidate != activated:
                fail('Activation must match the reviewed seed except enabled')

    def prepared(root, trusted):
        candidate, base = configuration(root), configuration(trusted)
        compare(candidate, base)
        if candidate is None or not candidate['enabled']:
            fail('Workflow execution requires an enabled configuration')
        result = dict(candidate)
        result['runtimes'] = dict(candidate['runtimes'], **base['runtimes'])
        approved = {check['id']: check for check in base['checks']}
        result['checks'] = [approved.get(check['id'], check) for check in candidate['checks']]
        # Candidate phase/kind edits cannot turn the approved command off.
        validate(result, complete=True)
        return result

    def write_json(path, value):
        path = safe_path(path, missing=True)
        safe_path(path.parent, directory=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                             dir=path.parent, delete=False) as handle:
                temporary = Path(handle.name)
                json.dump(value, handle, indent=2, sort_keys=True)
                handle.write('\n')
            os.replace(temporary, path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    def run_checks(args):
        root = safe_path(args.root, directory=True)
        config = validate(read_json(args.config), complete=True)
        if not config['enabled']:
            fail('Workflow execution requires an enabled configuration')
        permitted = {'quality': 'pr', 'security': 'pr', 'maintenance': 'maintenance',
                     'release': 'release', 'deploy': 'deploy'}
        if args.phase != permitted[args.category]:
            fail('Category does not support selected phase')
        if args.phase in {'release', 'deploy'} and args.phase not in config['capabilities']:
            fail('Delivery phase requires its capability')
        selected_kinds = {'quality': quality, 'security': security,
                          'maintenance': {'dependency', 'container'},
                          'release': release, 'deploy': deploy}[args.category]
        selected = [check for check in config['checks']
                    if args.phase in check['phases'] and check['kind'] in selected_kinds]
        if not selected:
            print('NOT APPLICABLE: no ' + args.category + ' checks required by approved configuration')
            return 0
        allowed_env = {'PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR', 'TEMP', 'TMP',
                       'SystemRoot', 'COMSPEC', 'PATHEXT', 'DOTNET_ROOT',
                       'DOTNET_ROOT_X64', 'DOTNET_CLI_TELEMETRY_OPTOUT',
                       'DOTNET_NOLOGO', 'PYTHONUTF8', 'PYTHONIOENCODING'}
        environment = {key: value for key, value in os.environ.items() if key in allowed_env}
        for check in selected:
            cwd = safe_path(root / check['cwd'], directory=True)
            print('RUN: ' + check['id'], flush=True)
            try:
                process = subprocess.Popen(check['argv'], cwd=cwd, env=environment,
                                           shell=False, stdin=subprocess.DEVNULL,
                                           start_new_session=(os.name == 'posix'))
                try:
                    returncode = process.wait(timeout=check['timeout_seconds'])
                except subprocess.TimeoutExpired:
                    if os.name == 'posix':
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    process.wait()
                    raise
            except subprocess.TimeoutExpired:
                fail('Check timed out: ' + check['id'])
            except OSError:
                fail('Check executable unavailable: ' + check['id'])
            if returncode != 0:
                fail('Check failed: ' + check['id'] + ' (exit ' + str(returncode) + ')')
            print('PASS: ' + check['id'], flush=True)
        return 0

    def scan(root):
        root = safe_path(root, directory=True)
        git_environment = {key: value for key, value in os.environ.items()
                           if key in {'PATH', 'HOME', 'SystemRoot', 'TEMP', 'TMP', 'TMPDIR'}}
        git_environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
        git_command = ['git', '-c', 'core.fsmonitor=false', '-c', 'submodule.recurse=false',
                       '-C', str(root)]
        try:
            membership = subprocess.run(git_command + ['rev-parse', '--show-toplevel'],
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        stdin=subprocess.DEVNULL, shell=False, timeout=30,
                                        env=git_environment, check=False)
        except (OSError, subprocess.TimeoutExpired):
            fail('Tracked-file discovery failed')
        if (membership.returncode != 0 or len(membership.stdout) > 4096
                or os.fsdecode(membership.stdout).rstrip('\r\n') != str(root)):
            fail('Secret scan requires the repository root')
        with tempfile.TemporaryFile() as listing:
            try:
                result = subprocess.run(git_command + ['ls-files', '-z', '--cached'],
                                        stdout=listing, stderr=subprocess.DEVNULL,
                                        stdin=subprocess.DEVNULL, shell=False, timeout=30,
                                        env=git_environment, check=False)
            except (OSError, subprocess.TimeoutExpired):
                fail('Tracked-file discovery failed')
            if result.returncode != 0:
                fail('Tracked-file discovery failed')
            if listing.tell() > 8388608:
                fail('Tracked-file listing exceeds size limit')
            listing.seek(0)
            raw = listing.read()
        names = raw.split(b'\0')
        if names[-1] != b'':
            fail('Invalid tracked-file listing')
        names = names[:-1]
        if len(names) > 20000:
            fail('Tracked-file count exceeds limit')
        patterns = (
            ('private-key', re.compile(rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----')),
            ('github-token', re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{36,255}\b')),
            ('github-fine-grained-token', re.compile(rb'\bgithub_pat_[A-Za-z0-9_]{40,255}\b')),
            ('aws-access-key', re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
        )
        total = 0
        findings = []
        for raw_name in names:
            try:
                name = raw_name.decode('utf-8')
            except UnicodeError:
                fail('Tracked filename is not UTF-8')
            safe_text(name, 'tracked filename', limit=4096)
            if (name.startswith('/') or '\\' in name
                    or any(part in ('', '.', '..') for part in name.split('/'))):
                fail('Unsafe tracked filename')
            path = safe_path(root / name)
            if path.stat().st_size > 2097152:
                fail('Tracked file exceeds scan size limit: ' + name)
            with path.open('rb') as handle:
                data = handle.read(2097153)
            if len(data) > 2097152:
                fail('Tracked file exceeds scan size limit: ' + name)
            total += len(data)
            if total > 67108864:
                fail('Tracked files exceed total scan size limit')
            for kind, pattern in patterns:
                if pattern.search(data):
                    findings.append((name, kind))
        for name, kind in findings:
            print('SECRET FINDING: ' + name + ' (' + kind + ')')
        if findings:
            fail('Secret scan found ' + str(len(findings)) + ' finding(s)')
        print('PASS: bounded tracked-file secret scan (' + str(len(names)) + ' files)')
        return 0

    parser = argparse.ArgumentParser(description='Trusted shared workflow kit')
    commands = parser.add_subparsers(dest='command', required=True)
    validate_parser = commands.add_parser('validate')
    validate_parser.add_argument('--root', required=True)
    validate_parser.add_argument('--trusted-base')
    prepare_parser = commands.add_parser('prepare')
    prepare_parser.add_argument('--root', required=True)
    prepare_parser.add_argument('--trusted-base', required=True)
    prepare_parser.add_argument('--phase', choices=sorted(phases), required=True)
    prepare_parser.add_argument('--output', required=True)
    run_parser = commands.add_parser('run')
    run_parser.add_argument('--root', required=True)
    run_parser.add_argument('--config', required=True)
    run_parser.add_argument('--phase', choices=sorted(phases), required=True)
    run_parser.add_argument('--category', choices=('quality', 'security', 'maintenance', 'release', 'deploy'), required=True)
    gate_parser = commands.add_parser('gate')
    gate_parser.add_argument('--needs-json', required=True)
    scan_parser = commands.add_parser('secret-scan')
    scan_parser.add_argument('--root', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            candidate = configuration(args.root)
            if args.trusted_base is not None:
                compare(candidate, configuration(args.trusted_base))
            print('PASS: workflow kit configuration' if candidate is not None else
                  'PASS: legacy consumer has no workflow kit configuration')
            return 0
        if args.command == 'prepare':
            value = prepared(args.root, args.trusted_base)
            if args.phase in {'release', 'deploy'} and args.phase not in value['capabilities']:
                fail('Delivery phase requires its capability')
            write_json(args.output, value)
            print('PASS: prepared approved execution configuration')
            return 0
        if args.command == 'run':
            return run_checks(args)
        if args.command == 'secret-scan':
            return scan(args.root)
        try:
            needs = json.loads(args.needs_json, object_pairs_hook=pairs,
                               parse_constant=lambda value: fail('Invalid JSON number'))
        except json.JSONDecodeError:
            fail('Invalid needs JSON')
        expected_jobs = {'configuration', 'governance', 'quality', 'security', 'secrets'}
        if not isinstance(needs, dict) or set(needs) != expected_jobs:
            fail('Gate requires the fixed complete job set')
        if any(not isinstance(job, dict) or job.get('result') != 'success'
               for job in needs.values()):
            fail('Every required job must have result success')
        print('PASS: all five mandatory jobs succeeded')
        return 0
    except (ValueError, OSError) as error:
        # Contract failures never include argument values, command output, or
        # secret matches. OSError paths may be uncontrolled, so redact them.
        print('FAIL: ' + (str(error) if isinstance(error, ValueError) else
                          'Filesystem operation failed'))
        return 1
# END COMPILED WORKFLOW KIT GUARD


# BEGIN COMPILED QUALITY GUARD
def quality_errors(root, trusted_base=None, *, source=False, navigation_request=None,
                   navigation_expected=None, navigation_output=None):
    """Return bounded contract errors, not semantic approval or certification."""
    import csv
    from datetime import date
    import io
    import json
    import os
    from pathlib import Path
    import re
    import stat

    catalog_json = '{"version":"1.0.0","sources":[{"id":"SRC-ISO-25010","title":"ISO/IEC 25010 product quality model","edition":"2023, edition 2","url":"https://www.iso.org/standard/78176.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public description of product quality evaluation; no full normative clauses reviewed."]},{"id":"SRC-ISO-12207","title":"ISO/IEC/IEEE 12207 software life cycle processes","edition":"2026, edition 2","url":"https://www.iso.org/standard/90219.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public lifecycle scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29148","title":"ISO/IEC/IEEE 29148 requirements engineering","edition":"2018, edition 2","url":"https://www.iso.org/standard/72089.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official published edition and public requirements scope; a revision draft is separate; no full normative clauses reviewed."]},{"id":"SRC-ISO-42010","title":"ISO/IEC/IEEE 42010 architecture description","edition":"2022, edition 2","url":"https://www.iso.org/standard/74393.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public architecture-description scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29119-2","title":"ISO/IEC/IEEE 29119-2 test processes","edition":"2021, edition 2","url":"https://www.iso.org/standard/79428.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public test-process scope; no full normative clauses reviewed."]},{"id":"SRC-ISO-29119-3","title":"ISO/IEC/IEEE 29119-3 test documentation","edition":"2021, edition 2","url":"https://www.iso.org/standard/79429.html","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public test-documentation scope; no normative templates or full clauses adopted."]},{"id":"SRC-MICROSOFT-SDL","title":"Microsoft SDL public practices","edition":"Living guidance observed 2026-10-13","url":"https://www.microsoft.com/en-us/securityengineering/sdl/practices","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public descriptions of security governance, threat analysis and security verification activities."]},{"id":"SRC-GOOGLE-CPP","title":"Google C++ Style Guide","edition":"Living guidance observed 2026-10-13; targets C++20","url":"https://google.github.io/styleguide/cppguide.html","status":"living-guidance","access":"public-guidance","adoption":"reference-only","verified_sections":["Public language-target description and readability/consistency guidance; C++17 compatibility subset not adopted."]},{"id":"SRC-CODEX-INSTRUCTIONS","title":"Codex project instruction discovery","edition":"Living guidance observed 2026-10-13","url":"https://learn.chatgpt.com/docs/agent-configuration/agents-md","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public discovery and override behavior; intended-client loading still requires project verification."]},{"id":"SRC-COPILOT-INSTRUCTIONS","title":"GitHub Copilot instruction support","edition":"Living guidance observed 2026-10-13","url":"https://docs.github.com/en/copilot/reference/custom-instructions-support","status":"living-guidance","access":"public-guidance","adoption":"public-guidance","verified_sections":["Public support matrix for instruction types and clients; intended-client loading still requires project verification."]},{"id":"SRC-IEC-61508","title":"IEC 61508-3 safety-related software","edition":"2010, edition 2","url":"https://webstore.iec.ch/en/publication/5517","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official edition and public safety-related software scope; full text, applicability and certification scheme unreviewed."]},{"id":"SRC-IEC-62304","title":"IEC 62304 medical device software lifecycle","edition":"2006 plus amendment 1:2015, consolidated edition 1.1","url":"https://webstore.iec.ch/en/publication/22794","status":"published","access":"public-scope-only","adoption":"reference-only","verified_sections":["Official consolidated edition and public medical-device software scope; full text, applicability and certification scheme unreviewed."]}],"rules":[{"id":"QUAL-REQ-001","version":"1","statement":"Before non-trivial work, record identified requirements, measurable quality goals, material risks and verifiable acceptance criteria. Map each selected quality rule to project requirements or risks and its planned evidence.","source_ids":["SRC-ISO-25010","SRC-ISO-29148"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-DES-001","version":"1","statement":"Before a material design or implementation change, document affected interfaces, architectural decisions, quality consequences and security assumptions. Obtain independent plan/design review proportional to risk; preserve existing architecture locations.","source_ids":["SRC-ISO-42010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","reviewer"],"phases":["planning","design"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-CODE-001","version":"1","statement":"Apply the project-selected language, coding and security rules to changed code. Review suitability, correctness and maintainability; run the applicable compiler, lint and analysis checks without weakening inherited controls.","source_ids":["SRC-ISO-25010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["implementer","quality_checker","reviewer"],"phases":["implementation","verification"],"verification":"hybrid","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-TEST-001","version":"1","statement":"Define risk-based tests for affected requirements and critical behavior, including relevant success, rejection, boundary and failure cases. Add meaningful regression coverage for reproducible fixes. Record automated and manual coverage and unresolved gaps.","source_ids":["SRC-ISO-29119-2","SRC-ISO-29119-3"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["test","docs"]],"waivable":false},{"id":"QUAL-DOC-001","version":"1","statement":"Update affected requirement, design, user and operational documentation when behavior, contracts or operation change. Trace the impact or a justified no-impact decision without duplicating established authoritative documents.","source_ids":["SRC-ISO-29148","SRC-ISO-42010"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["implementer","reviewer"],"phases":["implementation","review"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-EVID-001","version":"1","statement":"Bind actual check and review results to the inspected revision and record commands, exit codes, acceptance coverage and limitations. Keep unexecuted, failed and blocked evidence visible; declarations, generated reports and structural validation are not runtime proof.","source_ids":["SRC-ISO-12207","SRC-ISO-29119-3"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["quality_checker","reviewer"],"phases":["verification","review","publication"],"verification":"manual","artifacts":["traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-REVIEW-001","version":"1","statement":"Obtain independent review of one frozen base/head/patch snapshot after required checks. Triage before repairs; repair confirmed findings and review their Delta and direct regressions. Preserve human approvals, existing gates and stop conditions.","source_ids":["SRC-ISO-12207"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["reviewer","triage","implementer","quality_checker"],"phases":["review","publication"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-HANDOFF-001","version":"1","statement":"Each delegation must include the scoped task, exact project-profile and rule versions, requirement and acceptance IDs, relevant design context, authorized actions, required evidence and return/stop conditions. Verify instruction discovery in the intended client; do not assume delegation propagates context.","source_ids":["SRC-CODEX-INSTRUCTIONS","SRC-COPILOT-INSTRUCTIONS"],"source_alignment":"Organization-owned handoff contract using public client-discovery guidance; supported instruction formats do not prove runtime loading or compliance.","responsibilities":["planner","implementer","reviewer","quality_checker","triage"],"phases":["planning","implementation","verification","review"],"verification":"manual","artifacts":["quality_plan","traceability"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-SW-001","version":"1","statement":"For executable software, bind PR checks for build, lint, tests and static security analysis to the workflow contract. Select concrete project tools and scope; evaluate relevant integration and critical acceptance behavior in the test strategy.","source_ids":["SRC-ISO-25010","SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["build"],["lint"],["test"],["sast"]],"waivable":true},{"id":"QUAL-SEC-001","version":"1","statement":"Document material trust boundaries, threats and security assumptions. Verify relevant authorization, input handling, data protection and failure behavior with targeted security tests and analysis, and track unresolved security risk before release.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned selection informed by Microsoft public security practices; adoption does not claim compliance with Microsoft internal SDL requirements.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["design","implementation","verification","release"],"verification":"hybrid","artifacts":["quality_plan","traceability"],"check_kind_groups":[["sast"]],"waivable":true},{"id":"QUAL-PY-001","version":"1","statement":"For Python components, select supported runtime/tool versions and project coding rules. Bind PR lint and test commands; assess typing, dependency and packaging checks according to component risk and distribution model.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned Python refinement; specific style, type and packaging tools are selected by the project, not asserted as a normative SDL requirement.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["lint"],["test"]],"waivable":true},{"id":"QUAL-TS-001","version":"1","statement":"For TypeScript components, select supported runtime/tool versions and project coding rules. Bind PR lint, typecheck and test commands; test runtime boundaries where static types cannot establish external-data validity.","source_ids":["SRC-MICROSOFT-SDL"],"source_alignment":"Organization-owned TypeScript refinement; concrete compiler, style and runtime checks are selected by the project.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["lint"],["typecheck"],["test"]],"waivable":true},{"id":"QUAL-HIGH-001","version":"1","statement":"For high-risk changes, obtain independent design and behavior/security review and meaningful negative, compatibility and recovery coverage. Identify missing permissions, environments and manual approvals; unresolved mandatory evidence blocks completion.","source_ids":["SRC-MICROSOFT-SDL","SRC-ISO-12207"],"source_alignment":"Organization-owned requirement informed by the referenced public scopes; no normative clause conformance claimed.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["planning","design","verification","review"],"verification":"hybrid","artifacts":["quality_plan","test_strategy","traceability"],"check_kind_groups":[["test"]],"waivable":true},{"id":"QUAL-AGENT-001","version":"1","statement":"For agentic systems, test the complete task-to-dispatch-to-worker-to-review-to-gate-to-return chain, including scoped context, results, state transitions, rejection, cancellation and pause/resume where supported. Test invalid or missing evidence and authority boundaries; worker-only tests do not establish chain behavior.","source_ids":["SRC-CODEX-INSTRUCTIONS","SRC-COPILOT-INSTRUCTIONS"],"source_alignment":"Organization-owned agentic-system behavioral test requirement; client documentation informs discovery limits, not a claim that either provider implements this chain.","responsibilities":["planner","implementer","quality_checker","reviewer"],"phases":["design","implementation","verification"],"verification":"hybrid","artifacts":["test_strategy","traceability"],"check_kind_groups":[["test"]],"waivable":true},{"id":"QUAL-CPP-001","version":"1","statement":"Reference-only: before enabling C++17 quality rules, review the chosen compiler/toolchain and a C++17-compatible subset of the guide, define concrete checks and portability tests, and independently review profile activation.","source_ids":["SRC-GOOGLE-CPP"],"source_alignment":"Reference-only inactive rule. Google guidance currently targets C++20; no Google C++17 rules or compliance are adopted.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan"],"check_kind_groups":[],"waivable":false},{"id":"QUAL-IEC-001","version":"1","statement":"Reference-only: before adopting a safety or medical software standard, review full authorized text, project applicability, edition-specific obligations, lifecycle evidence and any certification scheme with qualified human ownership through a separate scoped profile integration.","source_ids":["SRC-IEC-61508","SRC-IEC-62304"],"source_alignment":"Reference-only inactive rule. Public IEC product scope establishes relevance only, not clause adoption, safety integrity, medical compliance or certification.","responsibilities":["planner","reviewer"],"phases":["planning"],"verification":"manual","artifacts":["quality_plan"],"check_kind_groups":[],"waivable":false}],"profiles":[{"id":"agentic","version":"1","description":"Behavioral verification of supported agent delegation, review, gate, return and recovery chains.","enabled":true,"rules":["QUAL-AGENT-001"],"workflow_profiles":[]},{"id":"baseline","version":"1","description":"Shared requirements, design, implementation, testing, documentation, evidence, review and handoff duties.","enabled":true,"rules":["QUAL-REQ-001","QUAL-DES-001","QUAL-CODE-001","QUAL-TEST-001","QUAL-DOC-001","QUAL-EVID-001","QUAL-REVIEW-001","QUAL-HANDOFF-001"],"workflow_profiles":[]},{"id":"cpp17","version":"1","description":"Reference-only C++17 integration placeholder; compatible guide subset and compiler checks are not adopted.","enabled":false,"rules":["QUAL-CPP-001"],"workflow_profiles":[]},{"id":"high-risk","version":"1","description":"Additional independent review and negative/compatibility/recovery evidence for high-risk work.","enabled":true,"rules":["QUAL-HIGH-001"],"workflow_profiles":[]},{"id":"iec61508","version":"1","description":"Reference-only functional-safety placeholder; full-text obligations and applicability are not adopted.","enabled":false,"rules":["QUAL-IEC-001"],"workflow_profiles":[]},{"id":"iec62304","version":"1","description":"Reference-only medical-device software placeholder; full-text obligations and applicability are not adopted.","enabled":false,"rules":["QUAL-IEC-001"],"workflow_profiles":[]},{"id":"python","version":"1","description":"Python component checks; select alongside baseline and the applicable software/risk profiles.","enabled":true,"rules":["QUAL-PY-001"],"workflow_profiles":["python"]},{"id":"software","version":"1","description":"Executable software with build, lint, tests, security analysis and threat-informed review.","enabled":true,"rules":["QUAL-SW-001","QUAL-SEC-001"],"workflow_profiles":[]},{"id":"typescript","version":"1","description":"TypeScript component checks; select alongside baseline and the applicable software/risk profiles.","enabled":true,"rules":["QUAL-TS-001"],"workflow_profiles":["typescript"]}]}'
    # BEGIN COMPILED NAVIGATION GUARD
    def navigation_context(root, trusted_base=None, *, source=False, request=None,
                           expected=None, authority=None):
        """Validate routes and optionally resolve/verify a complete handoff context."""
        import fnmatch
        from functools import lru_cache
        import hashlib
        import json
        import os
        from pathlib import Path
        import re
        import stat

        technology_catalog_json = '{"version":"1.0.0","sources":[{"id":"TECH-SRC-PYTHON","title":"Python PEP 8","edition":"Living documentation observed 2026-10-14","url":"https://peps.python.org/pep-0008/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Project consistency and compatibility; imports, public interfaces and documentation guidance."]},{"id":"TECH-SRC-DOCSTRINGS","title":"Python PEP 257","edition":"Living documentation observed 2026-10-14","url":"https://peps.python.org/pep-0257/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Public docstring conventions; selected guidance, not a prescribed test or typing framework."]},{"id":"TECH-SRC-ECMASCRIPT","title":"TC39 ECMAScript control abstraction objects","edition":"Living draft titled ECMAScript 2027, observed 2026-10-14","url":"https://tc39.es/ecma262/multipage/control-abstraction-objects.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Promise fulfilled, rejected and pending states; the living draft is not a project language-version selection."]},{"id":"TECH-SRC-TYPESCRIPT","title":"TypeScript strict compiler option","edition":"Living documentation observed 2026-10-14","url":"https://www.typescriptlang.org/tsconfig/strict.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Strict option enables a family of type checks; future compiler versions can add checks."]},{"id":"TECH-SRC-JAVA","title":"Google Java Style Guide","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/styleguide/javaguide.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Formatting, naming and programming-practice guide scope; project selects compatible conventions."]},{"id":"TECH-SRC-CSHARP","title":"Microsoft C# coding conventions","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Coding conventions and consistency guidance; compiler and language versions remain project decisions."]},{"id":"TECH-SRC-GO","title":"Effective Go","edition":"Living documentation observed 2026-10-14","url":"https://go.dev/doc/effective_go","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Formatting, names, errors and concurrency guidance; the page warns it is not a comprehensive modern Go guide."]},{"id":"TECH-SRC-C","title":"SEI CERT C Coding Standard publisher description","edition":"2016 edition; publisher scope observed 2026-10-14","url":"https://www.sei.cmu.edu/library/sei-cert-c-coding-standard-rules-for-developing-safe-reliable-and-secure-systems-2016-edition/","status":"observed","access":"public-scope-only","adoption":"reference-only","verified_sections":["Publisher confirms secure C coding scope and the 2016 edition. Full rule text was not retrieved; its download redirected to a registration form."]},{"id":"TECH-SRC-CPP","title":"C++ Core Guidelines","edition":"Living documentation observed 2026-10-14","url":"https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Resource, ownership and interface guidance scope; selected project obligations do not adopt the entire guide."]},{"id":"TECH-SRC-GOOGLE-CPP","title":"Google C++ Style Guide","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/styleguide/cppguide.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["C++ version section targets C++20; self-contained headers and direct includes; no universal exception policy is imported."]},{"id":"TECH-SRC-GOOGLETEST","title":"GoogleTest Primer","edition":"Living documentation observed 2026-10-14","url":"https://google.github.io/googletest/primer.html","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Assertions, tests and fixtures as an optional test-framework example."]},{"id":"TECH-SRC-PHP","title":"PHP-FIG PER Coding Style","edition":"PER Coding Style 3.1, observed 2026-10-14","url":"https://www.php-fig.org/per/coding-style/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["PER Coding Style 3.1 page and formatting guidance; selected PHP compatibility must be checked before adoption."]},{"id":"TECH-SRC-HTML","title":"WHATWG HTML semantics and structure","edition":"Living documentation observed 2026-10-14","url":"https://html.spec.whatwg.org/multipage/dom.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Element semantics, content models and accessibility-related definitions."]},{"id":"TECH-SRC-WCAG","title":"W3C Web Content Accessibility Guidelines 2.2","edition":"WCAG 2.2, observed 2026-10-14","url":"https://www.w3.org/TR/WCAG22/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Accessibility success criteria and conformance structure; automated tests alone do not establish conformance."]},{"id":"TECH-SRC-CSS","title":"W3C CSS Snapshot 2026","edition":"W3C Group Note, 2026-06-22","url":"https://www.w3.org/TR/2026/NOTE-css-2026-20260622/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Specification-module snapshot; explicitly not a browser-adoption compatibility profile."]},{"id":"TECH-SRC-SQL","title":"PostgreSQL SQL syntax","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/sql-syntax.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["SQL language syntax overview for PostgreSQL; not a portable SQL dialect promise."]},{"id":"TECH-SRC-PG-CONSTRAINTS","title":"PostgreSQL constraints","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/ddl-constraints.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Constraint behavior including check, not-null, unique, primary-key and foreign-key constraints."]},{"id":"TECH-SRC-PG-QUERIES","title":"PostgreSQL command execution functions","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/libpq-exec.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Parameterized command execution through libpq; each application driver needs its own reviewed equivalent."]},{"id":"TECH-SRC-PG-TRANSACTIONS","title":"PostgreSQL transaction isolation","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/transaction-iso.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Transaction isolation and concurrency behavior; no blanket retry or locking policy is prescribed."]},{"id":"TECH-SRC-PG-RESTORE","title":"PostgreSQL backup and restore","edition":"PostgreSQL 18 documentation","url":"https://www.postgresql.org/docs/18/backup.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Backup methods and restore guidance overview; project recovery goals and rehearsals are organization requirements."]},{"id":"TECH-SRC-POWERSHELL","title":"PowerShell try, catch and finally","edition":"PowerShell 7.5 documentation","url":"https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Terminating error handling and resource cleanup; native process errors require separate treatment."]},{"id":"TECH-SRC-PSSCRIPTANALYZER","title":"PSScriptAnalyzer overview","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview?view=ps-modules","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Static script quality checks and configurable rules."]},{"id":"TECH-SRC-PESTER","title":"Pester quick start","edition":"Living documentation observed 2026-10-14","url":"https://pester.dev/docs/quick-start","status":"observed","access":"public-selected-sections","adoption":"tool-example-only","verified_sections":["Executable behavior tests and assertions as a PowerShell testing option."]},{"id":"TECH-SRC-SHELLCHECK","title":"ShellCheck SC2086","edition":"Living documentation observed 2026-10-14","url":"https://www.shellcheck.net/wiki/SC2086","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Quoting to control word splitting and glob expansion; intentional splitting needs an explicit reviewed design."]},{"id":"TECH-SRC-BASH","title":"GNU Bash Reference Manual","edition":"Indexed official manual observed 2026-10-14","url":"https://www.gnu.org/software/bash/manual/bash.html","status":"retrieval-limited","access":"indexed-summary-only","adoption":"reference-only","verified_sections":["Official indexed summary identifies quoting and exit status; direct page retrieval timed out, so no section-level adoption is claimed."]},{"id":"TECH-SRC-JSON","title":"RFC 8259 JSON","edition":"RFC 8259, December 2017","url":"https://www.rfc-editor.org/rfc/rfc8259","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["JSON syntax, duplicate member interoperability concerns and encoding."]},{"id":"TECH-SRC-YAML","title":"YAML specification 1.2.2","edition":"YAML 1.2.2","url":"https://yaml.org/spec/1.2.2/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Mapping key uniqueness, representation model and schema-dependent scalar resolution."]},{"id":"TECH-SRC-ACTIONS","title":"GitHub Actions workflow syntax","edition":"Living documentation observed 2026-10-14","url":"https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Workflow events, permissions, job conditions and shell execution syntax."]},{"id":"TECH-SRC-DOCKER","title":"Docker build best practices","edition":"Living documentation observed 2026-10-14","url":"https://docs.docker.com/build/building/best-practices/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Base image selection, digest pinning and limiting unnecessary image content."]},{"id":"TECH-SRC-DOCKER-SECRETS","title":"Docker build secrets","edition":"Living documentation observed 2026-10-14","url":"https://docs.docker.com/build/building/secrets/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Build secret mounts and the risks of persisting secrets through build arguments or environment variables."]},{"id":"TECH-SRC-WINDOWS","title":"Microsoft Windows file and path naming","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Reserved device names, path separators, case behavior and relative path interpretation."]},{"id":"TECH-SRC-LINUX","title":"Linux kernel user-space API guide","edition":"Living documentation observed 2026-10-14","url":"https://docs.kernel.org/userspace-api/index.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["User-space API documentation scope; distro, shell and native-test support remain project obligations."]},{"id":"TECH-SRC-NODE","title":"Node.js errors","edition":"Living documentation observed 2026-10-14","url":"https://nodejs.org/api/errors.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Error propagation and errors from asynchronous APIs; displayed runtime version is not adopted for consumers."]},{"id":"TECH-SRC-DOTNET","title":"Microsoft testing in .NET","edition":"Living documentation observed 2026-10-14","url":"https://learn.microsoft.com/en-us/dotnet/core/testing/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Testing framework and test runner overview; target frameworks and runtime support are project choices."]},{"id":"TECH-SRC-JVM","title":"Java Virtual Machine Specification","edition":"Java SE 21 edition","url":"https://docs.oracle.com/javase/specs/jvms/se21/html/index.html","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Class-file format, loading, linking and execution model contents; selected JDK/runtime compatibility requires executable tests."]},{"id":"TECH-SRC-REACT","title":"Rules of React","edition":"Living documentation observed 2026-10-14","url":"https://react.dev/reference/rules","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Component and Hook purity, call order and use through React."]},{"id":"TECH-SRC-NEXTJS","title":"Next.js server and client components","edition":"Living documentation observed 2026-10-14","url":"https://nextjs.org/docs/app/getting-started/server-and-client-components","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["Server/client boundaries, serializable props and avoiding environment poisoning."]},{"id":"TECH-SRC-FASTAPI","title":"FastAPI testing tutorial","edition":"Living documentation observed 2026-10-14","url":"https://fastapi.tiangolo.com/tutorial/testing/","status":"observed","access":"public-selected-sections","adoption":"organization-owned-selection","verified_sections":["TestClient-based requests and assertions; authorization, persistence and lifecycle coverage are project risk-based additions."]}],"rules":[{"id":"TECH-PYTHON-001","version":"1","statement":"MUST: Record supported Python versions and one compatible style/type configuration. Keep changed public interfaces documented; type-check new application boundaries, validate external input and preserve useful exception context. Bind lint, typecheck and behavior tests, including relevant failure paths. Document generated/vendor exclusions and legacy typing debt without silently widening them.","source_ids":["TECH-SRC-PYTHON","TECH-SRC-DOCSTRINGS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["typecheck"],["test"]]},{"id":"TECH-JAVASCRIPT-001","version":"1","statement":"MUST: Record the ECMAScript target, supported hosts and module system. Validate external values, handle asynchronous rejection and avoid runtime code evaluation of untrusted input. Bind a consistent lint configuration and tests for observable success and failure behavior on the supported hosts.","source_ids":["TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-TYPESCRIPT-001","version":"1","statement":"MUST: Record compiler, runtime and ECMAScript targets. Enable strict type checking for new components; inventory inherited exceptions and justify any new suppression or unsafe any at a boundary. Validate external data at runtime and handle asynchronous failures. Bind lint, typecheck and tests without disabling checks to pass.","source_ids":["TECH-SRC-TYPESCRIPT","TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["typecheck"],["test"]]},{"id":"TECH-JAVA-001","version":"1","statement":"MUST: Record the supported JDK/language target and selected compatible style subset. Use a consistent formatter, preserve public contracts, close owned resources and handle exceptions without losing their cause. Bind compilation, lint/static analysis and tests on the promised runtime versions.","source_ids":["TECH-SRC-JAVA"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-CSHARP-001","version":"1","statement":"MUST: Record C# language and target-framework versions. Configure consistent formatting and analyzers; make null handling, disposable-resource ownership and asynchronous cancellation explicit at affected boundaries. Bind compilation, lint/analyzer and behavior tests; justify suppressions in review.","source_ids":["TECH-SRC-CSHARP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-GO-001","version":"1","statement":"MUST: Record supported Go versions. Apply gofmt, handle returned errors and bound the lifetime of started goroutines and owned resources. Bind build, lint/static analysis and tests; assess race testing for changed shared-state code and record its result or concrete unsupported-platform limit.","source_ids":["TECH-SRC-GO"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-C-001","version":"1","statement":"MUST: Record the C language edition, compiler targets and selected warning/analyzer configuration. Review buffer bounds, integer conversions, resource ownership and error returns in changed code. Bind build, lint/static analysis and boundary/failure tests; document sanitizer applicability and results for memory-risk changes.","source_ids":["TECH-SRC-C"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-CPP-001","version":"1","statement":"MUST: Record the C++ edition, compiler targets and a compatible chosen guide subset. Make ownership explicit, use automatic resource lifetime management, keep public headers self-contained and adopt one reviewed exception/error policy. Resolve Google/Core Guidelines conflicts before work. Bind build, lint/static analysis and behavior tests, with appropriate lifetime and boundary checks.","source_ids":["TECH-SRC-CPP","TECH-SRC-GOOGLE-CPP","TECH-SRC-GOOGLETEST"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["lint"],["test"]]},{"id":"TECH-PHP-001","version":"1","statement":"MUST: Record supported PHP versions and a compatible PER/PSR style selection. Validate request and persistence boundaries, handle errors explicitly and document public interfaces. Bind syntax/style/static analysis and tests; preserve framework conventions where reviewed and compatible.","source_ids":["TECH-SRC-PHP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-HTML-001","version":"1","statement":"MUST: Record supported browsers and the accessibility target. Use appropriate semantic elements, accessible names, labels and keyboard-operable controls. Bind markup lint/validation and rendered behavior tests; manually verify relevant accessibility criteria that automation cannot establish.","source_ids":["TECH-SRC-HTML","TECH-SRC-WCAG"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-CSS-001","version":"1","statement":"MUST: Record supported browsers and responsive/accessibility requirements. Select compatible CSS features and a consistent lint configuration. Preserve focus visibility and content usability under required resizing/zoom. Bind lint and rendered layout/interaction tests for affected critical views.","source_ids":["TECH-SRC-CSS","TECH-SRC-WCAG"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-SQL-001","version":"1","statement":"MUST: Record the database dialect and server/driver versions. Parameterize values; validate or safely select dynamic identifiers through the driver contract. State transaction boundaries and handle null semantics explicitly. Bind dialect-aware lint/validation and query behavior tests against the actual database dialect; a substitute dialect does not prove compatibility.","source_ids":["TECH-SRC-SQL","TECH-SRC-PG-QUERIES"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-POSTGRESQL-001","version":"1","statement":"MUST: Record supported PostgreSQL versions, extensions and driver settings. Use parameterized queries, appropriate constraints and least-privilege roles. Specify transaction/isolation and retry behavior. Bind real PostgreSQL integration tests and migration checks that preserve existing data; review lock/concurrency failure paths and rehearse restore or forward recovery according to the documented data-risk plan.","source_ids":["TECH-SRC-PG-CONSTRAINTS","TECH-SRC-PG-QUERIES","TECH-SRC-PG-TRANSACTIONS","TECH-SRC-PG-RESTORE"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"],["migration"]]},{"id":"TECH-POWERSHELL-001","version":"1","statement":"MUST: Record PowerShell edition/version and supported operating systems. Validate parameters, use literal-safe paths where appropriate, distinguish terminating/nonterminating errors from native process exit codes and clean up owned resources. Bind script analysis and behavior tests with failed commands, missing files and paths containing spaces; never log secrets.","source_ids":["TECH-SRC-POWERSHELL","TECH-SRC-PSSCRIPTANALYZER","TECH-SRC-PESTER"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-BASH-001","version":"1","statement":"MUST: Record the Bash interpreter version and target platforms; do not label Bash-specific code as portable sh. Quote expansions according to intended splitting/globbing, use argument arrays where appropriate, check command/pipeline failures and clean up temporary resources. Bind shell analysis and real script tests for whitespace paths, failed subprocesses and cleanup. Do not treat set -e alone as error-handling proof.","source_ids":["TECH-SRC-SHELLCHECK","TECH-SRC-BASH"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-JSON-001","version":"1","statement":"MUST: Record the consuming schema/parser contract. Validate syntax and required fields; reject duplicate keys in policy or security-sensitive inputs and avoid nonportable numeric assumptions. Bind schema/parser validation under a lint check; test changed loader behavior when executable parsing logic changes.","source_ids":["TECH-SRC-JSON"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"]]},{"id":"TECH-YAML-001","version":"1","statement":"MUST: Record parser/version and the consuming schema, including scalar-resolution behavior. Reject duplicate mapping keys, avoid executable object construction from untrusted input and validate required fields. Bind parser/schema lint and test changed loaders with ambiguous scalars or tags when relevant.","source_ids":["TECH-SRC-YAML"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"]]},{"id":"TECH-DOCKERFILE-001","version":"1","statement":"MUST: Record builder, target platform and trusted base-image digests with a reviewed update process. Keep build secrets out of arguments, layers and final images; minimize final contents and select least-privilege runtime users. Bind Dockerfile lint and checks that build and inspect the intended image; document justified runtime privilege requirements.","source_ids":["TECH-SRC-DOCKER","TECH-SRC-DOCKER-SECRETS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["container"]]},{"id":"TECH-GITHUB-ACTIONS-001","version":"1","statement":"MUST: Record workflow triggers, approved runners and explicit token permissions. Pin external actions to reviewed immutable identities, keep untrusted event data out of shell interpolation and prevent privileged execution of untrusted changes. Bind workflow lint and negative tests for required-check/gate behavior; cancelled, missing or unjustifiably skipped required checks must not become success.","source_ids":["TECH-SRC-ACTIONS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["test"]]},{"id":"TECH-WINDOWS-001","version":"1","statement":"MUST: Record supported Windows versions and architectures. Respect reserved names, case behavior, path/encoding and native process semantics. Bind tests on the promised native Windows environment covering affected path and failure behavior. A Linux container or WSL run alone is not native Windows acceptance evidence.","source_ids":["TECH-SRC-WINDOWS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"]]},{"id":"TECH-LINUX-001","version":"1","statement":"MUST: Record supported Linux distributions or base images, architectures and required user-space dependencies. Handle case-sensitive paths, permissions, signals and process cleanup. Bind tests on the promised Linux environment; distinguish container user-space checks from host/kernel behavior requiring native validation.","source_ids":["TECH-SRC-LINUX"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"]]},{"id":"TECH-NODE-001","version":"1","statement":"MUST: Record Node.js, package-manager and module-system versions. Use reproducible dependency installation from the reviewed lockfile, handle asynchronous errors and validate process shutdown behavior. Bind runtime tests and dependency checks; test native addons on supported platform/runtime combinations when present.","source_ids":["TECH-SRC-NODE","TECH-SRC-ECMASCRIPT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["test"],["dependency"]]},{"id":"TECH-DOTNET-001","version":"1","statement":"MUST: Record SDK and target-framework/runtime versions and supported operating systems. Restore reviewed dependency versions and preserve target-framework compatibility. Bind build, tests and dependency checks for the claimed targets; test platform-specific or native interop behavior on the affected targets.","source_ids":["TECH-SRC-DOTNET","TECH-SRC-CSHARP"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["test"],["dependency"]]},{"id":"TECH-JVM-001","version":"1","statement":"MUST: Record JDK/compiler and deployment JVM versions plus bytecode target. Use reviewed reproducible dependency resolution, preserve class-loading and public binary compatibility where promised and handle shutdown/resources. Bind build, tests and dependency checks on supported runtimes, including changed native interop.","source_ids":["TECH-SRC-JVM","TECH-SRC-JAVA"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["test"],["dependency"]]},{"id":"TECH-DOCKER-001","version":"1","statement":"MUST: Record container engine/target-platform and host assumptions. Run the built image with declared least privileges, external secret delivery and explicit persistent-data ownership. Bind image/container checks and start, readiness, shutdown and failure tests on the actual artifact; document host-dependent and recovery evidence separately.","source_ids":["TECH-SRC-DOCKER","TECH-SRC-DOCKER-SECRETS"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["container"],["test"]]},{"id":"TECH-REACT-001","version":"1","statement":"MUST: Record React and rendering-environment versions. Preserve component/Hook purity and Hook call rules; clean up effects and asynchronous work. Bind framework-aware lint and user-visible behavior tests covering affected loading, error and interaction states; preserve accessible semantics.","source_ids":["TECH-SRC-REACT","TECH-SRC-HTML"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["lint"],["browser","test"]]},{"id":"TECH-NEXTJS-001","version":"1","statement":"MUST: Record Next.js version and selected router/runtime. Keep server-only secrets and dependencies across the correct server/client boundary, validate serialized boundary data and specify caching/authentication behavior. Bind a production build and route/interaction tests covering affected server, client and authorization cases.","source_ids":["TECH-SRC-NEXTJS","TECH-SRC-REACT"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["build"],["browser","test"]]},{"id":"TECH-FASTAPI-001","version":"1","statement":"MUST: Record FastAPI, Pydantic and ASGI/runtime versions. Validate request/response contracts, enforce authorization, handle dependency/lifespan cleanup and avoid blocking asynchronous handlers with unbounded synchronous work. Bind API and behavior tests for success, rejection and relevant persistence/lifespan failures using realistic dependencies where integration matters.","source_ids":["TECH-SRC-FASTAPI","TECH-SRC-PYTHON"],"source_alignment":"Organization-owned minimum informed by the recorded source scope. Source language versions, examples and optional tools are not automatically adopted; no blanket guide, ISO/IEC or certification conformance is claimed.","check_kind_groups":[["api"],["test"]]}],"profiles":[{"id":"bash","version":"1","category":"shell","description":"Bash component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-BASH-001"],"quality_profiles":[],"recommendations":["Prefer ShellCheck with the declared shell dialect.","Keep shell adapters small; use Python for substantial shared cross-platform logic when practical."],"free_choices":["Control flow and helpers that preserve exit-status and argument semantics."]},{"id":"c","version":"1","category":"language","description":"C component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-C-001"],"quality_profiles":[],"recommendations":["Prefer bounded interfaces and one explicit resource-ownership convention.","Review full authorized CERT clauses before claiming clause conformance; only its publisher scope is recorded here."],"free_choices":["Data layout and algorithms within memory, ABI and platform constraints."]},{"id":"cpp","version":"1","category":"language","description":"C++ component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CPP-001"],"quality_profiles":[],"recommendations":["Prefer standard ownership types and project-approved clang-format/clang-tidy settings.","GoogleTest is an optional framework; a C++17 project must select compatible guide rules and tool releases rather than adopting a living C++20 guide wholesale."],"free_choices":["Internal templates, algorithms and abstractions supported by the chosen compiler and error policy."]},{"id":"csharp","version":"1","category":"language","description":"C# component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CSHARP-001"],"quality_profiles":[],"recommendations":["Prefer established Microsoft naming conventions and project-approved nullable analysis settings.","Propagate cancellation through operations that support cancellation."],"free_choices":["Internal types, records and decomposition when they preserve compatibility."]},{"id":"css","version":"1","category":"language","description":"CSS component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-CSS-001"],"quality_profiles":[],"recommendations":["Prefer established design tokens and component styles.","Treat the CSS snapshot as a standards inventory, not proof of browser support."],"free_choices":["Layout techniques, selectors and local styling choices that meet the contract."]},{"id":"docker","version":"1","category":"container","description":"Docker runtime component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOCKER-001"],"quality_profiles":[],"recommendations":["Prefer read-only filesystems and constrained resources when compatible with application needs.","Keep health/readiness checks aligned with actual service readiness."],"free_choices":["Image/runtime composition within the approved security, data and operating contract."]},{"id":"dockerfile","version":"1","category":"container","description":"Dockerfile component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOCKERFILE-001"],"quality_profiles":[],"recommendations":["Prefer multistage builds and a maintained minimal base appropriate to the application.","Use build-secret mounts where supported."],"free_choices":["Build-stage structure and caching strategy preserving reproducibility and secret boundaries."]},{"id":"dotnet","version":"1","category":"runtime","description":".NET component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-DOTNET-001"],"quality_profiles":[],"recommendations":["Use existing test-runner conventions and centrally reviewed dependency management where available."],"free_choices":["Internal assembly organization and test framework within the approved runtime contract."]},{"id":"fastapi","version":"1","category":"framework","description":"FastAPI component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-FASTAPI-001"],"quality_profiles":["python"],"recommendations":["Prefer dependency overrides for bounded unit/API tests and real infrastructure for critical integration contracts.","Keep schemas and documented API behavior synchronized."],"free_choices":["Internal dependency and service organization within the agreed API and lifecycle contracts."]},{"id":"github-actions","version":"1","category":"automation","description":"GitHub Actions component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-GITHUB-ACTIONS-001"],"quality_profiles":[],"recommendations":["Reuse the approved Backbone workflow contract and keep executable logic in reviewed scripts.","Prefer minimal job permissions and explicit shell selection."],"free_choices":["Job decomposition and safe parallelism within the existing runner and gate contracts."]},{"id":"go","version":"1","category":"language","description":"Go component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-GO-001"],"quality_profiles":[],"recommendations":["Prefer idiomatic small interfaces and explicit context propagation where cancellation is part of the contract.","Use go vet and race testing where supported; Effective Go alone is not the complete modern language specification."],"free_choices":["Package internals and concurrency mechanisms that satisfy the lifetime and correctness requirements."]},{"id":"html","version":"1","category":"language","description":"HTML component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-HTML-001"],"quality_profiles":[],"recommendations":["Use WCAG 2.2 AA as the default project accessibility target unless a reviewed project obligation requires another target.","Prefer native controls before custom interactive elements."],"free_choices":["Document composition and visual structure within semantics and accessibility constraints."]},{"id":"java","version":"1","category":"language","description":"Java component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JAVA-001"],"quality_profiles":[],"recommendations":["Prefer the standard resource-management constructs and existing project patterns.","Google Java conventions are a candidate subset; do not import an incompatible language feature."],"free_choices":["Class decomposition and algorithms; interfaces are needed only when justified by the design."]},{"id":"javascript","version":"1","category":"language","description":"JavaScript component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JAVASCRIPT-001"],"quality_profiles":[],"recommendations":["Prefer TypeScript for new application modules when the approved project architecture supports it; JavaScript remains supported.","Prefer established module and asynchronous patterns in the project."],"free_choices":["Internal helpers and algorithms, including async/await versus equivalent correctly handled promises."]},{"id":"json","version":"1","category":"format","description":"JSON component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JSON-001"],"quality_profiles":[],"recommendations":["Use UTF-8 and a single consistent formatter.","Prefer explicit schemas for shared contracts."],"free_choices":["Object organization allowed by the authoritative schema."]},{"id":"jvm","version":"1","category":"runtime","description":"JVM component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-JVM-001"],"quality_profiles":[],"recommendations":["Keep compiler target and deployment runtime compatibility explicit.","Prefer the existing approved build tool."],"free_choices":["Module and package internals within the runtime and binary contract."]},{"id":"linux","version":"1","category":"platform","description":"Linux component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-LINUX-001"],"quality_profiles":[],"recommendations":["Prefer portable APIs and least-privilege execution.","Keep distro-specific assumptions documented."],"free_choices":["Internal adapters satisfying the actual distribution and kernel boundary."]},{"id":"nextjs","version":"1","category":"framework","description":"Next.js component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-NEXTJS-001"],"quality_profiles":[],"recommendations":["Prefer the existing router and deployment model; migrations require explicit planning.","Minimize client boundaries when behavior permits."],"free_choices":["Internal components and route implementation within the approved rendering and data contracts."]},{"id":"node","version":"1","category":"runtime","description":"Node.js component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-NODE-001"],"quality_profiles":[],"recommendations":["Prefer maintained runtime lines selected through reviewed updates.","Use existing project scripts for equivalent local and CI checks."],"free_choices":["Package internal organization and approved asynchronous patterns."]},{"id":"php","version":"1","category":"language","description":"PHP component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-PHP-001"],"quality_profiles":[],"recommendations":["Prefer current project conventions and typed public boundaries where supported.","Use a reviewed subset of PER Coding Style compatible with the selected PHP version."],"free_choices":["Internal class/function organization and approved framework patterns."]},{"id":"postgresql","version":"1","category":"database","description":"PostgreSQL component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-POSTGRESQL-001"],"quality_profiles":[],"recommendations":["Test migrations from representative prior schema/data as well as fresh installation.","Prefer reversible changes when safe; use reviewed forward recovery when reversing would lose data."],"free_choices":["Schema normalization and index designs within approved data contracts and measured performance requirements."]},{"id":"powershell","version":"1","category":"shell","description":"PowerShell component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-POWERSHELL-001"],"quality_profiles":[],"recommendations":["Prefer PSScriptAnalyzer and Pester or reviewed equivalent checks.","Keep platform adapters small and use Python for shared cross-platform automation logic when practical."],"free_choices":["Functions and parameter structure within the approved command and platform contract."]},{"id":"python","version":"1","category":"language","description":"Python component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-PYTHON-001"],"quality_profiles":["python"],"recommendations":["Prefer standard-library facilities and existing project conventions; document deviations through normal review.","Ruff, mypy and pytest are examples; use approved project equivalents when they establish the same obligations."],"free_choices":["Internal function decomposition and suitable algorithms within the accepted contracts."]},{"id":"react","version":"1","category":"framework","description":"React component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-REACT-001"],"quality_profiles":[],"recommendations":["Prefer existing component and state-management patterns.","Use effects for external synchronization rather than avoidable derived state."],"free_choices":["Component decomposition and local state choices consistent with the architectural boundaries."]},{"id":"sql","version":"1","category":"language","description":"SQL component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-SQL-001"],"quality_profiles":[],"recommendations":["Prefer constraints for database invariants and readable explicit queries.","Use PostgreSQL rules as an additional profile when PostgreSQL is the selected dialect."],"free_choices":["Equivalent query structure and indexing proposals supported by measured plans and correctness tests."]},{"id":"typescript","version":"1","category":"language","description":"TypeScript component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-TYPESCRIPT-001"],"quality_profiles":["typescript"],"recommendations":["Prefer explicit boundary types and narrowing over unchecked assertions.","Select one formatter and a compatible typed lint configuration."],"free_choices":["Internal inferred types, helper layout and algorithms consistent with the public contract."]},{"id":"windows","version":"1","category":"platform","description":"Windows component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-WINDOWS-001"],"quality_profiles":[],"recommendations":["Prefer portable path/process APIs and explicit text encodings.","Keep operating-system-specific handling isolated."],"free_choices":["Internal adapters compatible with the documented Windows support contract."]},{"id":"yaml","version":"1","category":"format","description":"YAML component obligations; the project records supported versions and the selected tool configuration.","rules":["TECH-YAML-001"],"quality_profiles":[],"recommendations":["Quote scalar values whose interpretation varies across approved consumers.","Prefer straightforward mappings over complex aliases when readability improves."],"free_choices":["Mapping layout allowed by the consumer contract."]}]}'
        roles = {'planner', 'implementer', 'reviewer', 'quality_checker', 'triage'}
        tasks = {'bugfix', 'implementation', 'architecture', 'review', 'documentation'}
        manifest_path = '.engineering-backbone/navigation.json'
        profile_path = '.engineering-backbone/quality-profile.json'
        workflows_path = '.engineering-backbone/workflows.json'
        dependencies_path = '.engineering-backbone/dependencies.json'
        dependency_policy_path = ('policy/dependencies.md' if source else
                                  '.engineering-backbone/dependency-policy.md')
        missing = object()

        def fail(message):
            raise ValueError(message)

        def text(value, label, limit=4096):
            if (not isinstance(value, str) or not value.strip() or len(value) > limit
                    or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value)):
                fail('Invalid ' + label)
            value.encode('utf-8')
            return value

        def keys(value, names, label):
            if not isinstance(value, dict) or set(value) != set(names):
                fail(label + ' has missing or unknown keys')

        def identifier(value):
            if not isinstance(value, str) or re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,63}', value) is None:
                fail('Invalid identifier')
            return value

        def sequence(value, label, *, nonempty=False, maximum=256):
            if (not isinstance(value, list) or len(value) > maximum
                    or nonempty and not value):
                fail('Invalid ' + label)
            for item in value:
                text(item, label)
            if len(value) != len(set(value)):
                fail('Duplicate ' + label)
            return value

        def relative(value, *, anchor=False):
            value = text(value, 'relative path', 512)
            pieces = value.split('#')
            if len(pieces) > (2 if anchor else 1):
                fail('Unexpected path anchor')
            if anchor and len(pieces) == 2 and re.fullmatch(r'[a-z0-9][a-z0-9_-]*', pieces[1]) is None:
                fail('Anchor must be a lowercase portable Markdown heading ID')
            path = pieces[0]
            for part in path.split('/'):
                if (part in ('', '.', '..') or part[-1:] in ('.', ' ')
                        or any(c in part for c in '\\:<>"|?*')
                        or re.fullmatch(r'(?i)(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', part)):
                    fail('Unsafe or nonportable relative path')
            return path, pieces[1] if len(pieces) == 2 else None

        def scope_match(path, pattern):
            # Glob matching is segment-aware: * and ? never cross '/', while a
            # complete ** segment matches zero or more path segments.
            names, patterns = path.split('/'), pattern.split('/')

            @lru_cache(maxsize=None)
            def match(index, position):
                if position == len(patterns):
                    return index == len(names)
                if patterns[position] == '**':
                    return match(index, position + 1) or (
                        index < len(names) and match(index + 1, position))
                return index < len(names) and fnmatch.fnmatchcase(names[index], patterns[position]) and match(index + 1, position + 1)

            return match(0, 0)

        def linked(info):
            return stat.S_ISLNK(info.st_mode) or bool(
                getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0))

        def folder_path(value):
            value = Path(os.path.abspath(value))
            current = Path(value.anchor)
            for part in value.parts[1:]:
                current /= part
                info = current.lstat()
                if linked(info) or not stat.S_ISDIR(info.st_mode):
                    fail('Root has symlink or non-directory ancestor')
            return value

        def locate(folder, name, *, optional=False):
            path, _ = relative(name)
            current = folder
            for index, part in enumerate(path.split('/')):
                if not current.is_dir():
                    fail('Non-directory path ancestor')
                matches = [entry.name for entry in current.iterdir() if entry.name.casefold() == part.casefold()]
                if len(matches) > 1 or matches and matches[0] != part:
                    fail('Case mismatch or ambiguous path: ' + name)
                current /= part
                try:
                    info = current.lstat()
                    mode = info.st_mode
                except FileNotFoundError:
                    if optional:
                        return None
                    fail('Required document or directory absent: ' + name)
                if linked(info):
                    fail('Symlink in navigation path: ' + name)
                if index < len(path.split('/')) - 1 and not stat.S_ISDIR(mode):
                    fail('Non-directory path ancestor')
            return current

        def read(folder, name, *, optional=False, limit=1048576):
            path = locate(folder, name, optional=optional)
            if path is None:
                return missing
            if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > limit:
                fail('Nonregular or oversized navigation input: ' + name)
            data = path.read_bytes()
            if len(data) > limit:
                fail('Oversized navigation input: ' + name)
            return data

        def pairs(items):
            result = {}
            for key, value in items:
                if key in result:
                    fail('Duplicate JSON key')
                result[key] = value
            return result

        def decode(data):
            return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                              parse_constant=lambda value: fail('Invalid JSON number'))

        def json_file(folder, name, *, optional=False):
            data = read(folder, name, optional=optional, limit=262144)
            return missing if data is missing else decode(data)

        def digest(value):
            return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                            separators=(',', ':')).encode('utf-8')).hexdigest()

        def document(folder, reference):
            name, anchor = relative(reference, anchor=True)
            data = read(folder, name)
            content = data.decode('utf-8')
            if not content.strip() or '\x00' in content:
                fail('Empty or invalid navigation document: ' + name)
            if anchor:
                # Deliberately narrow heading convention; arbitrary HTML IDs, Setext
                # headings and renderer-specific punctuation are not assumed.
                headings, counts, fenced = set(), {}, False
                for line in content.splitlines():
                    if re.match(r'^\s*(```|~~~)', line):
                        fenced = not fenced
                        continue
                    match = re.match(r'^ {0,3}#{1,6} ([A-Za-z0-9 _-]+?)(?: +#+)?\s*$', line)
                    if match and not fenced:
                        slug = match[1].strip().lower().replace(' ', '-')
                        count = counts.get(slug, 0)
                        counts[slug] = count + 1
                        headings.add(slug + ('-' + str(count) if count else ''))
                if anchor not in headings:
                    fail('Missing or unsupported Markdown heading anchor: ' + reference)
            return {'path': reference, 'sha256': hashlib.sha256(data).hexdigest()}

        def package(folder, catalog):
            prefix = 'standards/technologies' if source else '.engineering-backbone/standards/technologies'
            for name in ('sources', 'rules'):
                wanted = {'schema_version': '1', 'version': catalog['version'], name: catalog[name]}
                if json_file(folder, prefix + '/' + name + '.json') != wanted:
                    fail('Managed technology ' + name + ' differs from trusted authority')
            directory = locate(folder, prefix + '/profiles')
            if not directory.is_dir():
                fail('Technology profiles path is not a directory')
            actual = {path.name for path in directory.iterdir()}
            if actual != {entry['id'] + '.json' for entry in catalog['profiles']}:
                fail('Managed technology profile set differs from trusted authority')
            for entry in catalog['profiles']:
                if json_file(folder, prefix + '/profiles/' + entry['id'] + '.json') != entry:
                    fail('Managed technology profile differs from trusted authority')
            return prefix

        def effective_workflow(folder, approved_root=None):
            value = json_file(folder, workflows_path, optional=True)
            if not isinstance(value, dict):
                return value

            def check_map(workflow):
                result = {}
                for check in workflow.get('checks', []):
                    if not isinstance(check, dict) or check.get('id') in result:
                        fail('Malformed or duplicate workflow check')
                    result[check.get('id')] = check
                return result

            current = check_map(value)
            if approved_root is None:
                return value
            approved = json_file(approved_root, workflows_path, optional=True)
            if not isinstance(approved, dict) or approved.get('enabled') is not True:
                return value
            approved_checks = check_map(approved)
            # Match workflow preparation: an existing ID executes the full approved
            # definition. Only genuinely new IDs retain candidate definitions.
            return dict(value, checks=[approved_checks.get(key, check)
                                       for key, check in current.items()])

        def manifest(folder, catalog, *, complete=False, approved_root=None):
            value = json_file(folder, manifest_path, optional=True)
            if value is missing:
                return None
            keys(value, {'schema_version', 'enabled', 'documents', 'always', 'roles', 'tasks', 'components'},
                 'Navigation manifest')
            if value['schema_version'] != '1' or type(value['enabled']) is not bool:
                fail('Invalid navigation schema or activation flag')
            package(folder, catalog)
            documents = value['documents']
            if not isinstance(documents, dict) or len(documents) > 256:
                fail('Invalid navigation documents')
            for key, reference in documents.items():
                identifier(key)
                document(folder, reference)

            def refs(items):
                sequence(items, 'document references')
                if set(items) - set(documents):
                    fail('Unknown navigation document ID')

            refs(value['always'])
            for field, names in (('roles', roles), ('tasks', tasks)):
                keys(value[field], names, 'Navigation ' + field)
                for items in value[field].values():
                    refs(items)
            components = value['components']
            if not isinstance(components, list) or len(components) > 256:
                fail('Invalid components')
            profiles = {item['id']: item for item in catalog['profiles']}
            rules = {item['id']: item for item in catalog['rules']}
            found = set()
            quality = json_file(folder, profile_path, optional=True)
            workflow = effective_workflow(folder, approved_root)
            active = complete or value['enabled']
            if active and (not isinstance(quality, dict) or quality.get('enabled') is not True
                           or not isinstance(workflow, dict) or workflow.get('enabled') is not True):
                fail('Active navigation requires active quality and workflow profiles')
            checks = {}
            if isinstance(workflow, dict):
                for check in workflow.get('checks', []):
                    if not isinstance(check, dict) or check.get('id') in checks:
                        fail('Malformed or duplicate workflow check')
                    checks[check.get('id')] = check
            for component in components:
                keys(component, {'id', 'paths', 'profiles', 'documents', 'checks'}, 'Component')
                key = identifier(component['id'])
                if key in found:
                    fail('Duplicate component ID')
                found.add(key)
                sequence(component['paths'], 'component paths', nonempty=True)
                for path in component['paths']:
                    relative(path)
                    locate(folder, path, optional=True)
                sequence(component['profiles'], 'technology profiles', nonempty=True)
                if set(component['profiles']) - set(profiles):
                    fail('Unknown technology profile')
                refs(component['documents'])
                selected = {rule for profile in component['profiles'] for rule in profiles[profile]['rules']}
                required_quality = {profile for name in component['profiles'] for profile in profiles[name]['quality_profiles']}
                if active and required_quality - set(quality.get('profiles', [])):
                    fail('Required quality profile missing for technology component')
                bindings = component['checks']
                if not isinstance(bindings, list) or len(bindings) > 256:
                    fail('Invalid component check bindings')
                bound = {}
                for binding in bindings:
                    keys(binding, {'rule_id', 'check_ids'}, 'Technology check binding')
                    rule = identifier(binding['rule_id'])
                    if rule not in selected or rule in bound:
                        fail('Unknown, unselected or duplicate technology rule binding')
                    sequence(binding['check_ids'], 'technology check IDs', nonempty=True, maximum=100)
                    for check in binding['check_ids']:
                        identifier(check)
                        if check not in checks or 'pr' not in checks[check].get('phases', []):
                            fail('Technology check binding must reference a PR workflow check')
                    bound[rule] = binding['check_ids']
                if active:
                    for rule in selected:
                        covered = {checks[key].get('kind') for key in bound.get(rule, [])}
                        if any(not covered.intersection(group) for group in rules[rule]['check_kind_groups']):
                            fail('Required technology check-kind coverage missing: ' + rule)
            if active and not components:
                fail('Active navigation requires mapped components')
            return value

        def inherited(candidate, base):
            if base is None or not base['enabled']:
                return
            if candidate is None or not candidate['enabled']:
                fail('Active navigation cannot be removed or disabled')
            if any(candidate['documents'].get(key) != value for key, value in base['documents'].items()):
                fail('Inherited navigation document targets cannot be removed or remapped')
            for field in ('always',):
                if set(base[field]) - set(candidate[field]):
                    fail('Inherited mandatory document route cannot be removed')
            for field in ('roles', 'tasks'):
                for route in base[field]:
                    if set(base[field][route]) - set(candidate[field][route]):
                        fail('Inherited role or task document route cannot be removed')
            current = {item['id']: item for item in candidate['components']}
            for previous in base['components']:
                now = current.get(previous['id'])
                if now is None:
                    fail('Inherited component cannot be removed')
                for field in ('paths', 'profiles', 'documents'):
                    if set(previous[field]) - set(now[field]):
                        fail('Inherited component routing cannot be weakened')
                bindings = {item['rule_id']: set(item['check_ids']) for item in now['checks']}
                for binding in previous['checks']:
                    if set(binding['check_ids']) - bindings.get(binding['rule_id'], set()):
                        fail('Inherited technology check bindings cannot be removed')

        dependency_file_fields = ('manifests', 'resolution_files', 'runtime_files', 'dockerfiles')

        def dependency_artifact(folder, name):
            # Native manifests and resolutions can be large or non-Markdown. Hash
            # their actual bytes without interpreting or executing package tooling.
            relative(name)
            data = read(folder, name, limit=16777216)
            if not data.strip():
                fail('Empty dependency artifact: ' + name)
            return {'path': name, 'sha256': hashlib.sha256(data).hexdigest()}

        def dependency_paths(component):
            return {component['compatibility_document']} | {
                path for field in dependency_file_fields for path in component[field]}

        def dependencies(folder, navigation, *, complete=False, approved_root=None):
            value = json_file(folder, dependencies_path, optional=True)
            if value is missing:
                return None
            keys(value, {'schema_version', 'enabled', 'components'}, 'Dependency contract')
            if value['schema_version'] != '1' or type(value['enabled']) is not bool:
                fail('Invalid dependency schema or activation flag')
            components = value['components']
            if not isinstance(components, list) or len(components) > 256:
                fail('Invalid dependency components')
            active = complete or value['enabled']
            workflow = effective_workflow(folder, approved_root)
            quality = json_file(folder, profile_path, optional=True)
            if active:
                if (navigation is None or navigation['enabled'] is not True
                        or not isinstance(quality, dict) or quality.get('enabled') is not True
                        or not isinstance(workflow, dict) or workflow.get('enabled') is not True):
                    fail('Active dependencies require active navigation, quality and workflow profiles')
                if not components:
                    fail('Active dependencies require mapped components')
                document(folder, dependency_policy_path)
            mapped = {} if navigation is None else {item['id']: item for item in navigation['components']}
            checks = {} if not isinstance(workflow, dict) else {item['id']: item for item in workflow.get('checks', [])}
            found = set()
            for component in components:
                keys(component, {'id', 'kind', 'compatibility_document', 'check_ids',
                                 *dependency_file_fields}, 'Dependency component')
                key = identifier(component['id'])
                if key in found:
                    fail('Duplicate dependency component ID')
                found.add(key)
                if component['kind'] not in {'application', 'library', 'tooling'}:
                    fail('Invalid dependency component kind')
                relative(component['compatibility_document'])
                document(folder, component['compatibility_document'])
                for field in dependency_file_fields:
                    sequence(component[field], 'dependency ' + field,
                             nonempty=field == 'manifests' or
                             field == 'resolution_files' and component['kind'] != 'library')
                    for path in component[field]:
                        dependency_artifact(folder, path)
                sequence(component['check_ids'], 'dependency check IDs', maximum=100)
                for check in component['check_ids']:
                    identifier(check)
                if not active:
                    continue
                if key not in mapped:
                    fail('Unknown dependency navigation component: ' + key)
                for path in dependency_paths(component):
                    if not any(path == prefix or path.startswith(prefix + '/') for prefix in mapped[key]['paths']):
                        fail('Dependency file is outside its component navigation paths: ' + path)
                for check in component['check_ids']:
                    if check not in checks or 'pr' not in checks[check].get('phases', []):
                        fail('Dependency check binding must reference a PR workflow check')
                required = {'dependency', 'build', 'test'}
                if component['dockerfiles']:
                    required.add('container')
                if required - {checks[key].get('kind') for key in component['check_ids']}:
                    fail('Required dependency check-kind coverage missing: ' + component['id'])
            return value

        def inherited_dependencies(candidate, base):
            if base is None or not base['enabled']:
                return
            if candidate is None or not candidate['enabled']:
                fail('Active dependencies cannot be removed or disabled')
            current = {item['id']: item for item in candidate['components']}
            for previous in base['components']:
                now = current.get(previous['id'])
                if now is None:
                    fail('Inherited dependency component cannot be removed')
                if any(now[field] != previous[field] for field in ('kind', 'compatibility_document')):
                    fail('Inherited dependency kind or compatibility document cannot be changed')
                for field in (*dependency_file_fields, 'check_ids'):
                    if set(previous[field]) - set(now[field]):
                        fail('Inherited dependency artifacts or check bindings cannot be removed')

        try:
            root = folder_path(root)
            catalog = decode(technology_catalog_json.encode('utf-8'))
            keys(catalog, {'version', 'sources', 'rules', 'profiles'}, 'Trusted technology catalog')
            if not isinstance(catalog['version'], str):
                fail('Invalid trusted technology catalog version')
            for section in ('sources', 'rules', 'profiles'):
                if not isinstance(catalog[section], list) or not 1 <= len(catalog[section]) <= 256:
                    fail('Invalid trusted technology catalog section')
                identifiers = [identifier(item['id']) for item in catalog[section]]
                if len(identifiers) != len(set(identifiers)):
                    fail('Duplicate trusted technology identity')
            if source:
                package(root, catalog)
            if trusted_base is not None:
                trusted_base = folder_path(trusted_base)
            candidate = manifest(root, catalog, approved_root=trusted_base)
            dependency_candidate = dependencies(root, candidate, approved_root=trusted_base)
            if trusted_base is not None:
                # A legacy approved base without navigation has no extension package.
                base = manifest(trusted_base, catalog)
                inherited(candidate, base)
                if candidate is not None and candidate['enabled'] and (base is None or not base['enabled']):
                    if base is None:
                        fail('Navigation activation requires an already reviewed inactive seed')
                    manifest(trusted_base, catalog, complete=True)
                    if candidate != dict(base, enabled=True):
                        fail('Navigation activation must match the reviewed seed except enabled')
                dependency_base = dependencies(trusted_base, base)
                inherited_dependencies(dependency_candidate, dependency_base)
                if (dependency_candidate is not None and dependency_candidate['enabled']
                        and (dependency_base is None or not dependency_base['enabled'])):
                    if dependency_base is None:
                        fail('Dependency activation requires an already reviewed inactive seed')
                    dependencies(trusted_base, base, complete=True)
                    if dependency_candidate != dict(dependency_base, enabled=True):
                        fail('Dependency activation must match the reviewed seed except enabled')
            if request is None:
                if expected is not None:
                    fail('Handoff verification requires a request')
                return {'errors': [], 'context': None}
            if candidate is None or not candidate['enabled']:
                fail('Context resolution requires active navigation')
            keys(request, {'schema_version', 'task_packet', 'task_type', 'paths', 'components', 'revision'},
                 'Navigation request')
            if request['schema_version'] != '1' or request['task_type'] not in tasks:
                fail('Invalid navigation request version or task type')
            if not isinstance(request['revision'], str) or re.fullmatch(r'[0-9a-f]{40}', request['revision']) is None:
                fail('Request revision must be a full lowercase commit SHA')
            relative(request['task_packet'])
            packet = json_file(root, request['task_packet'])
            packet_keys = {'schema_version', 'id', 'title', 'objective', 'role', 'risk', 'repository',
                           'approved_sources', 'scope', 'acceptance', 'validation', 'execution_budget',
                           'stop_conditions', 'forbidden_actions', 'status'}
            keys(packet, packet_keys, 'Task Packet')
            if packet['schema_version'] != '1' or packet['role'] not in roles:
                fail('Invalid Task Packet version or role')
            for field in ('id', 'title', 'objective'):
                text(packet[field], 'Task Packet ' + field)
            if packet['risk'] not in {'low', 'medium', 'high', 'critical'}:
                fail('Invalid Task Packet risk')
            if packet['status'] not in {'planned', 'active', 'blocked', 'ready_for_review', 'completed'}:
                fail('Invalid Task Packet status')
            keys(packet['validation'], {'commands', 'manual_evidence'}, 'Task Packet validation')
            for entries in packet['validation'].values():
                sequence(entries, 'Task Packet validation entries')
            keys(packet['execution_budget'], {'max_iterations'}, 'Task Packet execution budget')
            budget = packet['execution_budget']['max_iterations']
            if type(budget) is not int or not 1 <= budget <= 10:
                fail('Invalid Task Packet execution budget')
            acceptance = packet['acceptance']
            if not isinstance(acceptance, list) or not 1 <= len(acceptance) <= 256:
                fail('Invalid Task Packet acceptance')
            acceptance_ids = set()
            for criterion in acceptance:
                keys(criterion, {'id', 'description', 'verification', 'status', 'evidence'},
                     'Task Packet acceptance criterion')
                text(criterion['id'], 'acceptance ID')
                text(criterion['description'], 'acceptance description')
                if criterion['id'] in acceptance_ids:
                    fail('Duplicate Task Packet acceptance ID')
                acceptance_ids.add(criterion['id'])
                if criterion['verification'] not in {'automatic', 'manual', 'hybrid'}:
                    fail('Invalid Task Packet verification')
                if criterion['status'] not in {'pending', 'pass', 'fail', 'blocked'}:
                    fail('Invalid Task Packet acceptance status')
                sequence(criterion['evidence'], 'acceptance evidence', nonempty=criterion['status'] == 'pass')
                if packet['status'] == 'completed' and criterion['status'] != 'pass':
                    fail('Completed Task Packet has unresolved acceptance')
            keys(packet['scope'], {'include', 'exclude'}, 'Task Packet scope')
            for field in ('include', 'exclude'):
                sequence(packet['scope'][field], 'task scope', nonempty=field == 'include')
                for pattern in packet['scope'][field]:
                    text(pattern, 'Task Packet scope pattern', 512)
                    if (pattern.startswith('/') or '\\' in pattern or ':' in pattern
                            or any(part in ('', '.', '..') for part in pattern.split('/'))):
                        fail('Invalid Task Packet scope pattern')
            for field in ('stop_conditions', 'forbidden_actions', 'approved_sources'):
                sequence(packet[field], field, nonempty=True)
            repository = packet['repository']
            keys(repository, {'base_branch', 'base_revision', 'head_revision'}, 'Task Packet repository')
            branch = text(repository['base_branch'], 'Task Packet base branch')
            if (branch == 'HEAD' or branch.startswith(('-', '/', '.')) or branch.endswith(('/', '.'))
                    or any(char.isspace() or char in '~^:?*[\\' for char in branch)
                    or any(part.startswith('.') or part.endswith('.lock') for part in branch.split('/'))
                    or any(value in branch for value in ('..', '//', '@{'))):
                fail('Invalid Task Packet base branch')
            for field in ('base_revision', 'head_revision'):
                revision = repository[field]
                required = packet['status'] in {'completed', 'ready_for_review'} or (
                    packet['status'] == 'active' and packet['role'] == 'reviewer')
                if revision is None and not required:
                    continue
                if not isinstance(revision, str) or re.fullmatch(r'[0-9a-f]{40}', revision) is None:
                    fail('Invalid or missing Task Packet revision')
            if repository['head_revision'] is not None and repository['head_revision'] != request['revision']:
                fail('Request revision differs from Task Packet reviewed head')
            if packet['role'] == 'reviewer' and repository['head_revision'] is None:
                fail('Reviewer context requires a frozen Task Packet head')
            sequence(request['paths'], 'request paths')
            sequence(request['components'], 'request component IDs')
            if not request['paths'] and not request['components']:
                fail('Request needs affected paths or named components')
            mapped = {item['id']: item for item in candidate['components']}
            if set(request['components']) - set(mapped):
                fail('Unknown requested component')
            selected = set(request['components'])
            includes, excludes = packet['scope']['include'], packet['scope']['exclude']
            for path in request['paths']:
                relative(path)
                located = locate(root, path, optional=True)
                directory_request = located is not None and located.is_dir()
                if (not any(scope_match(path, pattern) for pattern in includes)
                        or any(scope_match(path, pattern) or directory_request and pattern == path + '/**'
                               for pattern in excludes)):
                    fail('Requested path is outside Task Packet authorized scope')
                matches = {key for key, item in mapped.items()
                           if any(path == prefix or path.startswith(prefix + '/')
                                  or directory_request and prefix.startswith(path + '/') for prefix in item['paths'])}
                if not matches:
                    fail('Requested path has no component route')
                selected.update(matches)
            # A named component must intersect declared task scope. Exact paths are
            # still the authorization boundary; this does not authorize its subtree.
            for key in request['components']:
                if not any(any(scope_match(prefix, pattern) or pattern.startswith(prefix + '/')
                               or scope_match(prefix + '/_navigation_scope_probe_', pattern)
                               for pattern in includes)
                           and not any(scope_match(prefix, pattern) or pattern == prefix + '/**' for pattern in excludes)
                           for prefix in mapped[key]['paths']):
                    fail('Named component is outside Task Packet scope')
            quality = json_file(root, profile_path)
            workflow = effective_workflow(root, trusted_base)
            references = set(candidate['always']) | set(candidate['roles'][packet['role']]) | set(candidate['tasks'][request['task_type']])
            selected_profiles, technology_bindings = set(), {}
            for key in sorted(selected):
                item = mapped[key]
                references.update(item['documents'])
                selected_profiles.update(item['profiles'])
                technology_bindings[key] = item['checks']
            paths = {candidate['documents'][key] for key in references}
            paths.update({manifest_path, profile_path, workflows_path, request['task_packet'],
                          '.engineering-backbone/project.json'})
            prefix = 'standards' if source else '.engineering-backbone/standards'
            paths.update({prefix + '/sources.json', prefix + '/rules.json',
                          prefix + '/technologies/sources.json', prefix + '/technologies/rules.json'})
            paths.update(prefix + '/profiles/' + key + '.json' for key in quality['profiles'])
            paths.update(prefix + '/technologies/profiles/' + key + '.json' for key in selected_profiles)
            paths.update(path for path in quality['documents'].values() if path)
            paths.update({'policy/core.md', 'policy/core.json', 'policy/quality.md', 'docs/quality/README.md',
                          'docs/quality/technology-profiles.md', 'docs/agent-navigation.md'} if source else
                         {'.engineering-backbone/core.md', '.engineering-backbone/core.json',
                          '.engineering-backbone/quality-policy.md',
                          '.engineering-backbone/quality-guide.md', '.engineering-backbone/technology-guide.md',
                          '.engineering-backbone/navigation-guide.md'})
            for name in ('AGENTS.md', 'CONTRIBUTING.md', '.github/copilot-instructions.md'):
                if locate(root, name, optional=True) is not None:
                    paths.add(name)
            directories = {''}
            instruction_scopes = list(request['paths'])
            instruction_scopes.extend(prefix for key in request['components'] for prefix in mapped[key]['paths'])
            visited = 0
            for path in instruction_scopes:
                located = locate(root, path, optional=True)
                is_directory = located is not None and located.is_dir()
                parts = path.split('/') if is_directory else path.split('/')[:-1]
                directories.update('/'.join(parts[:index]) for index in range(1, len(parts) + 1))
                if is_directory:
                    # Directory/component requests include all descendant instruction
                    # scopes. File requests include their ancestors. Bound traversal
                    # and refuse symlink subtrees instead of silently missing rules.
                    def discovery_error(error):
                        raise error

                    for current, subdirectories, files in os.walk(located, followlinks=False, onerror=discovery_error):
                        visited += 1
                        if visited > 4096:
                            fail('Instruction discovery exceeds directory limit; narrow request paths')
                        for child in subdirectories:
                            if linked((Path(current) / child).lstat()):
                                fail('Symlink subtree during instruction discovery')
                        directories.add(Path(current).relative_to(root).as_posix())
            for directory in sorted(directories):
                prefix_path = directory + '/' if directory else ''
                for filename in ('AGENTS.md', 'AGENTS.override.md'):
                    name = prefix_path + filename
                    if locate(root, name, optional=True) is not None:
                        if filename == 'AGENTS.override.md':
                            fail('Unresolved instruction override requires explicit reconciliation')
                        paths.add(name)
            rule_map = {item['id']: item for item in catalog['rules']}
            profile_map = {item['id']: item for item in catalog['profiles']}
            selected_rules = {rule for name in selected_profiles for rule in profile_map[name]['rules']}
            selected_check_ids = {check for bindings in technology_bindings.values()
                                  for binding in bindings for check in binding['check_ids']}
            selected_check_ids.update(check for binding in quality['checks'] for check in binding['check_ids'])
            dependency_artifacts = set()
            if dependency_candidate is not None and dependency_candidate['enabled']:
                paths.update({dependencies_path, dependency_policy_path})
                for component in dependency_candidate['components']:
                    if component['id'] in selected:
                        paths.add(component['compatibility_document'])
                        dependency_artifacts.update(path for field in dependency_file_fields
                                                    for path in component[field])
                        selected_check_ids.update(component['check_ids'])
                paths.update(dependency_artifacts)
            if not isinstance(authority, dict):
                fail('Context resolution requires compiler-owned core authority')
            core_rules, core_profiles = authority['rules'], authority['profiles']
            core_profile_map = {item['id']: item for item in core_profiles}
            core_rule_map = {item['id']: item for item in core_rules}
            selected_core_rules = {rule for key in quality['profiles'] for rule in core_profile_map[key]['rules']}
            context = {
                'schema_version': '1', 'claim': 'structural-context-only',
                'revision': request['revision'], 'task_id': packet['id'], 'role': packet['role'],
                'request_sha256': digest(request), 'navigation_sha256': digest(candidate),
                'quality_profile_sha256': digest(quality), 'backbone_ref': quality['backbone_ref'],
                'quality_catalog_version': quality['catalog_version'],
                'technology_catalog_version': catalog['version'], 'technology_catalog_sha256': digest(catalog),
                'components': sorted(selected),
                'technology_profiles': [{'id': key, 'version': profile_map[key]['version']} for key in sorted(selected_profiles)],
                'technology_rules': [{'id': key, 'version': rule_map[key]['version']} for key in sorted(selected_rules)],
                'technology_check_bindings': technology_bindings,
                'quality_profiles': [{'id': key, 'version': core_profile_map[key]['version']} for key in sorted(quality['profiles'])],
                'quality_rules': [{'id': key, 'version': core_rule_map[key]['version']} for key in sorted(selected_core_rules)],
                'quality_check_bindings': quality['checks'],
                'checks': sorted((item for item in workflow['checks'] if item['id'] in selected_check_ids), key=lambda item: item['id']),
                'documents': [(dependency_artifact(root, reference) if reference in dependency_artifacts else
                               document(root, reference)) for reference in sorted(paths)],
                'runtime_loading': 'unverified',
            }
            context['context_sha256'] = digest(context)
            if expected is not None and expected != context:
                fail('Handoff context differs from recomputed snapshot')
            return {'errors': [], 'context': context}
        except (ValueError, OSError, UnicodeError, KeyError, TypeError, RecursionError) as exc:
            return {'errors': ['Navigation: ' + str(exc)], 'context': None}
    # END COMPILED NAVIGATION GUARD

    missing = object()
    config_path = '.engineering-backbone/quality-profile.json'
    json_limit = 262144
    document_limit = 1048576
    identifier = re.compile(r'[A-Za-z][A-Za-z0-9_.-]{0,63}\Z')
    document_keys = {'quality_plan', 'test_strategy', 'traceability', 'exceptions'}
    workflow_profiles = {'docs', 'python', 'typescript', 'go', 'dotnet'}
    workflow_kinds = {'docs', 'build', 'lint', 'test', 'typecheck', 'browser', 'api',
                      'migration', 'sast', 'dependency', 'container', 'iac',
                      'release-integrity', 'provenance', 'signature', 'sbom',
                      'deployment-smoke', 'rollback', 'monitoring'}
    workflow_phases = {'pr', 'maintenance', 'release', 'deploy'}
    csv_headers = ('rule_id', 'requirement_id', 'risk', 'architecture', 'tests',
                   'check_ids', 'evidence', 'status')

    def fail(message):
        raise ValueError(message)

    def text(value, label, *, empty=False, limit=4096):
        if (not isinstance(value, str) or len(value) > limit
                or (not empty and not value.strip())
                or any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value)):
            fail('Invalid ' + label)
        try:
            value.encode('utf-8')
        except UnicodeError:
            fail('Invalid UTF-8 ' + label)
        return value

    def object_keys(value, expected, label):
        if not isinstance(value, dict) or set(value) != expected:
            fail(label + ' has missing or unknown keys')

    def ids(value, allowed, label, *, maximum=256):
        if (not isinstance(value, list) or len(value) > maximum
                or any(not isinstance(item, str) or item not in allowed for item in value)
                or len(value) != len(set(value))):
            fail('Invalid or duplicate ' + label)
        return set(value)

    def id_value(value, label):
        if not isinstance(value, str) or identifier.fullmatch(value) is None:
            fail('Invalid ' + label)
        return value

    def safe_path(value, *, directory=False, absent=False):
        value = Path(value)
        if '..' in value.parts:
            fail('Parent traversal in filesystem path')
        value = Path(os.path.abspath(value))
        current = Path(value.anchor)
        for part in value.parts[1:]:
            current = current / part
            try:
                mode = current.lstat().st_mode
            except FileNotFoundError:
                if absent:
                    return value
                fail('Required filesystem path is absent')
            if stat.S_ISLNK(mode):
                fail('Symlink in filesystem path')
            if current != value and not stat.S_ISDIR(mode):
                fail('Non-directory filesystem ancestor')
        mode = value.stat().st_mode
        if directory and not stat.S_ISDIR(mode):
            fail('Input root is not a directory')
        if not directory and not stat.S_ISREG(mode):
            fail('Input is not a regular file')
        return value

    def relative_path(value, label, *, empty=False):
        value = text(value, label, empty=empty, limit=512)
        if empty and value == '':
            return value
        if (value.startswith('/') or '\\' in value or ':' in value
                or any(part in ('', '.', '..') for part in value.split('/'))):
            fail(label + ' must be a safe relative file path')
        return value

    def read_bytes(value, *, limit, absent=False):
        path = safe_path(value, absent=absent)
        if absent and not path.exists():
            return missing
        if path.stat().st_size > limit:
            fail('Input exceeds size limit')
        with path.open('rb') as handle:
            result = handle.read(limit + 1)
        if len(result) > limit:
            fail('Input exceeds size limit')
        return result

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('Duplicate JSON object key')
            result[key] = value
        return result

    def read_json(value, *, absent=False):
        data = read_bytes(value, limit=json_limit, absent=absent)
        if data is missing:
            return missing
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda value: fail('Invalid JSON number'))

    def read_document(folder, value, *, required=False):
        if not value:
            if required:
                fail('Required quality document path is empty')
            return None
        data = read_bytes(folder / value, limit=document_limit)
        document = data.decode('utf-8')
        if '\x00' in document:
            fail('Quality document contains a NUL character')
        if required and not document.strip():
            fail('Required quality document is empty')
        return document

    def read_evidence(folder, value):
        # Evidence may be a text report, screenshot or PDF. Read bounded regular
        # bytes without interpreting the contents or authenticating the claim.
        if not read_bytes(folder / value, limit=document_limit):
            fail('Required evidence file is empty')

    def catalog():
        value = json.loads(catalog_json, object_pairs_hook=pairs,
                           parse_constant=lambda value: fail('Invalid trusted JSON number'))
        object_keys(value, {'version', 'sources', 'rules', 'profiles'}, 'Trusted catalog')
        if value['version'] != '1.0.0':
            fail('Unsupported trusted catalog version')
        for key in ('sources', 'rules', 'profiles'):
            if not isinstance(value[key], list) or not 1 <= len(value[key]) <= 256:
                fail('Invalid trusted catalog ' + key)
        sources = {}
        for entry in value['sources']:
            object_keys(entry, {'id', 'title', 'edition', 'url', 'status', 'access',
                               'adoption', 'verified_sections'}, 'Catalog source')
            key = id_value(entry['id'], 'source ID')
            if key in sources:
                fail('Duplicate source ID')
            for name in ('title', 'edition', 'url', 'status', 'access', 'adoption'):
                text(entry[name], 'source ' + name)
            if not isinstance(entry['verified_sections'], list) or len(entry['verified_sections']) > 100:
                fail('Invalid source verified sections')
            for section in entry['verified_sections']:
                text(section, 'source verified section')
            sources[key] = entry
        rules = {}
        for entry in value['rules']:
            object_keys(entry, {'id', 'version', 'statement', 'source_ids',
                               'source_alignment', 'responsibilities', 'phases',
                               'verification', 'artifacts', 'check_kind_groups',
                               'waivable'}, 'Catalog rule')
            key = id_value(entry['id'], 'rule ID')
            if key in rules or entry['version'] != '1':
                fail('Duplicate rule ID or unsupported rule version')
            text(entry['statement'], 'rule statement')
            text(entry['source_alignment'], 'rule source alignment')
            if not ids(entry['source_ids'], sources, 'rule sources'):
                fail('Rule has no source')
            if not ids(entry['responsibilities'], {'planner', 'implementer', 'reviewer',
                       'quality_checker', 'triage'}, 'rule responsibilities', maximum=5):
                fail('Rule has no responsibility')
            if not ids(entry['phases'], {'planning', 'design', 'implementation',
                       'verification', 'review', 'publication', 'release', 'operation'},
                       'rule phases', maximum=8):
                fail('Rule has no phase')
            if (not isinstance(entry['verification'], str)
                    or entry['verification'] not in {'automatic', 'manual', 'hybrid'}):
                fail('Invalid rule verification')
            ids(entry['artifacts'], document_keys - {'exceptions'}, 'rule artifacts', maximum=3)
            if type(entry['waivable']) is not bool:
                fail('Invalid rule waiver flag')
            groups = entry['check_kind_groups']
            if not isinstance(groups, list) or len(groups) > len(workflow_kinds):
                fail('Invalid rule check-kind groups')
            for group in groups:
                if not ids(group, workflow_kinds, 'rule check kinds', maximum=len(workflow_kinds)):
                    fail('Empty rule check-kind group')
            rules[key] = entry
        profiles = {}
        for entry in value['profiles']:
            object_keys(entry, {'id', 'version', 'description', 'enabled', 'rules',
                               'workflow_profiles'}, 'Catalog profile')
            key = id_value(entry['id'], 'catalog profile ID')
            if key in profiles or entry['version'] != '1' or type(entry['enabled']) is not bool:
                fail('Duplicate profile ID or invalid catalog profile version/flag')
            text(entry['description'], 'catalog profile description')
            if not ids(entry['rules'], rules, 'catalog profile rules'):
                fail('Catalog profile has no rules')
            ids(entry['workflow_profiles'], workflow_profiles, 'catalog workflow profiles', maximum=5)
            profiles[key] = entry
        if 'baseline' not in profiles or not profiles['baseline']['enabled']:
            fail('Trusted catalog lacks the enabled baseline profile')
        if any(rules[key]['waivable'] for key in profiles['baseline']['rules']):
            fail('Baseline rules cannot be waived')
        return value, rules, profiles

    def package(folder, authority, *, central=False):
        prefix = folder / ('standards' if central else '.engineering-backbone/standards')
        for key in ('sources', 'rules'):
            expected = {'schema_version': '1', 'version': authority['version'],
                        key: authority[key]}
            if read_json(prefix / (key + '.json')) != expected:
                fail('Managed ' + key + ' catalog differs from trusted authority')
        profile_dir = safe_path(prefix / 'profiles', directory=True)
        expected_names = {entry['id'] + '.json' for entry in authority['profiles']}
        actual_names = set()
        for path in profile_dir.iterdir():
            if len(actual_names) >= 256:
                fail('Managed catalog exceeds profile-file limit')
            actual_names.add(path.name)
        if actual_names != expected_names:
            fail('Managed catalog profile files differ from trusted authority')
        for entry in authority['profiles']:
            if read_json(profile_dir / (entry['id'] + '.json')) != entry:
                fail('Managed profile catalog differs from trusted authority')

    def workflow(folder, *, needed=False):
        value = read_json(folder / '.engineering-backbone/workflows.json', absent=True)
        if value is missing:
            if needed:
                fail('Quality bindings require an active complete workflow kit')
            return None
        object_keys(value, {'schema_version', 'enabled', 'profiles', 'capabilities',
                           'runtimes', 'checks'}, 'Workflow configuration')
        if value['schema_version'] != '1' or type(value['enabled']) is not bool:
            fail('Invalid workflow configuration version/flag')
        selected = ids(value['profiles'], workflow_profiles, 'workflow profiles', maximum=5)
        capabilities = ids(value['capabilities'], {'dependencies', 'web', 'api', 'database',
                          'container', 'iac', 'release', 'deploy'}, 'workflow capabilities', maximum=8)
        runtime_for = {'python': 'python', 'typescript': 'node', 'go': 'go', 'dotnet': 'dotnet'}
        runtimes = value['runtimes']
        if not isinstance(runtimes, dict) or set(runtimes) - set(runtime_for.values()):
            fail('Invalid workflow runtimes')
        for name, version in runtimes.items():
            text(version, 'workflow runtime version', limit=32)
            pattern = r'[0-9]{1,3}(?:\.[0-9]{1,3}){0,2}' + (r'(?:\.x)?' if name == 'dotnet' else '')
            if re.fullmatch(pattern, version) is None:
                fail('Invalid workflow runtime version')
        checks = value['checks']
        if not isinstance(checks, list) or len(checks) > 100:
            fail('Invalid workflow checks')
        check_map, coverage = {}, set()
        release_kinds = {'release-integrity', 'provenance', 'signature', 'sbom'}
        deploy_kinds = {'deployment-smoke', 'rollback', 'monitoring'}
        for check in checks:
            object_keys(check, {'id', 'kind', 'argv', 'cwd', 'timeout_seconds', 'phases'}, 'Workflow check')
            key = id_value(check['id'], 'workflow check ID')
            if key in check_map:
                fail('Duplicate workflow check ID')
            if not isinstance(check['kind'], str) or check['kind'] not in workflow_kinds:
                fail('Invalid workflow check kind')
            if not isinstance(check['argv'], list) or not 1 <= len(check['argv']) <= 64:
                fail('Invalid workflow command arguments')
            for argument in check['argv']:
                text(argument, 'workflow command argument', empty=True)
            if not check['argv'][0].strip():
                fail('Workflow command executable is empty')
            if check['cwd'] != '.':
                relative_path(check['cwd'], 'Workflow working directory')
            if type(check['timeout_seconds']) is not int or not 1 <= check['timeout_seconds'] <= 1800:
                fail('Invalid workflow check timeout')
            phases = ids(check['phases'], workflow_phases, 'workflow check phases', maximum=4)
            allowed = ({'release'} if check['kind'] in release_kinds else
                       {'deploy'} if check['kind'] in deploy_kinds else
                       {'pr', 'maintenance'} if check['kind'] in {'dependency', 'container'} else {'pr'})
            if not phases or phases - allowed:
                fail('Workflow kind does not support selected phases')
            coverage.update((check['kind'], phase) for phase in phases)
            check_map[key] = check
        if value['enabled'] or needed:
            if not value['enabled'] or not selected:
                fail('Quality bindings require an active complete workflow kit')
            if any(runtime_for[key] not in runtimes for key in selected if key in runtime_for):
                fail('Required workflow runtime is missing')
            required = set()
            for key in selected:
                required.update((kind, 'pr') for kind in
                                (['docs'] if key == 'docs' else ['build', 'lint', 'test', 'sast']))
                if key == 'typescript':
                    required.add(('typecheck', 'pr'))
            for capability, kind in [('web', 'browser'), ('api', 'api'),
                                      ('database', 'migration'), ('iac', 'iac')]:
                if capability in capabilities:
                    required.add((kind, 'pr'))
            for capability, kind in (('dependencies', 'dependency'), ('container', 'container')):
                if capability in capabilities:
                    required.update((kind, phase) for phase in ('pr', 'maintenance'))
            if 'release' in capabilities:
                required.update((kind, 'release') for kind in ('release-integrity', 'provenance', 'signature'))
                if capabilities & {'dependencies', 'container'}:
                    required.add(('sbom', 'release'))
            if 'deploy' in capabilities:
                required.update((kind, 'deploy') for kind in deploy_kinds)
            if required - coverage:
                fail('Required workflow checks are missing')
        return value

    def profile(folder, rules, profiles, authority, *, approved=False):
        value = read_json(folder / config_path, absent=True)
        if value is missing:
            return None
        object_keys(value, {'schema_version', 'enabled', 'catalog_version', 'backbone_ref',
                           'profiles', 'documents', 'checks', 'exceptions'}, 'Quality profile')
        if value['schema_version'] != '1' or type(value['enabled']) is not bool:
            fail('Invalid quality profile version/flag')
        if value['catalog_version'] != authority['version']:
            fail('Quality catalog version is not trusted')
        reference = text(value['backbone_ref'], 'backbone reference', empty=True, limit=40)
        if reference and re.fullmatch(r'[0-9a-fA-F]{40}', reference) is None:
            fail('Backbone reference must be a full commit SHA')
        selected = ids(value['profiles'], profiles, 'quality profiles')
        if any(not profiles[key]['enabled'] for key in selected):
            fail('Reference-only catalog profile cannot be selected')
        object_keys(value['documents'], document_keys, 'Quality document mapping')
        for key, path in value['documents'].items():
            relative_path(path, 'Quality document ' + key, empty=True)
        applicable = {key for profile_id in selected for key in profiles[profile_id]['rules']}
        bindings = value['checks']
        if not isinstance(bindings, list) or len(bindings) > 256:
            fail('Invalid quality check bindings')
        bound_rules = set()
        for binding in bindings:
            object_keys(binding, {'rule_id', 'check_ids'}, 'Quality check binding')
            rule_id = id_value(binding['rule_id'], 'bound rule ID')
            if rule_id not in applicable or rule_id in bound_rules:
                fail('Unknown, unselected or duplicate bound rule')
            check_ids = binding['check_ids']
            if (not isinstance(check_ids, list) or not 1 <= len(check_ids) <= 100
                    or any(not isinstance(key, str) or identifier.fullmatch(key) is None for key in check_ids)
                    or len(check_ids) != len(set(check_ids))):
                fail('Invalid or duplicate bound check IDs')
            bound_rules.add(rule_id)
        exceptions = value['exceptions']
        if not isinstance(exceptions, list) or len(exceptions) > 256:
            fail('Invalid quality exceptions')
        exception_ids = set()
        for exception in exceptions:
            object_keys(exception, {'rule_id', 'scope', 'reason', 'owner', 'approved_by',
                                   'expires_on', 'compensating_check_ids', 'evidence_path'}, 'Quality exception')
            rule_id = id_value(exception['rule_id'], 'exception rule ID')
            if rule_id not in applicable or rule_id in exception_ids or not rules[rule_id]['waivable']:
                fail('Unknown, unselected, duplicate or disallowed exception rule')
            exception_ids.add(rule_id)
            for key in ('scope', 'reason', 'owner', 'approved_by'):
                text(exception[key], 'exception ' + key)
            expiry = text(exception['expires_on'], 'exception expiry', limit=10)
            if (re.fullmatch(r'\d{4}-\d{2}-\d{2}', expiry) is None
                    or not approved and date.fromisoformat(expiry) < date.today()):
                fail('Invalid or expired quality exception')
            date.fromisoformat(expiry)
            compensating = exception['compensating_check_ids']
            if (not isinstance(compensating, list) or not 1 <= len(compensating) <= 100
                    or any(not isinstance(key, str) or identifier.fullmatch(key) is None for key in compensating)
                    or len(compensating) != len(set(compensating))):
                fail('Invalid compensating check IDs')
            evidence = relative_path(exception['evidence_path'], 'Exception evidence path')
            read_evidence(folder, evidence)
        package(folder, authority, central=source)
        return value

    def delimited(value, label):
        if not value:
            return []
        values = value.split(';')
        if any(not entry or entry != entry.strip() for entry in values) or len(values) != len(set(values)):
            fail('Invalid or duplicate CSV ' + label)
        return values

    def validate_content(folder, value, rules, profiles, *, complete=False, approved_workflow=None):
        if value is None:
            return
        complete = complete or value['enabled']
        selected = set(value['profiles'])
        applicable = {key for profile_id in selected for key in profiles[profile_id]['rules']}
        if complete and ('baseline' not in selected or not value['backbone_ref']):
            fail('Complete quality profile requires baseline and a full backbone reference')
        needed_workflow = complete or bool(value['checks']) or bool(value['exceptions'])
        current_workflow = workflow(folder, needed=needed_workflow)
        effective_workflow = current_workflow
        if current_workflow is not None and approved_workflow is not None:
            effective_workflow = dict(current_workflow)
            approved_checks = {check['id']: check for check in approved_workflow['checks']}
            effective_workflow['checks'] = [approved_checks.get(check['id'], check)
                                            for check in current_workflow['checks']]
            # Existing workflow profile selections cannot disappear here either.
            if set(approved_workflow['profiles']) - set(current_workflow['profiles']):
                fail('Approved workflow profiles cannot be removed')
        check_map = ({check['id']: check for check in effective_workflow['checks']}
                     if effective_workflow is not None else {})
        pr_checks = {key: check for key, check in check_map.items() if 'pr' in check['phases']}
        for profile_id in selected:
            required = set(profiles[profile_id]['workflow_profiles'])
            if complete and (effective_workflow is None or required - set(effective_workflow['profiles'])):
                fail('Required quality language workflow profile is missing')
        binding_map = {entry['rule_id']: set(entry['check_ids']) for entry in value['checks']}
        exceptions = {entry['rule_id']: entry for entry in value['exceptions']}
        for rule_id, bound in binding_map.items():
            if bound - set(pr_checks):
                fail('Quality binding references an unknown or non-PR workflow check')
        for exception in value['exceptions']:
            if set(exception['compensating_check_ids']) - set(pr_checks):
                fail('Exception references an unknown or non-PR workflow check')
        for rule_id in applicable:
            rule = rules[rule_id]
            if complete:
                for artifact in rule['artifacts']:
                    if not value['documents'][artifact]:
                        fail('Required rule artifact path is missing')
                if rule_id not in exceptions:
                    covered = {pr_checks[key]['kind'] for key in binding_map.get(rule_id, set())}
                    if any(not covered.intersection(group) for group in rule['check_kind_groups']):
                        fail('Required rule PR check-kind coverage is missing: ' + rule_id)
        documents = {}
        for key, path in value['documents'].items():
            required = complete and key != 'exceptions' or key == 'exceptions' and bool(exceptions)
            documents[key] = read_document(folder, path, required=required)
        trace = documents['traceability']
        if trace is None:
            return
        reader = csv.DictReader(io.StringIO(trace, newline=''), strict=True)
        if tuple(reader.fieldnames or ()) != csv_headers:
            fail('Traceability CSV has missing, reordered or unknown columns')
        mapped, trace_checks = set(), {}
        for index, row in enumerate(reader):
            if index >= 4096 or set(row) != set(csv_headers) or any(value is None for value in row.values()):
                fail('Traceability CSV is malformed or exceeds row limit')
            for key, cell in row.items():
                text(cell, 'CSV ' + key, empty=True, limit=65536)
            rule_id = row['rule_id']
            if rule_id not in applicable:
                fail('Traceability CSV references an unknown or unselected rule')
            if row['status'] not in {'pending', 'planned', 'verified', 'gap'}:
                fail('Invalid traceability declaration status')
            if complete and any(not row[key].strip() for key in ('requirement_id', 'risk', 'architecture', 'tests')):
                fail('Complete traceability row lacks requirement/risk/design/test mapping')
            row_checks = set(delimited(row['check_ids'], 'check IDs'))
            allowed = binding_map.get(rule_id, set()) | set(exceptions.get(rule_id, {}).get('compensating_check_ids', []))
            if row_checks - set(pr_checks) or row_checks - allowed:
                fail('Traceability check IDs are unknown, non-PR or not bound to their rule')
            evidence = delimited(row['evidence'], 'evidence paths')
            if row['status'] == 'verified' and not evidence:
                fail('Verified declaration lacks a regular evidence file')
            for reference in evidence:
                relative_path(reference, 'Traceability evidence path')
                safe_path(folder / reference, absent=row['status'] != 'verified')
                if row['status'] == 'verified':
                    read_evidence(folder, reference)
            mapped.add(rule_id)
            trace_checks.setdefault(rule_id, set()).update(row_checks)
        if complete:
            if applicable - mapped:
                fail('Traceability CSV does not map every selected rule')
            for rule_id, bound in binding_map.items():
                if bound - trace_checks.get(rule_id, set()):
                    fail('Traceability CSV omits declared rule check bindings')

    try:
        root = safe_path(root, directory=True)
        authority, rules, profiles = catalog()
        if source:
            package(root, authority, central=True)
        candidate = profile(root, rules, profiles, authority)
        base = None
        base_workflow = None
        if trusted_base is not None:
            trusted_base = safe_path(trusted_base, directory=True)
            base = profile(trusted_base, rules, profiles, authority, approved=True)
            validate_content(trusted_base, base, rules, profiles)
            if base is not None and base['enabled']:
                base_workflow = workflow(trusted_base, needed=True)
                if candidate is None or not candidate['enabled']:
                    fail('Active quality profile cannot be removed or disabled')
                if set(base['profiles']) - set(candidate['profiles']):
                    fail('Approved quality profiles cannot be removed')
                candidate_bindings = {item['rule_id']: set(item['check_ids']) for item in candidate['checks']}
                for binding in base['checks']:
                    if set(binding['check_ids']) - candidate_bindings.get(binding['rule_id'], set()):
                        fail('Approved rule check bindings cannot be removed')
                old_exceptions = {item['rule_id']: item for item in base['exceptions']}
                for exception in candidate['exceptions']:
                    if old_exceptions.get(exception['rule_id']) != exception:
                        fail('Active profile cannot introduce or alter an approved exception')
            if candidate is not None and candidate['enabled'] and (base is None or not base['enabled']):
                if base is None:
                    fail('Quality activation requires an already reviewed inactive seed')
                validate_content(trusted_base, base, rules, profiles, complete=True)
                if candidate != dict(base, enabled=True):
                    fail('Quality activation must match the reviewed seed except enabled')
        validate_content(root, candidate, rules, profiles, approved_workflow=base_workflow)
        navigation = navigation_context(root, trusted_base, source=source,
                                        request=navigation_request,
                                        expected=navigation_expected,
                                        authority=authority)
        if navigation['errors']:
            fail('Navigation: ' + '; '.join(navigation['errors']))
        if navigation_output is not None and navigation['context'] is not None:
            navigation_output.update(navigation['context'])
        return []
    except (ValueError, OSError, UnicodeError, csv.Error, RecursionError) as exc:
        return ['Quality framework: ' + str(exc)]
# END COMPILED QUALITY GUARD


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
            for name in ('engineering-backbone.yml', 'backbone-pr-checks.yml',
                         'backbone-maintenance.yml'):
                workflow = self.root / '.github/workflows' / name
                if workflow.is_file() and not workflow.is_symlink():
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
            if path.suffix not in {".yml", ".yaml"} or (not source and path.name not in {
                    'engineering-backbone.yml', 'backbone-pr-checks.yml', 'backbone-maintenance.yml'}):
                continue
            relative = self.label(path)
            if any(component.is_symlink() for component in (directory.parent, directory, path)):
                self.error(f'{relative}: managed workflow must have no symlink ancestors')
                continue
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
        # This compiled guard is part of the existing attested validator bytes.
        # Only its validation mode is used here; no project command executes.
        import contextlib
        import io
        kit_output = io.StringIO()
        kit_args = ['validate', '--root', str(self.root)]
        if self.trusted_base is not None:
            kit_args += ['--trusted-base', str(self.trusted_base)]
        with contextlib.redirect_stdout(kit_output), contextlib.redirect_stderr(kit_output):
            kit_status = workflow_kit_main(kit_args)
        if kit_status != 0:
            self.error('workflow kit: ' + kit_output.getvalue().strip())
        self.errors.extend(quality_errors(self.root, self.trusted_base, source=source))
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
