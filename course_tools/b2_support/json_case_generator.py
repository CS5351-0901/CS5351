"""Generate generic JSON cases as plain data.

Covers dict / list / nested / empty / numeric / boolean / null / Unicode values,
plus controllable malformed JSON raw text. Pure data generation: no business
module calls, no filesystem access.
"""

from typing import List, Optional, Tuple

from deterministic import make_rng


def generate_json_values(seed: Optional[int] = None) -> List[Tuple[str, object]]:
    """Return a list of (label, python_value) pairs covering the value kinds.

    The list is constant by design; `seed` is consumed only to keep the toolkit
    seed-deterministic across generators.
    """
    _ = make_rng(seed)
    return [
        ("dict", {"name": "b2", "count": 3}),
        ("list", [1, 2, 3]),
        ("nested", {"a": {"b": [1, {"c": None}]}}),
        ("empty", {}),
        ("numeric", 42),
        ("boolean", True),
        ("null", None),
        ("unicode", {"msg": "\u4f60\u597d \u4e16\u754c \u03c0"}),
    ]


def generate_malformed_json_texts(seed: Optional[int] = None) -> List[Tuple[str, str]]:
    """Return controllable malformed JSON raw text snippets.

    Each entry is (label, raw_text) where raw_text is NOT valid JSON.
    """
    _ = make_rng(seed)
    return [
        ("unterminated", '{"a": 1'),
        ("bad_token", '{"a": }'),
        ("trailing_comma", "[1, 2, ]"),
        ("unquoted_key", "{a: 1}"),
    ]


def generate_json_case_payloads(seed: Optional[int] = None) -> List[Tuple[str, object]]:
    """Alias for generate_json_values; serializable python objects."""
    return generate_json_values(seed)
