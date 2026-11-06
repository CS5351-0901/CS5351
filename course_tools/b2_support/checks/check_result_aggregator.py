#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the result aggregator."""

import os
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from result_aggregator import aggregate, filter_by_status, filter_by_category
from result_models import ResultRecord


def _sample() -> list:
    return [
        ResultRecord(case_id="c1", status="pass", category="unit", duration_ms=1.0),
        ResultRecord(case_id="c2", status="fail", category="unit", duration_ms=2.0),
        ResultRecord(case_id="c3", status="pass", category="contract", duration_ms=0.5),
        ResultRecord(case_id="c4", status="skip", category="boundary", duration_ms=0.0),
    ]


class CheckResultAggregatorTest(unittest.TestCase):
    def setUp(self):
        self.records = _sample()

    def test_aggregate_counts(self):
        agg = aggregate(self.records)
        self.assertEqual(agg["total"], 4)
        self.assertEqual(agg["pass"], 2)
        self.assertEqual(agg["fail"], 1)
        self.assertEqual(agg["skip"], 1)
        self.assertEqual(agg["error"], 0)

    def test_aggregate_empty(self):
        agg = aggregate([])
        self.assertEqual(agg["total"], 0)
        self.assertEqual(agg["pass"], 0)

    def test_filter_by_status(self):
        passed = filter_by_status(self.records, "pass")
        self.assertEqual([r.case_id for r in passed], ["c1", "c3"])

    def test_filter_by_category(self):
        contract = filter_by_category(self.records, "contract")
        self.assertEqual([r.case_id for r in contract], ["c3"])

    def test_unknown_status_not_in_aggregate(self):
        agg = aggregate(self.records)
        self.assertNotIn("bogus", agg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
