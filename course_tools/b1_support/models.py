"""Immutable inventory records containing only relative paths and metadata."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FileEntry:
    relative_path: str
    extension: str
    size_bytes: int


@dataclass(frozen=True)
class InventoryIssue:
    relative_path: str
    reason: str
    error_code: int | None = None


@dataclass(frozen=True)
class InventoryResult:
    files: tuple[FileEntry, ...]
    issues: tuple[InventoryIssue, ...] = ()

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_size_bytes(self) -> int:
        return sum(entry.size_bytes for entry in self.files)

    @property
    def extension_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in self.files:
            counts[entry.extension] = counts.get(entry.extension, 0) + 1
        return dict(sorted(counts.items()))
