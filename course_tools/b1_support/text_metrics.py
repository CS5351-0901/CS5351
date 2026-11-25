"""Read-only UTF-8 metrics and raw-byte hashes for generic files."""

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TextMetrics:
    status: str
    size_bytes: int | None = None
    sha256: str | None = None
    total_lines: int | None = None
    blank_lines: int | None = None
    nonblank_lines: int | None = None
    max_line_length: int | None = None
    average_line_length: float | None = None
    error_code: int | None = None


def decode_text_bytes(data: bytes) -> tuple[str, str | None]:
    """Classify binary controls before strict UTF-8 decoding; ignore a UTF-8 BOM.

    NUL, DEL, and C0 controls other than tab and recognized line separators
    mark binary-like input. This is a deterministic heuristic, not file-type
    detection. Other undecodable input has the separate invalid_utf8 status.
    """
    if any(byte < 9 or 14 <= byte < 32 or byte == 127 for byte in data):
        return "binary_like", None
    try:
        return "ok", data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "invalid_utf8", None


def read_file_bytes(
    path: str | os.PathLike[str],
) -> tuple[bytes | None, str, int | None]:
    """Read an explicitly selected regular file; omit OS messages and paths."""
    candidate = Path(path)
    try:
        if not stat.S_ISREG(candidate.stat().st_mode):
            return None, "not_regular_file", None
        return candidate.read_bytes(), "ok", None
    except OSError as exc:
        return None, "read_error", exc.errno


def analyze_text_bytes(data: bytes) -> TextMetrics:
    """Count splitlines without a phantom trailing line; lengths are characters.

    Blank lines contain only whitespace. Length statistics include blank lines
    and exclude separators. Empty text has zero lines and zero lengths. The
    SHA-256 always covers the original bytes, including any BOM or CRLF bytes.
    """
    digest = hashlib.sha256(data).hexdigest()
    status, text = decode_text_bytes(data)
    if text is None:
        return TextMetrics(status, size_bytes=len(data), sha256=digest)
    lines = text.splitlines()
    lengths = [len(line) for line in lines]
    blank = sum(not line.strip() for line in lines)
    return TextMetrics(
        status="ok", size_bytes=len(data), sha256=digest,
        total_lines=len(lines), blank_lines=blank, nonblank_lines=len(lines) - blank,
        max_line_length=max(lengths, default=0),
        average_line_length=sum(lengths) / len(lines) if lines else 0.0,
    )


def analyze_text_file(path: str | os.PathLike[str]) -> TextMetrics:
    data, status, error_code = read_file_bytes(path)
    if data is None:
        return TextMetrics(status, error_code=error_code)
    return analyze_text_bytes(data)
