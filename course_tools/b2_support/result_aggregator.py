"""Aggregate B2 ResultRecord lists into grouped statistics.

Pure data logic over B2's own ResultRecord; no dependency on other members.
"""

from typing import Dict, List

from result_models import ResultRecord, VALID_STATUSES


def aggregate(records: List[ResultRecord]) -> Dict[str, int]:
    """Count records by status plus a total."""
    counts = {s: 0 for s in VALID_STATUSES}
    for rec in records:
        counts[rec.status] = counts.get(rec.status, 0) + 1
    result: Dict[str, int] = {"total": len(records)}
    result.update(counts)
    return result


def filter_by_status(records: List[ResultRecord], status: str) -> List[ResultRecord]:
    return [r for r in records if r.status == status]


def filter_by_category(
    records: List[ResultRecord], category: str
) -> List[ResultRecord]:
    return [r for r in records if r.category == category]


def status_counts(records: List[ResultRecord]) -> Dict[str, int]:
    """Alias for aggregate without the total."""
    agg = aggregate(records)
    agg.pop("total", None)
    return agg
