#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the JSON case generator."""

import json
import os
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

import json_case_generator


class CheckJsonCaseGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.values = json_case_generator.generate_json_values(seed=1)

    def test_covers_required_value_kinds(self):
        labels = {label for label, _ in self.values}
        for k in ("dict", "list", "nested", "empty", "numeric", "boolean", "null", "unicode"):
            self.assertIn(k, labels)

    def test_values_are_json_serializable(self):
        for _, value in self.values:
            json.dumps(value)  # must not raise

    def test_null_is_none(self):
        nulls = [(l, v) for l, v in self.values if l == "null"]
        self.assertTrue(nulls)
        self.assertIsNone(nulls[0][1])

    def test_malformed_texts_are_not_valid_json(self):
        for label, raw in json_case_generator.generate_malformed_json_texts():
            with self.assertRaises(Exception):
                json.loads(raw)

    def test_deterministic(self):
        self.assertEqual(
            json_case_generator.generate_json_values(seed=9),
            json_case_generator.generate_json_values(seed=9),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
