<!-- prompt-source: skill/datas/product-history/definition.md 09d5d4f43324fa379052efb5c88e219d7c4621e695d09842216b8e13c5987f47 -->

> 英文原文：[原文](../../../../skill/datas/product-history/definition.md)

# 商品历史

查询前按[趋势查询期间](../../../contract/query.md#select-the-trend-period)确定要传入的窗口。

查看指定 ASIN 在所选期间的价格、类目排名或页面变化。

## 任务输入

一个商品 ASIN、要查看的指标和期间。

## 接口与调用顺序

1. 对同一 ASIN 和期间，将所需字段放入 `aspects`，调用一次 `openapi_v2_products_history`（`products/history`）。首次调用前核对接口计费。

## `products/history`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 必填。单个商品 ASIN。 |
| `startDate` | 必填。起始日，YYYY-MM-DD。 |
| `endDate` | 必填。结束日，YYYY-MM-DD。 |
| `aspects` | 按所问项目传数组：标题 `title`、主图 `imageUrl`、价格 `price`、大类和子类排名及其类目 `bsr`、`bsrCategory`、`subBsr`、`subBsrCategory`，星级和累计评分数 `rating`、`ratingCount`。需要区分父体变化时加 `parentAsin`。省略时返回全部支持项。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14","startDate":"2026-10-01","endDate":"2026-10-31","aspects":["title","imageUrl","price"]}
```

### 返回处理

1. 标题 `title` 和主图 `imageUrl` 返回带 `date` 和 `value` 的事件。比较前后两个已知值并标明各自的观测日期。两次采样之间有空档时，具体生效日未知。只有一条记录时用作基准；主图地址变化时记录新旧地址，画面差异需查看两张图才能描述。
2. 价格 `price`、BSR、购买量下限和评分等逐点数据按下标与 `timestamps` 对齐。用同一 ASIN 的有效价格计算价差，并用观测日期标注；两次观测之间有空档时保留日期范围。
3. 保留返回的观测覆盖。区分类目排名及父子体口径；没有足够记录时写“缺少可比记录”，有可比记录且数值相同时写“观测期间未见变化”。

## 交付结果

所选商品指标的历史记录和有日期的页面变化。
