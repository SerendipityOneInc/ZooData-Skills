<!-- prompt-source: skill/datas/product-review-profile/definition.md 2f7ab241b7fdaeacf0ead15fad5045fd1583148fa8bd0fa5716b758fab1003d3 -->

> 英文原文：[原文](../../../../skill/datas/product-review-profile/definition.md)

# 商品评价画像

按一个或多个 ASIN 查询商品评价画像，包括买家抱怨、好评、改进诉求及其提及率。

## 任务输入

一个或多个商品 ASIN；可指定评论期间。

## 接口与调用顺序

1. 使用 `openapi_v2_voc_analysis`（`voc/analysis`）查询评价画像。
2. 仅在画像未取得时，使用 `openapi_v2_realtime_reviews`（`realtime/reviews`）读取原文并生成画像。

## `voc/analysis`

### 查询参数

| 参数 | 必填 | 用法 |
|---|---|---|
| `mode` | 是 | 固定为 `asin`。 |
| `asins` | 是 | 1–100 个商品 ASIN，一次查询得到一份合并画像。每个 ASIN 对应其父体的评论范围，同父变体共用一组评论。 |
| `marketplace` | 否 | 美国站使用 `US`。 |
| `period` | 否 | 未指定时显式传 `1y`（最近 12 个月）。可选 `1m`、`3m`、`6m`、`1y`、`2y`。 |

```json
{"mode":"asin","asins":["B0C7P89D14"],"marketplace":"US","period":"1y"}
```

### 返回处理

保留请求的 ASIN、已有资料能确认的父 ASIN 及评论覆盖范围。父体汇总用于判断整组商品的表现。只有能识别具体变体的评论才支持该变体的结论。取 `data` 作为画像。画像有数据时即结束，保留缺项、未出现的主题和真实零值。

画像无结果或 `reviewCount=0` 时转实时接口。鉴权、连接或额度受限时停止。

## `realtime/reviews`

### 查询参数

| 参数 | 必填 | 用法 |
|---|---|---|
| `asin` | 是 | 一个待补查的商品 ASIN。 |
| `marketplace` | 否 | 沿用原查询的美国站 `US`。 |
| `cursor` | 否 | 首页省略；后续页传上一页的 `nextCursor`，为空时结束。 |

```json
{"asin":"B0C7P89D14","marketplace":"US"}
```

### 返回处理

1. 在查询预算内读取页面评论，只纳入与画像相同期间内有日期的可读原文。跨页和跨 ASIN 去重，每条评论在每个主题下最多计一次。
2. 按下方格式生成画像。整体或主题平均星级只使用相应集合中有星级的评论。可计算时填写分布与比例；无法确定的字段标为未获取。注明实际覆盖商品、日期及“页面评论样本”。没有可用原文时，说明未取得画像。

## 交付结果

按以下顺序交付同一份评价画像。对话中使用业务名称，结构化结果沿用接口字段。

1. **样本范围**：分析模式 `mode`、商品 `asins` 或类目 `categoryPath`、覆盖日期 `dateRangeStart` / `dateRangeEnd`、评论数 `reviewCount`。
2. **评价概况**：平均星级 `avgRating`、已验证购买占比 `verifiedRate`、各星级评论数 `ratingDistribution`、情感占比 `sentimentDistribution`。
3. **评价主题与高频词**：`consumerInsights` 和 `topKeywords` 使用相同的条目字段：维度 `labelType`、主题或词 `element`、提及次数 `count`、提及率 `reviewRate`、相关评论平均星级 `avgRating`。提及率以该画像的评论数为分母。商品问题（`issues`）、痛点（`painPoints`）、好评（`positives`）和改进诉求（`improvements`）分别列出，同一维度内按提及次数排序，同值并列。
