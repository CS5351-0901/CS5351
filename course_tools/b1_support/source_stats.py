"""Static Python AST and JSON structure statistics; source is never executed."""

import ast
import json
import os
from dataclasses import dataclass
from pathlib import Path

from .text_metrics import decode_text_bytes, read_file_bytes


@dataclass(frozen=True)
class SourceStats:
    kind: str
    status: str
    class_count: int | None = None
    function_count: int | None = None
    async_function_count: int | None = None
    top_level_type: str | None = None
    top_level_key_count: int | None = None
    error_line: int | None = None
    error_column: int | None = None
    error_code: int | None = None


def _reject_json_constant(value: str) -> None:
    raise ValueError("Nonstandard JSON numeric constant")


def analyze_source_bytes(data: bytes, *, kind: str) -> SourceStats:
    """Count nested AST definitions or top-level JSON keys after parsing.

    Python function_count excludes async functions. JSON object key counts
    count unique parsed keys, excluding nested objects. For non-object JSON,
    key count is None and top_level_type identifies the parsed value instead.
    Failed analyses use None counts rather than misleading zeroes. Errors have
    positions where available, without source excerpts or exception messages.
    """
    if kind not in ("python", "json"):
        raise ValueError("Source kind must be python or json")
    status, text = decode_text_bytes(data)
    if text is None:
        return SourceStats(kind, status)
    if kind == "python":
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            return SourceStats(kind, "syntax_error", error_line=exc.lineno,
                               error_column=exc.offset)
        nodes = list(ast.walk(tree))
        return SourceStats(
            kind, "ok",
            class_count=sum(isinstance(node, ast.ClassDef) for node in nodes),
            function_count=sum(isinstance(node, ast.FunctionDef) for node in nodes),
            async_function_count=sum(isinstance(node, ast.AsyncFunctionDef) for node in nodes),
        )
    try:
        value = json.loads(text, parse_constant=_reject_json_constant)
    except json.JSONDecodeError as exc:
        return SourceStats(kind, "syntax_error", error_line=exc.lineno,
                           error_column=exc.colno)
    except ValueError:
        return SourceStats(kind, "syntax_error")
    if isinstance(value, dict):
        return SourceStats(kind, "ok", top_level_type="object",
                           top_level_key_count=len(value))
    if isinstance(value, list):
        value_type = "array"
    elif isinstance(value, str):
        value_type = "string"
    elif isinstance(value, bool):
        value_type = "boolean"
    elif value is None:
        value_type = "null"
    else:
        value_type = "number"
    return SourceStats(kind, "ok", top_level_type=value_type)


def analyze_source_file(path: str | os.PathLike[str]) -> SourceStats:
    """Route .py/.json case-insensitively; unsupported types are not opened."""
    suffix = Path(path).suffix.lower()
    kind = {".py": "python", ".json": "json"}.get(suffix)
    if kind is None:
        return SourceStats("unknown", "unsupported_type")
    data, status, error_code = read_file_bytes(path)
    if data is None:
        return SourceStats(kind, status, error_code=error_code)
    return analyze_source_bytes(data, kind=kind)
