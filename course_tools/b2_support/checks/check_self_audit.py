#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the B2 support self-audit."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from self_audit import audit


class CheckSelfAuditTest(unittest.TestCase):
    def test_real_support_tree_passes(self):
        result = audit(SUPPORT_DIR)
        self.assertTrue(result["ok"])
        self.assertEqual(result["missing_modules"], [])
        self.assertEqual(result["missing_checks"], [])
        self.assertEqual(result["forbidden_imports"], [])
        self.assertEqual(result["third_party_imports"], [])
        self.assertEqual(result["errors"], [])

    def test_detects_missing_modules_and_checks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "case_models.py").write_text("", encoding="utf-8")
            result = audit(root)
            self.assertIn("deterministic", result["missing_modules"])
            self.assertIn("check_deterministic", result["missing_checks"])
            self.assertFalse(result["ok"])

    def test_detects_forbidden_import(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "bad.py").write_text("import main\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["forbidden_imports"][0]["module"], "main")
            self.assertFalse(result["ok"])

    def test_detects_third_party_import(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "ext.py").write_text("import requests\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["third_party_imports"][0]["module"], "requests")
            self.assertFalse(result["ok"])

    def test_deterministic(self):
        first = json.dumps(audit(SUPPORT_DIR), sort_keys=True)
        second = json.dumps(audit(SUPPORT_DIR), sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main(verbosity=2)
