"""Actual environment CLI behavior and credential-redaction failure cases."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".engineering-backbone/src/environment.py"
SPEC = importlib.util.spec_from_file_location("backbone_environment", SCRIPT)
environment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(environment)
SENTINEL = "FAKE_CREDENTIAL_DO_NOT_EMIT_61c2f8"


def variable(name="BB_TEST_TOKEN", kind="string", *, secret=True, required=None, **extra):
    return dict(name=name, component="test-component", purpose="test-only input",
                type=kind, secret=secret,
                required_in=["local"] if required is None else required, **extra)


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="backbone-env-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "config").mkdir()

    def contract(self, entries):
        (self.root / "config/environment.json").write_text(
            json.dumps(dict(version=1, variables=entries)), encoding="utf-8")

    def run_cli(self, *args, values=None):
        supplied = {key: value for key, value in os.environ.items()
                    if not key.startswith("BB_TEST_")}
        supplied.update(values or {})
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args],
                              env=supplied, capture_output=True, text=True, timeout=10)

    def assert_redacted(self, result, *secrets):
        output = result.stdout + result.stderr
        for secret in (SENTINEL, *secrets):
            self.assertNotIn(secret, output)
        self.assertNotIn("Traceback", output)
        return output

    def test_empty_contract_does_not_load_env_file_or_claim_application_readiness(self):
        self.contract([])
        (self.root / ".env").write_text(SENTINEL, encoding="utf-8")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("0 declared variables", result.stdout)
        self.assertIn("does not establish application readiness", result.stdout)
        self.assert_redacted(result)

    def test_process_values_validate_supported_types_and_contexts(self):
        self.contract([
            variable(), variable("BB_TEST_PORT", "integer", secret=False),
            variable("BB_TEST_FEATURE", "boolean", secret=False),
            variable("BB_TEST_MODE", "enum", secret=False, choices=["small", "large"]),
            variable("BB_TEST_PRODUCTION", required=["production"]),
        ])
        values = dict(BB_TEST_TOKEN=SENTINEL, BB_TEST_PORT="+42", BB_TEST_FEATURE="false",
                      BB_TEST_MODE="large")
        result = self.run_cli(values=values)
        self.assertEqual(result.returncode, 0)
        self.assertIn("5 declared variables", result.stdout)
        self.assert_redacted(result)
        result = self.run_cli("--environment", "production", values=values)
        self.assertEqual(result.returncode, 1)
        self.assertIn("BB_TEST_PRODUCTION: required value is missing", result.stderr)
        self.assert_redacted(result)

    def test_missing_required_and_invalid_values_fail_without_disclosure(self):
        self.contract([
            variable(), variable("BB_TEST_PORT", "integer", secret=False),
            variable("BB_TEST_FEATURE", "boolean", secret=False),
            variable("BB_TEST_MODE", "enum", secret=False, choices=["small"]),
        ])
        result = self.run_cli(values=dict(BB_TEST_PORT=SENTINEL, BB_TEST_FEATURE=SENTINEL,
                                         BB_TEST_MODE=SENTINEL))
        self.assertEqual(result.returncode, 1)
        self.assertIn("BB_TEST_TOKEN: required value is missing", result.stderr)
        self.assertIn("BB_TEST_PORT: expected an integer", result.stderr)
        self.assertIn("BB_TEST_FEATURE: expected true or false", result.stderr)
        self.assertIn("BB_TEST_MODE: expected a declared public choice", result.stderr)
        self.assert_redacted(result)

    def test_literal_file_never_executes_or_interpolates_supplied_values(self):
        self.contract([variable()])
        marker = self.root / "must-not-exist"
        value = f"{SENTINEL} $(touch {marker}) `touch {marker}` ${{HOME}} # literal 'quotes'"
        (self.root / ".env").write_text("# comment\n\nBB_TEST_TOKEN=" + value + "\n",
                                        encoding="utf-8")
        parsed = environment.load_env_file(self.root / ".env", {"BB_TEST_TOKEN"})
        self.assertEqual(parsed["BB_TEST_TOKEN"], value)
        result = self.run_cli("--env-file", ".env")
        self.assertEqual(result.returncode, 0)
        self.assertFalse(marker.exists())
        self.assert_redacted(result, value)

    def test_process_overrides_file_even_when_process_value_is_empty(self):
        self.contract([variable("BB_TEST_PORT", "integer", secret=False)])
        (self.root / ".env").write_text("BB_TEST_PORT=" + SENTINEL + "\n", encoding="utf-8")
        result = self.run_cli("--env-file", ".env", values={"BB_TEST_PORT": "7"})
        self.assertEqual(result.returncode, 0)
        self.assert_redacted(result)
        result = self.run_cli("--env-file", ".env", values={"BB_TEST_PORT": ""})
        self.assertEqual(result.returncode, 1)
        self.assertIn("required value is missing", result.stderr)
        self.assert_redacted(result)

    def test_env_file_rejects_duplicate_unknown_and_malformed_lines_safely(self):
        self.contract([variable()])
        samples = [
            "BB_TEST_TOKEN=first\nBB_TEST_TOKEN=" + SENTINEL,
            "UNKNOWN_SECRET_NAME=" + SENTINEL,
            SENTINEL,
            "export BB_TEST_TOKEN=" + SENTINEL,
            " BB_TEST_TOKEN=" + SENTINEL,
            "BB_TEST_TOKEN=" + SENTINEL + "\0",
        ]
        for sample in samples:
            with self.subTest(case=samples.index(sample)):
                (self.root / ".env").write_text(sample, encoding="utf-8")
                result = self.run_cli("--env-file", ".env")
                self.assertEqual(result.returncode, 1)
                self.assertIn("env file line", result.stderr)
                self.assert_redacted(result, "UNKNOWN_SECRET_NAME")

    def test_contract_rejects_values_defaults_secret_enums_and_invalid_metadata(self):
        entries = [
            variable(value=SENTINEL), variable(default=SENTINEL),
            variable("BB_TEST_MODE", "enum", choices=[SENTINEL]),
            variable(SENTINEL.lower()),
            variable(required=["local", "local"]),
            variable(required=["unknown"]),
            variable("BB_TEST_PORT", "integer", choices=[SENTINEL]),
            variable("BB_TEST_MODE", "enum", secret=False, choices=["same", "same"]),
            dict(variable(), secret="true"), dict(variable(), type=[]),
        ]
        for index, entry in enumerate(entries):
            with self.subTest(case=index):
                self.contract([entry])
                result = self.run_cli()
                self.assertEqual(result.returncode, 1)
                self.assertIn("contract entry", result.stderr)
                self.assert_redacted(result, SENTINEL.lower())

    def test_invalid_json_duplicate_names_or_object_keys_and_encoding_are_redacted(self):
        path = self.root / "config/environment.json"
        samples = [
            SENTINEL.encode(),
            b'{"version":1,"version":1,"variables":[]}',
            json.dumps(dict(version=True, variables=[])).encode(),
            json.dumps(dict(version=1, variables=[variable(), variable()])).encode(),
            json.dumps(dict(version=1, variables=[], unexpected=SENTINEL)).encode(),
            b'\xff' + SENTINEL.encode(),
        ]
        for index, sample in enumerate(samples):
            with self.subTest(case=index):
                path.write_bytes(sample)
                result = self.run_cli()
                self.assertEqual(result.returncode, 1)
                self.assert_redacted(result)

    def test_optional_empty_values_are_allowed_but_invalid_supplied_values_are_not(self):
        self.contract([variable("BB_TEST_FEATURE", "boolean", secret=False, required=[])])
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertEqual(self.run_cli(values={"BB_TEST_FEATURE": ""}).returncode, 0)
        result = self.run_cli(values={"BB_TEST_FEATURE": "TRUE"})
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected true or false", result.stderr)

    def test_value_file_and_contract_limits_are_enforced_without_leaks(self):
        self.contract([variable()])
        (self.root / ".env").write_text("BB_TEST_TOKEN=" + SENTINEL + "x" * 65536,
                                        encoding="utf-8")
        result = self.run_cli("--env-file", ".env")
        self.assertEqual(result.returncode, 1)
        self.assert_redacted(result)
        (self.root / "config/environment.json").write_bytes(b" " * (environment.MAX_BYTES + 1))
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("size limit", result.stderr)
        self.assert_redacted(result)

    def test_explicit_paths_stay_inside_root_and_link_paths_are_rejected(self):
        self.contract([])
        result = self.run_cli("--contract", "../" + SENTINEL)
        self.assertEqual(result.returncode, 1)
        self.assertIn("inside the selected root", result.stderr)
        self.assert_redacted(result)
        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaisesRegex(environment.EnvironmentError, "symbolic links"):
                environment._input_path(self.root, Path("config/environment.json"))

    def test_unknown_cli_argument_is_redacted(self):
        self.contract([])
        result = self.run_cli("--unexpected", SENTINEL)
        self.assertEqual(result.returncode, 2)
        self.assert_redacted(result)


if __name__ == "__main__":
    unittest.main()
