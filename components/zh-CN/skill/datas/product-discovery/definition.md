<!-- prompt-source: skill/datas/product-discovery/definition.md 8955e89330ccf2368959ae39581836239b045388f5b033f3f3d08e814c01ca58 -->

> 英文原文：[原文](../../../../skill/datas/product-discovery/definition.md)

# 商品筛选

按确认的用途、关键词或类目查找符合条件的商品。

## 任务输入

已确认的筛选范围（全部类目或指定类目）、可选商品关键词、实际筛选条件及排序要求。

## 接口与调用顺序

1. 调用 `openapi_v2_products_search`（`products/search`）。首次调用前核对接口计费。

## `products/search`

### 查询参数

| 参数 | 用法 |
|---|---|
| `dateRange` | 留空查询最新可用数据。查询已结束的月份时传 YYYY-MM。若该月尚未发布，保留指定月份并说明数据尚未提供。 |
| `keyword` | 本次查询的搜索词。 |
| `categoryPath` | 从根类目到目标类目的路径。 |
| `keywordMatchType` | 仅在提供关键词时传入。 |
| `listingAge` | 上架时长上限可选 `30d`、`90d`、`180d`、`1y` 或 `2y`。近半年传 `180d`。不限上架时间时省略。 |
| `monthlySalesMax`、`fulfillments` | 按已选条件传入月购买量下限的上限及配送方式。 |
| `sortBy` | 接口支持的排序字段。 |
| `sortOrder` | 升序 asc 或降序 desc。 |
| `page` | 需要分页时传页码。 |
| `pageSize` | 每页返回条数。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"keyword":"small storage baskets"}
```

### 返回处理

1. 保留 ASIN、商品属性与类目路径，分别记录匹配总数和实际读取条数。
2. 分别记录请求期间和实际数据日期。指定历史月份并成功命中时，使用该月月末记录。查最新数据时以返回的实际数据日期为准；未提供实际日期时，保留“近 30 天”的指标口径，具体截止日写“未返回”。
3. 在最新每日数据中，`salesGrowthRate` 计算同一商品 ASIN 当前的近 30 天购买量下限，相对 30 天前记录的同口径下限的变化率。父体同期的购买量下限和增长率分别取 `parentMonthlySalesFloor` 和 `parentSalesGrowthRate`，保留 `parentAsin`。返回值为小数；筛选参数也用小数。缺少比较基数或基数为零时无可用增长率。

4. 每个商品保留累计评分数 `ratingCount` 和近 30 天评分数净变化 `monthlyRatingCount`。净变化为当前累计评分数减去 30 天前的累计评分数，单位为条。保留负数、零和空值。

## 交付结果

符合筛选条件的商品列表及其覆盖范围。
