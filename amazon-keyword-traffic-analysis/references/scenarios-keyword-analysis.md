# Single Keyword Analysis

> Load this file for single-keyword evaluation.

## Contents

- [Inputs](#inputs)
- [Target-Keyword Decision Journey](#target-keyword-decision-journey)
- [Task Constraints](#task-constraints)
- [Analysis Dimensions](#analysis-dimensions)
- [Decision Logic](#decision-logic)
- [Output Template](#output-template)

## 2. Single Keyword Analysis

> Trigger includes natural seller questions such as "Is yoga mat worth focusing on in the US, and how hard would it be for a new product to enter?", as well as "keyword deep dive" / "is this keyword worth targeting" / "single keyword analysis".

### Inputs

- required: target keyword
- optional: marketplace
- optional: weekly snapshot date
- optional: trend lookback window, default 8-12 weeks when available
- date rule: if a keyword endpoint needs `date` or `dateTo`, prefer T-1 or earlier; avoid current-date lookup unless explicitly requested

### Target-Keyword Decision Journey

Use this staged sequence only for a target-keyword decision that naturally progresses from market screening to product-specific operating strategy. It is not a universal workflow for every keyword scenario.

| Stage | Available input and evidence | Maximum conclusion | End-of-stage action |
|-------|------------------------------|--------------------|---------------------|
| 1. Keyword market screening | Target keyword, marketplace, market profile, 8–12 week trend, and only the SERP evidence required for product type / intent | Whether the term merits ASIN-level validation, new-product entry difficulty, and a provisional `Core` / `Secondary` / `Observe` role | Ask for the user's ASIN. Do not request SQP yet. |
| 2. ASIN × target keyword diagnosis | Stage 1 evidence plus observed ASIN relevance, price/rating/reviews/sales basis, organic/ad positions, traffic structure, changes, and market-relative barrier | Current `Defend` / `Expand` / `Observe` / `Avoid` posture, evidence-supported constraint hypotheses, and unresolved questions | Generate a candidate pool, but do not recommend unvalidated candidates. |
| 3. Candidate market-profile validation | Candidate terms from ASIN traffic, target-term extensions, attributes/scenes, user-provided SQP queries, or competitor terms; batch market profiles | Preliminary `Priority test` / `Selective test` / `Harvest` / `Observe only` / `Avoid` validation tiers | Ask for ABA-SQP; ask for Ads search-term data only when profitability or exact ad-budget decisions are requested. |
| 4. Seller data request | Clear list of required ABA-SQP and optional Ads fields | Explain the remaining decision gaps without strengthening prior conclusions | Wait for screenshot, CSV, or pasted fields. |
| 5. Seller-real calibration | Seller ABA-SQP funnel and, for financial execution, Ads performance | Final keyword groups and evidence-authorized operating actions; exact budget/bid/spend and continue/raise/lower/pause conditions require the relevant Ads fields and Evidence-to-Action authorization | State calibrated decisions and monitoring conditions within the supplied fields. |

#### Journey Routing Rules

- Start at Stage 1 when the user asks whether a target keyword is worth focusing on or how difficult new-product entry would be, even when no technical metrics are named.
- At Stage 1 assess demand scale, 8–12 week trend, ad activity, Top-20 organic entry difficulty, supply saturation, brand concentration, head-product barrier, and SERP product type / buying intent.
- If a metric dimension is unsupported, mark it unavailable rather than forcing a same-source data-layer call that cannot add different evidence.
- The Stage 1 answer must not contain final product priority, budget allocation, or bid actions. Its only proactive request is the ASIN.
- At Stage 2 distinguish observed facts from possible click/conversion issues. Without seller funnel data, describe click or conversion weakness as an unresolved question, not a measured fact or a generic cause list.
- At Stage 2, a funnel weakness identifies the relevant handoff but does not explain its cause. Apply `execution-guide.md § Evidence-Seeking Diagnosis Protocol` to obtain the smallest discriminating evidence before forming hypotheses, then apply `§ Evidence-to-Action Protocol` before recommending any specific asset or operating change.
- Treat image evidence according to fidelity. A thumbnail supports only thumbnail-level observations; an image URL/change event proves only that the image changed. Require direct inspection of each targeted asset before proposing an asset-level test or change.
- Candidate generation and candidate recommendation are different operations. Every candidate must pass Stage 3 batch market-profile validation before appearing in a recommended validation tier.
- Candidate priority formula: `product fit × current ASIN performance × keyword market profile`. Title relevance or an occasional observed position is not sufficient by itself.
- Stage 3 compares at least demand scale, ad activity, Top-20 organic entry difficulty, supply saturation, brand structure, head-product barrier, and Top-3 concentration when covered.
- Do not ask for ABA-SQP until Stages 2 and 3 are complete, unless the user supplied it earlier or explicitly requests an immediate seller-real diagnosis.
- If the user supplies later-stage inputs in the initial request, execute the supplied stages without an artificial pause. If the user requests only one stage, honor that boundary.
- At Stage 5, separate keyword-role calibration from causal diagnosis. SQP may support a role such as `Defend + Diagnose`, controlled validation, or no current scale support without explaining why the weak handoff occurred.
- Do not open a post-click cause branch merely because SQP located a weak handoff. Open it only if the user asked why or if the requested action depends on the cause; then apply the Diagnostic Closure Gate and continue to discriminating evidence before finalizing.
- When a post-click cause branch is opened, acquire evidence only through ZooData tools: use the matching data API first (for example `realtime/product` for live ASIN/product fields); for a known page URL use ZooData WebTools `/scrape`, escalating to `/scrape-interactive` only when rendering or actions are required. Never open an external interactive browser, navigate directly to Amazon outside ZooData, or use public web search; if ZooData cannot obtain the evidence, request the minimum seller-provided screenshot/report instead.
- If the only next evidence requested is Ads search-term performance, limit the unresolved question to Ads economics, traffic precision, and order attribution. Do not also name detail-page, price, promotion, fulfillment, variation, or asset explanations that the requested Ads report cannot distinguish.
- If causal diagnosis is outside the current run, state only the supported funnel fact and operating implication—for example, `clicks occurred but purchases were not observed, so retain controlled validation and do not scale yet`—then stop that branch.

#### Journey Conclusion Gate

| Stage | Required conclusion label | Allowed | Forbidden |
|-------|---------------------------|---------|-----------|
| 1 | `Market-screen conclusion` | Market attractiveness, relative entry difficulty, provisional role, risks, and whether ASIN validation is worthwhile | Final focus/do-not-focus decision, product fit, budget, bid, expansion, pause, profitability, or conversion claims |
| 2 | `ASIN-observation preliminary conclusion` | Observed fit/position/traffic posture, current posture label, evidence-supported constraint hypotheses, unresolved questions, candidate pool, and evidence-seeking actions authorized by the observed problem domain | Generic unsupported cause lists, final keyword priority, unvalidated candidate recommendations, uninspected asset changes, budget/bid changes, profitability, or measured click/conversion claims without seller data |
| 3 | `Candidate-validation preliminary conclusion` | Market-profile-validated ranking for controlled seller-funnel validation | Final expansion list, fixed budget split, bid changes, pause/negative decisions, profitability, or unconditional GO/NO-GO |
| 4 | `Awaiting seller evidence` | Decision gaps and minimum required seller fields | Repeating or strengthening prior conclusions while waiting |
| 5 | `Final calibrated conclusion` | Final keyword groups, budget and bid/spend actions, validation rules, and decision thresholds | Profit or ACOS/ROAS claims when Ads performance is absent |

Before Stage 5, use bounded language such as `merits the next validation stage`, `controlled-test candidate`, `awaiting SQP/Ads before changing budget or bids`, `downgrade candidate pending validation`, or `current evidence does not support advancing`.

If evidence required for the requested decision is missing, end with exactly three logical parts: current-stage conclusion, unresolved final decision, and required next evidence. Do not introduce unrelated unresolved diagnoses; never manufacture closure merely because the user asked a yes/no question.

### Task Constraints

- Minimum evidence is judgment-specific, not a fixed pair of data endpoints. Use metric-layer `keywords/market-profile` first for weekly market judgment and `keywords/search-results-metrics` when live for SERP structure judgment.
- Use `keywords/detail` only when `market-profile` is unavailable or a named inference requires raw snapshot fields that the metric contract omits. Do not call it merely because one profile dimension is unsupported/unavailable.
- Use raw `keywords/search-results` when the SERP metric is unavailable or the inference requires product/placement rows; do not call it merely to confirm a sufficient SERP metric.
- Prefer `keywords/trend-profile`. Use raw `keywords/trend` only when the Agent needs weekly points or fields omitted from the profile; otherwise do not make strong demand-direction claims.
- Use one batch call when comparing multiple target keywords; read each `data.items[]` status independently
- If a metric returns an unsupported dimension because its calculation inputs are missing, mark that conclusion unavailable. Only descend when the data contract provides different evidence needed for another valid inference.
- Page-1 product rows must come from `keywords/search-results`; aggregate SERP structure should come from `keywords/search-results-metrics` when live.
- `products/search` is allowed only as broader market context when the user explicitly asks for that broader view
- Interpret `marketProfile` only for items with `status=available`. Read scores through returned `context.scoringSpec` and each dimension's `supported`, `calculationStatus`, `unsupportedReason`, `level`, and `levelEvidence.score.{value,direction}`. Treat `marketCharacteristics.volatility` and `annualSeasonality` as independent evidence; never turn either into a trend series, root cause, or strategy output.
- `status=not_found` means the keyword was not observed and does not qualify for a recommendation tier. It is not evidence of low demand. A batch HTTP 500 is a service failure; do not silently fan it out into repeated single-keyword calls.
- The analysis may use any efficient call pattern, but the final verdict must stay within the available evidence scope
- ZooData evidence is estimated search/exposure/visibility data, not the user's ASIN-specific ABA Search Query Performance funnel. The first reply is a market-level directional judgment, not a final keyword-value or budget judgment.
- After the market screening, ask only for the user's ASIN. Do not request ABA-SQP in the first reply.
- If the conversation already contains an ASIN, continue with the ASIN × keyword stage. Generate candidate terms when useful, but do not recommend them until they pass a batch `market-profile` validation.
- Ask for ABA-SQP only after the ASIN diagnosis and candidate validation are complete. If the user already provided SQP, use impressions, clicks, cart adds, purchases, and their shares to calibrate the final decision.
- Apply the Journey Conclusion Gate before drafting the verdict. Stage 1 may decide only whether ASIN-level validation is justified; it must not present a final focus/do-not-focus operating decision.

### SERP Source Rule

- When the user asks what products are showing on the first page, answer from `keywords/search-results` first
- Do not treat `keywords/search-results` as "only a SERP structure endpoint"; it already includes listing-level product fields
- Do not append `products/search` by default for this question
- Use `products/search` only if the user also asks for market-wide best sellers, sales distribution, price-band distribution, or a broader market view that goes beyond the observed keyword SERP

### Analysis Dimensions

| Dimension | Questions |
|-----------|-----------|
| Demand | Is the search volume meaningful enough? |
| Trend | Is volume stable, rising, or weakening? |
| Competition | Is the keyword ad-heavy and crowded? |
| Market profile | What do the covered demand, concentration, ad activity, entry difficulty, saturation, brand, and organic benchmark dimensions show? |
| SERP intent | Do current results match the user's product intent? |
| Organic room | Is there room outside the entrenched leaders? |
| Launch fit | Better for discovery, exact defense, or long-tail harvest? |

Stage 1 should cover these operator-facing questions even when the user does not name the metrics explicitly:

1. How large is demand?
2. What happened over the last 8–12 weeks?
3. How active is advertising?
4. How hard is Top-20 organic entry?
5. How saturated is supply?
6. How concentrated are brands and Top-3 traffic?
7. What are the review/rating/sales barriers among head products?
8. What product types and buying intents dominate the SERP?

Do not report planned `demandLifecycle`, `competitionMetrics`, or `entryEvidence` as API data unless the corresponding metric endpoint actually returned them.

### Decision Logic

- Merits ASIN-level validation:
  demand is real, trend is not deteriorating, and the SERP is still contestable; describe only a provisional core, secondary, or observation role
- Merits selective validation:
  demand is good but competition is heavy, or intent fit is narrower
- No current support for advancing:
  demand is weak, trend is poor, or SERP mismatch is strong; this is not an unconditional final rejection
- Do not call a keyword definitively profitable, high-converting, fully validated, or ready for a final budget unless the user provides SQP or equivalent first-party conversion data

### Output Template

```markdown
# Keyword Analysis — [Keyword]

> Data is based on ZooData keyword snapshots as of [date]. Weekly search and traffic metrics are sampled observations, not exact Amazon Ads billing data. This analysis is for reference only and should not be the sole basis for business decisions.
> ZooData estimates exposure/search/visibility. This first-stage report is a market-level directional judgment, not a product-specific or final budget decision.

## [Localized Data Notes title]
[State that this is a market-level directional judgment based on ZooData market, trend, and observed SERP evidence. It is not yet a product-specific or final budget judgment. Do not request SQP here.]

## Market-screen Conclusion
- Merits ASIN-level validation: [yes / selectively / observe / no current support]
- New-product entry difficulty: [low / medium / high / unavailable]
- Provisional market role: [Core candidate / Secondary candidate / Observe]
- Not yet decided: [product-specific priority, final expansion decision, budget]

## Findings
- Demand: [📊 / 🔍]
- Trend: [📊 / 🔍]
- Competition: [📊 / 🔍]
- SERP structure: [📊 / 🔍]
- Product type and buying intent: [📊 / 🔍]
- Recommended usage scene: [💡]

## Next Step
[Ask for the user's ASIN so the next stage can compare product fit, current organic/ad positions, traffic structure, and market-relative barrier. Do not give final budget advice and do not ask for SQP yet.]

## API Usage
| Endpoint | Calls | Credits |
|----------|-------|---------|
| [endpoint] | [call count] | [credits consumed] |
| Total | [sum of calls] | [sum of credits] |

Do not omit this section. Use the markdown table format above, not bullet lists, and include the `Total` row. Extract from `meta.creditsConsumed` per response. End with `Credits remaining: N` using the latest `meta.creditsRemaining`. Use `not returned` when credit fields are absent.
```
