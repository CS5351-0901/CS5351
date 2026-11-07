# D2 Week 6 change

## Engineering change

Added a D2-owned shell dangerous-pattern check in `skills/CodeAgent/scripts/codeagent_security.py`. Shell scans now independently flag recursive deletion of `/` (including `-rf`/`-fr` and `--no-preserve-root` forms) and `eval` as CRITICAL before relying on ShellCheck. This closes the Week 5 gap where a missing ShellCheck executable produced only a LOW tool-error finding and did not identify these dangerous commands.

Added regression coverage in `tests/roles/d2/test_security_baseline.py` for root deletion when ShellCheck is unavailable, dynamic shell evaluation, and a scoped `/tmp` recursive delete that should not trigger the root-deletion rule.

## Validation

`RUNTIME_TEST: PASS`

Executed `python.exe -m pytest tests/roles/d2 -q` with Python 3.14.6 and pytest 9.1.1: **7 passed**. This includes the root-deletion, `eval`, and scoped-delete regression checks.

`STATIC_PATTERN_CHECK: PASS` — checked the rule expressions in PowerShell against `rm -rf /`, `rm -fr /`, both `--no-preserve-root` placements, the non-root `/tmp/build` case, and `eval`. This does not replace running the Python tests.

## Repository state

The provided project directory and its parent do not contain Git metadata, so Git diff/status and the Week 6 local commit could not be performed. No GitHub push or PR action was attempted, as requested.
