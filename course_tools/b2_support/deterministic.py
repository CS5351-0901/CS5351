"""Deterministic seeding utilities.

The whole B2 support toolkit must be seed-deterministic: the same seed
produces the same generated cases on every run. Uses only the stdlib `random`
module seeded from a stable integer derived from the given seed value.
"""

import random
from typing import List, Optional


def seed_to_int(seed) -> int:
    """Map an arbitrary seed value to a stable 32-bit integer.

    `None` maps to a fixed default so repeated calls are reproducible.
    """
    if seed is None:
        seed = 20261025
    h = 0
    for ch in str(seed):
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def make_rng(seed=None) -> random.Random:
    """Create a deterministic random.Random instance from a seed."""
    return random.Random(seed_to_int(seed))


def stable_strings(seed: Optional[int] = None, count: int = 4) -> List[str]:
    """Return `count` deterministic strings for a given seed."""
    rng = make_rng(seed)
    base = seed_to_int(seed)
    return [f"s{base}_{i}_{rng.random():.9f}" for i in range(count)]
