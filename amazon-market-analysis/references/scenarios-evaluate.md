# Evaluate a Named Market

This scenario owns market entry assessment for a resolved category. Use the guide's stage/Gate order and shared output skeleton. Endpoint facts, market metric meanings, and seller input semantics remain with their owner modules.

## Scenario boundary

Use this route for a named category or niche, including questions such as "how competitive is it?" or "should I enter?". A market screen assesses observed category conditions; a seller-specific GO/CAUTION/AVOID also requires the seller's constraints. Do not turn a generic market score into a guaranteed product launch decision.

## Evidence stages

| Stage | Entry input | Evidence | Conclusion authority |
|---|---|---|---|
| Market screen | Resolved category ID and selected product-inclusion scope | Exact `market` snapshot; named `market-structure-profile` dimensions and `market-history` periods as needed; category-scoped product/brand/price/review observations only for a named question | Describe size, selected-sample concentration, price/review barriers, and observed trajectory; no seller-specific GO. |
| Seller fit and entry verdict | Resolved category plus explicit entry decision request, compatible market evidence, and seller capital/operating inputs sufficient for the requested verdict | Carried or newly acquired market-screen evidence plus seller-provided cost, budget, differentiator, validation plan, and known compliance/IP constraints interpreted through `seller-input-semantics.md` | Conditional GO/CAUTION/AVOID for this seller and category; no guarantee of profit, legal clearance, or automatic launch action. |

The seller-fit stage may obtain the named market-screen evidence in the same turn when the user's request and inputs already support it. If seller inputs are absent, complete the market screen and name the exact missing decision inputs as a possible continuation.

## Market screen application

- Acquire and validate one exact market snapshot through `reference.md` and `evidence-protocols.md`, then interpret only the fields needed by the named market question through `market-metric-semantics.md`.
- For a named structural or trajectory question, choose only the relevant documented distribution or history capability and require compatible evidence identity before comparison.
- For a parent market, compare the validated child-market population required by the question. Apply the evidence protocol's identity and overlap constraints before ranking or aggregation.
- `brand-overview`, `price-band-overview`, `products`, `competitors`, and `analyze` can support a named barrier or consumer-gap question. Reconcile them with market evidence only through the shared semantics and evidence protocols.
- A comprehensive `market-entry` composite may be used only when the user requests a broad assessment and the multi-endpoint credit cost is within the stated budget. Reuse its available results locally; do not rerun a component solely to restyle the report.

## Seller fit and verdict

Judge these dimensions separately before the verdict: demand/trajectory, concentration and review barrier, differentiating evidence, capital/cash cycle, contribution economics, validation speed, and known compliance/IP exposure. User-stated thresholds take precedence over default qualitative judgments.

| Verdict | Required support |
|---|---|
| GO | Favorable compatible market evidence, a plausible differentiator and validation plan, sufficient seller capital and unit-economics inputs, and no known unresolved hard block. State assumptions and remaining validation work. |
| CAUTION | Mixed market signals or a material seller input/assumption still unresolved but testable through a bounded validation step. Do not phrase this as an approved launch. |
| AVOID | A seller-stated non-negotiable threshold fails, or known capital/compliance/IP constraints make the proposed entry infeasible under the seller's conditions. Name the observed or seller-supplied basis. |

Apply `seller-input-semantics.md` to missing cost, fee, compliance, and IP inputs. When that owner classifies a material input as unresolved, the verdict cannot exceed conditional CAUTION or unresolved. Conflicting category and child-market signals narrow the conclusion rather than silently overriding one another.

## Section content requirements

In `Evidence`, show the resolved market identity, returned snapshot/date, sample scope, and the seller inputs actually supplied. In `Analysis`, separate observed market barriers from seller-specific assumptions and explain conflicts. In `Conclusion`, state either the market screen or the supported conditional verdict, including any material evidence gap. An evidence-backed next question can be selected only through the guide-owned final list.
