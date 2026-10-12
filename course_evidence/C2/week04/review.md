# Week 4 — 接口契约复核

RUNTIME_TEST: NOT_RUN

本次只静态复核课程 main 的接口，并准备 C2 Week 1–4 角色证据。

| 项目 | main.py 包装函数 | packager CLI / 实现 | 复核结论 |
| --- | --- | --- | --- |
| 业务文件 | files → JSON `--files` | 解析列表并读取 name/content/description | 字段契约对应；缺少结构与路径校验。 |
| 测试文件 | 非空时传 `--test-files` | 空时默认空列表 | 传参对应；Python 空测试目录风险见 Week 3。 |
| 名称和描述 | `--name`、`--description` | 创建项目名；空描述被替换为默认描述 | 存在空描述语义差异，名称未见边界限制。 |
| 类型 | project_type → `--type` | 保存 project_type；按扩展名检测语言 | 参数传输一致，类型参数不保证控制打包语言。 |
| 可选能力 | 不传入口、目录扫描和结果输出文件选项 | CLI 支持 `--main`、`--file-dir`、`--output` | 当前包装函数只覆盖 JSON 文件列表和 stdout 结果路径；extra_files 仅 pack API 支持。 |
| 返回 | 直接解析 stdout JSON | 常规 pack 结果包含 success/zip_path/file_count/size/error | 正常协议对应；包装函数未校验类型、字段和退出码。 |
| 错误 | 脚本缺失及异常返回 success=false/error | pack 捕获异常；CLI 失败非零退出；部分解析错误没有 JSON | 错误路径返回结构不统一，stderr 没有被包装函数作为诊断使用。 |
| 时限 | 子进程 120 秒 | npm 安装上限 300 秒 | 超时预算不一致，需后续实际验证。 |

主流程以 success 决定是否进入交付分支，并检查 ZIP 存在后发送、删除归档。没有验证 ZIP 内容、解压安装、生成测试执行结果或回传文件计数；成功打包不能等同于可运行交付。

Week 1–4 仅增加本角色的五个 Markdown 文件：week01 角色范围、week02 模块映射、week03 静态发现、week04 接口复核与 Git 证据。未更改业务源码。提交与推送后需按 git_evidence.md 的命令核对四个提交、目录边界、未来周文件和工作区状态；最终结果以实际 Git 检查为准。
