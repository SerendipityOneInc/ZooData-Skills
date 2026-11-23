# WorkBuddy 打包与发布

格式依据官方 [Skill](https://open.workbuddy.cn/docs/skill)、[专家](https://open.workbuddy.cn/en/docs/expert)、[连接器](https://open.workbuddy.cn/docs/connector) 文档；2026-11-16 复核 Skill 和专家文档。源码/ZIP 校验、平台导入、真实会话和正式发布分别记录。

## 维护来源

- [targets.json](targets.json)：统一版本、Skill 触发描述、资源、能力及专家允许任务。
- [workbuddy.json](workbuddy.json)：中英文市场介绍、三个独立示例问题、专家卡片、图标和 MCP 配置。
- skills/、contracts/、experts/（含 agent-core/）：运行指令，职责见 [开发规范](DEVELOPMENT.md)。
- [zh-CN/README.md](zh-CN/README.md)：逐文件完整中文 Prompt，不进入发布包。

独立 Skill 与专家内置副本保持同源。竞品、市场选品和关键词专家分别预加载对应工作流及报告工具，其他专家的主分析 Skill 和报告 Skill 预加载，辅助分析 Skill 按条件使用；只有声明的 Skill 与任务进入专家装配。接口事实以实际 MCP 工具描述和 Schema 为准，完整 HTTP/CLI 手册不打包。

名称、介绍、标签和示例必须符合实际能力。技能名称保持英文唯一标识，展示名称采用“能力 · ZooData”。专家默认问题与三个 quickPrompts 的第一项一致。修改 Skill export_name 时同步所有绑定并重新打包；名称是否可用由平台确认。

## 本地构建

先完成 [职责与冲突检查](VALIDATION.md#pre-build-review)，再执行：

```bash
rtk python -m unittest discover -s components/checks -v
rtk python components/build_workbuddy.py
```

默认按工作流、专家和连接器生成发布包，并记录到构建报告。目前为三个工作流、六个公开专家、一个连接器。

```text
components/targets/
  skills/<workflow-name>.zip
  experts/<expert-name>.zip
  connectors/zoodata.zip
  build-report.json
```

targets/ 已加入 Git 忽略。默认构建覆盖当前 ZIP 和报告；上次构建报告中记录、且摘要未改变的停用 ZIP 会被移除。用户文件、未列入报告的 ZIP 和已修改旧包保留，不产生展开的 SKILL.md。发布时仅使用本次 build-report.json 列出的产物。程序不读取本机凭据、不访问网络、不安装或发布。

需要逐个检查数据 Skill、报告工具或旧分析 Skill 时，加上 `--include-components`，输出到所有 ClawHub 扫描范围之外的新目录或空目录：

```bash
rtk python components/build_workbuddy.py --include-components --output /private/tmp/zoodata-workbuddy-inspection
```

关键词研究工作流和专家均使用标识 `zoodata-keyword-research`，分别从 `skills/` 和 `experts/` 选择上传包。两种入口提供相同的三条示例和领域报告提纲。

## Skill 资源结构

每个 ZIP 包含一个同名根目录。Skill 限制为根目录 / 二级目录 / 文件；资源平铺并保持链接完整：

```text
<skill-name>/
  SKILL.md
  references/
    capabilities.json
    contracts-evidence.md
    contracts-reporting.md
    contracts-mcp.md
    contracts-seller-evidence.md
    skills-product-definition.md
    skills-product-methods.md
    skills-product-semantics.md
```

入口用 @references/ 引用任务定义、数据规则和报告规则；相应方法/语义、MCP 和商家资料规则按需读取。中文审阅版、开发规范和完整 API 手册不进入包。

业务流程包 zoodata-competitor-comparison.zip 内置本流程的任务提纲、数据方法和同源 HTML 生成器、模板及报告规范。安装该 Skill 并连接 ZooData 即可独立分析。竞品专家包内置同一份流程 Skill、流程直接使用的数据 Skill和报告生成 Skill。流程按所需指标选择数据 Skill，月购买量专项只加载月度销量；独立使用流程时读取随包的同源接口说明。

选品与市场研究工作流 zoodata-product-selection.zip 支持类目市场研究，按用户问题选择分析方法，内置筛选参数脚本、任务提纲与 HTML 生成器。选品专家和技能的标识均为 `zoodata-product-selection`。上传专家时选择 `experts/` 下的同名 ZIP，上传独立技能时选择 `skills/` 下的 ZIP。

专家包内置报告工具，独立业务工作流直接携带所需生成资源。开发验包时生成的 `zoodata-report-generator.zip` 结构如下：

```text
zoodata-report-generator/
  SKILL.md
  references/
    reporting.md
    layouts.md
    example.json
  scripts/
    render_report.py
  assets/
    template.html
```

专家默认使用报告 Skill 生成 HTML；五个分析 Skill 的独立会话仍默认 Markdown。报告 Skill 消费已有结果，不需要数据连接，不声明新的数据查询能力。

## 专家和连接器

专家 ZIP 包含 plugin.json、Agent 定义、必要 Skill、该专家专属头像及连接声明。独立技能的市场头像在确认页上传：竞品分析使用 assets/avatars/skill-competitor-comparison.png，选品分析使用 assets/avatars/skill-product-selection.png。公共运行模块由 targets.json 的 agent_sources 声明，build_workbuddy.py 统一合并进 Agent 指令。领域配置不再自行导入公共模块。开发规范不进入业务 Prompt，通用报告和专家答复检查各保留一份。所有专家均装配报告生成工具。独立业务工作流在自己的 ZIP 中携带同源生成资源和任务校验规则，独立安装即可生成相同版式。不要把 agent-core 单独发布为 Skill。

默认使用嵌入式 MCP 和用户自填 API Key。已有正式连接器 ID 时可改为依赖：

```bash
rtk python components/build_workbuddy.py --connector-id actual-published-connector-id
```

参数须替换为平台真实 ID。该模式不携带嵌入式 .mcp.json。连接器 source 为 zoodata，ZIP 为 zoodata.zip；旧 zoodata-amazon 的 assetId、发布 ID 和本地授权不会由改名自动迁移。独立 Skill 的新查询需要已配置的 ZooData 连接；兼容的用户资料可直接分析。

连接器整体服务范围不扩大 Skill 或专家职责。能力列表和 allowed_checks 是指令/装配约束，不是连接器权限控制。

## 本机更新和正式发布

上传竞品、市场选品或关键词研究前，对最终 ZIP 执行[发布前自审](VALIDATION.md#发布前自审)，分别记录客户端校验、业务用例和公约审核结论。

重建 ZIP 不会更新本机安装或已有会话。通过 WorkBuddy 原生 Skill 编辑、专家管理流程应用生成内容，保留用户连接及凭据，再核对版本和实际文件；真实会话验证使用新会话。

向开放平台分别上传 Skill、专家和连接器 ZIP。核对中文/英文元数据、三个独立示例、鉴权、空数据、额度不足及代表性任务，再按平台流程提交审核。静态检查不代表导入或会话通过。

WorkBuddy 包不执行 clawhub sync；根目录 ClawHub 发布单元继续按仓库现有流程维护。

市场选品打包时将数据方法中的操作名绑定到 `workbuddy.json` 的连接器 source。为使用不同服务名的本机环境打包时，将已安装 MCP 的服务名传给 `--mcp-source`，并用 `--output` 指定临时目录。安装时保留已有连接地址和凭证。市场选品专家与独立工作流使用该工作流在 `targets.json` 声明的版本。
