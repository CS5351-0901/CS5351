# Week 9 — C2 Sprint 2 closeout

Date: 2026-11-02
BRANCH: course/c2
REVIEWED_MAIN: 72fc675e22cc2440e6e4970b8e399a8d8a794e4f
REVIEWED_C2_HEAD: 196ee4f81e95e8315eb3ab32971b6c136d202d3d
TESTED_INTEGRATION_TREE: d02a451dacdeeac55d4dc5c73bc5624e8a54e84f

## Delivered work, Weeks 6–9

| Week | Actual artifact | Observed result |
| --- | --- | --- |
| 6 | Packager counts actual ZIP entries; four new regressions and count assertions in three existing successful-archive tests. Commit 3c2e8aaf5d7cb282b65b73ef96d7e3892d9f03ee. | The expanded 16-case suite exposed seven count mismatches before the fix; all 16 passed after it. Generated configurations, extra files and simulated Node install artifacts are counted; cleaned files and overwritten duplicates are not overcounted. |
| 7 | Packager creates parent directories for nested test files; six layout and failure-path tests. Commit 28a725564ce3c1d83fd47502ac07b3d394bf20b6. | Four new successful-layout cases failed with missing-directory errors before the fix. All 22 scoped cases passed after it, including file/directory conflict cleanup. |
| 8 | Integration review of updated main, isolated combined checkout, interface review and current-policy replay. Commit 196ee4f81e95e8315eb3ab32971b6c136d202d3d. | 22 C2 tests and 16 policy tests passed. No new C2 interface change or source fix was required. |
| 9 | This closeout; full role verification rerun; Sprint 2 publication/PR preparation. | Results below are from this Week 9 execution; final PR/merge identifiers are recorded in the execution report after publication. |

Sprint 2 includes production changes in the owned packager and ten new test cases. It is not a documentation-only sprint. The cumulative PR is limited to C2 Week 6–9 evidence, tests/roles/c2 and the owned packager script; main.py and other roles are unchanged.

## Validation actually rerun at closeout

Fetched origin --prune and verified main and the C2 remote head. Main is unchanged from the Week 8 review. `git merge-tree --write-tree HEAD origin/main` returned cleanly. A temporary detached checkout at REVIEWED_C2_HEAD was combined with reviewed main using `git merge --no-commit --no-ff origin/main`; its tree matched TESTED_INTEGRATION_TREE. No integration merge commit was created by this preflight.

Python 3.12.14 on Windows, from the combined checkout:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
python -B tools/test_pr_ownership.py
```

- **22/22 C2 tests passed**, exit 0, no skips or expected failures.
- **16/16 current-main ownership-policy tests passed**, exit 0. These are policy tests, not additional C2 runtime cases.
- Text merge preflight and the temporary combined checkout were conflict-free.
- The latest trusted-main ownership validator is also run on the final submitted head. Required GitHub Check ownership must pass before merge; a local replay is not a replacement for CI.

The bundled interpreter was used with writable TEMP/TMP scratch storage. The suite covers real ZIP creation, CRC/member/content/count/size checks, generated configurations, absent/empty tests, nested test layouts, write/conflict failure cleanup, dependency-manifest fixtures, and wrapper argument/error behavior.

RUNTIME_TEST: PASS (22/22 scoped C2 cases)

## Remaining risks and verification limits

- Wrapper subprocesses and selected dependency classification are mocked. Node installation is simulated; no real npm installation was run.
- Staging paths are redirected to test-owned temporary directories. Production temporary-path portability, same-second concurrency and cleanup of partial archive failures are not fully established.
- Absolute paths, parent-directory traversal and symlinks are not confined by this sprint's changes. Valid nested-path tests are not a path-security claim.
- Node dependency parsing still strips quoted strings before import matching; Python dependency detection still depends on installed modules and import/distribution naming.
- Default entry-point commands can disagree with the src layout; nested extra_files and dependency/config escaping remain open review items.
- Wrapper exit-code/schema checks and the 120-second wrapper versus 300-second npm timeout mismatch remain unresolved.
- Full AstrBot execution, real CLI subprocess integration, extracted-project install/startup and executing the generated/archived tests remain NOT_RUN. The combined checkout includes main and C2 only, not all unmerged member branches.

These limitations do not invalidate the scoped regression results, but they prevent any claim of complete end-to-end delivery readiness.

## Next Sprint objectives

1. Add executable, ownership-scoped validation for dependency extraction and generated metadata, and fix demonstrated failures.
2. Prioritize safe output-path handling and temporary/archive lifecycle tests before expanding packaging inputs.
3. Extend wrapper return/error contracts and extracted-project usability checks; coordinate shared-main ownership where needed.
4. Re-run the full C2 suite after each change and report mocks, skipped or unavailable integrations explicitly.

These are planned objectives only. No Week 10 or later files or implementation are created here.

## Sprint 2 submission

Commit message: `docs(c2): week 09 close sprint 2`.

Open course/c2 into main as the Sprint 2 PR, verify the exact PR head and allowed changed paths, wait for required Check ownership and any enforced review conditions, and stop if conflicts occur. Merge only through the PR without bypassing protection. After merge, fetch and fast-forward course/c2 to origin/main. The execution report records the actual final state; this document does not pre-claim a PR merge that had not happened at commit time.
