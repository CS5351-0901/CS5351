"""Generate generic path cases as plain string data.

Covers POSIX / Windows / relative / Unicode path strings. Path values are
kept as strings only; the toolkit never resolves, opens or creates any real
path (no dangerous filesystem access).
"""

from typing import List, Optional

from case_models import PathCase
from deterministic import make_rng


def generate_path_cases(seed: Optional[int] = None) -> List[PathCase]:
    """Return a deterministic list of path cases for the given seed."""
    _ = make_rng(seed)  # keep seeding stable even if the value list is constant
    cases: List[PathCase] = []

    def add(label: str, style: str, value: str) -> None:
        cases.append(
            PathCase(
                case_id=f"path_{len(cases) + 1:03d}",
                label=label,
                style=style,
                value=value,
            )
        )

    add("posix_absolute", "posix", "/home/user/project/scripts/main.py")
    add("posix_tilde", "posix", "~/workspace/repo")
    add("posix_relative", "relative", "data/inputs/sample.txt")
    add("windows_drive", "windows", "C:\\Users\\b2\\data\\out.csv")
    add("windows_backslash_rel", "relative", "build\\dist\\app.exe")
    add("unicode_posix", "unicode", "/\u6570\u636e/\u8f93\u5165/\u6d4b\u8bd5\u6587\u4ef6.txt")

    return cases
