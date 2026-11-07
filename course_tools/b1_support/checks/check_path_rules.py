"""Explicit unittest checks for B1 support path and filtering contracts."""

import unittest
from pathlib import PurePosixPath

from course_tools.b1_support.path_rules import (
    classify_extension, matches_path, matches_pattern, normalize_patterns,
    normalize_relative_path,
)


class PathRuleChecks(unittest.TestCase):
    def test_normalize_separators_and_dot_segments(self):
        self.assertEqual(normalize_relative_path("./src\\nested//./a.py"), "src/nested/a.py")
        self.assertEqual(normalize_relative_path(PurePosixPath("src/a.py")), "src/a.py")

    def test_preserve_unicode_and_filename_spaces(self):
        self.assertEqual(normalize_relative_path("目录/ 文件.py"), "目录/ 文件.py")

    def test_reject_absolute_parent_empty_and_nul_paths(self):
        for value in ("/root/a", "C:\\files\\a", "C:a", "\\\\server\\share", "../a",
                      "src/../a", "", ".", "a\x00b"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_relative_path(value)

    def test_reject_bytes_and_single_string_pattern_collection(self):
        with self.assertRaises(TypeError):
            normalize_relative_path(b"a.py")
        with self.assertRaises(TypeError):
            normalize_patterns("*.py")

    def test_basename_glob_matches_at_any_depth_and_is_case_sensitive(self):
        self.assertTrue(matches_pattern("src/a.py", "*.py"))
        self.assertTrue(matches_pattern("a.py", "*.py"))
        self.assertFalse(matches_pattern("src/a.PY", "*.py"))

    def test_recursive_glob_matches_zero_or_many_directories(self):
        for path in ("src/a.py", "src/nested/a.py", "src/deep/nested/a.py"):
            with self.subTest(path=path):
                self.assertTrue(matches_pattern(path, "src/**/*.py"))
        self.assertTrue(matches_pattern("src", "src/**"))
        self.assertTrue(matches_pattern("any/path", "**"))

    def test_single_segment_wildcard_does_not_cross_directory(self):
        self.assertTrue(matches_pattern("src/a.py", "src/*.py"))
        self.assertFalse(matches_pattern("src/nested/a.py", "src/*.py"))
        self.assertFalse(matches_pattern("other/src/a.py", "src/*.py"))

    def test_exclusions_win_and_empty_inclusions_select_all(self):
        self.assertTrue(matches_path("README"))
        self.assertTrue(matches_path("src/a.py", include=("*.py",)))
        self.assertFalse(matches_path("src/a.txt", include=("*.py",)))
        self.assertFalse(matches_path("src/private/a.py", include=("*.py",),
                                      exclude=("src/private/**",)))

    def test_invalid_pattern_is_rejected_even_for_nonmatching_path(self):
        with self.assertRaises(ValueError):
            matches_path("a.py", include=("../*.py",))

    def test_extension_uses_final_suffix_and_handles_dotfiles(self):
        cases = {"file.PY": ".py", "archive.tar.gz": ".gz", "README": "",
                 ".gitignore": "", "file.": "", "目录/代码.JSON": ".json"}
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(classify_extension(path), expected)


if __name__ == "__main__":
    unittest.main()
