# Week 4 — B1 Git Evidence

This record captures the course Git state after the Week 1–3 evidence commits and immediately before the Week 4 evidence commit.

```text
COURSE_REPO: https://github.com/CS5351-0901/CS5351
BASE_MAIN: 83273a40a3ed3d616f24250bcb8e55ef7db5995c
BRANCH: course/b1
EXPECTED_DIFF_SCOPE: course_evidence/B1/**
COMMITS_VS_MAIN_BEFORE_WEEK04: 3
ANCESTRY_FROM_MAIN: PASS
```

The remote `main` branch was confirmed before creating `course/b1`, and the local baseline matched `origin/main`. The remote did not contain `course/b1`, so the local branch was created cleanly from the current `origin/main`.

Immediately before the Week 4 commit, `git rev-list --count origin/main..HEAD` returned `3`. The preceding commits are `33cd020` for Week 3, `a97d69d` for Week 2, and `d0446ad` for Week 1. `git merge-base --is-ancestor origin/main HEAD` passed. The committed diff against `origin/main` contained only the three earlier B1 evidence files, while the Week 4 directory remained untracked for its own commit.

After the Week 4 commit, the final `COMMITS_VS_MAIN=4`, changed-path scope, future-week absence, and clean-worktree gate must be evaluated separately rather than claimed in advance.
