"""Read-only directory inventory; no plugin imports, file writes, or network."""

import os
import stat
from pathlib import Path
from typing import Iterable

from .models import FileEntry, InventoryIssue, InventoryResult
from .path_rules import classify_extension, matches_path, matches_pattern, normalize_patterns


def scan_directory(
    directory: str | os.PathLike[str],
    *,
    include: Iterable[str] = (),
    exclude: Iterable[str] = (),
) -> InventoryResult:
    """Inventory regular files in deterministic relative-path order.

    Metadata comes from stat calls, not file contents. Symlinks and special
    files are skipped with structured issues, preventing traversal outside the
    selected root or through link cycles. Empty directories return no files.
    Invalid roots raise explicit exceptions; entry-level OS failures are
    reported without embedding machine paths or OS exception messages.
    """
    inclusions = normalize_patterns(include)
    exclusions = normalize_patterns(exclude)
    root = Path(directory)
    try:
        root_stat = root.stat(follow_symlinks=False)
    except FileNotFoundError:
        raise FileNotFoundError("Inventory root does not exist") from None
    if stat.S_ISLNK(root_stat.st_mode):
        raise ValueError("Inventory root must not be a symbolic link")
    if not stat.S_ISDIR(root_stat.st_mode):
        raise NotADirectoryError("Inventory root must be a directory")

    files: list[FileEntry] = []
    issues: list[InventoryIssue] = []
    pending = [(root, "")]
    while pending:
        current, prefix = pending.pop()
        try:
            with os.scandir(current) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as exc:
            issues.append(InventoryIssue(prefix or ".", "scan_error", exc.errno))
            continue
        for entry in entries:
            relative_path = f"{prefix}/{entry.name}" if prefix else entry.name
            # A literal backslash in a POSIX filename cannot be represented by
            # our portable separator contract without changing its identity.
            if "\\" in entry.name or (not prefix and len(entry.name) >= 2
                                       and entry.name[1] == ":"):
                issues.append(InventoryIssue(relative_path, "nonportable_path_skipped"))
                continue
            # Prune excluded directories as well as excluding individual files.
            if any(matches_pattern(relative_path, pattern) for pattern in exclusions):
                continue
            try:
                entry_stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                issues.append(InventoryIssue(relative_path, "stat_error", exc.errno))
                continue
            mode = entry_stat.st_mode
            if stat.S_ISLNK(mode):
                issues.append(InventoryIssue(relative_path, "symlink_skipped"))
            elif stat.S_ISDIR(mode):
                pending.append((Path(entry.path), relative_path))
            elif stat.S_ISREG(mode):
                if matches_path(relative_path, include=inclusions):
                    files.append(FileEntry(
                        relative_path, classify_extension(relative_path), entry_stat.st_size
                    ))
            else:
                issues.append(InventoryIssue(relative_path, "special_file_skipped"))

    return InventoryResult(
        tuple(sorted(files, key=lambda entry: entry.relative_path)),
        tuple(sorted(issues, key=lambda issue: (
            issue.relative_path, issue.reason,
            issue.error_code if issue.error_code is not None else -1,
        ))),
    )
