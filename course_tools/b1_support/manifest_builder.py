"""Deterministic relative-path manifests; no timestamps or machine root paths."""

from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .file_inventory import scan_directory
from .source_stats import analyze_source_bytes
from .text_metrics import analyze_text_bytes, read_file_bytes


def build_manifest(directory, *, detail="manifest", include: Iterable[str] = (),
                   exclude: Iterable[str] = (), omit_paths: Iterable[str] = ()) -> dict:
    """scan uses metadata; manifest adds raw hashes; stats adds text/AST/JSON data.

    Omitted paths are exact root-relative entries (used to omit a CLI output).
    Input files may change during scanning; this is not a transactional snapshot.
    """
    if detail not in ("scan", "manifest", "stats"):
        raise ValueError("Unknown manifest detail")
    inventory = scan_directory(directory, include=include, exclude=exclude)
    omitted = set(omit_paths)
    files = []
    extensions: dict[str, int] = {}
    for entry in inventory.files:
        if entry.relative_path in omitted:
            continue
        record = {"path": entry.relative_path, "extension": entry.extension,
                  "size_bytes": entry.size_bytes}
        extensions[entry.extension] = extensions.get(entry.extension, 0) + 1
        if detail != "scan":
            data, status, error_code = read_file_bytes(Path(directory) / entry.relative_path)
            if data is None:
                record.update(sha256=None, content_status=status, error_code=error_code)
            else:
                metrics = analyze_text_bytes(data)
                record.update(sha256=metrics.sha256, content_status=metrics.status)
                if detail == "stats":
                    record["text"] = asdict(metrics)
                    kind = {".py": "python", ".json": "json"}.get(entry.extension)
                    if kind:
                        record["source"] = asdict(analyze_source_bytes(data, kind=kind))
        files.append(record)
    summary = {"file_count": len(files),
               "total_size_bytes": sum(item["size_bytes"] for item in files),
               "extension_counts": dict(sorted(extensions.items())),
               "issue_count": len(inventory.issues)}
    if detail == "stats":
        summary["total_lines"] = sum(item.get("text", {}).get("total_lines") or 0
                                     for item in files)
    return {"schema_version": 1, "detail": detail, "summary": summary,
            "files": files, "issues": [asdict(issue) for issue in inventory.issues]}
