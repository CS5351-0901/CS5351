# Week 8 — C2 integration review

Date: 2026-11-02
BRANCH: course/c2
PREVIOUS_REVIEWED_MAIN: 6b0472c36ffd09c6bfe6e647380cd0d0799ea076
REVIEWED_MAIN: 72fc675e22cc2440e6e4970b8e399a8d8a794e4f
REVIEWED_C2_HEAD: 28a725564ce3c1d83fd47502ac07b3d394bf20b6
INTEGRATION_TREE: 81882d1d9f18a93e89ca86d3c1cd8b4ffeb59d88

## Upstream and scope review

Fetched origin with --prune and pulled course/c2 with --ff-only. The member branch was already current. Since the Week 7 reviewed main, upstream added four commits through PRs #16 and #17, changing only:

- course_evidence/team/week08/integration_review.md
- docs/PR_OWNERSHIP.md
- tools/check_pr_ownership.py
- tools/test_pr_ownership.py

The governance change permits short sibling-module imports only when a matching module exists in the respective B role's support root. It does not expand C2 ownership. Neither main.py nor the packager script changed in this upstream interval (Git diff exit 0 for those paths). C2 has not edited shared main.py or governance files.

## Interface impact

| Boundary | Reviewed behavior and integration impact |
| --- | --- |
| Main orchestration to _call_packager | files, test_files, name, description and project_type still map to the existing wrapper parameters. No upstream caller or wrapper change. |
| Wrapper to CLI | JSON --files and optional --test-files remain unchanged, along with --name, --description and --type. Existing argument, missing-script, malformed-output and timeout regressions pass. These use a mocked subprocess. |
| Packager result to delivery | success, zip_path, file_count, size and error retain their field names/types. Main displays file_count; the Week 6 change now reports actual archived files instead of an estimate. Existing ZIP-content/count regressions pass in the combined checkout. |
| Test layout | Week 7 creates test parent directories before writing. Nested paths, Unicode/empty content, shared parents and file/directory conflict cleanup still pass. Flat test-file input used by the main caller remains covered. |
| Ownership enforcement | Replayed the latest reviewed main validator from the combined checkout. C2's five existing Sprint 2 changed paths pass. The B-support exception does not apply to C2. |

No new integration defect requiring a C2 source fix was found in this reviewed upstream interval. This week adds this evidence only. Sprint 2 already has non-document engineering artifacts in Week 6 (correct archive file counts and four new regressions) and Week 7 (nested test-directory fix and six new cases).

## Actual isolated integration verification

First ran `git merge-tree --write-tree HEAD origin/main`: exit 0, producing the integration tree above with no conflicts. Then created a temporary detached worktree at REVIEWED_C2_HEAD and ran `git merge --no-commit --no-ff origin/main`. This combined the two revisions for testing without creating a merge commit or moving either source branch. Its `git write-tree` matched the preflight tree.

Using Python 3.12.14 on Windows, the following ran in that combined checkout:

```text
python -B -m unittest discover -s tests/roles/c2 -p 'test_*.py' -v
python -B tools/test_pr_ownership.py
python -B tools/check_pr_ownership.py --base origin/main --head HEAD --branch course/c2 --author yousj828 --head-repo CS5351-0901/CS5351 --expected-head-sha 28a725564ce3c1d83fd47502ac07b3d394bf20b6
```

Results:

- C2 regression suite: **22/22 passed**, no skips or expected failures, exit 0.
- Latest ownership-policy unit tests: **16/16 passed**, exit 0. These are governance tests, not additional C2 runtime tests.
- Latest main ownership validator: **PASS, role=c2, changed=5** for the pre-Week-8 head. The final document commit is checked separately before publication.
- Text merge preflight and temporary combined checkout: **CLEAN**.

The bundled interpreter was used, with TEMP/TMP pointing to writable scratch storage outside the repository. Test fixtures redirect the production staging path into a test-owned temporary directory. ZIP creation/reads and cleanup are real; wrapper subprocess execution, dependency classification fixtures and the Node install fixture retain their documented mocks.

RUNTIME_TEST: PASS (22/22 scoped C2 cases on the combined checkout)

## Limits and next checkpoint

The combined checkout contains current main and C2 Week 6–7 changes, not other members' unmerged Sprint 2 branches. Thus this is not a claim of all-role behavioral compatibility. Live AstrBot, real CLI subprocess/npm execution, generated-test execution, extracted-project startup, path-confinement security and staging concurrency remain NOT_RUN here. Existing Node dependency parsing, entry-point layout and subprocess exit-code concerns remain open.

The temporary merge is discarded after review; no merge into main or early Sprint 2 PR is performed. Week 8 is committed as `docs(c2): week 08 integration review` and published to course/c2. The execution report records final commit, current-policy scope check, remote synchronization and cleanup. No C2 Week 9 or later files are created. Sprint 2 closeout/PR remains the Week 9 checkpoint and must re-check the then-current main and required CI.
