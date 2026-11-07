# D1 — Week 9 Sprint 2 closeout

Recorded: 2026-11-02. TARGET_WEEK: 9. BRANCH: course/d1.
Sprint 2 covers Weeks 6–9. No Week 10+ work is created.

## Delivered engineering work

| Stage | Actual artifact |
| --- | --- |
| Week 6 | `e74446e`: raw source adapter arguments, readable temporary sandbox configuration and cleanup, checker fail-closed behavior; see `week06/contract_repair.md` and `week06/change.md` |
| Week 7 | `e74446e` / `7de2841`: Windows-compatible sandbox startup/execution, current Python interpreter, resolved workspace/temp paths, unique checker temp directories, tool discovery and Function rule boundary, real adapter-to-sandbox Unicode integration test; see `week07/platform_integration.md` and `week07/verification.md` |
| Week 8 | Merged main `1ebb67da2f282de849a93073b1921a59b83c4743` without conflicts; `f764c59` records integration checks and handbook-named Week 6/7 evidence indexes |
| Week 9 | Reran complete D1 verification, recorded sprint results, remaining dependency and next sprint goals; updates existing Sprint 2 PR #15 rather than creating a duplicate |

Production scope: `main.py::_call_sandbox`, `main.py::_call_js_checker`,
`skills/CodeAgent/scripts/codeagent_sandbox.py`, and
`skills/CodeAgent/scripts/codeagent_js_checker.js`.
Executable verification: `tests/roles/d1/test_baseline.py`.
Sprint 2 contains non-document engineering work.

## Executed acceptance evidence

Week 9 final rerun on Windows / Python 3.11.5 / Node v22.22.3:

```text
python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v
Ran 25 tests; OK; exit 0; no skips or expected failures

node --check skills/CodeAgent/scripts/codeagent_js_checker.js
exit 0
```

Week 8 integration reruns: B1 7/7 OK, C2 22/22 OK, ownership guard regression
suite 16/16 OK. A1 7/8 OK, one ERROR. Full commands and diagnosis are in
`week08/integration_review.md`. The PR diff ownership validator also passed
against origin/main after the Week 8 commit (9 changed paths).
These are separate role suites, not full AstrBot end-to-end acceptance.

## Remaining risks and integration gate

- A1's main-branch baseline still expects inline sandbox JSON. Its
  `test_sandbox_receives_configured_limits_and_timeout` raises JSONDecodeError
  with D1's repaired config-file contract. A1 owns migration of that test.
  Cross-role acceptance remains incomplete; D1's 25 passing tests do not imply
  a green whole-team suite.
- Windows CPU/memory/process limits are not enforced; network isolation and
  whitelist enforcement remain unverified. This is not an OS security boundary.
- Live AstrBot startup, event dispatch and complete `/agent` flow: NOT_RUN.
- Real installed ESLint/TypeScript correctness: NOT_RUN; node_modules is absent.
  Missing-tool reporting and checker structural contracts are tested.

Sprint 2 PR: https://github.com/CS5351-0901/CS5351/pull/15
Base: main; head: course/d1. Integration is pending review of the disclosed
A1 contract migration dependency. Required `Check ownership` must pass for the
final head. No check bypass, direct main push, or self-approval is claimed.
After a reviewed merge, synchronize course/d1 with `git fetch origin --prune`
and `git merge --ff-only origin/main`; report divergence/conflicts if any.

## Next Sprint goals (planning only)

1. Coordinate A1's config-file assertion migration before claiming team-wide
   regression acceptance.
2. Exercise installed ESLint/TypeScript diagnostics in a reproducible setup.
3. Investigate sandbox path containment, file collection limits and effective
   timeout/resource controls with focused reproductions before owned fixes.
4. Arrange a real AstrBot lifecycle and `/agent` integration check.

ROLE_VERIFICATION: PASS (25 executed tests)

WEEK08_REVIEW: COMPLETED

WEEK09_ROLE_DELIVERY: COMPLETED

SPRINT2_MERGE: PENDING_REVIEW_AND_CROSS_ROLE_CONTRACT_MIGRATION

WHOLE_TEAM_ACCEPTANCE: NOT_CLAIMED
