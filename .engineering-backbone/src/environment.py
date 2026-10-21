"""Validate declared environment inputs without displaying their values.

This checker does not configure an application's loader or grant credential access.
An env file is read only when explicitly selected; its values are literal text.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import sys


CONTEXTS = ("local", "test", "ci", "production")
TYPES = {"string", "integer", "boolean", "enum"}
NAME = re.compile(r"[A-Z][A-Z0-9_]{0,127}\Z")
INTEGER = re.compile(r"[+-]?[0-9]+\Z")
MAX_BYTES = 1024 * 1024
MAX_VARIABLES = 256
MAX_VALUE_LENGTH = 65536


class EnvironmentError(ValueError):
    """A deliberately redacted diagnostic safe for command output."""


def _read(path: Path) -> str:
    """Bound reads and keep OS, parser and decoding details out of diagnostics."""
    try:
        if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
            raise EnvironmentError("input must be a regular file")
        with path.open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise EnvironmentError("input exceeds the size limit")
        return raw.decode("utf-8")
    except (OSError, UnicodeError):
        raise EnvironmentError("input cannot be read as UTF-8") from None


def _unique_object(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise EnvironmentError("contract contains duplicate object keys")
        data[key] = value
    return data


def load_contract(path: Path) -> list[dict]:
    """Read a closed metadata contract; no value/default/example field is allowed."""
    try:
        data = json.loads(_read(path), object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, RecursionError):
        raise EnvironmentError("contract is not valid bounded JSON") from None
    if not isinstance(data, dict) or set(data) != {"version", "variables"}:
        raise EnvironmentError("contract must contain only version and variables")
    if type(data["version"]) is not int or data["version"] != 1:
        raise EnvironmentError("contract version must be 1")
    entries = data["variables"]
    if not isinstance(entries, list) or len(entries) > MAX_VARIABLES:
        raise EnvironmentError("contract variables must be a bounded list")
    names = set()
    fields = {"name", "component", "purpose", "type", "secret", "required_in"}
    for index, entry in enumerate(entries, start=1):
        label = f"contract entry {index}"
        if not isinstance(entry, dict) or not fields <= set(entry) <= fields | {"choices"}:
            raise EnvironmentError(label + " has unsupported or missing fields")
        name = entry["name"]
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise EnvironmentError(label + " has an invalid variable name")
        if name in names:
            raise EnvironmentError(label + " duplicates a variable name")
        names.add(name)
        for field in ("component", "purpose"):
            text = entry[field]
            if not isinstance(text, str) or not text.strip() or len(text) > 1024:
                raise EnvironmentError(label + " has invalid descriptive metadata")
        kind = entry["type"]
        if not isinstance(kind, str) or kind not in TYPES:
            raise EnvironmentError(label + " has an unsupported type")
        if type(entry["secret"]) is not bool:
            raise EnvironmentError(label + " needs a boolean secret classification")
        contexts = entry["required_in"]
        if (not isinstance(contexts, list) or len(contexts) > len(CONTEXTS)
                or any(not isinstance(item, str) or item not in CONTEXTS for item in contexts)
                or len(set(contexts)) != len(contexts)):
            raise EnvironmentError(label + " has invalid required contexts")
        if kind == "enum":
            choices = entry.get("choices")
            if (entry["secret"] or not isinstance(choices, list) or not 1 <= len(choices) <= 64
                    or any(not isinstance(item, str) or not item or len(item) > 1024
                           for item in choices)
                    or len(set(choices)) != len(choices)):
                raise EnvironmentError(label + " needs distinct public enum choices")
        elif "choices" in entry:
            raise EnvironmentError(label + " allows choices only for a public enum")
    return entries


def load_env_file(path: Path, names: set[str]) -> dict[str, str]:
    """Parse literal KEY=VALUE lines, never shell code or dotenv interpolation."""
    values = {}
    for line_number, line in enumerate(_read(path).splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "=" not in line or "\0" in line:
            raise EnvironmentError(f"env file line {line_number}: expected literal KEY=VALUE")
        key, value = line.split("=", 1)
        if not NAME.fullmatch(key) or key not in names:
            raise EnvironmentError(f"env file line {line_number}: undeclared or invalid key")
        if key in values:
            raise EnvironmentError(f"env file line {line_number}: duplicate key")
        if len(value) > MAX_VALUE_LENGTH:
            raise EnvironmentError(f"env file line {line_number}: value exceeds the size limit")
        values[key] = value
    return values


def validate_values(entries: list[dict], values: dict[str, str], context: str) -> list[str]:
    """Return names and reasons only; supplied values are never formatted."""
    if context not in CONTEXTS:
        raise EnvironmentError("unsupported environment context")
    errors = []
    for entry in entries:
        name = entry["name"]
        value = values.get(name)
        if value is None or value == "":
            if context in entry["required_in"]:
                errors.append(name + ": required value is missing")
            continue
        if not isinstance(value, str) or len(value) > MAX_VALUE_LENGTH or "\0" in value:
            errors.append(name + ": value is invalid or exceeds the size limit")
            continue
        kind = entry["type"]
        if kind == "integer" and not INTEGER.fullmatch(value):
            errors.append(name + ": expected an integer")
        elif kind == "boolean" and value not in {"true", "false"}:
            errors.append(name + ": expected true or false")
        elif kind == "enum" and value not in entry["choices"]:
            errors.append(name + ": expected a declared public choice")
    return errors


def _input_path(root: Path, supplied: Path) -> Path:
    path = Path(os.path.abspath(supplied if supplied.is_absolute() else root / supplied))
    if not path.is_relative_to(root):
        raise EnvironmentError("input path must stay inside the selected root")
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise EnvironmentError("input path must not contain symbolic links")
    return path


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        # Unknown arguments may themselves contain secrets; do not quote them.
        self.exit(2, "ERROR: invalid arguments; use --help\n")


def main(argv=None) -> int:
    parser = _Parser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--contract", type=Path, default=Path("config/environment.json"))
    parser.add_argument("--environment", choices=CONTEXTS, default="local")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args(argv)
    try:
        root = Path(os.path.abspath(args.root))
        if not root.is_dir() or any(part.is_symlink() for part in (root, *root.parents)):
            raise EnvironmentError("root must be an existing directory without symbolic links")
        entries = load_contract(_input_path(root, args.contract))
        names = {entry["name"] for entry in entries}
        values = (load_env_file(_input_path(root, args.env_file), names)
                  if args.env_file is not None else {})
        values.update({name: os.environ[name] for name in names if name in os.environ})
        errors = validate_values(entries, values, args.environment)
        if errors:
            for error in errors:
                print("ERROR: " + error, file=sys.stderr)
            return 1
        print(f"PASS: {len(entries)} declared variables checked for {args.environment}.")
        print("This does not establish application readiness, credential permissions or loader behavior.")
        return 0
    except EnvironmentError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("ERROR: environment inputs could not be validated", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
