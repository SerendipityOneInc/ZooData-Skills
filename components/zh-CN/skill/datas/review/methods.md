<!-- prompt-source: skill/datas/review/methods.md 5587a8b9c0b6bd959904ccae1dabd0aafd6b1062859f9b86c4b73ba467102368 -->

> 英文原文：[skill/datas/review/methods.md](../../../../skill/datas/review/methods.md)

<a id="consumer-feedback-analysis-methods"></a>

# 消费者反馈分析方法

<a id="categories-category-lookup"></a>

## categories：类目检索

1. 按目标类目名称或路径取得准确的返回路径，供类目模式分析使用。

<a id="reviewsanalysis-consumer-theme-profiles"></a>

## reviews/analysis：买家反馈分析

1. 使用连接器中对应的消费者聚合分析工具，按当前定义选择 ASIN 或类目模式，传入相应标识、站点及支持的期间。
2. 读取返回的评论数、星级和情感分布及消费者洞察维度，从该响应中选择所需维度。
3. 保留各主题的维度、名称、提及数量、提及率和关联星级；按要求在同一评论集合内用数量或比例本地排序。

<a id="reviewssearch-stored-review-text"></a>

## reviews/search：已存评论原文

1. 对已明确ASIN，按问题需要使用工具支持的评论日期、星级或其他筛选。按所需覆盖范围使用分页及支持的排序；记录中返回的主题标签不是筛选参数。
2. 保留评论ID、原文、星级、日期和商品或变体信息。该查询返回ASIN所属父体的评论；只有原文或返回的变体信息能够证明归属时，才将体验归到特定变体。

<a id="realtimereviews-current-page-reviews"></a>

## realtime/reviews：当前页面评论

1. 用户需要商品页面当前展示的最新评论时，使用该来源，传入已明确ASIN和站点。第一页不传游标；需要继续读取时使用返回的 `nextCursor`，为空表示没有下一页。
2. 保留该页面样本的实际评论日期和商品范围，不以它替代指定历史期间的评论。

<a id="local-analysis-theme-evidence"></a>

## Local analysis：主题原文证据

1. 所需主题及覆盖范围已包含在用户或已有评论原文中时，直接在本地分析，不要求提供ASIN或再次查询。
2. 仍需要评论原文时，使用[已存评论](#reviewssearch-stored-review-text)，传入所需评论期间。用户明确要求当前页面的最新评论时，使用[当前页面评论](#realtimereviews-current-page-reviews)。只有上下文和接口默认值都不能补足必要ASIN或站点时才询问用户。
3. 保留评论ID、原文、星级、日期和变体信息，按来源ID去重；没有ID时使用本地行标识。
4. 用户要求文本分析时，按原文标记情感和主题，合并等价表达时保留否定和使用情境；每条评论对每个主题只计一次。
5. 本地提及率为提及该主题的不同可读评论数除以全部不同可读评论数。按支持评论的有效星级计算主题均值，保留支持ID并标注这些本地计算。
6. 必要原文未取得时，交付现有文本支持的发现并说明缺少的覆盖；完全没有可读原文时，说明无法形成所问的文本判断。

<a id="realtimeproduct-rating-distribution"></a>

## realtime/product：评分分布

1. 按连接器商品工具的实际返回路径，读取目标 ASIN 的评分数、星级及可用星级分布。
2. 将商品整体评分范围与消费者主题使用的文字评论范围分别保留。

<a id="local-analysis-feedback-comparison"></a>

## Local analysis：反馈比较

1. 对各指定商品或评论集合，复用口径相符的主题报告。只有 ASIN 或类目时，按[买家反馈分析](#reviewsanalysis-consumer-theme-profiles)分别取得各比较集合的报告。已有用户评论原文，或用户明确要求基于原文比较时，按[主题原文证据](#local-analysis-theme-evidence)补齐所需主题分析。
2. 在指定期间和变体范围内比较相同主题维度，保留各自来源和分母，报告观察到的数量和比例差异及可用支持文本；描述用户特征与使用场景的关联时，使用明确连接两者的原文。
3. 某评论集合的必要主题数据无法取得或口径无法对齐时，分别报告已有发现，指出尚不能比较的部分，不将缺失主题当作提及数量为 0。
