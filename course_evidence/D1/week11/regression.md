# D1 — Week 11 regression and cleanup

Recorded: 2026-11-20 (Asia/Shanghai). TARGET_WEEK: 11. Branch: course/d1.
Base main: `60743b0`. Week 10 engineering commit: `429c4da`.

## Engineering and regression coverage

Week 10 repaired the artifact-count off-by-one defect after two failing real
CLI reproductions. Week 11 adds `tests/roles/d1/test_week11_regression.py` with
six real subprocess cases: syntax failure, runtime exception, wall timeout,
hidden/source-file filtering, oversized artifact filtering, and Unicode
filename metadata with UTF-8 byte counts. The 30-second sleep fixture returns
failure under a 1-second configured wall timeout; the parent test invocation
also has a 15-second watchdog. Tests use trusted fixture code and disposable
workspaces. They do not execute arbitrary user input.

No additional production fix was needed for these paths. The Week 10 count
check is the concrete technical-debt cleanup. Shared main.py and other roles'
files are unchanged by this Sprint 3 increment.

## Actual executed checks

Environment: Windows / Python 3.11.5 / Node v22.22.3.

| Command | Actual result |
| --- | --- |
| `python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v` | 34 tests, OK, exit 0; no skips/expected failures |
| `node --check skills/CodeAgent/scripts/codeagent_js_checker.js` | exit 0 |
| `python -B tools/test_pr_ownership.py` | 16 tests, OK, exit 0 |
| `python -B -m unittest discover -s tests/roles/a1 -p 'test_*.py' -v` | 28 tests, 26 OK, 2 ERROR, suite exit 1 |
| `git -c core.whitespace=cr-at-eol diff --check` | exit 0 |

A1's sandbox configuration test now passes; the previous Sprint 2 migration
dependency is resolved on main. The two current A1 errors are
`test_official_node_corrupt_archive_stops_before_copying` and
`test_official_node_download_failure_returns_false_without_extracting`.
In this fresh Python 3.11 process, platform.system() invokes Windows version
discovery through a mocked subprocess and receives a MagicMock; platform's
regex raises TypeError. These installer-test errors are outside D1 ownership
and were not hidden or edited. Whole-team regression is not claimed PASS.

## Git content audit

Used `git grep -n -I -E` on tracked content to inspect URL candidates, absolute
path candidates, source-origin markers, and the known local source-input
directory name; then repeated the source-marker/path and GitHub URL searches
over the entire tracked tree (including course_tools).

Observed: no external source repository links or source-origin fields found.
GitHub repository URLs point to this course repo/PRs. Other URL candidates are
the production Node download endpoint and a sample GitHub API request.
Absolute-path candidates are interpreter paths in historical team/A1 evidence,
the sandbox's runtime PATH setting, and a synthetic POSIX path fixture in B2
support code; these are not local source-input directory disclosures.
Regex false positives in strings were reviewed. No historical evidence or
other members' content was deleted to obtain this result. This is a tracked
working-tree content audit, not a scan of all historical commits or secrets.

## Delivery boundary and limits

Week 10 and Week 11 have separate role commits and are pushed to course/d1.
No Week 12/13 D1 evidence or Sprint 3 final PR is created before its checkpoint.
Pre-existing untracked output/ and tmp/ remain untouched and uncommitted;
the overall working tree is therefore not described as clean.

Linux/macOS runtime, real AstrBot event dispatch, installed ESLint/TypeScript
correctness, Windows resource enforcement, filename containment and effective
network isolation remain unverified. The artifact-count fix does not bound
disk writes, total output memory, or make this an OS security boundary.

D1_WEEK11_REGRESSION: PASS (34 executed tests)

WHOLE_TEAM_REGRESSION: NOT_CLAIMED

FUTURE_D1_WEEK_FILES_CREATED: NONE
