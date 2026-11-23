<!-- prompt-source: skill/datas/traffic-structure/definition.md 1875d4a56e390d9f9dd732f0f48abf2359cee909603f1e33c3de7a2f2093fe77 -->

> 英文原文：[原文](../../../../skill/datas/traffic-structure/definition.md)

# 商品流量来源

比较指定商品的自然搜索曝光和广告曝光。

## 任务输入

商品 ASIN 和观察周。

## 接口与调用顺序

1. 调用 `openapi_v2_product_traffic_structure_profile`（`keywords/product-traffic-structure-profile`）。首次调用前核对接口计费。

## `keywords/product-traffic-structure-profile`

### 查询参数

| 参数 | 用法 |
|---|---|
| `asin` | 单个商品 ASIN。 |
| `date` | 必填。观察日期，格式 YYYY-MM-DD。 |
| `asins` | 商品 ASIN 数组，多商品查询时使用。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"asin":"B0C7P89D14","date":"2026-11-07"}
```

### 返回处理

1. 读取各 ASIN 的 `productTrafficTermsProfile` 及本期和上期范围。
2. 按返回内容读取 `summary`、`trafficStructureChange`、`organicStructureChange` 和 `termChangeDrivers`，保留渠道标识及已有流量词记录的实际字段。

## 交付结果

商品的流量来源和渠道占比。
