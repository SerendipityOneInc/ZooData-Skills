<!-- prompt-source: skill/datas/market/methods.md c31297cf2cc0a9673ae135a6de95438bff5e7d4a57bfedbf8e9e3c7587310750 -->

> 英文原文：[skill/datas/market/methods.md](../../../../skill/datas/market/methods.md)

<a id="market-analysis-methods"></a>

# 市场分析方法

1. 画像、分布和集中度接口共用选定的类目 ID、商品包含范围和样本选择。指定快照时使用已发布的业务日期；承接市场发现时，使用其返回的 `resolvedDate`。
2. 数值分布保留接口返回的桶编码、上下界和指标。来源明确采用其他边界规则时，保留该次返回的分组，不把数量移到新区间；边界包含规则尚未明确时，只报告原分组及指标，不自行添加区间括号或计算阈值累计值。

<a id="categories-category-lookup"></a>

## categories：类目检索

1. 按给定名称或路径查询类目，或用 `parentCategoryPath` 取得指定父类的直接子类；逐项读取 `categoryId`、`categoryName` 和 `categoryPath`。
2. 比较直接子类时，以返回的子类 ID 作为市场范围；匹配结果对应不同目标市场时，请用户明确要研究的类目。

<a id="marketssearch-market-discovery"></a>

## markets/search：市场发现

1. 按当前工具定义传入类目范围、商品包含规则、样本选择及明确筛选条件。不指定日期时读取最新发布快照，实际日期读取返回的 `resolvedDate`。
2. 问题指定下表取数目标时，使用工具支持的对应排序。按所需覆盖范围继续分页，保留每项类目身份及平铺的全市场和样本字段。

| 取数目的 | 排序方式 |
|---|---|
| 类目销量较高 | `totalMonthlySales desc` |
| 类目收入较高 | `totalMonthlyRevenue desc` |
| 样本商品平均收入较高 | `avgMonthlyRevenue desc` |
| 前三商品月销量份额较低 | `top3ProductMonthlySalesRate asc` |

<a id="marketsprofile-market-profile"></a>

## markets/profile：市场画像

1. 从 `marketSize` 读取全市场指标，从 `sampleProfile` 读取样本指标，提取当前问题所需的价格、评分、新品和集中度部分。

<a id="marketsprice-distributions-price-distribution"></a>

## markets/price-distributions：价格分布

1. 读取 `priceDistribution` 及其价格上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketsrating-distributions-star-rating-distribution"></a>

## markets/rating-distributions：星级分布

1. 读取 `ratingDistribution` 及其星级上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketsrating-count-distributions-rating-count-distribution"></a>

## markets/rating-count-distributions：评分数分布

1. 读取 `ratingCountDistribution` 及其评分数上下界，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketslisting-age-distributions-listing-age-distribution"></a>

## markets/listing-age-distributions：上架时长分布

1. 读取 `listingAgeDistribution` 及其上架时长区间，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketsfulfillment-distributions-fulfillment-distribution"></a>

## markets/fulfillment-distributions：配送方式分布

1. 读取 `fulfillmentDistribution` 及其配送方式标识，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketsseller-country-distributions-seller-country-distribution"></a>

## markets/seller-country-distributions：卖家国家分布

1. 读取 `sellerCountryDistribution` 及其卖家国家标识，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketscontent-distributions-content-distribution"></a>

## markets/content-distributions：内容配置分布

1. 读取 `contentDistribution` 及其返回的内容类型标识，保留各组商品数量与占比、销量和收入及其份额，以及该分布返回的样本总量。

<a id="marketstop-product-concentrations-product-concentration"></a>

## markets/top-product-concentrations：商品集中度

1. 读取 `topnMetrics` 和 `topProductList`，保留各 Top N 标识、`concentrationRate`、样本排序依据及各返回对象的销量和收入指标。

<a id="marketsbrand-concentrations-brand-concentration"></a>

## markets/brand-concentrations：品牌集中度

1. 读取 `topnMetrics` 和 `topBrandList`，保留各 Top N 标识、`concentrationRate`、样本排序依据及各返回对象的销量和收入指标。

<a id="marketsseller-concentrations-seller-concentration"></a>

## markets/seller-concentrations：卖家集中度

1. 读取 `topnMetrics` 和 `topSellerList`，保留各 Top N 标识、`concentrationRate`、样本排序依据及各返回对象的销量和收入指标。

<a id="marketslisting-launch-trend-launch-composition"></a>

## markets/listing-launch-trend：新品构成

1. 传入类目 ID、商品包含和样本规则，以及所需首次上架日期范围和月或年粒度。
2. 读取当前头部样本的 `points[].date` 和 `productCount`，保留首次上架分组及实际返回期间。

<a id="marketshistory-market-history"></a>

## markets/history：市场历史

1. 传入类目 ID、`dateFrom`、`dateTo` 及一致的商品包含和样本规则，读取各序列的类目身份和 `points`。
2. 按返回的月末日期对齐，比较 `marketSize` 或 `sampleProfile` 中的同一指标；按问题要求计算观测变化，保留各期样本选择。
