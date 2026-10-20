"""Real checkout regressions for the eight managed toolchain attributes."""
from __future__ import annotations

from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

from copier import run_copy

from src.maintenance.compile_toolchain_fingerprint import FILES, bundle_digest


ROOT = Path(__file__).resolve().parents[2]


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, text=True,
                          capture_output=True, check=True).stdout.strip()


def initialize(root):
    git(root, '-c', 'init.defaultBranch=main', 'init')
    git(root, 'config', 'user.email', 'attributes-tests@example.invalid')
    git(root, 'config', 'user.name', 'Attributes fixture')


def commit(root, message, *paths):
    git(root, 'add', *(paths or ('.',)))
    git(root, 'commit', '-m', message)


class AttributesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_temp = tempfile.TemporaryDirectory(prefix='backbone-attributes-source-')
        cls.addClassCleanup(cls.source_temp.cleanup)
        cls.template = Path(cls.source_temp.name) / 'source'
        shutil.copytree(ROOT, cls.template, ignore=shutil.ignore_patterns(
            '.git', 'artifacts', '.venv', '__pycache__'))
        initialize(cls.template)
        commit(cls.template, 'Current template fixture')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='backbone-attributes-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.source = self.workspace / 'consumer'
        run_copy(str(self.template), self.source, defaults=True, quiet=True,
                 skip_tasks=True, vcs_ref='HEAD')
        initialize(self.source)
        self.application = b'print("ordinary application")\n'
        (self.source / 'application.py').write_bytes(self.application)
        commit(self.source, 'Plain canonical consumer bytes')

    def checkout(self, attributes):
        # Add only the parent attributes after committing canonical UTF-8 bytes;
        # the next fresh checkout is where inherited transformations take effect.
        (self.source / '.gitattributes').write_text(attributes, encoding='utf-8')
        commit(self.source, 'Parent attribute fixture', '.gitattributes')
        target = self.workspace / 'checkout'
        git(self.workspace, 'clone', '--no-checkout', str(self.source), str(target))
        return target

    def assert_managed_tuple_preserved(self, checkout):
        self.assertEqual(bundle_digest(self.source), bundle_digest(checkout))
        for name in FILES:
            with self.subTest(name=name):
                self.assertEqual((self.source / '.engineering-backbone' / name).read_bytes(),
                                 (checkout / '.engineering-backbone' / name).read_bytes())
                values = git(checkout, 'check-attr', 'filter', 'working-tree-encoding',
                             '--', '.engineering-backbone/' + name)
                self.assertIn('filter: unset', values)
                self.assertIn('working-tree-encoding: unset', values)

    def test_parent_content_filter_cannot_transform_managed_tooling(self):
        target = self.checkout('* filter=parent diff=python\n')
        script = self.workspace / 'filter.py'
        script.write_text('import sys\ndata = sys.stdin.buffer.read()\n'
                          'sys.stdout.buffer.write(data if len(sys.argv) > 1 else '
                          'data + b"\\n# parent filter\\n")\n', encoding='utf-8')
        command = shlex.quote(sys.executable) + ' ' + shlex.quote(str(script))
        git(target, 'config', 'filter.parent.clean', command + ' clean')
        git(target, 'config', 'filter.parent.smudge', command)
        git(target, 'config', 'filter.parent.required', 'true')
        git(target, 'checkout', '-f', 'HEAD')
        self.assert_managed_tuple_preserved(target)
        self.assertEqual(self.application + b'\n# parent filter\n',
                         (target / 'application.py').read_bytes())
        # Checkout-byte protection does not disable the existing text diff driver.
        self.assertIn('diff: python', git(target, 'check-attr', 'diff',
                                        '--', '.engineering-backbone/validate.py'))

    def test_parent_working_tree_encoding_cannot_transform_managed_tooling(self):
        attributes = ('*.py working-tree-encoding=UTF-16LE\n'
                      'requirements.txt working-tree-encoding=UTF-16LE\n'
                      'requirements.lock working-tree-encoding=UTF-16LE\n'
                      '*.schema.json working-tree-encoding=UTF-16LE\n')
        target = self.checkout(attributes)
        git(target, 'checkout', '-f', 'HEAD')
        self.assert_managed_tuple_preserved(target)
        self.assertEqual(self.application.decode('utf-8').encode('utf-16-le'),
                         (target / 'application.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
