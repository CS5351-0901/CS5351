"""B2's own generic result record model.

Defines the result shape B2 aggregates and reports. This is intentionally a
self-contained schema owned by B2: it does NOT import or mirror any other
member's result format.
"""

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


VALID_STATUSES = ("pass", "fail", "error", "skip")


def is_valid_status(status: str) -> bool:
    return status in VALID_STATUSES
