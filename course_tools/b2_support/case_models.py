"""Generic case data models for the B2 support toolkit.

The toolkit only ever deals with plain data (strings), never with business
modules, filesystem side effects, or other members' formats.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class StringCase:
    """A single generated string case."""

    case_id: str
    label: str
    category: str
    value: str


@dataclass(frozen=True)
class PathCase:
    """A single generated path case, kept as a plain string only.

    The toolkit never touches the filesystem; a PathCase value is purely
    illustrative string data.
    """

    case_id: str
    label: str
    style: str  # one of: posix / windows / relative / unicode
    value: str


def required_string_categories() -> Tuple[str, ...]:
    """The string categories the generator must cover."""
    return ("empty", "whitespace", "unicode", "emoji", "long_text", "newline", "tab")


def required_path_styles() -> Tuple[str, ...]:
    """The path styles the generator must cover."""
    return ("posix", "windows", "relative", "unicode")
