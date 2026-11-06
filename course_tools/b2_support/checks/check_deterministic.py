#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the deterministic seeding module.

Name intentionally uses check_* (not test_*) so the team root pytest default
discovery does not collect it. Run via:

    python -m unittest discover -s course_tools/b2_support/checks -p "check_*.py"
"""

import os
import sys
import unittest
from pathlib import Path

# Allow top-level import of sibling support modules regardless of cwd.
SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

import deterministic
from case_models import required_string_categories


class CheckDeterministicTest(unittest.TestCase):
    def test_seed_to_int_is_stable(self):
        self.assertEqual(deterministic.seed_to_int(1), deterministic.seed_to_int(1))
        self.assertEqual(deterministic.seed_to_int("abc"), deterministic.seed_to_int("abc"))

    def test_different_seeds_differ(self):
        self.assertNotEqual(deterministic.seed_to_int(1), deterministic.seed_to_int(2))

    def test_none_seed_is_stable_default(self):
        self.assertEqual(deterministic.seed_to_int(None), deterministic.seed_to_int(None))

    def test_make_rng_is_deterministic(self):
        a = deterministic.make_rng(42)
        b = deterministic.make_rng(42)
        self.assertEqual(a.random(), b.random())

    def test_stable_strings_are_deterministic(self):
        self.assertEqual(
            deterministic.stable_strings(seed=7, count=4),
            deterministic.stable_strings(seed=7, count=4),
        )

    def test_stable_strings_are_strings(self):
        for s in deterministic.stable_strings(seed=1, count=3):
            self.assertIsInstance(s, str)


class CheckCaseModelsTest(unittest.TestCase):
    def test_required_string_categories_present(self):
        cats = set(required_string_categories())
        for c in ("empty", "whitespace", "unicode", "emoji", "long_text", "newline", "tab"):
            self.assertIn(c, cats)


if __name__ == "__main__":
    unittest.main(verbosity=2)
