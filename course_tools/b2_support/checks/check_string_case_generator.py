#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the string case generator."""

import os
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

import string_case_generator
from case_models import StringCase, required_string_categories


class CheckStringCaseGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.cases = string_case_generator.generate_string_cases(seed=1)

    def test_returns_string_cases(self):
        for c in self.cases:
            self.assertIsInstance(c, StringCase)
            self.assertIsInstance(c.value, str)

    def test_covers_all_categories(self):
        cats = {c.category for c in self.cases}
        for c in required_string_categories():
            self.assertIn(c, cats)

    def test_empty_category_value_is_empty(self):
        empty = [c for c in self.cases if c.category == "empty"]
        self.assertTrue(empty)
        self.assertEqual(empty[0].value, "")

    def test_long_text_is_long(self):
        long_ = [c for c in self.cases if c.category == "long_text"]
        self.assertTrue(long_)
        self.assertGreaterEqual(len(long_[0].value), 1000)

    def test_unicode_category_is_not_ascii_only(self):
        uni = [c for c in self.cases if c.category == "unicode"]
        self.assertTrue(uni)
        self.assertTrue(any(ord(ch) > 127 for ch in uni[0].value))

    def test_deterministic(self):
        self.assertEqual(
            string_case_generator.generate_string_cases(seed=9),
            string_case_generator.generate_string_cases(seed=9),
        )

    def test_unique_case_ids(self):
        ids = [c.case_id for c in self.cases]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
