"""Render B2 result summaries to JSON / CSV / Markdown.

Each renderer is a pure function returning a string; no filesystem access.
"""

import json
from typing import Dict, List

from result_models import ResultRecord


def render_json(
    records: List[ResultRecord],
    aggregate: Dict[str, int],
    stats: Dict[str, object],
) -> str:
    """Render a JSON document with summary, aggregate and records."""
    payload = {
        "summary": stats,
        "aggregate": aggregate,
        "records": [r.to_dict() for r in records],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _csv_cell(value: object) -> str:
    text = str(value)
    if any(ch in text for ch in (",", '"', "\n")):
        text = '"' + text.replace('"', '""') + '"'
    return text


def render_csv(
    records: List[ResultRecord],
    aggregate: Dict[str, int],
    stats: Dict[str, object],
) -> str:
    """Render CSV: header + one row per record, plus a trailing summary block."""
    lines = ["case_id,status,category,duration_ms,message"]
    for r in records:
        lines.append(
            ",".join(
                [
                    _csv_cell(r.case_id),
                    _csv_cell(r.status),
                    _csv_cell(r.category),
                    _csv_cell(r.duration_ms),
                    _csv_cell(r.message),
                ]
            )
        )
    lines.append("")
    lines.append("summary")
    for key in ("total", "pass", "fail", "error", "skip"):
        lines.append(f"{key},{stats.get(key, 0)}")
    return "\n".join(lines)


def render_markdown(
    records: List[ResultRecord],
    aggregate: Dict[str, int],
    stats: Dict[str, object],
) -> str:
    """Render a Markdown report with a metrics table and a per-case table."""
    lines = ["# B2 Result Summary", ""]

    lines.append("## Metrics")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("| --- | --- |")
    for key, value in stats.items():
        lines.append(f"| {key} | {value} |")
    lines.append("")

    lines.append("## Cases")
    lines.append("")
    lines.append("| case_id | status | category | duration_ms | message |")
    lines.append("| --- | --- | --- | --- | --- |")
    for r in records:
        lines.append(
            f"| {r.case_id} | {r.status} | {r.category} | {r.duration_ms} | {r.message} |"
        )
    lines.append("")
    return "\n".join(lines)
