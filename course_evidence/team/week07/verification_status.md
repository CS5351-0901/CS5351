# Week 7 — Sprint 2 verification status

Recorded: 2026-10-25 (Asia/Singapore). Scope: Week 7 team-leader review of remote member branches and executable verification. This records observed results, not an invented team meeting or authorization to write other members' code.

## Actual remote checkpoint

Current Sprint 2 is Weeks 6–9. Member Sprint 2 PR reviews/merges are scheduled for Week 9; no Week 6–7 member integration is claimed here. Team leader inspected current `origin/course/<role>` heads and each member's Week 6/7 evidence, changes to tests/scripts, and recent commits.

| Role | Highest committed week on member branch | Evidence of added engineering verification | Week 7 status |
| --- | --- | --- | --- |
| A1 | Week 7 | Week 6 added 12 executable preparation tests. Week 7 commit `f12de5de26df17d1b0e95c3f8b1f27c00da633b5` added 8 boundary/contract/failure-path tests in `tests/roles/a1/test_week07_contracts.py`. Week 5–7 suite ran 28/28 PASS. | A1 Week 7: PASS |
| A2 | Week 5 | Week 5 existing orchestration baseline only; no Week 6/7 evidence on the branch. | Behind Week 7; Week 6 and Week 7 real engineering/verification due |
| B1 | Week 7 | Week 6 regression and independent inventory tool; Week 7 expanded role tests and added standalone V3 text/source metrics with explicit support checks. | Week 7 engineering/tests present; independently rerun below |
| B2 | Week 5 | Week 5 role baseline only; no Week 6/7 evidence or V3 support extension on the branch. | Behind Week 7; original Week 6/7 role work and optional V3 support addenda due |
| C1 | Week 6 | Week 6 modified the owned snapshot helper and added two executable regressions; no Week 7 evidence. | Week 6 submitted; Week 7 contract/boundary verification due |
| C2 | Week 5 | Week 5 packaging baseline only; no Week 6/7 evidence. | Behind Week 7; Week 6/7 real engineering/verification due |
| D1 | Week 5 | Week 5 existing sandbox/checker baseline (six known expected failures); no Week 6/7 evidence. | Behind Week 7; Week 6/7 real engineering/verification due |
| D2 | Week 6 | Week 6 security scanner and role tests added shell dangerous-pattern regression; no Week 7 evidence. | Week 6 submitted; Week 7 contract/boundary verification due |

These are **branch evidence states**, not claims that every role is fully accepted for Sprint 2. No Week 8/9 artifacts were created during this review.

## Independently executed checks

Team leader used isolated temporary Git worktrees at the exact remotely fetched branch heads and Windows Miniconda Python 3.13.2. Source branches and members' commit history were left unchanged. Temporary review worktrees were removed after the tests.

| Test source | Command or method | Observed result |
| --- | --- | --- |
| A1 on `course/a1` | `python -B -m unittest discover -s tests/roles/a1 -p test_*.py -v` | 28 tests, OK, exit 0; includes 8 new Week 7 tests |
| B1 on `origin/course/b1` | `python -B -m unittest discover -s tests/roles/b1 -p test_*.py -v` | 14 tests, OK, exit 0 |
| B1 V3 support on `origin/course/b1` | `python -B -m unittest discover -s course_tools/b1_support/checks -p check_*.py -v` | 44 tests, OK (2 skipped), exit 0 |
| C1 on `origin/course/c1` | `python -B -m unittest discover -s tests/roles/c1 -p test_*.py -v` | 8 tests, OK, exit 0 |
| D2 on `origin/course/d2` | Python standard-library import then direct invocation of the 7 `test_*` functions in `tests/roles/d2/test_security_baseline.py` | 7 checks passed, exit 0; **pytest NOT_RUN** in this leader environment (`No module named pytest`) |

The B1 auxiliary suite has **two skipped cases** in this actual Windows run and must not be rewritten as `44 passed, no skips`. D2 direct invocation is not a pytest collection claim.

## Review decisions and requests for remaining work

- Evidence of increasing Week 7 contract/boundary/regression coverage is confirmed for A1 and B1. For C1 and D2, Week 6 produced real non-document changes and runnable verification, but Week 7 is not yet delivered. For A2/B2/C2/D1, Week 6–7 is not delivered, so the Week 7 verification growth check remains **PENDING**.
- No branch was observed to have **Week 7 evidence consisting only of Markdown** without an engineering increment. Thus there is no verified docs-only Week 7 submission to reject. Missing weekly work cannot be counted as PASS; members should provide real owned tests/checks or a demonstrated source fix, not just `verification.md`.
- B1's support files under `course_tools/b1_support/**` are allowed by the V3 manual and the updated `Check ownership` rules on `main` (governance PR #13). This does not waive Week 9 review of real support behavior or zero-coupling guarantees.
- D1's known six expected failures are tracked technical debt, not already repaired; they do not justify inventing a new mandatory Week 7 fix.
- All eight roles should keep Week 6–8 work scoped to their own branch/files, keep test results reproducible, and submit individual Sprint 2 PRs at Week 9. Leader will review them individually then; no early merge or modifications to other members' work were performed.

## Week 7 team-leader verdict

TEAM_WEEK07_BRANCH_REVIEW: COMPLETED

A1_WEEK07: PASS (new executable tests and evidence committed and pushed)

B1_WEEK07: EVIDENCE_AND_TESTS_PRESENT (independent checks completed)

C1_AND_D2_WEEK07: PENDING

A2_B2_C2_D1_WEEK06_07: PENDING

WHOLE_TEAM_WEEK07: INCOMPLETE (not claimed PASS)

SPRINT2_PR_INTEGRATION: NOT_DUE_UNTIL_WEEK09
