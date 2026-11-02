"""Week 7: nested test layout and conflicting filesystem paths."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import test_baseline as baseline


packager = baseline.packager


class TestLayoutContracts(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='c2-layout-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.staging = self.root / 'staging'
        self.archive = self.root / 'archive'

        def isolated_path(value):
            if str(value).startswith('/tmp/codeagent_pack_'):
                return self.staging
            return Path(value)

        redirect = patch.object(packager, 'Path', side_effect=isolated_path)
        redirect.start()
        self.addCleanup(redirect.stop)
        self.subject = packager.ProjectPackager(str(self.archive))
        self.files = [{'name': 'main.py', 'content': 'VALUE = 42\n'}]

    def assert_delivery(self, tests):
        result = self.subject.pack(self.files, tests, name='layout')
        self.assertTrue(result['success'], result['error'])
        self.assertIsNone(result['error'])
        self.assertFalse(self.staging.exists())
        archive = Path(result['zip_path'])
        self.assertEqual(result['size'], archive.stat().st_size)
        with zipfile.ZipFile(archive) as zf:
            self.assertIsNone(zf.testzip())
            expected = {'layout/src/main.py', 'layout/src/__init__.py',
                        'layout/tests/__init__.py', 'layout/README.md',
                        'layout/pyproject.toml'}
            expected.update('layout/tests/' + item['name'] for item in tests)
            self.assertEqual(set(zf.namelist()), expected)
            self.assertEqual(result['file_count'], len(expected))
            for item in tests:
                content = zf.read('layout/tests/' + item['name']).decode('utf-8')
                self.assertEqual(content.replace('\r\n', '\n'), item['content'])

    def test_single_nested_test_directory(self):
        self.assert_delivery([{'name': 'unit/test_main.py',
                               'content': 'from src.main import VALUE\nassert VALUE == 42\n'}])

    def test_deep_directories_preserve_same_basename(self):
        self.assert_delivery([
            {'name': 'unit/models/test_value.py', 'content': 'UNIT = 1\n'},
            {'name': 'integration/models/test_value.py', 'content': 'INTEGRATION = 2\n'}])

    def test_unicode_names_and_empty_nested_file(self):
        self.assert_delivery([
            {'name': 'unit/data/empty.txt', 'content': ''},
            {'name': 'unicode/test_\u6570\u636e.py',
             'content': 'MESSAGE = "\u4f60\u597d"\n'}])

    def test_flat_and_nested_tests_share_existing_parent(self):
        self.assert_delivery([
            {'name': 'test_root.py', 'content': 'ROOT = True\n'},
            {'name': 'unit/test_first.py', 'content': 'FIRST = True\n'},
            {'name': 'unit/test_second.py', 'content': 'SECOND = True\n'}])

    def assert_path_conflict(self, tests):
        result = self.subject.pack(self.files, tests, name='layout')
        self.assertFalse(result['success'])
        self.assertTrue(result['error'])
        self.assertEqual(result['zip_path'], '')
        self.assertEqual(result['file_count'], 0)
        self.assertEqual(result['size'], 0)
        self.assertFalse(self.staging.exists())
        self.assertEqual(list(self.archive.iterdir()), [])

    def test_existing_file_cannot_be_parent_directory(self):
        self.assert_path_conflict([
            {'name': 'unit', 'content': 'a regular file'},
            {'name': 'unit/test_main.py', 'content': 'assert True\n'}])

    def test_existing_directory_cannot_be_test_file(self):
        self.assert_path_conflict([
            {'name': 'unit/test_main.py', 'content': 'assert True\n'},
            {'name': 'unit', 'content': 'must not overwrite directory'}])


if __name__ == '__main__':
    unittest.main()
