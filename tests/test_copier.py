"""Real template copy/update and existing-governance preservation checks."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

from copier import run_copy, run_update
import yaml


ROOT = Path(__file__).resolve().parents[1]


def git(path, *arguments):
    result = subprocess.run(
        ["git", *arguments], cwd=path, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def initialize(path):
    git(path, "-c", "init.defaultBranch=main", "init")
    git(path, "config", "user.email", "backbone-tests@example.invalid")
    git(path, "config", "user.name", "Backbone test fixture")


def commit(path, message):
    git(path, "add", ".")
    git(path, "commit", "-m", message)


class CopierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="backbone-copier-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.source = self.workspace / "source"
        shutil.copytree(
            ROOT,
            self.source,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "artifacts", ".venv"),
        )
        initialize(self.source)
        commit(self.source, "Template fixture v0.1.0")
        git(self.source, "tag", "v0.1.0")

    def copy(self, **data):
        target = self.workspace / f"consumer-{len(list(self.workspace.glob('consumer-*')))}"
        run_copy(
            str(self.source),
            target,
            data=data,
            vcs_ref="v0.1.0",
            defaults=True,
            quiet=True,
            skip_tasks=True,
        )
        return target

    def validation_result(self, target):
        return subprocess.run(
            [sys.executable, str(target / ".engineering-backbone/validate.py"), "--root", str(target)],
            cwd=target,
            env=os.environ.copy(),
            text=True,
            capture_output=True,
        )

    def validate(self, target):
        result = self.validation_result(target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_python_cli_and_typescript_frontend_have_native_profiles(self):
        for name, language, frontend, command in (
            ("example-cli", "Python", False, "python -m unittest discover -s tests -v"),
            ("example-web", "TypeScript", True, "npm run lint && npm test"),
        ):
            with self.subTest(project=name):
                target = self.copy(
                    project_name=name,
                    language=language,
                    has_frontend=frontend,
                    has_backend=False,
                    validation_command=command,
                )
                facts = json.loads((target / ".engineering-backbone/project.json").read_text())
                self.assertEqual(facts["project"]["name"], name)
                self.assertEqual(facts["project"]["language"], language)
                self.assertEqual(facts["project"]["has_frontend"], frontend)
                self.assertFalse(facts["project"]["has_backend"])
                self.assertEqual(facts["project"]["validation_command"], command)
                self.assertEqual(facts["agents"], {"codex": True, "copilot": True})
                for role in ("planner", "implementer", "reviewer"):
                    native = target / f".codex/agents/backbone-{role}.toml"
                    data = tomllib.loads(native.read_text())
                    self.assertEqual(data["name"], f"backbone_{role}")
                    expected_mode = "workspace-write" if role == "implementer" else "read-only"
                    self.assertEqual(data["sandbox_mode"], expected_mode)
                    self.assertNotIn("model", data)
                    self.assertNotIn("model_reasoning_effort", data)
                    copilot = target / f".github/agents/backbone-{role}.agent.md"
                    header = yaml.safe_load(copilot.read_text().split("---", 2)[1])
                    expected_tools = ["read", "search", "edit", "execute"] if role == "implementer" else ["read", "search"]
                    self.assertEqual(header["tools"], expected_tools)
                self.assertEqual(
                    (target / ".engineering-backbone/core.md").read_text().strip(),
                    (self.source / "policy/core.md").read_text().strip(),
                )
                self.assertEqual(
                    (target / ".engineering-backbone/requirements.lock").read_bytes(),
                    (self.source / "requirements.lock").read_bytes(),
                )
                self.assertFalse((target / "_partials").exists())
                self.assertFalse((target / ".github/workflows/engineering-backbone.yml").exists())
                self.validate(target)

    def test_both_adapters_can_be_disabled(self):
        target = self.copy(use_codex=False, use_copilot=False)
        self.assertFalse((target / "AGENTS.md").exists())
        self.assertFalse((target / ".codex").exists())
        self.assertFalse((target / ".github").exists())
        for name in ("AGENTS.fragment.md", "Copilot.fragment.md"):
            self.assertTrue((target / ".engineering-backbone" / name).is_file())
        self.validate(target)

    def test_existing_native_governance_config_and_facts_are_preserved(self):
        target = self.workspace / "existing"
        target.mkdir()
        preserved = {
            "AGENTS.md": "Existing stronger agent policy\n",
            "nested/AGENTS.md": "Nested stronger policy\n",
            ".github/copilot-instructions.md": "Existing stronger Copilot policy\n",
            ".codex/config.toml": "# Existing local runtime configuration\n",
            ".codex/agents/backbone-reviewer.toml": "# Existing reviewer configuration\n",
            ".codex/agents/custom.toml": "# Custom role remains untouched\n",
            ".github/agents/backbone-reviewer.agent.md": "Existing custom reviewer\n",
            ".github/agents/custom.agent.md": "Existing additional role\n",
            ".github/workflows/engineering-backbone.yml": "# Existing project workflow\n",
            ".engineering-backbone/project.json": '{"existing": "project facts"}\n',
        }
        for relative, text in preserved.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        run_copy(str(self.source), target, vcs_ref="v0.1.0", defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        for relative, text in preserved.items():
            self.assertEqual((target / relative).read_text(), text, relative)
        self.assertTrue((target / ".engineering-backbone/AGENTS.fragment.md").is_file())
        self.assertTrue((target / ".engineering-backbone/Copilot.fragment.md").is_file())

    def test_pinned_update_refreshes_core_and_fragments_preserving_local_files(self):
        target = self.copy(project_name="upgrade-example")
        initialize(target)
        protected = (
            "AGENTS.md",
            ".github/copilot-instructions.md",
            ".codex/agents/backbone-reviewer.toml",
            ".github/agents/backbone-reviewer.agent.md",
            ".engineering-backbone/project.json",
        )
        for relative in protected[:-1]:
            with (target / relative).open("a") as stream:
                stream.write("\n# Existing stricter local addition\n")
        original = {relative: (target / relative).read_bytes() for relative in protected}
        (target / "project-specific.md").write_text("Project-specific content remains.\n")
        commit(target, "Consumer with stricter local governance")
        with (self.source / "policy/core.md").open("a") as stream:
            stream.write("\nReviewed upgrade fixture: preserve local governance.\n")
        with (self.source / "templates/_partials/essential.md.jinja").open("a") as stream:
            stream.write("\nReviewed update fixture: verify downstream adoption.\n")
        core = json.loads((self.source / "policy/core.json").read_text())
        core["version"] = "0.2.0"
        (self.source / "policy/core.json").write_text(json.dumps(core, indent=2) + "\n")
        commit(self.source, "Reviewed template fixture v0.2.0")
        git(self.source, "tag", "v0.2.0")
        run_update(
            target,
            answers_file=".engineering-backbone/copier-answers.yml",
            vcs_ref="v0.2.0",
            defaults=True,
            quiet=True,
            skip_tasks=True,
            overwrite=True,
        )
        self.assertIn("Reviewed upgrade fixture", (target / ".engineering-backbone/core.md").read_text())
        self.assertEqual(json.loads((target / ".engineering-backbone/core.json").read_text())["version"], "0.2.0")
        for fragment in ("AGENTS.fragment.md", "Copilot.fragment.md"):
            self.assertIn("Reviewed update fixture", (target / ".engineering-backbone" / fragment).read_text())
        for relative, content in original.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assertEqual((target / "project-specific.md").read_text(), "Project-specific content remains.\n")
        answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertEqual(answers["_commit"], "v0.2.0")

    def test_json_quoting_and_invalid_answers(self):
        command = 'python -c "print(\'quoted value\')"'
        target = self.copy(validation_command=command, language='Python + "quoted metadata"')
        facts = json.loads((target / ".engineering-backbone/project.json").read_text())
        self.assertEqual(facts["project"]["validation_command"], command)
        self.assertEqual(facts["project"]["language"], 'Python + "quoted metadata"')
        for field, value in (
            ("project_name", "bad\nname"),
            ("base_branch", "../main"),
            ("base_branch", "bad\nbranch"),
            ("validation_command", "python\necho injected"),
            ("validation_command", " "),
            ("language", "Python\nInjected instructions"),
            ("backbone_workflow_ref", "main"),
        ):
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    self.copy(**{field: value})

    def test_optional_active_workflow_requires_exact_sha(self):
        ref = "a" * 40
        target = self.copy(backbone_workflow_ref=ref)
        workflow = target / ".github/workflows/engineering-backbone.yml"
        text = workflow.read_text()
        self.assertIn("governance-checks.yml@" + ref, text)
        self.assertNotIn("PIN_APPROVED_COMMIT", text)
        self.assertNotIn("secrets:", text)
        self.validate(target)

    def test_invalid_git_branches_reject_before_consumer_mutation(self):
        target = self.workspace / "existing-branch-target"
        target.mkdir()
        (target / "AGENTS.md").write_text("Existing stronger policy\n")
        before = {path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()}
        invalid = (
            "feature/.hidden", "release.lock/next", "x/a.lock.lock/z", "HEAD", "main\n",
            "/main", "main/", "main.", ".main", "feature//one", "feature/../main", "-main",
            "bad~name", "bad^name", "bad:name", "bad?name", "bad*name", "bad[name",
            "bad\\name", "bad@{name", "bad name", "bad\tname", "bad\x7fname",
        )
        for branch in invalid + ("bad\x00name",):
            with self.subTest(branch=repr(branch)):
                if "\x00" not in branch:
                    result = subprocess.run(["git", "check-ref-format", "--branch", branch], capture_output=True)
                    self.assertNotEqual(result.returncode, 0, repr(branch))
                with self.assertRaisesRegex(ValueError, "valid single-line Git branch"):
                    run_copy(str(self.source), target, data={"base_branch": branch}, vcs_ref="v0.1.0",
                             defaults=True, quiet=True, skip_tasks=True, overwrite=True)
                after = {path.relative_to(target): path.read_bytes() for path in target.rglob("*") if path.is_file()}
                self.assertEqual(before, after)

    def test_valid_nested_git_branches_generate_valid_consumers(self):
        for branch in ("main", "feature/frontend", "release/v1.0", "feature/a./next", "feature/a.lockx/next", "x/HEAD"):
            with self.subTest(branch=branch):
                git(self.source, "check-ref-format", "--branch", branch)
                target = self.copy(base_branch=branch)
                facts = json.loads((target / ".engineering-backbone/project.json").read_text())
                self.assertEqual(facts["project"]["base_branch"], branch)
                self.validate(target)

    def test_uppercase_workflow_sha_is_normalized_and_consumer_validates(self):
        ref = "ABCDEF0123456789" * 2 + "ABCDEF01"
        target = self.copy(backbone_workflow_ref=ref)
        workflow = (target / ".github/workflows/engineering-backbone.yml").read_text()
        self.assertIn("governance-checks.yml@" + ref.lower(), workflow)
        self.assertNotIn("governance-checks.yml@" + ref, workflow)
        self.validate(target)

    def test_conditional_selection_updates_reject_before_consumer_mutation(self):
        # Reproduce the supported HEAD update that previously deleted stricter
        # preexisting instructions even though they matched _skip_if_exists.
        # Start consumers on a pre-fix fixture with no immutable-choice guard.
        config_path = self.source / "copier.yml"
        fixed_config = config_path.read_text()
        legacy_config = yaml.safe_load(fixed_config)
        legacy_config.pop("_external_data")
        for field in ("use_codex", "use_copilot"):
            legacy_config[field].pop("validator")
        legacy_config["backbone_workflow_ref"]["validator"] = legacy_config[
            "backbone_workflow_ref"
        ]["validator"].split("{% set previous", 1)[0]
        config_path.write_text(yaml.safe_dump(legacy_config, sort_keys=False))
        commit(self.source, "Pre-fix template fixture v0.1.1")
        git(self.source, "tag", "v0.1.1")
        config_path.write_text(fixed_config)
        with (self.source / "policy/core.md").open("a") as stream:
            stream.write("\nReviewed fixture update.\n")
        commit(self.source, "Template fixture v0.2.0")
        git(self.source, "tag", "v0.2.0")
        cases = (
            ("use_codex", True, False),
            ("use_copilot", True, False),
            ("backbone_workflow_ref", "a" * 40, ""),
            ("use_codex", False, True),
            ("use_copilot", False, True),
            ("backbone_workflow_ref", "", "a" * 40),
        )
        for index, (field, initial, requested) in enumerate(cases):
            with self.subTest(field=field, initial=initial, requested=requested):
                target = self.workspace / f"existing-switch-{index}"
                target.mkdir()
                sentinels = {
                    "AGENTS.md": "Strict preexisting agent policy must remain.\n",
                    "nested/AGENTS.md": "Strict nested policy must remain.\n",
                    ".github/copilot-instructions.md": "Strict preexisting Copilot policy must remain.\n",
                    ".codex/agents/backbone-reviewer.toml": "# Strict existing Codex reviewer\n",
                    ".github/agents/backbone-reviewer.agent.md": "Strict existing Copilot reviewer\n",
                    ".github/workflows/engineering-backbone.yml": "# Existing protected workflow\n",
                }
                for relative, content in sentinels.items():
                    path = target / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                run_copy(
                    str(self.source), target, data={field: initial}, vcs_ref="v0.1.1",
                    defaults=True, quiet=True, skip_tasks=True, overwrite=True,
                )
                initialize(target)
                commit(target, "Consumer with strict preexisting governance")
                before = {
                    path.relative_to(target): path.read_bytes()
                    for path in target.rglob("*")
                    if path.is_file() and ".git" not in path.relative_to(target).parts
                }
                with self.assertRaisesRegex(ValueError, "installation-only"):
                    run_update(
                        target, answers_file=".engineering-backbone/copier-answers.yml",
                        vcs_ref="HEAD", data={field: requested}, defaults=True,
                        quiet=True, skip_tasks=True, overwrite=True,
                    )
                after = {
                    path.relative_to(target): path.read_bytes()
                    for path in target.rglob("*")
                    if path.is_file() and ".git" not in path.relative_to(target).parts
                }
                self.assertEqual(after, before)
                self.assertEqual(git(target, "status", "--porcelain"), "")
                for relative, content in sentinels.items():
                    self.assertEqual((target / relative).read_text(), content)

    def test_consumer_accepts_unrelated_app_content_and_stricter_native_permissions(self):
        target = self.copy()
        for relative, content in {
            "policy/core.json": '{"application": "unrelated business policy"}\n',
            "examples/api-response.json": '{"items": []}\n',
            "README.md": "[Site documentation](/docs)\n",
            "AGENTS.md": "Stricter local guidance with [project link](local-doc-not-managed.md).\n",
        }.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        reviewer = target / ".github/agents/backbone-reviewer.agent.md"
        reviewer.write_text(reviewer.read_text().replace("tools: [read, search]", "tools: [read]"))
        implementer = target / ".codex/agents/backbone-implementer.toml"
        implementer.write_text(implementer.read_text().replace('sandbox_mode = "workspace-write"', 'sandbox_mode = "read-only"'))
        self.validate(target)

    def test_consumer_rejects_managed_contract_and_reviewer_failures(self):
        cases = (
            (".engineering-backbone/README.md", "[Missing managed documentation](missing.md)\n", "broken local Markdown link"),
            (".engineering-backbone/tasks/invalid.json", '{"schema_version": "1", "scope": {}}\n', "required property"),
            (".github/agents/backbone-reviewer.agent.md", "---\nname: backbone-reviewer\ndescription: Unsafe reviewer\ntools: [edit]\n---\nReview.\n", "tools"),
        )
        for relative, content, expected in cases:
            with self.subTest(path=relative):
                target = self.copy()
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                result = self.validation_result(target)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_no_executable_template_hooks(self):
        config = yaml.safe_load((self.source / "copier.yml").read_text())
        self.assertNotIn("_tasks", config)
        self.assertNotIn("_migrations", config)
        self.assertNotIn("_jinja_extensions", config)


if __name__ == "__main__":
    unittest.main()
