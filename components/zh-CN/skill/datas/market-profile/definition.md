<!-- prompt-source: skill/datas/market-profile/definition.md 724082615f2d449a165f6cb3f47baf99aea8eb9c4ddb7f68e9b3eaad0c27fc50 -->

> 英文原文：[原文](../../../../skill/datas/market-profile/definition.md)

# 类目画像

查看指定类目的整体需求和头部商品表现。

## 任务输入

一个或多个已确认的类目及要比较的市场指标。

## 接口与调用顺序

1. 调用 `openapi_v2_markets_profile`（`markets/profile`）。首次调用前核对接口计费。

## `markets/profile`

### 查询参数

| 参数 | 用法 |
|---|---|
| `categoryIds` | 必填。已确认的类目 ID 数组。 |
| `sampleType` | 选择按销量或营收取头部样本的方式。 |
| `includeDescendantCategoryProducts` | 是否计入下级类目的商品。 |
| `date` | 观察日期，格式 YYYY-MM-DD。 |
| `marketplace` | 美国站使用 `US`。 |

```json
{"categoryIds":["679399011"]}
```

### 返回处理

1. 从 `marketSize` 读取全市场指标，从 `sampleProfile` 读取样本指标，提取当前问题所需的价格、评分、新品和集中度部分。
2. 按实际数据日和一致的子类目范围比较。类目总量按父商品（SPU）统计，样本指标只描述按指定规则选出的头部父商品。

## 交付结果

类目规模与该类目头部商品的画像。
