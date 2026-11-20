"""Sandbox CLI failure paths and artifact filtering, using trusted fixtures."""

import unittest

from test_week10_file_limits import run_sandbox


class SandboxFailurePaths(unittest.TestCase):
    def test_syntax_error_is_failure_with_diagnostics(self):
        result = run_sandbox('def broken(:')
        self.assertFalse(result['success'])
        self.assertNotEqual(result['exit_code'], 0)
        self.assertIn('SyntaxError', result['stderr'])

    def test_runtime_exception_is_failure_with_diagnostics(self):
        result = run_sandbox("raise ValueError('fixture failure')")
        self.assertFalse(result['success'])
        self.assertNotEqual(result['exit_code'], 0)
        self.assertIn('ValueError: fixture failure', result['stderr'])

    def test_real_sleep_is_stopped_by_wall_timeout(self):
        result = run_sandbox('import time\ntime.sleep(30)', wall_time_limit=1)
        self.assertFalse(result['success'])
        self.assertNotEqual(result['exit_code'], 0)
        self.assertTrue(result['error'] or result['stderr'], result)


class ArtifactFiltering(unittest.TestCase):
    def test_hidden_files_and_source_do_not_use_artifact_capacity(self):
        result = run_sandbox(
            "from pathlib import Path\n"
            "Path('.hidden').write_text('secret')\n"
            "Path('visible.txt').write_text('ok')", max_files=1)
        self.assertTrue(result['success'], result)
        self.assertEqual([item['name'] for item in result['files']], ['visible.txt'])

    def test_oversize_file_does_not_use_artifact_capacity(self):
        result = run_sandbox(
            "from pathlib import Path\n"
            "Path('large.bin').write_bytes(b'x' * (1024 * 1024 + 1))\n"
            "Path('small.txt').write_text('ok')", max_files=1, file_size_limit_mb=1)
        self.assertTrue(result['success'], result)
        self.assertEqual([item['name'] for item in result['files']], ['small.txt'])

    def test_unicode_file_metadata_uses_encoded_byte_count(self):
        result = run_sandbox(
            "from pathlib import Path\n"
            "Path('结果.txt').write_text('你好', encoding='utf-8')")
        self.assertTrue(result['success'], result)
        self.assertEqual(len(result['files']), 1)
        self.assertEqual(result['files'][0]['name'], '结果.txt')
        self.assertEqual(result['files'][0]['size'], 6)


if __name__ == '__main__':
    unittest.main()
