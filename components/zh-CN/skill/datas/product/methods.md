<!-- prompt-source: skill/datas/product/methods.md 1a7ebaf819fe8772cf0537b9a84b29bf381cba434e975623f0fc4aa7dc1d4a34 -->

> 英文原文：[skill/datas/product/methods.md](../../../../skill/datas/product/methods.md)

<a id="product-analysis-methods"></a>

# 商品分析方法

<a id="categories-category-lookup"></a>

## categories：类目检索

1. 按给定类目名称或路径取得对应 ID 和路径；匹配项对应不同目标类目时，请用户明确范围。

<a id="productssearch-product-discovery"></a>

## products/search：商品筛选

1. 传入已确认的商品关键词、类目和明确筛选条件。用户确认全部类目时，不传类目筛选条件。使用工具支持的快照选择，保留返回的商品和类目身份。
2. 将用户指定的条件映射到工具支持的筛选字段。有关键词时才传匹配方式，百分比按接口要求换算成小数。
3. 查询前确认冲突的上下界。条件不受支持时向用户说明，并在放宽条件前取得同意。
4. 按所需取数目的从下表选择工具支持的排序，按要求分页并按 ASIN 去重。

5. 将响应中的匹配商品总数与已取得记录数分开保留。按统一类目层级和 ID 对已取得商品分组。全部结果的精确类目数量和排名需要同口径类目汇总或完整匹配商品数据；本查询工具不直接提供类目汇总。否则交付样本类目数量和样本排名，不替换成无关市场总数，也不发起没有范围上限的全量查询。
6. 查询类目内领先商品时，保留原筛选条件和已确认的排序方式，使用该类目的 ID/路径，遵守已约定的范围及费用。相同数值保留并列；已取得记录内按 ASIN 保持稳定顺序仅用于展示，不代表经营表现更好。

| 取数目的 | 排序方式 |
|---|---|
| 购买量下限较高 | `monthlySalesFloor desc` |
| 收入下限较高 | `monthlyRevenueFloor desc` |
| 销量增长较快 | `salesGrowthRate desc` |
| 上架时间较新 | `listingDate desc` |
| 价格较低 | `price asc` |
| 评分数较少 | `ratingCount asc` |
| 同一类目内排名更靠前 | `bsr asc` |

<a id="productscompetitors-competitor-discovery"></a>

## products/competitors：竞品查找

1. 按本工具的输入定义传入指定 ASIN、品牌、卖家或商品和类目范围。
2. 分页读取匹配行，保留ASIN、商品信息及返回的表现指标，使用用户所需且工具支持的排序，并保留查询范围。保留实际返回的ASIN；只返回输入ASIN的查询，不证明已取得其他竞品或执行了自动相似商品搜索。

<a id="realtimeproduct-real-time-product-details"></a>

## realtime/product：实时商品详情

1. 按需查询目标 ASIN 和站点，从实际返回的当前报价、属性、变体及页面文字中提取所需内容。
2. 保留已取得的目录资料。实时查询失败时按 MCP 失败处理规则结束或重试，交付已有结果并标明仍缺少的部分。

<a id="productsdetail-product-details"></a>

## products/detail：商品详情

1. 优先使用已有兼容商品资料。按当前MCP Schema选择 `asins` 或 `parentAsin`，两者互斥。ASIN列表模式最多50个规范ASIN，按请求顺序返回，不接受分页、筛选和排序；父体模式按接口规定的分页和顺序读取该父体成员。
2. 用 `dateRange` 选择所需目录期间，保留返回的上下文、商品标识、单项状态及实际快照日期（如有）。请求ASIN对应的空结果仍保留，不删除或替换。
3. 提取实际返回的商品属性、页面内容、价格、购买量和营收下限、评分、卖家及变体指标。子体与父体分开记录。

<a id="productshistory-product-history"></a>

## products/history：商品历史

1. 传入单个 ASIN、`startDate`、`endDate` 和站点，只需部分序列时按工具支持情况使用 `aspects`。
2. 将价格、BSR、购买量下限和评分等逐点数组与 `timestamps` 对齐；标题、图片和状态的带日期变化按事件记录读取。
3. 跨观测日期比较相同来源指标、排名类目及父子体范围，保留返回的观测覆盖。

