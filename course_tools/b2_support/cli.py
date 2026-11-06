#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B2 generic result aggregator CLI (stdlib only).

Reads a JSONL file of ResultRecord dicts and prints a summary as JSON, CSV or
Markdown. Explicitly human-run; the support toolkit never registers any hook.

Examples:
  python course_tools/b2_support/cli.py results.jsonl --format json
  python course_tools/b2_support/cli.py results.jsonl --format csv
  python course_tools/b2_support/cli.py results.jsonl --format markdown
"""

import argparse
import json
import sys
from typing import List

from result_models import ResultRecord
from result_aggregator import aggregate
from summary_stats import summary
from report_renderer import render_json, render_csv, render_markdown


def load_records(path: str) -> List[ResultRecord]:
    """Load ResultRecord dicts from a JSONL file."""
    records: List[ResultRecord] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(ResultRecord(**json.loads(line)))
    return records


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="b2_result",
        description="B2 generic result aggregator: summarize ResultRecord JSONL.",
    )
    parser.add_argument(
        "input",
        help="path to a JSONL file of ResultRecord dicts",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "markdown"],
        default="json",
        help="output format (default: json)",
    )
    args = parser.parse_args(argv)

    records = load_records(args.input)
    agg = aggregate(records)
    stats = summary(records)

    if args.format == "json":
        sys.stdout.write(render_json(records, agg, stats))
    elif args.format == "csv":
        sys.stdout.write(render_csv(records, agg, stats))
    else:
        sys.stdout.write(render_markdown(records, agg, stats))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
