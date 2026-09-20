# Execution Guide — Amazon Market Analysis

This guide owns the shared scenario and stage contract. The market story is `discover candidates → evaluate a selected market → track its changes`; a user may enter at any step with the required subject. Each step is a different decision scope, not a mandatory pipeline.

## Authority and routing

Apply `question → scenario → active stage → evidence → Gates → stage conclusion → supported continuation → final output`. `SKILL.md` classifies the question and loads modules. Scenario files supply stage-specific entry inputs and evidence. `reference.md` owns API facts; `market-metric-semantics.md` and `seller-input-semantics.md` own interpretation; `evidence-protocols.md` owns detailed acquisition and comparison; `output-rules.md` owns rendering. This guide owns shared Gate decisions and the maximum authority of each evidence level.

## Execution mode

| Question | Mode | Behavior |
|---|---|---|
| One exact category metric, distribution, or history lookup | Quick | Return the requested observation with identity, scope, date, source, and usage; no scenario stage. |
| Opportunity discovery, market entry assessment, category trend, comparison, or watch question | Full | Select one scenario and complete one applicable decision stage. |

Quick mode still applies the Field Identity, Interface Failure Stop, and Final Output Gates.

## Stage schema and story

Each full-mode scenario stage defines exactly `Stage`, `Entry input`, `Evidence`, and `Conclusion authority`. A stage list does not require traversal in order. A user who already names a category may start evaluation or tracking directly; a user who supplies seller inputs early need not repeat them. A broad request does not authorize every later stage or a recurring monitor.

| Scenario | Primary subject | Decision boundary |
|---|---|---|
| Discover | Observed category set or category-scoped product candidate set | Which observed candidates merit validation; no entry verdict or profit claim |
| Evaluate | One resolved category and, when supplied, the seller's constraints | Market screen, then a conditional entry verdict within supplied evidence |
| Track | One or more resolved categories and comparable periods or an explicitly opted-in watchlist | What changed and which changes merit investigation; no causal or automatic operating decision |

## Shared evidence levels

| Level | Available evidence | Maximum conclusion |
|---|---|---|
| Market observation | Category snapshot, selected Top 100 structure, available month-end history | Bounded market size, structure, relative attractiveness, or observed movement |
| Candidate observation | Market evidence plus product, competitor, review, or price-band observations | Candidate validation priority and specific barriers; no measured margin or seller fit |
| Seller-constrained | Compatible observations plus seller-provided capital, cost, operational constraints, and known compliance facts | Conditional GO/CAUTION/AVOID for the named seller and market; no guarantee of profit or legal clearance |

## Active-stage sequence

1. Verify the subject and the selected stage's `Entry input`. Preserve later-stage inputs without interpreting them in a lower stage.
2. Plan only the stage's named evidence. Use `evidence-protocols.md` to acquire the smallest sufficient set; a broad composite is justified only when its full fan-out serves the active stage and its credit cost was made clear.
3. After every tool result apply the Interface Failure Stop Gate before another call. Then apply Field Identity and the appropriate semantic owner before interpreting any value.
4. Apply the Evidence and Conclusion Authority Gates. Render the current stage only through `output-rules.md`.
5. Apply the Handoff Gate and render the Stage-End Selection List after API Usage. Do not automatically execute another story step or begin recurring monitoring.
6. Apply the Final Output Gate immediately before sending.

## Gate order

| Order | Gate | Decision |
|---:|---|---|
| 1 | Stage Entry Gate | Select one stage whose required subject and requested conclusion are present. |
| 2 | Interface Failure Stop Gate | Stop on the shared CLI contract's terminal interface classification. |
| 3 | Field Identity Gate | Verify endpoint, subject, scope, sample, metric path, unit, denominator, and returned date. |
| 4 | Evidence Gate | Require the right evidence type and adequate coverage for each claim. |
| 5 | Conclusion Authority Gate | Cap the judgment at the shared level and the stricter scenario stage. |
| 6 | Handoff Gate | Derive evidence-supported continuation questions with clear entry inputs. |
| 7 | Stage-End Selection List Rule | Close every normally completed full stage with one selection list. |
| 8 | Final Output Gate | Check the whole rendered answer against the chosen output mode. |

### Stage Entry Gate

Complete at most one decision stage per turn. A stage changes candidate set, category, time scope, or seller-decision authority. Enter it only when the latest user request asks for a conclusion in its scope and its entry input exists. A follow-up selecting a category or supplying a file may satisfy entry in the same reply; do not demand another confirmation. Reclassify the user's actual follow-up instead of following a hidden pending queue.

### Interface Failure Stop Gate

Classify every CLI result through `cli-contract.md`. On a terminal interface failure, make no market ranking, entry verdict, trend claim, or monitoring-state write. Preserve earlier successful data for compatible later reuse; render only the local interface-failure route in `output-rules.md`. A valid empty market row or absent history point is an evidence boundary, not an interface failure.

### Field Identity Gate

