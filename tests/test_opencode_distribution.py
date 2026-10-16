"""Real optional Copier install/update checks; these do not prove native loading."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from copier import run_copy, run_update
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml

from tests.test_copilot_distribution import (
    ROOT, COPY_IGNORE, SKILLS, commit, git, historical_source, initialize,
    native_document, snapshot,
)

ROLES = {'planner': 'planner', 'implementer': 'implementer', 'reviewer': 'reviewer',
         'quality-checker': 'quality-checker', 'triage': 'finding-triage'}
ASSETS = ('opencode.json', '.opencode', '.engineering-backbone/opencode.json',
          '.engineering-backbone/opencode-guide.md', '.engineering-backbone/opencode-runner-contract.md',
          '.engineering-backbone/opencode.fragment.json', '.engineering-backbone/opencode.schema.json')


class OpenCodeDistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix='opencode-distribution-source-')
        cls.addClassCleanup(temporary.cleanup)
        cls.source = Path(temporary.name) / 'source'
        shutil.copytree(ROOT, cls.source, ignore=COPY_IGNORE)
        initialize(cls.source)
        commit(cls.source, 'OpenCode distribution fixture')
        git(cls.source, 'tag', 'v0.2.0')

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='opencode-consumer-')
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.counter = 0

    def copy(self, *, target=None, **data):
        if target is None:
            target = self.workspace / str(self.counter)
            self.counter += 1
        run_copy(str(self.source), target, data=data, vcs_ref='v0.2.0', defaults=True,
                 quiet=True, skip_tasks=True)
        return target

    def test_optional_matrix_keeps_exact_project_schema_and_inactive_seed(self):
        for codex, copilot, opencode in itertools.product((False, True), repeat=3):
            with self.subTest(codex=codex, copilot=copilot, opencode=opencode):
                target = self.copy(use_codex=codex, use_copilot=copilot, use_opencode=opencode)
                self.assertEqual(json.loads((target / '.engineering-backbone/project.json').read_text())['agents'],
                                 {'codex': codex, 'copilot': copilot})
                self.assertEqual((target / 'AGENTS.md').exists(), codex or opencode)
                for name in ASSETS:
                    self.assertEqual((target / name).exists(), opencode, name)
                if opencode:
                    companion = json.loads((target / ASSETS[2]).read_text())
                    self.assertFalse(companion['enabled'])
                    self.assertEqual(companion['native_config'], 'opencode.json')
                    self.assertEqual({path.name for path in (target / '.opencode/agents').iterdir()},
                                     {'backbone-' + role + '.md' for role in ROLES})
                    self.assertEqual({path.parent.name for path in (target / '.opencode/skills').rglob('SKILL.md')}, set(SKILLS))
                    for name in json.loads((target / 'opencode.json').read_text())['instructions']:
                        self.assertTrue((target / name).is_file(), name)
        default = self.copy()
        self.assertFalse((default / 'opencode.json').exists())
        self.assertFalse(yaml.safe_load((default / '.engineering-backbone/copier-answers.yml').read_text())['use_opencode'])

    def test_source_and_generated_native_bodies_share_existing_procedures(self):
        target = self.copy(use_opencode=True)
        environment = Environment(loader=FileSystemLoader(self.source), undefined=StrictUndefined,
                                  keep_trailing_newline=True)
        for name, partial in [*ROLES.items(), *[(name, 'skill-' + name) for name in SKILLS]]:
            skill = partial.startswith('skill-')
            relative = (Path('.opencode/skills') / name / 'SKILL.md' if skill else
                        Path('.opencode/agents') / ('backbone-' + name + '.md'))
            source_header, source_body = native_document(self.source / relative)
            target_header, target_body = native_document(target / relative)
            self.assertEqual(source_header, target_header)
            prefix = '../../../' if skill else '../../'
            procedure = environment.get_template('templates/_partials/copilot/' + partial + '.md.jinja')
            for body, core, guide in ((source_body, 'policy/core.md', 'docs/opencode/workflow.md'),
                                     (target_body, '.engineering-backbone/core.md', '.engineering-backbone/opencode-guide.md')):
                self.assertEqual(body, procedure.render(core_link=prefix + core, guide_link=prefix + guide,
                                                       workflow_label='OpenCode workflow', plan_review=True).strip())
            if not skill:
                self.assertEqual(source_header['mode'], 'primary')
                self.assertEqual(next(iter(source_header['permission'])), '*')
                self.assertEqual(source_header['permission']['*'], 'deny')
        reviewer = (target / '.opencode/agents/backbone-reviewer.md').read_text()
        self.assertIn('Completed implementation checks are not a prerequisite for plan review.', reviewer)

    def test_update_preserves_native_jsonc_roles_skills_and_stronger_local_instructions(self):
        target = self.copy(use_opencode=True)
        initialize(target)
        additions = {
            'AGENTS.md': '\nLocal Publish-Go and history signatures remain required.\n',
            'opencode.jsonc': '// Existing native configuration; reconcile before controlled execution.\n{}\n',
            '.opencode/agents/backbone-reviewer.md': '\nAdditional local review gate.\n',
            '.opencode/skills/code-review/SKILL.md': '\nAdditional local review procedure.\n',
            '.opencode/skills/code-review/resources/local.txt': 'Ordinary support resource.\n',
        }
        for name, content in additions.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text((path.read_text() if path.exists() else '') + content)
        config = json.loads((target / 'opencode.json').read_text())
        config['permission']['skill'] = 'deny'
        (target / 'opencode.json').write_text(json.dumps(config) + '\n')
        before = snapshot(target)
        commit(target, 'Local stronger preserved controls')
        run_update(target, vcs_ref='v0.2.0', answers_file='.engineering-backbone/copier-answers.yml',
                   defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        after = snapshot(target)
        for name in {*additions, 'opencode.json', '.engineering-backbone/opencode.json'}:
            self.assertEqual(before[name], after[name], name)

    def test_installation_choice_change_rejected_before_mutation(self):
        for enabled in (False, True):
            with self.subTest(installed=enabled):
                target = self.copy(use_opencode=enabled)
                initialize(target)
                commit(target, 'Installed adapter choice')
                before = snapshot(target)
                with self.assertRaises(Exception) as caught:
                    run_update(target, data={'use_opencode': not enabled}, vcs_ref='v0.2.0',
                               answers_file='.engineering-backbone/copier-answers.yml',
                               defaults=True, quiet=True, overwrite=True, skip_tasks=True)
                self.assertIn('installation-only', str(caught.exception))
                self.assertEqual(before, snapshot(target))

    def test_legacy_missing_answer_remains_false_on_real_update(self):
        source = self.workspace / 'historical-source'
        historical_source(source)
        initialize(source)
        commit(source, 'Pinned historical source')
        git(source, 'tag', 'v0.1.0')
        target = self.workspace / 'legacy-consumer'
        run_copy(str(source), target, defaults=True, quiet=True, skip_tasks=True, vcs_ref='v0.1.0')
        initialize(target)
        commit(target, 'Legacy consumer')
        for path in list(source.iterdir()):
            if path.name == '.git':
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        shutil.copytree(self.source, source, dirs_exist_ok=True, ignore=COPY_IGNORE)
        commit(source, 'Current optional package')
        git(source, 'tag', 'v0.2.0')
        run_update(target, vcs_ref='v0.2.0', answers_file='.engineering-backbone/copier-answers.yml',
                   defaults=True, quiet=True, overwrite=True, skip_tasks=True)
        self.assertFalse((target / 'opencode.json').exists())
        self.assertFalse(yaml.safe_load((target / '.engineering-backbone/copier-answers.yml').read_text())['use_opencode'])


if __name__ == '__main__':
    unittest.main()
