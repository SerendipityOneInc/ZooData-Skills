# Amazon US keyword research

## Select the task before acquiring data

| Seller request | Instructions to open |
|---|---|
| Expand a seed into related terms and group them by search intent | Open the [related-keyword method](../../datas/keyword-expansion/definition.md) before the first query. Use each seller-specified seed once for the first page. Preserve that seed across pages. Treat variations found in the results as candidates. |
| Understand or compare specified terms on demand, competition or seasonality | Open the profile and comparison route in [research methods](methods.md). |
| Study changes in demand or examine specific weeks | Open the demand trend route in [research methods](methods.md). |
| Identify a specified ASIN's terms or assess visibility on named terms | Open the ASIN route in [research methods](methods.md). |

1. Reuse matching supplied records. Apply the [query rules](../../../contract/query.md) to new reads and the [evidence rules](../../../contract/evidence.md) to the results.
2. For expansion, follow the grouping method in [research methods](methods.md). If the seller also requests priorities, compare relevant candidates against the requested criterion. Clarify the criterion only when it would change the selection.

## Deliver the report

1. After the data arrives, open the selected [report outline](report-outline.md) and the [report guide](../../../tools/report/definition.md). Build the report input for that task. For a keyword list, populate each row from the candidate record, including the baseline measures named in the outline.
2. Unless the seller explicitly requests another format, run the [shared HTML generator](../../../tools/report/scripts/render_report.py) on that input and verify the HTML exists. Both the expert and standalone workflow deliver one file.
3. Present the finished file using the [HTML handoff](../../../contract/report.md#hand-off-the-html-report) and finish the turn. If generation or presentation fails, follow the report guide's recovery procedure.
