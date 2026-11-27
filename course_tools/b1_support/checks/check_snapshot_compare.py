"""Snapshot change, size delta, hash and manifest validation checks."""

import copy
import tempfile
import unittest
from pathlib import Path

from course_tools.b1_support.manifest_builder import build_manifest
from course_tools.b1_support.snapshot_compare import compare_snapshots


class SnapshotChecks(unittest.TestCase):
    def test_added_removed_changed_and_total_byte_delta(self):
        old = {"files": [{"path": "removed.txt", "size_bytes": 2},
                         {"path": "data.bin", "size_bytes": 5, "sha256": "a" * 64}]}
        new = {"files": [{"path": "data.bin", "size_bytes": 8, "sha256": "b" * 64},
                         {"path": "new.txt", "size_bytes": 4}]}
        copies = copy.deepcopy((old, new))
        result = compare_snapshots(old, new)
        self.assertEqual([row["path"] for row in result["added"]], ["new.txt"])
        self.assertEqual([row["path"] for row in result["removed"]], ["removed.txt"])
        change, = result["changed"]
        self.assertEqual(change["path"], "data.bin")
        self.assertEqual(change["size_delta_bytes"], 3)
        self.assertTrue(change["hash_changed"])
        self.assertEqual((change["before"]["sha256"], change["after"]["sha256"]),
                         ("a" * 64, "b" * 64))
        self.assertEqual(result["total_size_delta_bytes"], 5)
        self.assertEqual((old, new), copies)

    def test_metadata_order_and_hash_case_do_not_change_snapshot(self):
        old = {"files": [{"path": "z", "size_bytes": 0},
                         {"path": "./目录/a.py", "size_bytes": 1, "sha256": "A" * 64}]}
        new = {"files": [{"path": "目录/a.py", "size_bytes": 1, "sha256": "a" * 64,
                          "extension": ".py"}, {"path": "z", "size_bytes": 0}]}
        self.assertEqual(compare_snapshots(old, new),
                         {"added": [], "removed": [], "changed": [],
                          "total_size_delta_bytes": 0})

    def test_unavailable_hash_and_size_only_delta_are_explicit(self):
        old = {"files": [{"path": "a", "size_bytes": 3, "sha256": "a" * 64},
                         {"path": "b", "size_bytes": 3}]}
        new = {"files": [{"path": "b", "size_bytes": 1},
                         {"path": "a", "size_bytes": 3}]}
        a, b = compare_snapshots(old, new)["changed"]
        self.assertEqual((a["path"], a["size_delta_bytes"], a["hash_changed"]),
                         ("a", 0, True))
        self.assertIsNone(a["after"]["sha256"])
        self.assertEqual((b["path"], b["size_delta_bytes"], b["hash_changed"]),
                         ("b", -2, False))

    def test_invalid_manifests_are_rejected(self):
        cases = (
            {},
            {"files": [{"path": "../escape", "size_bytes": 0}]},
            {"files": [{"path": "a", "size_bytes": True}]},
            {"files": [{"path": "a", "size_bytes": -1}]},
            {"files": [{"path": "a", "size_bytes": 1, "sha256": "z" * 64}]},
            {"files": [{"path": "a", "size_bytes": 1},
                       {"path": "./a", "size_bytes": 2}]},
        )
        for manifest in cases:
            with self.subTest(manifest=manifest), self.assertRaises(ValueError):
                compare_snapshots({"files": []}, manifest)

    def test_week8_manifests_detect_same_size_content_edits(self):
        with tempfile.TemporaryDirectory() as temporary:
            file = Path(temporary) / "input.txt"
            file.write_bytes(b"abc")
            before = build_manifest(temporary)
            file.write_bytes(b"xyz")
            result = compare_snapshots(before, build_manifest(temporary))
            change, = result["changed"]
            self.assertEqual(change["size_delta_bytes"], 0)
            self.assertTrue(change["hash_changed"])
            self.assertEqual(file.read_bytes(), b"xyz")


if __name__ == "__main__":
    unittest.main()
