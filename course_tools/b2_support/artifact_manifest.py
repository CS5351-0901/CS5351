"""Build a deterministic artifact manifest for a B2-owned directory tree.

Only operates on files under a caller-provided root. Records relative path,
size, SHA-256 and extension. Deterministic: entries are sorted by relative path
and paths use POSIX separators. No runtime state, no other member's tooling.
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ArtifactEntry:
    """One file in a manifest."""

    relative_path: str
    size: int
    sha256: str
    extension: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "relative_path": self.relative_path,
            "size": self.size,
            "sha256": self.sha256,
            "extension": self.extension,
        }


def sha256_file(path: Path) -> str:
    """Return the hex SHA-256 of a file read in binary chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    root: str | Path,
    extensions: Optional[List[str]] = None,
) -> List[ArtifactEntry]:
    """Build a sorted manifest of files under root.

    extensions optionally filters by lower-case extension without the leading
    dot. Paths are relative to root and use '/' separators.
    """
    root_path = Path(root)
    if not root_path.exists():
        return []

    allowed = None
    if extensions is not None:
        allowed = {ext.lower().lstrip(".") for ext in extensions}

    entries: List[ArtifactEntry] = []
    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root_path).as_posix()
        ext = path.suffix.lower().lstrip(".")
        if allowed is not None and ext not in allowed:
            continue
        entries.append(
            ArtifactEntry(
                relative_path=rel,
                size=path.stat().st_size,
                sha256=sha256_file(path),
                extension=ext,
            )
        )

    entries.sort(key=lambda entry: entry.relative_path)
    return entries


def manifest_to_dicts(entries: List[ArtifactEntry]) -> List[Dict[str, object]]:
    """Serialize a manifest to a list of plain dicts."""
    return [entry.to_dict() for entry in entries]
