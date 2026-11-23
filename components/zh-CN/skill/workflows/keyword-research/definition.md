<!-- prompt-source: skill/workflows/keyword-research/definition.md abb269e21e2f7026ea12d28ece49203316a0d3a81811365bf6bff29830c070b2 -->

> 英文原文：[原文](../../../../skill/workflows/keyword-research/definition.md)

# 亚马逊美国站关键词研究

## 查询前选择任务

| 用户问题 | 需要读取的说明 |
|---|---|
| 从核心词拓展相关词，并按搜索意图分组 | 首次查询前读取[相关词取数方法](../../datas/keyword-expansion/definition.md)。对用户指定的每个核心词查一次首页，翻页时沿用同一个词。把结果中出现的其他说法作为候选词。 |
| 了解或比较指定词的需求、竞争或季节性 | 读取[研究方法](methods.md)中的指定词画像与比较方法。 |
| 研究需求变化或查看指定周的数据 | 读取[研究方法](methods.md)中的需求趋势方法。 |
| 查指定 ASIN 的流量词或商品在指定词下的曝光与位置 | 读取[研究方法](methods.md)中的指定商品研究方法。 |

1. 优先复用用户提供且符合本次要求的数据。新增查询使用[取数规则](../../../contract/query.md)，按[证据规则](../../../contract/evidence.md)解释结果。
2. 拓词使用[研究方法](methods.md)中的分组依据。用户同时要求推荐时，再按其标准比较相关候选。只有不同理解会改变筛选结果时才澄清比较依据。

## 交付报告

1. 取得数据后，读取对应的[报告提纲](report-outline.md)和[报告生成指南](../../../tools/report/definition.md)，按所选任务整理报告输入。展示关键词列表时，每行从候选记录填写提纲要求的基础指标。
2. 用户未明确指定其他格式时，运行[共享 HTML 生成器](../../../../tools/report/scripts/render_report.py)，确认实际生成了 HTML 文件。专家和独立技能各交付一份报告。
3. 按[HTML 文件交付规则](../../../contract/report.md#hand-off-the-html-report)展示成品并结束本轮。生成或展示失败时，按报告指南处理。
