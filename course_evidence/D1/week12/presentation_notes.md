# D1 — Week 12 Presentation / Report Preparation

记录日期：2026-11-24（Asia/Shanghai）

TARGET_WEEK: 12

MEMBER: D1

BRANCH: course/d1

已验证工程版本：`b9ad819`；本次 fetch 后的 origin/main：`60743b0`。

本文是个人展示及 final report 的素材，不代表已经完成团队演示或最终验收。
本周重跑角色验证并整理已有贡献；没有新建 Week 13 文件或提前创建最终 PR。

## 1. 角色范围与接口

D1 负责 sandbox / JavaScript checker 及其插件适配层：

| 所属模块 | 责任 | 本项目实际交付 |
| --- | --- | --- |
| `main.py::_call_sandbox` | 把代码、会话、语言、文件名及限制配置传给执行器，接收 JSON 结果 | 原始代码传递、临时配置文件、错误处理及清理 |
| `main.py::_call_js_checker` | 调用 Node 检查器并返回检查结果 | 原始 JS/TS 输入、检查器不可用或异常时返回失败 |
| `skills/CodeAgent/scripts/codeagent_sandbox.py` | 执行代码、超时处理与产物收集 | Windows 兼容、当前 Python 解释器、路径准备、文件数量上限修复 |
| `skills/CodeAgent/scripts/codeagent_js_checker.js` | JS/TS 静态检查、诊断与 JSON 输出 | 独立临时目录、工具发现、动态 Function 规则边界修复 |
| `skills/CodeAgent/scripts/package.json` | 检查器的依赖声明，属于 D1 范围 | 本轮没有修改，不计作个人工程增量 |

调用关系：插件适配方法 → CLI 参数／临时配置 → sandbox 或 checker → JSON 结果。
测试通过 AstrBot 注册依赖 stub 加载真实插件方法；真实 CLI 测试另外启动子进程。
这两种验证不能等同于真实 AstrBot 事件分发测试。

## 2. 可追溯的工程贡献

| 阶段／提交 | 问题与改动 | 可查证材料 |
| --- | --- | --- |
| Week 5，`8be7051` | 建立角色 baseline，并明确记录当时缺陷 | [baseline.md](../week05/baseline.md)、`tests/roles/d1/test_baseline.py` |
| Week 6–7，`e74446e` | 修复重复 JSON 编码；配置改为可读临时文件；checker 适配层异常返回失败；修复 Windows 启动、解释器和目录准备；checker 临时目录隔离与规则边界 | [contract_repair.md](../week06/contract_repair.md)、[platform_integration.md](../week07/platform_integration.md) |
| Week 7，`7de2841` | 添加真实适配层到 sandbox 的 Windows 多行 Unicode 子进程验证 | `tests/roles/d1/test_baseline.py` |
| Week 8–9，`f764c59`、`b3294aa` | main 集成复核、Sprint 2 汇总和接口迁移依赖记录 | [integration_review.md](../week08/integration_review.md)、[sprint2_summary.md](../week09/sprint2_summary.md) |
| Week 10，`429c4da` | 修复返回文件数量 off-by-one，新增 3 个真实 CLI 测试 | [improvement.md](../week10/improvement.md)、`tests/roles/d1/test_week10_file_limits.py` |
| Week 11，`b9ad819` | 新增 6 个真实 CLI 失败路径及文件过滤测试，并审查来源元数据 | [regression.md](../week11/regression.md)、`tests/roles/d1/test_week11_regression.py` |

