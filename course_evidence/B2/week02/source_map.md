WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# B2 Source Map (Week 2)

以下映射基于当前课程 `main` 的静态源码观察，仅覆盖本角色负责模块。不含外部仓库 URL、外部 commit SHA、来源追踪字段或本机绝对路径。

## main.py::_is_exit_command

- 作用：判断输入文本是否为退出指令。
- 实现：对文本执行 `re.search(r'/exitconver', text, re.IGNORECASE)`，命中返回 `True`。
- 依赖：标准库 `re`。

## main.py::_sanitize_session_id

- 作用：由群组 ID 与用户 ID 生成规范化的会话 ID。
- 实现：返回 `f"{group_id}_{user_id}"`，并将 `:` 与 `/` 替换为 `_`。
- 说明：会话 ID 同时用于 `active_sessions` 键名与 workspace 下的目录名。

## main.py::_cleanup_session

- 作用：清理会话对应的工作目录。
- 实现：若 `self.workspace / session_id` 目录存在，则 `shutil.rmtree(session_dir, ignore_errors=True)`。
- 依赖：标准库 `shutil`。

## active_sessions

- 定义：`self.active_sessions: Dict[str, Dict[str, Any]] = {}`，在插件初始化时创建。
- 作用：进程内会话状态表，键为会话 ID，值为包含 `active`、`requirement`、`step`、`start_time` 等字段的字典。
- 生命周期：`agent_command` 启动会话时写入，退出/完成/异常时 pop。

## main.py::_create_process_json

- 作用：为会话创建 `process.json` 状态文件。
- 实现：写入 `workspace / session_id / process.json`，包含 `session_id`、`requirement`、`project_type`、`project_size`、`status`、`current_step`、`completed_steps`、`snapshots`、`created_at`、`updated_at` 等字段。
- 依赖：标准库 `json`、`time`；父目录自动创建。
