"""Report rendering and output-boundary checks using temporary fixtures."""

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from course_tools.b1_support.report_writer import render_report, validate_output_path, write_report


class ReportChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.report = {"summary": {"file_count": 1, "total_size_bytes": 2, "issue_count": 0},
                       "files": [{"path": "目录/a|b.txt", "extension": ".txt", "size_bytes": 2}],
                       "issues": []}
        self.repository = Path(__file__).resolve().parents[3]

    def test_all_formats_are_repeatable_and_preserve_summary(self):
        self.assertEqual(json.loads(render_report(self.report)), self.report)
        rows = list(csv.reader(io.StringIO(render_report(self.report, "csv"))))
        self.assertEqual(rows[1][0], "summary")
        self.assertEqual(rows[1][-1], "1")
        self.assertEqual(rows[2][1], "目录/a|b.txt")
        markdown = render_report(self.report, "markdown")
        self.assertIn("目录/a\\|b.txt", markdown)
        for format in ("json", "csv", "markdown"):
            self.assertEqual(render_report(self.report, format), render_report(self.report, format))

    def test_temp_output_is_explicit_and_never_overwritten(self):
        output = self.root / "nested" / "report.json"
        write_report(self.report, output=output)
        self.assertEqual(json.loads(output.read_text()), self.report)
        with self.assertRaises(ValueError):
            write_report({}, output=output)
        self.assertEqual(json.loads(output.read_text()), self.report)

    def test_runtime_other_roles_and_generic_repo_paths_are_rejected(self):
        for relative in ("data/report.json", "course_evidence/B2/report.json", "report.json",
                         "course_tools/b1_support/report.json", "main.py"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                validate_output_path(self.repository / relative)
        with self.assertRaises(ValueError):
            validate_output_path(self.repository.parent / "outside-b1-report.json")

    def test_own_evidence_and_own_temporary_locations_are_allowed(self):
        for relative in ("course_evidence/B1/week08/new-report.json",
                         "course_tools/b1_support/.tmp/report.json"):
            self.assertEqual(validate_output_path(self.repository / relative),
                             self.repository / relative)

    def test_symlink_output_and_escape_parent_are_rejected(self):
        target = self.root / "target"
        target.write_text("keep")
        link = self.root / "link"
        link.symlink_to(target)
        with self.assertRaises(ValueError):
            validate_output_path(link)
        directory = self.root / "escape"
        directory.symlink_to(self.repository, target_is_directory=True)
        with self.assertRaises(ValueError):
            validate_output_path(directory / "data/report.json")
        self.assertEqual(target.read_text(), "keep")

    def test_invalid_format_creates_nothing(self):
        output = self.root / "not-created" / "report"
        with self.assertRaises(ValueError):
            write_report(self.report, output=output, format="invalid")
        self.assertFalse(output.parent.exists())

    def test_markdown_escapes_markup_and_csv_disables_filename_formulas(self):
        self.report["files"][0]["path"] = "=SUM(1,2)<tag>\nfile"
        markdown = render_report(self.report, "markdown")
        self.assertNotIn("<tag>", markdown)
        self.assertIn("\\nfile", markdown)
        rows = list(csv.reader(io.StringIO(render_report(self.report, "csv"))))
        self.assertTrue(rows[2][1].startswith("'="))


if __name__ == "__main__":
    unittest.main()
