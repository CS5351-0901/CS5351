"""Portable relative paths and case-sensitive include/exclude glob rules."""

import os
from fnmatch import fnmatchcase
from functools import lru_cache
from pathlib import PurePosixPath, PureWindowsPath
from typing import Iterable


def normalize_relative_path(value: str | os.PathLike[str]) -> str:
    """Return a POSIX relative path; reject absolute paths and parent traversal."""
    text = os.fspath(value)
    if not isinstance(text, str):
        raise TypeError("A path must be text")
    text = text.replace("\\", "/")
    if "\x00" in text or text.startswith("/") or PureWindowsPath(text).drive:
        raise ValueError("A path must be relative and contain no NUL bytes")
    parts = text.split("/")
    if ".." in parts:
        raise ValueError("Parent traversal is not permitted")
    normalized = "/".join(part for part in parts if part not in ("", "."))
    if not normalized:
        raise ValueError("A path must identify a relative entry")
    return normalized


def normalize_patterns(patterns: Iterable[str]) -> tuple[str, ...]:
    """Validate a pattern collection, rather than interpreting one string as it."""
    if isinstance(patterns, (str, bytes)):
        raise TypeError("Patterns must be a collection of strings")
    return tuple(normalize_relative_path(pattern) for pattern in patterns)


def matches_pattern(relative_path: str, pattern: str) -> bool:
    """Match a basename glob or a root-relative glob with recursive ** segments.

    A pattern without slashes matches a basename at any depth. With slashes it
    is rooted at the inventory directory; ** matches zero or more segments.
    """
    path = normalize_relative_path(relative_path)
    glob = normalize_relative_path(pattern)
    if "/" not in glob and glob != "**":
        return fnmatchcase(path.rsplit("/", 1)[-1], glob)
    path_parts = path.split("/")
    pattern_parts = glob.split("/")

    @lru_cache(maxsize=None)
    def match(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        segment = pattern_parts[pattern_index]
        if segment == "**":
            return match(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and match(path_index + 1, pattern_index)
            )
        return (
            path_index < len(path_parts)
            and fnmatchcase(path_parts[path_index], segment)
            and match(path_index + 1, pattern_index + 1)
        )

    return match(0, 0)


def matches_path(
    relative_path: str, *, include: Iterable[str] = (), exclude: Iterable[str] = ()
) -> bool:
    """Select all paths by default; exclusions take priority over inclusions."""
    path = normalize_relative_path(relative_path)
    inclusions = normalize_patterns(include)
    exclusions = normalize_patterns(exclude)
    return (
        not any(matches_pattern(path, pattern) for pattern in exclusions)
        and (not inclusions or any(matches_pattern(path, pattern) for pattern in inclusions))
    )


def classify_extension(relative_path: str) -> str:
    """Return the lowercase final suffix, or an empty string for suffixless files."""
    suffix = PurePosixPath(normalize_relative_path(relative_path)).suffix.lower()
    # Python versions differ on whether a terminal dot is a suffix.
    return "" if suffix == "." else suffix
