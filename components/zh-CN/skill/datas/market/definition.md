<!-- prompt-source: skill/datas/market/definition.md ac07236729f71343c39a5063792469b977826f5a6493df4c3f30815580ed80c3 -->

> 英文原文：[skill/datas/market/definition.md](../../../../skill/datas/market/definition.md)

<a id="category-market-analysis"></a>

# 类目市场分析

1. 本 Skill 以类目市场为对象，提供细分类目筛选、市场规模、价格与评分分布、竞争格局、商品上架时间和历史变化分析。

<a id="identify-required-inputs"></a>

## 确认分析所需输入

1. 使用类目 ID 或明确的发现范围、站点、快照或日期范围、商品包含范围、样本选择及筛选条件。
2. 根据名称或路径确定类目时，使用[类目检索方法](methods.md#categories-category-lookup)。

<a id="select-an-analysis-task"></a>

## 选择分析任务

| 任务标识 | 必要输入 | 标准报告内容 | 对应方法 |
|---|---|---|---|
| Market discovery（市场发现） | 类目范围、站点及明确条件 | 类目清单、市场规模、样本指标和条件匹配结果 | [对应方法](methods.md#marketssearch-market-discovery) |
| Market profile（市场画像） | 类目 ID、站点及快照选择 | 全市场规模及头部样本的价格、评分、集中度和新品指标 | [对应方法](methods.md#marketsprofile-market-profile) |
| Market price distribution（价格分布） | 类目 ID、快照及样本选择 | 按价格上下界划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketsprice-distributions-price-distribution) |
| Market rating distribution（星级分布） | 类目 ID、快照及样本选择 | 按星级上下界划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketsrating-distributions-star-rating-distribution) |
| Market rating-count distribution（评分数分布） | 类目 ID、快照及样本选择 | 按评分数上下界划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketsrating-count-distributions-rating-count-distribution) |
| Market listing-age distribution（上架时长分布） | 类目 ID、快照及样本选择 | 按上架时长区间划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketslisting-age-distributions-listing-age-distribution) |
| Market fulfillment distribution（配送方式分布） | 类目 ID、快照及样本选择 | 按配送方式标识划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketsfulfillment-distributions-fulfillment-distribution) |
| Market seller-country distribution（卖家国家分布） | 类目 ID、快照及样本选择 | 按卖家国家标识划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketsseller-country-distributions-seller-country-distribution) |
| Market content distribution（内容配置分布） | 类目 ID、快照及样本选择 | 按返回的内容类型标识划分的样本数量、占比和销售指标 | [对应方法](methods.md#marketscontent-distributions-content-distribution) |
| Market product concentration（商品集中度） | 类目 ID、快照及样本选择 | Top N 集中度及返回的头部对象数据 | [对应方法](methods.md#marketstop-product-concentrations-product-concentration) |
| Market brand concentration（品牌集中度） | 类目 ID、快照及样本选择 | Top N 集中度及返回的头部对象数据 | [对应方法](methods.md#marketsbrand-concentrations-brand-concentration) |
| Market seller concentration（卖家集中度） | 类目 ID、快照及样本选择 | Top N 集中度及返回的头部对象数据 | [对应方法](methods.md#marketsseller-concentrations-seller-concentration) |
| Launch composition（新品构成） | 类目 ID、样本及首次上架日期范围 | 当前样本按首次上架月或年的商品数量 | [对应方法](methods.md#marketslisting-launch-trend-launch-composition) |
| Market trend（市场历史） | 类目 ID、日期范围及商品包含和样本规则 | 月末市场总量、样本均值及可比变化 | [对应方法](methods.md#marketshistory-market-history) |

<a id="preserve-object-features-and-report-findings"></a>

## 保留对象特征并交付报告

1. 保留类目 ID、名称、路径、站点、实际期间、商品包含范围和样本选择，以及已有的市场商品数、月销量和月收入。
2. 市场发现交付所需类目清单和明确条件的匹配结果；市场画像交付问题所需的全市场和样本指标。
3. 分布及集中度报告保留所需分组、数量、指标及其统计总体；历史与新品构成报告保留返回日期及比较范围。
