"""Adversarial tests for structural contracts, not runtime agent compliance."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate import BUNDLE, POLICY_FLOOR, validate_root


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "candidate"
        self.root.mkdir()
        self.write("policy/core.json", {"schema_version": "1", "version": "0.1.0", "invariants": dict(POLICY_FLOOR)})
        self.write("policy/core.md", "# Shared policy\n")
        self.write(".engineering-backbone/project.json", {
            "schema_version": "1",
            "project": {"name": "example", "base_branch": "main", "language": "Python", "has_frontend": False,
                        "has_backend": False, "validation_command": "python -m unittest discover -s tests -v"},
            "agents": {"codex": True, "copilot": True},
        })
        self.write("AGENTS.md", "Read [the policy](policy/core.md).\n")
        self.write(".github/copilot-instructions.md", "Read [the policy](../policy/core.md).\n")
        for role in ("planner", "implementer", "reviewer"):
            mode = "workspace-write" if role == "implementer" else "read-only"
            self.write(f".codex/agents/backbone-{role}.toml", f'name = "backbone_{role}"\ndescription = "Scoped {role}"\nsandbox_mode = "{mode}"\ndeveloper_instructions = "Read the shared policy before acting."\n')
            tools = "[read, search, edit, execute]" if role == "implementer" else "[read, search]"
            self.write(f".github/agents/backbone-{role}.agent.md", f"---\nname: backbone-{role}\ndescription: Scoped {role}\ntools: {tools}\n---\nRead the shared policy.\n")
        for filename in ("requirements.txt", "requirements.lock"):
            shutil.copy2(BUNDLE / filename, self.root / filename)
        for directory in ("schemas", "examples"):
            shutil.copytree(BUNDLE / directory, self.root / directory)

    def write(self, path, data):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(data, indent=2) + "\n" if isinstance(data, dict) else data, encoding="utf-8")

    def mutate_json(self, relative, mutation):
        data = json.loads((self.root / relative).read_text())
        mutation(data)
        self.write(relative, data)

    def make_consumer(self):
        managed = self.root / ".engineering-backbone"
        for filename in ("core.json", "core.md"):
            shutil.move(self.root / "policy" / filename, managed / filename)
        shutil.rmtree(self.root / "policy")
        for filename in ("requirements.txt", "requirements.lock"):
            shutil.move(self.root / filename, managed / filename)
        for directory in ("schemas", "examples"):
            shutil.move(self.root / directory, managed / directory)
        self.write("AGENTS.md", "Read [policy](.engineering-backbone/core.md).\n")
        self.write(".github/copilot-instructions.md", "Read [policy](../.engineering-backbone/core.md).\n")

    def reject(self, fragment, trusted_base=None, *, mode=None):
        errors = validate_root(self.root, trusted_base, mode=mode)
        self.assertTrue(errors, "mutation was unexpectedly accepted")
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_source_and_examples(self):
        self.assertEqual([], validate_root(self.root))

    def test_root_run_artifacts_are_excluded_from_source_validation(self):
        self.write("artifacts/review-run/output.md", "<<<<<<< captured example\n[Captured link](absent.md)\n")
        self.write("artifacts/reviews/result.json", {"scope": {"unvalidated": "captured payload"}})
        self.assertEqual([], validate_root(self.root))

    def test_nested_source_artifacts_remain_governed(self):
        self.write("docs/reviews/artifacts/control.md", "<<<<<<< candidate\n[Missing guide](absent.md)\n")
        self.reject("unresolved merge conflict marker")
        self.reject("broken local Markdown link")
        self.write("docs/reviews/artifacts/task-packet.json", {"scope": {}})
        self.reject("task-packet.json: scope:")

    def test_managed_consumer_artifacts_remain_governed(self):
        self.make_consumer()
        self.write(".engineering-backbone/artifacts/control.md", "<<<<<<< candidate\n[Missing guide](absent.md)\n")
        self.reject("unresolved merge conflict marker", mode="consumer")
        self.reject("broken local Markdown link", mode="consumer")
        self.write(".engineering-backbone/artifacts/reviews/task-packet.json", {"scope": {}})
        self.reject("task-packet.json: scope:", mode="consumer")

    def test_project_and_task_branches_follow_git_branch_rules(self):
        invalid = (
            "feature/.hidden", "release.lock/next", "x/a.lock.lock/z", "HEAD", "main\n",
            "/main", "main/", "main.", ".main", "feature//one", "feature/../main", "-main",
            "bad~name", "bad^name", "bad:name", "bad?name", "bad*name", "bad[name",
            "bad\\name", "bad@{name", "bad name", "bad\tname", "bad\x7fname",
        )
        valid = ("main", "feature/frontend", "release/v1.0", "feature/a./next", "feature/a.lockx/next",
                 "x/HEAD", "refs/heads/main", "équipe/main", "feature/+foo", "@")
        for branch in invalid + valid:
            oracle = subprocess.run(["git", "check-ref-format", "--branch", branch], capture_output=True)
            self.assertEqual(oracle.returncode == 0, branch in valid, repr(branch))
        for mode in ("source", "consumer"):
            if mode == "consumer":
                self.make_consumer()
            packet_path = "examples/task-packet.json" if mode == "source" else ".engineering-backbone/examples/task-packet.json"
            for branch in invalid + ("bad\x00name",) + valid:
                with self.subTest(mode=mode, branch=repr(branch)):
                    self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(base_branch=branch))
                    self.mutate_json(packet_path, lambda data: data["repository"].update(base_branch=branch))
                    errors = validate_root(self.root, mode=mode)
                    if branch in valid:
                        self.assertEqual([], errors)
                    else:
                        self.assertTrue(any("project.base_branch" in error for error in errors), errors)
                        self.assertTrue(any("repository.base_branch" in error for error in errors), errors)
            self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(base_branch="main"))

    def test_weakened_or_removed_policy_is_rejected(self):
        self.mutate_json("policy/core.json", lambda data: data["invariants"].update(human_merge_required=False))
        self.reject("human_merge_required")
        self.mutate_json("policy/core.json", lambda data: data["invariants"].pop("delta_after_fix"))
        self.reject("delta_after_fix")

    def test_automatic_downstream_apply_is_rejected(self):
        self.mutate_json("policy/core.json", lambda data: data["invariants"].update(automatic_downstream_apply=True))
        self.reject("automatic_downstream_apply")

    def test_trusted_base_additional_invariant_cannot_be_removed(self):
        base = Path(self.temp.name) / "base"
        shutil.copytree(self.root, base)
        path = base / "policy/core.json"
        policy = json.loads(path.read_text())
        policy["invariants"]["security_review_required"] = True
        path.write_text(json.dumps(policy))
        self.reject("trusted-base invariant security_review_required", base)

    def test_stronger_new_invariant_is_allowed(self):
        base = Path(self.temp.name) / "base"
        shutil.copytree(self.root, base)
        self.mutate_json("policy/core.json", lambda data: data["invariants"].update(security_review_required=True))
        self.assertEqual([], validate_root(self.root, base))

    def test_base_without_policy_requires_explicit_bootstrap(self):
        base = Path(self.temp.name) / "base"
        base.mkdir()
        self.reject("BOOTSTRAP", base)

    def test_candidate_schema_cannot_relax_executing_validator(self):
        self.write("schemas/core-policy.schema.json", {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"})
        self.mutate_json("policy/core.json", lambda data: data.update(version="forged"))
        self.reject("version")

    def test_invalid_schema_and_example_are_rejected(self):
        self.write("schemas/invalid.schema.json", {"type": "made-up"})
        self.reject("invalid JSON schema")
        self.mutate_json("examples/task-packet.json", lambda data: data.update(role="autonomous_merger"))
        self.reject("role")

    def test_task_scope_cannot_escape_repository(self):
        self.mutate_json("examples/task-packet.json", lambda data: data["scope"].update(include=["../another-repo/**"]))
        self.reject("scope.include")

    def test_missing_scope_is_rejected(self):
        self.mutate_json("examples/task-packet.json", lambda data: data.pop("scope"))
        self.reject("unrecognized governance JSON artifact")

    def test_completed_task_needs_frozen_revisions_and_evidence(self):
        self.mutate_json("examples/task-packet.json", lambda data: data.update(status="completed"))
        self.reject("base_revision")
        self.mutate_json("examples/task-packet.json", lambda data: data["acceptance"][0].update(status="pass"))
        self.reject("evidence")

    def test_passed_requirement_needs_evidence_and_implementation(self):
        self.mutate_json("examples/requirement.json", lambda data: data["verification"].update(status="pass"))
        self.reject("evidence")
        self.reject("implementation")

    def test_review_cannot_self_certify_independence(self):
        self.mutate_json("examples/review-evidence.json", lambda data: data.update(implementer=data["reviewers"][0]["id"]))
        self.reject("their own independent reviewer")

    def test_forged_no_findings_without_pass_evidence_is_rejected(self):
        self.mutate_json("examples/review-evidence.json", lambda data: data.update(outcome="no_findings"))
        self.reject("checks.0.status")
        self.mutate_json("examples/review-evidence.json", lambda data: data["checks"][0].update(status="pass"))
        self.reject("evidence")

    def test_delta_review_needs_finding_and_regression_scope(self):
        self.mutate_json("examples/review-evidence.json", lambda data: data.update(kind="delta"))
        self.reject("delta")

    def test_fixed_finding_requires_confirmed_triage(self):
        finding = {"id": "F-1", "severity": "P1", "location": {"path": "src/feature.py", "line": 1},
                   "claim": "Boundary is bypassed", "evidence": ["Review reproduction"],
                   "triage": "untriaged", "disposition": "fixed"}
        self.mutate_json("examples/review-evidence.json", lambda data: data.update(outcome="changes_requested", findings=[finding]))
        self.reject("triage")

    def test_missing_reviewer_and_unsafe_codex_sandbox_are_rejected(self):
        path = self.root / ".codex/agents/backbone-reviewer.toml"
        content = path.read_text()
        path.unlink()
        self.reject("missing required file")
        path.write_text(content.replace('"read-only"', '"workspace-write"'))
        self.reject("sandbox_mode must be read-only")

    def test_codex_cannot_pin_model_or_credentials(self):
        path = self.root / ".codex/agents/backbone-reviewer.toml"
        path.write_text(path.read_text() + 'model = "override"\n')
        self.reject("unapproved keys")

    def test_copilot_reviewer_cannot_execute_or_delegate(self):
        path = self.root / ".github/agents/backbone-reviewer.agent.md"
        for forbidden in ("execute", "edit", "agent/*"):
            original = path.read_text()
            path.write_text(original.replace("tools: [read, search]", f"tools: [read, search, {forbidden}]"))
            self.reject("tools must be exactly")
            path.write_text(original)

    def test_disabled_adapter_does_not_require_entrypoints(self):
        self.mutate_json(".engineering-backbone/project.json", lambda data: data.update(agents={"codex": False, "copilot": False}))
        shutil.rmtree(self.root / ".codex")
        shutil.rmtree(self.root / ".github")
        (self.root / "AGENTS.md").unlink()
        self.assertEqual([], validate_root(self.root))

    def test_trusted_base_enabled_adapters_cannot_be_disabled_or_removed(self):
        for mode in ("source", "consumer"):
            if mode == "consumer":
                self.make_consumer()
            base = Path(self.temp.name) / f"{mode}-trusted-adapters"
            shutil.copytree(self.root, base)
            for disabled in (("codex",), ("copilot",), ("codex", "copilot")):
                with self.subTest(mode=mode, disabled=disabled):
                    candidate = Path(self.temp.name) / (mode + "-disable-" + "-".join(disabled))
                    shutil.copytree(base, candidate)
                    facts_path = candidate / ".engineering-backbone/project.json"
                    facts = json.loads(facts_path.read_text())
                    for adapter in disabled:
                        facts["agents"][adapter] = False
                    facts_path.write_text(json.dumps(facts))
                    # Metadata-only opt-outs fail even if all native files remain.
                    errors = validate_root(candidate, base, mode=mode)
                    for adapter in disabled:
                        self.assertTrue(any(f"enabled {adapter} must remain enabled" in error for error in errors), errors)
                        if adapter == "codex":
                            (candidate / "AGENTS.md").unlink()
                            shutil.rmtree(candidate / ".codex")
                        else:
                            (candidate / ".github/copilot-instructions.md").unlink()
                            shutil.rmtree(candidate / ".github/agents")
                    # The effective union also retains the actual file checks.
                    errors = validate_root(candidate, base, mode=mode)
                    for adapter in disabled:
                        expected = "AGENTS.md" if adapter == "codex" else ".github/copilot-instructions.md"
                        self.assertTrue(any(f"missing required file: {expected}" in error for error in errors), errors)

    def test_disabled_flags_cannot_hide_installed_adapter_permissions_or_content(self):
        self.make_consumer()
        base = Path(self.temp.name) / "trusted-content"
        shutil.copytree(self.root, base)
        self.mutate_json(".engineering-backbone/project.json", lambda data: data.update(agents={"codex": False, "copilot": False}))
        reviewer = self.root / ".github/agents/backbone-reviewer.agent.md"
        reviewer.write_text(reviewer.read_text().replace("tools: [read, search]", "tools: [execute]") + "\n<<<<<<< candidate\n[Missing guide](missing.md)\n")
        self.reject("tools must be", base, mode="consumer")
        self.reject("unresolved merge conflict marker", base, mode="consumer")
        self.reject("broken local Markdown link", base, mode="consumer")

    def test_trusted_base_project_configuration_must_be_readable_and_valid(self):
        for mode in ("source", "consumer"):
            if mode == "consumer":
                self.make_consumer()
            base = Path(self.temp.name) / f"{mode}-trusted-facts"
            shutil.copytree(self.root, base)
            facts_path = base / ".engineering-backbone/project.json"
            original = facts_path.read_text()
            facts_path.unlink()
            self.reject("trusted-base project configuration is unreadable", base, mode=mode)
            for invalid in ("{broken", '{"agents":{"codex":true,"codex":false}}'):
                facts_path.write_text(invalid)
                self.reject("trusted-base project configuration is unreadable", base, mode=mode)
            for invalid in ([], {}, {"agents": {"codex": "yes", "copilot": False}}):
                facts_path.write_text(json.dumps(invalid))
                self.reject("trusted-base project configuration:", base, mode=mode)
            facts_path.write_text(original)
            self.assertEqual([], validate_root(self.root, base, mode=mode))

    def test_initial_disabled_selection_and_later_strengthening_remain_valid(self):
        for mode in ("source", "consumer"):
            if mode == "consumer":
                self.make_consumer()
            base = Path(self.temp.name) / f"{mode}-initial-disabled"
            shutil.copytree(self.root, base)
            facts_path = base / ".engineering-backbone/project.json"
            facts = json.loads(facts_path.read_text())
            facts["agents"] = {"codex": False, "copilot": False}
            facts_path.write_text(json.dumps(facts))
            for adapter in ("codex", "copilot"):
                if adapter == "codex":
                    (base / "AGENTS.md").unlink()
                    shutil.rmtree(base / ".codex")
                else:
                    shutil.rmtree(base / ".github")
            self.assertEqual([], validate_root(base, mode=mode))
            self.assertEqual([], validate_root(base, base, mode=mode))
            # The complete candidate adds both providers against a disabled base.
            self.assertEqual([], validate_root(self.root, base, mode=mode))

    def test_unrelated_project_facts_remain_editable_against_trusted_base(self):
        for mode in ("source", "consumer"):
            if mode == "consumer":
                self.make_consumer()
            base = Path(self.temp.name) / f"{mode}-editable-facts"
            shutil.copytree(self.root, base)
            self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(
                name="renamed-project", base_branch="feature/new-base", language="TypeScript", has_frontend=True,
                validation_command="npm test"))
            self.assertEqual([], validate_root(self.root, base, mode=mode))

    def test_broken_relative_markdown_link_is_rejected(self):
        self.write("README.md", "See [policy](policy/missing.md).\n")
        self.reject("broken local Markdown link")

    def test_escaped_symlink_is_rejected(self):
        external = Path(self.temp.name) / "external.md"
        external.write_text("External")
        (self.root / "external.md").symlink_to(external)
        self.reject("resolves outside the repository")

    def test_source_template_conflict_marker_is_rejected(self):
        self.write("template/file.md.jinja", "<<<<<<< conflicting-head\nunsafe\n>>>>>>> conflicting-base\n")
        self.reject("unresolved merge conflict marker")

    def test_duplicate_json_keys_are_rejected(self):
        self.write("policy/core.json", '{"schema_version":"1","schema_version":"1"}')
        self.reject("duplicate JSON key")

    def test_commands_are_data_and_are_never_executed(self):
        marker = self.root / "EXECUTED"
        self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(validation_command="touch EXECUTED"))
        self.mutate_json("examples/task-packet.json", lambda data: data["validation"].update(commands=["touch EXECUTED"]))
        self.assertEqual([], validate_root(self.root))
        self.assertFalse(marker.exists())

    def test_core_and_config_reject_source_domains_or_machine_paths(self):
        self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(validation_command="python /workspace/private/check.py"))
        self.reject("absolute machine path")
        self.mutate_json(".engineering-backbone/project.json", lambda data: data["project"].update(validation_command="curl https://github.com/Artifaktory/Tars/private"))
        self.reject("source-project domain")

    def test_direct_dependency_bump_requires_lock_regeneration(self):
        path = self.root / "requirements.txt"
        path.write_text(path.read_text().replace("jsonschema==4.26.0", "jsonschema==4.27.0"))
        self.reject("dependency lock mismatch")

    def test_lock_rejects_unhashed_unpinned_or_external_installs(self):
        path = self.root / "requirements.lock"
        original = path.read_text()
        for bad_entry in ("unsafe==1.0", "unsafe>=1.0", "--index-url https://example.invalid", "unsafe @ git+https://example.invalid/project.git"):
            with self.subTest(entry=bad_entry):
                path.write_text(original + "\n" + bad_entry + "\n")
                self.reject("exact == pins")
        path.write_text(original)

    def workflow(self, change=""):
        self.write(".github/workflows/backbone-ci.yml", """name: Backbone
