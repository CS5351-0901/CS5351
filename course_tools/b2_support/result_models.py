"""B2's own generic result record model.

Defines the result shape B2 aggregates and reports. This is intentionally a
self-contained schema owned by B2: it does NOT import or mirror any other
member's result format.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field, asdict
from typing import Any, Dict


@dataclass
class ResultRecord:
    """A single generic result record.

    Fields:
      case_id:    unique identifier for the case.
      status:     one of "pass" | "fail" | "error" | "skip".
      category:   logical grouping, e.g. "unit", "boundary", "contract".
      duration_ms: measured execution time in milliseconds.
      message:    human-readable note.
      metadata:   free-form extra data.
    """

    case_id: str
    status: str
    category: str
    duration_ms: float = 0.0
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ResultRecord":
        """Strictly parse a result payload.

        Raises ValueError for malformed input: a non-mapping payload, missing
        required fields, an unknown status, a non-numeric duration_ms, or non-dict
        metadata.
        """
        if not isinstance(payload, Mapping):
            raise ValueError("result payload must be a mapping")

        for key in ("case_id", "status", "category"):
            if key not in payload:
                raise ValueError(f"missing required field: {key}")

        status = payload["status"]
        require_valid_status(status)

        duration = payload.get("duration_ms", 0.0)
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            raise ValueError(
                f"duration_ms must be numeric, got {type(duration).__name__}"
            )

        metadata = payload.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a dict")

        return cls(
            case_id=str(payload["case_id"]),
            status=status,
            category=str(payload["category"]),
            duration_ms=float(duration),
            message=str(payload.get("message", "")),
            metadata=dict(metadata),
        )


VALID_STATUSES = ("pass", "fail", "error", "skip")


def is_valid_status(status: str) -> bool:
    return status in VALID_STATUSES


def require_valid_status(status: str) -> None:
    """Raise ValueError when `status` is not one of the known statuses."""
    if status not in VALID_STATUSES:
        raise ValueError(f"unknown status: {status}")
