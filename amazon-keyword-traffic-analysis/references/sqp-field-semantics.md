# ABA Search Query Performance Field Semantics

> Load this file whenever the user supplies an ABA-SQP screenshot, CSV, or pasted table.

## Provisioning contract

The active scenario requests this data only when seller-funnel calibration is needed. Guide the user through artifact acquisition instead of asking them to assemble fields manually.

Once the active scenario determines that seller-funnel calibration is needed, state the request directly in a separate next-input section and end with an upload action. The screenshot/CSV formats below are alternatives for how to provide the artifact, not a choice about whether to continue. Do not introduce the request with optional wording such as `if you want`, `if needed`, or `如需`. Name the selected view, subject, marketplace, latest completed reporting week, and target-query scope needed for the unresolved decision.

### User-facing SQP acquisition

1. Open Seller Central: `Brand Analytics → Search Analytics → Search Query Performance`.
2. For an ASIN-specific judgment, select `ASIN View`, the target ASIN, marketplace, and latest completed reporting week, then locate the target query. For a brand-level judgment, select `Brand View` instead.
3. Offer two alternatives: upload one screenshot showing the selected view/subject/period, target query, and visible funnel headers and row; or click the page's `Download` control and upload the original CSV unchanged.

Do not enumerate the full SQP schema in the request, require manual transcription, or ask for both formats. Accept pasted data when the user volunteers it. After receiving the artifact, inspect whether the `Impressions`, `Clicks`, `Cart Adds`, `Purchases`, and `Search Query Volume` fields required for the named decision are present; request one missing field only if its absence blocks the conclusion.

One completed week is sufficient for the initial current-period funnel judgment. Do not default to requesting 4–8 weeks. Request additional completed weeks only when the user asks for trend/stability or when the first week's visible event counts are too sparse or atypical to support the named conclusion; explain that specific reason and retain the same subject/query scope.

### Later Ads acquisition

Do not request Ads data together with SQP. First analyze the SQP artifact. Only if the remaining question concerns profitability, bids, budgets, match types, or allocation, give the user this complete acquisition path:

1. Open the Amazon Ads advertising console and switch to the requested marketplace/account profile.
2. In the standard sponsored-ads interface, open `Measurement & Reporting → Sponsored ads reports → Create report`. If the account has migrated to unified reporting and those labels are absent, use `Reporting → Create report` instead.
3. Select `Sponsored Products` as the ad product/campaign type and `Search term` as the report type, then set the exact requested start and end dates. Use the summary/aggregate time unit when that control is shown unless the named question requires daily rows.
4. Run the report. After its status is complete, download the original CSV from the reports list and upload it unchanged.

If downloading is inconvenient, accept one screenshot containing the CSV/report headers and the complete target search-term row. Inspect the artifact's available Search term, Match type, Impressions, Clicks, Spend, Orders, Sales, CPC, CVR, and ACOS/ROAS fields internally; do not make that schema the user's manual checklist.

## SQP schema identity

Record this identity tuple before extracting values:

`source → view → selected subject → search query → marketplace → period → funnel stage → field label → unit → denominator`

- `Brand View` reports the selected brand's owned counts/shares. It does not identify one ASIN's performance.
- `ASIN View` can support a selected-ASIN judgment only when the target ASIN is visibly selected or unambiguously identified in the export.
- If the view or selected subject is cropped, ambiguous, or inconsistent with the user's requested subject, do not infer it from conversation context. State the visible scope and request the missing header only when subject attribution is necessary.
- Preserve the exact displayed owner noun. Never rewrite `Brand Count/Share` as `ASIN Count/Share`, or the reverse.

## Field hierarchy and semantic mapping

Repeated child labels such as `Total Count` have no safe standalone meaning. Always retain their parent stage on first mention.

