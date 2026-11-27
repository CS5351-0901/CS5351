# Team Week 13 — Final integration and delivery status

Recorded: 2026-11-27. Course repository: https://github.com/CS5351-0901/CS5351

## Final member integration

All eight roles have complete Week 01–13 evidence on main. The following are the three actual course PRs per member, all confirmed MERGED on GitHub and reachable from the reviewed main. Each PR contains at least one owned non-document engineering/test artifact; the counts were checked from the actual merge commit changes, not from weekly summaries alone.

| Role | Sprint 1 PR / non-doc paths | Sprint 2 PR / non-doc paths | Sprint 3 PR / non-doc paths |
| --- | --- | --- | --- |
| A1 | #1 / 1 | #20 / 2 | #30 / 4 |
| A2 | #7 / 2 | #19 / 2 | #29 / 1 |
| B1 | #3 / 2 | #23 / 17 | #28 / 9 |
| B2 | #5 / 1 | #22 / 23 | #33 / 19 |
| C1 | #2 / 2 | #21 / 2 | #31 / 2 |
| C2 | #6 / 2 | #18 / 3 | #34 / 5 |
| D1 | #4 / 1 | #15 / 4 | #32 / 3 |
| D2 | #8 / 2 | #24 / 3 | #35 / 3 |

A1's additional integration-test correction #25 remains merged. Team Weeks 10–11 #27 and Week 12 #36 are merged. Week 12 collects all eight contributions and presentation/report material at [presentation_and_report_prep.md](../week12/presentation_and_report_prep.md).

A1 #30, C1 #31, B2 #33 and C2 #34 were already merged before this closeout. Their exact GitHub states, required-check outcomes, merge ancestry and engineering artifacts were reviewed, and their final integrated suites were independently rerun.

For the remaining four, the leader verified the original member head, all Week 01–13 evidence, non-document engineering, active ownership validator, CRLF-aware diff check and conflict-free merge-tree preflight. Each outdated PR was updated through GitHub to the then-current main, with its original commits preserved, then tested in an isolated archive of the exact updated head. Required Check ownership succeeded for that head, mergeability was CLEAN, and the protected merge used the reviewed head. No conflict override, force push or bypass was used.

| Role / PR | Updated head | Independent pre-merge result | Final decision |
| --- | --- | --- | --- |
| A2 #29 | b476816 | 29/29 role tests | Merged |
| B1 #28 | 14fb5a8 | 19/19 role; 77 support checks, 2 skipped, zero failures | Merged |
| D1 #32 | 93f98de | 34/34 role; node --check exit 0 | Merged |
| D2 #35 | 4fb43a6 | 18/18 pytest tests | Merged |

D2 had already pushed Week 13 evidence and engineering work but had not opened its final PR. On the user's explicit instruction, the team leader opened #35 from course/d2 using the leader account, transparently identifying the submission as on behalf of D2. The active policy permits this course branch and validates D2 ownership against the actual actor. Original D2 commits/authorship and files were retained; no ownership rule was changed or bypassed. No other role implementation was edited by the leader during this closeout.

SPRINT1_PRS: 8/8 MERGED
SPRINT2_PRS: 8/8 MERGED
SPRINT3_PRS: 8/8 MERGED
ENGINEERING_ARTIFACT_CHECK: 24/24 member Sprint PRs contain non-document engineering
FAILED_OR_BLOCKED_MEMBER_PRS: NONE

Sprint 1 PRs predate introduction of Check ownership (19e8dea, 2026-10-12 21:11 +08); their empty GitHub statusCheckRollup is NOT a failed check. The last Sprint 1 merge preceded this introduction. The historical Week 5 closeout records the actual baseline verification, including six expected D1 failures and D2 direct checks. Sprint 2 and Sprint 3 role PRs have successful Check ownership results. The final checks below do not retroactively invent CI for Sprint 1.

## Independently executed final integrated validation

Reviewed and tested main at e6bbd703, after all eight final member PRs and team Week 12 integration. Environment: Windows, Miniconda Python 3.13.2, Node v26.2.0, PYTHONUTF8=1, with separate scratch checkout and temporary output directories. pytest 9.2.0 and its dependencies were installed only into this review's temporary directory for D2; no installed project dependency or environment was changed persistently.

