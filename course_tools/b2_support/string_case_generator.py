"""Generate generic string cases as plain data.

Produces cases covering the required categories:
empty / whitespace / Unicode / emoji / long text / newline / tab.
The generator never calls any business module and never touches the filesystem.
"""

from typing import List, Optional

from case_models import StringCase
from deterministic import make_rng


def generate_string_cases(seed: Optional[int] = None) -> List[StringCase]:
    """Return a deterministic list of string cases for the given seed."""
    _ = make_rng(seed)  # keep seeding stable even if the value list is constant
    cases: List[StringCase] = []

    def add(label: str, category: str, value: str) -> None:
        cases.append(
            StringCase(
                case_id=f"str_{len(cases) + 1:03d}",
                label=label,
                category=category,
                value=value,
            )
        )

    add("empty", "empty", "")
    add("spaces_only", "whitespace", "   ")
    add("tab_only", "whitespace", "\t")
    add("unicode_chinese", "unicode", "你好世界 计算器 π")
    add("emoji", "emoji", "hello \U0001F680 \u2705 world")
    add("long_text", "long_text", "x" * 5000)
    add("newline", "newline", "line1\nline2\nline3")
    add("tabs", "tab", "a\tb\tc")

    return cases
