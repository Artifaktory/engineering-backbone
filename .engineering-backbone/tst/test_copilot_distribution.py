"""Real Copier distribution/upgrade checks for the Copilot-native package.

These exercise rendered files and safe installation behavior. They do not prove
that a live Copilot client discovers profiles, obeys instructions or runs tools.
"""
from __future__ import annotations

import glob
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy, run_update
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


ROOT = Path(__file__).resolve().parents[2]
COPY_IGNORE = shutil.ignore_patterns(".git", "__pycache__", "artifacts", ".venv")
ORIGINAL_ROLES = ("planner", "implementer", "reviewer")
COPILOT_ROLES = (
    "analyst", "planner", "plan-reviewer", "implementer", "test-engineer",
    "quality-checker", "reviewer", "security-reviewer", "documentation", "finding-triage",
)
SKILLS = (
    "task-intake", "implementation-plan", "bug-reproduction", "test-and-quality",
    "code-review", "finding-triage", "delta-review", "docs-traceability",
)
CORE_RULES = ("governance", "tests", "docs")
PROFILE_CHOICES = ("copilot_python_profile", "copilot_frontend_profile")


def git(root, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=root, text=True, capture_output=True, check=True,
    ).stdout.strip()


def initialize(root):
    git(root, "-c", "init.defaultBranch=main", "init")
    git(root, "config", "user.email", "copilot-distribution@example.invalid")
    git(root, "config", "user.name", "Copilot distribution fixture")


