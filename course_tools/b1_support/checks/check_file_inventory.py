"""Explicit inventory checks using temporary fixtures only."""

import errno
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from course_tools.b1_support.file_inventory import scan_directory


class InventoryChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def make_file(self, name, content=b""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_order_sizes_extensions_and_unicode(self):
        self.make_file("z.PY", b"123")
        self.make_file("a/README", b"12")
        self.make_file("目录/代码.py", "你好".encode("utf-8"))
        result = scan_directory(self.root)
        self.assertEqual([entry.relative_path for entry in result.files],
                         ["a/README", "z.PY", "目录/代码.py"])
        self.assertEqual(result.total_files, 3)
        self.assertEqual(result.total_size_bytes, 11)
        self.assertEqual(result.extension_counts, {"": 1, ".py": 2})
        self.assertEqual(result.issues, ())

    def test_include_exclude_and_directory_pruning(self):
        self.make_file("src/a.py", b"a")
        self.make_file("src/nested/b.py", b"b")
        self.make_file("src/notes.txt", b"c")
        self.make_file("src/private/c.py", b"d")
        result = scan_directory(self.root, include=("src/**/*.py",),
                                exclude=("src/private/**",))
        self.assertEqual([entry.relative_path for entry in result.files],
                         ["src/a.py", "src/nested/b.py"])
        self.assertEqual(result.total_size_bytes, 2)

    def test_empty_directory_and_zero_byte_file(self):
        (self.root / "empty").mkdir()
        self.assertEqual(scan_directory(self.root).total_files, 0)
        self.make_file("empty/zero.txt")
        self.assertEqual(scan_directory(self.root).total_files, 1)
        self.assertEqual(scan_directory(self.root).total_size_bytes, 0)

    def test_missing_root_and_file_root_have_explicit_errors(self):
        with self.assertRaises(FileNotFoundError):
            scan_directory(self.root / "missing")
        with self.assertRaises(NotADirectoryError):
            scan_directory(self.make_file("file"))

    def test_symlinks_are_skipped_without_following_files_or_cycles(self):
        target = self.make_file("inside.txt", b"payload")
        (self.root / "file-link").symlink_to(target)
        (self.root / "directory-link").symlink_to(self.root, target_is_directory=True)
        result = scan_directory(self.root)
        self.assertEqual([entry.relative_path for entry in result.files], ["inside.txt"])
        self.assertEqual([(issue.relative_path, issue.reason) for issue in result.issues],
                         [("directory-link", "symlink_skipped"),
                          ("file-link", "symlink_skipped")])
        with self.assertRaises(ValueError):
            scan_directory(self.root / "directory-link")

    def test_excluded_symlink_is_not_traversed_or_reported(self):
        (self.root / "ignored-link").symlink_to(self.root, target_is_directory=True)
        result = scan_directory(self.root, exclude=("ignored-link",))
        self.assertEqual(result.files, ())
        self.assertEqual(result.issues, ())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO fixtures need POSIX")
    def test_special_file_is_reported_without_opening_it(self):
        os.mkfifo(self.root / "pipe")
        result = scan_directory(self.root)
        self.assertEqual(result.files, ())
        self.assertEqual(result.issues[0].reason, "special_file_skipped")

    def test_scan_failure_is_relative_and_structured(self):
        failure = PermissionError(errno.EACCES, "unreadable", str(self.root))
        with patch("course_tools.b1_support.file_inventory.os.scandir", side_effect=failure):
            result = scan_directory(self.root)
        self.assertEqual(result.files, ())
        self.assertEqual(result.issues[0].relative_path, ".")
        self.assertEqual(result.issues[0].reason, "scan_error")
        self.assertEqual(result.issues[0].error_code, errno.EACCES)
        self.assertNotIn(str(self.root), repr(result))

    def test_stat_failure_is_reported_without_aborting_other_files(self):
        self.make_file("good.txt", b"ok")
        with os.scandir(self.root) as iterator:
            real_entries = list(iterator)
        entry = Mock(name="broken_entry")
        entry.name = "missing.txt"
        entry.stat.side_effect = FileNotFoundError(errno.ENOENT, "gone")
        with patch("course_tools.b1_support.file_inventory.os.scandir") as scandir:
            scandir.return_value.__enter__.return_value = iter(real_entries + [entry])
            result = scan_directory(self.root)
        self.assertEqual([file.relative_path for file in result.files], ["good.txt"])
        self.assertEqual(result.issues[0].relative_path, "missing.txt")
        self.assertEqual(result.issues[0].reason, "stat_error")

    def test_scan_needs_no_file_contents(self):
        self.make_file("binary.bin", b"\x00\xff")
        with patch.object(Path, "open", side_effect=AssertionError("must not read files")):
            result = scan_directory(self.root)
        self.assertEqual(result.total_size_bytes, 2)

    @unittest.skipUnless(os.name == "posix", "These names are POSIX-only fixtures")
    def test_nonportable_names_are_reported_without_path_aliases(self):
        self.make_file("a\\b.txt", b"a")
        self.make_file("C:notes.txt", b"b")
        result = scan_directory(self.root)
        self.assertEqual(result.files, ())
        self.assertEqual([issue.reason for issue in result.issues],
                         ["nonportable_path_skipped", "nonportable_path_skipped"])

    def test_scan_is_repeatable_and_leaves_fixture_unchanged(self):
        self.make_file("b.txt", b"b")
        self.make_file("nested/a.txt", b"abc")
        def snapshot():
            return {p.relative_to(self.root).as_posix():
                    (p.read_bytes(), p.stat().st_mtime_ns)
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        self.assertEqual(scan_directory(self.root), scan_directory(self.root))
        self.assertEqual(snapshot(), before)


if __name__ == "__main__":
    unittest.main()
