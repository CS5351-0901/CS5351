"""Diff two B2 artifact manifests.

Reports added / removed / changed relative paths and per-extension count deltas.
Deterministic: all output lists are sorted, and the delta dict is key-sorted.
"""

from typing import Dict, List

from artifact_manifest import ArtifactEntry


def _index(entries: List[ArtifactEntry]) -> Dict[str, ArtifactEntry]:
    return {entry.relative_path: entry for entry in entries}


def category_count_delta(
    old_entries: List[ArtifactEntry],
    new_entries: List[ArtifactEntry],
) -> Dict[str, int]:
    """Return per-extension count delta (new count - old count, non-zero only)."""
    counts: Dict[str, int] = {}
    for entry in old_entries:
        counts[entry.extension] = counts.get(entry.extension, 0) - 1
    for entry in new_entries:
        counts[entry.extension] = counts.get(entry.extension, 0) + 1
    return {key: value for key, value in sorted(counts.items()) if value != 0}


def diff_manifests(
    old_entries: List[ArtifactEntry],
    new_entries: List[ArtifactEntry],
) -> Dict[str, object]:
    """Return added / removed / changed paths plus category count delta."""
    old = _index(old_entries)
    new = _index(new_entries)

    old_paths = set(old)
    new_paths = set(new)

    added = sorted(new_paths - old_paths)
    removed = sorted(old_paths - new_paths)
    changed = sorted(
        path
        for path in (old_paths & new_paths)
        if old[path].sha256 != new[path].sha256
    )

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "category_count_delta": category_count_delta(old_entries, new_entries),
    }
