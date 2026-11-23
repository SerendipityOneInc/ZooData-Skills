<!-- prompt-source: skill/datas/market-review-profile/definition.md 31857301cad6d2b5cb6af40e78d809622e38d824ec5cb9c86a74a0c7673cd987 -->

> 英文原文：[原文](../../../../skill/datas/market-review-profile/definition.md)

# 类目评价画像

按亚马逊美国站类目查询评价画像，了解买家的使用场景、购买原因、抱怨和改进诉求。

## 任务输入

一个明确的类目路径；可指定评论期间。

## 接口与调用顺序

1. 使用 `openapi_v2_voc_analysis`（`voc/analysis`）查询评价画像。

## `voc/analysis`

### 查询参数

| 参数 | 必填 | 用法 |
|---|---|---|
| `mode` | 是 | 固定为 `category`。 |
| `categoryPath` | 是 | 从根类目到目标类目的路径数组。 |
| `marketplace` | 否 | 美国站使用 `US`。 |
| `period` | 否 | 未指定时显式传 `1y`（最近 12 个月）。可选 `1m`、`3m`、`6m`、`1y`、`2y`。 |

```json
{"mode":"category","categoryPath":["Home & Kitchen","Storage & Organization"],"marketplace":"US","period":"1y"}
```

### 返回处理

直接取 `data` 作为画像。画像有数据时即结束，保留缺项、未出现的主题和真实零值。

未取得画像时说明所查类目及期间。

## 交付结果

按以下顺序交付同一份评价画像。对话中使用业务名称，结构化结果沿用接口字段。

1. **样本范围**：分析模式 `mode`、商品 `asins` 或类目 `categoryPath`、覆盖日期 `dateRangeStart` / `dateRangeEnd`、评论数 `reviewCount`。
2. **评价概况**：平均星级 `avgRating`、已验证购买占比 `verifiedRate`、各星级评论数 `ratingDistribution`、情感占比 `sentimentDistribution`。
3. **评价主题与高频词**：`consumerInsights` 和 `topKeywords` 使用相同的条目字段：维度 `labelType`、主题或词 `element`、提及次数 `count`、提及率 `reviewRate`、相关评论平均星级 `avgRating`。提及率以该画像的评论数为分母。商品问题（`issues`）、痛点（`painPoints`）、好评（`positives`）和改进诉求（`improvements`）分别列出，同一维度内按提及次数排序，同值并列。
