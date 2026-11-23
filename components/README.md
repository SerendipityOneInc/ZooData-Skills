# WorkBuddy 组件

开发与 review 先读 [DEVELOPMENT.md](DEVELOPMENT.md)。本目录维护五个分析 Skill、一个报告生成 Skill、六个专家及 WorkBuddy 打包程序；根目录的 ClawHub 发布单元保持原有结构。

## 来源与职责

| 来源 | 负责内容 |
|---|---|
| [targets.json](targets.json) | 版本、Skill 资源/能力、专家绑定与允许任务 |
| [workbuddy.json](workbuddy.json) | 中英文市场介绍、示例、专家卡片和连接器配置 |
| skill/datas/*/definition.md | 分析对象、任务、输入和报告内容 |
| [数据 Skill 共享取数规则](contract/query.md) | 查询窗口、排序分页、响应复用与异常处理 |
| skill/datas/*/methods.md、semantics.md | 分析方法、指标含义及推断边界 |
| [关键词研究流程](skill/workflows/keyword-research/definition.md) | 拓词分组、需求与竞争画像、需求趋势和指定商品流量词研究 |
| [选品流程](skill/workflows/product-selection/definition.md) | 研究类目市场、按模式或条件筛选商品、评估指定候选 |
| [竞品对比流程](skill/workflows/competitor-comparison/definition.md) | 工作流任务、比较维度及报告提纲 |
| tools/report/ | 报告生成入口、组件说明、公共 HTML 模板和生成脚本 |
| contract/*.md | 共享取数、证据、商家资料与报告规则 |
| expert/agent-core/*.md | 用户沟通、报告解读与答复检查 |
| expert/*.md | 专家领域、研究角度、能力用途、启用条件及具体判断限制 |
| [zh-CN/README.md](zh-CN/README.md) | 与英文目录、文件逐一对应的完整中文 Prompt，不参与打包 |
| [build_workbuddy.py](build_workbuddy.py) | 本地装配与打包 |
| [PUBLISHING.md](PUBLISHING.md)、[VALIDATION.md](VALIDATION.md) | 发布说明与验证要求 |

Skill 提供专业数据分析报告，专家基于业务目标解读报告和提出方案。两者在同一宿主 Agent 的上下文中执行。独立 Skill Session 使用相同的分析方法，不依赖 ZooData 专家配置。

竞品、市场选品和关键词研究分别预加载对应工作流和报告工具，流程内置获准的数据方法。其余专家的主分析 Skill 和报告 Skill 预加载；辅助分析 Skill 只按声明的业务条件加载。每个专家只携带自身领域相关的 Skill 和允许任务，独立判断能否回答，不配置其他专家名录或转介流程。数据与结论规则的所有权以开发规范和各入口责任图为准。

## 专业 Skill

| 对象 | 来源与任务 |
|---|---|
| 类目市场 | [市场分析](skill/datas/market/definition.md)：发现、画像、结构、趋势、新品构成 |
| 商品 | [商品分析](skill/datas/product/definition.md)：筛选、事实、页面内容、历史、对比、价格带/品牌 |
| 关键词 | [关键词分析](skill/datas/keyword/definition.md)：拓词、基础指标统计、关键词画像、趋势画像及周度趋势数据 |
| 商品详情 | [商品详情](skill/datas/product-detail/definition.md)，按指定商品 ASIN 查询 |
| 商品评价画像 | [商品评价画像](skill/datas/product-review-profile/definition.md) |
| 类目评价画像 | [类目评价画像](skill/datas/market-review-profile/definition.md) |
| 单接口评论原文 | [已存评论](skill/datas/review-search/definition.md)，按 ASIN 读取所属父体的评论 |
| 单接口商品月度销量 | [月度序列](skill/datas/product-sales-trend/definition.md)，按单个 ASIN 获取目录月度数据 |
| 商品流量 | [流量分析](skill/datas/traffic/definition.md)：结构、趋势、贡献词、指定词变化 |
| 消费者反馈 | [评论分析](skill/datas/review/definition.md)：主题画像、主题证据、反馈对比 |

## 专家

[选品与市场研究](expert/product-selection.md)、[关键词研究](expert/keyword-research.md)、[流量诊断](expert/traffic-diagnosis.md)、[消费者洞察与产品改良](expert/review-voc.md)、[竞品研究](expert/competitor-insight.md)、[商品诊断与优化](expert/product-research.md)。

## 研究报告交付

专家先确认一个分析目标及必要的比较依据，再生成一份从总到分的 HTML 研究报告，采用各自的领域提纲和统一的[报告规范](contract/report.md)。同一份报告不混合不同排序的候选池，每项信息只展示一次。报告按固定内容位置组合概览、图表、紧凑表格和业务解释，交付后不主动推荐问题或弹出研究选择面板。必要的分析前输入确认仍保留。独立业务工作流与对应专家使用相同的提纲和 HTML 模板；数据 Skill 提供分析结果。

[报告生成 Skill](tools/report/definition.md)统一维护[组件](tools/report/layouts.md)、[模板](tools/report/assets/template.html)和[生成脚本](tools/report/scripts/render_report.py)。专家安排业务内容，报告 Skill 将结构化内容填入公共模板，不获取数据、不决定结论。

## 加载与接口

入口加载任务目录、数据规则和报告规范；方法、语义、MCP 和商家资料规则按任务需要读取。完整 API 手册不进入运行包，调用以连接器实际工具描述和 Schema 为准。根目录现有 API 文档保留为开发参考。

分析 Skill 资源在发布包中平铺到 references/；报告 Skill 的资源分别放在 references/、scripts/、assets/，保持 WorkBuddy 已验证的两级 Skill 目录结构。agent-core 由 targets.json 和 build_workbuddy.py 统一装配进专家指令，领域配置不重复导入；它不作为 Skill 发布。开发规范不进入运行指令。独立与专家内置 Skill 由同一来源生成。

## 打包边界

默认按每个业务工作流一个 ZIP 输出到 skills/，目前为竞品分析、市场选品和关键词研究三个工作流；另生成六个公开专家 ZIP 和一个连接器 ZIP，位于 Git 忽略的 components/targets/，不在仓库内生成可被 ClawHub 发现的 Skill 入口。外部空目录可用于展开检查。

能力列表和允许任务是装配/指令约束，不是平台工具权限。构建不连接服务、不安装、不发布。连接器承载 ZooData 数据服务；专家和 Skill 的范围由自身定义决定。构建命令及嵌入式 MCP / 已发布连接器两种模式见 [发布说明](PUBLISHING.md)。
