WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# D1 — Week 1：职责与范围

D1 负责 Sandbox / JavaScript Checker：
- skills/CodeAgent/scripts/codeagent_sandbox.py：执行入口、资源限制、会话目录及结果收集。
- skills/CodeAgent/scripts/codeagent_js_checker.js：JavaScript / TypeScript 检查和 JSON 结果。
- skills/CodeAgent/scripts/package.json：检查器依赖、Node.js 版本要求和脚本。
- main.py::_call_sandbox：插件到 sandbox 的参数和返回值适配。
- main.py::_call_js_checker：插件到 checker 的参数和返回值适配。

Week 1–4 个人分支只提交 course_evidence/D1/** 下的角色 evidence。当前阶段只阅读课程 main 的业务源码并记录静态观察，不修改业务实现，不声称完成运行验证。后续工程阶段再为职责范围内问题建立测试与修复；共享 main.py 的修改须遵守 ownership / review 规则。

本次目标为 Week 4。提交采用执行时真实 Git 日期，不回填历史日期，不创建 Week 5 或更晚文件。
