"""Week 10 Python syntax validation tests for the D2 scanner."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


SCRIPT_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "CodeAgent"
    / "scripts"
    / "codeagent_security.py"
)


def load_security_module():
    spec = importlib.util.spec_from_file_location("codeagent_security_week10", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_invalid_python_fails_without_optional_external_tools():
    module = load_security_module()
    scanner = module.CodeSecurityScanner()

    report = scanner.scan_python("def broken(:\n    pass\n", "broken.py")

    syntax_issue = next(
        issue for issue in report.quality_issues
        if issue.category == "syntax"
    )
    assert report.passed is False
    assert report.quality_score == 0
    assert report.quality_details["syntax_valid"] is False
    assert syntax_issue.line == 1
    assert syntax_issue.tool == "ast"


def test_valid_python_records_successful_syntax_check():
    module = load_security_module()

    report = module.scan_code(
        "def identity(value):\n    return value\n",
        "valid.py",
        "python",
    )

    assert report.quality_details["syntax_valid"] is True
    assert not any(issue.category == "syntax" for issue in report.quality_issues)


def test_cli_returns_failed_report_for_invalid_python():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--code",
            "def broken(:\n    pass",
            "--language",
            "python",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["passed"] is False
    assert payload["quality_score"] == 0
    assert payload["quality_details"]["syntax_valid"] is False
    assert payload["quality_issues"][0]["category"] == "syntax"
