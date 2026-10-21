# 市场接口 Request / Response 审计

核对日期：2026-10-21。以配置中的 `http://localhost:8080/mcp` 直接 initialize、tools/list 得到的当前 14 个市场工具定义为准，并核对实际 MCP tools/call 返回。没有使用公开 OpenAPI 文档推断部署状态。dev 状态由用户提供，本轮未独立请求 dev。

## 当前契约与适配结果

- search 使用可选截止日期 date，实际日期为 resolvedDate；filters 仅有 28 对平铺 Min/Max 及 sellerCountryCodes，192 个排序指标独立维护。CLI 范围标志展开为平铺边界，不发送 dateRange 或嵌套指标对象。
- profile、七种分布、三种集中度使用可选精确 date；分布及集中度保留根层 sample-prefixed 总量与均值，profile 的样本统计在 sampleProfile。
- history 是月度历史，边界无需月末，只返回范围内已发布月末。读取 data[].points[].date 和 marketSize/sampleProfile，样本含单品月均销量/销售额；不读取 history[]、snapshotDate 或不存在的 min/max 评分价格。
- launch 使用可选 dateFrom/dateTo，过滤首次上架日期后分组；始终采用最新样本。拒绝请求 date，响应为 points[].date/productCnt，无快照日期。
- search 按次收费，空数据也收费；其他接口按实际返回去重市场数收费，空结果免费。余额准入按请求去重市场数检查而不预扣；多市场计费规则来自当前描述，尚未实测。
- 运行时参考、市场语义、证据读取、输出与共享 CLI 已按上述定义更新，所有权映射未改变。源码冻结 fixture 现由当前 MCP 输入和本地服务响应模型交叉核对生成，包含 4 种请求模型和 39 种根/嵌套响应模型的公开字段类型及可空性。

## 14 个接口逐项结果

每个工具都取得 success=true 且有数据的结果，外层 success/data/error/meta 原样保留。单类目为 679399011、样本为 unitSalesTop100；除 history/launch 外，详情 date=2026-10-19。history 查询 2026-06-01 至 09-30，launch 的基础请求不设上架范围。根字段数来自响应模型并与实际返回交叉核对，不表示所有字段必填。

| 接口 | 请求模型 | 根响应模型 | 根字段数 | 市场数 | requestId |
|---|---|---|---:|---:|---|
| search | MarketSearchRequest | MarketSearchFact | 202 | 1 | req_d6d713d597c54eea |
| history | MarketHistoryRequest | MarketHistorySeries | 6 | 1 | req_ce2f539f35ca4022 |
| profile | MarketIdentity | MarketProfile | 11 | 1 | req_bb69ae20eb654802 |
| price-distributions | MarketIdentity | PriceDistribution | 18 | 1 | req_e2353bc638df4ad0 |
| rating-distributions | MarketIdentity | RatingDistribution | 18 | 1 | req_c988927a55ac4de1 |
| rating-count-distributions | MarketIdentity | RatingCountDistribution | 18 | 1 | req_2e9187c81d6242e4 |
| listing-age-distributions | MarketIdentity | ListingAgeDistribution | 18 | 1 | req_6b0a0bb3a7824175 |
| fulfillment-distributions | MarketIdentity | FulfillmentDistribution | 18 | 1 | req_e33bfa902229412a |
| seller-country-distributions | MarketIdentity | SellerCountryDistribution | 18 | 1 | req_472a761b54214d1b |
| content-distributions | MarketIdentity | ContentDistribution | 18 | 1 | req_4ea42d21876c4eb0 |
| top-product-concentrations | MarketIdentity | TopProductConcentration | 19 | 1 | req_bc604da55e7f4e9f |
| brand-concentrations | MarketIdentity | BrandConcentration | 20 | 1 | req_14a2b347167046c2 |
| seller-concentrations | MarketIdentity | SellerConcentration | 19 | 1 | req_014d446a950a4837 |
| listing-launch-trend | MarketLaunchRequest | ListingLaunchTrend | 8 | 1 | req_0d609b1ae6054410 |

history 实际返回 2026-06-30、07-31、08-31、09-30 四个月末点。当前月中区间 10-01 至 10-19 为空且计费 0，不是接口或鉴权失败。launch 基础请求返回 55 个首次上架批次。每个有数据的单类目请求消耗 1 credit。

额外直接经 localhost MCP tools/call 验证：
- search 使用 date=2026-09-15、avgProductPrice30dMin=10、avgProductPrice30dMax=50，返回 resolvedDate=2026-08-31，确认截止日选择；requestId=req_4410ef3bc214420b。
- launch 使用 dateFrom=2026-07-01、dateTo=2026-09-30、granularity=month，返回 07/08/09 三个上架批次，商品数 5/5/1；requestId=req_36177510b3604227。

本会话注入的旧工具定义与直接 tools/list 的新定义不同。因此不能用旧会话定义认定当前服务描述错误，也不能仅凭配置文件确定原生工具历史请求实际连接了哪个实例。适配使用本次直接取得的当前定义。

## 本地验证与边界

- 332 组 CLI 构造请求通过当前 MCP JSON Schema 和本地服务原始 Pydantic 模型校验：14 接口 × 2 样本 × 2 范围，以及 28 筛选各三种边界、192 个排序值。
- 28 组完整嵌套/全 null 模拟响应通过原始模型及序列化检查；14 份已取得的真实 MCP 响应通过相同模型，序列化后字段与数值不丢失。
- 冻结清单见 [contract fixture](../tests/fixtures/market-spu-contract.json)；CLI 路由、非法输入不发请求、日期边界、0/null、分组身份和元数据保留均有回归检查。
- 全量仓库测试为 311 passed、2 skipped（可选 live 测试）；共享文件分发检查为 8 个技能、0 差异；9 个相关技能的 quick_validate 和 git diff --check 通过。
- 使用更新后的 CLI 构造参数，直接经 localhost MCP tools/call 完成三条集成验证：search 截止日返回 2026-08-31（req_9554921cfdf5461f）；history 返回 07/08/09 三个月末（req_0bc2d260edb84966）；launch 返回 07/08/09 三个上架批次（req_129a66fac0234d41）。每条消耗 1 credit。

上述实测是单类目和有限请求组合，不是全部业务参数、数据分布、BigQuery 计算或计费的穷举验收。未部署服务，未发布技能或验收已安装副本。
