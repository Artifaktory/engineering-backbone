"""Real optional workflow-kit installation, preservation and activation fixtures.

Profile smoke commands below are actual fixture checks. They test template and
runner integration, not production compiler, SAST or dependency-scanner coverage.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy, run_update
import yaml


ROOT = Path(__file__).resolve().parents[1]
KIT_FILES = (
    ".engineering-backbone/workflows.json",
    ".engineering-backbone/schemas/workflows.schema.json",
    ".engineering-backbone/workflow-kit.py",
    ".engineering-backbone/workflow-guide.md",
    ".engineering-backbone/profiles.json",
    ".engineering-backbone/workflow-examples/release.yml.example",
    ".engineering-backbone/workflow-examples/deploy.yml.example",
)
CALLERS = (
    ".github/workflows/backbone-pr-checks.yml",
    ".github/workflows/backbone-maintenance.yml",
)
SEED = {
    "schema_version": "1", "enabled": False, "profiles": [],
    "capabilities": [], "runtimes": {}, "checks": [],
}


def git(path, *arguments):
    result = subprocess.run(
        ["git", *arguments], cwd=path, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def initialize(path):
    git(path, "-c", "init.defaultBranch=main", "init")
    git(path, "config", "user.email", "backbone-tests@example.invalid")
    git(path, "config", "user.name", "Backbone workflow fixture")


def commit(path, message):
    git(path, "add", ".")
    git(path, "commit", "-m", message)


def snapshot(path):
    return {
        item.relative_to(path): item.read_bytes()
        for item in path.rglob("*")
        if item.is_file() and ".git" not in item.relative_to(path).parts
    }


class WorkflowKitCopierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="backbone-kit-copier-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.source = self.workspace / "source"
        shutil.copytree(
            ROOT, self.source,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "artifacts", ".venv"),
        )
        initialize(self.source)
        commit(self.source, "Workflow template fixture v0.1.0")
        git(self.source, "tag", "v0.1.0")
        self.counter = 0

    def copy(self, *, target=None, ref="v0.1.0", **data):
        if target is None:
            target = self.workspace / f"consumer-{self.counter}"
            self.counter += 1
        run_copy(
            str(self.source), target, data=data, vcs_ref=ref,
            defaults=True, quiet=True, skip_tasks=True, overwrite=True,
        )
        return target

    def upgrade_source(self):
        guide = self.source / "docs/workflows/README.md"
        guide.write_text(guide.read_text() + "\nReviewed workflow guide fixture update.\n")
        commit(self.source, "Workflow template fixture v0.2.0")
        git(self.source, "tag", "v0.2.0")

    def update(self, target, **data):
        run_update(
            target, answers_file=".engineering-backbone/copier-answers.yml",
            vcs_ref="v0.2.0", data=data, defaults=True, quiet=True,
            skip_tasks=True, overwrite=True,
        )

    def runner(self, target, *arguments):
        return subprocess.run(
            [sys.executable, "-I", str(target / ".engineering-backbone/workflow-kit.py"),
             *arguments], cwd=target, text=True, capture_output=True,
        )

    def test_default_copy_retains_legacy_project_and_has_no_kit(self):
        target = self.copy(use_codex=False, use_copilot=False)
        self.assertFalse((target / ".github").exists())
        for relative in KIT_FILES + CALLERS:
            self.assertFalse((target / relative).exists(), relative)
        facts = json.loads((target / ".engineering-backbone/project.json").read_text())
        self.assertEqual(facts["schema_version"], "1")
        self.assertNotIn("workflows", facts)
        self.assertEqual(
            (target / ".engineering-backbone/schemas/project.schema.json").read_text().strip(),
            (self.source / "schemas/project.schema.json").read_text().strip(),
        )

    def test_selected_kit_renders_inactive_empty_seed_and_reference_tools(self):
        target = self.copy(use_workflow_kit=True, use_codex=False, use_copilot=False)
        for relative in KIT_FILES:
            self.assertTrue((target / relative).is_file(), relative)
        for relative in CALLERS:
            self.assertFalse((target / relative).exists(), relative)
        self.assertEqual(json.loads((target / KIT_FILES[0]).read_text()), SEED)
        self.assertEqual(
            (target / KIT_FILES[1]).read_text().strip(),
            (self.source / "schemas/workflows.schema.json").read_text().strip(),
        )
        self.assertEqual(
            (target / KIT_FILES[2]).read_text().strip(),
            (self.source / "scripts/workflow_kit.py").read_text().strip(),
        )
        catalog = json.loads((target / ".engineering-backbone/profiles.json").read_text())
        self.assertEqual(set(catalog["profiles"]), {"docs", "python", "typescript", "go", "dotnet"})
        self.assertEqual(set(catalog["capabilities"]),
                         {"dependencies", "web", "api", "database", "container", "iac", "release", "deploy"})
        result = self.runner(target, "validate", "--root", str(target))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        guide = (target / ".engineering-backbone/workflow-guide.md").read_text()
        self.assertIn("No native callers were selected", guide)
        self.assertIn("inactive", guide)

    def test_pinned_callers_render_with_read_only_permissions_and_supported_events(self):
        pin = "ABCDEF0123456789" * 2 + "ABCDEF01"
        target = self.copy(use_workflow_kit=True, workflow_kit_ref=pin, base_branch="feature/frontend")
        for relative, job_id, reusable in (
            (CALLERS[0], "pr-checks", "workflow-kit-pr.yml"),
            (CALLERS[1], "maintenance", "workflow-kit-maintenance.yml"),
        ):
            with self.subTest(caller=relative):
                text = (target / relative).read_text()
                data = yaml.safe_load(text)
                self.assertEqual(data["permissions"], {"contents": "read"})
                job = data["jobs"][job_id]
                self.assertEqual(job["uses"], "Artifaktory/engineering-backbone/.github/workflows/" + reusable + "@" + pin.lower())
                self.assertEqual(job["permissions"], {"contents": "read"})
                self.assertNotIn("secrets", job)
                self.assertNotIn("with", job)
                self.assertNotIn("{{", text)
        # PyYAML's YAML 1.1 loader treats the GitHub `on` key as boolean True.
        pr_events = yaml.safe_load((target / CALLERS[0]).read_text())[True]
        self.assertEqual(set(pr_events), {"pull_request", "push", "workflow_dispatch"})
        self.assertEqual(pr_events["push"]["branches"], ["feature/frontend"])
        maintenance_events = yaml.safe_load((target / CALLERS[1]).read_text())[True]
        self.assertEqual(set(maintenance_events), {"schedule", "workflow_dispatch"})
        self.assertEqual(maintenance_events["schedule"], [{"cron": "23 5 * * 1"}])

    def test_first_install_pin_cannot_turn_incomplete_seed_into_successful_execution(self):
        target = self.copy(use_workflow_kit=True, workflow_kit_ref="a" * 40)
        result = self.runner(
            target, "prepare", "--root", str(target), "--trusted-base", str(target),
            "--phase", "pr", "--output", str(target / "prepared.json"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires an enabled configuration", result.stdout)
        self.assertFalse((target / "prepared.json").exists())

    def test_invalid_install_choices_reject_before_consumer_mutation(self):
        target = self.workspace / "existing"
        target.mkdir()
        (target / "README.md").write_text("Existing local project remains.\n")
        before = snapshot(target)
        for data in (
            {"use_workflow_kit": True, "workflow_kit_ref": "main"},
            {"use_workflow_kit": True, "workflow_kit_ref": "a" * 40 + "\n"},
            {"use_workflow_kit": True, "workflow_kit_ref": "a" * 39},
            {"use_workflow_kit": False, "workflow_kit_ref": "a" * 40},
        ):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.copy(target=target, **data)
                self.assertEqual(snapshot(target), before)

    def test_creation_and_update_preserve_local_config_callers_and_delivery_files(self):
        target = self.workspace / "preserved"
        target.mkdir()
        protected = {
            KIT_FILES[0]: json.dumps(dict(SEED, profiles=["docs"])) + "\n",
            CALLERS[0]: "# Existing stronger PR gate remains byte-identical.\n",
            CALLERS[1]: "# Existing scheduled security control remains.\n",
            ".github/workflows/backbone-release.yml": "# Reviewed local release workflow remains.\n",
            ".github/workflows/backbone-deploy.yml": "# Reviewed local deployment workflow remains.\n",
            ".github/workflows/project-ci.yml": "# Unrelated project workflow remains.\n",
            KIT_FILES[-2]: "# Existing release integration example remains.\n",
            KIT_FILES[-1]: "# Existing deployment integration example remains.\n",
        }
        for relative, content in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.copy(target=target, use_workflow_kit=True, workflow_kit_ref="a" * 40)
        initialize(target)
        commit(target, "Preserved project-owned workflow configuration")
        self.upgrade_source()
        self.update(target)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_text(), content, relative)
        self.assertIn("Reviewed workflow guide fixture update", (target / ".engineering-backbone/workflow-guide.md").read_text())

    def test_update_cannot_switch_kit_selection_or_pin(self):
        self.upgrade_source()
        cases = (
            ({"use_workflow_kit": False}, {"use_workflow_kit": True}),
            ({"use_workflow_kit": True}, {"use_workflow_kit": False}),
            ({"use_workflow_kit": True}, {"workflow_kit_ref": "a" * 40}),
            ({"use_workflow_kit": True, "workflow_kit_ref": "a" * 40}, {"workflow_kit_ref": ""}),
            ({"use_workflow_kit": True, "workflow_kit_ref": "a" * 40}, {"workflow_kit_ref": "b" * 40}),
        )
        for initial, requested in cases:
            with self.subTest(initial=initial, requested=requested):
                target = self.copy(**initial)
                initialize(target)
                commit(target, "Reviewed initial consumer selection")
                before = snapshot(target)
                with self.assertRaisesRegex(ValueError, "installation-only"):
                    self.update(target, **requested)
                self.assertEqual(snapshot(target), before)
                self.assertEqual(git(target, "status", "--porcelain"), "")

    def test_legacy_upgrade_does_not_adopt_kit_and_rejects_requested_autoadoption(self):
        copier_path = self.source / "copier.yml"
        modern = copier_path.read_bytes()
        modern_config = yaml.safe_load(modern)
        legacy_config = dict(modern_config)
        legacy_config.pop("use_workflow_kit")
        legacy_config.pop("workflow_kit_ref")
        legacy_config["_skip_if_exists"] = [
            value for value in legacy_config["_skip_if_exists"]
            if "backbone-pr-checks" not in value and "backbone-maintenance" not in value
            and "backbone-release" not in value and "backbone-deploy" not in value
            and "workflows.json" not in value and "workflow-examples" not in value
        ]
        optional_templates = {
            item.relative_to(self.source): item.read_bytes()
            for item in (self.source / "templates").rglob("*")
            if item.is_file() and "use_workflow_kit" in str(item)
        }
        for relative in optional_templates:
            (self.source / relative).unlink()
        copier_path.write_text(yaml.safe_dump(legacy_config, sort_keys=False))
        commit(self.source, "Legacy fixture without workflow choices")
        git(self.source, "tag", "v0.0.0")
        copier_path.write_bytes(modern)
        for relative, content in optional_templates.items():
            (self.source / relative).write_bytes(content)
        self.upgrade_source()
        for requested in ({}, {"use_workflow_kit": True}):
            with self.subTest(requested=requested):
                target = self.copy(ref="v0.0.0")
                answers_path = target / ".engineering-backbone/copier-answers.yml"
                old_answers = yaml.safe_load(answers_path.read_text())
                self.assertNotIn("use_workflow_kit", old_answers)
                self.assertNotIn("workflow_kit_ref", old_answers)
                initialize(target)
                commit(target, "Legacy consumer with no workflow kit")
                before = snapshot(target)
                if requested:
                    with self.assertRaisesRegex(ValueError, "installation-only"):
                        self.update(target, **requested)
                    self.assertEqual(snapshot(target), before)
                else:
                    self.update(target)
                    answers = yaml.safe_load(answers_path.read_text())
                    self.assertFalse(answers["use_workflow_kit"])
                    self.assertEqual(answers["workflow_kit_ref"], "")
                for relative in KIT_FILES + CALLERS:
                    self.assertFalse((target / relative).exists(), relative)

    def test_every_profile_can_render_then_run_actual_local_fixture_checks(self):
        catalog = json.loads((self.source / "docs/workflows/profiles.json").read_text())
        for profile, contract in catalog["profiles"].items():
            with self.subTest(profile=profile):
                target = self.copy(use_workflow_kit=True, language=profile)
                fixture = target / "fixture-check.py"
                fixture.write_text("import sys\nassert sys.argv[1] == 'actual-fixture-check'\nprint('fixture check executed')\n")
                checks = [
                    {"id": "fixture_" + kind, "kind": kind,
                     "argv": [sys.executable, "fixture-check.py", "actual-fixture-check"],
                     "cwd": ".", "timeout_seconds": 10, "phases": ["pr"]}
                    for kind in contract["pr"]
                ]
                runtimes = {} if contract["runtime"] is None else {contract["runtime"]: "12"}
                config = dict(SEED, enabled=True, profiles=[profile], runtimes=runtimes, checks=checks)
                config_path = target / KIT_FILES[0]
                config_path.write_text(json.dumps(config))
                for category in ("quality", "security"):
                    result = self.runner(
                        target, "run", "--root", str(target), "--config", str(config_path),
                        "--phase", "pr", "--category", category,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    if category == "quality" or profile != "docs":
                        self.assertIn("fixture check executed", result.stdout)
                self.assertEqual(json.loads(config_path.read_text())["checks"], checks)

    def test_inert_delivery_examples_have_real_activation_failure_and_environment_boundaries(self):
        target = self.copy(use_workflow_kit=True)
        for relative, delivery_job, environment, expected_kinds in (
            (KIT_FILES[-2], "release", "backbone-release-review", ("release-integrity", "provenance", "signature", "sbom")),
            (KIT_FILES[-1], "deployment", "backbone-deployment-review", ("deployment-smoke", "rollback", "monitoring")),
        ):
            with self.subTest(example=relative):
                text = (target / relative).read_text()
                data = yaml.safe_load(text)
                self.assertEqual(set(data[True]), {"workflow_dispatch"})
                self.assertEqual(data["permissions"], {"contents": "read"})
                delivery = data["jobs"][delivery_job]
                self.assertEqual(delivery["environment"], environment)
                self.assertEqual(delivery["needs"], "prerequisites")
                guard = data["jobs"]["prerequisites"]["steps"][0]["run"]
                result = subprocess.run(["bash", "-c", guard], cwd=target, text=True, capture_output=True)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("BLOCKED", result.stdout)
                self.assertIn("'head_sha': os.environ['GITHUB_SHA']", text)
                self.assertIn("'conclusion': 'success'", text)
                for kind in expected_kinds:
                    self.assertIn(kind, text)
                self.assertFalse((target / ".github/workflows" / Path(relative).name).exists())

    def test_delivery_prerequisite_scripts_reject_other_commits_workflows_and_failed_runs(self):
        target = self.copy(use_workflow_kit=True)
        command_directory = target / "fixture-bin"
        command_directory.mkdir()
        gh = command_directory / "gh"
        gh.write_text(
            "#!" + sys.executable + "\n"
            "import os\nfrom pathlib import Path\n"
            "print(Path(os.environ['GH_API_FIXTURE']).read_text())\n"
        )
        gh.chmod(0o755)
        response_file = target / "fixture-run.json"
        environment = dict(
            os.environ, PATH=str(command_directory) + os.pathsep + os.environ["PATH"],
            GH_API_FIXTURE=str(response_file), RUNNER_TEMP=str(target),
            GITHUB_REPOSITORY="fixture/project", GITHUB_SHA="a" * 40,
            PREREQUISITE_RUN_ID="123", GH_TOKEN="",
        )
        expected = {
            "head_sha": "a" * 40, "status": "completed", "conclusion": "success",
            "event": "push", "path": ".github/workflows/backbone-pr-checks.yml",
        }
        for relative in KIT_FILES[-2:]:
            script = yaml.safe_load((target / relative).read_text())["jobs"]["prerequisites"]["steps"][1]["run"]
            for replacements in (
                {}, {"head_sha": "b" * 40}, {"status": "in_progress"},
                {"conclusion": "failure"}, {"event": "pull_request"},
                {"path": ".github/workflows/unrelated.yml"},
            ):
                with self.subTest(example=relative, replacements=replacements):
                    response_file.write_text(json.dumps(dict(expected, **replacements)))
                    result = subprocess.run(
                        ["bash", "-c", script], cwd=target, env=environment,
                        text=True, capture_output=True,
                    )
                    self.assertEqual(result.returncode == 0, not replacements,
                                     result.stdout + result.stderr)
                    if replacements:
                        self.assertIn("BLOCKED", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
