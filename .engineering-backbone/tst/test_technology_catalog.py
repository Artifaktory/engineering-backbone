"""Verify the technology extension delivered by real Copier consumer renders.

These checks establish catalog/consumer contract coverage, not execution of every
language toolchain or formal standards conformance. Navigation behavior and
adversarial binding/authority checks are covered by the navigation tests.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from copier import run_copy

from src.maintenance.compile_navigation import technology_catalog, validate_catalog
from tst.test_quality_copier import commit, initialize


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_PROFILES = {
    'python', 'javascript', 'typescript', 'java', 'csharp', 'go', 'c', 'cpp',
    'php', 'html', 'css', 'sql', 'postgresql', 'powershell', 'bash', 'json',
    'yaml', 'dockerfile', 'github-actions', 'windows', 'linux', 'node',
    'dotnet', 'jvm', 'docker', 'react', 'nextjs', 'fastapi',
}


class TechnologyCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix='backbone-technologies-')
        cls.addClassCleanup(temporary.cleanup)
        cls.workspace = Path(temporary.name)
        cls.source = cls.workspace / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', 'artifacts', '.venv'))
        initialize(cls.source)
        commit(cls.source, 'Reviewed technology template fixture')
        cls.consumer = cls.workspace / 'consumer'
        run_copy(str(cls.source), cls.consumer, data={
            'use_quality_framework': True, 'use_codex': False,
            'use_copilot': False,
        }, vcs_ref='HEAD', defaults=True, quiet=True, skip_tasks=True)
        cls.catalog_root = cls.consumer / '.engineering-backbone/standards/technologies'
        cls.sources = json.loads((cls.catalog_root / 'sources.json').read_text())
        cls.rules_wrapper = json.loads((cls.catalog_root / 'rules.json').read_text())
        cls.rules = {rule['id']: rule for rule in cls.rules_wrapper['rules']}
        cls.profiles = {
            path.stem: json.loads(path.read_text())
            for path in (cls.catalog_root / 'profiles').glob('*.json')
        }

    def test_real_render_contains_every_agreed_technology_and_identical_authority(self):
        self.assertEqual(EXPECTED_PROFILES, set(self.profiles))
        original = self.source / '.engineering-backbone/standards/technologies'
        expected_files = {path.relative_to(original) for path in original.rglob('*') if path.is_file()}
        actual_files = {path.relative_to(self.catalog_root) for path in self.catalog_root.rglob('*') if path.is_file()}
        self.assertEqual(expected_files, actual_files)
        for relative in expected_files:
            with self.subTest(relative=relative):
                self.assertEqual(
                    json.loads((original / relative).read_text()),
                    json.loads((self.catalog_root / relative).read_text()),
                )

    def test_default_legacy_render_does_not_install_or_activate_the_extension(self):
        legacy = self.workspace / 'legacy'
        run_copy(str(self.source), legacy, data={
            'use_codex': False, 'use_copilot': False,
        }, vcs_ref='HEAD', defaults=True, quiet=True, skip_tasks=True)
        self.assertFalse((legacy / '.engineering-backbone/standards/technologies').exists())
        self.assertFalse((legacy / '.engineering-backbone/technology-guide.md').exists())

    def test_installed_guidance_carries_authority_limits_and_agent_decision_space(self):
        guide = (self.consumer / '.engineering-backbone/technology-guide.md').read_text()
        original = (self.source / 'docs/quality/technology-profiles.md').read_text()
        self.assertEqual(original.strip(), guide.strip())
        for concept in ('MUST / MUSS', 'SHOULD / SOLL', 'FREE / FREI',
                        'native Windows', 'actual PostgreSQL',
                        'not that a model read it', 'not a certification'):
            self.assertIn(concept, guide)
        for profile in EXPECTED_PROFILES:
            self.assertIn('`' + profile + '`', guide)

    def test_every_selected_rule_has_sources_and_compatible_existing_check_kinds(self):
        source_ids = {source['id'] for source in self.sources['sources']}
        self.assertEqual(len(source_ids), len(self.sources['sources']))
        self.assertEqual(len(self.rules), len(self.rules_wrapper['rules']))
        workflow_schema = json.loads((self.source / '.engineering-backbone/schemas/workflows.schema.json').read_text())
        allowed_kinds = set(workflow_schema['$defs']['check']['properties']['kind']['enum'])
        core_profiles = {
            path.stem: json.loads(path.read_text())
            for path in (self.source / '.engineering-backbone/standards/profiles').glob('*.json')
        }
        selected_rule_ids = set()
        for name, profile in self.profiles.items():
            with self.subTest(profile=name):
                self.assertEqual(name, profile['id'])
                self.assertEqual('1', profile['version'])
                self.assertTrue(profile['rules'])
                self.assertTrue(profile['recommendations'])
                self.assertTrue(profile['free_choices'])
                for core_id in profile['quality_profiles']:
                    self.assertTrue(core_profiles[core_id]['enabled'])
                for rule_id in profile['rules']:
                    selected_rule_ids.add(rule_id)
                    rule = self.rules[rule_id]
                    self.assertEqual('1', rule['version'])
                    self.assertTrue(rule['statement'].startswith('MUST: '))
                    self.assertTrue(rule['source_ids'])
                    self.assertLessEqual(set(rule['source_ids']), source_ids)
                    self.assertTrue(rule['check_kind_groups'])
                    for group in rule['check_kind_groups']:
                        self.assertTrue(group)
                        self.assertEqual(len(group), len(set(group)))
                        self.assertLessEqual(set(group), allowed_kinds)
        self.assertEqual(selected_rule_ids, set(self.rules))

    def test_database_shell_and_platform_obligations_cannot_be_docs_only(self):
        expected = {
            'python': {'lint', 'typecheck', 'test'},
            'typescript': {'lint', 'typecheck', 'test'},
            'postgresql': {'test', 'migration'},
            'powershell': {'lint', 'test'},
            'bash': {'lint', 'test'},
            'windows': {'test'},
            'linux': {'test'},
        }
        for profile_id, required_kinds in expected.items():
            with self.subTest(profile=profile_id):
                groups = [group for rule_id in self.profiles[profile_id]['rules']
                          for group in self.rules[rule_id]['check_kind_groups']]
                for kind in required_kinds:
                    self.assertIn([kind], groups)
                self.assertNotIn(['docs'], groups)
        self.assertEqual(['python'], self.profiles['fastapi']['quality_profiles'])
        self.assertEqual(['typescript'], self.profiles['typescript']['quality_profiles'])

    def test_provenance_limits_and_old_reference_profiles_remain_explicit(self):
        sources = {source['id']: source for source in self.sources['sources']}
        self.assertEqual('reference-only', sources['TECH-SRC-C']['adoption'])
        self.assertEqual('public-scope-only', sources['TECH-SRC-C']['access'])
        self.assertEqual('retrieval-limited', sources['TECH-SRC-BASH']['status'])
        self.assertEqual('indexed-summary-only', sources['TECH-SRC-BASH']['access'])
        for source in sources.values():
            self.assertTrue(source['url'].startswith('https://'))
            self.assertTrue(source['edition'])
            self.assertTrue(source['verified_sections'])
        for reference in ('cpp17', 'iec61508', 'iec62304'):
            original = json.loads((self.source / '.engineering-backbone/standards/profiles' / (reference + '.json')).read_text())
            installed = json.loads((self.consumer / '.engineering-backbone/standards/profiles' / (reference + '.json')).read_text())
            self.assertFalse(original['enabled'])
            self.assertEqual(original, installed)

    def test_compiler_rejects_broken_source_rule_check_and_prerequisite_contracts(self):
        # Exercise the real compiler entry point before any mutation. Profiles
        # without a language-specific core prerequisite are valid; navigation
        # still requires the project baseline independently.
        original = technology_catalog(self.source)
        mutations = {
            'duplicate source identity': lambda value: value['sources'].append(copy.deepcopy(value['sources'][0])),
            'empty sources': lambda value: value.update(sources=[]),
            'missing provenance': lambda value: value['sources'][0].update(verified_sections=[]),
            'source code field': lambda value: value['sources'][0].update(command='execute-candidate'),
            'unknown rule source': lambda value: value['rules'][0].update(source_ids=['TECH-SRC-ABSENT']),
            'unsupported rule version': lambda value: value['rules'][0].update(version='2'),
            'unknown check kind': lambda value: value['rules'][0].update(check_kind_groups=[['arbitrary-shell']]),
            'empty check group': lambda value: value['rules'][0].update(check_kind_groups=[[]]),
            'removed check obligations': lambda value: value['rules'][0].update(check_kind_groups=[]),
            'unknown profile rule': lambda value: value['profiles'][0].update(rules=['TECH-ABSENT-001']),
            'unknown core prerequisite': lambda value: value['profiles'][0].update(quality_profiles=['unknown']),
            'inactive core prerequisite': lambda value: value['profiles'][0].update(quality_profiles=['cpp17']),
            'missing decision space': lambda value: value['profiles'][0].update(free_choices=[]),
        }
        for label, mutate in mutations.items():
            with self.subTest(mutation=label):
                altered = copy.deepcopy(original)
                mutate(altered)
                with self.assertRaises(ValueError):
                    validate_catalog(altered, self.source)

    def test_compiler_rejects_ambiguous_catalog_json_and_mismatched_filename(self):
        with tempfile.TemporaryDirectory(prefix='backbone-technology-invalid-') as directory:
            source = Path(directory)
            shutil.copytree(self.source / '.engineering-backbone/standards', source / '.engineering-backbone/standards')
            sources_path = source / '.engineering-backbone/standards/technologies/sources.json'
            original = sources_path.read_text()
            sources_path.write_text(original.replace(
                '"schema_version": "1",', '"schema_version": "1", "schema_version": "1",', 1))
            with self.assertRaisesRegex(ValueError, 'Duplicate technology authority key'):
                technology_catalog(source)
            sources_path.write_text(original)
            profile = source / '.engineering-backbone/standards/technologies/profiles/bash.json'
            profile.rename(profile.with_name('wrong-name.json'))
            with self.assertRaisesRegex(ValueError, 'identity differs from filename'):
                technology_catalog(source)


if __name__ == '__main__':
    unittest.main()
