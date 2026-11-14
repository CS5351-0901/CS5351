"""Duplicate groups, filtering, and read-only manifest checks."""

import copy
import tempfile
import unittest
from pathlib import Path

from course_tools.b1_support.duplicate_finder import find_duplicates
from course_tools.b1_support.manifest_builder import build_manifest


class DuplicateChecks(unittest.TestCase):
    def test_groups_match_both_hash_and_size_in_stable_order(self):
        manifest = {"files": [
            {"path": "z.txt", "size_bytes": 3, "sha256": "a" * 64},
            {"path": "c.txt", "size_bytes": 4, "sha256": "a" * 64},
            {"path": "a.txt", "size_bytes": 3, "sha256": "A" * 64},
            {"path": "b.txt", "size_bytes": 3, "sha256": "b" * 64},
        ]}
        copy_before = copy.deepcopy(manifest)
        expected = [{"sha256": "a" * 64, "size_bytes": 3,
                     "paths": ["a.txt", "z.txt"], "redundant_bytes": 3}]
        self.assertEqual(find_duplicates(manifest), expected)
        self.assertEqual(find_duplicates({"files": list(reversed(manifest["files"]))}), expected)
        self.assertEqual(manifest, copy_before)

    def test_extensions_and_size_filters_apply_before_grouping(self):
        manifest = {"files": [{"path": path, "size_bytes": 7, "sha256": "a" * 64}
                              for path in ("one.PY", "two.py", "three.txt", "README")]}
        group, = find_duplicates(manifest, extensions=("PY",), min_size=7, max_size=7)
        self.assertEqual(group["paths"], ["one.PY", "two.py"])
        self.assertEqual(find_duplicates(manifest, extensions=(".txt",)), [])
        self.assertEqual(find_duplicates(manifest, min_size=8), [])
        self.assertEqual(find_duplicates(manifest, max_size=6), [])

    def test_unknown_hashes_do_not_group_but_empty_files_can(self):
        manifest = {"files": [
            {"path": "one", "size_bytes": 0, "sha256": "a" * 64},
            {"path": "two", "size_bytes": 0, "sha256": "a" * 64},
            {"path": "unknown.txt", "size_bytes": 0},
            {"path": "also-unknown.txt", "size_bytes": 0, "sha256": None},
        ]}
        group, = find_duplicates(manifest, extensions=("",), max_size=0)
        self.assertEqual(group["paths"], ["one", "two"])
        self.assertEqual(group["redundant_bytes"], 0)
        self.assertEqual(find_duplicates(manifest, extensions=(".txt",)), [])

    def test_invalid_filters_and_invalid_manifest_are_rejected(self):
        for kwargs in ({"min_size": -1}, {"min_size": True},
                       {"min_size": 3, "max_size": 2}, {"extensions": "py"},
                       {"extensions": (123,)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                find_duplicates({"files": []}, **kwargs)
        with self.assertRaises(ValueError):
            find_duplicates({"files": [{"path": "/machine/path", "size_bytes": 0}]})

    def test_week8_manifest_duplicate_report_leaves_files_untouched(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = {"first.bin": b"\x00\xff", "second.bin": b"\x00\xff",
                        "different.bin": b"\x00\x01"}
            for name, data in original.items():
                (root / name).write_bytes(data)
            group, = find_duplicates(build_manifest(root))
            self.assertEqual(group["paths"], ["first.bin", "second.bin"])
            self.assertEqual({path.name: path.read_bytes() for path in root.iterdir()}, original)


if __name__ == "__main__":
    unittest.main()
