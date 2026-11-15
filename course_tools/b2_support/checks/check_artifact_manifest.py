#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the artifact manifest builder."""

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from artifact_manifest import build_manifest, manifest_to_dicts, sha256_file


class CheckArtifactManifestTest(unittest.TestCase):
    def test_fields_and_sorting(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.txt").write_text("hello", encoding="utf-8")
            (root / "sub").mkdir()
            (root / "sub" / "b.py").write_text("print(1)", encoding="utf-8")

            entries = build_manifest(root)
            self.assertEqual([e.relative_path for e in entries], ["a.txt", "sub/b.py"])

            first = entries[0]
            self.assertEqual(first.size, 5)
            self.assertEqual(first.extension, "txt")
            self.assertEqual(first.sha256, hashlib.sha256(b"hello").hexdigest())

    def test_deterministic_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "x.md").write_text("one", encoding="utf-8")
            (root / "y.md").write_text("two", encoding="utf-8")
            a = json.dumps(manifest_to_dicts(build_manifest(root)), sort_keys=True)
            b = json.dumps(manifest_to_dicts(build_manifest(root)), sort_keys=True)
            self.assertEqual(a, b)

    def test_empty_or_missing_root(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(build_manifest(Path(td)), [])
        self.assertEqual(build_manifest(Path(tempfile.gettempdir()) / "b2_no_such_dir_xyz"), [])

    def test_extension_filter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "keep.py").write_text("a", encoding="utf-8")
            (root / "skip.txt").write_text("b", encoding="utf-8")
            entries = build_manifest(root, extensions=["py"])
            self.assertEqual([e.relative_path for e in entries], ["keep.py"])

    def test_sha256_matches_file_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "f.bin"
            data = b"\x00\x01\x02unicode-" + "中文".encode("utf-8")
            path.write_bytes(data)
            expected = hashlib.sha256(data).hexdigest()
            self.assertEqual(sha256_file(path), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
