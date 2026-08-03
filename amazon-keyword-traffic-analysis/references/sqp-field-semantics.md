# Seller Artifact Field Semantics — ABA-SQP and Amazon Ads

> Load this file whenever the user supplies an ABA-SQP or Amazon Ads screenshot, CSV, report, settings view, or pasted table.

## Provisioning contract

Load this acquisition guidance when the shared workflow requests a seller-funnel artifact as the one exact next input. Guide artifact acquisition instead of asking the user to assemble fields manually.

Request one seller report or view at a time. Do not request SQP and Ads artifacts in the same stage-end list; analyze SQP first and request Ads only through its later evidence stage when that evidence remains required.

Render the artifact request as one continuation item under the shared Stage-End Selection List Rule, with the upload action inside that item. Screenshot and CSV are format alternatives for supplying the same requested evidence, not separate list items. Name the selected view, subject, marketplace, latest completed reporting week, and target-query scope needed for the unresolved decision.

### User-facing SQP acquisition

1. Open Seller Central: `Brand Analytics → Search Analytics → Search Query Performance`.
2. For an ASIN-specific judgment, select `ASIN View`, the target ASIN, marketplace, and latest completed reporting week, then locate the target query. For a brand-level judgment, select `Brand View` instead.
3. Offer two alternatives: upload one screenshot showing the selected view/subject/period, target query, and visible funnel headers and row; or click the page's `Download` control and upload the original CSV unchanged.

Do not enumerate the full SQP schema in the request, require manual transcription, or ask for both formats. Accept pasted data when the user volunteers it. After receiving the artifact, inspect whether the `Impressions`, `Clicks`, `Cart Adds`, `Purchases`, and `Search Query Volume` fields required for the named decision are present; include one exact missing-field continuation in the stage-end list only if its absence blocks the conclusion.

One completed week is sufficient for the initial current-period funnel judgment. Do not default to requesting 4–8 weeks. Request additional completed weeks only when the user asks for trend/stability or when the first week's visible event counts are too sparse or atypical to support the named conclusion; explain that specific reason and retain the same subject/query scope.

### Later Ads acquisition

Do not request Ads data together with SQP. First analyze the SQP artifact. Use the following Ads acquisition path only when the shared workflow subsequently requests an Ads artifact as the one exact next input for a remaining profitability, bid, budget, match-type, or allocation question:

1. Open the Amazon Ads advertising console and switch to the requested marketplace/account profile.
2. In the standard sponsored-ads interface, open `Measurement & Reporting → Sponsored ads reports → Create report`. If the account has migrated to unified reporting and those labels are absent, use `Reporting → Create report` instead.
3. Select `Sponsored Products` as the ad product/campaign type and `Search term` as the report type, then set the exact requested start and end dates. Use the summary/aggregate time unit when that control is shown unless the named question requires daily rows.
4. Run the report. After its status is complete, download the original CSV from the reports list and upload it unchanged.

If downloading is inconvenient, accept one screenshot containing the CSV/report headers and the complete target search-term row. Inspect the artifact's available Search term, Match type, Impressions, Clicks, Spend, Orders, Sales, CPC, CVR, and ACOS/ROAS fields internally; do not make that schema the user's manual checklist.

A Search term report supplies attributed performance evidence; it does not normally establish the current bid, effective bid after placement adjustments, bidding strategy, campaign budget, spend ceiling, or product unit economics. When the named decision requires one of those fields, accept the smallest later targeting/campaign settings view or export and seller-provided economics that exposes the missing identity. Do not infer a current control setting from CPC or infer profit from attributed sales.

## Amazon Ads schema identity

Record this identity tuple before extracting or combining Ads values:

`source → account profile → marketplace → ad product → report/view → campaign → ad group → target → search term → match type → attribution scope → period → time unit → currency → field → unit → denominator`

- A search term is the shopper query that received attributed performance. A keyword/product target is the advertiser-controlled target. They are not interchangeable even when their text matches.
- Campaign, ad-group, portfolio, placement, target, and search-term rows have different scopes. Preserve the row scope through extraction, aggregation, and conclusion.
- Preserve the report's start/end dates, time unit, currency, and returned attribution labels or window. If attribution identity is absent, describe sales/orders as report-returned attributed values and do not invent the window.
- A current settings screenshot or export must visibly identify the controlled target and its marketplace/account/campaign context. Conversation context cannot repair a cropped or ambiguous control identity.

## Amazon Ads field semantics

| Field | Measurement | Unit / denominator | Supported interpretation boundary |
|---|---|---|---|
| `Impressions` | Returned ad impressions in the row scope | impression events | Delivery volume; not shopper reach, relevance, or demand by itself |
| `Clicks` | Returned ad clicks in the row scope | click events | Click volume; not CTR without compatible impressions |
| `Spend` | Advertising cost in the report currency | currency | Attributed ad spend for the row scope; not total product cost |
| `Orders` | Report-attributed orders | order events under the returned attribution scope | Attributed order volume; not total seller orders or profit |
| `Sales` | Report-attributed sales | currency under the returned attribution scope | Attributed revenue; not contribution profit |
| `CPC` | Spend per click | `Spend ÷ Clicks` | Average click cost in the row scope; not the current bid or clearing rule |
| `CVR` | Attributed orders per click | `Orders ÷ Clicks` | Ads-attributed click-to-order rate for the row scope |
| `ACOS` | Spend relative to attributed sales | `Spend ÷ Sales` | Advertising cost ratio within the returned attribution scope; not profit margin |
| `ROAS` | Attributed sales relative to spend | `Sales ÷ Spend` | Attributed revenue multiple within the returned attribution scope; not profit multiple |
| Current bid / budget | Visible advertiser control setting | report currency per click or per day, as labeled | Current configured control only; it is not the effective CPC or a recommended value |

### Ads denominator and aggregation rules

1. Use a returned rate only with its visible row scope and attribution context. When deriving a rate, label the formula and use compatible non-null numerators and denominators from the same scope and period.
2. Do not average row-level CPC, CVR, ACOS, or ROAS values to form a combined result. Sum compatible numerators and denominators first, then recompute the rate.
3. A zero or missing denominator makes the corresponding derived rate unavailable. Do not replace it with zero, infinity, a default, or a category benchmark.
4. Do not combine currencies, marketplaces, attribution scopes, ad products, time units, or overlapping rollups. Do not sum a campaign total together with its child rows.
5. Keep search-term performance separate from target settings. CPC does not reveal the current bid, and a campaign budget does not reveal how spend should be allocated among targets.

### Ads economics and control boundaries

- Ads impressions, clicks, spend, attributed orders, attributed sales, CPC, CVR, ACOS, and ROAS support advertising-performance observations only within the preserved report scope.
- Product profitability requires seller-supplied unit economics that cover the material revenue adjustments, Amazon/referral and fulfillment fees, product and inbound costs, promotions, returns or other applicable costs, or a seller-provided break-even/target ACOS or ROAS explicitly grounded in those economics.
- Bid-control identity is incomplete unless the exact current bid, bidding strategy, material placement adjustments, and controlled target are visible in one compatible scope. None of those fields by itself encodes a recommended bid.
- Budget-control identity is incomplete unless the exact current budget, spend and budget-pacing scope, and relevant campaign/portfolio constraints are visible in one compatible scope. None of those fields by itself encodes a recommended budget or allocation.
- No universal click, order, spend, or date threshold is defined here. Sparse, zero-denominator, newly launched, promotion-distorted, stockout-affected, or otherwise atypical observations limit sufficiency; they never authorize a guessed number.

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
