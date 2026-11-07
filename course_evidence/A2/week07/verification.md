# Week 7 — A2 Boundary and Failure-Path Verification

Recorded: 2026-10-25. Target: Week 7. This checkpoint follows the A2 handbook's contract/boundary verification step, after the separate Week 6 cleanup fix was committed and pushed.

## Engineering increment

Added seven executable regressions to `tests/roles/a2/test_orchestration.py`. They exercise the real command generator with controlled AstrBot imports and helper boundaries. Week 7 changes only A2 tests and this evidence; it adds no production change.

| Case | Contract or boundary checked |
| --- | --- |
| Close an unstarted generator | Closing a command that never ran must not remove an existing session. |
| Interleave two users | Closing one user's command must leave the other user's session intact; closing both releases both entries. |
| Zero debug budget | No sandbox execution, checking, or packaging begins, and the session is released. This checks command behavior, not configuration validation. |
| Success on the final allowed retry | A failed first attempt followed by success uses exactly two attempts and proceeds to checking, snapshotting, and packaging once. |
| Malformed sandbox response | A `None` response reaches the existing error path; downstream checks and packaging do not run, and the session is released. |
| Snapshot failure | A simulated disk error is reported and packaging does not begin; the command releases its session. |
| Reply-rendering failure | If both the normal reply and error reply cannot be built, the exception reaches the caller after session cleanup. |

These cases extend Week 6's explicit close/cancellation coverage. They check session isolation, retry limits, and behavior when adjacent components fail, rather than asserting that a helper was merely called.

## Validation performed

Interpreter: Python 3.14.6 on Windows. Commands run from the course repository root:

```text
python -B -m unittest discover -s tests/roles/a2 -p 'test_*.py' -v
python -m ruff check tests/roles/a2/test_orchestration.py
git -c core.whitespace=cr-at-eol diff --check
```

All 26 A2 tests passed: the 19 existing tests and seven new Week 7 cases. There were no failures, skips, or expected failures; unittest exited 0. Ruff reported `All checks passed!`, and the whitespace check passed. No failing production behavior was found in these new cases, so no additional source fix was made this week.

## Limits and remaining work

Interleaving two generators is an isolation check, not a load test or proof of live AstrBot concurrency. The malformed-result case exercises the current exception handler; it does not add a formal response-schema validator. The retry test controls sandbox results and does not show that generated code was actually repaired. Live loader startup, actual subprocess cancellation, real snapshot disk failures, and adapter delivery were not exercised.

The Week 6 limitations still apply: callers must close an abandoned generator for immediate cleanup, and synchronous subprocess work can delay cancellation. These remain visible for later integration review.

## Submission scope

Week 6 remains a separate commit, `417b726`, containing the owned command fix and its evidence. Week 7 uses the handbook commit message `test(a2): week 07 expand verification` and is pushed to `course/a2`. Sprint 2 PR review/integration remains scheduled for Week 9. No A2 Week 8 or later files are included.
