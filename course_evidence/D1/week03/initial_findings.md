WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# D1 — Week 3：初步静态发现

RUNTIME_TEST: NOT_RUN

以下均来自课程 main 的静态源码阅读，不是复现结果或安全保证。Week 1–4 不修改业务源码；验证和修复安排在 Week 5+。

## Sandbox 资源与平台边界

- 默认 CPU 60 秒、墙钟 120 秒、内存 512 MB、单文件 10 MB、总文件 50 MB、max_files=50、max_subprocesses=5。
- ResourceLimiter.apply_limits 设置 CPU、AS、DATA、STACK、FSIZE、NPROC、NOFILE；限制应用于当前 sandbox 进程，异常被忽略，不能据此断言所有限制生效。
- 顶层直接 import resource；TimeoutManager 使用 SIGALRM / alarm。标准执行还依赖 python3、Unix 风格 PATH 和进程组处理；Windows 兼容性需要单独验证。
- StandardExecutor._build_env 对默认字符串 workspace_root 使用路径除法运算，存在类型不匹配风险；外层虽保存了 Path，但没有转换这个配置字段。
- allow_network=False 只调整代理环境变量；network_whitelist 未形成可见的网络隔离机制。文件权限规则也不能视为完整隔离边界。
- 文件数量判断在 append 后使用大于 max_files，总大小超过阈值仅产生 warning；这些是收集策略，不能等同于写入硬限制。

## JS Checker 输入输出

- --code 被当作原始文本使用；--code-file 读取 UTF-8 文件；--language 默认 auto；--output 将 JSON 写入指定文件。
- 常规结果提供 passed、issues、quality_score、summary 和四类分项；高危/严重问题或质量评分低于 75 可导致失败。
- _checkCommand 使用 which 检查 eslint/tsc，运行命令依赖 PATH；package.json 的本地 devDependencies 不意味着直接 node 调用一定能找到这些命令。
- 缺少 ESLint/tsc 时返回分项 error，但 check 的 passed 没有统一按这些 error 置 false；可能出现工具未运行而总体通过的表达。
- 临时目录及 main.js/main.ts 文件名固定，finally 删除整个临时目录；并发运行存在相互覆盖和清理风险。

## Week 5+ 验证清单（均未执行）

1. 参数契约：使用带换行、引号、中文的原始代码，核对调用方与 CLI 接收值；核对 sandbox config 文件路径与内联 JSON 的差异。
2. Windows：验证 resource 导入、计时机制、python3 解析、PATH、workspace_root 类型及含空格路径。
3. Node.js：验证 Node 缺失、仅本地安装 eslint/tsc、缺少检查工具、JS/TS 正反样例。
4. 返回值：验证非零退出码但 JSON 有效、JSON 损坏、超时、空输入，区分检查未执行与检查通过。
5. 资源边界：在受控测试环境验证 CPU/墙钟/文件阈值、子进程终止与会话路径约束，避免把配置声明当作有效限制。
6. 并发：检查多个 checker 调用能否各自保留输入与结果，不相互删除临时文件。
