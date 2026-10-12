# D1 — Week 4：集成静态复核

RUNTIME_TEST: NOT_RUN

本次只复核课程 main 到 sandbox / checker 的调用契约。下列不匹配是源码观察，尚未做运行复现或修复。

| 调用位置 / 参数 | 调用方行为 | 接收方行为 | 静态结论 |
| --- | --- | --- | --- |
| _call_sandbox / --code | json.dumps(code) 作为一个 argv 元素 | argparse 直接取得字符串，写入代码文件 | 多出 JSON 引号和转义；接收方未 json.loads，还原契约不一致 |
| _call_sandbox / --config | 传入 wall_time_limit、memory_limit_mb、file_size_limit_mb 的 JSON 文本 | open(args.config) 后 json.load | 接收方要求配置文件路径，调用方传内联 JSON，不匹配 |
| _call_sandbox / session-id、language、filename | 直接传入同名 CLI 参数 | argparse 后传给 execute | 名称对应；会话 ID 做字符替换，filename 未见相同约束，后续验证路径边界 |
| _call_sandbox / timeout | 外部 timeout 为配置墙钟值加 30 秒 | 内部默认 120 秒，可从配置文件覆盖 | 设计有内外两层超时；配置契约问题解决前不能断言用户配置已生效 |
| _call_js_checker / --code | json.dumps(code) | 直接将 options.code 写入检查文件 | 与 sandbox 相同的原始文本/JSON 编码不匹配，可能检查字符串字面量而非原代码 |
| _call_js_checker / --language | 直接传入 language | 支持 javascript、typescript、auto | 正常枚举名称对应；未知值没有统一拒绝，需边界验证 |

## 返回与故障处理

- Sandbox 常规入口输出 JSON；代码执行失败可体现在 success=false / exit_code 中，而 CLI 本身并不必然非零退出。调用方解析成功时保留业务结果；子进程非零时返回 stderr 错误。
- JS checker 常规失败可退出 1 并输出有效 JSON，调用方保留解析该 JSON 的逻辑，契约在这点一致。
- JS 脚本缺失、Node 不可用、超时和一般异常时，调用方多处返回 passed=true 并附 error；后续需验证上游如何处理，以免把未执行当成通过。
- package.json 声明 Node >=16 与两项开发依赖；checker 使用 which 和 PATH 命令探测。Windows 和仅本地依赖安装的可用性仍待验证。

## 本阶段交付范围

Week 1–4 仅新增 course_evidence/D1/** 的五份文档，分别说明职责、模块映射、静态发现、集成复核与 Git 基线。业务源码保持课程 main 状态。四次提交使用真实当前日期；前三周文档明确 WEEK4_CATCH_UP。未创建 Week 5 或更晚文件。

Week 4 checkpoint 验收以实际 Git 命令输出为准：四次个人提交、限定路径、四周目录完整、无未来周文件、无禁止元数据、工作区干净。这里的文档交付验收不表示 sandbox 或 checker 运行测试通过。
