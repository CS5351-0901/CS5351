# Team Week 11 — Sprint 3 regression status

Recorded: 2026-11-20 (Asia/Singapore). This is the team leader's factual Week 11 review, not an assertion that every member's Week 11 work has been completed.

## Actual remote role progress

Snapshot taken after `git fetch origin --prune`. The protected `main` still contains the completed Sprint 2 team report through Week 9. Week 10–11 contributions remain on member branches, with no open Sprint 3 / Final PR.

| Role | Highest evidence week on personal branch | Actual Sprint 3 contribution / remaining issue |
| --- | --- | --- |
| A1 | 11 | Week 10 JS dependency setup fix and five tests; Week 11 five recovery-path tests and source scan; both pushed |
| A2 | 9 | Week 10 engineering and Week 11 regression not yet submitted |
| B1 | 10 | Snapshot comparison / duplicate finder support tools and role tests; Week 11 evidence pending |
| B2 | 10 | Artifact manifest / corpus diff support tools and role tests; Week 11 evidence pending |
| C1 | 9 | Week 10 engineering and Week 11 regression not yet submitted |
| C2 | 9 | Week 10 engineering and Week 11 regression not yet submitted |
| D1 | 9 | Week 10 engineering and Week 11 regression not yet submitted |
| D2 | 11 | Python syntax / security scanner change and Week 11 checker cleanup evidence; pytest-dependent checks require separate verification |

Week 11 evidence is present for 2/8 roles (A1 and D2). Week 10 is present for 4/8 roles (A1, B1, B2 and D2). These counts are based on committed role evidence directories, not estimates or offline messages.

## Executed role regressions

The following tests were run on the fully integrated Sprint 2 code plus the A1 Week 10–11 changes (`course/a1` at `e3ecb442e7b8a063d719a7beb6a6dc55f932be04`). Windows / Miniconda Python 3.13.2 with `PYTHONUTF8=1`:

| Area | Actual result |
| --- | --- |
| A1 | 38/38 PASS |
| A2 | 26/26 PASS |
| B1 integrated role baseline | 14/14 PASS |
| B2 integrated role baseline | 29/29 PASS |
| C1 | 10/10 PASS |
| C2 | 22/22 PASS |
| D1 | 25/25 PASS |
| B1 V3 integrated support | 62 total, 2 SKIPPED, 0 failures |
| B2 V3 integrated support | 51/51 PASS |
| D2 integrated security tests | 12 direct tests PASS (not a pytest run) |
| JS checker | `node --check` exit 0 |
| Python syntax | Four integrated Python files parsed with `ast.parse` |

The following additional independent checks were executed in isolated scratch copies of the member's **actual latest Sprint 3 branch**, not merely against `main`:

| Branch | Result |
| --- | --- |
| B1 Week 10 `44adf8c` | 17 role tests PASS; support: 72 total, 2 SKIPPED, 0 failures |
| B2 Week 10 `a3c8881` | 34 role tests PASS; 61 support checks PASS |
| D2 Week 11 `a2fdfe0` | 15 directly callable security / Python syntax tests PASS; the three tests in `test_checker_cleanup.py` were NOT_RUN because the runner has no pytest dependency (including pytest fixtures) |

No extra dependencies were installed. The failed/skip/not-run distinction is intentional: a direct invocation of D2's free functions is not equivalent to running the full pytest collection. Existing role checks use substantial mocking, so these outcomes do not prove live AstrBot or real npm installation.

## Failure paths, ownership and course-source traceability

- A1 Week 10 changed only its `_ensure_js_dependencies` function and A1 tests; an incomplete `node_modules` now leads to a retry. Week 11 tests exercised retry after a failed npm process, failed Node probe, scoped package directories, empty manifests and malformed nonmapping manifests. No real Node/npm installation was performed.
- D1 sandbox temporary-JSON contract was preserved; the old A1 test was already corrected and merged in Sprint 2 PR #25.
- The active `main` static ownership checker was executed against A1, B1, B2 and D2's latest personal heads. **All four checks passed**; this does not substitute for the Week 13 PR status checks.
- Read-only source-leakage scan across `origin/main` and all eight `origin/course/<role>` refs checked exact original-source directory identifiers, absolute local source paths and source provenance/commit metadata fields. All nine scanned refs had zero matches for those indicators. A separate A1 text scan found 20 GitHub URL occurrences belonging to the team's own course repository; these are legitimate Git evidence, not external-source metadata. The old A1 Week 9 `origin/main` commit ID is course history, not an external upstream source hash. No genuine course evidence was deleted.
- Real cross-role live integration, Linux/macOS installers, npm network installation and D2's pytest fixture-based checks are unresolved validation limits. Do not report them as passing.

## Action and boundary

Members still at Week 9 (A2, C1, C2, D1) must submit their own Week 10 engineering before Sprint 3 closeout. B1 and B2 still need Week 11 regression/cleanup evidence. D2's fixture-based pytest tests require an approved environment or should remain NOT_RUN in the leader audit. The team must defer Week 12 presentation evidence and Week 13 final role PR integration until those actual stages and prerequisites, without manufacturing submissions or merging early.

TEAM_WEEK11_LEADER_REVIEW: COMPLETE
WHOLE_TEAM_WEEK11: INCOMPLETE
WEEK11_ROLE_EVIDENCE: 2/8
WEEK10_ROLE_EVIDENCE: 4/8
SPRINT3_FINAL_ROLE_PRS: NOT_OPENED
D2_PYTEST_CLEANUP_CHECKS: NOT_RUN
WEEK12_WEEK13_LEADER_ARTIFACTS: NOT_CREATED
