# Product trend panels

Use one section per selected product. Put the product name, ASIN and observation period in its heading or subtitle. Use these blocks in order. For a focused request include the requested measures only.

| Panel | Report block and series |
|---|---|
| Monthly sales | `chart`, line. Use one label per month and unit “units, purchase lower bound”. Plot the selected ASIN and the identifiable parent listing on the same axis. Label each series with its ASIN. Start a new series if the parent changes. Keep a partial month separately labeled. |
| Daily price | `daily-history` with `field="price"`, the selected ASIN, requested dates and the original saved product history in `source`. Use the currency from that response. |
| Weekly estimated exposure | `chart`, line. Label each complete week by its end date and use estimated exposure points as the unit. Plot organic and sponsored exposure for the selected ASIN as separately named series. If the request asks for total exposure, use the returned total. |
| Daily category ranks | Produce both panels from the same original daily history using the [rank chart builder](scripts/rank_charts.py). Pass the report period as `--start-date` and `--end-date`. The first shows rank in the main category, the second in the subcategory. Each uses its own scale, with the category name and the direction of the ranking in view. |

For an October 2026 report run the following command, substituting the study dates for other periods: `python3 <linked script> HISTORY.json ASIN --start-date 2026-10-01 --end-date 2026-10-31 --lang zh-CN` (or `en`). Insert its JSON blocks directly into the section. The builder pairs each rank with the category recorded on that date and breaks the series when the category changes. If a level has no identified rank, keep its short availability note and show the other level.

Use the same study period across panels at each measure’s own frequency. Leave missing observations as gaps and retain measured zeroes. For a single observation show the dated value. For an unavailable measure show a short note in its place. Show each series once.