| Suite | Actual final result |
| --- | --- |
| A1 | 38/38 passed |
| A2 | 29/29 passed |
| B1 role | 19/19 passed |
| B2 role | 34/34 passed |
| C1 | 11/11 passed |
| C2 | 33/33 passed |
| D1 | 34/34 passed |
| D2 | 18/18 passed under actual pytest |
| B1 V3 support | 77 entries: 75 passed, 2 skipped |
| B2 V3 support | 81/81 passed |
| Ownership guard self-tests | 16/16 passed |
| Python syntax | py_compile on main.py, packager, sandbox and security scanner: exit 0 |
| JavaScript syntax | node --check on codeagent_js_checker.js: exit 0 |

Role suites (A1 through D1 except D2) used python -B -m unittest discover -s tests/roles/<role> -p test_*.py -q. B1/B2 support checks were explicitly discovered under course_tools/<role>_support/checks with check_*.py. D2 used python -B -m pytest -p no:cacheprovider tests/roles/d2 -q with temporary pytest on PYTHONPATH and third-party plugin autoload disabled. All thirteen validation commands exited 0.

Total role and support entries: 374; 372 passed, 2 skipped, zero failures. Guard tests add 16 passing tests, not part of the role/support count. Python and Node syntax checks are separate from test counts. The two B1 skips remain skips, not passes. After the tests, the B2 read-only residue fixture left a deliberately read-only file under the review's scratch directory; the first scratch removal failed on Windows. The fixture was identified in the test source, the temporary file permissions were restored, and the entire dedicated review directory (including temporary pytest) was removed successfully. No repository or unrelated user file was removed. This cleanup error was not a test assertion failure.

PYTHON_VALIDATION: PASS
NODE_VALIDATION: PASS
ROLE_TESTS: 372 PASS / 2 SKIPPED / 0 FAILED (374 entries)
GUARD_TESTS: 16/16 PASS
LIVE_ASTRBOT_END_TO_END: NOT_RUN

## Delivery and source metadata checks

All eight independent course branches exist. Each role's week01 through week13 directories contains tracked evidence in integrated main. Team week01 through week12 are present; this file supplies week13. No week14 or later evidence paths exist. README.md remains the CS5351 CodeAgent Course Project introduction, not an upstream README.

The final pre-report tracked-tree scan examined all 231 UTF-8 tracked files and reachable main commit messages for source-input directory identifiers, absolute source-workspace paths, external source repository URL patterns and source-provenance field assignments: zero candidates. Of 68 existing full-length Git reference occurrences, 65 match reachable course history. The historical A1 Week 4 baseline is separately confirmed as a course commit by the course GitHub API. Two C2 references are explicitly labeled historical temporary integration-tree IDs; their objects could not be independently resolved here, and no external source attribution was found. The original course evidence is preserved. No confirmed forbidden source metadata was identified; the pattern-based current-tree and commit-message review is not a forensic audit of every historical object.

FORBIDDEN_SOURCE_METADATA_HITS: 0 CONFIRMED (bounded audit)
FUTURE_WEEK_FILES: NONE
README_COURSE_INTRODUCTION: PASS
TEAM_WEEK01_13: PRESENT INCLUDING THIS FILE
A1_WEEK01_13: YES
A2_WEEK01_13: YES
B1_WEEK01_13: YES
B2_WEEK01_13: YES
C1_WEEK01_13: YES
C2_WEEK01_13: YES
D1_WEEK01_13: YES
D2_WEEK01_13: YES

## Remaining limitations and final acceptance boundary

The role and support suites establish scoped helper, contract, filesystem and controlled subprocess behaviors. They do not establish full live AstrBot startup, event delivery and end-to-end agent operation; actual Node/npm network installation and real Linux/macOS installer behavior remain unverified. C1 rollback lacks a call site in the main debug flow; D1's sandbox is not established as OS-level isolation; D2's optional external checker integration remains unverified; C2's hostile path/symlink and multiprocess boundaries remain open. B2 cleanup can leave read-only residue, as explicitly tested. These are retained engineering limitations, not hidden or relabeled passes.

All member integration and scoped engineering validation gates are satisfied. At preparation, the leader checkout is clean and no member PR is open. Final publication of this report via its own protected team PR, verification of all thirteen team weeks on main, and a clean synchronized leader checkout are the remaining publication gates. The final execution response records MAIN_HEAD, WORKTREE_CLEAN and FINAL_WEEK13_RESULT after these checks; no merge result is predeclared in the file.
