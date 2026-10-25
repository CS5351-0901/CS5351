"""Week 7 boundary and contract tests for the D2 security scanner."""

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
    spec = importlib.util.spec_from_file_location("codeagent_security_week7", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unavailable_shellcheck(scanner):
    scanner.shellcheck_checker.check = lambda code, file_path: {
        "error": "ShellCheck unavailable",
        "issues": [],
    }


def test_shell_root_delete_contract_reports_exact_source_line():
    module = load_security_module()
    scanner = module.CodeSecurityScanner()
    unavailable_shellcheck(scanner)

    report = scanner.scan_shell("#!/bin/sh\n\nrm --no-preserve-root -fr /\n", "dangerous.sh")

    finding = next(
        finding for finding in report.findings
        if finding.category == "dangerous_pattern"
    )
    assert report.risk_level is module.RiskLevel.CRITICAL
    assert report.passed is False
    assert finding.line == 3
    assert finding.file_path == "dangerous.sh"
    assert finding.tool == "pattern_checker"


def test_shell_root_boundary_does_not_flag_scoped_or_prefixed_paths():
    module = load_security_module()
    scanner = module.CodeSecurityScanner()
    unavailable_shellcheck(scanner)

    report = scanner.scan_shell(
        "rm -rf /tmp/build\n"
        "rm -rf /var/tmp/cache\n"
        "echo rm -rf /tmp\n",
        "cleanup.sh",
    )

    assert report.risk_level is module.RiskLevel.LOW
    assert not any(
        finding.category == "dangerous_pattern"
        for finding in report.findings
    )


def test_shellcheck_high_issue_contract_fails_closed():
    module = load_security_module()
    scanner = module.CodeSecurityScanner()
    scanner.shellcheck_checker.check = lambda code, file_path: {
        "error": None,
        "issues": [
            {
                "line": 1,
                "severity": "high",
                "message": "unsafe shell construct",
                "suggestion": "quote the expansion",
            }
        ],
    }

    report = scanner.scan_shell("echo $user_input\n", "unsafe.sh")

    assert report.risk_level is module.RiskLevel.HIGH
    assert report.passed is False
    assert report.findings[0].category == "security"
    assert report.findings[0].tool == "shellcheck"


def test_scan_code_unknown_language_contract_is_json_serializable():
    module = load_security_module()

    report = module.scan_code("text", "sample.xyz", "unknown")
    payload = json.loads(report.to_json())

    assert report.risk_level is module.RiskLevel.LOW
    assert report.passed is True
    assert payload["risk_level"] == "RiskLevel.LOW"
    assert payload["findings"][0]["category"] == "unsupported"