on: [pull_request]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@0000000000000000000000000000000000000000
        with:
          persist-credentials: false
      - run: python scripts/validate.py
""" + change)

    def test_workflow_security_rejects_mutable_actions_and_credentials(self):
        self.workflow()
        self.assertEqual([], validate_root(self.root))
        path = self.root / ".github/workflows/backbone-ci.yml"
        original = path.read_text()
        path.write_text(original.replace("@" + "0" * 40, "@main"))
        self.reject("full commit SHA")
        path.write_text(original.replace("persist-credentials: false", "persist-credentials: true"))
        self.reject("persist-credentials")

    def test_workflow_security_rejects_privileged_events_and_permissions(self):
        self.workflow()
        path = self.root / ".github/workflows/backbone-ci.yml"
        original = path.read_text()
        path.write_text(original.replace("pull_request", "pull_request_target"))
        self.reject("pull_request_target")
        path.write_text(original.replace("contents: read", "contents: write"))
        self.reject("read-only contents")
        path.write_text(original.replace("    runs-on:", "    secrets: inherit\n    runs-on:"))
        self.reject("secrets: inherit")

    def test_unrelated_consumer_workflows_are_not_restricted(self):
        self.make_consumer()
        self.write(".github/workflows/deploy.yml", "on: [workflow_dispatch]\npermissions: write-all\njobs: {}\n")
        self.assertEqual([], validate_root(self.root, mode="consumer"))

    def test_review_ready_and_active_reviewer_require_frozen_revisions(self):
        path = "examples/task-packet.json"
        original = json.loads((self.root / path).read_text())
        for status, role in (("ready_for_review", "implementer"), ("active", "reviewer")):
            with self.subTest(status=status, role=role):
                packet = {**original, "status": status, "role": role}
                self.write(path, packet)
                self.reject("base_revision")
                self.reject("head_revision")
                packet["repository"] = {**original["repository"], "base_revision": "a" * 40, "head_revision": "b" * 40}
                self.write(path, packet)
                self.assertEqual([], validate_root(self.root))
        original["status"] = "active"
        self.write(path, original)
        self.assertEqual([], validate_root(self.root))

    def test_consumer_ordinary_policy_and_application_content_are_unrelated(self):
        self.make_consumer()
        self.write("policy/core.json", {"application": "ordinary local policy"})
        self.write("examples/api-response.json", {"message": "application example"})
        self.write("plans/application-plan.json", {"plan": "ordinary local application plan"})
        self.write("README.md", "[Site docs](/docs). [Local page](not-generated.md)\n<<<<<<< application-example\n")
        self.write("AGENTS.md", "[Project conventions](/docs) and [local page](not-generated.md).\n")
        self.write(".github/copilot-instructions.md", "[Project conventions](/docs).\n")
        self.assertEqual([], validate_root(self.root, mode="consumer"))
        self.mutate_json(".engineering-backbone/core.json", lambda data: data["invariants"].update(human_merge_required=False))
        self.reject("human_merge_required", mode="consumer")

    def test_candidate_vendored_marker_cannot_bypass_source_policy_guard(self):
        self.write(".engineering-backbone/validate.py", "# Consumer marker candidate\n")
        self.write(".engineering-backbone/core.json", {"schema_version": "1", "version": "0.1.0", "invariants": dict(POLICY_FLOOR)})
        self.mutate_json("policy/core.json", lambda data: data["invariants"].update(human_merge_required=False))
        self.reject("human_merge_required")

    def test_consumer_still_checks_managed_links_artifacts_and_conflicts(self):
        self.make_consumer()
        self.write(".engineering-backbone/README.md", "[Missing managed guide](missing.md).\n")
        self.reject("broken local Markdown link", mode="consumer")
        self.mutate_json(".engineering-backbone/examples/task-packet.json", lambda data: data.update(status="ready_for_review"))
        self.reject("base_revision", mode="consumer")
        self.write(".engineering-backbone/core.md", "<<<<<<< candidate\nManaged policy\n")
        self.reject("unresolved merge conflict marker", mode="consumer")

    def test_consumer_allows_stricter_native_permissions_only(self):
        self.make_consumer()
        reviewer = self.root / ".github/agents/backbone-reviewer.agent.md"
        original = reviewer.read_text()
        reviewer.write_text(original.replace("tools: [read, search]", "tools: [read]"))
        implementer = self.root / ".codex/agents/backbone-implementer.toml"
        implementer.write_text(implementer.read_text().replace('"workspace-write"', '"read-only"'))
        self.assertEqual([], validate_root(self.root, mode="consumer"))
        for tools in ("[]", "[read, read]", "[read, edit]", "[read, execute]", "[read, agent/*]", "[unknown]"):
            with self.subTest(tools=tools):
                reviewer.write_text(original.replace("tools: [read, search]", f"tools: {tools}"))
                self.reject("nonempty unique subset", mode="consumer")
        reviewer.write_text(original.replace("tools: [read, search]\n", ""))
        self.reject("nonempty unique subset", mode="consumer")
        reviewer.write_text(original.replace("tools: [read, search]", "tools: [read]"))
        implementer.write_text(implementer.read_text().replace('"read-only"', '"danger-full-access"'))
        self.reject("sandbox_mode", mode="consumer")

    def test_source_native_profiles_retain_exact_defaults(self):
        reviewer = self.root / ".github/agents/backbone-reviewer.agent.md"
        reviewer.write_text(reviewer.read_text().replace("tools: [read, search]", "tools: [read]"))
        self.reject("tools must be exactly")
        implementer = self.root / ".codex/agents/backbone-implementer.toml"
        implementer.write_text(implementer.read_text().replace('"workspace-write"', '"read-only"'))
        self.reject("sandbox_mode must be workspace-write")


if __name__ == "__main__":
    unittest.main()
