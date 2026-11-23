<!-- prompt-source: skill/datas/traffic-weeks/definition.md 864295052797f222e395dc949cf7c1b904db766f23e79d0f456a844fd704e66d -->

> 英文原文：[原文](../../../../skill/datas/traffic-weeks/definition.md)

# 商品每周曝光

查询前按[趋势查询期间](../../../contract/query.md#select-the-trend-period)确定要传入的窗口。

查看指定商品每周的曝光及展示位置指标。

## 任务输入

商品 ASIN 和观察期间。

## 接口与调用顺序

1. 调用 `openapi_v2_product_traffic_trend`（`keywords/product-traffic-trend`）。首次调用前核对接口计费。

## `keywords/product-traffic-trend`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 单个商品 ASIN。 |
| `dateFrom` | 必填。周度数据的起始日期。 |
| `dateTo` | 必填。周度数据的截止日期。 |
| `asins` | 商品 ASIN 数组，多商品查询时使用。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14","dateFrom":"2026-08-16","dateTo":"2026-11-07"}
```

### 返回处理

1. 逐个读取商品的返回状态和周度 `series`。
2. 保留每周边界、整体和自然及广告曝光点、词数，以及返回的位置和需求排名分布，按所需周次比较相同指标。

3. 每次最多 26 个完整周（周日至周六）。使用每周返回的自然、广告和总预估曝光点数；总点数大于零时才计算占比。

## 交付结果

同一商品逐周可比的曝光记录。
