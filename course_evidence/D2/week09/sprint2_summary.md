# D2 Week 9 Sprint 2 summary

## Sprint 2 engineering artifacts

- Week 6: added shell dangerous-pattern checks for root-recursive deletion and `eval`, with regression coverage.
- Week 7: added boundary and contract tests for shell command paths, finding metadata, ShellCheck failure/high-severity behavior, and unsupported-language JSON output.
- Week 8: reviewed upstream integration and corrected `SecurityReport.to_json()` to serialize `RiskLevel` values as lowercase strings accepted by `main.py`'s security gate; added a CLI regression test.

The D2 changes are limited to the owned security scanner, D2 role tests, and D2 evidence. No `main.py` change was needed: upstream edits since the reviewed common base were outside `_call_security_scan`.

## Validation

`RUNTIME_TEST: PASS`

Re-ran the complete role suite for Week 9:

```text
python.exe -m pytest -p no:cacheprovider tests/roles/d2 -q
12 passed in 1.19s
```

The suite includes the baseline, Week 6 scanner regression, Week 7 boundary/contract checks, and Week 8 CLI serialization integration test. Python 3.14.6 and pytest 9.1.1 were used.

## Remaining risks

- ShellCheck tool behavior is tested with injected success/failure responses; an end-to-end run against an installed ShellCheck executable remains unverified.
- The supplied local checkout has no local commits and remains on an unborn `master` branch. The remote `course/d2` contains Week 6–8 artifacts, but this Week 9 summary has not been committed or pushed.

## Next sprint goals

Sprint 3 should add a second role-owned engineering improvement, expand regression checks around failure and boundary behavior, rerun the full D2 suite, and prepare final presentation evidence before Week 13 closeout.
