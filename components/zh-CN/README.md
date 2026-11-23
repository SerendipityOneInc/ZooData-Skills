# WorkBuddy 中文 Prompt

这里逐文件提供英文 Prompt 的完整中文版本，目录和文件名与英文来源对应。字段、任务标识、工具名与资源路径保留原文。英文来源用于当前运行；中文文件用于阅读和核对，不进入发布包。

每份文件标注英文来源及摘要，修改英文后须同步对应中文。

## 专家公共 Prompt

- [解读报告并检查业务判断](expert/agent-core/delivery.md)
- [与用户沟通](expert/agent-core/interaction.md)

## 专家与技能共用的规则

- [共享取数规则与默认趋势期间](contract/query.md)
- [共享报告呈现与交付规则](contract/report.md)
- [数据口径与结论依据](contract/evidence.md)
- [商家报表与成本口径](contract/seller-evidence.md)

## 专家领域 Prompt

- [竞品研究专家 · ZooData](expert/competitor-insight.md)
- [关键词研究专家 · ZooData](expert/keyword-research.md)
- [商品诊断与优化专家 · ZooData](expert/product-research.md)
- [选品与市场专家·ZooData](expert/product-selection.md)
- [消费者洞察与产品改良专家 · ZooData](expert/review-voc.md)
- [商品流量诊断专家 · ZooData](expert/traffic-diagnosis.md)

## 业务流程 Skill Prompt

- [关键词研究入口](skill/workflows/keyword-research/definition.md)、[研究方法](skill/workflows/keyword-research/methods.md)、[报告提纲](skill/workflows/keyword-research/report-outline.md)

- [选品与市场研究](skill/workflows/product-selection/definition.md)
- [类目市场研究](skill/workflows/product-selection/market-research.md)

- [竞品对比任务](skill/workflows/competitor-comparison/definition.md)
- [竞品对比方法](skill/workflows/competitor-comparison/methods.md)
- [竞品近三个月购买量](skill/workflows/competitor-comparison/monthly-purchases.md)
- [竞品对比提纲](skill/workflows/competitor-comparison/report-outline.md)

## 数据 Skill Prompt

- [相关关键词](skill/datas/keyword-expansion/definition.md)、[基础统计](skill/datas/keyword-statistics/definition.md)、[关键词市场画像](skill/datas/keyword-profile/definition.md)、[需求趋势画像](skill/datas/keyword-trend-profile/definition.md)


- [商品详情](skill/datas/product-detail/definition.md)
- [商品评价画像](skill/datas/product-review-profile/definition.md)
- [类目评价画像](skill/datas/market-review-profile/definition.md)
- [单接口评论原文](skill/datas/review-search/definition.md)
- [单接口商品月度销量](skill/datas/product-sales-trend/definition.md)

- [关键词分析](skill/datas/keyword/definition.md)
- [关键词分析方法](skill/datas/keyword/methods.md)
- [关键词指标含义](skill/datas/keyword/semantics.md)
- [类目市场分析](skill/datas/market/definition.md)
- [市场分析方法](skill/datas/market/methods.md)
- [市场指标含义](skill/datas/market/semantics.md)
- [商品分析](skill/datas/product/definition.md)
- [商品分析方法](skill/datas/product/methods.md)
- [商品指标含义](skill/datas/product/semantics.md)
- [消费者反馈分析](skill/datas/review/definition.md)
- [消费者反馈分析方法](skill/datas/review/methods.md)
- [消费者反馈指标含义](skill/datas/review/semantics.md)
- [商品流量分析](skill/datas/traffic/definition.md)
- [商品流量分析方法](skill/datas/traffic/methods.md)
- [商品流量指标含义](skill/datas/traffic/semantics.md)


## 生成入口 Prompt

- [Skill 入口](templates/skill-entry.md)
- [Expert 能力装配](templates/expert-bindings.md)

这两份保留生成模板中的变量位置。正文为对应中文指令，变量在装配时替换为实际路径、Skill 名称和允许任务。

## 报告生成 Skill

- [使用入口与生成流程](tools/report/definition.md)
- [固定结构与报告组件](tools/report/layouts.md)

报告 Skill 随各位专家装配，中文目录只供审阅，不进入运行包。页面模板和脚本由运行源码维护，不复制到中文目录。
