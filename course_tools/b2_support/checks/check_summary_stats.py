#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for summary statistics."""

import os
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from result_models import ResultRecord
from summary_stats import summary


def _sample() -> list:
    return [
        ResultRecord(case_id="c1", status="pass", category="unit", duration_ms=10.0),
        ResultRecord(case_id="c2", status="pass", category="unit", duration_ms=20.0),
        ResultRecord(case_id="c3", status="fail", category="contract", duration_ms=30.0),
    ]


class CheckSummaryStatsTest(unittest.TestCase):
    def setUp(self):
        self.records = _sample()

    def test_counts(self):
        s = summary(self.records)
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["pass"], 2)
        self.assertEqual(s["fail"], 1)

    def test_duration_totals_per_status(self):
        s = summary(self.records)
        self.assertEqual(s["pass_duration_ms_total"], 30.0)
        self.assertEqual(s["fail_duration_ms_total"], 30.0)

    def test_overall_duration_stats(self):
        s = summary(self.records)
        self.assertEqual(s["duration_ms_total"], 60.0)
        self.assertEqual(s["duration_ms_min"], 10.0)
        self.assertEqual(s["duration_ms_max"], 30.0)
        self.assertEqual(s["duration_ms_mean"], 20.0)

    def test_empty_records(self):
        s = summary([])
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["duration_ms_min"], 0.0)
        self.assertEqual(s["duration_ms_mean"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