| Exact field path | Measurement | Unit / denominator | Supported interpretation boundary |
|---|---|---|---|
| `Search Query Volume` | Query occurrences in the selected reporting scope | query count; no funnel denominator | Demand count for the query; keep distinct from product-level funnel events |
| `Search Funnel → Impressions → Total Count` | All impression events at the impression stage | impression events | Funnel-stage total within the selected row/report scope, not an owned-subject count |
| `Search Funnel → Impressions → Brand Count` | Impression events owned by the selected brand | impression events | Brand-level impression count |
| `Search Funnel → Impressions → Brand Share` | Selected brand's share of impression events | `Brand Count ÷ Impressions Total Count` | Brand-level impression share within the same query/report scope |
| `Search Funnel → Clicks → Total Count` | All click events at the click stage | click events | Funnel-stage total within the selected row/report scope |
| `Search Funnel → Clicks → Brand Count/Share` | Selected brand's click count/share | click events; share denominator is click-stage Total Count | Brand-level click evidence, distinct from click-through rate |
| `Search Funnel → Cart Adds → Total Count` | All cart-add events at the cart-add stage | cart-add events | Funnel-stage total within the selected row/report scope |
| `Search Funnel → Cart Adds → Brand Count/Share` | Selected brand's cart-add count/share | cart-add events; share denominator is cart-add Total Count | Brand-level cart-add evidence, distinct from conversion rate |
| `Search Funnel → Purchases → Total Count` | All purchase events at the purchase stage | purchase events | Funnel-stage total within the selected row/report scope |
| `Search Funnel → Purchases → Brand Count/Share` | Selected brand's purchase count/share | purchase events; share denominator is purchase Total Count | Brand-level purchase evidence, distinct from revenue or customer count |

For ASIN View, apply the same funnel-stage meanings but quote the exact ASIN-owned label shown in the screenshot/export. Do not invent an `ASIN Count` or `ASIN Share` label when it is not visible.

## Output label construction

Build localized labels from schema roles, in this order:

1. `Search Query Volume` → localized **search-query count/volume**. The measurement noun is query occurrence.
2. `<Funnel Stage> → Total Count` → localized **<stage> total event count**. The measurement noun comes from the parent stage: impression, click, cart add, or purchase.
3. `<Funnel Stage> → <Owner> Count` → localized **<owner> <stage> event count**.
4. `<Funnel Stage> → <Owner> Share` → localized **<owner> <stage> share**.

Query, marketplace, report, and period are scope qualifiers. State them in the title, note, or identity context; do not inject them into the measurement label. In particular, an event total scoped to one query remains an impression/click/cart-add/purchase event total—it does not become a query count.

When funnel stages are table rows, use the localized semantic header pattern:

`Funnel stage | Stage total events | Owned-subject events | Owned-subject share`

The row supplies the event noun, so each value remains typed by its stage. Display `Search Query Volume` separately from this funnel-event table.

## Denominator and comparison gate

1. Verify a displayed share against `owned count ÷ same-stage Total Count` when both values are readable; allow for display rounding.
2. Never divide a funnel count by `Search Query Volume` unless interpreting a separately named rate whose documented denominator is query volume.
3. Compare `impression share → click share → cart-add share → purchase share` only within the same view, subject, query, marketplace, and period.
4. Describe a share increase/decrease as a relative handoff pattern. It may locate where the subject gains or loses share versus the query-level funnel, but it does not identify the cause.
5. Keep the owned event count visible beside every interpreted share. Low counts limit stability regardless of the displayed share level.

## Interpretation boundaries

- Use the complete path to choose the localized measurement noun. Do not translate or interpret a repeated child label independently.
- Keep query counts and impression/click/cart-add/purchase event counts as different units even when they appear in the same row.
- Keep view ownership and selected-subject ownership unchanged through extraction, translation, tabulation, and conclusion.
- A share change across funnel stages describes relative share movement only. Product relevance, asset quality, conversion causality, and operating actions require separate evidence.
- Keep the owned count beside its share when judging stability; sparse counts limit confidence even when the displayed share is large.
- SQP funnel counts/shares do not provide CPC, ACOS, ROAS, profitability, bid, or budget evidence.

## Output rule

On first use, label values with full paths or the stage-relative table pattern above. Headers must preserve owner, measure, and unit; scope qualifiers cannot replace the measurement noun. A localized shortcut is allowed only after the complete field identity has been established and remains unambiguous in context.
