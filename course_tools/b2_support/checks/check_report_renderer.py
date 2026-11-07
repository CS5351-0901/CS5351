#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for report renderers."""

import csv
import io
import json
import os
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from report_renderer import render_json, render_csv, render_markdown
from result_models import ResultRecord
from result_aggregator import aggregate
from summary_stats import summary


def _sample() -> list:
    return [
        ResultRecord(case_id="c1", status="pass", category="unit", duration_ms=1.0, message="ok"),
        ResultRecord(case_id="c2", status="fail", category="contract", duration_ms=2.5, message="boom"),
    ]


class CheckReportRendererTest(unittest.TestCase):
    def setUp(self):
        self.records = _sample()
        self.agg = aggregate(self.records)
        self.stats = summary(self.records)

    def test_json_is_valid_and_complete(self):
        text = render_json(self.records, self.agg, self.stats)
        data = json.loads(text)
        self.assertEqual(data["aggregate"]["total"], 2)
        self.assertEqual(len(data["records"]), 2)
        self.assertEqual(data["records"][0]["case_id"], "c1")

    def test_json_is_deterministic(self):
        a = render_json(self.records, self.agg, self.stats)
        b = render_json(self.records, self.agg, self.stats)
        self.assertEqual(a, b)

    def test_csv_has_header_and_rows(self):
        text = render_csv(self.records, self.agg, self.stats)
        rows = list(csv.reader(io.StringIO(text)))
        self.assertEqual(rows[0][:2], ["case_id", "status"])
        self.assertEqual(len(rows), 10)  # header + 2 cases + blank + summary header + 5 metrics

    def test_markdown_has_metric_and_case_tables(self):
        text = render_markdown(self.records, self.agg, self.stats)
        self.assertIn("| metric | value |", text)
        self.assertIn("| case_id | status |", text)
        self.assertIn("| c1 | pass | unit | 1.0 | ok |", text)

    def test_markdown_embeds_stats(self):
        text = render_markdown(self.records, self.agg, self.stats)
        self.assertIn("| total | 2 |", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
