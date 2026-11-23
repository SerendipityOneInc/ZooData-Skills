<!-- prompt-source: skill/datas/keyword/definition.md 4e126c7b827e267c07ea1254d7086f2152b0b77b1564f442b80205aa3e3b2384 -->

> 英文原文：[skill/datas/keyword/definition.md](../../../../skill/datas/keyword/definition.md)

<a id="keyword-analysis"></a>

# 关键词分析

1. 本 Skill 以搜索词或明确的词集为分析对象，提供相关关键词拓展、关键词分类、基础指标统计、关键词画像、趋势画像和周度趋势数据分析。

<a id="identify-required-inputs"></a>

## 确认分析所需输入

1. 使用种子词或指定词集、站点，以及所需期间和筛选条件。

<a id="select-an-analysis-task"></a>

## 选择分析任务

| 任务标识 | 必要输入 | 标准报告内容 | 对应方法 |
|---|---|---|---|
| Keyword expansion（拓词） | 种子词、站点及明确的召回约束 | 相关关键词、关键词分类、相关度，以及返回的候选词快照中的基础指标 | [拓词](methods.md#keywordsextends-related-term-expansion) |
| Keyword statistics（关键词基础指标统计） | 指定词或明确的词集、站点及快照日期 | 当前问题所需的搜索需求、Top3 份额、商品供给、自然位及广告数量、头部商品基准等快照统计，以及实际统计期间 | [关键词详情](methods.md#keywordsdetail-keyword-details) |
| Keyword profile（关键词画像） | 指定词或明确的词集、站点及快照期间 | 搜索需求量、自然位竞争难度、供给饱和度、头部商品基准、点击及转化集中度、品牌结构、广告覆盖率和年度季节性 | [画像分析](methods.md#keywordsmarket-profile-keyword-profiles) |
| Keyword trend profile（趋势画像） | 词集、站点、截至日期及工具支持的时间窗口 | 搜索需求量及 ABA 排名的趋势分类、支撑变化数据、需求波动程度和最新一期在窗口内的位置 | [趋势画像](methods.md#keywordstrend-profile-trend-profiles) |
| Keyword weekly history（周度趋势数据） | 词集、站点及日期范围 | 逐周搜索量、ABA 排名及当前问题所需的 Top3 点击和转化份额，以及实际周起止日期 | [周度趋势数据](methods.md#keywordstrend-weekly-trend-data) |

<a id="preserve-object-features-and-report-findings"></a>

## 保留对象特征并交付报告

1. 保留每个原始关键词、站点，以及已取得的预估搜索次数、统计窗口和 ABA 搜索频率排名。
2. 拓词时交付关键词列表、预估搜索量、ABA 排名、相关度和关键词分类。
3. 用户要求基础指标统计时，逐词报告所需数值和实际快照期间。
4. 用户要求关键词画像时，报告当前问题所需的搜索需求量、竞争及搜索结构维度和支撑指标，涉及季节性时报告年度季节性。
5. 用户要求趋势画像时，报告所选窗口、返回的趋势方向、支撑变化数据，以及已返回的波动程度和最新一期在窗口内的位置。
6. 用户要求周度趋势数据时，报告所需序列和观测变化，保留返回的期间边界和覆盖范围。
