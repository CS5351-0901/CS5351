"""Manifest determinism, content levels and relative-path contracts."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from course_tools.b1_support.manifest_builder import build_manifest


class ManifestChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "z.py").write_bytes(b"def example(): pass\n")
        (self.root / "配置.json").write_bytes(b'{"key": 1}')

    def test_repeatable_content_independent_of_machine_root(self):
        first = build_manifest(self.root)
        with tempfile.TemporaryDirectory() as temporary:
            other = Path(temporary)
            for path in self.root.iterdir():
                (other / path.name).write_bytes(path.read_bytes())
            self.assertEqual(first, build_manifest(other))
        self.assertEqual(first, build_manifest(self.root))
        self.assertNotIn(str(self.root), json.dumps(first))
        self.assertEqual([f["path"] for f in first["files"]], ["z.py", "配置.json"])
        self.assertEqual(first["files"][0]["sha256"],
                         hashlib.sha256(b"def example(): pass\n").hexdigest())

    def test_scan_never_reads_content(self):
        with patch("course_tools.b1_support.manifest_builder.read_file_bytes",
                   side_effect=AssertionError("no content reads")):
            result = build_manifest(self.root, detail="scan")
        self.assertNotIn("sha256", result["files"][0])
        self.assertEqual(result["summary"]["file_count"], 2)

    def test_stats_include_real_python_and_json_analysis(self):
        result = build_manifest(self.root, detail="stats")
        self.assertEqual(result["files"][0]["source"]["function_count"], 1)
        self.assertEqual(result["files"][1]["source"]["top_level_key_count"], 1)
        self.assertEqual(result["summary"]["total_lines"], 2)

    def test_filters_and_exact_omission_update_summary(self):
        result = build_manifest(self.root, include=("*.py",), exclude=("z.py",))
        self.assertEqual(result["summary"]["file_count"], 0)
        result = build_manifest(self.root, omit_paths=("z.py",))
        self.assertEqual(result["summary"]["extension_counts"], {".json": 1})
        self.assertEqual(result["summary"]["total_size_bytes"], 10)

    def test_content_failures_and_symlinks_are_structured(self):
        (self.root / "bad.py").write_bytes(b"\xff")
        (self.root / "link").symlink_to(self.root, target_is_directory=True)
        result = build_manifest(self.root, detail="stats")
        self.assertEqual(result["files"][0]["content_status"], "invalid_utf8")
        self.assertEqual(result["files"][0]["source"]["status"], "invalid_utf8")
        self.assertEqual(result["issues"][0]["reason"], "symlink_skipped")
        with patch("course_tools.b1_support.manifest_builder.read_file_bytes",
                   return_value=(None, "read_error", 13)):
            self.assertEqual(build_manifest(self.root)["files"][0]["error_code"], 13)

    def test_invalid_detail_and_missing_directory(self):
        with self.assertRaises(ValueError):
            build_manifest(self.root, detail="unknown")
        with self.assertRaises(FileNotFoundError):
            build_manifest(self.root / "missing")


if __name__ == "__main__":
    unittest.main()
