"""Explicit static Python and JSON checks using isolated byte fixtures."""

import errno
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from course_tools.b1_support.source_stats import analyze_source_bytes, analyze_source_file


class SourceStatChecks(unittest.TestCase):
    def test_python_counts_nested_classes_sync_and_async_separately(self):
        source = b"""class A:
    def method(self):
        def nested():
            pass
    async def worker(self):
        pass
class B:
    pass
async def task():
    pass
"""
        result = analyze_source_bytes(source, kind="python")
        self.assertEqual(result.status, "ok")
        self.assertEqual((result.class_count, result.function_count, result.async_function_count),
                         (2, 2, 2))

    def test_python_is_parsed_without_running_top_level_statements(self):
        result = analyze_source_bytes(b'raise RuntimeError("must never run")', kind="python")
        self.assertEqual(result.status, "ok")
        self.assertEqual((result.class_count, result.function_count), (0, 0))

    def test_python_syntax_error_has_position_and_unknown_counts(self):
        result = analyze_source_bytes(b"def broken(\n", kind="python")
        self.assertEqual(result.status, "syntax_error")
        self.assertEqual(result.error_line, 1)
        self.assertIsNone(result.function_count)

    def test_decoding_failures_are_stable_for_both_kinds(self):
        for kind in ("python", "json"):
            for data, status in ((b"\x00", "binary_like"), (b"\xff", "invalid_utf8")):
                with self.subTest(kind=kind, data=data):
                    result = analyze_source_bytes(data, kind=kind)
                    self.assertEqual(result.status, status)
                    self.assertIsNone(result.class_count)
                    self.assertIsNone(result.top_level_key_count)

    def test_utf8_bom_and_unicode_sources(self):
        self.assertEqual(analyze_source_bytes(
            "\ufeffdef 你好():\n    pass\n".encode("utf-8"), kind="python"
        ).function_count, 1)
        self.assertEqual(analyze_source_bytes(
            '\ufeff{"名字": 1}'.encode("utf-8"), kind="json"
        ).top_level_key_count, 1)

    def test_json_counts_unique_top_level_keys_only(self):
        result = analyze_source_bytes(b'{"a":{"nested":1},"b":2,"a":3}', kind="json")
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.top_level_type, "object")
        self.assertEqual(result.top_level_key_count, 2)
        self.assertEqual(analyze_source_bytes(b"{}", kind="json").top_level_key_count, 0)

    def test_non_object_json_is_valid_without_object_key_count(self):
        for data, value_type in ((b"[]", "array"), (b'"text"', "string"),
                                 (b"true", "boolean"), (b"null", "null"), (b"1.5", "number")):
            with self.subTest(data=data):
                result = analyze_source_bytes(data, kind="json")
                self.assertEqual(result.status, "ok")
                self.assertEqual(result.top_level_type, value_type)
                self.assertIsNone(result.top_level_key_count)

    def test_bad_json_and_nonstandard_numeric_constants_are_reported(self):
        result = analyze_source_bytes(b'{\n"a": }', kind="json")
        self.assertEqual(result.status, "syntax_error")
        self.assertEqual(result.error_line, 2)
        for data in (b"", b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(data=data):
                self.assertEqual(analyze_source_bytes(data, kind="json").status, "syntax_error")

    def test_file_routing_and_missing_file_results(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "code.PY"
            source.write_bytes(b"class Example: pass")
            self.assertEqual(analyze_source_file(source).class_count, 1)
            config = root / "config.JSON"
            config.write_bytes(b'{"a": 1}')
            self.assertEqual(analyze_source_file(config).top_level_key_count, 1)
            missing = analyze_source_file(root / "missing.py")
            self.assertEqual(missing.status, "read_error")
            self.assertEqual(missing.error_code, errno.ENOENT)
            self.assertNotIn(temporary, repr(missing))

    def test_unsupported_types_are_not_opened(self):
        with patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
            result = analyze_source_file("unselected.txt")
        self.assertEqual((result.kind, result.status), ("unknown", "unsupported_type"))

    def test_unknown_explicit_kind_is_a_caller_error(self):
        with self.assertRaises(ValueError):
            analyze_source_bytes(b"", kind="javascript")


if __name__ == "__main__":
    unittest.main()
