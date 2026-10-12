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

    def policy(self):
        path = self.policy_path(self.root)
        policy = self.load(path)
        if policy is None:
            return
        self.validate_data("core-policy", policy, self.label(path))
        invariants = policy.get("invariants", {}) if isinstance(policy, dict) else {}
        for key, value in POLICY_FLOOR.items():
            if not isinstance(invariants, dict) or invariants.get(key) is not value:
                self.error(f"{self.label(path)}: mandatory policy invariant {key} must be {value}")
        if self.trusted_base is not None:
            try:
                base_path = self.policy_path(self.trusted_base)
                base = read_json(base_path)
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
        if agents.get("codex") is True:
            self.required_file("AGENTS.md")
            for role in NATIVE_ROLES:
                relative = f".codex/agents/backbone-{role}.toml"
                if not self.required_file(relative):
                    continue
                try:
                    data = tomllib.loads((self.root / relative).read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    self.error(f"{relative}: invalid TOML: {exc}")
                    continue
                allowed = {"name", "description", "developer_instructions", "sandbox_mode"}
                if set(data) - allowed:
                    self.error(f"{relative}: unapproved keys (model, credentials and permission overrides are prohibited): {sorted(set(data)-allowed)}")
                for key in ("name", "description", "developer_instructions"):
                    if not isinstance(data.get(key), str) or not data[key].strip():
                        self.error(f"{relative}: required nonempty string {key}")
                if data.get("name") != f"backbone_{role}":
                    self.error(f"{relative}: incorrect native agent name")
                mode = "workspace-write" if role == "implementer" else "read-only"
                allowed_modes = {mode}
                if not self.source and role == "implementer":
                    allowed_modes.add("read-only")
                if not isinstance(data.get("sandbox_mode"), str) or data["sandbox_mode"] not in allowed_modes:
                    self.error(f"{relative}: sandbox_mode must be {mode}" + (" or the stricter read-only" if len(allowed_modes) > 1 else ""))
        if agents.get("copilot") is True:
            self.required_file(".github/copilot-instructions.md")
            for role in NATIVE_ROLES:
                relative = f".github/agents/backbone-{role}.agent.md"
                if not self.required_file(relative):
                    continue
                try:
                    content = (self.root / relative).read_text(encoding="utf-8")
                    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
                    if not match:
                        raise ValueError("missing YAML frontmatter")
                    data = yaml.safe_load(match.group(1))
                    if not isinstance(data, dict):
                        raise ValueError("frontmatter must be a mapping")
                    if not content[match.end():].strip():
                        raise ValueError("missing agent instructions")
                except (OSError, ValueError, yaml.YAMLError) as exc:
                    self.error(f"{relative}: {exc}")
                    continue
                if set(data) - {"name", "description", "tools"}:
                    self.error(f"{relative}: unapproved frontmatter keys: {sorted(set(data)-{'name','description','tools'})}")
                for key in ("name", "description"):
                    if not isinstance(data.get(key), str) or not data[key].strip():
                        self.error(f"{relative}: required nonempty string {key}")
                if data.get("name") != f"backbone-{role}":
                    self.error(f"{relative}: incorrect native agent name")
                tools = data.get("tools")
                allowed = {"read", "search", "edit", "execute"} if role == "implementer" else {"read", "search"}
                valid = isinstance(tools, list) and bool(tools) and all(isinstance(t, str) for t in tools)
                if valid:
                    valid = len(tools) == len(set(tools)) and (set(tools) == allowed if self.source else set(tools).issubset(allowed))
                if not valid:
                    requirement = "exactly" if self.source else "a nonempty unique subset of"
                    self.error(f"{relative}: tools must be {requirement} {sorted(allowed)}; planner/reviewer cannot edit, execute, or delegate")

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
            for adapter, extension, folder in (("codex", "toml", ".codex/agents"), ("copilot", "agent.md", ".github/agents")):
                if self.agents.get(adapter) is True:
                    paths.extend(self.root / folder / f"backbone-{role}.{extension}" for role in NATIVE_ROLES if (self.root / folder / f"backbone-{role}.{extension}").is_file())
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
