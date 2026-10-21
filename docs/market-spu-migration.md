# SPU 市场接口迁移

<!-- 上游为组织内部仓库，匿名链接检查无法访问。 -->
<!-- markdown-link-check-disable-next-line -->
本次适配依据 [hermes-workspace #616](https://github.com/SerendipityOneInc/hermes-workspace/pull/616) 的 `4284967a4b6a02290a9b50a35e33c79c727d4560`。该提交定义 14 个市场接口；保留 search/history 的 HTTP 路径，更换请求和响应契约，退役 structure-profile。

2026-10-21 已直接从 localhost MCP tools/list 取得新契约，全部 14 个原生 MCP 工具取得有数据响应。当前服务与下文指定源码版本仍有日期、筛选、history 和 launch 请求/响应差异，运行时适配尚未完成，不能视为当前 PR 已兼容实际服务。详细证据见[市场接口审计](market-api-contract-audit.md#实际-mcp-核对2026-10-21)。

## 命令迁移

| 原调用 | 新调用 |
|---|---|
| `market --date YYYY-MM-DD` | `market --date-range 30d` 或 `--date-range YYYY-MM`；任意精确日快照使用 `market-profile --date YYYY-MM-DD` |
| `market --sample-avg-price-min 10 --sample-avg-price-max 30` | `market --avg-product-price30d 10:30` |
| `market --total-monthly-revenue-min 100000` | `market --total-monthly-sale-amt 100000:` |
| `market --seller-country US` | `market --seller-country-codes US` |
| `market --sort sampleAvgMonthlySales` | `market --sort avgProductMonthlySaleCnt` |
| `market-structure-profile --category-id ID --dimension price` | `market-price-distributions --category-id ID` |
| `market-structure-profile --category-id ID --dimension brand` | `market-brand-concentrations --category-id ID` |
| detail/history 的 `--category-scope direct` | `--no-include-descendant-category-products`；所有市场命令统一使用布尔开关 |

数值筛选的 `MIN:MAX`、`MIN:`、`:MAX` 分别表示双边、仅下限、仅上限，边界包含在内。金额直接使用美元，比例使用小数。CLI 暴露完整 192 个数值筛选及排序字段，拒绝旧字段、无效范围和已退役结构命令。具体参数以各命令 `--help` 为准。

独立接口包括 profile、价格/评分/评分数/上架年龄/履约/卖家国家/内容七种分布、商品/品牌/卖家三种集中度、listing-launch-trend。命令均为 `market-<接口名>`，支持 `--category-ids ID1,ID2` 批量查询，默认 `includeDescendantCategoryProducts=true`。listingYear 使用 `market-listing-launch-trend --granularity year`；productFeature 对应内容分布。

## 数据解释

- 同款变体合并为 SPU。旧 SKU 数量、旧 SKU 历史及旧持久化基线不能直接用于新口径比较；已有监控须在用户授权范围内建立兼容 SPU 基线，首次运行不能声称发生变化。
- search 返回扁平 Product 字段，使用 `snapshotDate`、`includeDescendantCategoryProducts`、`sampleType` 保留证据身份。`sampleMonthlySaleCnt/Amt` 是样本总量，`avgProductMonthlySaleCnt/Amt` 是单品均值；全市场销量/销售额分别为 `totalMonthlySaleCnt/Amt`。
- profile 的全市场为 `marketSize`；样本数量、销量、销售额及单品均值全部位于 `sampleProfile`，不再放在顶层。分布和集中度各有自己的数组字段，不再读取通用 `data.buckets[]`。分布桶使用 `bucketProductCnt/Rate` 和 `monthlySaleCntRate/monthlySaleAmtRate`；集中度实体明细仍使用 `saleCntRate/saleAmtRate`。Top N 汇总返回销量、销售额两种总量。
- history 的 `data[]` 按完整市场身份分组；组内 `history[]` 点使用 `snapshotDate`，并包含 `marketSize` 全市场总量和 `sampleProfile` 样本总量及价格、评分、评分数指标。同一类目路径变化时会产生多个系列，不能只按类目 ID 合并。没有 `data.points[]`、新品历史或 resolvedDateFrom/To。缺日期不补零、不拼接 SKU 历史。launch trend 是单期快照中的上架批次，不是历史需求趋势。
- 浮点值在公开单位下保留两位小数；整数、null 和真实 0 保留。国家/内容成员集合允许重叠；集中度随样本选择使用销量或销售额口径。暂不提供 `avgProductReviewCnt`。

## 部署与发布

新请求范围字段统一位于顶层。detail/history 不接受 `categoryScope` 或嵌套范围；search 服务仍兼容已发布的旧类目、范围、日期、筛选和排序参数，并在冲突时拒绝请求。CLI 只发送标准参数；history 请求已完全移除 `date`，即使 `date=null` 也不接受。响应不再提供 `dt`、`snapshotDt` 或 `productGrain`，但统计口径仍是 SPU。样本类型统一返回 `unitSalesTop100/revenueTop100`。

本改动只更新仓库源文件，未部署上游服务，也未发布 ClawHub 技能或创建 GitHub Release。运行前确认服务的 OpenAPI/MCP 已切换到这套 SPU 契约；仍暴露旧三接口契约的部署不兼容，不能静默回退到 SKU 字段。

服务与技能发布需要协调。共享 CLI 通过 `scripts/sync-scripts.sh` 分发到 8 个活跃技能；market-analysis 和 amazon-analysis 的白名单开放新市场命令，其余技能保持原命令范围。用户已有的本地安装需单独更新。ClawHub 由维护者手动执行 `clawhub sync`；合并本 PR 不代表发布完成。

回滚时也需协调服务与技能版本：恢复兼容旧服务的技能发布，并重置不兼容的监控基线。不要将旧、新统计口径混合输出。

完整逐接口核对范围、请求/响应模型与验证限制见[市场接口审计](market-api-contract-audit.md)。
