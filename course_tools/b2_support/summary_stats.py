"""Compute summary statistics over B2 ResultRecord lists.

Pure data logic; no filesystem or external dependency.
"""

from typing import Dict, List

from result_models import ResultRecord, VALID_STATUSES


def _durations(records: List[ResultRecord], status: str) -> List[float]:
    return [r.duration_ms for r in records if r.status == status]


def summary(records: List[ResultRecord]) -> Dict[str, object]:
    """Return a flat dictionary of summary metrics.

    Includes status counts, per-status totals, and duration stats (total, min,
    max, mean) computed from the provided records.
    """
    counts = {s: 0 for s in VALID_STATUSES}
    for rec in records:
        counts[rec.status] = counts.get(rec.status, 0) + 1

    out: Dict[str, object] = {"total": len(records)}
    out.update(counts)

    for status in VALID_STATUSES:
        ds = _durations(records, status)
        out[f"{status}_duration_ms_total"] = round(sum(ds), 3)

    all_durations = [r.duration_ms for r in records]
    out["duration_ms_total"] = round(sum(all_durations), 3)
    out["duration_ms_min"] = round(min(all_durations), 3) if all_durations else 0.0
    out["duration_ms_max"] = round(max(all_durations), 3) if all_durations else 0.0
    out["duration_ms_mean"] = (
        round(sum(all_durations) / len(all_durations), 3) if all_durations else 0.0
    )

    return out
