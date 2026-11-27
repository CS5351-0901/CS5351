"""Read-only repository inventory totals for manual inspection."""

from collections import Counter

from .file_inventory import scan_directory


def build_health_report(directory, *, include=(), exclude=()) -> dict:
    """Summarize file counts, byte sizes, and inventory issues by category.

    Git metadata and Python bytecode caches are skipped. The report uses
    file metadata only and describes the selected tree without scoring code.
    """
    if isinstance(exclude, (str, bytes)):
        raise TypeError("Exclusions must be a collection of patterns")
    inventory = scan_directory(
        directory, include=include, exclude=(".git", "__pycache__", *exclude)
    )
    extension_bytes = Counter()
    for entry in inventory.files:
        extension_bytes[entry.extension] += entry.size_bytes
    return {
        "file_count": len(inventory.files),
        "total_size_bytes": inventory.total_size_bytes,
        "extensions": {
            extension: {"file_count": count, "size_bytes": extension_bytes[extension]}
            for extension, count in inventory.extension_counts.items()
        },
        "issue_count": len(inventory.issues),
        "issue_counts": dict(sorted(Counter(issue.reason for issue in inventory.issues).items())),
    }
