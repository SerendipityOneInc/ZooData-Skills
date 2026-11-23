<!-- prompt-source: skill/datas/traffic-trend/definition.md c66025aa70c534036b7e3d678b11ded6d1d04bb98eeff1bf9a8063aa712da709 -->

> 英文原文：[原文](../../../../skill/datas/traffic-trend/definition.md)

# 商品曝光趋势

查询前按[趋势查询期间](../../../contract/query.md#select-the-trend-period)确定要传入的窗口。

查看指定商品在所选期间的曝光趋势与波动。

## 任务输入

商品 ASIN、截止周及要比较的趋势窗口。

## 接口与调用顺序

1. 调用 `openapi_v2_product_traffic_trend_profile`（`keywords/product-traffic-trend-profile`）。首次调用前核对接口计费。

## `keywords/product-traffic-trend-profile`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 单个商品 ASIN。 |
| `date` | 必填。观察日期，格式 YYYY-MM-DD。 |
| `windowPeriods` | 当前接口支持 `[4]`，对应四周。 |
| `asins` | 商品 ASIN 数组，多商品查询时使用。 |
| `detailLevel` | 按问题选择接口支持的详细程度。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14","date":"2026-11-07","windowPeriods":[4]}
```

### 返回处理

1. 读取各窗口记录的状态，再读取 `trafficTrendProfile` 中可用部分；逐项读取已返回的 `trend`、`trendEvidence`、`volatilityLevel` 和 `lastPeriodWindowPosition`。

## 交付结果

所选窗口内的曝光方向、变化和波动。
