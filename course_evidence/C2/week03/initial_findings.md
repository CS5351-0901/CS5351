WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
This file/commit uses the real current Git date and does not claim that the file existed earlier.

# Week 3 — 初始静态发现

RUNTIME_TEST: NOT_RUN

本记录仅基于课程 main 静态阅读；以下是源码行为与待验证风险，不代表运行结果。

## 输入、输出与打包边界

- 包装函数将字典列表序列化为 `--files` 和可选 `--test-files`。列表元素使用 name、content、description；其他字段未传入项目文件模型。
- `pack()` 返回 success、zip_path、file_count、size、error；CLI 正常路径向 stdout 输出 JSON，向 stderr 输出摘要。参数解析和空文件列表可在 JSON 结果生成前失败。
- 业务文件写入项目的 `src/`，测试文件写入 `tests/`；项目根部生成 README 和语言相关配置。调用方传入的 README、空依赖清单与空配置也会作为业务文件进入 src。
- 语言由业务文件扩展名频率确定，project_type 仅记录在项目元数据中，不直接控制 Python / Node 打包分支。
- Node 分支调用 npm 安装，然后遍历项目目录归档；清理规则主要针对 Python 缓存，不排除 node_modules。归档完成后清理临时目录，主流程发送后删除 ZIP。

## 依赖生成观察

1. Python AST 提取顶层模块名；语法错误被吞掉并返回空集合。分类阶段实际 import 模块，只有模块文件路径包含 site-packages 才视为外部依赖，因此依赖识别受当前环境影响，并有导入副作用。未安装包可能漏报，导入名与发行包名也未转换。
2. Python 依赖清单不固定版本，不扫描测试专用 import。默认开发依赖是固定工具集合。
3. Node 扫描先移除引号字符串，而后匹配依赖引号中的名称；静态上存在常规 import / require 包名被删除而漏报的风险。子路径包名规范化与裸 Node 内置模块过滤也需验证。
4. package.json 使用 latest；pyproject 以字符串插值生成，描述中的引号和换行需要验证。无业务依赖时不生成安装命令，即使仍有开发依赖。

## Week 5 起需要执行的验证

| 待验证点 | 静态依据与验证方向 |
| --- | --- |
| 无测试文件的 Python 项目 | tests 目录仅在 test_files 非空时建立，Python 分支却总写 tests/__init__.py；验证空值和空列表失败路径。 |
| 生成测试与打包前验证 | 主流程固定生成 Python 测试并断言 main() 非空，打包前未运行该生成测试；需验证返回 None 的入口及 JS / TS 项目的模板适配。之前执行核心代码不等于运行生成测试。 |
| 文件路径边界 | name、文件名及 extra_files 未见路径归一化与目录约束；验证父目录跳转、绝对文件名、重名及嵌套测试目录。 |
| 入口与布局 | 文件写入 src，但默认使用命令和 Node main 字段使用未加 src 的入口名；验证解压后安装、启动与测试。 |
| 安装失败和超时 | npm 返回的布尔状态未被 pack 使用；包装函数超时 120 秒，而 npm 超时 300 秒；验证错误传播及子进程清理。 |
| 返回协议 | 包装函数不检查退出码或结果结构，直接解析 stdout；验证非 JSON、空输出、缺字段和失败退出码。 |
| 归档计数及并发 | file_count 固定为输入文件数加测试数再加 2，不是 ZIP 实际条目数；临时目录和 ZIP 名使用秒级时间，需验证同秒调用与实际产物计数。 |

以上验证均尚未执行；本阶段不运行打包脚本、不安装生成项目依赖、不声称交付包可以运行。
