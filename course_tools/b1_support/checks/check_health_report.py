"""Opt-in checks for the read-only health report and support self-audit."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from course_tools.b1_support.health_report import build_health_report
from course_tools.b1_support.self_audit import REQUIRED_MODULES, _audit_tree, audit_support


class HealthReportChecks(unittest.TestCase):
    def test_inventory_totals_filters_and_relative_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, data in (
                ("示例.py", b"123"), ("readme", b"abcd"), ("ignore.py", b"ignore"),
                (".git/config", b"ignored"), ("__pycache__/x.pyc", b"ignored"),
            ):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            with patch.object(Path, "read_bytes", side_effect=AssertionError("metadata only")):
                report = build_health_report(root, exclude=("ignore.py",))
                self.assertEqual(report, build_health_report(root, exclude=("ignore.py",)))
            self.assertEqual(report, {
                "file_count": 2,
                "total_size_bytes": 7,
                "extensions": {
                    "": {"file_count": 1, "size_bytes": 4},
                    ".py": {"file_count": 1, "size_bytes": 3},
                },
                "issue_count": 0,
                "issue_counts": {},
            })
            self.assertNotIn(temporary, repr(report))
            self.assertEqual(build_health_report(root, include=("*.py",))["file_count"], 2)

    def test_empty_and_missing_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(build_health_report(root)["extensions"], {})
            with self.assertRaises(FileNotFoundError):
                build_health_report(root / "missing")
            with self.assertRaises(TypeError):
                build_health_report(root, exclude="*.txt")

    def test_inventory_issues_are_counted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            try:
                (root / "link").symlink_to(root)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable")
            report = build_health_report(root)
            self.assertEqual(report["file_count"], 0)
            self.assertEqual(report["issue_count"], 1)
            self.assertEqual(report["issue_counts"], {"symlink_skipped": 1})


class SelfAuditChecks(unittest.TestCase):
    def test_installed_support_tree_passes(self):
        report = audit_support()
        self.assertTrue(report["passed"], report["issues"])
        self.assertGreaterEqual(report["files_checked"], len(REQUIRED_MODULES))

    def test_audit_reports_missing_and_forbidden_patterns_without_execution(self):
        samples = {
            "health_report.py": (
                "import main\nimport requests\nimport socket\nfrom .. import b2_support\n"
                "raise RuntimeError('must not execute')\n"
            ),
            "cli.py": (
                "from pathlib import Path\nimport os\n"
                "target = Path('/machine/config.json')\n"
                "target.write_text('change')\nopen('settings.json', mode='w')\n"
                "os.environ['SETTING'] = 'change'\n__import__('other')\n"
            ),
            "models.py": "def invalid(:\n",
            "path_rules.py": "from . import cli\nimport re\n",
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, source in samples.items():
                (root / name).write_text(source, encoding="utf-8")
            report = _audit_tree(root)
            self.assertFalse(report["passed"])
            self.assertEqual(report["files_checked"], 4)
            self.assertNotIn(temporary, repr(report))
            codes_by_file = {}
            for issue in report["issues"]:
                codes_by_file.setdefault(issue["path"], set()).add(issue["code"])
            self.assertEqual(codes_by_file["health_report.py"],
                             {"outside_support_import", "network_import"})
            self.assertEqual(codes_by_file["cli.py"],
                             {"absolute_path_literal", "runtime_mutation", "dynamic_import"})
            self.assertEqual(codes_by_file["models.py"], {"syntax_error"})
            self.assertEqual(codes_by_file["snapshot_compare.py"], {"missing_module"})
            self.assertNotIn("path_rules.py", codes_by_file)


if __name__ == "__main__":
    unittest.main()
