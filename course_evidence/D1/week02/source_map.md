WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# D1 — Week 2：课程 main 模块映射

| 模块 | 入口与职责 | 输入 / 输出及关联 |
| --- | --- | --- |
| skills/CodeAgent/scripts/codeagent_sandbox.py | main、SandboxConfig、ResourceLimiter、TimeoutManager、SandboxExecutor.execute | CLI 接收 code 或 code-file、session-id、language、filename、args、config；输出 JSON 执行结果 |
| skills/CodeAgent/scripts/codeagent_js_checker.js | main、JavaScriptChecker.check | 接收原始代码和 language；组合 ESLint、TypeScript、安全规则、质量评分；输出 JSON 或写入 output 文件 |
| skills/CodeAgent/scripts/package.json | Node ESM 包配置 | Node >=16；devDependencies 为 eslint ^8.57.0、typescript ^5.3.0；npm test 调用 checker --test |
| main.py::_call_sandbox | 插件执行适配 | 获取 code_running_time、memory_limit、max_file_size，启动 python3 子进程，解析 stdout JSON，返回 success/error 等字段 |
| main.py::_call_js_checker | 插件检查适配 | 先探测 node -v，启动 node 子进程；即使退出码非零仍尝试解析 JSON，返回 passed/issues 等字段 |

SandboxExecutor 按会话创建目录，写入代码，应用资源限制，再选 RestrictedPython 或 StandardExecutor。标准执行支持 python、javascript、bash；结果包含 success、stdout、stderr、exit_code、time_elapsed、files、error、security_warning、execution_method，收集阶段可能增加 warning。

JavaScriptChecker 支持 javascript、typescript、auto，auto 使用模式识别语言。结果包含 issues、passed、quality_score、summary，以及 eslint、typescript、security、quality 分项。常规 CLI 在检查失败或出现 high/critical 问题时退出 1；不能仅凭非零退出码认定没有可用 JSON。

映射仅根据当前课程 main 阅读所得。调用参数差异和环境约束记录于 Week 3 / Week 4；此处不代表动态验证已通过。
