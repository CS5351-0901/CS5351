# Week 4 — 课程 Git 证据

COURSE_REPO: https://github.com/CS5351-0901/CS5351
BASE_MAIN: 83273a40a3ed3d616f24250bcb8e55ef7db5995c
BRANCH: course/c2
EXPECTED_DIFF_SCOPE: course_evidence/C2/**

启动时已实际检查课程远端分支，main 存在，course/c2 不存在。在全新课程副本中 fetch 后，从上述 origin/main 建立 course/c2；起点工作区干净。未恢复或推送任何旧本机分支。

本阶段使用真实当前 Git 日期，不修改提交时间。Week 1–3 文件包含 WEEK4_CATCH_UP 声明。

预定的四个提交（顺序如下）：
1. `docs(c2): week 01 define role and scope`
2. `docs(c2): week 02 map owned source`
3. `docs(c2): week 03 record initial findings`
4. `docs(c2): week 04 review staged integration`

验收命令（提交和推送后执行，最终执行报告记录结果）：
```bash
git fetch origin --prune
git rev-list --count origin/main..HEAD
git diff --name-only origin/main...HEAD
git status --short
git log --reverse --format="%H %s" origin/main..HEAD
git ls-tree -r --name-only HEAD course_evidence/C2
git rev-parse HEAD origin/course/c2
```

验收条件：相对 main 恰好四个提交；diff 仅含 course_evidence/C2 下五个预期文档；week01–week04 均存在且无后续周文件；证据不含外部仓库地址、外部提交标识和本机绝对路径；工作区干净，推送后的远端分支与 HEAD 一致。

运行时测试与 Git 验收分开记录：业务 RUNTIME_TEST 为 NOT_RUN。四个提交的最终标识由提交后的实际 Git 日志取得，避免在提交内记录其自身尚不存在的标识。
