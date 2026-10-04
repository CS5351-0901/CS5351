# D2 Week 5 baseline

## Scope

This week adds the first executable D2 baseline under `tests/roles/d2/`. The tests cover the owned security-report and scanner contract without changing `main.py` or the shared scanner implementation.

Covered behaviors:

- HIGH findings escalate `SecurityReport.risk_level` and set `passed` to `False`.
- Python scanning detects dynamic execution (`eval`) as a CRITICAL dangerous pattern.
- Automatic language dispatch selects the Shell scan path and reports missing ShellCheck as a tool error.
- Unsupported languages produce a LOW unsupported-language finding.
- `SecurityReport.to_json()` produces a JSON object containing quality and test-result fields.

## Validation

`RUNTIME_TEST: PARTIAL`

- Standard-library execution of all five baseline functions: **PASS** (`STANDARD_LIBRARY_BASELINE_PASS 5 tests`).
- Pytest execution: **NOT_RUN**. The available Python 3.14.6 environment reports `No module named pytest`.

The direct execution is a lightweight fallback for this dependency-limited environment. It does not claim pytest collection, fixtures, coverage, or plugin behavior.

## Findings and follow-up

The initial Shell test assumed that the Shell path reused the Python dangerous-pattern checker. The executed baseline showed that the current implementation instead reports missing ShellCheck as a LOW `tool_error`; the test was corrected to assert the implemented Shell-path contract. A future D2 verification should decide whether dangerous-pattern checks belong in the Shell path and add a regression test if that behavior is changed.

This Week 5 artifact is limited to D2's test directory and evidence directory. No business-source file was modified.
