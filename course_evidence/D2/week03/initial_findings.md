WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Initial static findings

## Responsibilities observed

- `codeagent_security.py` defines the report model, language-specific checkers, security pattern checks, quality scoring, and generated-test path.
- `main.py::_call_security_scan` launches the security script and deserializes its stdout. The main flow calls it for non-JavaScript/TypeScript projects, then checks `risk_level` and `quality_score`.
- `SecurityReport` marks HIGH and CRITICAL findings as not passed. Missing Ruff, Mypy, or Bandit is represented by a LOW `tool_error` finding in the Python scan path; ShellCheck absence is handled similarly in the shell scan path.

## Failure behavior to validate from Week 5 onward

- The caller returns `passed=True` when the security script is missing.
- Any exception while starting the subprocess or parsing its output also returns `passed=True`. The subprocess return code is not checked before stdout is parsed.
- The caller's exception fallback does not include `risk_level` or `quality_score`; the main flow defaults those fields and does not branch directly on `passed` or `error`.
- Checker-tool absence is reported at LOW risk, so tests should establish whether an unavailable checker can still result in a report treated as acceptable by the caller.
- Add regression/failure-path coverage for missing script, nonzero subprocess exit, empty or malformed JSON, missing checker tools, and HIGH/CRITICAL findings. Verify both the `passed` flag and the fields actually consumed by `main.py`.

These are code-reading observations and proposed validation items, not demonstrated runtime behavior.

RUNTIME_TEST: NOT_RUN
