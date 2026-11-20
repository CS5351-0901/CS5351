# A1 Week 11 — Regression / Cleanup

Recorded: 2026-11-20 (Asia/Singapore). Owner: A1. Week 10 was committed first as `b59ef6f1a310a0b992f9031e99f8966f883fc690`.

## Regression and failure paths

The A1 Week 10 change in `_ensure_js_dependencies` avoids accepting an incomplete `node_modules` directory as a completed dependency installation. Week 11 added `tests/roles/a1/test_week11_recovery.py` with five executable tests for a failed install followed by a retry, an unavailable Node binary, an empty dependency manifest, scoped npm package paths, and a nonmapping manifest that must warn instead of claiming successful installation.

Executed on Windows with Miniconda Python 3.13.2:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests/roles/a1 -p test_*.py -q
Ran 38 tests
OK
```

A1: 38/38 PASS (28 previous tests plus 5 Week 10 plus 5 Week 11).

Additional checks of the integrated branch were actually run using `PYTHONUTF8=1`: A2 26/26 PASS; B1 role 14/14 PASS; B2 role 29/29 PASS; C1 10/10 PASS; C2 22/22 PASS; D1 25/25 PASS; B1 V3 support 62 total, 2 SKIPPED, 0 failures; B2 V3 support 51/51 PASS. D2's 12 pytest-style free functions were directly executed successfully because pytest is not installed in the runner. The JavaScript checker's `node --check` exited 0; four key Python files parsed successfully with `ast.parse`. These are role/regression checks, not full live AstrBot integration.

## Source-leakage and provenance check

Read-only text scan of the 175 Git-tracked files at the check point, covering source-directory names, local absolute source paths, source-repository/commit/provenance metadata fields, and public Git repository links, returned:

- Original source directory names: 0 hits.
- Absolute source workspace paths: 0 hits.
- Source provenance metadata fields: 0 hits.
- External repository URLs: 0 hits.
- Course repository URLs: 20 occurrences, all targeting the team's own `CS5351-0901/CS5351` GitHub repository and PRs; retained as real course evidence.
- One contextual full commit ID: in A1 Week 9 evidence, explicitly labeled `origin/main` and referring to the course repository's own Sprint 2 baseline; it is not an external source commit. This legitimate audit evidence was retained, not deleted.

No suspected original-source leakage was identified in this text scan. It is not a forensic audit of untracked files, binaries, or all Git history.

## Cleanup and remaining technical debt

The observed A1 incomplete-install handling was corrected in Week 10 and is now covered by Week 11 retry/boundary tests; no unrelated production refactor was introduced. Remaining A1 limitations: the checker only verifies package directory presence, not package versions/integrity, npm installs and Node.js platform download paths are mocked, and a real AstrBot initialization and full startup latency test have not been performed. Do not call these unrun checks PASS.

WEEK11_A1_REGRESSION: 38/38 PASS
WEEK11_A1_FAILURE_PATH_CHECKS: 5 NEW TESTS
WEEK11_A1_FORBIDDEN_SOURCE_METADATA: NO CONFIRMED HITS
WEEK11_A1_REAL_NPM_INSTALL: NOT_RUN
WEEK11_A1_LIVE_ASTRBOT: NOT_RUN
WEEK12_WEEK13_WORK: NOT_STARTED
