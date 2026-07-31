# Execution Guide — Amazon Keyword Intelligence

This file defines the shared execution protocol for every keyword scenario.

## Contents

- [Authority and routing](#authority-and-routing)
- [Structured Field Identity Gate](#structured-field-identity-gate)
- [User-Facing Language Rule](#user-facing-language-rule)
- [Retrieval Progress Updates](#retrieval-progress-updates)
- [Execution Mode](#execution-mode)
- [Two-Pass Metric Protocol](#two-pass-metric-protocol)
- [Evidence-Level Progression](#evidence-level-progression)
- [Stage Handoff Closure Gate](#stage-handoff-closure-gate)
- [Evidence-Seeking Diagnosis Protocol](#evidence-seeking-diagnosis-protocol)
- [Evidence-to-Action Protocol](#evidence-to-action-protocol)
- [Quick Mode Output](#quick-mode-output)
- [Full-Mode Checklist](#full-mode-checklist)
- [Evidence Handling Rules](#evidence-handling-rules)
- [General Rules](#general-rules)
- [Output Rules](#output-rules)
- [Monitoring Cadence Suggestion](#monitoring-cadence-suggestion)

## Authority and routing

Use this guide for all cross-scenario rules. Follow the workflow in this order:

`question → evidence plan → retrieval → field interpretation → analysis → evidence-bounded conclusion → next evidence or action`.

- `SKILL.md` supplies trigger and non-negotiable boundaries.
- This guide supplies the shared workflow, conclusion authority, diagnostic/action gates, and output rules.
- Scenario files are downstream applications. They select suitable capability combinations, stage transitions, and report shapes only, and must align upward with this guide plus the applicable API and field-semantic references. They do not create separate evidence thresholds, scoring formulas, action authority, acquisition procedures, or exceptions to a top-level specification.
- `reference.md` is authoritative for API facts. If an endpoint contract conflicts with prose, use the documented contract and narrow the conclusion.
- When instructions conflict, apply the stricter evidence/action limit. Never average conflicting metrics or recover an API capability from non-equivalent evidence.

## Structured Field Identity Gate

Before translating or interpreting an API field, screenshot, CSV, or report field:

1. Resolve `(source, view, selected subject, metric path, field, unit, denominator, grain, period)`; leave unreadable components unknown.
2. Preserve the full metric path and ownership. Do not reassign market, brand, ASIN, query, placement, or campaign evidence to another subject.
3. Translate the documented measurement, not a presumed business meaning. Verify compatible denominators before comparing or calculating rates; label each derivation with its formula.
4. Treat cross-stage or cross-metric patterns as bounded relationships, never as causes or operating actions without separately authorized evidence.

## User-Facing Language Rule

Localize all generated headings, labels, human-readable status labels, table headers, disclaimers, and fixed phrases to the user's language. Preserve source spelling for exact identifiers such as endpoint paths, fields, enum values, ASINs, query strings, brands, product names, placement codes, and established abbreviations. When reporting a source enum such as `status=empty`, retain the exact enum value and add a localized explanation when needed; do not translate the value inside the identifier. Before sending, remove template-language leakage.

## Retrieval Progress Updates

- When a progress update is needed, use one short, natural sentence in the user's language. State only the subject and business question currently being examined; include marketplace or period only when it helps the user understand the scope.
- Do not mention tools, commands, endpoints, batching, call-count optimization, schemas, field names, support/calculation states, validation mechanics, confidence routing, internal safeguards, or output-authority limits in progress messages.
- Do not expose partial judgments, candidate verdicts, internal reconciliation, stage-transition deliberation, future seller-calibration paths, or a list of things the answer will not do. Reserve all such judgment and necessary evidence boundaries for the completed `evidence → analysis → conclusion` report.
- Do not narrate every retrieval call. Send another progress sentence only when work is still continuing long enough to require an update or when the user-facing task state materially changes.
- Natural example before retrieval: `我先看看这 6 个词在美国站最近一周的市场表现。`
- Natural example while continuing: `数据已经拿到，我正在整理这 6 个词之间的差异。`

## Execution Mode

| Task Type | Mode | Behavior |
|-----------|------|----------|
| Single lookup such as one snapshot field | Quick | Return the key metric with light interpretation |
| Expansion, full keyword judgment, reverse ASIN, keyword traffic diagnosis | Full | Run only the evidence calls justified for the current question and output API usage |

## Two-Pass Metric Protocol

Every full-mode judgment uses two logical passes:

1. **Route and retrieve:** translate the user's question into claim-sized evidence needs, map each need to the primary endpoint/field, and retrieve the smallest sufficient response. Do not draft the verdict or assign a strategy/test label in this pass.
2. **Interpret and judge:** inspect the actual response status, period, coverage, and fields; load the relevant metric-semantic reference; map every candidate claim to its exact returned evidence and forbidden stronger inference; reconcile metrics that inform the same question; only then apply conclusion authority and draft the answer. Documentation alone is never a metric result.

The semantic references are loaded progressively: `metrics-market-profile.md` for market dimensions, `metrics-trend-profile.md` for trend dimensions, and `serp-and-rollover.md` for placement/exposure/rollover questions. A second API call is not automatically the second pass. Make an additional call only when one named inference remains unresolved, another contract provides the missing evidence, and no interface failure has occurred.

## Evidence-Level Progression

Apply these rules to every full-mode scenario. Scenario files select relevant capabilities and may supply a report shape; they do not alter these rules.

| Evidence level | Evidence scope | Maximum conclusion authority |
|----------------|----------------|------------------------------|
| Market evidence | Keyword demand, trend, market profile, and SERP observations | Market attractiveness, structure, relative difficulty, and directional opportunity |
| Subject observation evidence | Market evidence plus observed ASIN, listing, placement, traffic, or timeline signals | Subject-specific fit, current posture, movement, and evidence-supported bounded hypotheses |
| Seller-real evidence | User-provided ABA-SQP funnel and, when relevant, Amazon Ads performance | Calibrated operating decisions, subject to the fields actually provided |

### Interactive Stage Gate

- Complete at most one user-decision stage per assistant turn. A stage is a unit that changes the evidence level, subject scope, candidate set, or decision authority; multiple justified evidence calls inside that one stage are allowed.
- Finish the active stage in `evidence → analysis → stage conclusion` order, followed by at most one next-step confirmation or input request when progression is needed, then stop and wait for the user. If the requested journey is complete, stop after the stage conclusion and required usage reporting without manufacturing another request. Do not call a later-stage capability before the user explicitly confirms progression or supplies the requested next-stage input.
- A broad request for a complete analysis does not pre-authorize every later stage. The user must be able to understand, adjust, or reject each stage's conclusion and candidate scope before the workflow advances.
- Keep each response focused on the current stage. Do not combine several completed stages into one long process report, narrate the full future workflow, or include future-stage evidence and conclusions. Mention only the single next action needed from the user, if any.
- When later-stage data was supplied early, retain it without interpreting it. At the current stage boundary, ask for a concise confirmation to continue with that retained input; do not ask the user to upload it again.
- A user reply such as `confirm`, `continue`, or the requested ASIN/file/list counts as stage confirmation. Do not ask for a second confirmation after the user has supplied the exact next-stage input.
- The Two-Pass Metric Protocol operates inside the active stage and does not require a user pause between retrieval and interpretation. Batch calls and other calls required to complete the same stage also remain allowed.
- Quick single-lookup tasks and multiple evidence calls that answer one unchanged decision stage are not multi-stage workflows.

### Stage Handoff Closure Gate

Apply this gate after every full-mode stage conclusion and before drafting the next-input section:

1. Classify the stage as exactly one of:
   - `complete`: the user's current decision is answered at the available evidence level; omit next input;
   - `advance`: the conclusion assigns a transition label or says a subject merits/requires a later evidence level;
   - `unresolved`: the conclusion names one exact missing evidence item needed to answer the current decision.
2. For `advance` or `unresolved`, progression is required by the conclusion itself. Render a separate localized next-input section with one direct, executable request that names the subject/scope, acquisition path when applicable, and confirmation or upload action. Then stop and wait for the user.
3. Never make a required handoff optional with `if you want`, `if needed`, `when wanted`, `如需`, or equivalent wording. Screenshot/CSV or other artifact formats may be alternatives; whether to perform the required handoff is not.
4. Keep the stage conclusion declarative and separate from the request. Do not bury the next input in the conclusion, replace the conclusion with a question, or call a pre-seller-data result a `Final calibrated conclusion`.
5. Scenario journey rows must name the observable trigger for a transition, such as a specific label, advanced candidate, or exact unresolved evidence. Vague predicates such as “when calibration is wanted/needed” are invalid.

Every full-mode scenario must explicitly inherit this gate. Scenario files may define their transition triggers and requested artifact, but may not weaken the required handoff after a trigger fires.

### General Progression Rules

- Determine the highest evidence level currently available before selecting endpoints or drafting conclusions.
- Never allow a conclusion to exceed the authority of its supporting evidence level.
- Treat all conclusions below seller-real evidence as provisional when the request concerns product-specific priority, conversion, profitability, bids, spend, or budget.
- Request only the next evidence that resolves the named decision gap. Do not expose every possible future input at once.
- Request one report or view at a time. Do not ask the user to provide SQP and Ads data in the same next-input step; inspect and analyze the first artifact before deciding whether the second is still needed.
- Write the request as a short acquisition path plus an upload action. When a standard screenshot or CSV contains the needed schema, ask for that artifact instead of making the user transcribe or assemble a field list; after inspection, request only a specifically missing field if it blocks the decision.
- If the user already supplied higher-level evidence, skip only stages that the active scenario does not require for the requested conclusion. Higher-level inputs do not waive required earlier stages and do not authorize completing several stages in one response; retain the input and apply the Interactive Stage Gate.
- Reuse compatible evidence already obtained in the conversation. Do not repeat API calls when subject, marketplace, period, filters, and required grain are unchanged.
- Keep observed facts, Agent inference, provisional action, and final action distinct.
- If evidence required for the user's requested decision is unavailable, give the current supported conclusion and request only the next evidence that would resolve that decision. Do not enumerate capabilities or decisions outside the user's request.

### General Conclusion Authority Gate

- Market evidence cannot support product-specific priority, measured conversion performance, profitability, bids, spend, budget allocation, or unconditional go/no-go decisions.
- Subject observation evidence cannot support measured click/conversion claims without seller funnel data, and it cannot support profitability or exact ad-budget decisions without Ads performance.
- Intermediate labels describe current posture or validation priority only; they do not authorize execution changes unless the scenario explicitly reaches seller-real calibration.
- Use bounded language before seller-real calibration: `merits further validation`, `controlled-test candidate`, `current evidence does not support advancing`, or `awaiting seller evidence`.
- Scenario limits may be stricter: single target-keyword Stage 1 may only decide whether to advance to ASIN validation and must not assign a controlled-test, SEO, ad, `Core`, or `Secondary` role.
- Reserve `Final calibrated conclusion` for decisions supported by the relevant seller-real fields.
- Require Amazon Ads performance in addition to ABA-SQP for profitability, ACOS/ROAS, exact bid changes, or exact ad-budget allocation.

## Evidence-Seeking Diagnosis Protocol

Apply this protocol whenever the task asks what is wrong, why a metric moved, or what explains a funnel pattern.

1. Record the observed fact without causal language.
2. Identify the narrowest problem domain supported by that fact.
3. Convert the problem into an unresolved question.
4. Identify the smallest evidence that can distinguish among material explanations.
5. Acquire that evidence when it is available through authorized in-scope tools or already-provided context; do not finalize while a usable discriminating source remains unchecked.
6. Form an explanation only from the evidence actually obtained, while retaining material alternatives not yet ruled out.
7. Apply the Evidence-to-Action Protocol before recommending a test, change, scale, or stop decision.

All evidence acquisition in this protocol must use the production-whitelisted ZooData channels in `reference.md`. Use the matching structured data API first. For a known page URL, use ZooData WebTools `/scrape`; use `/scrape-interactive` only when rendering or page actions are required. Use WebTools `/search` only when the URL must first be discovered. WebTools `/search` is not `products/search`, which remains prohibited. Never switch to an external interactive browser, direct Amazon navigation, or non-ZooData public web search. If no whitelisted ZooData channel can obtain the discriminating evidence, carry that exact gap into the single next-step request for user-provided evidence.

An anomaly is not a diagnosis. Do not fill an evidence gap with a standard inventory of possible causes. A list of compatible causes is allowed only as an internal evidence-search map or when each reported hypothesis has supporting evidence. If discriminating evidence is unavailable, report the identified problem, the unresolved question, the minimum next evidence, and the decision that cannot yet be made.

### Diagnostic Closure Gate

- Open a diagnostic branch only when the user requested a causal explanation or when the requested operating decision depends on resolving it.
- If the current evidence already supports the requested operating decision without explaining cause, state that decision and omit unused causal discussion. Do not append “this is not caused by X” or “factors Y/Z require investigation” merely to demonstrate caution.
- Every diagnostic branch mentioned in the report must end in exactly one of three states: `resolved by cited evidence`, `actively pursued with an in-scope evidence call`, or `carried into the single Next Step with directly matching evidence`.
- The requested next evidence must discriminate the exact explanations named in the unresolved question. Evidence for Ads economics/order attribution does not by itself resolve detail-page, price, promotion, offer, fulfillment, variation, or asset-quality explanations.
- If no available or requestable evidence can resolve the branch, omit the branch unless the user's explicit question requires reporting that it is unresolved.
- Do not continue the report as though a diagnostic branch were closed after writing only “further investigation is needed.”

## Evidence-to-Action Protocol

Apply this protocol after scoping the conclusion and before writing recommendations. Confidence labels describe evidentiary strength; they do not authorize a more specific action.

### Authorization checklist

For every proposed action, record:

1. **Target** — exact asset, field, keyword, campaign setting, offer, or business decision affected.
2. **Direct observation** — whether the target was inspected at sufficient fidelity.
3. **Defect signal** — the concrete issue observed on that target.
4. **Alternatives** — material alternative explanations that the evidence search must distinguish; compatibility alone does not make them findings.
5. **Validation** — comparison, experiment, time series, or first-party measurement that distinguishes the target from alternatives.
6. **Impact** — reversibility, cost, and downside if the action is wrong.

Map the evidence to the highest authorized action level:

| Level | Minimum authorization |
|-------|-----------------------|
| `Inspect` | A broad signal identifies a relevant problem domain |
| `Diagnose` | Multiple bounded hypotheses are supported and alternatives remain explicit |
| `Test` | The target was directly observed, a specific defect hypothesis exists, and the test is reversible with predefined success/failure criteria |
| `Change` | Direct target evidence plus validation distinguishes the target from material alternatives |
| `Scale` / `Stop` | Seller-real outcome evidence and thresholds justify the financial consequence |

If any required condition is absent, downgrade the action itself. Do not retain a `Change`, `Scale`, or `Stop` action by softening its wording.

### General examples

| Available evidence | Not authorized | Authorized next action |
|--------------------|----------------|------------------------|
| Clicks/cart adds but weak purchases | Rebuild the first three secondary images or list generic conversion causes | Locate the unresolved issue at the post-click/purchase handoff, then request the smallest evidence that can distinguish traffic quality from purchase-condition explanations |
| Search-result main-image thumbnail only | Rebuild the main image or secondary images | Inspect thumbnail-level subject recognition and request the full image set for asset-level review |
| High ACOS alone | Lower bids by a fixed percentage | Diagnose search-term CPC, conversion, placement, and attribution; define a reversible bid test only after target-level evidence |
| Organic rank decline | Pause the keyword or list every compatible cause | Define which movement remains unexplained, then retrieve the smallest time-aligned evidence that can distinguish demand, placement, subject, and market movement |
| Review deterioration | Redesign the product | Cluster complaint themes and validate frequency, recency, variant scope, and product causality |

Anti-pattern: `Current evidence does not support attributing this to the main image or title; detail-page persuasion, price, promotion, fulfillment, variation, and traffic source require further distinction.` This opens several unsupported branches without pursuing them. If causal diagnosis is not required, omit it and state only the supported operating implication. If it is required, retrieve or request evidence that directly resolves the named branch before continuing.

Acquisition anti-pattern: opening the Amazon detail page in an external browser because SQP shows clicks or cart adds without purchases. First use whitelisted ZooData structured endpoints such as `realtime/product`; for page evidence absent from structured responses, use ZooData WebTools `/scrape` or `/scrape-interactive` as required. Use WebTools `/search` only to discover an unknown URL, never as `products/search` or as a substitute for inspecting the selected page. External browser and non-ZooData public-web fallback are prohibited even when those ZooData calls are incomplete or unavailable.

### Asset-fidelity rule

State what representation was actually observed when an asset enters the diagnosis: full-resolution asset, detail-page rendering, mobile rendering, search-result thumbnail, URL/change event, or no visual observation. An asset URL or detected change event proves that an asset changed, not that its content is defective or caused the performance movement.

## Quick Mode Output

For single-lookup tasks (e.g., "what's the search volume for X", "what's the ABA rank for X", "show me the SERP for Y"):

- Answer the specific metric(s) directly with field name and value
- Tag each value with one confidence label: 📊 for direct API field, 🔍 if derived
- State the returned source identifier and snapshot date inline.
- No Data Provenance table required
- A localized API-usage table is required, same format as Full Mode: localized endpoint/calls/credits headers, a localized total row, and a localized credits-remaining label on the final line; if credit fields are absent, localize `not returned`
- No full report disclaimer block is required. Keep the answer within the returned evidence and add a concise source/period note only when it materially changes interpretation.
- Do not upgrade a Quick task to Full mode unless the user's follow-up questions expand the scope

## Full-Mode Checklist

Before running any Full-mode keyword task:

- [ ] Read the relevant tool documentation before selecting the tool: CLI help/reference docs for `zoodata.py`, or live schema / field descriptions for MCP/session tools
- [ ] Complete Pass 1 without a verdict: map each requested claim to the primary endpoint and exact expected field
- [ ] Write down the required judgment/evidence type and select its metric endpoint first; do not begin from a fixed data-endpoint chain
- [ ] Inspect metric item status, period, returned scoring/profile version, each dimension's calculation status, and the fields exposed for the required inference
- [ ] Complete Pass 2 before drafting: load the semantic reference for the fields actually returned and create a claim-to-field ledger including forbidden stronger inferences
- [ ] Build an evidence-coverage ledger from every returned judgment-relevant evidence unit, not only fields selected for candidate claims; assign a disposition and do not allow silent omission
- [ ] Group metrics by operator question; normalize subject, measure, grain, period, reference scope, direction, and conclusion authority
- [ ] Classify each material relationship as aligned, complementary, incomparable, or genuinely inconsistent; handle it in the initial report according to the generic reconciliation protocol
- [ ] If this is a later stage in an ongoing journey, apply the Cross-Stage Evidence Continuity Protocol; retain every compatible material constraint and record why any prior signal was updated, superseded, incompatible, or unavailable
- [ ] Re-run the semantic reference's forbidden inferences before the headline; do not translate one evidence subject/class into another or exceed the weakest authority required by the joint conclusion
- [ ] Integrate reconciliation into the substantive domain analysis; do not create user-facing methodology/process sections unless the user asked for them
- [ ] Draft decision-oriented output in `evidence → analysis → conclusion → next step` order; keep direct observations out of the conclusion and keep recommendations out of the evidence section
- [ ] If the metric satisfies the inference, stop; if it does not, determine whether data actually contains additional evidence before calling it—an unsupported/unavailable dimension alone is not a fallback reason
- [ ] Prefer `python {skill_base_dir}/scripts/zoodata.py` and choose the matching keyword subcommand after the documentation check
- [ ] If selecting an alternate execution surface before retrieval, inspect its live schema and field descriptions before use. Never switch surfaces as a runtime workaround after an interface failure.
- [ ] Classify the task: seed keyword / target keyword / ASIN / ASIN + keyword
- [ ] Confirm marketplace; default to `US` if absent
- [ ] For endpoints independently justified by the inference plan, group compatible subjects into batches within the documented contract. Batch support does not justify calling multiple layers.
- [ ] Before the first call to a batch-capable endpoint, collect the complete compatible subject set; do not issue per-keyword calls when one batch or sequential 20-item chunks can serve the same context
- [ ] Check `reference.md § Production availability`; route only to endpoints listed in that production whitelist.
- [ ] Confirm the date lens: weekly snapshot, recent 4-8 weeks, or latest sliding window; for keyword lookups that require `date` or `dateTo`, prefer T-1 or earlier and avoid the current date unless explicitly requested. In user-facing progress updates, simply state the selected marketplace/date without extra rationale unless the user asks why.
- [ ] Identify the current evidence level and, when applicable, the scenario-defined conversation stage before selecting conclusions or the next-step request
- [ ] Apply the Interactive Stage Gate: verify that every planned call belongs to the current user-decision stage, omit later-stage calls, and end with one confirmation or input request
- [ ] Apply the Stage Handoff Closure Gate: classify the stage as `complete`, `advance`, or `unresolved`; for the latter two, render the scenario-defined next-input request as mandatory, separate, and executable
- [ ] Check whether the user provided Amazon backend ABA-SQP search conversion data for the relevant ASIN/brand/query/date range
- [ ] Add one short, localized `Data Notes` section near the top naming the evidence source, period, and current analysis scope; do not duplicate it near the end
- [ ] Apply the User-Facing Language Rule to every title, heading, label, table header, status value, disclaimer, and fixed phrase; preserve only exact identifiers that require source spelling
- [ ] Use the next-step request defined by the active scenario; do not infer a universal fixed sequence
- [ ] Track every live response for usage accounting: use `_query.endpoint` / `_query.params` for bundled CLI responses; use the exact WebTools route/request scope for session calls; retain returned `meta.creditsConsumed` and `meta.creditsRemaining`
- [ ] Separate traffic facts from strategy advice using confidence labels
- [ ] Apply the Evidence-Seeking Diagnosis Protocol: state the unresolved question, acquire discriminating evidence, and do not substitute a generic cause list when evidence is missing
- [ ] Apply the Diagnostic Closure Gate: every diagnostic branch is resolved, actively pursued, or matched to the single final evidence request; omit branches irrelevant to the requested decision
- [ ] Apply the Evidence-to-Action Protocol to every recommendation; verify target observation, defect signal, alternatives, validation, and authorized action level
- [ ] Include the localized API-usage section as the final report section; if credit fields are missing, use a localized not-returned value instead of omitting the section

## Evidence Handling Rules

Before calling endpoints, identify the input shape, requested judgment, and applicable scenario capability combination. Use `reference.md` for endpoint capability and contract facts; the initial route never guarantees the final conclusion scope.

For a substantive report, organize applicable evidence in `evidence → analysis → conclusion` order. The evidence section states observations; the analysis section explains their relationship and limitations; the conclusion contains only the decision supported by that analysis.

### Partial Data Protocol

Apply this protocol only to successful responses containing a mix of usable and valid empty/unsupported evidence. A service/interface failure is handled by the Interface Failure Stop Gate instead.

1. Produce conclusions only from the data actually retrieved
2. Mention a missing evidence gap only when it blocks the decision the user asked for. State the smallest next evidence needed, without listing unrelated unavailable capabilities.
3. Do not infer a missing capability's output from an adjacent, non-equivalent capability.
4. Downgrade the overall conclusion scope to match the weakest available evidence; do not frame partial data as a complete analysis

### Cross-Metric Reconciliation Protocol

1. Group returned metrics by the operator question they inform.
2. Normalize each signal's subject, measure, population/grain, period, reference scope, direction, and conclusion authority.
3. Classify the relationship:
   - `aligned`: synthesize only the common supported scope;
   - `complementary`: preserve each distinct axis and state the bounded joint meaning;
   - `incomparable`: report separately without a shared score or ranking;
   - `genuinely inconsistent`: verify context/status/fields and keep the conflict unresolved unless discriminating evidence exists.
4. Preserve every material signal. Do not average unlike scores, silently choose one, invent a causal bridge, or turn the group into an undocumented umbrella concept.
5. Limit the joint conclusion to the intersection of evidence authority and state what remains unknown.
6. Integrate material reconciliation into the initial substantive analysis, not in a later reply after the user notices it.
7. Use the applicable semantic reference for field meaning and forbidden inference; do not use a fixed pair list as the routing mechanism.
8. Keep `aligned` / `complementary` / `incomparable` / `genuinely inconsistent` as internal reasoning labels unless naming one materially improves the user's domain understanding. Never create a fixed methodology section merely to display the classification.

### Evidence Coverage Protocol

1. Inventory the evidence returned by every justified call. Use decision-relevant evidence units: each metric dimension/status, requested trend result, declared aggregate or sample observation, and subject observation. Do not require a prose bullet for every raw row when a disclosed aggregate preserves its meaning.
2. Give each unit one disposition: `explained`, `synthesized`, `unavailable`, `inapplicable`, or `superseded`. A material unit is one that can change the decision, confidence, interpretation, or boundary. Record a scope/status reason for any non-explained disposition.
3. The evidence section must account for every usable material unit with its direct meaning, subject, scope, period, and direction. Do not select only favorable, simple, or mutually aligned evidence.
4. The comprehensive analysis must assign every material unit to an operator question and explain whether it supports, limits, complements, is incomparable to, or conflicts with the other evidence for that question.
5. The conclusion may be concise, but its basis must include both decisive supporting and decisive limiting evidence. If removing a signal would make the verdict stronger, simpler, or different, that signal cannot be omitted from the synthesis or conclusion basis.
6. Before sending, reconcile `returned units → dispositions → evidence section → analysis → conclusion basis`. Any material unit without a traceable path blocks the conclusion until it is explained or validly dispositioned.

### Valid No-Data Reporting

A valid `status=empty` or documented unsupported result is still material retrieval evidence, not an interface error. When it blocks the requested judgment, retain the normal report order instead of jumping straight to a conclusion:

1. **Evidence:** identify the endpoint, subject, requested/resolved period, returned status, and whether any usable field was obtained.
2. **Analysis:** explain which specific claim questions remain untested because of that valid response state.
3. **Conclusion:** state only the supported current state and, only if it unblocks the user's requested decision, the smallest next evidence or retry condition.

Do not replace this evidence chain with generic capability disclaimers, a list of things the system will not do, or a guessed operating recommendation.

### Interface Failure Stop Gate

Treat a timeout after the client's documented retries, connection/DNS failure, HTTP 5xx, unavailable endpoint, rate-limit/service rejection, non-zero execution without a valid structured result, or malformed/unparseable response as an interface failure.

An HTTP 5xx returned after the client's built-in retry budget is exhausted is a terminal failure for the current workflow and a hard interrupt for the current turn, not a first failed observation and not evidence that the requested date or other parameters are wrong. Report the service as currently unavailable and, when useful, tell the user to retry the same request later. Do not execute any subsequent API or tool command in that turn. In particular, never announce or attempt “an earlier date,” another marketplace, subject, filter, pagination value, endpoint, or surface to work around the 5xx.

A local parsing, transformation, extraction, or formatting command that fails after a paid API response is also an interface failure for that evidence unit. If the original valid structured response is still available, use it directly without another evidence call; otherwise stop under this gate. Never call the same paid endpoint again merely to change output format or recover from local post-processing failure.

1. Stop the workflow immediately after the failure. Do not call another endpoint, retry through another surface, descend to a data layer, split/fan out the request, or continue to a later scenario stage.
2. Report the failing endpoint or tool, subject/request scope, attempt/retry status, and exact returned error or absence of a parseable response.
3. Do not produce the requested market/product/operating conclusion from partial evidence and do not request ASIN, price, margin, SQP, Ads, or any other next-stage input.
4. If earlier calls succeeded, they may be listed as completed retrieval evidence, but must not be presented as a completed analysis after the required interface failed.
5. End with API usage already returned. Do not estimate missing credits or continue execution.

Parameter correction belongs to a different response class: only HTTP 422 authorizes correcting the documented validation violation identified by the server. A valid `status=empty` may justify a separately supported alternate query or period when the active scenario and endpoint contract permit it; that is no-data follow-up, not recovery from an interface failure. Never transfer either behavior to HTTP 5xx.

### Cross-Stage Evidence Continuity Protocol

1. Build the prior-stage ledger from evidence already retrieved in the conversation: field identity, value/direction, period, scope, conclusion authority, and the decision axis it constrains.
2. Check compatibility with the current subject, keyword, marketplace, period, and requested decision. Reuse compatible evidence; refresh only when the current decision requires a newer/incompatible scope.
3. Assign each prior material signal one state: `carried`, `updated`, `superseded`, `incompatible`, or `unavailable`. Never omit a signal merely because the later stage added more specific evidence.
4. Merge later-stage observations by decision axis. Preserve signals that measure different target levels, populations, or grains instead of collapsing them into one umbrella score.
5. For accessibility/difficulty claims, resolve separately: target-set entry, higher-position competition, position stability, and the observed subject's current gap. Do not project a result from one target level onto another.
6. Re-run cross-metric reconciliation on the merged ledger, then limit the conclusion to the combined authority. A later-stage verdict must not strengthen solely because a prior adverse or limiting signal disappeared from the report.

### Metric-First Access Protocol

1. Call the matching metric endpoint first when it exists on the target surface.
2. Map each requested conclusion to a returned metric dimension/field and verify what the metric can actually express.
3. Stop calling when all requested conclusions are supported.
4. For each unsupported conclusion, distinguish calculation-data absence from metric-contract insufficiency. Calculation-data absence normally ends that conclusion; it does not automatically trigger data access.
5. Descend only after a successful metric response when the data contract exposes additional fields or grain required for a named Agent inference. If the metric interface fails, apply the Interface Failure Stop Gate.
6. Before descending, record the missing inference and the exact extra fields/rows/series expected from data.
7. Do not call a source data endpoint merely to duplicate or “double-check” a supported metric.
8. Direct data access is correct when rows/series are the requested deliverable or no corresponding metric exists.

### Batch Response Protocol

1. After an endpoint is justified by the inference plan, collect all subjects with compatible documented request context.
2. Prefer `--keywords` over repeated `--keyword` calls. Do not loop singles when a valid batch can carry them.
3. Deduplicate case-insensitively and preserve first-occurrence order before calling.
4. When a compatible subject set exceeds the endpoint's documented batch limit, send sequential valid chunks and restore global input order.
5. Use a single-subject call only for one subject, incompatible request contexts, or an endpoint without batch capability.
6. Inspect each item's `status`; retain `empty` items with their reasons.
7. Analyze only `status=ok` evidence. Outer `success=true` does not upgrade empty items.
8. Use `meta.creditsConsumed` from each batch response. Do not estimate billing from request size; final billing is based on successful items.
9. Do not call both metric and source data merely because both support batching.

---

## General Rules

### Tool and Contract Discipline

- Read the candidate tool's documentation/help/schema before selecting it; never infer capability from a name alone.
- Prefer the documented local CLI. Use a live MCP/session tool only after inspecting its exact schema; if its callable name differs from documentation, use the live name.
- If no documented execution path is available, report that evidence gap rather than substituting an adjacent source.
- Use exact documented arguments, dates, limits, status meanings, and callable mappings from `reference.md` and CLI help.
- Use only the acquisition channels and evidence classes permitted by `SKILL.md` and `reference.md`.

### Scenario Selection Rule

- Select the scenario by the user's input shape and requested judgment, then use its capability combination as a starting plan rather than a mandatory chain.
- Treat diagnosis and reverse-ASIN discovery as mutually exclusive active routes. Temporal movement, anomaly, and causal questions belong to diagnosis; current traffic-term mapping and candidate discovery belong to reverse ASIN. When one request mentions both, give diagnosis precedence and follow its bounded triage or named-keyword path instead of adding a full traffic-term map.
- Combine scenario capability combinations only when their boundaries are non-exclusive and every call belongs to the same active user-decision stage. Never use combination to bypass a scenario's stop, confirmation, or conclusion limit.
- Apply the shared evidence and conclusion rules after retrieval; scenarios never authorize a stronger conclusion.

### Evidence Gate Rule

- Every conclusion must be directly supported by the endpoint designed for that evidence type
- If an endpoint returned no data or was unavailable, state the gap explicitly; do not downgrade silently
- Do not bridge a missing evidence type with a loosely related endpoint
- After detecting a problem, seek evidence that distinguishes explanations before stating a cause; if none is available, stop at the unresolved problem and request the minimum next evidence instead of listing generic causes

### Conclusion Scope Rule

- `Data-backed` means directly supported by the correct endpoint for that claim type
- `Inferred` means evidence-backed reasoning, not endpoint substitution
- `Directional` means evidence-bounded validation or monitoring advice. It does not permit an unsupported explanation, and it never means proven causality.
- Strong wording is not allowed when the claim depends on optional enrichers that were not available

### Comparative Claims Rule

- Do not say the product, listing, CTR, CVR, rank, or traffic quality is better than competitors unless the report has direct competitor evidence for the same metric, same keyword/query, same marketplace, comparable date range, and comparable placement or position scope
- When competitor-specific evidence is unavailable, compare to the market instead: above/below market median, ahead/behind the market midpoint, near the upper/lower band, or ranking toward the front/back
- If a market average, median, or band is calculated from ABA/SQP screenshots, ZooData aggregates, or visible SERP samples, state how it was calculated and name the limitation
- Do not treat a market-wide query average as competitor-specific proof
- If position or placement cannot be controlled, downgrade confidence and use restrained wording such as "not an obvious weak point" rather than "significantly better than competitors"

### Usage Accounting Rule

- Every full-mode report that used live API data must end with the localized section representing the internal `API Usage` role
- Count every API call actually executed, including duplicate, diagnostic, or recovery calls whose output was later discarded. A local parse failure does not erase the preceding call or its returned credit usage.
- Do not include a separate `Data Provenance` table unless the user explicitly asks for source-by-section details
- The localized API-usage section must contain a markdown table, not a bullet list
- Its table must aggregate calls by endpoint and sum `meta.creditsConsumed` from the responses
- Its final row must use the user's language for the total label and sum all endpoint calls and returned credits consumed
- If any endpoint's credits are absent, use a localized equivalent of `not returned`; write the localized equivalent of `partial N + not returned` when some credits are known
- Required table format:
  `| [Localized endpoint header] | [Localized calls header] | [Localized credits header] |`
  `|---|---:|---:|`
  `| [endpoint] | 1 | 1 |`
  `| [Localized total label] | 1 | 1 |`
- End with `[Localized credits-remaining label]: N` using the latest `meta.creditsRemaining`
- If `meta.creditsConsumed` or `meta.creditsRemaining` is absent, use the localized equivalent of `not returned`; do not infer or hide credit usage
- Do not finish the response after recommendations, caveats, or limitations if API usage has not been reported

### HTTP Validation Rule

- HTTP 422 is a parameter validation error, not a retryable transient failure.
- Do not retry the same 422 request repeatedly.
- Read the returned error detail and correct the call before retrying.
- Inspect the structured server error and request metadata, then use `reference.md` and CLI help to correct the documented contract violation.

### Credential and Credit Failures

- If `ZOODATA_API_KEY` is missing, run `python {skill_base_dir}/scripts/zoodata.py check`, then stop before retrieving evidence and direct the user to the documented key page. Do not substitute other data sources.
- On HTTP 401, stop further calls and report that the key was rejected.
- On HTTP 402, stop further calls and report only the partial evidence already retrieved. Do not estimate credits required for unfinished calls from request size; request a credit top-up or a narrower confirmed scope instead.

### Data Notes Rule

- Full-mode reports use one short, localized `Data Notes` section immediately after the title/source line. Name the evidence source, period, and current analysis scope in neutral language.
- Do not duplicate a `Data Notes Reminder` near the end and do not place evidence requests inside individual findings.
- At market evidence level, identify the analysis as a market screen. At subject-observation level, identify the observed ASIN/keyword scope. At seller-real-data level, name the supplied SQP/Ads fields used.
- Keep the wording natural and translated to the user's language. Avoid deficit-framed language and form-like status blocks.
- Do not use ZooData estimated exposure/search/visibility signals as a substitute for user-provided ABA-SQP conversion evidence.
- The active scenario defines when to request seller data and points to its semantic reference.
- Keep the substantive report in `evidence → analysis → conclusion` order even when no endpoint produced a usable metric. `Data Notes` is context, not a replacement for the evidence or analysis sections.

### Date Handling

- Treat keyword inputs as search queries, select dates according to the documented endpoint contract, and report returned periods rather than inferred periods.
- Never compare incompatible returned grains or periods as though they were the same.

### Ad vs Organic Separation

- Keep organic and sponsored observations separate.
- Do not equate placement-record counts with exposure contribution, or exposure signals with CPC, bid economics, conversion, or budget priority.
- Use the relevant semantic reference before interpreting placement or exposure fields.

### Anomaly Standards

| Signal type | Minimum evidence | Max confidence |
|-------------|------------------|----------------|
| Weekly trend change | 2+ weekly points in same direction | 🔍 |
| SERP change | 2 timestamps showing changed rank mix | 🔍 |
| One-day movement | single snapshot difference | 💡 |


## Output Rules

### Candidate Validation Rule

Use any label supplied by the active scenario only as a description of the current evidence-bounded validation posture. A label must not imply a bid, match type, budget, pause, negative keyword, profitability, or final expansion decision.

Before assigning a candidate-validation label, require all of the following:

- evidence appropriate to the requested subject and decision;
- supported, non-materially-limiting evidence for every market dimension used in the label;
- directly observed ASIN/product-fit evidence when the label is product-specific; and
- no unobserved placement, conversion, or operating strategy inference.

### Observation Flags

Report these as evidence-scoped observations, not automatic financial or investment risk:

- high `adCount` means greater observed ad participation; it does not establish CPC, auction competition, ROI, or spend posture
- search demand falling across multiple weekly points is a demand-trend concern within that window
- an observed ASIN appearing only in sponsored placements is a placement-posture observation, not proof of weak organic relevance or conversion
- repeated brands or parent ASIN families describe concentration only within the disclosed returned sample
- low `daysCoverageRate` or low `observationCount` limits confidence rather than proving instability

## Monitoring Cadence Suggestion

Recommended default cadence:

- weekly for keyword opportunity watchlists
- weekly for launched terms and incident follow-up, using the latest resolved weekly period
- use seller Ads or other explicitly daily-granular first-party data for intraweek monitoring; do not present repeated ZooData keyword calls as daily tracking
