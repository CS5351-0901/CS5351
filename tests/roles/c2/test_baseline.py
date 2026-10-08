"""C2 offline baseline: python -B -m unittest discover -s tests/roles/c2 -v."""

import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'skills/CodeAgent/scripts/codeagent_packager.py'
spec = importlib.util.spec_from_file_location('c2_packager', SCRIPT)
packager = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = packager
spec.loader.exec_module(packager)


def load_wrapper():
    """Compile the real owned method without importing the AstrBot host."""
    tree = ast.parse((ROOT / 'main.py').read_text(encoding='utf-8'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
               and n.name == 'CodeAgentPlugin')
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef)
                  and n.name == '_call_packager')
    namespace = {'json': json, 'subprocess': subprocess,
                 'List': list, 'Dict': dict, 'Any': object}
    exec(compile(ast.Module(body=[method], type_ignores=[]),
                 'main.py', 'exec'), namespace)
    return namespace['_call_packager']


class PackagerBaseline(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='c2-baseline-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.staging = self.root / 'staging'

        def isolated_path(value):
            # Redirect only the existing fixed temporary path; real filesystem
            # and ZIP operations still run within the test-owned directory.
            if str(value).startswith('/tmp/codeagent_pack_'):
                return self.staging
            return Path(value)

        redirect = patch.object(packager, 'Path', side_effect=isolated_path)
        redirect.start()
        self.addCleanup(redirect.stop)
        self.subject = packager.ProjectPackager(str(self.root / 'archive'))
        self.files = [{'name': 'main.py', 'content': 'def main():\n    return 42\n'}]

    def assert_archive(self, result, has_test=False):
        self.assertTrue(result['success'], result['error'])
        self.assertIsNone(result['error'])
        archive = Path(result['zip_path'])
        self.assertEqual(result['size'], archive.stat().st_size)
        with zipfile.ZipFile(archive) as zf:
            self.assertIsNone(zf.testzip())
            expected = {'demo/src/main.py', 'demo/src/__init__.py',
                        'demo/tests/__init__.py', 'demo/README.md',
                        'demo/pyproject.toml'}
            if has_test:
                expected.add('demo/tests/test_main.py')
            self.assertEqual(set(zf.namelist()), expected)
            self.assertEqual(zf.read('demo/src/main.py').decode().replace('\r\n', '\n'),
                             self.files[0]['content'])
            self.assertIn('[project]', zf.read('demo/pyproject.toml').decode())
        self.assertFalse(self.staging.exists())

    def test_python_zip_preserves_source_and_test(self):
        test_code = 'from src.main import main\nassert main() == 42\n'
        result = self.subject.pack(self.files, [{'name': 'test_main.py',
                                   'content': test_code}], name='demo')
        self.assert_archive(result, has_test=True)
        with zipfile.ZipFile(result['zip_path']) as zf:
            self.assertEqual(zf.read('demo/tests/test_main.py').decode().replace('\r\n', '\n'), test_code)

    def test_python_without_test_files(self):
        self.assert_archive(self.subject.pack(self.files, name='demo'))

    def test_python_with_empty_test_files(self):
        self.assert_archive(self.subject.pack(self.files, [], name='demo'))

    def test_write_failure_returns_error_and_cleans_staging(self):
        with patch.object(packager.ReadmeGenerator, 'generate',
                          side_effect=OSError('simulated disk failure')):
            result = self.subject.pack(self.files, name='demo')
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'simulated disk failure')
        self.assertEqual(result['zip_path'], '')
        self.assertFalse(self.staging.exists())
        self.assertEqual(list((self.root / 'archive').iterdir()), [])


class DependencyBaseline(unittest.TestCase):
    def test_python_imports_include_aliases_and_dotted_modules(self):
        code = 'import json, xml.etree as et\nfrom collections.abc import Mapping\n'
        self.assertEqual(packager.DependencyGenerator.extract_python_imports(code),
                         {'json', 'xml', 'collections'})

    def test_dependencies_deduplicate_sort_and_ignore_non_python(self):
        files = [packager.create_project_file('main.py',
                 'import zebra\nimport alpha\nimport zebra\nimport os\n'),
                 packager.create_project_file('notes.txt', 'import ignored')]
        with patch.object(packager.DependencyGenerator, '_is_external_module',
                          side_effect=lambda name: name in {'zebra', 'alpha'}):
            deps = packager.DependencyGenerator.detect_python_dependencies(files)
        self.assertEqual(deps, ['alpha', 'zebra'])
        self.assertEqual(packager.DependencyGenerator.generate_requirements(deps),
                         'alpha\nzebra\n')
        self.assertEqual(packager.DependencyGenerator.generate_requirements([]), '')

    def test_package_json_keeps_runtime_and_development_dependencies(self):
        project = packager.ProjectInfo(name='Demo App', description='example',
                  language='javascript', main_file='index.js',
                  dependencies=['express'], dev_dependencies=['jest'])
        data = json.loads(packager.DependencyGenerator.generate_package_json(project))
        self.assertEqual(data['name'], 'demo-app')
        self.assertEqual(data['dependencies'], {'express': 'latest'})
        self.assertEqual(data['devDependencies'], {'jest': 'latest'})
        self.assertEqual(data['scripts']['test'], 'jest')


class WrapperBaseline(unittest.TestCase):
    def setUp(self):
        self.call = load_wrapper()
        self.host = SimpleNamespace(scripts_dir=SCRIPT.parent)

    def test_cli_arguments_and_json_result(self):
        files = [{'name': 'main.py', 'content': 'print("hello")'}]
        tests = [{'name': 'test_main.py', 'content': 'assert True'}]
        result = {'success': True, 'zip_path': 'archive/demo.zip',
                  'file_count': 4, 'size': 123, 'error': None}
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(
                stdout=json.dumps(result), returncode=0)) as run:
            self.assertEqual(self.call(self.host, files, tests, 'demo',
                             'description', 'python'), result)
        args = run.call_args.args[0]
        self.assertEqual(args[:2], ['python3', str(SCRIPT)])
        for flag, expected in [('--files', files), ('--test-files', tests)]:
            self.assertEqual(json.loads(args[args.index(flag) + 1]), expected)
        self.assertEqual(args[args.index('--name') + 1], 'demo')
        self.assertEqual(args[args.index('--description') + 1], 'description')
        self.assertEqual(args[args.index('--type') + 1], 'python')
        self.assertEqual(run.call_args.kwargs,
                         {'capture_output': True, 'text': True, 'timeout': 120})

    def test_empty_tests_omit_optional_cli_argument(self):
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(
                stdout='{"success": false, "error": "fixture"}')) as run:
            result = self.call(self.host, [], [])
        self.assertNotIn('--test-files', run.call_args.args[0])
        self.assertEqual(result, {'success': False, 'error': 'fixture'})

    def test_missing_script_does_not_spawn(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(subprocess, 'run') as run:
                result = self.call(SimpleNamespace(scripts_dir=Path(directory)), [])
        run.assert_not_called()
        self.assertEqual(result, {'success': False, 'error': 'Packager script not found'})

    def test_invalid_stdout_returns_failure(self):
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(stdout='bad')):
            result = self.call(self.host, [])
        self.assertFalse(result['success'])
        self.assertTrue(result['error'])

    def test_timeout_returns_failure(self):
        with patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired(
                cmd='packager', timeout=120)):
            result = self.call(self.host, [])
        self.assertFalse(result['success'])
        self.assertIn('120', result['error'])


if __name__ == '__main__':
    unittest.main()
