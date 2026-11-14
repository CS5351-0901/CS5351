"""Compare generic inventory manifests without reading or modifying their files."""

from collections.abc import Mapping
from string import hexdigits

from .path_rules import normalize_relative_path


def index_manifest(manifest: Mapping) -> dict:
    """Validate and copy the path, byte size, and optional hash of each entry.

    Accepts the Week 8 report schema and other mappings with a files list.
    Unknown metadata does not affect comparisons. Normalized paths must be
    unique so ambiguous snapshots cannot silently overwrite entries.
    """
    if not isinstance(manifest, Mapping) or not isinstance(manifest.get("files"), list):
        raise ValueError("Manifest must contain a files list")
    records = {}
    for item in manifest["files"]:
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
            raise ValueError("Manifest entry requires a text path")
        path = normalize_relative_path(item["path"])
        if path in records:
            raise ValueError("Duplicate normalized manifest path")
        size = item.get("size_bytes")
        if type(size) is not int or size < 0:
            raise ValueError("Manifest entry requires a nonnegative integer byte size")
        digest = item.get("sha256")
        if digest is not None and (
            not isinstance(digest, str) or len(digest) != 64
            or any(character not in hexdigits for character in digest)
        ):
            raise ValueError("Manifest hash must be SHA-256 hex or null")
        records[path] = {"path": path, "size_bytes": size,
                         "sha256": digest.lower() if digest is not None else None}
    return records


def compare_snapshots(before: Mapping, after: Mapping) -> dict:
    """Report sorted path changes and after-minus-before size deltas.

    A known hash becoming unavailable, or vice versa, is a change in the
    recorded hash, not evidence that the file bytes changed.
    """
    old = index_manifest(before)
    new = index_manifest(after)
    added = [new[path] for path in sorted(new.keys() - old.keys())]
    removed = [old[path] for path in sorted(old.keys() - new.keys())]
    changed = []
    for path in sorted(old.keys() & new.keys()):
        if old[path] != new[path]:
            changed.append({
                "path": path, "before": old[path], "after": new[path],
                "size_delta_bytes": new[path]["size_bytes"] - old[path]["size_bytes"],
                "hash_changed": new[path]["sha256"] != old[path]["sha256"],
            })
    total_delta = sum(row["size_bytes"] for row in new.values()) - sum(
        row["size_bytes"] for row in old.values()
    )
    return {"added": added, "removed": removed, "changed": changed,
            "total_size_delta_bytes": total_delta}
