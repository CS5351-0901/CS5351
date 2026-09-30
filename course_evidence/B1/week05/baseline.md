# Week 5 — B1 Executable Baseline

## Engineering change

Added `tests/roles/b1/test_role_baseline.py`, which imports the actual course `main.py` with minimal AstrBot import stubs and exercises B1's three owned helpers without running plugin initialization. Its seven tests cover plain and mentioned `/agent` requests, multiline and blank requirements, user and group blacklist normalization, project-type precedence, and the 29/30/99/100-character size boundaries.

The new tests first exposed two failures in `_extract_requirement`: a multiline request lost everything after its first line, and an all-whitespace request returned an empty string instead of `None`. Within the B1-owned method, both capture patterns now require a non-whitespace first requirement character and allow later newline characters. The method signature and return contract are unchanged; no other `main.py` method was edited.

## Validation performed

- Before the source fix: `python3 -m unittest discover -s tests/roles/b1 -v` — FAIL, 2 of 7 tests failed on the two cases above.
- After the source fix: `python3 -m unittest discover -s tests/roles/b1 -v` — PASS, 7 tests ran.
- `python3 -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS, exit code 0.
- `git -c core.whitespace=cr-at-eol diff --check` — PASS, no whitespace errors. The repository's `main.py` uses CRLF line endings; the default `git diff --check` reports the CR bytes on changed lines as trailing whitespace without this rule.

## Limits and next gate

These tests call the real helpers in isolation. They do not exercise installed AstrBot startup, event dispatch, or a full coding session. This Week 5 work remains under local review; the Week 5 commit, push, Sprint 1 PR, merge, and branch synchronization are pending the user's later instruction.
