<!-- prompt-source: skill/datas/traffic/definition.md 3cd0c5d0427c2ba835483137e792304e15ef60e763451b68f2267bd934da8613 -->

> 英文原文：[skill/datas/traffic/definition.md](../../../../skill/datas/traffic/definition.md)

<a id="product-traffic-analysis"></a>

# 商品流量分析

1. 本 Skill 以 ASIN 的曝光和流量词为对象，分析自然与广告曝光来源、曝光趋势、每周变化、各搜索词带来的曝光及商品搜索位置；对用户提供的搜索和广告报表分析实际表现。

<a id="identify-required-inputs"></a>

## 确认分析所需输入

1. 使用 ASIN、站点及所需快照、窗口或日期范围；指定词分析还需明确词集。
2. 当前流量对比需要补充数据时，对应方法为[关键词同期统计](methods.md#keywordsdetail-query-snapshot-context)、[关键词画像](methods.md#keywordsmarket-profile-query-profile-context)、[关键词趋势画像](methods.md#keywordstrend-profile-query-trend-context)、[关键词周度数据](methods.md#keywordstrend-weekly-query-context)和[商品观测](methods.md#realtimeproduct-product-observation-context)。
3. 商家表现分析使用用户提供的报表、明确的商品或报表视图、站点和期间；广告报表还需保留归因窗口。指标按[商家报表规范](../../../contract/seller-evidence.md)解释。

<a id="select-an-analysis-task"></a>

## 选择分析任务

| 任务标识 | 必要输入 | 标准报告内容 | 对应方法 |
|---|---|---|---|
| Traffic structure（流量结构画像） | ASIN 或可比商品集合及快照日期 | 本期与上期的曝光、带来曝光的词数、渠道变化，以及曝光增加或减少对应的搜索词 | [对应方法](methods.md#keywordsproduct-traffic-structure-profile-traffic-structure-profile) |
| Traffic trend profile（流量趋势画像） | ASIN 集合、截至日期及支持窗口 | 整体、自然、广告曝光和词覆盖的趋势分类及支撑指标 | [对应方法](methods.md#keywordsproduct-traffic-trend-profile-traffic-trend-profile) |
| Traffic weekly history（流量周度数据） | ASIN 集合及日期范围 | 逐周曝光、词数及返回的分布数据 | [对应方法](methods.md#keywordsproduct-traffic-trend-weekly-traffic-data) |
| Traffic contributors（流量词） | ASIN、快照及明确列表筛选和排序要求 | 搜索词、曝光点和份额、位置、位置类型及关键词基础指标 | [对应方法](methods.md#keywordsproduct-traffic-terms-traffic-contributors) |
| Named-term movement（指定词周度变化） | ASIN、指定词及日期范围 | 同期的 ASIN 曝光、搜索位置，以及该词的搜索量或 ABA 排名；按需补充商品和广告观测 | [对应方法](methods.md#keywordsproduct-traffic-terms-trend-named-term-weekly-data) |
| Search-placement comparison（搜索展示位置对比） | 搜索词、快照及目标 ASIN 或对比范围 | 指定范围内观测到的 ASIN、位置类型、绝对位置和预估曝光 | [对应方法](methods.md#keywordssearch-results-search-placement-records) |
| Seller search performance（商家搜索词表现） | 用户提供的搜索表现报表、明确商品或报表视图、站点及期间 | 搜索词的展示、点击、加购、购买、已有份额或比率及所需期间对比 | [对应方法](methods.md#local-analysis-seller-search-performance) |
| Seller advertising performance（商家广告表现） | 用户提供的广告报表、明确商品或报表视图、站点、期间及归因窗口 | 搜索词或投放对象、展示、点击、花费、归因订单和销售额，以及所需效率指标或对比 | [对应方法](methods.md#local-analysis-seller-advertising-performance) |

<a id="preserve-object-features-and-report-findings"></a>

## 保留对象特征并交付报告

1. 保留 ASIN、站点和实际期间；词级记录保留搜索词原文、位置类型、位置、曝光贡献及已有搜索量和 ABA 排名。
2. 结构与趋势画像报告交付选定的返回维度及支撑数值；周度数据报告交付所需观测及可比变化。
3. 报告某个 ASIN 在指定词下的变化时，将三项指标按相同期间一起展示：该商品在这个词下的曝光、搜索位置，以及该词的搜索量或 ABA 排名。明确位置类型。某项仍未取得时，在对比旁说明缺项，只对已有指标作出判断。
4. 补充的关键词和商品指标保留各自的来源期间；对应字段含义见[关键词指标](../keyword/semantics.md)和[商品指标](../product/semantics.md)。
5. 商家报表保留原始行标识、报表视图、商品归属和期间；实际经营数量与公开预估曝光分别呈现，未提供的指标保持暂无数据。
