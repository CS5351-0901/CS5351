# A1 Week 13 — Final Role Closeout

Recorded: 2026-11-25. Role: metadata, configuration and environment preparation. Target: Week 13.

## Contributions and engineering evidence

Weeks 1–4 recorded role boundaries, source mapping, initial findings and course Git/integration review. Week 5 introduced the eight-test executable baseline. Sprint 2 added twelve Node/npm environment regressions in Week 6 and eight configuration/installer boundary tests in Week 7, followed by integration review and closeout in Weeks 8–9. After Sprint 2 integration, A1 PR #25 corrected the baseline's sandbox-config test to match D1's temporary JSON-file interface, checking values and cleanup.

Sprint 3 contains real engineering changes, not only reports:
- `main.py::_ensure_js_dependencies`: checks manifest-defined dependency directories before skipping npm; incomplete installations trigger the existing install route and invalid manifests warn rather than silently claiming success.
- `tests/roles/a1/test_baseline.py`: fixture updated to exercise the corrected dependency check.
- `tests/roles/a1/test_week10_js_dependencies.py` and `test_week11_recovery.py`: ten new executable tests for incomplete and complete dependency directories, failed installs and retries, manifest-defined/scoped dependencies, invalid manifests and failed Node probes.
- Week 12 presentation/report notes, including a reproducible demo and contribution summary: [presentation_notes.md](../week12/presentation_notes.md).

The A1 scope remains metadata, configuration and environment preparation; the Sprint 3 PR changes only the owned dependency helper, A1 tests and A1 evidence. The metadata/schema/project declaration files did not require speculative edits.

## Final verification actually executed

Refreshed the remote with git fetch origin --prune, confirmed a clean A1 checkout, and ran:

```text
python -B -m unittest discover -s tests/roles/a1 -p test_*.py -q
Ran 38 tests
OK
```

Windows / Miniconda Python 3.13.2, PYTHONUTF8=1, exit 0; no skipped tests or failures. The suite consists of 8 baseline + 12 Week 6 + 8 Week 7 + 5 Week 10 + 5 Week 11 tests. The current ownership-guard self-test suite also ran: 16 tests, OK, exit 0. Week 01–12 evidence exists; this file is the Week 13 evidence. The committed tree and final PR scope will be checked separately before submission/merge.

A read-only scan of the 180 tracked UTF-8 text files immediately before creating this summary found zero matches for original source-directory/path patterns, provenance fields, external repository URLs, or absolute source-workspace path patterns. Of 59 full-length hexadecimal Git references, 56 were matched against course remote history and one earlier A1 base was independently confirmed by the course repository's commit API. Two remaining references are explicitly labeled historical C2 integration-tree IDs, not external commit references; their tree objects were not independently verified. No confirmed forbidden source metadata was found. This is a pattern-based scan of tracked content, not a forensic audit of the full history or untracked data. Historical course evidence is preserved. No other role's files were changed.

## Sprint submissions and handoff

- Sprint 1: [PR #1](https://github.com/CS5351-0901/CS5351/pull/1), merged.
- Sprint 2: [PR #20](https://github.com/CS5351-0901/CS5351/pull/20), merged; integration follow-up [PR #25](https://github.com/CS5351-0901/CS5351/pull/25), merged.
- Sprint 3: final course/a1 -> main PR to be opened following this commit. Actual PR and merge state are checked separately, not assumed in this report.

Remaining limitations: the dependency check tests directory presence rather than versions, integrity or lockfile consistency. Node/npm processes and platform installers in A1's tests are mocked. No real AstrBot startup, network installation, startup latency measurement or full-team end-to-end execution was performed. Final team acceptance is separate from this role's evidence.

A1_WEEK01_13_PRESENT: YES (including this file)
A1_ENGINEERING_ARTIFACTS: PRESENT
A1_ROLE_VALIDATION: PASS (38/38)
OWNERSHIP_GUARD_UNIT_TESTS: PASS (16/16)
FORBIDDEN_SOURCE_METADATA_HITS: 0 CONFIRMED (bounded tracked-content scan)
SPRINT3_FINAL_PR: TO_BE_SUBMITTED
WEEK01_13_RESULT: PENDING_FINAL_PR_ACCEPTANCE