<a id="productssales-trend-monthly-sales-and-revenue"></a>

## products/sales-trend：月度销量营收

1. 传入单个规范ASIN；用户指定月份时，在当前工具支持的范围内传入 `startMonth` 和 `endMonth`。读取目录快照口径下子体及父体的月购买量、月营收下限，以及返回的增长指标。
2. 保留各月的 `pointKind` 和 `inCatalog`。完整月 `monthEnd` 之间相互比较；`monthToDate` 单独标为当月数据，不作为完整月或完整月增长率。
3. 当月没有目录记录与已有目录记录但指标为空是不同状态，分别保留，不补零。使用返回的相邻月增长率；前期基数不满足条件时，保留接口返回的空值。

<a id="productsprice-band-overview-price-band-overview"></a>

## products/price-band-overview：价格带概览

1. 传入限定所需商品样本的关键词，读取 `sampleMedianPrice` 及返回的 `hottestBand`、`bestOpportunityBand` 概览。
2. 对每个返回价格带，保留价格上下界、商品数、销量份额和返回指数。

<a id="productsprice-band-detail-price-band-statistics"></a>

## products/price-band-detail：价格带统计

1. 传入样本关键词，读取 `priceBands`、`sampleSkuCount` 和 `sampleTotalMonthlySales`。
2. 按价格分组报告上下界、商品和品牌数、销量份额及返回的均值和指数。

<a id="productsbrand-overview-brand-overview"></a>

## products/brand-overview：品牌概览

1. 传入样本关键词，读取 `sampleBrandCount`、`sampleTop10BrandSalesRate`、`sampleTop10AvgRating` 和 `sampleTop10AvgPrice`。

<a id="productsbrand-detail-brand-statistics"></a>

## products/brand-detail：品牌统计

1. 传入样本关键词，读取 `brands` 及响应中的样本商品、销量和品牌总量。
2. 保留各品牌名称、商品数、销量和收入、份额、价格和评分指标及返回的 `sampleProducts`。

<a id="local-analysis-product-facts"></a>

## Local analysis：商品信息

1. 先复用已有资料。需查询已知美国站 ASIN 时，先查[商品详情](#productsdetail-product-details)。取得商品记录即使用返回结果。
2. 查询当前商品时，仅对目录服务请求失败或未找到的 ASIN 使用[实时商品详情](#realtimeproduct-real-time-product-details)。历史期间及父体变体清单使用目录来源。

<a id="local-analysis-product-content"></a>

## Local analysis：商品内容整理

1. 对照用户所问的页面部分，按[商品信息方法](#local-analysis-product-facts)取得或复用原文，再按页面部分整理。
2. 整理已取得的标题、五点、描述、规格及实际查看的图片。保留原有品牌、材质、尺寸、套装内容和兼容信息，以及商品身份和来源部分。
3. 先区分返回文本的含义，再编五点描述的序号。条目仅重复已知规格值时，将其归入对应属性。完整卖点描述按原顺序编号，保留原文及其来源位置，不将返回数组长度当作五点描述条数。
4. 缺少五点原文时，将五点描述标为“未获取”。标题和页面标记只作为各自部分的证据。其他缺失部分同样单独标明，继续交付已取得的内容。
5. 当前分析需要将明确的短语与页面文字比较时，分别保留每个短语、所检查的页面区域及支持结果的原文。按[短语出现情况的含义](semantics.md#history-and-page-content)解释结果，与已提供的流量观测分开保留。

<a id="local-analysis-product-comparison"></a>

## Local analysis：商品比较

1. 对每个商品按[商品信息方法](#local-analysis-product-facts)取得所需属性、报价与目录指标。月度销量和营收使用[月度趋势](#productssales-trend-monthly-sales-and-revenue)，页面随时间的变化使用[商品历史](#productshistory-product-history)，页面各部分使用[商品内容](#local-analysis-product-content)。只执行当前会话允许的任务。
2. 按相同指标定义和统计范围，比较已取得的规格、价格、评分、表现指标或页面部分。对明确可测条件，报告满足、不满足或暂无数据及所用值；每项差异保留 ASIN 或用户产品身份。
3. 某商品的必要数值无法取得时，将该项标为暂无数据，交付已有数据支持的比较，不作出依赖缺失值的差异或条件匹配判断。
