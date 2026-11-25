"""Pure report rendering and explicitly requested, restricted output writes."""

import csv
import html
import io
import json
import tempfile
from pathlib import Path


def render_report(report: dict, format: str = "json") -> str:
    if format == "json":
        return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if format == "csv":
        def safe_cell(value):
            text = str(value)
            return "'" + text if text.startswith(("=", "+", "-", "@", "\t", "\r")) else text
        stream = io.StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["record_type", "path", "extension", "size_bytes", "sha256",
                         "status", "total_lines", "file_count"])
        summary = report["summary"]
        writer.writerow(["summary", "", "", summary["total_size_bytes"], "", "",
                         summary.get("total_lines", ""), summary["file_count"]])
        for item in report["files"]:
            # Keep spreadsheet applications from interpreting filenames as formulas.
            name = safe_cell(item["path"])
            writer.writerow(["file", name, item["extension"], item["size_bytes"],
                             item.get("sha256", ""), item.get("content_status", ""),
                             item.get("text", {}).get("total_lines", ""), ""])
        for issue in report["issues"]:
            writer.writerow(["issue", safe_cell(issue["relative_path"]), "", "", "", issue["reason"], "", ""])
        return stream.getvalue()
    if format == "markdown":
        def cell(value):
            return html.escape(str(value)).replace("\r", "\\r").replace("\n", "\\n").replace("|", "\\|")
        summary = report["summary"]
        lines = ["# B1 Repository Summary", "",
                 f"Files: {summary['file_count']}; bytes: {summary['total_size_bytes']}; "
                 f"issues: {summary['issue_count']}", "",
                 "| Path | Extension | Bytes | Status |", "| --- | --- | ---: | --- |"]
        for item in report["files"]:
            lines.append("| " + " | ".join(cell(value) for value in (
                item["path"], item["extension"], item["size_bytes"],
                item.get("content_status", "metadata_only"))) + " |")
        if report["issues"]:
            lines.extend(["", "## Inventory issues", ""])
            lines.extend(f"- {cell(issue['relative_path'])}: {cell(issue['reason'])}"
                         for issue in report["issues"])
        return "\n".join(lines) + "\n"
    raise ValueError("Format must be json, csv, or markdown")


def validate_output_path(output) -> Path:
    """Allow system temp, own evidence, or own .tmp; never repository runtime.

    Existing files and symlink outputs are refused, including allowed targets.
    Resolving ancestors prevents a symlink directory from escaping the policy.
    """
    candidate = Path(output)
    if candidate.is_symlink():
        raise ValueError("Output must not be a symbolic link")
    target = candidate.resolve()
    repository = Path(__file__).resolve().parents[2]
    evidence = repository / "course_evidence" / "B1"
    own_temp = repository / "course_tools" / "b1_support" / ".tmp"
    own_allowed = target.is_relative_to(evidence) or target.is_relative_to(own_temp)
    if target.is_relative_to(repository) and not own_allowed:
        raise ValueError("Output is outside B1 report locations")
    if not own_allowed and not target.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise ValueError("Output must be in temporary storage or B1 report locations")
    if target.exists():
        raise ValueError("Output already exists; choose a new file")
    return target


def write_report(report: dict, *, output, format: str = "json") -> None:
    target = validate_output_path(output)
    content = render_report(report, format)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="") as stream:
        stream.write(content)
