"""Subprocess checks for the documented direct-script entry point."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "cli.py"


class CliChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.input = self.root / "input"
        self.input.mkdir()
        (self.input / "a.py").write_bytes(b"def example(): pass\n")
        (self.input / "skip.txt").write_bytes(b"skip")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(CLI), *map(str, args)],
                              cwd=self.root, capture_output=True, text=True, timeout=15)

    def test_help_requires_no_output_and_lists_commands(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        for command in ("scan", "stats", "manifest"):
            self.assertIn(command, result.stdout)
        self.assertIn("--output", self.run_cli("scan", "--help").stdout)

    def test_missing_output_is_an_error_without_generated_files(self):
        result = self.run_cli("scan", self.input)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["input"])

    def test_all_commands_write_expected_detail_and_apply_exclusion(self):
        for command in ("scan", "manifest", "stats"):
            output = self.root / (command + ".json")
            result = self.run_cli(command, self.input, "--output", output,
                                  "--exclude", "*.txt")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(report["detail"], command)
            self.assertEqual([f["path"] for f in report["files"]], ["a.py"])
            self.assertEqual("sha256" in report["files"][0], command != "scan")
            self.assertEqual("source" in report["files"][0], command == "stats")
            self.assertNotIn(str(self.root), output.read_text())
            self.assertNotIn(str(self.root), result.stdout)

    def test_csv_and_markdown_and_output_self_omission(self):
        for format in ("csv", "markdown"):
            output = self.root / ("summary." + format)
            result = self.run_cli("stats", self.input, "--format", format, "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("a.py", output.read_text())
        output = self.input / "new.json"
        self.assertEqual(self.run_cli("manifest", self.input, "--output", output).returncode, 0)
        self.assertNotIn("new.json", [f["path"] for f in json.loads(output.read_text())["files"]])

    def test_invalid_input_existing_output_and_runtime_output_fail_safely(self):
        output = self.root / "report.json"
        output.write_text("keep")
        self.assertEqual(self.run_cli("scan", self.input, "--output", output).returncode, 2)
        self.assertEqual(output.read_text(), "keep")
        missing = self.run_cli("scan", self.root / "missing", "--output", self.root / "new.json")
        self.assertEqual(missing.returncode, 2)
        self.assertNotIn(str(self.root), missing.stderr)
        runtime = CLI.parents[2] / "data" / "b1-report.json"
        self.assertEqual(self.run_cli("scan", self.input, "--output", runtime).returncode, 2)
        self.assertFalse(runtime.exists())


if __name__ == "__main__":
    unittest.main()
