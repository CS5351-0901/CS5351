"""Write JSON / JSONL / text corpora with an explicit output path.

Safety contract:
  - output must be given explicitly; nothing is auto-placed in a runtime dir.
  - overwrite is OFF by default; writing to an existing path raises
    FileExistsError unless overwrite=True.
  - a deterministic manifest is returned for every write.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Union


class OutputExistsError(FileExistsError):
    """Raised when the target output path already exists and overwrite is off."""


def _content_bytes(records: List[Dict[str, object]], fmt: str) -> bytes:
    """Serialize records deterministically into the target format bytes."""
    if fmt == "jsonl":
        lines = [
            json.dumps(rec, ensure_ascii=False, sort_keys=True)
            for rec in records
        ]
        text = "\n".join(lines)
    elif fmt == "json":
        text = json.dumps(records, ensure_ascii=False, sort_keys=True, indent=2)
    elif fmt == "text":
        text = "\n".join(str(rec) for rec in records)
    else:
        raise ValueError(f"unsupported format: {fmt}")
    return text.encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_corpus(
    output_path: Union[str, Path],
    records: List[Dict[str, object]],
    fmt: str = "jsonl",
    overwrite: bool = False,
) -> Dict[str, object]:
    """Write records to `output_path` and return a deterministic manifest.

    Raises OutputExistsError if the path exists and overwrite is False.
    """
    p = Path(output_path)
    if p.exists() and not overwrite:
        raise OutputExistsError(
            f"output already exists (overwrite disabled): {p}"
        )

    content = _content_bytes(records, fmt)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)

    return {
        "output": str(p),
        "format": fmt,
        "record_count": len(records),
        "bytes": len(content),
        "sha256": _sha256(content),
    }
