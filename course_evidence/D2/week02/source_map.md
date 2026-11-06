WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# D2 source map

This map records static relationships visible in the supplied project workspace. The course remote's current `main` was not available for comparison, so this is not a claim that the remote has the same revision.

| Owned area | Observed responsibility | Relationship |
| --- | --- | --- |
| `skills/CodeAgent/scripts/codeagent_security.py` | Defines `RiskLevel`, `SecurityFinding`, `QualityIssue`, and `SecurityReport`; checker classes for Ruff, Mypy, Bandit, and ShellCheck; `CodeSecurityScanner`; and the `scan_code` entry point. | Builds security findings and quality/test details, then returns a `SecurityReport`. |
| `SecurityReport` and related checker/test classes | `SecurityReport.add_finding` raises the report risk level and sets `passed=False` for HIGH or CRITICAL findings. The scanner also records tool errors and invokes its test-generation path. | The report exposes `risk_level`, `passed`, `quality_score`, `test_coverage`, `test_results`, and a JSON representation. |
| `main.py::_call_security_scan` | Runs `codeagent_security.py` in a subprocess with the code and language arguments, then parses stdout as JSON. | The project flow calls this helper for non-JavaScript/TypeScript code and uses the returned risk level and quality score. |

The observations above are static only; no remote comparison or runtime validation is claimed.
