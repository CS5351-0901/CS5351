WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# B2 Role and Scope (Week 1)

## Role

B2 负责 CodeAgent 插件 `main.py` 中与 **会话生命周期（session / state）** 相关的状态管理职责，以及与之配套的会话状态数据文件生成。

## Owned Scope

B2 职责覆盖以下 `main.py` 条目：

- `main.py::_is_exit_command` — 识别退出指令（`/exitconver`）
- `main.py::_sanitize_session_id` — 由群组 ID 与用户 ID 生成规范化的会话 ID
- `main.py::_cleanup_session` — 清理会话对应的工作目录（workspace 下的临时文件）
- `active_sessions` — 进程内会话状态表（`Dict[str, Dict[str, Any]]`）
- `main.py::_create_process_json` — 为会话创建 `process.json` 状态文件

## Branch / Evidence Policy (Week 1–4)

- Week 1–4 个人分支仅提交角色 evidence（`course_evidence/B2/**`）。
- 不修改业务源码。
- evidence 文件不含外部源码地址、commit SHA、来源字段。
