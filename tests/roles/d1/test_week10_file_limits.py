"""Real sandbox CLI regressions for returned artifact count limits."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[3] / 'skills/CodeAgent/scripts/codeagent_sandbox.py'


def run_sandbox(code, **settings):
    """Run only trusted fixture code in an isolated disposable workspace."""
    with tempfile.TemporaryDirectory(prefix='d1 cli regression ') as directory:
        root = Path(directory)
        config = {
            'workspace_root': str(root / 'workspace'),
            'use_restricted_python': False,
            'wall_time_limit': 5,
            **settings,
        }
        config_path = root / 'sandbox config.json'
        config_path.write_text(json.dumps(config), encoding='utf-8')
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), '--code', code, '--session-id', 'regression',
             '--config', str(config_path)],
            cwd=root, capture_output=True, encoding='utf-8', timeout=15,
        )
        if proc.returncode != 0:
            raise AssertionError(f'CLI failed: {proc.returncode}: {proc.stderr}')
        return json.loads(proc.stdout)


class FileCountLimits(unittest.TestCase):
    CODE = "from pathlib import Path\nfor i in range(4): Path(f'item{i}.txt').write_text('ok')"

    def test_one_file_limit_never_returns_two(self):
        result = run_sandbox(self.CODE, max_files=1)
        self.assertTrue(result['success'], result)
        self.assertEqual(len(result['files']), 1)

    def test_zero_file_limit_returns_no_artifacts(self):
        result = run_sandbox(self.CODE, max_files=0)
        self.assertTrue(result['success'], result)
        self.assertEqual(result['files'], [])

    def test_limit_larger_than_output_preserves_all_artifacts(self):
        result = run_sandbox(self.CODE, max_files=10)
        self.assertTrue(result['success'], result)
        self.assertEqual({item['name'] for item in result['files']},
                         {'item0.txt', 'item1.txt', 'item2.txt', 'item3.txt'})


if __name__ == '__main__':
    unittest.main()
