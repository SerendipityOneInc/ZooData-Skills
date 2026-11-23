<!-- prompt-source: skill/datas/traffic/methods.md 11b4108208b324154e8f1a98f0b0b8f1cc45f97367bda9605b2f510b98be03db -->

> 英文原文：[skill/datas/traffic/methods.md](../../../../skill/datas/traffic/methods.md)

<a id="product-traffic-analysis-methods"></a>

# 商品流量分析方法

<a id="keywordsproduct-traffic-structure-profile-traffic-structure-profile"></a>

## keywords/product-traffic-structure-profile：流量结构画像

1. 传入 ASIN 集合、站点和快照日期，读取各对象身份、`productTrafficTermsProfile` 及本期和上期范围。
2. 按返回内容读取 `summary`、`trafficStructureChange`、`organicStructureChange` 和 `termChangeDrivers`，保留渠道标识及已有流量词记录的实际字段。

<a id="keywordsproduct-traffic-trend-profile-traffic-trend-profile"></a>

## keywords/product-traffic-trend-profile：流量趋势画像

1. 传入 ASIN、站点、日期及支持窗口，按问题需要选择工具支持的返回详略程度。
2. 读取各窗口记录的状态，再读取 `trafficTrendProfile` 中可用部分；逐项读取已返回的 `trend`、`trendEvidence`、`volatilityLevel` 和 `lastPeriodWindowPosition`。

<a id="keywordsproduct-traffic-trend-weekly-traffic-data"></a>

## keywords/product-traffic-trend：流量周度数据

1. 传入 ASIN、站点及工具支持的 `dateFrom`、`dateTo` 范围，读取各对象状态和 `series`。
2. 保留每周边界、整体和自然及广告曝光点、词数，以及返回的位置和需求排名分布，按所需周次比较相同指标。

<a id="keywordsproduct-traffic-terms-traffic-contributors"></a>

## keywords/product-traffic-terms：流量词

1. 传入 ASIN、站点、快照及明确的位置类型和关键词筛选，按所需取数顺序使用下表中工具支持的排序。
2. 逐行读取搜索词、`trafficShare`、`estimateImpressionPoint`、位置、位置类型、搜索量和 ABA 排名及观测覆盖，按所需范围继续分页。

| 取数目的 | 排序方式 |
|---|---|
| 曝光贡献较高 | `trafficShare desc` 或 `estimateImpressionPoint desc` |
| 同一位置类型内观测位置更靠前 | `avgPosition asc` 或 `absolutePosition asc` |
| 搜索词需求量较高 | `keywordEstimateSearchCount desc` |

<a id="keywordsproduct-traffic-terms-trend-named-term-weekly-data"></a>

## keywords/product-traffic-terms-trend：指定词周度数据

1. 传入单个 ASIN、指定词集、站点及支持日期范围，读取各词的周度 `series`。
2. 逐期读取 `totalEstimateImpressionPoint`、`trafficByExploreType`、`keywordEstimateSearchCount` 和 `keywordAbaRank`。各位置类型只比较自身的曝光和位置，`absolutePosition` 与 `avgPosition` 分别比较。仅在问题需要时读取 `asinSnapshot` 和对应位置类型的 `adActivity`。
3. 按返回的期间边界，对齐曝光、位置，以及搜索量或 ABA 排名。已有关键词序列直接复用，搜索量和 ABA 排名具备一项即可。两项都不能提供本次对比所需的关键词背景时，在查询限制内通过[关键词周度背景](#keywordstrend-weekly-query-context)补充缺少的期间。

<a id="keywordssearch-results-search-placement-records"></a>

## keywords/search-results：搜索展示位置记录

1. 传入搜索词、站点、快照及所需位置类型；查看位置时使用工具支持的 `absolutePosition asc`，查看曝光时使用 `estimateImpressionPoint desc`。
2. 保留 ASIN、可读商品名称、`exploreType`、`absolutePosition` 和 `estimateImpressionPoint`，在相同搜索词、期间及位置类型内比较选定商品，明确取得的记录范围。
3. 每个搜索词及期间的 `keywordTotalEstimateImpressionPoint` 读取一次。用户要求样本内曝光份额时，将指定分组的记录曝光点求和，再除以同一样本全部记录的曝光点之和。

<a id="keywordsdetail-query-snapshot-context"></a>

## keywords/detail：关键词同期统计

1. 所需流量对比涉及响应中未提供的关键词同期统计时，按相符站点和日期读取指定词的 `snapshotData`，保留词身份及其统计期间。

<a id="keywordsmarket-profile-query-profile-context"></a>

## keywords/market-profile：关键词画像背景

1. 问题要求对照关键词需求或竞争时，读取指定词的 `marketProfile` 及所需维度的 `level`、`interpretation` 和 `levelEvidence`，保留关键词快照范围。

<a id="keywordstrend-profile-query-trend-context"></a>

## keywords/trend-profile：关键词趋势背景

1. 问题要求对照 ASIN 曝光与搜索需求方向时，读取指定词在所需窗口的 `trend` 和 `trendEvidence`，分别保留流量和关键词窗口。

<a id="keywordstrend-weekly-query-context"></a>

## keywords/trend：关键词周度背景

1. 尚无所需关键词周度数据时，按相符站点和支持日期范围读取指定词的 `series`，提取搜索量或 ABA 排名，按返回的期间边界与 ASIN 在该词下的曝光和位置对齐。

<a id="realtimeproduct-product-observation-context"></a>

## realtime/product：商品观测背景

1. 所需流量对比缺少当前商品信息时，读取目标 ASIN 实际返回的属性或报价字段，分别保留当前商品观测日期与历史流量窗口。

<a id="local-analysis-seller-search-performance"></a>

## Local analysis：商家搜索词表现

1. 在本地处理用户提供的搜索表现文件，确认站点、期间、品牌或 ASIN 视图及记录维度。将原始列对应到该视图的搜索词及已有展示、点击、加购、购买和份额。
2. 按[商家报表规范](../../../contract/seller-evidence.md)，使用口径相符的数量和分母计算所需比率及差异；仅在相应报表已提供时比较期间。
3. 交付所需词级指标、变化及明确条件匹配结果，并保留对应行标识。实际表现只使用商家报表，未提供的字段保持暂无数据，不用公开估计值补齐。

<a id="local-analysis-seller-advertising-performance"></a>

## Local analysis：商家广告表现

1. 在本地处理用户提供的广告文件，确认站点、期间、归因窗口、商品归属及记录维度；保留记录描述的是买家搜索词还是广告投放对象。
2. 提取已有展示、点击、花费、归因订单和归因销售额，按[商家报表规范](../../../contract/seller-evidence.md)计算所需 CPC、CVR、ACOS 或 ROAS；输入不足的结果保持不可计算。
3. 交付所需逐行或分组指标及可比变化。保留广告活动、广告组标识和商品归属，不将报表整体结果归给报表未明确关联的 ASIN。
