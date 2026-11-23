<!-- prompt-source: skill/datas/traffic/semantics.md 6e01d4987fd4f4fd86551c0d403e8e2082f544ad2f693a49344e68eccf64b94e -->

> 英文原文：[skill/datas/traffic/semantics.md](../../../../skill/datas/traffic/semantics.md)

<a id="product-traffic-metric-meanings"></a>

# 商品流量指标含义

<a id="exposure-and-placement"></a>

## 曝光与位置

| 指标 | 含义 |
|---|---|
| 预估曝光分值（`estimateImpressionPoint`） | 指定 ASIN、词或位置类型在返回期间内的估计曝光分值。 |
| `trafficShare` | 流量词列表中，表示该行曝光占对应 ASIN 同期曝光的份额；指定词周度数据中，`trafficByExploreType.<type>.trafficShare` 表示该位置类型曝光占此 ASIN 在该词下同期曝光的份额。 |
| `asinTrafficShare` | 指定词周度数据中，该 ASIN 在此词下的曝光除以该 ASIN 同期全部关键词曝光。 |
| `exploreType` | 展示类型，`ORG` 表示自然结果，广告类型沿用返回标识。 |
| 绝对位置与平均位置 | 指定 ASIN 在某个搜索词及位置类型下的位置。`absolutePosition` 为期间内最后一次有效位置观测，`avgPosition` 为该期间有效位置观测的平均值，数值越小越靠前。这些观测衡量 ASIN 与搜索词对应的展示位置，不衡量商品标题中的某个词或片段。 |
| 观测次数与覆盖天数 | 支持某项指标的实际观测次数及覆盖天数。 |
| 空位置 | 该字段未返回数值位置，结合[位置数据可用性](#position-availability)解释对应的覆盖信息。 |
| 搜索词总曝光点 | 在结果行重复出现的搜索词期间曝光点总量，属于关键词级数值。 |

<a id="position-availability"></a>

## 位置数据可用性

在相同 ASIN、搜索词、期间和位置类型内，分别读取 `absolutePosition` 与 `avgPosition`。只使用该接口实际提供的字段；某个字段为空，不影响另一个字段已返回的数值。

| 返回条件 | 可以作出的解释 |
|---|---|
| 位置为空，且流量词列表行的 `observationCount=0` | 该行没有返回有效位置观测，位置未知。 |
| 位置为空，且流量词列表行的 `observationCount>0` | 该行有有效位置观测，但这个位置字段未提供数值；保留观测数，该位置保持未知。 |
| 位置为空，`observationCount` 未提供，且 `daysCoverageRate=0` | 该位置类型在本期间未记录观测天数，位置未知。 |
| 位置为空，`observationCount` 未提供，且 `daysCoverageRate>0` | 已记录观测天数，但这个位置字段未提供数值，位置未知。 |
| 周期已返回，但 `trafficByExploreType` 中缺少该位置类型的标识 | 该位置类型没有返回记录，位置和曝光未知。 |
| 对象状态为 `status=empty` 且 `emptyReason=asin_keyword_not_found`，或 `series` 缺少所需周期 | 所查范围或期间未返回匹配的 ASIN 与搜索词记录，位置未知。 |
| 位置为空，且相应覆盖字段为空、缺失或不足以说明原因 | 响应未明确位置缺失的原因，位置及原因均保留未知。 |

不只凭位置缺失或覆盖信息推断排名流失、曝光为 0；已经返回的曝光值照实保留。`resolvedDateFrom`、`resolvedDateTo` 或 `resolvedDate` 为空，也不能单独证明数据源未观测该期间。

<a id="structure-and-weekly-measures"></a>

## 结构与周度指标

| 指标 | 含义 |
|---|---|
| 结构画像 | 返回 ASIN 的本期与上期周度聚合及渠道构成。 |
| 上期空值与零 | 上期数量、份额或曝光为空，表示上期数据不可用；数值零表示可用期间内该指标未观察到对应信号。 |
| 词数及新增和流失词 | 观测到的搜索词覆盖数量，新增和流失以可用对照期间为比较基础。 |
| 变化贡献项 | 对观测曝光增减作出贡献的词。 |
| 份额绝对变化与相对变化 | 份额差 0.05 表示五个百分点，相对变化 0.05 表示百分之五。 |

<a id="trend-and-context"></a>

## 趋势与背景指标

| 指标 | 含义 |
|---|---|
| 趋势分类 | 接口对指定对象、维度和实际窗口返回的方向分类。 |
| 波动程度与最新一期位置 | 窗口内起伏程度，以及最新观测处于该窗口数值范围的位置。 |
| 标准化斜率 | 接口用于支持单个对象在其窗口内趋势的无量纲指标。 |
| 关键词指标 | 搜索量和 ABA 排名描述关键词自身统计窗口内的情况。 |
| 商品快照与广告观测 | 快照日期下的商品信息，以及对应流量期间内观察到的广告参与情况。 |
