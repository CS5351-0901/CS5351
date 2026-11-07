WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 2 — 当前课程 main 模块映射

下列位置根据本次读取的课程 main 静态源码整理，行号仅用于定位。

| 模块 | 位置 | 职责与连接 |
| --- | --- | --- |
| `_call_packager` | `main.py:305–339` | 接收 files、test_files、name、description、project_type；调用 Python CLI 并反序列化 stdout。 |
| 主流程交付调用 | `main.py:626–687` | 构造源文件与固定 Python 测试模板，保存快照，调用打包器；成功后发送 ZIP 并删除归档文件。 |
| 打包 CLI `main()` | `skills/CodeAgent/scripts/codeagent_packager.py:558` | 解析 JSON 文件列表或扫描文件目录，创建 ProjectPackager，输出结果 JSON；错误状态以非零退出码返回。 |
| `ProjectFile` / `ProjectInfo` | 同脚本 `:22` / `:32` | 保存文件内容、语言、项目依赖、测试文件、入口与使用命令。 |
| `DependencyGenerator` | 同脚本 `:131` | AST 提取 Python import，按运行环境分类模块；正则识别 Node 依赖；生成三类依赖配置。 |
| `ProjectPackager` | 同脚本 `:292` | 按扩展名频率检测语言，构建项目元数据，写入 src 和 tests、README 与配置，清理并压缩。 |
| `create_project_file` | 同脚本 `:535` | 根据 name、content、description 创建文件对象，计算 UTF-8 字节大小并映射语言。 |
| `ReadmeGenerator` | 同脚本 `:49` | 从项目元数据生成说明、依赖、使用命令和测试命令。 |

调用关系：主流程 → `_call_packager` → CLI `main()` → `ProjectPackager.pack()` → `build_project_info()` / `DependencyGenerator` / `ReadmeGenerator` → ZIP 与结果字典 → 主流程交付。

依赖生成只扫描业务文件，不扫描 test_files；生成测试的上游逻辑属于接口复核范围，本阶段不修改它。