Resolve `(source, categoryId, categoryScope, sampleType, marketplace, metric path, unit, denominator, date or comparison periods)` before a claim. Do not move a Top 100 rate to the whole category, use `meta.total` as product count, or equate product history with market history. If identity is unresolved, state the unavailable field instead of guessing. For derived values, show the compatible inputs and formula.

### Evidence Gate

Use the stage's named endpoint or compatible carried evidence for each claim. Acquire and project live results through the shared temporary-result procedure; displayed truncation, `success=true`, or `meta.total` alone never establishes that every compared row and required field was inspected. A current snapshot cannot by itself establish a trend or cause. An empty distribution cannot prove zero share; a missing month cannot be filled by interpolation. Do not replace missing market evidence with generic industry knowledge, price × sales arithmetic, or a different subject's product observation. Reconcile material conflicts under `evidence-protocols.md`.

### Conclusion Authority Gate

Market observations permit a screen, not a seller-specific GO or measured profitability. Product observations permit candidate validation, not actual seller conversion or a guaranteed opportunity. A seller-specific verdict requires the inputs named by the evaluation scenario and remains conditional on unknown legal, supply, and execution risks. A market movement is an observation, not proof of a causal driver or a buy/sell/price action. User thresholds narrow conclusions; they do not make absent evidence available.

### Handoff Gate

After a normally completed full stage, reread the user's still-current question and the current conclusion. Offer a continuation only when it addresses a material remaining decision, an available capability can supply the missing evidence, and a scenario stage names its exact `Entry input`. A category-market shortlist can support a deeper child-market comparison, a named market screen, or category-scoped product validation; a market screen can support a seller-fit decision when the user seeks one; a change observation can support investigation of the named changed market. Choose only the questions justified by this report, not a fixed catalog of every possible endpoint.

Each continuation must state the exact category, candidate set, period, or seller input and the business question it would answer. When several finite shortlist subjects support the same continuation, make each subject separately selectable; do not point to a table rank or ask the user to choose from another list in the report body. Do not offer a causal, profit, seller-specific GO, or recurring-monitoring conclusion whose evidence path is unavailable. A suggested continuation does not authorize its API calls until the user selects or directly requests it. If no remaining decision has a supported route, offer no continuation. Stages describe evidence scopes, not mandatory progression or a hidden queue.

### Stage-End Selection List Rule

Every normally completed full stage ends with one concise localized numbered selection list after API Usage, or after the conclusion when no live calls were made. Use it even if no continuation passed the Handoff Gate.

1. Put every supported selectable subject and action directly in this final list, using user-domain language and an exact subject label. Keep the list decision-sized; do not turn every observed market row or later capability into an option. Put an evidence-supported priority first and mark it recommended only when the evidence supports that priority.
2. Number items `1`, `2`, `3`, … in display order. Append exactly one final item meaning **Ask another question or end this analysis**, with no explanation attached. If there is no supported continuation, that fixed item is the only item.
3. Do not render another action menu or selection key inside Evidence, Analysis, or Conclusion. The category ranks in a comparison table are data, not menu numbers. Tell the user they may reply with a final-list number or label, directly ask a different question, or stop. Do not auto-select a route.

At the next user turn, classify the actual reply through `SKILL.md`. A bare number selects only the most recent final-list item, never a market rank in the report body. A direct new question or changed scope supersedes the prior list. If the selected item already supplies its required category and period, proceed without another confirmation; otherwise ask only for the missing entry input. Reuse compatible earlier evidence, obtain only the additional evidence needed for the new decision, and keep the new conclusion within its active stage.

### Final Output Gate

Apply `analysis-contract.md § 7. Final Response Gate` immediately before every user-facing send. This market module adds only the following rendering checks:

1. Select one market output route and its complete permitted shape from `output-rules.md`; a normally completed full stage also uses the Stage-End Selection List Rule above.
2. For quick mode, require source, scope, returned date, requested metric, limitations, and usage. For a normally completed full stage, require the canonical `Data Notes → Evidence → Analysis → Conclusion → API Usage → one final numbered selection list` order. A prose-only “next step”, missing final list, or missing fixed new-question/exit item fails.
3. Ensure every number maps to an observed field or labeled derivation, every verdict stays within market authority, and internal stage/Gate terms are absent from user-facing prose.
4. Interface and credential failures use only their market failure rendering and do not render the normal report or list.

## Credential and credit failures

Use `python {skill_base_dir}/scripts/zoodata.py check` for credentials without endpoint probes. A missing or rejected key stops evidence retrieval and receives localized setup guidance. `_transport.status=402` stops further calls; report the last completed evidence and returned credit metadata when available, without fabricating the missing result. Do not change credential sources or issue alternate endpoints to evade these states. For broad scans with an actual variable fan-out, state the expected call range and ask for a credit cap before executing it. A parent-market comparison with at most 100 direct children is a bounded two-call acquisition (`categories` once and `markets/search` once); proceed without an extra budget pause unless the user set a stricter cap. One exact lookup likewise does not need a scan budget.
