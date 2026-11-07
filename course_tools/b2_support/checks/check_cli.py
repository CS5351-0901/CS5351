#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the CLI (exercised via subprocess with real temp files)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

CLI = SUPPORT_DIR / "cli.py"


def _write_sample(dirpath: Path) -> Path:
    inp = dirpath / "results.jsonl"
    lines = [
        {"case_id": "c1", "status": "pass", "category": "unit", "duration_ms": 1.0, "message": "ok", "metadata": {}},
        {"case_id": "c2", "status": "fail", "category": "contract", "duration_ms": 2.5, "message": "boom", "metadata": {}},
    ]
    inp.write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")
    return inp


class CheckCliTest(unittest.TestCase):
    def test_help_exits_zero(self):
        r = subprocess.run(
            [sys.executable, str(CLI), "--help"], capture_output=True, text=True
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("usage", r.stdout.lower())

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as td:
            inp = _write_sample(Path(td))
            r = subprocess.run(
                [sys.executable, str(CLI), str(inp), "--format", "json"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0)
            data = json.loads(r.stdout)
            self.assertEqual(data["aggregate"]["pass"], 1)
            self.assertEqual(data["aggregate"]["fail"], 1)

    def test_csv_output(self):
        with tempfile.TemporaryDirectory() as td:
            inp = _write_sample(Path(td))
            r = subprocess.run(
                [sys.executable, str(CLI), str(inp), "--format", "csv"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0)
            self.assertIn("case_id,status", r.stdout)

    def test_markdown_output(self):
        with tempfile.TemporaryDirectory() as td:
            inp = _write_sample(Path(td))
            r = subprocess.run(
                [sys.executable, str(CLI), str(inp), "--format", "markdown"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0)
            self.assertIn("# B2 Result Summary", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
