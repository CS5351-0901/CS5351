#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the corpus diff."""

import json
import sys
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from artifact_manifest import ArtifactEntry
from corpus_diff import diff_manifests, category_count_delta


def _entry(path, size, digest, ext):
    return ArtifactEntry(relative_path=path, size=size, sha256=digest, extension=ext)


class CheckCorpusDiffTest(unittest.TestCase):
    def test_added_removed_changed(self):
        old = [
            _entry("keep.txt", 1, "h1", "txt"),
            _entry("gone.txt", 1, "h2", "txt"),
            _entry("edit.py", 1, "h3", "py"),
        ]
        new = [
            _entry("keep.txt", 1, "h1", "txt"),
            _entry("fresh.py", 1, "h4", "py"),
            _entry("edit.py", 2, "h5", "py"),
        ]
        diff = diff_manifests(old, new)
        self.assertEqual(diff["added"], ["fresh.py"])
        self.assertEqual(diff["removed"], ["gone.txt"])
        self.assertEqual(diff["changed"], ["edit.py"])

    def test_category_count_delta(self):
        old = [
            _entry("a.txt", 1, "h1", "txt"),
            _entry("b.txt", 1, "h2", "txt"),
            _entry("c.py", 1, "h3", "py"),
        ]
        new = [
            _entry("a.txt", 1, "h1", "txt"),
            _entry("d.py", 1, "h4", "py"),
            _entry("e.py", 1, "h5", "py"),
        ]
        delta = category_count_delta(old, new)
        self.assertEqual(delta["txt"], -1)
        self.assertEqual(delta["py"], 1)

    def test_no_change(self):
        same = [_entry("a.py", 1, "h1", "py"), _entry("b.txt", 1, "h2", "txt")]
        diff = diff_manifests(same, list(same))
        self.assertEqual(diff["added"], [])
        self.assertEqual(diff["removed"], [])
        self.assertEqual(diff["changed"], [])
        self.assertEqual(diff["category_count_delta"], {})

    def test_unchanged_files_not_reported(self):
        old = [_entry("same.txt", 5, "stable", "txt"), _entry("swap.txt", 1, "old", "txt")]
        new = [_entry("same.txt", 5, "stable", "txt"), _entry("swap.txt", 1, "new", "txt")]
        diff = diff_manifests(old, new)
        self.assertNotIn("same.txt", diff["added"] + diff["removed"] + diff["changed"])
        self.assertEqual(diff["changed"], ["swap.txt"])

    def test_deterministic(self):
        old = [_entry("z.txt", 1, "a", "txt"), _entry("a.txt", 1, "b", "txt")]
        new = [_entry("m.txt", 1, "c", "txt")]
        first = json.dumps(diff_manifests(old, new), sort_keys=True)
        second = json.dumps(diff_manifests(old, new), sort_keys=True)
        self.assertEqual(first, second)
        self.assertEqual(diff_manifests(old, new)["added"], ["m.txt"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
