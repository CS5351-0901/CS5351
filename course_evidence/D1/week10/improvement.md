# D1 — Week 10 Sprint 3 improvement

Recorded: 2026-11-20 (Asia/Shanghai). TARGET_WEEK: 11. Branch: course/d1.
Week 10 catch-up was performed today; no historical date is claimed.

## Baseline and engineering change

Fetched origin after an initial ls-remote connection failure. Remote main
exists at `60743b0`. Sprint 2 PR #15 merged at
`7506aee21e881a794cd3394f8b91a9db85415f91`; its ownership check passed.
Fast-forwarded through origin/course/d1 and origin/main without conflicts.
The previous A1 config-file contract test migration is now on main.

Fixed sandbox artifact collection's off-by-one limit. Previously it appended
a file before checking count > max_files: a limit of 1 returned 2 files and
0 returned 1. It now checks capacity before collecting the next entry.
The schema and defaults are unchanged. This bounds returned artifacts,
not filesystem writes or disk quotas.

Source: `skills/CodeAgent/scripts/codeagent_sandbox.py`.
Tests: `tests/roles/d1/test_week10_file_limits.py`.
Three real CLI subprocess cases use disposable workspaces/config paths with
spaces: limits 0, 1, and a limit larger than the four generated outputs.

## Executed red/green verification

Before repair, `python -B -m unittest discover -s tests/roles/d1 -p
test_week10_file_limits.py -v` ran 3 tests: 1 OK, 2 FAIL (2 != 1; one artifact
!= empty list), exit 1.

After repair, `python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v`
ran 28 tests, all OK, no skips/expected failures, exit 0.
`node --check skills/CodeAgent/scripts/codeagent_js_checker.js`: exit 0.
`git -c core.whitespace=cr-at-eol diff --check`: exit 0.
Environment: Windows / Python 3.11.5 / Node v22.22.3.

Windows resource enforcement, network isolation, filename containment,
installed ESLint/TypeScript diagnostics and live AstrBot end-to-end execution
remain unverified. Pre-existing untracked output/ and tmp/ are preserved and
excluded from commits. No D1 Week 12/13 files or early final PR are created.

WEEK10_ROLE_ENGINEERING: PASS
