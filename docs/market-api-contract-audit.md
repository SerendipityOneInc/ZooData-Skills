# 市场接口 Request / Response 审计

核对日期：2026-10-20。基准为 [hermes-workspace #616](https://github.com/SerendipityOneInc/hermes-workspace/pull/616) 的 `4284967a4b6a02290a9b50a35e33c79c727d4560`，不代表服务已部署。

## 核对方法与结果

逐一从实际路由读取请求模型和响应模型，加载该提交的原始 Pydantic 模型（包含继承字段、验证器和序列化器），核对 4 种请求模型、14 种根响应、25 种嵌套响应。没有以字段注释或旧版字段清单代替实际 Schema。本机执行环境为 Python 3.11、Pydantic 2.6.4，未启动完整后端服务。

- 248 组 CLI 请求通过原始请求模型校验：14 个接口 × 2 种样本类型 × 2 种商品范围，加上全部 192 个数值筛选与排序组合。
- 28 组模拟响应通过原始响应模型及序列化检查：每个接口各验证全部字段有值和全部仓库字段为 null。有值样本包含完整嵌套对象、数组及真实 0；这不是线上数据查询。
- 8 组兼容/拒绝场景通过：旧类目、范围、Min/Max、样本类型、日期窗口正常转换；选择器冲突、旧新边界冲突、字符串布尔值及 history 的 `date=null` 被拒绝。
- 各根响应及其嵌套模型的公开字段集合与上次适配一致。已将冻结清单补全为字段类型、可空性、请求默认值、必填字段及逐接口映射，见 [contract fixture](../tests/fixtures/market-spu-contract.json)。

## 14 个接口逐项结果

均为 `POST /openapi/v2/markets/<名称>`。响应外层保留 `{success,data,error,meta}`，表中模型对应 `data[]` 的元素；meta 的分页、请求和计费信息不能丢失。

| 接口名称 | 请求模型 | 必填参数 | 根响应模型 | 根字段数 | 结果 |
|---|---|---|---|---:|---|
| search | MarketSearchRequest | 无 | MarketSearchFact | 202 | 标准 CLI 请求兼容 |
| history | MarketHistoryRequest | categoryIds、dateFrom、dateTo | MarketHistorySeries | 6 | 标准 CLI 请求兼容 |
| profile | MarketIdentity | categoryIds | MarketProfile | 11 | 标准 CLI 请求兼容 |
| price-distributions | MarketIdentity | categoryIds | PriceDistribution | 13 | 标准 CLI 请求兼容 |
| rating-distributions | MarketIdentity | categoryIds | RatingDistribution | 13 | 标准 CLI 请求兼容 |
| rating-count-distributions | MarketIdentity | categoryIds | RatingCountDistribution | 13 | 标准 CLI 请求兼容 |
| listing-age-distributions | MarketIdentity | categoryIds | ListingAgeDistribution | 13 | 标准 CLI 请求兼容 |
| fulfillment-distributions | MarketIdentity | categoryIds | FulfillmentDistribution | 13 | 标准 CLI 请求兼容 |
| seller-country-distributions | MarketIdentity | categoryIds | SellerCountryDistribution | 13 | 标准 CLI 请求兼容 |
| content-distributions | MarketIdentity | categoryIds | ContentDistribution | 13 | 标准 CLI 请求兼容 |
| top-product-concentrations | MarketIdentity | categoryIds | TopProductConcentration | 14 | 标准 CLI 请求兼容 |
| brand-concentrations | MarketIdentity | categoryIds | BrandConcentration | 15 | 标准 CLI 请求兼容 |
| seller-concentrations | MarketIdentity | categoryIds | SellerConcentration | 14 | 标准 CLI 请求兼容 |
| listing-launch-trend | MarketLaunchRequest | categoryIds | ListingLaunchTrend | 11 | 标准 CLI 请求兼容 |

## Request 完整范围

| 请求模型 | 公开标准字段 |
|---|---|
| MarketSearchRequest | marketplace、category、categoryIds、categoryKeyword、includeDescendantCategoryProducts、sampleType、dateRange、filters、topN、newProductPeriod、page、pageSize、sortBy、sortOrder |
| MarketIdentity | marketplace、categoryIds、includeDescendantCategoryProducts、sampleType、date |
| MarketHistoryRequest | marketplace、categoryIds、includeDescendantCategoryProducts、sampleType、dateFrom、dateTo |
| MarketLaunchRequest | MarketIdentity 的所有字段，另加 granularity |

`category` 的 `ids/path/name` 至多选一个；顶层 `categoryIds` 不能与这些定位字段组合。ID 数组为 1–100 项，ID 非空且至多 128 字符；路径数组为 1–10 项。关键词长度为 1–200。搜索筛选条件之间为 AND，国家代码列表内部为 OR。

search 的 filters、商品范围及部分定位字段可为 null；省略/null 商品范围的有效语义是包含下级商品。其他接口的范围为严格 boolean，默认 true，不能用字符串或 null 替代。sampleType 默认为 unitSalesTop100，另一个标准值为 revenueTop100。

search 使用 dateRange：标准值为 30d 或 YYYY-MM。detail/launch 可传精确 date，也允许 null；history 的两个日期必填且有序，其 Schema 已完全没有 date，连 date=null 也拒绝。所有详情日期与 history 范围日期不能混用。

### 新发现并修正的兼容说明

服务现在对旧 search 请求执行转换，包括旧类目及 scope 定位、snapshotDate/date、正数 Nd 范围、平铺或分组 Min/Max、旧指标/排序名和样本别名。旧日期不是任意日快照请求：当前月份解析为最新快照，其他月份解析为月末；Nd 选择最新快照。旧日期选择器优先于 30d 窗口；不一致的明确历史月份或筛选边界会失败。响应始终为新 SPU 结构。

CLI 仍只生成标准请求，不因此新增旧参数别名。REST 的模型兼容性与 MCP 的公开 inputSchema 不是同一层；MCP 应使用其公开标准值，不能据 REST 接受某个别名就推断所有 MCP 工具也接受它。

## Response 完整核对范围

字段名称、类型、可空性、对象/数组引用均已逐模型核对并冻结。所有仓库来源字段都是可选且可空；data=[]、某个嵌套数组=null、某项数值=0 是三种不同结果。

- **search**：202 个扁平字段；包含市场身份、全市场/样本总量、单品均值、固定和动态 Top N、新品窗口。192 个筛选/排序指标都使用公开单位，不再额外乘除 100。
- **profile**：marketSize 表示全市场；样本数量、销量、销售额、均值和子画像均在 sampleProfile。样本计数为零或缺失时，单品月均指标为 null，不能填 0。
- **七种分布**：逐一核对各自数组与桶类型。外层份额分母是样本；价格/内容桶中的新品份额分母是父桶，桶内品牌集中度也使用父桶。数值边界的开闭规则由 bucket 编码确定，不能仅看 lowerBound/upperBound；上架年龄边界使用日历月。
- **三种集中度**：逐一核对 Top N 汇总与商品/品牌/卖家实体明细。汇总同时返回销量、销售额；浓度跟随 sampleType。新品 saleRate 的分母为所在 Top N 组。实体明细的 saleCntRate/saleAmtRate 不得套用到分布桶。
- **history**：data[] 是完整市场身份系列，history[] 才是时间点。逐点分别读取 marketSize 与 sampleProfile。路径、币种、范围或样本类型不同的系列不得只凭 category.id 合并。历史样本块没有独立 profile 的单品月均指标，也没有新品窗口。
- **listing-launch-trend**：只提供某个快照内按月/年分组的上架数量，不能解释为历史需求曲线。

### 上游尚存的说明问题

MarketHistoryFact 的 marketSize 字段注释仍提到“available new-product windows”，sampleProfile 注释仍提到“per-SPU averages / available sample subprofiles”。实际 MarketHistorySales 与 MarketHistorySampleProfile Schema 不包含新品窗口或 avgProductMonthlySaleCnt/Amt。本仓库按实际字段解释，已明确排除这些不存在的能力；这些上游注释需要另外修正。

## 线上与发布边界

只读获取 `https://zoodata.ai/api/v1/openapi-spec?format=json` 后，实际 Schema 位于外层 spec。2026-10-20 仍只有 search、structure-profile、history 三个旧市场接口，与上述 14 接口源码契约不一致。

本轮未调用付费市场数据接口，未验证 BigQuery 数据、鉴权、线上 MCP 调用或已安装技能，也未部署服务或发布技能。源码模型校验和模拟序列化通过不能替代这些验收。

仓库验证：`python -m pytest -q --tb=short` 为 310 passed、2 skipped（可选 live 测试）；`bash scripts/sync-scripts.sh --check` 为 8 个技能、0 个差异；`git diff --check` 通过。
