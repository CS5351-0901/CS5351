"""Baseline tests for the D2 security and quality scanner."""

import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "CodeAgent"
    / "scripts"
    / "codeagent_security.py"
)


def load_security_module():
    spec = importlib.util.spec_from_file_location("codeagent_security", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_security_report_escalates_high_and_critical_findings():
    module = load_security_module()
    report = module.SecurityReport(file_path="sample.py")

    report.add_finding(
        module.SecurityFinding(
            level=module.RiskLevel.HIGH,
            category="security",
            message="high-risk pattern",
            line=1,
        )
    )

    assert report.risk_level is module.RiskLevel.HIGH
    assert report.passed is False


def test_scan_code_detects_dynamic_execution_as_critical():
    module = load_security_module()
    report = module.scan_code("result = eval(user_input)\n", "sample.py", "python")

    assert report.risk_level is module.RiskLevel.CRITICAL
    assert report.passed is False
    assert any(f.category == "dangerous_pattern" for f in report.findings)


def test_scan_code_dispatches_shell_and_reports_tool_status():
    module = load_security_module()
    report = module.scan_code("rm -rf /\n", "sample.sh", "auto")

    assert report.file_path == "sample.sh"
    assert report.quality_score >= 0
    assert any(finding.category == "tool_error" for finding in report.findings)


def test_unsupported_language_returns_low_risk_finding():
    module = load_security_module()
    report = module.scan_code("console.log('ok')", "sample.js", "javascript")

    assert report.risk_level is module.RiskLevel.LOW
    assert report.passed is True
    assert report.findings[0].category == "unsupported"


def test_security_report_json_is_serializable_and_contains_results():
    module = load_security_module()
    report = module.scan_code("def safe(value):\n    return value\n", "sample.py", "python")

    payload = json.loads(report.to_json())

    assert payload["file_path"] == "sample.py"
    assert "quality_score" in payload
    assert "test_results" in payload