def commit(root, message):
    git(root, "add", ".")
    git(root, "commit", "-m", message)


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def native_document(path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
    if match is None:
        raise AssertionError(f"Missing native frontmatter: {path}")
    return yaml.safe_load(match.group(1)), content[match.end():].strip()


def historical_source(destination):
    """Reconstruct the reviewed three-role source from pinned fixture blobs."""
    fixtures = ROOT / ".engineering-backbone/tst/fixtures/historical"
    manifest = json.loads((fixtures / "manifest.json").read_text())
    if manifest["format"] != "engineering-backbone-historical-source-v1":
        raise ValueError("Unknown historical fixture format")
    version = "attested-review"
    record = manifest["versions"][version]
    if record["source_tree"] != "2727bd2a2c0f7a10bca749165f29a9a50021343b":
        raise ValueError("Historical fixture provenance mismatch")
    shutil.copytree(fixtures / manifest["baseline"], destination, symlinks=True)
    shutil.copytree(fixtures / version, destination, dirs_exist_ok=True, symlinks=True)
    paths = {path.relative_to(destination).as_posix(): path for path in destination.rglob("*") if path.is_file()}
    if set(paths) != set(record["files"]):
        raise ValueError("Historical source file set differs from pinned fixture")
    for relative, path in paths.items():
        content = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        if path.is_symlink() or digest != record["files"][relative]:
            raise ValueError("Historical fixture content mismatch: " + relative)


class CopilotDistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_directory = tempfile.TemporaryDirectory(prefix="copilot-native-source-")
        cls.addClassCleanup(cls.source_directory.cleanup)
        cls.source = Path(cls.source_directory.name) / "source"
        shutil.copytree(ROOT, cls.source, ignore=COPY_IGNORE)
        initialize(cls.source)
        commit(cls.source, "Current Copilot package fixture")
        git(cls.source, "tag", "v0.2.0")
        # The CLI mode is deliberately fixed by trusted bundle location. Make
        # an independent current consumer bundle rather than adding a mode flag
        # or executing an older/candidate-supplied validator.
        cls.validator_bundle = Path(cls.source_directory.name) / "trusted-tooling/.engineering-backbone"
        cls.validator_bundle.mkdir(parents=True)
        shutil.copy2(cls.source / ".engineering-backbone/src/validate.py", cls.validator_bundle / "validate.py")
        shutil.copytree(cls.source / ".engineering-backbone/schemas", cls.validator_bundle / "schemas")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="copilot-distribution-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)

    def copy(self, **data):
        target = self.workspace / f"consumer-{len(list(self.workspace.glob('consumer-*')))}"
        run_copy(str(self.source), target, data=data, vcs_ref="v0.2.0",
                 defaults=True, quiet=True, skip_tasks=True)
        return target

    def validate(self, target, *, trusted_base=None):
        # Invoke trusted current code, never candidate-supplied executable code.
        command = [sys.executable, str(self.validator_bundle / "validate.py"), "--root", str(target)]
        if trusted_base is not None:
            command.extend(["--trusted-base", str(trusted_base)])
        result = subprocess.run(command, cwd=self.workspace, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_package(self, target, *, codex, copilot, python=False, frontend=False):
        facts = json.loads((target / ".engineering-backbone/project.json").read_text())
        self.assertEqual(facts["agents"], {"codex": codex, "copilot": copilot})
        codex_files = {path.name for path in (target / ".codex/agents").glob("*.toml")}
        self.assertEqual(codex_files, {f"backbone-{role}.toml" for role in ORIGINAL_ROLES} if codex else set())
        roles = {path.name for path in (target / ".github/agents").glob("*.agent.md")}
        self.assertEqual(roles, {f"backbone-{role}.agent.md" for role in COPILOT_ROLES} if copilot else set())
        skills = {path.parent.name for path in (target / ".github/skills").glob("*/SKILL.md")}
        self.assertEqual(skills, set(SKILLS) if copilot else set())
        selected_rules = set(CORE_RULES)
        if python:
            selected_rules.add("python")
        if frontend:
            selected_rules.add("frontend")
        rules = {path.name for path in (target / ".github/instructions").glob("*.instructions.md")}
        self.assertEqual(rules, {f"backbone-{rule}.instructions.md" for rule in selected_rules} if copilot else set())
        self.assertEqual((target / "AGENTS.md").exists(), codex)
        self.assertEqual((target / ".github/copilot-instructions.md").exists(), copilot)
        guide = target / ".engineering-backbone/copilot-guide.md"
        self.assertTrue(guide.is_file(), "Neutral integration guide must survive disabled providers")
        self.assertIn("```mermaid", guide.read_text())
        for fragment in ("AGENTS.fragment.md", "Copilot.fragment.md"):
            self.assertTrue((target / ".engineering-backbone" / fragment).is_file())
        self.assertFalse((target / "_partials").exists())
        self.assertFalse(list(target.rglob("*.jinja")))

    def test_fresh_provider_and_profile_matrix_is_explicit_and_link_valid(self):
        # Every provider combination and every optional-profile combination;
        # descriptive language/frontend facts deliberately do not select rules.
        for codex, copilot, python, frontend in itertools.product((False, True), repeat=4):
            with self.subTest(codex=codex, copilot=copilot, python=python, frontend=frontend):
                target = self.copy(
                    use_codex=codex, use_copilot=copilot,
                    copilot_python_profile=python, copilot_frontend_profile=frontend,
                    language="Python + TypeScript", has_frontend=True,
                )
                self.assert_package(target, codex=codex, copilot=copilot, python=python, frontend=frontend)
                self.validate(target)

    def test_default_profiles_are_not_inferred_from_project_metadata(self):
        target = self.copy(language="Python + TypeScript", has_frontend=True, has_backend=True)
        answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertEqual({key: answers[key] for key in PROFILE_CHOICES}, {key: False for key in PROFILE_CHOICES})
        self.assert_package(target, codex=True, copilot=True)
        self.validate(target)

    def test_source_docs_rule_covers_nested_markdown_and_docs_data(self):
        header, _ = native_document(self.source / ".github/instructions/backbone-docs.instructions.md")
        expected = {
            "README.md",
            "apps/frontend/README.md",
            ".engineering-backbone/README.md",
            "docs/templates/examples/task-packet.json",
        }
        code_path = ".engineering-backbone/src/validate.py"
        optional_path = "apps/frontend/README.md"
        for relative in (expected - {optional_path}) | {code_path}:
            self.assertTrue((self.source / relative).is_file(), relative)
        selection_roots = [self.source]
        if not (self.source / optional_path).is_file():
            # Adopted projects can omit the frontend component. Keep its path
            # example in a separate fixture without restoring it in the repo.
            fixture_root = self.workspace / "docs-selection-fixture"
            fixture_path = fixture_root / optional_path
            fixture_path.parent.mkdir(parents=True)
            fixture_path.write_text("# Optional frontend documentation\n", encoding="utf-8")
            selection_roots.append(fixture_root)

        def selected_paths(selector):
            # Model slash-aware glob selection over real repository files;
            # this is not a native Copilot-host execution test.
            return {
                relative
                for root in selection_roots
                for pattern in selector.split(",")
                for relative in glob.glob(
                    pattern, root_dir=root, recursive=True, include_hidden=True,
                )
                if (root / relative).is_file()
            }

        old_selection = selected_paths("*.md,docs/**,plans/**")
        for relative in ("apps/frontend/README.md", ".engineering-backbone/README.md"):
            self.assertNotIn(relative, old_selection, "The previous selector missed nested Markdown")
        selection = selected_paths(header["applyTo"])
        self.assertTrue(expected <= selection, f"Docs selector misses: {sorted(expected - selection)}")
        self.assertNotIn(code_path, selection)

    def test_native_source_and_generated_bodies_share_copilot_partials(self):
        target = self.copy(copilot_python_profile=True, copilot_frontend_profile=True)
        environment = Environment(loader=FileSystemLoader(self.source), undefined=StrictUndefined,
                                  keep_trailing_newline=True)
        for kind, names, partial_name, directory, filename, prefix in (
            ("role", COPILOT_ROLES, "{name}.md.jinja", ".github/agents", "backbone-{name}.agent.md", "../../"),
            ("skill", SKILLS, "skill-{name}.md.jinja", ".github/skills/{name}", "SKILL.md", "../../../"),
            ("rule", CORE_RULES + ("python", "frontend"), "instruction-{name}.md.jinja", ".github/instructions", "backbone-{name}.instructions.md", "../../"),
        ):
            for name in names:
                with self.subTest(kind=kind, name=name):
                    partial = environment.get_template(".engineering-backbone/legacy/templates/_partials/copilot/" + partial_name.format(name=name))
                    relative = Path(directory.format(name=name)) / filename.format(name=name)
                    source_header, source_body = native_document(self.source / relative)
                    consumer_header, consumer_body = native_document(target / relative)
                    # Source/reference rules cover the new repository paths;
                    # legacy installations keep their reviewed existing globs.
                    # Role/skill metadata, including permissions, stays equal.
                    if kind == "rule" and name == "governance":
                        self.assertEqual(source_header, {"applyTo":
                            ".github/**,.codex/**,.opencode/**,.engineering-backbone/**,docs/agent-governance/**,docs/quality/**,copier.yml,opencode.json"})
                        self.assertEqual(consumer_header, {"applyTo":
                            ".github/**,.engineering-backbone/**,templates/**,scripts/validate.py,scripts/compile_toolchain_fingerprint.py,policy/**,schemas/**,copier.yml"})
                    elif kind == "rule" and name == "tests":
                        self.assertEqual(source_header, {"applyTo":
                            "tst/**,**/tst/**,tests/**,**/test_*.py,**/*.test.*,**/*.spec.*"})
                        self.assertEqual(consumer_header, {"applyTo":
                            "tests/**,**/test_*.py,**/*.test.*,**/*.spec.*"})
                    elif kind == "rule" and name == "docs":
                        self.assertEqual(source_header, {"applyTo": "*.md,**/*.md,docs/**"})
                        self.assertEqual(consumer_header, {"applyTo": "*.md,docs/**,plans/**"})
                    else:
                        self.assertEqual(source_header, consumer_header)
                    self.assertEqual(source_body, partial.render(
                        core_link=prefix + "docs/agent-governance/core.md", guide_link=prefix + "docs/agent-governance/adapters/copilot/workflow.md",
                    ).strip())
                    self.assertEqual(consumer_body, partial.render(
                        core_link=prefix + ".engineering-backbone/core.md",
                        guide_link=prefix + ".engineering-backbone/copilot-guide.md",
                    ).strip())
        self.validate(target)

    def test_creation_preserves_existing_native_skills_rules_and_profiles(self):
        target = self.workspace / "existing-project"
        native = {
            ".github/copilot-instructions.md": "Stricter signed-review project policy.\n",
            ".github/agents/backbone-reviewer.agent.md": "Project-owned reviewer; manual reconciliation required.\n",
            ".github/agents/local-performance.agent.md": "Local specialized profile.\n",
            ".github/skills/task-intake/SKILL.md": "Existing task intake procedure remains authoritative.\n",
            ".github/skills/local-performance/SKILL.md": "Local performance workflow.\n",
            ".github/instructions/backbone-governance.instructions.md": "Local signed review instructions.\n",
            ".github/instructions/backbone-python.instructions.md": "Project-specific Python rules.\n",
            ".github/instructions/local-rust.instructions.md": "Existing Rust instructions.\n",
        }
        for relative, content in native.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        before = snapshot(target)
        run_copy(str(self.source), target, data={"copilot_python_profile": True}, vcs_ref="v0.2.0",
                 defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        for relative, content in before.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assertTrue((target / ".github/agents/backbone-plan-reviewer.agent.md").is_file())
        self.assertTrue((target / ".engineering-backbone/copilot-guide.md").is_file())
        # Preserved incomplete local formats intentionally need review/migration;
        # file preservation must never falsely certify them as a valid adoption.

    def test_historical_upgrade_adds_package_without_replacing_local_authority(self):
        source = self.workspace / "upgrade-source"
        historical_source(source)
        initialize(source)
        commit(source, "Pinned historical three-role fixture")
        git(source, "tag", "v0.1.0")
        target = self.workspace / "upgraded-project"
        # Use Git transport for both tagged revisions, avoiding local object-copy optimization.
        source_url = "git+" + source.resolve().as_uri()
        run_copy(source_url, target, data={
            "project_name": "existing-client", "language": "Go", "has_frontend": False,
            "base_branch": "integration/local", "validation_command": "go test ./...",
            "backbone_workflow_ref": "a" * 40,
        }, vcs_ref="v0.1.0", defaults=True, quiet=True, skip_tasks=True)
        initial_answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertEqual(initial_answers["_src_path"], source_url)
        self.assertEqual(initial_answers["_commit"], "v0.1.0")
        self.assertEqual({path.name for path in (target / ".github/agents").glob("*.agent.md")},
                         {f"backbone-{role}.agent.md" for role in ORIGINAL_ROLES})
        self.assertFalse((target / ".github/skills").exists())
        self.validate(target)  # Complete old-three-role bundle remains supported.
        initialize(target)
        native = {
            "AGENTS.md": "Require local signed reviews and human Publish-Go.\n",
            ".github/copilot-instructions.md": "Require local signed reviews and human Publish-Go.\n",
            ".github/skills/local-performance/SKILL.md": "Local procedure and evidence format.\n",
            ".github/instructions/local-rust.instructions.md": "Project-owned Rust instructions.\n",
            ".codex/config.toml": "# Local runtime permissions are project-owned.\n",
        }
        for role in ORIGINAL_ROLES:
            relative = f".github/agents/backbone-{role}.agent.md"
            header, body = native_document(target / relative)
            header["tools"] = ["read"]
            native[relative] = "---\n" + yaml.safe_dump(header, sort_keys=False) + "---\n\n" + body + "\nLocal signed reviews are required.\n"
        for relative, content in native.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        facts_path = target / ".engineering-backbone/project.json"
        facts = json.loads(facts_path.read_text())
        facts["project"]["validation_command"] = "go test -race ./..."
        facts_path.write_text(json.dumps(facts, indent=2) + "\n")
        protected = {relative: (target / relative).read_bytes() for relative in native}
        for relative in (".engineering-backbone/project.json", ".github/workflows/engineering-backbone.yml"):
            protected[relative] = (target / relative).read_bytes()
        previous_fragment = (target / ".engineering-backbone/Copilot.fragment.md").read_bytes()
        commit(target, "Stronger local roles, policy, facts and workflow pin")
        trusted = self.workspace / "trusted-consumer"
        shutil.copytree(target, trusted, ignore=COPY_IGNORE)
        shutil.copytree(self.source, source, dirs_exist_ok=True, ignore=COPY_IGNORE)
        commit(source, "Current Copilot distribution fixture")
        git(source, "tag", "v0.2.0")
        # Missing legacy optional-profile answers mean false, including while
        # checking an attempted ordinary update before it can copy any file.
        before = snapshot(target)
        for key in PROFILE_CHOICES:
            with self.subTest(legacy_profile_change=key):
                with self.assertRaisesRegex(ValueError, "installation-only"):
                    run_update(target, answers_file=".engineering-backbone/copier-answers.yml",
                               vcs_ref="v0.2.0", data={key: True}, defaults=True,
                               quiet=True, skip_tasks=True, overwrite=True)
                self.assertEqual(snapshot(target), before)
        run_update(target, answers_file=".engineering-backbone/copier-answers.yml", vcs_ref="v0.2.0",
                   defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        for role in set(COPILOT_ROLES) - set(ORIGINAL_ROLES):
            self.assertTrue((target / f".github/agents/backbone-{role}.agent.md").is_file(), role)
        for skill in SKILLS:
            self.assertTrue((target / f".github/skills/{skill}/SKILL.md").is_file(), skill)
        self.assertNotEqual((target / ".engineering-backbone/Copilot.fragment.md").read_bytes(), previous_fragment)
        self.assertTrue((target / ".engineering-backbone/copilot-guide.md").is_file())
        answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertEqual(answers["_src_path"], source_url)
        self.assertEqual(answers["_commit"], "v0.2.0")
        self.assertEqual({key: answers[key] for key in PROFILE_CHOICES}, {key: False for key in PROFILE_CHOICES})
        self.assertEqual(answers["backbone_workflow_ref"], "a" * 40)
        self.assertFalse((target / ".github/instructions/backbone-python.instructions.md").exists())
        self.assertFalse((target / ".github/instructions/backbone-frontend.instructions.md").exists())
        self.assertFalse(list(target.rglob("*.rej")))
        self.validate(target, trusted_base=trusted)

    def test_extended_package_update_preserves_custom_native_assets_and_facts(self):
        source = self.workspace / "extended-upgrade-source"
        shutil.copytree(self.source, source, ignore=COPY_IGNORE)
        initialize(source)
        commit(source, "Extended package before update")
        git(source, "tag", "v0.2.0")
        target = self.workspace / "extended-local-project"
        run_copy(str(source), target, data={
            "copilot_python_profile": True, "copilot_frontend_profile": True,
            "backbone_workflow_ref": "a" * 40,
        }, vcs_ref="v0.2.0", defaults=True, quiet=True, skip_tasks=True)
        initialize(target)
        for relative in (
            ".github/copilot-instructions.md",
            ".github/skills/task-intake/SKILL.md",
            ".github/instructions/backbone-governance.instructions.md",
            ".github/instructions/backbone-python.instructions.md",
            ".github/instructions/backbone-frontend.instructions.md",
        ):
            with (target / relative).open("a") as stream:
                stream.write("\nProject-owned signed review evidence is mandatory.\n")
        reviewer = target / ".github/agents/backbone-security-reviewer.agent.md"
        header, body = native_document(reviewer)
        header["tools"] = ["read"]
        reviewer.write_text("---\n" + yaml.safe_dump(header, sort_keys=False) + "---\n\n" + body + "\n")
        facts_path = target / ".engineering-backbone/project.json"
        facts = json.loads(facts_path.read_text())
        facts["project"].update(name="local-project", language="Go", validation_command="go test -race ./...")
        facts_path.write_text(json.dumps(facts, indent=2) + "\n")
        protected = {
            relative: content for relative, content in snapshot(target).items()
            if relative.startswith((".github/", ".codex/"))
            or relative in ("AGENTS.md", ".engineering-backbone/project.json")
        }
        previous_guide = (target / ".engineering-backbone/copilot-guide.md").read_bytes()
        previous_fragment = (target / ".engineering-backbone/Copilot.fragment.md").read_bytes()
        commit(target, "Project-owned native procedure, path rules and permissions")
        trusted = self.workspace / "extended-trusted-consumer"
        shutil.copytree(target, trusted, ignore=COPY_IGNORE)
        for relative in ("docs/agent-governance/adapters/copilot/workflow.md", ".engineering-backbone/legacy/templates/.engineering-backbone/Copilot.fragment.md.jinja"):
            with (source / relative).open("a") as stream:
                stream.write("\nReviewed shared update fixture; integrate through a project PR.\n")
        # Native rule and skill bodies change upstream but must remain locally
        # owned: their refreshed recommendation is separate from auto-overwrite.
        for relative in (
            ".engineering-backbone/legacy/templates/_partials/copilot/skill-task-intake.md.jinja",
            ".engineering-backbone/legacy/templates/_partials/copilot/instruction-governance.md.jinja",
        ):
            with (source / relative).open("a") as stream:
                stream.write("\nReviewed upstream native-body update fixture.\n")
        commit(source, "Reviewed shared package update")
        git(source, "tag", "v0.3.0")
        run_update(target, answers_file=".engineering-backbone/copier-answers.yml", vcs_ref="v0.3.0",
                   defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        for relative, content in protected.items():
            self.assertEqual((target / relative).read_bytes(), content, relative)
        self.assertNotEqual((target / ".engineering-backbone/copilot-guide.md").read_bytes(), previous_guide)
        self.assertNotEqual((target / ".engineering-backbone/Copilot.fragment.md").read_bytes(), previous_fragment)
        self.assertFalse(list(target.rglob("*.rej")))
        self.validate(target, trusted_base=trusted)

    def test_ordinary_selection_changes_reject_before_any_mutation(self):
        # Both directions matter: enabling changes adoption scope, while disabling
        # formerly deleted native governance files even with skip_if_exists.
        for key in ("use_copilot",) + PROFILE_CHOICES:
            for initial in (False, True):
                with self.subTest(choice=key, initial=initial):
                    target = self.copy(**{key: initial})
                    initialize(target)
                    commit(target, "Installed choices and native governance")
                    before = snapshot(target)
                    with self.assertRaisesRegex(ValueError, "installation-only"):
                        run_update(target, answers_file=".engineering-backbone/copier-answers.yml",
                                   vcs_ref="v0.2.0", data={key: not initial}, defaults=True,
                                   quiet=True, skip_tasks=True, overwrite=True)
                    self.assertEqual(snapshot(target), before)
                    self.assertEqual(git(target, "status", "--porcelain"), "")

    def test_managed_guide_and_fragment_refresh_even_when_providers_disabled(self):
        source = self.workspace / "disabled-upgrade-source"
        shutil.copytree(self.source, source, ignore=COPY_IGNORE)
        initialize(source)
        commit(source, "Copilot guide before update")
        git(source, "tag", "v0.2.0")
        target = self.workspace / "disabled-providers"
        run_copy(str(source), target, data={"use_codex": False, "use_copilot": False},
                 vcs_ref="v0.2.0", defaults=True, quiet=True, skip_tasks=True)
        initialize(target)
        commit(target, "Disabled providers retain integration documentation")
        guide = target / ".engineering-backbone/copilot-guide.md"
        fragment = target / ".engineering-backbone/Copilot.fragment.md"
        previous_guide, previous_fragment = guide.read_bytes(), fragment.read_bytes()
        for relative in ("docs/agent-governance/adapters/copilot/workflow.md", ".engineering-backbone/legacy/templates/.engineering-backbone/Copilot.fragment.md.jinja"):
            with (source / relative).open("a") as stream:
                stream.write("\nReviewed integration-guide update fixture.\n")
        commit(source, "Updated neutral guide and fragment")
        git(source, "tag", "v0.3.0")
        run_update(target, answers_file=".engineering-backbone/copier-answers.yml", vcs_ref="v0.3.0",
                   defaults=True, quiet=True, skip_tasks=True, overwrite=True)
        self.assertNotEqual(guide.read_bytes(), previous_guide)
        self.assertNotEqual(fragment.read_bytes(), previous_fragment)
        self.assertIn("Reviewed integration-guide update fixture", guide.read_text())
        self.assertIn("Reviewed integration-guide update fixture", fragment.read_text())
        self.assert_package(target, codex=False, copilot=False)
        self.validate(target)


if __name__ == "__main__":
    unittest.main()
