# D1 — Week 4：课程 Git 证据

COURSE_REPO: https://github.com/CS5351-0901/CS5351
BASE_MAIN: 83273a40a3ed3d616f24250bcb8e55ef7db5995c
BRANCH: course/d1
EXPECTED_DIFF_SCOPE: course_evidence/D1/**
TARGET_WEEK: 4
EXPECTED_COMMITS_VS_MAIN: 4

## 验收命令

```sh
git fetch origin --prune
git rev-parse origin/main
git rev-list --count origin/main..HEAD
git log --reverse --format="%H %s" origin/main..HEAD
git diff --name-only origin/main...HEAD
git status --short
```

## 预期文件清单

- course_evidence/D1/week01/role_and_scope.md
- course_evidence/D1/week02/source_map.md
- course_evidence/D1/week03/initial_findings.md
- course_evidence/D1/week04/review.md
- course_evidence/D1/week04/git_evidence.md

提交后核对实际清单、四周目录和提交数，并检查没有未来周、业务源码差异、课程仓库之外的 URL / SHA 或本机绝对路径。最终提交标识及检查结果在交付回复列出，避免本文件记录自身提交标识造成循环修改。
