<!-- prompt-source: skill/datas/product/semantics.md 46389d6c22d469e8374abc5699b6e773b5df97c390b70bf83f648462655ddd57 -->

> 英文原文：[skill/datas/product/semantics.md](../../../../skill/datas/product/semantics.md)

<a id="product-metric-meanings"></a>

# 商品指标含义

<a id="product-identity-and-commerce-measures"></a>

## 商品身份与经营指标

| 指标 | 含义 |
|---|---|
| ASIN 与父 ASIN | 商品或变体标识，以及归并其变体的父体标识。 |
| `monthlySalesFloor` | 选定目录快照沿用页面“N+ bought in past month”观测的月购买量下限档位。 |
| `monthlyRevenueFloor` | 接口独立返回的月收入下限。 |
| 价格 | 指定目录快照或实时报价中的价格，含其来源和币种。 |
| 星级与评分数 | 星级分值及累积评分数量。 |
| BSR 与子类 BSR | 商品在指定排名类目中的名次，数值越小越靠前。 |
| 上架日期与变体数 | 返回商品范围内记录的上架日期和变体数量。 |
| New Release 标签 | 长期保留、不会过期的历史标记，只说明商品曾有 New Release 标识，不代表当前仍是新品；上架时长由上架日期确定。 |

<a id="history-and-page-content"></a>

## 历史与页面内容

| 指标 | 含义 |
|---|---|
| 历史观测 | 按返回时间戳对齐的历史页面指标，某个时点可能沿用此前观测值。 |
| 历史购买量档位 | 历史观测中记录的页面月购买量下限文字。 |
| 月度目录销量营收点 | ASIN及父体在月末目录快照中的购买量、营收下限，或另行标注的当月快照值。与目录数据同口径，不是页面观测历史口径。 |
| 完整月与当月 | `monthEnd` 为完整月，`monthToDate` 为持续更新的当月。返回的完整月增长率不适用于后者。 |
| 月度目录可用状态 | `inCatalog=false` 表示该月无商品目录记录；`inCatalog=true` 但指标为空表示商品存在、指标未取得。两者都不是测得的零。 |
| 变更记录 | 标题、图片或状态字段发生变化时记录的带日期数值。 |
| 返回的商品文本 | 已取得标题、五点、描述或规格中明确描述的商品信息。 |
| 五点描述 | 商品的完整卖点描述。返回特征文本中夹带的独立规格值属于属性信息，不额外计为卖点描述。 |
| 页面中的短语出现情况 | 指定完整短语是否出现在已取得的某个页面区域，只描述该区域的文字；搜索可见性由 ASIN 与搜索词对应的曝光和位置观测说明。 |
| 图片 URL 与已查看图片 | 分别表示图片资源引用和实际查看到的图像内容。 |
| A+ 状态 | 返回标记记录的 A+ 可用状态，正文属于另行取得的内容。 |

<a id="sample-price-bands-and-brands"></a>

## 样本价格带与品牌

| 指标 | 含义 |
|---|---|
| 样本总体 | 由请求关键词和接口采样规则选取的商品样本。 |
| 价格带边界与 `sampleMedianPrice` | 价格分组的上下界，以及返回样本的价格中位数。 |
| `sampleSalesRate` | 该价格带或品牌在返回样本中的销量份额。 |
| `sampleTop3BrandSalesRate` 与 `sampleTop10BrandSalesRate` | 分别为指定价格带或整体样本中，所指头部品牌的销量份额。 |
| `sampleOpportunityIndex` | 接口模型返回的价格带比较综合指数。 |
| `sampleProducts` | 接口为某品牌返回的示例商品记录。 |
