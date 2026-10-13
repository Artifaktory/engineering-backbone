"""Real optional quality-framework creation, protected updates and role context.

These fixtures prove rendered contracts and bounded upgrade behavior. They do not
claim provider loading, semantic quality review or external certification.
"""

import json
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
PROFILE = ".engineering-backbone/quality-profile.json"
DOCUMENTS = (
    "docs/quality/quality-plan.md", "docs/quality/test-strategy.md",
    "docs/quality/traceability.csv", "docs/quality/exceptions.md",
)
PROFILES = (
    "baseline", "software", "python", "typescript", "high-risk", "agentic",
    "cpp17", "iec61508", "iec62304",
)
MANAGED = (
    ".engineering-backbone/quality-guide.md",
    ".engineering-backbone/quality-profile.schema.json",
    ".engineering-backbone/quality-guard.py",
    ".engineering-backbone/standards/sources.json",
    ".engineering-backbone/standards/rules.json",
) + tuple(f".engineering-backbone/standards/profiles/{name}.json" for name in PROFILES)
SEED = {
    "schema_version": "1", "enabled": False, "catalog_version": "1.0.0",
    "backbone_ref": "", "profiles": ["baseline"],
    "documents": {
        "quality_plan": DOCUMENTS[0], "test_strategy": DOCUMENTS[1],
        "traceability": DOCUMENTS[2], "exceptions": DOCUMENTS[3],
    },
    "checks": [], "exceptions": [],
}
CSV_HEADER = "rule_id,requirement_id,risk,architecture,tests,check_ids,evidence,status\n"


def git(path, *arguments):
    return subprocess.run(
        ["git", *arguments], cwd=path, text=True, capture_output=True, check=True
    ).stdout.strip()


def initialize(path):
    git(path, "-c", "init.defaultBranch=main", "init")
    git(path, "config", "user.name", "Backbone quality fixture")
    git(path, "config", "user.email", "backbone-tests@example.invalid")


def commit(path, message):
    git(path, "add", ".")
    git(path, "commit", "-m", message)


def snapshot(path):
    return {
        item.relative_to(path): item.read_bytes()
        for item in path.rglob("*")
        if item.is_file() and ".git" not in item.relative_to(path).parts
    }


class QualityCopierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="backbone-quality-copier-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.source = self.workspace / "source"
        shutil.copytree(
            ROOT, self.source,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "artifacts", ".venv"),
        )
        initialize(self.source)
        commit(self.source, "Quality template fixture v0.1.0")
        git(self.source, "tag", "v0.1.0")
        self.counter = 0

    def copy(self, *, target=None, ref="v0.1.0", **data):
        if target is None:
            target = self.workspace / f"consumer-{self.counter}"
            self.counter += 1
        run_copy(
            str(self.source), target, data=data, vcs_ref=ref,
            defaults=True, quiet=True, overwrite=True, skip_tasks=True,
        )
        return target

    def upgrade_source(self):
        guide = self.source / "docs/quality/README.md"
        guide.write_text(guide.read_text() + "\nReviewed quality guide fixture update.\n")
        commit(self.source, "Quality template fixture v0.2.0")
        git(self.source, "tag", "v0.2.0")

    def update(self, target, **data):
        run_update(
            target, answers_file=".engineering-backbone/copier-answers.yml",
            vcs_ref="v0.2.0", data=data, defaults=True, quiet=True,
            overwrite=True, skip_tasks=True,
        )

    def guard(self, target):
        return subprocess.run(
            [sys.executable, "-I", str(target / ".engineering-backbone/quality-guard.py"),
             "validate", "--root", str(target)],
            cwd=target, text=True, capture_output=True,
        )

    def test_default_copy_has_no_quality_bundle_or_project_document_side_effect(self):
        target = self.copy(use_codex=False, use_copilot=False)
        for relative in (PROFILE,) + DOCUMENTS + MANAGED:
            self.assertFalse((target / relative).exists(), relative)
        self.assertFalse((target / "docs").exists())
        self.assertTrue((target / ".engineering-backbone/quality-policy.md").is_file())
        self.assertIn("(quality-policy.md)", (target / ".engineering-backbone/core.md").read_text())
        facts = json.loads((target / ".engineering-backbone/project.json").read_text())
        self.assertEqual(facts["schema_version"], "1")
        self.assertNotIn("quality", facts)
        answers = yaml.safe_load((target / ".engineering-backbone/copier-answers.yml").read_text())
        self.assertFalse(answers["use_quality_framework"])
        self.assertNotIn("[quality guide]", (target / ".engineering-backbone/README.md").read_text())

    def test_opt_in_copies_truthful_inactive_seed_catalog_guard_and_empty_mapping(self):
        target = self.copy(use_quality_framework=True, use_codex=False, use_copilot=False)
        for relative in (PROFILE,) + DOCUMENTS + MANAGED:
            self.assertTrue((target / relative).is_file(), relative)
        self.assertEqual(json.loads((target / PROFILE).read_text()), SEED)
        self.assertEqual((target / DOCUMENTS[2]).read_text(), CSV_HEADER)
        for relative in ("sources.json", "rules.json"):
            self.assertEqual(
                json.loads((target / ".engineering-backbone/standards" / relative).read_text()),
                json.loads((self.source / "standards" / relative).read_text()),
            )
        for name in PROFILES:
            self.assertEqual(
                json.loads((target / f".engineering-backbone/standards/profiles/{name}.json").read_text()),
                json.loads((self.source / f"standards/profiles/{name}.json").read_text()),
            )
        self.assertEqual(
            (target / ".engineering-backbone/quality-guard.py").read_text().strip(),
            (self.source / "scripts/quality_framework.py").read_text().strip(),
        )
        self.assertEqual(
            (target / ".engineering-backbone/quality-profile.schema.json").read_text().strip(),
            (self.source / "schemas/quality-profile.schema.json").read_text().strip(),
        )
        result = self.guard(target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((target / ".github").exists())
        self.assertFalse((target / ".engineering-backbone/workflows.json").exists())
        self.assertIn("incomplete installation seed", (target / DOCUMENTS[1]).read_text())

    def test_quality_selection_is_independent_of_provider_choices_and_keeps_role_context(self):
        for codex, copilot in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(codex=codex, copilot=copilot):
                target = self.copy(use_quality_framework=True, use_codex=codex, use_copilot=copilot)
                self.assertTrue((target / PROFILE).is_file())
                self.assertEqual((target / ".codex").exists(), codex)
                self.assertEqual((target / ".github").exists(), copilot)
                if codex:
                    for name, sandbox in (("planner", "read-only"), ("implementer", "workspace-write"), ("reviewer", "read-only")):
                        data = tomllib.loads((target / f".codex/agents/backbone-{name}.toml").read_text())
                        self.assertEqual(data["name"], "backbone_" + name)
                        self.assertEqual(data["sandbox_mode"], sandbox)
                        self.assertEqual(set(data), {"name", "description", "sandbox_mode", "developer_instructions"})
                        text = data["developer_instructions"]
                        for expected in ("quality-profile.json", "catalog_version", "backbone_ref", "rule IDs", "Task Packet", "handoff"):
                            self.assertIn(expected, text)
                if copilot:
                    for relative in (
                        ".github/copilot-instructions.md",
                        ".github/agents/backbone-planner.agent.md",
                        ".github/agents/backbone-test-engineer.agent.md",
                        ".github/agents/backbone-reviewer.agent.md",
                        ".github/skills/task-intake/SKILL.md",
                        ".github/skills/test-and-quality/SKILL.md",
                        ".github/instructions/backbone-tests.instructions.md",
                    ):
                        text = (target / relative).read_text()
                        self.assertIn("quality-profile.json", text, relative)
                        self.assertIn("rule IDs", text, relative)

    def test_creation_and_upgrade_preserve_project_profile_docs_and_native_rules(self):
        target = self.workspace / "preserved"
        target.mkdir()
        profile = dict(SEED, profiles=["baseline", "agentic"])
        protected = {PROFILE: json.dumps(profile) + "\n"}
        protected.update({relative: "Existing stronger project quality record.\n" for relative in DOCUMENTS})
        protected[".github/agents/backbone-reviewer.agent.md"] = "Existing stricter independently signed reviewer.\n"
        protected[".github/skills/test-and-quality/SKILL.md"] = "Existing local test and evidence procedure.\n"
        protected["AGENTS.md"] = "Existing stronger project instructions.\n"
        for relative, text in protected.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.copy(target=target, use_quality_framework=True)
        initialize(target)
        commit(target, "Preserved project-owned quality records")
        self.upgrade_source()
        self.update(target)
        for relative, text in protected.items():
            self.assertEqual((target / relative).read_text(), text, relative)
        self.assertIn("Reviewed quality guide fixture update", (target / ".engineering-backbone/quality-guide.md").read_text())
        self.assertIn("Selected quality context", (target / ".engineering-backbone/AGENTS.fragment.md").read_text())

    def test_update_rejects_selection_changes_before_any_consumer_mutation(self):
        self.upgrade_source()
        for initial, requested in ((False, True), (True, False)):
            with self.subTest(initial=initial, requested=requested):
                target = self.copy(use_quality_framework=initial)
                initialize(target)
                commit(target, "Reviewed initial quality selection")
                before = snapshot(target)
                with self.assertRaisesRegex(ValueError, "installation-only"):
                    self.update(target, use_quality_framework=requested)
                self.assertEqual(snapshot(target), before)
                self.assertEqual(git(target, "status", "--porcelain"), "")

    def test_legacy_missing_choice_remains_disabled_and_rejects_auto_adoption(self):
        copier_path = self.source / "copier.yml"
        modern = copier_path.read_bytes()
        legacy = yaml.safe_load(modern)
        legacy.pop("use_quality_framework")
        legacy["_skip_if_exists"] = [
            item for item in legacy["_skip_if_exists"]
            if item != PROFILE and item not in DOCUMENTS
        ]
        optional_templates = {
            path.relative_to(self.source): path.read_bytes()
            for path in (self.source / "templates").rglob("*")
            if path.is_file() and "use_quality_framework" in str(path)
        }
        for relative in optional_templates:
            (self.source / relative).unlink()
        readme_path = self.source / "templates/.engineering-backbone/README.md.jinja"
        modern_readme = readme_path.read_bytes()
        # The historical fixture has neither the option nor its conditional guide.
        text = modern_readme.decode()
        start = text.index("The optional `use_quality_framework` choice")
        readme_path.write_text(text[:start])
        copier_path.write_text(yaml.safe_dump(legacy, sort_keys=False))
        commit(self.source, "Legacy fixture with no quality selection")
        git(self.source, "tag", "v0.0.0")
        copier_path.write_bytes(modern)
        readme_path.write_bytes(modern_readme)
        for relative, content in optional_templates.items():
            (self.source / relative).write_bytes(content)
        self.upgrade_source()
        for requested in ({}, {"use_quality_framework": True}):
            with self.subTest(requested=requested):
                target = self.copy(ref="v0.0.0")
                answers_path = target / ".engineering-backbone/copier-answers.yml"
                self.assertNotIn("use_quality_framework", yaml.safe_load(answers_path.read_text()))
                initialize(target)
                commit(target, "Legacy consumer without quality framework")
                before = snapshot(target)
                if requested:
                    with self.assertRaisesRegex(ValueError, "installation-only"):
                        self.update(target, **requested)
                    self.assertEqual(snapshot(target), before)
                else:
                    self.update(target)
                    self.assertFalse(yaml.safe_load(answers_path.read_text())["use_quality_framework"])
                for relative in (PROFILE,) + DOCUMENTS + MANAGED:
                    self.assertFalse((target / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