Sprint 2 的 [PR #15](https://github.com/CS5351-0901/CS5351/pull/15) 已合并，
merge commit 为 `7506aee21e881a794cd3394f8b91a9db85415f91`。
Week 10–11 工程仍在个人分支，尚未计为合入 main 的 Sprint 3 成果。
早期 evidence 中“PR 未合并”和“A1 待迁移”描述保留其历史状态；
A1 的配置文件契约迁移已在当前 main 完成，参见团队 Week 9 closeout。

## 3. 展示重点：问题、修复与证据

### 例一：输入／配置契约

原先适配层对源代码再做一次 JSON 编码，使多行和 Unicode 输入与 CLI 期望不一致；
配置也使用了与执行器文件读取接口不匹配的形式。现在 `--code` 传原始字符串，
`--config` 传临时 UTF-8 JSON 文件路径，并在调用结束后清理。
可展示的证据包括原始输入断言、调用期间读取配置文件、返回后确认清理，以及真实 Windows 子进程测试。

### 例二：文件数量上限（最适合现场复现）

旧逻辑先追加文件，再判断数量是否“大于”上限，因此 `max_files=1` 返回 2 个文件，
`max_files=0` 仍返回 1 个。Week 10 先运行测试，观察到 3 项中 2 项失败，
再把容量检查移到收集下一项之前。修复后 0、1 和大于产物数量的上限测试全部通过。
该限制控制的是返回的文件列表数量，不能据此宣称限制了代码的磁盘写入。

### 例三：异常与平台边界

Windows 缺少 Unix 专属模块／信号时，sandbox 可以启动并走子进程执行路径。
Week 11 的可信 fixture 中，30 秒 sleep 在 1 秒 wall timeout 配置下返回失败；
语法错误和运行异常也返回失败及诊断。checker 适配层在工具入口不可用或异常时返回失败；
checker 内部 ESLint／TypeScript 缺失的报告不等同于已完成这两种工具的语义检查。

## 4. 2026-11-24 实际验证

环境：Windows、Python 3.11.5、Node v22.22.3。从课程仓库根目录执行：

```text
python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v
Ran 34 tests in 6.212s
OK
exit code 0

node --check skills/CodeAgent/scripts/codeagent_js_checker.js
exit code 0
```

| 测试来源 | 数量 | 今日结果 |
| --- | --- | --- |
| `test_baseline.py`：适配层契约、真实 checker CLI、sandbox 平台／Unicode 路径 | 25 | OK |
| `test_week10_file_limits.py`：返回文件数量上限 | 3 | OK |
| `test_week11_regression.py`：语法、异常、超时、隐藏／超大文件过滤和 Unicode 元数据 | 6 | OK |
| 合计 | 34 | 全部通过；无 skip、无 expected failure |

测试数量不表示代码覆盖率；Node `--check` 仅验证脚本语法。
Week 11 记录的 A1 两项安装器测试环境报错，本周没有重跑或宣称解决。
本次只对 D1 结果作出 PASS 判断。

## 5. 可直接采用的 slides 结构与演示步骤

1. **职责与接口**：使用第 1 节调用关系，说明 D1 如何把插件请求送入 CLI 并接回 JSON。
2. **关键缺陷与修复**：用第 3 节的原始代码／配置契约和文件上限案例说明用户可观察的前后差异。
3. **证据与边界**：展示今日 34 项测试结果，区分 stub 适配层测试和真实子进程测试，再说明尚未验证的部分。

现场演示优先运行这一组短测试：

```text
python -B -m unittest discover -s tests/roles/d1 -p test_week10_file_limits.py -v
```

预期为 3 项 OK。测试会在临时目录生成四个文件，并分别检查上限为 0、1、10 的行为。
如需展示完整验证，再运行第 4 节的 34 项测试命令。
历史失败证据引用 Week 10 文档，不需要现场回退生产代码。
演示准备步骤不是已完成真实课堂展示的声明。

## 6. 仍存在的限制

- 未运行真实 AstrBot 启动、事件分发和完整 `/agent` 流程。
- 本次执行环境是 Windows，未验证 Linux/macOS 运行行为；Windows CPU／内存／进程资源限制未被强制执行。
- 网络隔离、白名单和文件名路径包含性仍未验证；该执行器不能据此视为 OS 安全边界。
- 未安装并实际验证 ESLint／TypeScript 的完整诊断；目前证明的是相关报告和接口行为。
- 文件数量上限不限制总磁盘写入，也没有证明并发会话、输出内存或所有子孙进程的隔离。
- 整体团队测试与 Sprint 3 最终集成不在本次个人 Week 12 验收内。

## 7. 可复制的贡献摘要

**中文：** 我负责 CodeAgent 的 sandbox、JavaScript checker 及插件适配层。
我修复了源代码与配置传递契约、检查器异常处理、Windows 执行兼容性、检查器临时目录隔离，
以及产物列表数量上限的 off-by-one 问题，并维护契约、CLI 和失败路径回归测试。
2026-11-24 在 Windows 上重跑的 34 项 D1 测试全部通过。
验证范围为角色接口及可信 fixture 的子进程行为，未覆盖完整 AstrBot 运行与 OS 级隔离。

**English:** My D1 contribution covers CodeAgent's sandbox, JavaScript checker,
and plugin adapters. I repaired source/configuration argument contracts,
checker failure handling, Windows execution compatibility, checker temporary
directory isolation, and an off-by-one artifact-count limit. I also maintained
contract, CLI, and failure-path regression tests. All 34 D1 tests passed on
Windows on 24 November 2026. This evidence covers role interfaces and trusted
subprocess fixtures; live AstrBot operation and OS-level isolation remain
unverified.

WEEK12_PRESENTATION_EVIDENCE: PREPARED

D1_WEEK12_VALIDATION: PASS (34 executed tests)

SPRINT3_FINAL_INTEGRATION: NOT_YET_DUE (Week 13)

WORKTREE_NOTE: Pre-existing untracked output/ and tmp/ are preserved and excluded from this delivery.
