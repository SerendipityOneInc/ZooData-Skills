# Arrange the selected comparison

| Task | Content in reading order |
|---|---|
| Profile one competitor | Identify the product. Cover its selling points, price, recent purchases, traffic sources and recurring buyer feedback. |
| Recent monthly purchases | Use one comparison table. Show adjacent rows for the selected ASIN and its parent, with one purchase lower-bound column in units per calendar month. Put unavailable months in their cells. Leave headline cards empty. |
| Monitor competitor changes | Identify the ASIN and observed period. List the changed field, before and after values by date. Briefly distinguish fields with no observed change from fields lacking comparable observations. |
| Find comparable products | Name the target and the selection basis. Show each candidate's name, ASIN and reason for inclusion in one shortlist. |
| Compare competitors | Introduce the compared products and the main difference. Show current commercial differences, traffic sources and changes over time. Add a same-theme feedback comparison for a deep study. |
| Compare a specific aspect | Answer the question, then show the comparable observations supporting it. For a trend, identify the period and show the series. |
| Find evidence for differentiation | Start with the buyer need or use case. Pair the observed product or page difference with the relevant buyer feedback and identify which product each finding describes. |

For monitoring with a saved daily history response, run the [change summary](../../datas/product-history/summarize_changes.py) with `response.json ASIN startDate endDate` followed by the requested fields (`title`, `imageUrl`, `price`). Use its dated differences and per-field coverage to fill the monitoring table directly. The original response contains `data.asin` and `data.context` with `granularity=day`, `requestedDateFrom` and `requestedDateTo`. For seller-provided excerpts, compare the dated observations directly. For title and main image, a prior event may supply the comparison baseline. Show changes observed within the requested period. A null count means the available values cannot establish a comparison.

1. Include specifications alongside the comparison they affect. Omit unused sections. Keep an unavailable measure visible when it prevents answering part of the question.
2. End an overall comparison with one side-by-side product card per ASIN in a single `profiles` block. Name the product and ASIN. Label its relative strengths and weaknesses and give the decisive evidence for each. Keep only supported judgments, even if a card has evidence for one side only. A focused comparison or single-product teardown ends with its last relevant finding.

For each HTML report, set the top-level `task` to the selected workflow task: `teardown`, `monthly-purchases`, `monitoring`, `discovery`, `comparison`, `focused-comparison` or `differentiation`, respectively, in the order of the task table above.

## First screen and evidence for a single-product teardown

1. Identify the product, ASIN and marketplace in the header. Answer the most important questions with two to four headline cards: use the business topic as the label, a short finding as the main value and one sentence of evidence with its period as the note. Put detailed coverage beside the measure it describes.
2. Title each section with its finding. Use a single `daily-history` block for price, with `field="price"`, the selected ASIN and the requested price observation dates. Point `source` to the original saved products/history JSON response. The renderer aligns the daily observations and computes observed changes. If arrays differ in length, recover the original response before delivery. If daily observations cannot be obtained, state the gap in that section. Chart monthly purchases separately and label the months actually covered. Plot the selected variant and its full listing (all variants including this one) on the same month axis. Keep missing months as gaps and different parent ASINs as separate series. If no listing total is available, plot the available variant values and label the listing total unavailable. For a single observed price show the date and price.
3. When a page claim and buyer feedback concern the same specific feature, discuss them together. Identify the sample for praise and problems; review themes can overlap. Quote only retrieved review text. Develop each headline finding with new evidence.
4. When a trend could lead the reader to a different business conclusion in isolation, place a `callout` beside it. State what the comparison establishes and, if material, where that conclusion stops. Replace the corresponding explanatory paragraph with the card. Use a descriptive section heading when the card carries the judgment.
