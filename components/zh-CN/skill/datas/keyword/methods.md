<!-- prompt-source: skill/datas/keyword/methods.md d228f36039ec4a144fe7d20ba27560e5178aa88e5ef7a0077c8e4e47d5a3feab -->

> 英文原文：[skill/datas/keyword/methods.md](../../../../skill/datas/keyword/methods.md)

<a id="keyword-analysis-methods"></a>

# 关键词分析方法

<a id="keywordsextends-related-term-expansion"></a>

## keywords/extends：相关词拓展

1. 传入种子词 `query` 和站点。普通相关词拓展使用 `queryType=fuzzy`，用户指定短语匹配时使用 `queryType=phrase`。
2. 按下表选择工具支持的取数顺序。用户未指定顺序时，普通相关词拓展按相关度降序。排序参数按[MCP 排序规则](../../../contract/query.md#apply-sorting-and-pagination)处理。

| 取数目的 | 排序方式 |
|---|---|
| 与种子词相关 | `relevanceScore desc` |
| 预估搜索量较高 | `estimateSearchCount desc` |
| 搜索频率排名更靠前 | `abaRank asc` |
| 按字母排列 | `keyword asc` |

3. 逐行从 `matchData.keyword` 读取候选词，从 `matchData.site` 读取站点，从 `matchData.relevanceScore` 读取相关度。从 `keywordSnapshot.estimateSearchCount` 读取预估搜索量，从 `keywordSnapshot.abaRank` 读取 ABA 排名，从 `keywordSnapshot.dataWindow.currentPeriod` 读取实际统计期间。候选词快照已提供拓词报告所需的基础指标，无需为相同指标和期间另查 `keywords/detail`。
4. 所需候选词数量或覆盖范围超出当前页时，继续分页获取。按候选词、站点和统计期间去重。
5. 按词中表达的品类、属性、用途或场景分组，以共同条件命名分组，相邻产品品类单列，各组保留已选排序。

<a id="keywordsdetail-keyword-details"></a>

## keywords/detail：关键词详情

1. 用户要求指定词的基础指标统计时，传入关键词或词集、站点和快照日期。
2. 从每项结果的 `snapshotData` 读取当前问题所需的基础指标：搜索量及 ABA 排名、Top3 点击及转化份额、商品和品牌数量、标题覆盖、自然位及广告数量，或 Top48 商品基准。保留关键词身份及响应上下文中的实际统计期间。

<a id="keywordsmarket-profile-keyword-profiles"></a>

## keywords/market-profile：关键词画像

1. 传入指定词或词集、站点和快照日期，读取每个词的 `marketProfile`。
2. 对当前问题所需的每项分级维度，读取 `level`、`interpretation` 及 `levelEvidence` 中的数值依据。搜索量和 ABA 排名已包含在 `demandScale.levelEvidence` 中。
3. 从 `adCoverage` 读取广告覆盖率，从 `annualSeasonality` 读取年度季节性分类及已返回的历史高峰信息。

<a id="keywordstrend-profile-trend-profiles"></a>

## keywords/trend-profile：趋势画像

1. 传入指定词或词集、站点、截至日期及需要的工具支持窗口 `windowPeriods`。
2. 逐个窗口读取搜索需求量及 ABA 排名的 `trend` 方向和 `trendEvidence` 变化数据。
3. 从 `volatilityLevel` 读取需求波动程度，从 `lastPeriodWindowPosition` 读取最新观测在窗口内的位置。各项结果保留对应的返回窗口。

<a id="keywordstrend-weekly-trend-data"></a>

## keywords/trend：周度趋势数据

1. 用户要求周度历史数据或逐周观测值图表时，传入指定词或词集、站点及工具支持的日期范围。
2. 读取每项结果的 `series`，保留每周起止日期、预估搜索量、ABA 排名及当前问题所需的 Top3 点击和转化份额。
