<!-- prompt-source: skill/workflows/product-selection/definition.md 21d0886e09c83df5ac571feb96f875b52298af802282faeb831640d025e5f5db -->

> 英文原文：[原文](../../../../skill/workflows/product-selection/definition.md)

# 选品与市场研究·ZooData

## 选择数据来源

1. 卖家提供的数字或文件足以回答时，直接在本次会话分析并注明来源，跳过连接配置。卖家限定只用所给资料时，仅报告资料能支持的结果。
2. 新的亚马逊美国站数据由已配置的 ZooData 连接器查询，付费查询使用 API Key 对应账户的积分。成本和供应商报价仅用于会话内分析。

## 调用所选数据工具

查询指定类目的下级类目，先用 `openapi_v2_categories`。其他任务使用相应数据方法列出的业务工具（服务名 `{{mcp_server}}`）。工具需要按名加载时，将完整业务工具名传给 `ToolSearch.tool_names`，找到后按数据方法传参调用。开场的连接器列表未列出 ZooData，不能据此判断连接失败。按[共享取数规则](../../../contract/query.md)处理实际查找或调用结果。

## 按用户问题选择任务

按用户要比较的对象选择路径。选商品时，全部类目和经营条件共同限定一个筛选范围。选类目时，先读[类目市场研究方法](market-research.md)，用市场数据批量比较目标类目。统计上榜新品数用 `openapi_v2_markets_listing_launch_trend`；需要榜内商品示例时用 `openapi_v2_markets_top_product_concentrations`，沿用方法规定的榜单日期和上架窗口。若要逐个深入研究，先筛出市场，再一次研究一个选定类目。

| 用户想做什么 | 分析入口 | 交付 |
|---|---|---|
| 目标还不清楚 | 请用户用自己的话说明想解决的选品问题 | 只问一个能确定分析方向的问题。用户询问如何提问时，可举一个相关示例。 |
| 研究或比较类目需求、价格、竞争、买家诉求或进入条件 | [类目市场研究](market-research.md) | 按问题交付市场发现，按需列举代表商品。 |
| 比较各类目上榜新品的数量 | [类目市场研究](market-research.md) | 用 `market-research` 展示数量和排名。 |
| 除类目比较外，还想了解上榜新品的成长走势 | [上榜新品的成长表现](market-research.md) | 用 `new-launches` 展示类目排名及已识别新品中月销量前三款的走势。 |
| 查找飙升市场 | [比较增长市场](market-research.md) | 按类目整体销量增幅比较同层级市场，用户需要时再展示代表商品。 |
| 按用户条件找商品，包括按购买量查找爆款 | [筛选候选](screening.md) | 按已确认的条件和一种排序列出候选。 |
| 评估指定候选：商品是怎样成长的，哪些指标达到我给的门槛？ | [评估候选](methods.md) | 一份候选成长报告。可综合评估，也可聚焦销量等指定指标。 |

复用已有资料，遵循[取数规则](../../../contract/query.md)、[证据规则](../../../contract/evidence.md)及涉及私有数据时的[商家资料规则](../../../contract/seller-evidence.md)。研究任务采用[对应的报告提纲](report-outline.md)。独立使用时按[生成指南](../../../tools/report/definition.md)生成 HTML；由专家使用时交给专家一次成稿。按[报告交付规则](../../../contract/report.md)展示文件，用户指定其他格式时按其要求交付。
