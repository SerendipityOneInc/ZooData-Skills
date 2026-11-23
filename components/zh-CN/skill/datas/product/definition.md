<!-- prompt-source: skill/datas/product/definition.md 17717d68c1fa82cbeab40c5d4be4e0e8bac2c576c3888ed5af8b392dda76dbcd -->

> 英文原文：[skill/datas/product/definition.md](../../../../skill/datas/product/definition.md)

<a id="product-analysis"></a>

# 商品分析

1. 本 Skill 以商品或候选集合为对象，提供商品筛选、竞品查找、商品信息、页面内容、月度销量营收、历史变化、商品比较及相关商品的价格分布和品牌统计。

<a id="identify-required-inputs"></a>

## 确认分析所需输入

1. 使用 ASIN 或用户产品资料、站点、所需日期及比较条件。商品筛选使用用户的筛选条件。线上查询候选前，需要确认类目范围：指定类目或全部类目。保留用户提供的商品关键词。
2. 依赖类目的问题使用[类目检索](methods.md#categories-category-lookup)确定范围；价格带和品牌统计使用对应工具支持的关键词输入。

<a id="select-an-analysis-task"></a>

## 选择分析任务

| 任务标识 | 必要输入 | 标准报告内容 | 对应方法 |
|---|---|---|---|
| Product discovery（商品筛选） | 用户的筛选条件、站点，以及已确认的筛选范围 | 实际查询条件、候选 ASIN、基础指标及条件匹配结果 | [对应方法](methods.md#productssearch-product-discovery) |
| Competitor discovery（竞品查找） | 当前查询Schema支持的商品关键词、品牌、卖家、类目或ASIN | 按这些条件实际返回的ASIN及商品指标 | [对应方法](methods.md#productscompetitors-competitor-discovery) |
| Product facts（商品信息） | 已知ASIN列表、父ASIN或明确的用户商品资料 | 所需目录属性及购买量、营收指标，或当前页面属性及报价，保留实际商品范围 | [对应方法](methods.md#local-analysis-product-facts) |
| Product content（商品内容） | ASIN、已有页面或产品资料 | 已取得的标题、五点描述、商品描述、规格、实际查看的图片内容，以及用户所需的分区域短语出现情况 | [对应方法](methods.md#local-analysis-product-content) |
| Product history（商品历史） | ASIN 及日期范围 | 价格、类目排名、购买量下限、评分及变更记录 | [对应方法](methods.md#productshistory-product-history) |
| Product sales trend（月度销量营收） | 单个ASIN及所需月份 | 月度子体及父体购买量、营收下限，完整月或当月状态，以及接口返回的环比变化 | [对应方法](methods.md#productssales-trend-monthly-sales-and-revenue) |
| Product comparison（商品比较） | 明确商品集合及比较维度或条件 | 可比商品信息和内容、差异及明确条件匹配结果 | [对应方法](methods.md#local-analysis-product-comparison) |
| Price-band overview（价格带概览） | 限定商品样本的关键词 | 样本价格中位数及返回的概览价格带 | [对应方法](methods.md#productsprice-band-overview-price-band-overview) |
| Price-band statistics（价格带统计） | 限定商品样本的关键词 | 价格分组、商品及品牌数、销量份额和返回的分组指标 | [对应方法](methods.md#productsprice-band-detail-price-band-statistics) |
| Brand overview（品牌概览） | 限定商品样本的关键词 | 样本品牌数、前十品牌销量集中度及价格和星级均值 | [对应方法](methods.md#productsbrand-overview-brand-overview) |
| Brand statistics（品牌统计） | 限定商品样本的关键词 | 各品牌样本数量、销量和收入、份额、价格和评分指标及返回的示例商品 | [对应方法](methods.md#productsbrand-detail-brand-statistics) |

<a id="preserve-object-features-and-report-findings"></a>

## 保留对象特征并交付报告

1. 保留已有的 ASIN、名称和品牌、站点、相关规格、价格、月购买量下限、星级及评分数，涉及变体时保留父子体身份。
2. 筛选与比较报告交付所需商品、指标及明确条件匹配结果；内容报告保留已取得部分和商品信息。
3. 历史报告交付所需序列及可比变化；价格带和品牌报告保留关键词限定的样本、分组及返回分母。
