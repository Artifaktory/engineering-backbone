"""Exercise shared Codex/Copilot contracts through real Copier installs/upgrades.

These are distribution and preservation checks, not evidence that a running
provider discovers the files or enforces the prose review contract.
"""

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

from copier import run_copy, run_update
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


ROOT = Path(__file__).resolve().parents[2]
ROLES = ("planner", "implementer", "reviewer")
COPY_IGNORE = shutil.ignore_patterns(".git", "__pycache__", "artifacts", ".venv")


def git(root, *arguments):
    result = subprocess.run(
        ["git", *arguments], cwd=root, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def initialize(root):
    git(root, "-c", "init.defaultBranch=main", "init")
    git(root, "config", "user.email", "consolidation-tests@example.invalid")
    git(root, "config", "user.name", "Consolidation fixture")


def commit(root, message):
    git(root, "add", ".")
    git(root, "commit", "-m", message)


def codex_profile(root, role):
    return tomllib.loads((root / f".codex/agents/backbone-{role}.toml").read_text())


def copilot_profile(root, role):
    text = (root / f".github/agents/backbone-{role}.agent.md").read_text()
    _, header, body = text.split("---", 2)
    return yaml.safe_load(header), body.strip()


class CodexConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_directory = tempfile.TemporaryDirectory(prefix="backbone-shared-contract-")
        cls.addClassCleanup(cls.source_directory.cleanup)
        cls.source = Path(cls.source_directory.name) / "source"
        shutil.copytree(ROOT, cls.source, ignore=COPY_IGNORE)
        initialize(cls.source)
        commit(cls.source, "Current shared governance fixture")
        git(cls.source, "tag", "v0.2.0")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="backbone-consolidation-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)

    def copy(self, **data):
        target = self.workspace / f"consumer-{len(list(self.workspace.glob('consumer-*')))}"
        run_copy(
            str(self.source), target, data=data, vcs_ref="v0.2.0",
            defaults=True, quiet=True, skip_tasks=True,
        )
        return target

    def validate(self, target, *, trusted_base=None):
        command = [sys.executable, str(target / ".engineering-backbone/validate.py"), "--root", str(target)]
        if trusted_base is not None:
            command.extend(["--trusted-base", str(trusted_base)])
        result = subprocess.run(command, cwd=target, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_reviewer_contract(self, text):
        text = " ".join(text.split())
        for clause in (
            "prior reviewed head, repaired head and confirmed IDs",
            "current-diff causation",
            "report inspected and unreviewed areas",
            "default two-Full-round limit",
            "Remote review is advisory without a separately approved formal project contract",
            "Provider automatic fixes cannot bypass triage or local gates",
        ):
            self.assertIn(clause, text)

    def assert_copilot_reviewer_contract(self, text):
        text = " ".join(text.split())
        for clause in (
            "Start a separate independent review session",
            "fixed base/head, patch digest",
            "current-diff causation",
            "Report coverage and unreviewed areas",
            "prior reviewed head, repaired head and confirmed IDs",
            "default maximum is two Full rounds",
            "Provider automation stays advisory and cannot bypass triage",
        ):
            self.assertIn(clause, text)

    def assert_shared_fragments(self, target):
        for fragment in ("AGENTS.fragment.md", "Copilot.fragment.md"):
            text = " ".join((target / ".engineering-backbone" / fragment).read_text().split())
            for clause in (
                "prior reviewed head, repaired head and confirmed IDs",
                "diff causation",
                "Report coverage and unreviewed areas",
                "Default to at most two Full rounds",
                "Remote reviews remain advisory without a separately approved formal project contract",
                "Preserve installed local Publish-Go, signatures and history gates",
            ):
                self.assertIn(clause, text, fragment)

    def test_source_and_generated_provider_roles_share_the_rendered_contract(self):
        target = self.copy()
        environment = Environment(
            loader=FileSystemLoader(self.source), undefined=StrictUndefined,
            keep_trailing_newline=True,
        )
        for role in ROLES:
            with self.subTest(role=role):
                partial = environment.get_template(f".engineering-backbone/legacy/templates/_partials/{role}.md.jinja")
                source_body = partial.render(policy_path="docs/agent-governance/core.md").strip()
                consumer_body = partial.render(policy_path=".engineering-backbone/core.md").strip()
                self.assertEqual(source_body.replace("docs/agent-governance/core.md", ".engineering-backbone/core.md"), consumer_body)
                for root, expected in ((self.source, source_body), (target, consumer_body)):
                    codex = codex_profile(root, role)
                    copilot, copilot_body = copilot_profile(root, role)
                    self.assertEqual(codex["developer_instructions"].strip(), expected)
                    # Copilot has native procedural roles, with unchanged tool
                    # budgets; Codex continues to use the shared baseline body.
                    copilot_partial = environment.get_template(f".engineering-backbone/legacy/templates/_partials/copilot/{role}.md.jinja")
                    copilot_expected = copilot_partial.render(
                        core_link="../../docs/agent-governance/core.md" if root == self.source else "../../.engineering-backbone/core.md",
                        guide_link="../../docs/agent-governance/adapters/copilot/workflow.md" if root == self.source else "../../.engineering-backbone/copilot-guide.md",
                    ).strip()
                    self.assertEqual(copilot_body, copilot_expected)
                    self.assertEqual(set(codex), {"name", "description", "sandbox_mode", "developer_instructions"})
                    mode = "workspace-write" if role == "implementer" else "read-only"
                    tools = ["read", "search", "edit", "execute"] if role == "implementer" else ["read", "search"]
                    self.assertEqual(codex["sandbox_mode"], mode)
                    self.assertEqual(copilot["tools"], tools)
                if role == "reviewer":
                    self.assert_reviewer_contract(consumer_body)
        self.validate(target)

    def test_fresh_cli_and_frontend_keep_project_facts_without_source_runtime_settings(self):
        for name, language, frontend, branch, command in (
            ("portable-cli", "Python", False, "integration/cli", "python -m unittest discover"),
            ("portable-web", "TypeScript", True, "integration/web", "npm run lint && npm test"),
        ):
            with self.subTest(project=name):
                target = self.copy(
                    project_name=name, language=language, has_frontend=frontend,
                    has_backend=False, base_branch=branch, validation_command=command,
                )
                facts = json.loads((target / ".engineering-backbone/project.json").read_text())
                self.assertEqual(facts["project"], {
                    "name": name, "language": language, "has_frontend": frontend,
                    "has_backend": False, "base_branch": branch, "validation_command": command,
                })
                self.assertEqual(
                    (target / ".engineering-backbone/core.md").read_bytes().strip(),
                    (self.source / "docs/agent-governance/core.md").read_bytes().strip().replace(b"(../quality/policy.md)", b"(quality-policy.md)"),
                )
                self.assert_shared_fragments(target)
                self.assert_reviewer_contract(codex_profile(target, "reviewer")["developer_instructions"])
                paths = [target / "AGENTS.md", target / ".github/copilot-instructions.md"]
                paths += list((target / ".codex/agents").glob("*.toml"))
                paths += list((target / ".github/agents").glob("*.agent.md"))
                paths += [target / ".engineering-backbone" / name for name in (
                    "core.md", "AGENTS.fragment.md", "Copilot.fragment.md",
                )]
                for path in paths:
                    self.assertNotRegex(
                        path.read_text(),
                        re.compile(r"\b(?:Tars|Artifaktory|Binary-Refinery|AO)\b|feature/frontend|\bstaging\b|pc[12]-build", re.I),
                        str(path.relative_to(target)),
                    )
                self.assertFalse((target / ".codex/config.toml").exists())
                self.assertFalse((target / ".github/workflows/engineering-backbone.yml").exists())
                self.validate(target)

    def test_providers_are_independently_selectable_with_shared_fragments_always_available(self):
        for codex in (False, True):
            for copilot in (False, True):
                with self.subTest(codex=codex, copilot=copilot):
                    target = self.copy(use_codex=codex, use_copilot=copilot)
                    facts = json.loads((target / ".engineering-backbone/project.json").read_text())
                    self.assertEqual(facts["agents"], {"codex": codex, "copilot": copilot})
                    self.assertEqual((target / "AGENTS.md").exists(), codex)
                    self.assertEqual((target / ".github/copilot-instructions.md").exists(), copilot)
                    for role in ROLES:
                        self.assertEqual((target / f".codex/agents/backbone-{role}.toml").exists(), codex)
                        self.assertEqual((target / f".github/agents/backbone-{role}.agent.md").exists(), copilot)
                    if codex:
                        self.assert_reviewer_contract(codex_profile(target, "reviewer")["developer_instructions"])
                    if copilot:
                        self.assert_copilot_reviewer_contract(copilot_profile(target, "reviewer")[1])
                    self.assert_shared_fragments(target)
                    self.validate(target)

    def test_historical_upgrade_refreshes_shared_contract_without_replacing_native_authority(self):
        # The baseline is reconstructed from committed fixtures, not old Git
        # objects; it remains usable after the backbone's history is squashed.
        fixtures = self.source / ".engineering-backbone/tst/fixtures/historical"
        manifest = json.loads((fixtures / "manifest.json").read_text())
        self.assertEqual(manifest["baseline"], "bootstrap")
        source = self.workspace / "upgrade-source"
        shutil.copytree(fixtures / "bootstrap", source)
        expected_blobs = manifest["versions"]["bootstrap"]["files"]
        actual_paths = {path.relative_to(source).as_posix(): path for path in source.rglob("*") if path.is_file()}
        self.assertEqual(set(actual_paths), set(expected_blobs))
        for relative, path in actual_paths.items():
            content = path.read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
            self.assertEqual(digest, expected_blobs[relative], relative)
        initialize(source)
        commit(source, "Immutable bootstrap inputs")
        git(source, "tag", "v0.1.0")
        target = self.workspace / "upgraded-project"
        run_copy(
            str(source), target, vcs_ref="v0.1.0", data={
                "project_name": "existing-web", "language": "TypeScript",
                "has_frontend": True, "has_backend": False,
                "base_branch": "integration/local", "validation_command": "npm test",
                "backbone_workflow_ref": "a" * 40,
            }, defaults=True, quiet=True, skip_tasks=True,
        )
        initialize(target)
        native = {
            "AGENTS.md": "# Local authority\nRequire human Publish-Go and a signed local review before publication.\n",
            "frontend/AGENTS.md": "# Frontend authority\nKeep the local accessibility gate.\n",
            ".github/copilot-instructions.md": "# Local Copilot authority\nNever bypass the local signed-review gate.\n",
            ".codex/config.toml": "# Local provider runtime configuration\n",
            ".codex/agents/local-security.toml": '# Additional project-native role\nname = "local_security"\n',
            ".github/agents/local-security.agent.md": "Additional local reviewer; never remove.\n",
            ".github/workflows/engineering-backbone.yml": (
                (target / ".github/workflows/engineering-backbone.yml").read_text()
                + "\n# Existing workflow remains separately reviewed.\n"
            ),
            "project-specific.md": "Local architecture and operating decisions remain.\n",
        }
        for role in ROLES:
            data = codex_profile(target, role)
            data["developer_instructions"] += "\nLocal signed-review and Publish-Go gates are mandatory.\n"
            # A local implementer may deliberately have stricter permissions.
            data["sandbox_mode"] = "read-only"
            native[f".codex/agents/backbone-{role}.toml"] = "\n".join(
                f"{key} = {json.dumps(value)}" for key, value in data.items()
            ) + "\n"
            header, body = copilot_profile(target, role)
            header["tools"] = ["read"]
            native[f".github/agents/backbone-{role}.agent.md"] = (
                "---\n" + yaml.safe_dump(header, sort_keys=False) + "---\n\n"
                + body + "\nLocal signed-review and Publish-Go gates are mandatory.\n"
            )
        for relative, content in native.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        facts_path = target / ".engineering-backbone/project.json"
        facts = json.loads(facts_path.read_text())
        facts["project"]["validation_command"] = "npm run local-gated-checks"
        facts_path.write_text(json.dumps(facts, indent=2) + "\n")
        protected = {relative: (target / relative).read_bytes() for relative in native}
        protected[".engineering-backbone/project.json"] = facts_path.read_bytes()
        previous_core = (target / ".engineering-backbone/core.md").read_bytes()
        previous_fragments = {
            name: (target / ".engineering-backbone" / name).read_bytes()
            for name in ("AGENTS.fragment.md", "Copilot.fragment.md")
        }
        commit(target, "Stricter local instructions and runtime facts")
        trusted_base = self.workspace / "previous-consumer"
        shutil.copytree(target, trusted_base, ignore=COPY_IGNORE)
        shutil.copytree(self.source, source, dirs_exist_ok=True, ignore=COPY_IGNORE)
        commit(source, "Current shared contract update")
        git(source, "tag", "v0.2.0")
        run_update(
            target, answers_file=".engineering-backbone/copier-answers.yml",
            vcs_ref="v0.2.0", defaults=True, quiet=True, skip_tasks=True, overwrite=True,
        )
        self.assertNotEqual((target / ".engineering-backbone/core.md").read_bytes(), previous_core)
        self.assertEqual(
            (target / ".engineering-backbone/core.md").read_bytes().strip(),
            (self.source / "docs/agent-governance/core.md").read_bytes().strip().replace(b"(../quality/policy.md)", b"(quality-policy.md)"),
        )
        self.assert_shared_fragments(target)
        for name, old_content in previous_fragments.items():
            self.assertNotEqual((target / ".engineering-backbone" / name).read_bytes(), old_content, name)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertEqual(answers["_commit"], "v0.2.0")
        self.assertFalse(list(target.rglob("*.rej")))
        self.validate(target, trusted_base=trusted_base)


if __name__ == "__main__":
    unittest.main()
