# Team Week 9 — Sprint 2 closeout

Recorded: 2026-11-08 (Asia/Singapore). Sprint 2 covered Weeks 6–9. The team leader reviewed the submitted branches and integrated their changes through GitHub PRs, not by copying other members' files.

## Member PR decisions

| Role | Sprint 2 PR | Decision |
| --- | --- | --- |
| A1 | [#20](https://github.com/CS5351-0901/CS5351/pull/20) | Merged |
| A2 | [#19](https://github.com/CS5351-0901/CS5351/pull/19) | Merged after updating to latest main and rerunning tests |
| B1 | [#23](https://github.com/CS5351-0901/CS5351/pull/23) | Merged after updated-base role and V3 support checks |
| B2 | [#22](https://github.com/CS5351-0901/CS5351/pull/22) | Merged before this closeout; own V3 support changes retained |
| C1 | [#21](https://github.com/CS5351-0901/CS5351/pull/21) | Merged after updated-base tests |
| C2 | [#18](https://github.com/CS5351-0901/CS5351/pull/18) | Merged before this closeout |
| D1 | [#15](https://github.com/CS5351-0901/CS5351/pull/15) | Merged; despite the early PR title, the final PR included Week 6–9 evidence and the sandbox/checker engineering changes |
| D2 | [#24](https://github.com/CS5351-0901/CS5351/pull/24) | Merged after updated-base security checks |

All eight Sprint 2 PRs are merged. Their changed paths passed the required GitHub `Check ownership` workflow. The five PRs still open at the start of this review were checked separately: owned file scope, Week 6–9 evidence, actual non-document engineering or executable checks, tests, and `git merge-tree --write-tree` conflict preflight. No text-level merge conflicts were detected. GitHub's protected `main` branch required an up-to-date PR and passing status check; outdated branches were updated through their PR before merging, one at a time. No `ours/theirs` overrides or force merges were used.

There was one integration-level follow-up: [A1 PR #25](https://github.com/CS5351-0901/CS5351/pull/25). D1 correctly changed sandbox `--config` from inline JSON to a temporary UTF-8 JSON file, but an A1 Sprint 1 baseline test still expected the inline value. That A1-owned test initially failed after all role PRs were merged. PR #25 changed only `tests/roles/a1/test_baseline.py` to inspect the temporary file during the mocked subprocess and verify removal afterward. All 28 A1 tests then passed; PR #25 passed CI and was merged. D1 production code was not modified for this test correction.

## Actual validation on integrated main

The final independent test run used `main` at `64b232d1d1161bb9e72b65272f521265676d1717`, after all member PRs and the A1 integration-test fix. The test tree was extracted to an isolated directory. Environment: Windows, Miniconda Python 3.13.2, Node.js v26.2.0, `PYTHONUTF8=1`, with separate temporary directories for test output.

| Test area | Actual final result |
| --- | --- |
| A1 | 28 tests OK |
| A2 | 26 tests OK |
| B1 role | 14 tests OK |
| B2 role | 29 tests OK |
| C1 | 10 tests OK |
| C2 | 22 tests OK |
| D1 | 25 tests OK |
| D2 security | 12 direct `test_*` function checks passed |
| B1 V3 support | 62 tests OK, 2 skipped |
| B2 V3 support | 51 tests OK |
| Ownership guard unit suite | 16 tests OK |
| JavaScript checker syntax | `node --check` exited 0 |
| Python syntax | 4 files parsed successfully with `ast.parse`: `main.py`, packager, sandbox, security scanner |

The role and support suites contain 279 test/check entries in total; 2 B1 cases were skipped, and the others passed. The separate ownership-guard suite adds 16 passing tests. D2 tests were invoked directly because `pytest` was unavailable in this Miniconda environment; this is not a claim of pytest execution. No live AstrBot end-to-end run was performed.

Initial independent runs exposed environment-sensitive failures: B1's report fixture encountered the Windows GBK default and a false path rejection when the review checkout itself sat under the temporary directory; D1's live Windows subprocess tests also needed UTF-8 mode. Rechecking in UTF-8 mode with a distinct temporary working area resolved these errors without editing B1 or D1 code. The later A1/D1 integration mismatch was a genuine stale test contract and was resolved through PR #25 as described above.

Final failed or blocked Sprint 2 member PRs: none. The two B1 skipped cases remain skips, not passes.

## Remaining technical debt for Sprint 3

- Validate the integrated CodeAgent plugin inside an actual AstrBot instance, including startup, concurrent sessions, sandbox, security scanner, JavaScript checker and packaging. Existing role tests mostly use mocks/stubs and do not establish this end-to-end behavior.
- A1 Node/npm installation and Linux/macOS fallback paths remain mock-tested only. Startup latency and partially installed dependencies are not established in a real deployment.
- Keep the sandbox `--config` file-path contract and cleanup covered as shared integration behavior; A1's former inline-JSON assumption is now corrected.
- Verify B1 support checks on a normal UTF-8 test environment and investigate the two platform-specific skips only if a supported target requires them. Document the Windows UTF-8 test assumption so the earlier locale failures are not misreported as functionality regressions.
- If the team uses pytest for D2's free-function tests later, run that collector in an approved environment; no new dependency was installed merely for this leader review.

TEAM_WEEK09_SPRINT2_MEMBER_PRS: 8/8 MERGED

A1_INTEGRATION_FOLLOWUP_PR25: MERGED

FINAL_INTEGRATED_ROLE_SUPPORT_CHECKS: 279 ENTRIES, 2 SKIPPED, 0 FAILURES

OWNERSHIP_GUARD_TESTS: 16/16 PASS

LIVE_ASTRBOT_END_TO_END: NOT_RUN

WEEK10_AND_LATER_WORK: NOT_STARTED
