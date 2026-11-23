# Seller report and cost definitions

## Identify report scope

1. Analyze SQP, advertising and cost records supplied by the user; do not assume direct access to the seller account.
2. Retain the report's marketplace, brand or ASIN view, period, row dimensions and attribution window. If a cropped report omits information needed for the analysis, identify the specific missing context instead of guessing it.

## Interpret SQP data

1. Search Query Volume counts queries; impressions, clicks, cart adds and purchases count events at their respective stages.
2. Brand or ASIN stage share = that subject's event count at the stage / total events at the same stage in the selected view. Query volume is not that denominator.
3. When comparing stage shares, retain each stage's subject and total counts. If counts are absent, keep them missing rather than inferring them from another stage.
4. SQP alone does not supply advertising spend, bids or costs; do not use its funnel counts to calculate CPC, ACOS, ROAS or profit.

## Interpret advertising data

1. Distinguish shopper search terms from advertiser-controlled keywords or product targets. Retain campaign, ad group, placement and match type, aggregating at the report's stated grain without adding summary rows to their detail rows.
2. Attributed sales are revenue, not profit; CPC is a measured cost per click, not the current bid.

| Metric | Formula |
|---|---|
| CPC | Spend / clicks |
| CVR | Attributed orders / clicks |
| ACOS | Spend / attributed sales |
| ROAS | Attributed sales / spend |

## Interpret costs and targets

1. Distinguish quoted, estimated and incurred costs, and whether each amount is per unit or a period total.
2. Unit contribution = net realized price minus landed cost, marketplace and fulfillment fees, acquisition cost, and expected returns or allowances. State the included costs and do not deduct an item twice. If material costs are missing, label the result a calculation from known costs rather than complete profit.
3. Contribution margin = unit contribution / net realized price; calculate it only when net realized price is positive.
4. Budgets and target ACOS or ROAS are constraints, not inputs representing actual spend, revenue or profit.
