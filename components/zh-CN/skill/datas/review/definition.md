<!-- prompt-source: skill/datas/review/definition.md 32e2bb1133f04c3ba09739008308b375d4cf970c73e0fd834ac56ef1a0a1d520 -->

> 英文原文：[skill/datas/review/definition.md](../../../../skill/datas/review/definition.md)

<a id="consumer-feedback-analysis"></a>

# 消费者反馈分析

1. 本 Skill 按选定类目或指定 ASIN 列表分析买家评论，涵盖购买原因、使用场景、满意点、常见抱怨、商品评论原文、星级分布及反馈差异。

<a id="identify-required-inputs"></a>

## 确认分析所需输入

1. 使用 ASIN 或已明确类目、站点、相关期间及消费者问题；已有评论原文保留来源、商品身份和覆盖范围。
2. 按类目分析且需要准确路径时，使用[类目检索](methods.md#categories-category-lookup)。

<a id="select-an-analysis-task"></a>

## 选择分析任务

| 任务标识 | 必要输入 | 标准报告内容 | 对应方法 |
|---|---|---|---|
| Consumer-theme profile（买家反馈分析） | ASIN 集合或类目、站点及期间 | 买家关注点、购买原因、使用场景、评价倾向、提及数量和比例及评论范围 | [对应方法](methods.md#reviewsanalysis-consumer-theme-profiles) |
| Theme evidence（主题原文证据） | ASIN 或已提供评论原文及明确主题问题 | 取得的评论原文和标识、文本支持的主题及按需本地统计 | [对应方法](methods.md#local-analysis-theme-evidence) |
| Rating distribution（评分分布） | ASIN 及站点 | 返回的评分数、星级和星级分布 | [对应方法](methods.md#realtimeproduct-rating-distribution) |
| Feedback comparison（反馈比较） | 明确评论集合及比较维度 | 同主题提及数量和比例、支持文本及样本范围差异 | [对应方法](methods.md#local-analysis-feedback-comparison) |

<a id="preserve-object-features-and-report-findings"></a>

## 保留对象特征并交付报告

1. 保留 ASIN 或类目、有效文字评论数、期间、来源及相关变体选择。
2. 买家反馈分析交付所需维度的提及数量和比例及已返回的关联星级；原文证据保留来源标识，区分摘录与摘要。
3. 评分报告呈现返回的星级分布；反馈比较保留各评论集合自身的分母及所需共同主题。
