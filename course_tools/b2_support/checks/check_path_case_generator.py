#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the path case generator."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

import path_case_generator
from case_models import PathCase, required_path_styles


class CheckPathCaseGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.cases = path_case_generator.generate_path_cases(seed=3)

    def test_returns_path_cases(self):
        for c in self.cases:
            self.assertIsInstance(c, PathCase)
            self.assertIsInstance(c.value, str)

    def test_covers_all_styles(self):
        styles = {c.style for c in self.cases}
        for s in required_path_styles():
            self.assertIn(s, styles)

    def test_windows_style_uses_backslash(self):
        win = [c for c in self.cases if c.style == "windows"]
        self.assertTrue(win)
        self.assertIn("\\", win[0].value)

    def test_deterministic(self):
        self.assertEqual(
            path_case_generator.generate_path_cases(seed=5),
            path_case_generator.generate_path_cases(seed=5),
        )

    def test_unique_case_ids(self):
        ids = [c.case_id for c in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_generator_has_no_filesystem_side_effect(self):
        # The generator must only return strings and must never create files.
        with tempfile.TemporaryDirectory() as td:
            old = os.getcwd()
            os.chdir(td)
            try:
                before = set(os.listdir(td))
                path_case_generator.generate_path_cases(seed=1)
                self.assertEqual(before, set(os.listdir(td)))
            finally:
                os.chdir(old)


if __name__ == "__main__":
    unittest.main(verbosity=2)
