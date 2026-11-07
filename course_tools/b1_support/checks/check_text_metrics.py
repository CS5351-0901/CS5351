"""Explicit checks for text metrics and stable unreadable-input results."""

import errno
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from course_tools.b1_support.text_metrics import analyze_text_bytes, analyze_text_file


class TextMetricChecks(unittest.TestCase):
    def test_empty_input_has_zero_counts(self):
        result = analyze_text_bytes(b"")
        self.assertEqual(result.status, "ok")
        self.assertEqual((result.total_lines, result.blank_lines, result.nonblank_lines), (0, 0, 0))
        self.assertEqual((result.max_line_length, result.average_line_length), (0, 0.0))

    def test_blank_lines_and_trailing_newline_have_explicit_counts(self):
        result = analyze_text_bytes(b"abc\n \t\n\nxy\n")
        self.assertEqual((result.total_lines, result.blank_lines, result.nonblank_lines), (4, 2, 2))
        self.assertEqual(result.max_line_length, 3)
        self.assertEqual(result.average_line_length, 1.75)

    def test_crlf_and_cr_separators_are_not_counted_in_lengths(self):
        result = analyze_text_bytes(b"ab\r\nc\rd")
        self.assertEqual(result.total_lines, 3)
        self.assertEqual(result.max_line_length, 2)
        self.assertAlmostEqual(result.average_line_length, 4 / 3)

    def test_unicode_lengths_are_codepoints_and_size_is_bytes(self):
        result = analyze_text_bytes("你好\n\u2003\n🙂a".encode("utf-8"))
        self.assertEqual(result.total_lines, 3)
        self.assertEqual(result.blank_lines, 1)
        self.assertEqual(result.max_line_length, 2)
        self.assertEqual(result.size_bytes, 16)
        self.assertAlmostEqual(result.average_line_length, 5 / 3)

    def test_sha256_matches_known_value_and_preserves_raw_newlines(self):
        self.assertEqual(analyze_text_bytes(b"abc").sha256,
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        self.assertNotEqual(analyze_text_bytes(b"a\n").sha256,
                            analyze_text_bytes(b"a\r\n").sha256)

    def test_bom_is_ignored_for_text_but_included_in_hash(self):
        result = analyze_text_bytes(b"\xef\xbb\xbfabc")
        self.assertEqual(result.max_line_length, 3)
        self.assertEqual(result.sha256, hashlib.sha256(b"\xef\xbb\xbfabc").hexdigest())

    def test_binary_controls_return_hash_without_text_counts(self):
        for data in (b"a\x00b", b"\x01", b"\x7f", b"\xff\x00"):
            with self.subTest(data=data):
                result = analyze_text_bytes(data)
                self.assertEqual(result.status, "binary_like")
                self.assertIsNone(result.total_lines)
                self.assertIsNone(result.average_line_length)
                self.assertEqual(result.sha256, hashlib.sha256(data).hexdigest())

    def test_invalid_utf8_is_distinct_from_binary_like(self):
        result = analyze_text_bytes(b"abc\xff")
        self.assertEqual(result.status, "invalid_utf8")
        self.assertIsNone(result.nonblank_lines)
        self.assertEqual(result.size_bytes, 4)

    def test_file_api_is_repeatable_and_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "文档.txt"
            data = "hello\n你好".encode("utf-8")
            path.write_bytes(data)
            before = path.stat().st_mtime_ns
            self.assertEqual(analyze_text_file(path), analyze_text_bytes(data))
            self.assertEqual(path.read_bytes(), data)
            self.assertEqual(path.stat().st_mtime_ns, before)
            self.assertEqual(sorted(p.name for p in Path(temporary).iterdir()), ["文档.txt"])

    def test_missing_or_unreadable_file_has_no_path_or_os_message(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "missing"
            result = analyze_text_file(path)
            self.assertEqual(result.status, "read_error")
            self.assertEqual(result.error_code, errno.ENOENT)
            self.assertIsNone(result.sha256)
            self.assertNotIn(temporary, repr(result))
            with patch.object(Path, "stat", side_effect=PermissionError(errno.EACCES, "private")):
                self.assertEqual(analyze_text_file(path).error_code, errno.EACCES)

    def test_directory_is_rejected_without_reading(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
                self.assertEqual(analyze_text_file(temporary).status, "not_regular_file")


if __name__ == "__main__":
    unittest.main()
