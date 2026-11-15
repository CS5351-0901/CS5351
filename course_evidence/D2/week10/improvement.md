# D2 Week 10 Sprint 3 improvement

## Engineering improvement

Added a built-in Python syntax validation step to the D2 security and quality scanner. The scanner now parses Python input with the standard-library AST before optional external tools run. A syntax error is recorded as a structured `QualityIssue` with its source line and checker name, sets `syntax_valid` to false, forces the quality score to 0, and causes the report and CLI command to fail.

This closes a dependency-boundary gap: invalid Python could previously retain a passing heuristic quality score when Ruff, Mypy, or Bandit was unavailable. The improvement does not require any optional package and does not change shared `main.py` code.

Added `tests/roles/d2/test_python_syntax.py` with API and CLI regression coverage for invalid and valid Python input.

## Validation

`RUNTIME_TEST: PASS`

Executed `python.exe -m pytest -p no:cacheprovider tests/roles/d2 -q` with Python 3.14.6 and pytest 9.1.1: **15 passed in 1.57s**. This includes the 12 existing D2 tests and three Week 10 syntax-validation tests.
