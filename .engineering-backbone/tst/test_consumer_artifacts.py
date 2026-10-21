"""Real legacy rendering and old-source artifact-boundary compatibility."""
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from tst import test_copier as copier_tests
from tst.test_source_layout_compatibility import frozen_files


ROOT = Path(__file__).resolve().parents[2]


class RenderedArtifactBoundaryTests(unittest.TestCase):
    setUp = copier_tests.CopierTests.setUp
    copy = copier_tests.CopierTests.copy
    validation_result = copier_tests.CopierTests.validation_result
    validate = copier_tests.CopierTests.validate

    def test_rendered_consumer_accepts_product_fixtures_but_rejects_managed_artifacts(self):
        target = self.copy()
        self.validate(target)
        fixtures = {
            'apps/backend/tst/examples/request.json': '{"value": 1}\n',
            'apps/backend/tst/tasks/task-packet.json': '{"scope": {}}\n',
            'src/reviews/review-evidence.json': '{"reviewers": []}\n',
            'docs/requirements/request.json': '{"statement": "product-owned"}\n',
            'examples/invalid.schema.json': '{"type": "made-up"}\n',
            'examples/invalid-json.json': '{"incomplete":\n',
        }
        for relative, content in fixtures.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        self.validate(target)
        for relative, content, message in (
            ('.engineering-backbone/examples/unknown.json', '{"value": 1}',
             'unrecognized governance JSON artifact'),
            ('.engineering-backbone/artifacts/reviews/task-packet.json', '{"scope": {}}',
             'scope:'),
            ('.engineering-backbone/schemas/invalid.schema.json', '{"type": "made-up"}',
             'invalid JSON schema'),
        ):
            with self.subTest(path=relative):
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
                result = self.validation_result(target)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(relative, result.stdout + result.stderr)
                self.assertIn(message, result.stdout + result.stderr)
                path.unlink()


class OldSourceArtifactBoundaryTests(unittest.TestCase):
    def test_original_source_roots_remain_reserved_without_claiming_product_paths(self):
        with tempfile.TemporaryDirectory(prefix='backbone-artifact-old-source-') as temporary:
            target = Path(temporary)
            for relative, content in frozen_files('old-source').items():
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

            def validate():
                return subprocess.run([
                    sys.executable, '-I', str(ROOT / '.engineering-backbone/src/validate.py'),
                    '--root', str(target),
                ], cwd=target, capture_output=True, text=True, timeout=60)

            baseline = validate()
            self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
            product = target / 'apps/backend/tst/examples/request.json'
            product.parent.mkdir(parents=True)
            product.write_text('{"value": 1}', encoding='utf-8')
            accepted = validate()
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            for relative, content, message in (
                ('examples/request.json', '{"value": 1}', 'unrecognized governance JSON artifact'),
                ('plans/new-task.json', '{"scope": {}}', 'scope:'),
                ('schemas/invalid.schema.json', '{"type": "made-up"}', 'invalid JSON schema'),
            ):
                with self.subTest(path=relative):
                    path = target / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding='utf-8')
                    result = validate()
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn(relative, result.stdout + result.stderr)
                    self.assertIn(message, result.stdout + result.stderr)
                    path.unlink()


if __name__ == '__main__':
    unittest.main()
