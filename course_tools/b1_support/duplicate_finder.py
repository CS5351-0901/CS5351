"""Report content-hash duplicate groups from a manifest; never touch its files."""

from collections.abc import Iterable, Mapping

from .path_rules import classify_extension
from .snapshot_compare import index_manifest


def find_duplicates(
    manifest: Mapping, *, extensions: Iterable[str] | None = None,
    min_size: int = 0, max_size: int | None = None,
) -> list[dict]:
    """Group entries with the same recorded SHA-256 and byte size.

    Filters are applied before grouping. Sizes are inclusive, and extensions
    are case-insensitive final suffixes with or without a leading dot.
    An empty extension string selects suffixless files. Unknown hashes never
    form groups. The report trusts the snapshot; it does not reread bytes.
    """
    if type(min_size) is not int or min_size < 0:
        raise ValueError("Minimum size must be a nonnegative integer")
    if max_size is not None and (type(max_size) is not int or max_size < min_size):
        raise ValueError("Maximum size must be an integer at least as large as minimum")
    allowed = None
    if extensions is not None:
        if isinstance(extensions, (str, bytes)):
            raise ValueError("Extensions must be a collection of strings")
        allowed = set()
        for extension in extensions:
            if not isinstance(extension, str):
                raise ValueError("Extensions must be strings")
            suffix = extension.lower()
            allowed.add("." + suffix if suffix and not suffix.startswith(".") else suffix)

    buckets: dict[tuple[str, int], list[str]] = {}
    for path, entry in sorted(index_manifest(manifest).items()):
        size, digest = entry["size_bytes"], entry["sha256"]
        if digest is None or size < min_size or (max_size is not None and size > max_size):
            continue
        if allowed is not None and classify_extension(path) not in allowed:
            continue
        buckets.setdefault((digest, size), []).append(path)
    return [
        {"sha256": digest, "size_bytes": size, "paths": paths,
         "redundant_bytes": size * (len(paths) - 1)}
        for (digest, size), paths in sorted(buckets.items()) if len(paths) > 1
    ]
