"""Structural and safety guardrails for the keyword-analysis skill."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "amazon-keyword-traffic-analysis"


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_skill_is_a_concise_router_not_a_second_execution_guide():
    skill = read("SKILL.md")

    assert len(skill.splitlines()) < 120
    assert "## Start here" in skill
    assert "## Source-of-truth boundaries" in skill
    assert "references/execution-guide.md" in skill
    assert "references/reference.md" in skill
    assert "references/metrics-market-profile.md" in skill
    assert "references/metrics-trend-profile.md" in skill
    assert "references/serp-and-rollover.md" in skill
    assert "references/sqp-field-semantics.md" in skill
    assert "### Two-Pass Metric Interpretation Gate" not in skill
    assert "### Evidence-to-Action Authorization Gate" not in skill
    assert "### Candidate Validation Rule" not in skill
    assert "current traffic terms, traffic-source structure, candidate discovery" in skill
    assert "This diagnosis route takes precedence" in skill
    assert "ASIN-wide anomaly without a named keyword" in skill
    assert "applicable scenario guide, or to multiple non-exclusive guides" in skill
    assert "Load exactly one scenario" not in skill
    assert "Before requesting or interpreting a seller artifact" in skill
    assert "Without `--endpoints` or `--keyword-endpoints`, it makes no evidence calls" in skill


def test_source_of_truth_boundaries_define_exclusive_module_ownership():
    skill = read("SKILL.md")

    assert "This file owns only trigger classification, reference loading, scenario routing" in skill
    assert "must not define endpoint contracts, shared workflow procedures, field semantics" in skill
    assert "`reference.md` owns only production API and acquisition-surface facts" in skill
    assert "must not define Agent workflow, action/output policy, business interpretation" in skill
    assert "`execution-guide.md` owns only cross-scenario Agent workflow" in skill
    assert "must not redefine API contracts, field meanings, or scenario-specific capability/stage maps" in skill
    assert "The metric/observation semantic references (`metrics-*.md` and `serp-and-rollover.md`) own only" in skill
    assert "must not define production availability or request parameters, shared workflow policy" in skill
    assert "`sqp-field-semantics.md` owns seller-artifact acquisition order, schema identity" in skill
    assert "must not define ZooData API contracts or scenario-specific stage triggers and conclusions" in skill
    assert "Scenario files own only scenario-specific capability selection, stage transitions, and report shape" in skill
    assert "must not restate, relax, replace, or create exceptions" in skill
    assert "Cross-module references are allowed; cross-module redefinition and duplicated policy are not" in skill
    assert "split API fact, shared workflow consequence, field interpretation, and scenario application" in skill
    assert "Apply each rule from its responsible owner module above" in skill
    assert "A downstream module may narrow behavior but must not override an owner contract" in skill
    assert "surface it for discussion" not in skill
    assert "changing a top-level owner contract" not in skill
    assert "maintainer" not in skill.lower()


def test_maintenance_conflict_governance_stays_out_of_runtime_skill():
    skill = read("SKILL.md")
    contributing = (ROOT.parent / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "## Skill Specification Ownership" in contributing
    assert "If a change exposes an inseparable conflict between owner contracts" in contributing
    assert "request a maintainer decision in the issue or pull request" in contributing
    assert "Do not silently" in contributing
    assert "Keep this repository-maintenance process out of runtime skill instructions" in contributing
    assert "surface it for discussion" not in skill
    assert "request a maintainer decision" not in skill


def test_contributing_constrains_skill_router_and_ownership_reviews():
    skill = read("SKILL.md")
    contributing = (ROOT.parent / "CONTRIBUTING.md").read_text(encoding="utf-8")
    contributing_flat = " ".join(contributing.split())

    assert "Each skill's `SKILL.md` is that skill's runtime router and module-responsibility manifest" in contributing_flat
    assert "declare the owner of each policy class used by the skill" in contributing_flat
    assert "must not absorb the detailed" in contributing_flat
    assert "Every bundled reference, scenario, script-facing instruction" in contributing_flat
    assert "must follow the ownership map declared by its own `SKILL.md`" in contributing_flat
    assert "automated consistency checks must read the affected" in contributing_flat
    assert "review every bundled module strictly against its declared responsibility" in contributing_flat
    assert "must not invent a parallel ownership model in the review program" in contributing_flat
    assert "A change to the ownership map is an architectural change" in contributing_flat
    assert "not silently adjusted to make another file or test pass" in contributing_flat
    assert "constrains what a `SKILL.md` may own" in contributing_flat
    assert "does not define or duplicate any skill's domain-specific policy" in contributing_flat
    assert "## Source-of-truth boundaries" in skill


def test_module_files_do_not_declare_foreign_owner_sections():
    def headings(relative_path):
        return {
            line.lstrip("#").strip()
            for line in read(relative_path).splitlines()
            if line.startswith("#")
        }

    api_headings = headings("references/reference.md")
    execution_headings = headings("references/execution-guide.md")
    semantic_paths = (
        "references/metrics-market-profile.md",
        "references/metrics-trend-profile.md",
        "references/serp-and-rollover.md",
    )
    scenario_paths = (
        "references/scenarios-expand.md",
        "references/scenarios-keyword-analysis.md",
        "references/scenarios-reverse-asin.md",
        "references/scenarios-keyword-traffic-diagnosis.md",
    )

    assert api_headings.isdisjoint({
        "Interactive Stage Gate",
        "Stage Handoff Closure Gate",
        "User journey",
        "Report shape",
    })
    assert execution_headings.isdisjoint({
        "Production availability",
        "Common keyword endpoint contract",
        "Live endpoints by layer",
        "CLI and callable mapping",
        "User journey",
        "Report shape",
    })
    for path in semantic_paths:
        assert headings(path).isdisjoint({
            "Production availability",
            "Common keyword endpoint contract",
            "Interactive Stage Gate",
            "Interface Failure Stop Gate",
            "User journey",
            "Stage transition gate",
            "Report shape",
        }), path
    for path in scenario_paths:
        assert headings(path).isdisjoint({
            "Production availability",
            "Common keyword endpoint contract",
            "Empty results and errors",
            "Interface Failure Stop Gate",
            "HTTP Validation Rule",
        }), path


def test_interface_failure_policy_respects_module_ownership():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    reference = read("references/reference.md")
    script = read("scripts/zoodata.py")
    scenarios = [
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "references").glob("scenarios-*.md"))
    ]

    # The router owns loading and dispatch only.
    assert "apply its `Interface Failure Stop Gate` before selecting any next capability or command" in skill
    for leaked_detail in (
        "HTTP 5xx",
        "HTTP 422",
        "workflowDisposition",
        "retryPolicy",
        "parameterMutationAllowed",
        "earlier-date request",
    ):
        assert leaked_detail not in skill

    # The API reference owns response meaning, not agent recovery behavior.
    assert "HTTP 422 means request validation failed" in reference
    assert "HTTP 5xx after the client's built-in retries means the service is currently unavailable" in reference
    assert "does not establish that the requested date or other parameters are invalid" in reference
    for leaked_action in (
        "Stop the current workflow",
        "retry the same request later",
        "permits an alternate date or query",
        "workflowDisposition",
    ):
        assert leaked_action not in reference

    # The shared execution guide owns stop/retry/parameter-mutation policy.
    assert "### Interface Failure Stop Gate" in guide
    assert "Do not execute any subsequent API or tool command in that turn" in guide
    assert "only HTTP 422 authorizes correcting the documented validation violation" in guide
    assert "A valid `status=empty` may justify a separately supported alternate query or period" in guide

    # The CLI owns deterministic retry mechanics and machine-readable disposition.
    assert '"workflowDisposition": "stop_current_turn"' in script
    assert '"retryPolicy": "later_same_request_only"' in script
    assert '"parameterMutationAllowed": False' in script

    # Scenarios inherit the shared gate and cannot redefine transport recovery.
    for scenario in scenarios:
        assert "workflowDisposition" not in scenario
        assert "retryPolicy" not in scenario
        assert "parameterMutationAllowed" not in scenario
        assert "HTTP 5xx" not in scenario


def test_execution_guide_is_the_single_shared_workflow_source():
    guide = read("references/execution-guide.md")

    assert "## Authority and routing" in guide
    assert guide.index("## Contents") < guide.index("## Authority and routing")
    assert "[Structured Field Identity Gate](#structured-field-identity-gate)" in guide
    assert "[User-Facing Language Rule](#user-facing-language-rule)" in guide
    assert "[User-Facing Output Boundary](#user-facing-output-boundary)" in guide
    assert "[Monitoring Cadence Suggestion](#monitoring-cadence-suggestion)" in guide
    assert "question → evidence plan → retrieval → field interpretation → analysis → evidence-bounded conclusion" in guide
    assert "Scenario files are downstream applications" in guide
    assert "must align upward with this guide plus the applicable API and field-semantic references" in guide
    assert "## Retrieval Progress Updates" in guide
    assert "use one short, natural sentence in the user's language" in guide
    assert "State only the subject and business question currently being examined" in guide
    assert "Do not announce the execution mode or stage number" in guide
    assert "do not render an execution-plan heading, numbered plan, endpoint list, or capability list" in guide
    assert "Do not mention tools, commands, endpoints, batching" in guide
    assert "support/calculation states, validation mechanics" in guide
    assert "Do not expose partial judgments, candidate verdicts" in guide
    assert "stage-transition deliberation" in guide
    assert "a list of things the answer will not do" in guide
    assert "Do not narrate every retrieval call" in guide
    assert "I’ll check the recent US market performance of these six keywords" in guide
    assert "Running Stage 1. Execution plan" in guide
    assert "## Two-Pass Metric Protocol" in guide
    assert "### Interactive Stage Gate" in guide
    assert "### Stage Handoff Closure Gate" in guide
    assert "Classify the stage as exactly one of" in guide
    assert "`complete`" in guide
    assert "`advance`" in guide
    assert "`unresolved`" in guide
    assert "Scenario journey rows must name the observable trigger" in guide
    assert "Every full-mode scenario must explicitly inherit this gate" in guide
    assert "Complete at most one user-decision stage per assistant turn" in guide
    assert "Do not call a later-stage capability before the user explicitly confirms progression" in guide
    assert "does not pre-authorize every later stage" in guide
    assert "Do not combine several completed stages into one long process report" in guide
    assert "followed by at most one next-step confirmation or input request when progression is needed" in guide
    assert "progression is required by the conclusion itself" in guide
    assert "one direct, executable request" in guide
    assert "Never make a required handoff optional" in guide
    assert "without manufacturing another request" in guide
    assert "single next action needed from the user, if any" in guide
    assert "retain it without interpreting it" in guide
    assert "does not require a user pause between retrieval and interpretation" in guide
    assert "complete them sequentially in one response without an artificial pause" not in guide
    assert "### Cross-Metric Reconciliation Protocol" in guide
    assert "### Candidate Validation Rule" in guide
    assert "Do not average unlike scores" in guide
    assert "### Valid No-Data Reporting" in guide
    assert "### Interface Failure Stop Gate" in guide
    assert "Stop the workflow immediately after the failure" in guide
    assert "Do not call another endpoint" in guide
    assert "do not request ASIN, price, margin, SQP, Ads" in guide
    assert "local parsing, transformation, extraction, or formatting command that fails" in guide
    assert "Never call the same paid endpoint again merely to change output format" in guide
    assert "not evidence that the requested date or other parameters are wrong" in guide
    assert "#### HTTP 5xx User-Facing Template" in guide
    assert "Source template: `Service is temporarily unavailable. Please try again later.`" in guide
    assert "Do not execute any subsequent API or tool command in that turn" in guide
    assert "never announce or attempt “an earlier date,”" in guide
    assert "only HTTP 422 authorizes correcting the documented validation violation" in guide
    assert "A valid `status=empty` may justify a separately supported alternate query or period" in guide
    assert "Never transfer either behavior to HTTP 5xx" in guide
    assert "evidence → analysis → conclusion" in guide
    assert "### Available Data → Conclusion Scope" not in guide
    assert "### Scenario Routing Rule" not in guide
    assert "`keywords/detail`" not in guide
    assert "sqp-field-semantics.md" not in guide
    assert "Treat diagnosis and reverse-ASIN discovery as mutually exclusive active routes" in guide
    assert "give diagnosis precedence" in guide
    assert "Combine scenario capability combinations only when their boundaries are non-exclusive" in guide
    assert "combine their relevant capability combinations" not in guide


def test_user_facing_output_boundary_hides_internal_failure_policy():
    guide = read("references/execution-guide.md")
    scenarios = [
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "references").glob("scenarios-*.md"))
    ]

    assert "## User-Facing Output Boundary" in guide
    assert "Runtime rules determine what the Agent does; they are not user-facing report content" in guide
    assert "Do not expose rule names, specification ownership, module boundaries" in guide
    assert "Surface a technical identifier or diagnostic detail only when the user explicitly asks" in guide
    assert "Do not add a meta heading such as `Action` or `Action guidance`" in guide
    assert "Retain the failing endpoint or tool" in guide
    assert "Do not surface them by default" in guide
    assert "#### HTTP 5xx User-Facing Template" in guide
    assert "Source template: `Service is temporarily unavailable. Please try again later.`" in guide
    assert "Output only the natural localized rendering of the source template" in guide
    assert "Do not quote or expand the CLI error payload's `message` or `action`" in guide
    assert "The CLI value is a safe fallback, not the final-output template owner" in guide
    assert "Do not add a heading, endpoint/tool name, HTTP status, retry count" in guide
    assert "retrieved product data, API-usage section, parameter-preservation warning" in guide
    assert "next-step section, or action-guidance section" in guide
    assert "A one-sentence interface-failure notice is not a completed full-mode report" in guide
    assert "Report the failing endpoint or tool" not in guide
    assert "report the interface error" not in "\n".join(scenarios)


def test_top_level_localization_preserves_exact_enums_and_localizes_usage_labels():
    guide = read("references/execution-guide.md")

    assert "human-readable status labels" in guide
    assert "When reporting a source enum such as `status=empty`, retain the exact enum value" in guide
    assert "do not translate the value inside the identifier" in guide
    assert "| [Localized endpoint header] | [Localized calls header] | [Localized credits header] |" in guide
    assert "| [Localized total label] | 1 | 1 |" in guide
    assert "[Localized credits-remaining label]: N" in guide
    assert "use a localized equivalent of `not returned`" in guide
    assert "`| Endpoint | Calls | Credits |`" not in guide
    assert "`Credits remaining: N`" not in guide


def test_interface_failure_never_descends_to_data_layer():
    guide = read("references/execution-guide.md")
    reference = read("references/reference.md")

    assert "Do not call another endpoint" in guide
    assert "descend to a data layer" in guide
    assert "Descend only after a successful metric response" in guide
    assert "does not establish that the requested date or other parameters are invalid" in reference


def test_timeline_health_probe_omits_unsupported_pagination():
    script = read("scripts/zoodata.py")
    timeline_probe = script.split(
        '"keywords/product-traffic-terms-timeline"', 1
    )[1].split('"ASIN + keyword timeline"', 1)[0]

    assert '"pageSize"' not in timeline_probe


def test_scenarios_are_capability_guides_without_independent_scoring_or_gates():
    for relative_path in (
        "references/scenarios-expand.md",
        "references/scenarios-keyword-analysis.md",
        "references/scenarios-reverse-asin.md",
        "references/scenarios-keyword-traffic-diagnosis.md",
    ):
        text = read(relative_path)
        assert "Capability Guide" in text.splitlines()[0]
        assert "execution-guide.md" in text
        assert "downstream scenario" in text
        assert "must align upward" in text
        assert "Task Constraints" not in text
        assert "Evidence-to-Action Protocol" not in text
        assert "Cross-Metric Reconciliation Protocol" not in text


def test_all_scenarios_inherit_and_preserve_stage_handoff_closure_gate():
    scenarios = sorted((ROOT / "references").glob("scenarios-*.md"))
    assert len(scenarios) == 4

    vague_transition = re.compile(
        r"\b(?:if|when)\b[^|]*(?:needed|wanted)\b",
        re.IGNORECASE,
    )
    for path in scenarios:
        text = path.read_text(encoding="utf-8")
        assert "`Stage Handoff Closure Gate`" in text, path.name
        assert "one optional next input" not in text, path.name

        in_journey = False
        for line in text.splitlines():
            if line == "## User journey":
                in_journey = True
                continue
            if in_journey and line.startswith("## "):
                break
            if in_journey and line.startswith("|") and vague_transition.search(line):
                raise AssertionError(
                    f"{path.name} has a vague journey transition: {line}"
                )


def test_scenarios_keep_their_user_input_journeys():
    target = read("references/scenarios-keyword-analysis.md")
    expand = read("references/scenarios-expand.md")
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## User journey" in target
    assert "target ASIN" in target
    assert "ABA-SQP" in target
    assert "### Stage transition gate" in target
    assert "evidence → analysis → stage conclusion" in target
    assert "followed by a next input only when the journey row defines one" in target
    assert "Do not request an ASIN until Stage 1" in target
    assert "Do not request price, contribution margin" in target
    assert "stop without another call, analysis verdict, or next-stage input request" in target
    assert "4. Seller-funnel calibration" in target
    assert "5. Ads-economics calibration" in target
    assert "This section is mandatory for the multi-stage journey" in target
    assert "never hide the request in the conclusion paragraph" in target
    assert "after Stage 1, request only the target ASIN" in target
    assert "sqp-field-semantics.md" in target
    assert "### Seller-data input guidance" not in target
    assert "acquisition, sequencing, sufficiency, and field-interpretation rules" in target
    assert "worth targeting" in target
    assert "`product-traffic-terms-timeline`" not in target
    assert "Route movement, anomaly, and causal questions" in target
    assert "movement posture" not in target
    for text in (expand, reverse, diagnosis):
        assert "## User journey" in text
        assert "sqp-field-semantics.md" in text

    for text in (target, expand, reverse, diagnosis):
        assert "Interactive Stage Gate" in text


def test_expansion_does_not_define_an_undocumented_composite_score():
    scenario = read("references/scenarios-expand.md")

    assert "Suggested weight" not in scenario
    assert "35 |" not in scenario
    assert "market-screen score" not in scenario
    assert "High validation priority" in scenario
    assert "Existing-fit validation" in scenario
    for action_label in ("Priority test", "Selective test", "Harvest", "`Avoid`"):
        assert action_label not in scenario
    assert "Advance to ASIN validation" in scenario
    assert "Do not request SQP before the ASIN observation and candidate-validation conclusion" in scenario
    assert "sqp-field-semantics.md" in scenario
    assert "| 1. Candidate recall" in scenario
    assert "| 2. Market screening" in scenario
    assert "Do not call `market-profile` before the Stage 1 candidate list is confirmed" in scenario
    assert "do not combine candidate recall, market screening, and ASIN validation into one report" in scenario
    assert "are transition labels" in scenario
    assert "makes the ASIN the mandatory next input" in scenario
    assert "advance a candidate to seller-funnel validation" in scenario
    assert "makes one SQP artifact the mandatory next input" in scenario
    assert "Do not phrase the ASIN or SQP handoff" in scenario
    assert "if product-specific prioritization is wanted" not in scenario
    assert "If seller calibration is needed" not in scenario


def test_reverse_asin_preserves_optional_routes_and_candidate_progression():
    scenario = read("references/scenarios-reverse-asin.md")

    assert "| 1. Traffic-term discovery" in scenario
    assert "| 2. Candidate keyword examination" in scenario
    assert "| 3. Seller-funnel calibration" in scenario
    assert "| 4. Ads-economics calibration" in scenario
    assert "Seller-data handoff" not in scenario
    assert "### Stage transition gate" in scenario
    assert "A raw-list-only request must be explicit" in scenario
    assert "a raw-list-only request ends without a confirmation request" in scenario
    assert "omit it for a raw-list-only request" in scenario
    assert "Stage 1 is discovery, not keyword judgment" in scenario
    assert "A generic full-analysis request does not authorize automatic progression" in scenario
    assert "Do not call `market-profile` before that confirmation" in scenario
    assert "Advance to Stage 2 only when the candidate list was explicitly confirmed" in scenario
    assert "A reply such as “确认 / 继续 / 就分析这些词” is sufficient" in scenario
    assert "Every candidate included in the Stage 2 posture conclusion must have completed market-profile validation" in scenario
    assert "`realtime/product` for the target ASIN" in scenario
    assert "sufficient directly observed ASIN/product-fit evidence" in scenario
    assert "without sufficient direct product-fit evidence remain unvalidated" in scenario
    assert "Assigning this label means seller-funnel calibration is the required next stage" in scenario
    assert "If any candidate receives `Headroom validation`" in scenario
    assert "render a separate mandatory SQP next-input request" in scenario
    assert "assigning `Headroom validation` makes seller-funnel calibration necessary by definition" in scenario
    assert "never a `Final calibrated conclusion`" in scenario
    assert "turn that required handoff into an optional offer" in scenario
    assert "include the mandatory separate SQP next-input section" in scenario
    assert "For Stage 1, render localized sections in this order and then stop" in scenario
    assert "asking the user to confirm the list or name additions/removals" in scenario
    assert "Do not collapse the two stages into one response, auto-run Stage 2" in scenario
    assert "move the SQP request directly after the traffic-source table" in scenario
    assert "## Posture labels" in scenario
    assert "Use these labels only after Stage 2 candidate market validation" in scenario
    for label in ("`Established posture`", "`Headroom validation`", "`Observe`", "`No current support`"):
        assert label in scenario
    for action_label in ("`Defend`", "`Expand`", "`Avoid`"):
        assert action_label not in scenario
    assert "sole source for acquisition, sequencing, sufficiency, and field interpretation" in scenario
    assert "a sponsored-only row or selected Top-N subset does not establish overall advertising dependence" in scenario
    assert "algorithmic recognition, or organic improvement potential" in scenario
    assert "Do not call coverage `full`, `complete`, or `stable`" in scenario


def test_reverse_and_diagnosis_have_exclusive_question_boundaries():
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## Scenario boundary" in reverse
    assert "does not diagnose temporal movement, anomalies, or causes" in reverse
    assert "Route them to `scenarios-keyword-traffic-diagnosis.md`" in reverse
    assert "Do not call `product-traffic-terms-timeline` or `product-traffic-terms-overview`" in reverse
    assert "| ASIN × keyword movement |" not in reverse
    assert "Aggregate ASIN traffic movement" not in reverse
    assert "returned listing-event signals" not in reverse

    assert "## Scenario boundary" in diagnosis
    assert "owns temporal movement, anomaly, and causal questions" in diagnosis
    assert "Do not produce a full current traffic-term map, candidate pool" in diagnosis
    assert "| 1A. ASIN-wide anomaly triage" in diagnosis
    assert "| 1B. ASIN × keyword diagnosis" in diagnosis
    assert "select a target keyword for diagnosis or confirm a separate reverse-ASIN discovery stage" in diagnosis
    assert "Stage 1A ends only with a target-keyword selection request" in diagnosis
    assert "do not request SQP there" in diagnosis


def test_diagnosis_keeps_alert_semantics_and_artifact_guidance():
    scenario = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## Alert-level meaning" in scenario
    assert "magnitude and persistence of the observed movement" in scenario
    assert "not confidence in its cause" in scenario
    assert "sqp-field-semantics.md" in scenario
    assert "instead of redefining them here" in scenario
    assert "seller-funnel evidence as the exact next evidence" in scenario
    assert "the next-input request is mandatory" in scenario
    assert "one required next input when the conclusion carries a named unresolved question forward" in scenario
    assert "one optional next input" not in scenario


def test_target_keyword_candidate_advancement_requires_explicit_sqp_handoff():
    scenario = read("references/scenarios-keyword-analysis.md")

    assert "advances any term for seller-funnel validation" in scenario
    assert "render a separate mandatory SQP next-input request" in scenario
    assert "makes seller-funnel calibration necessary by definition" in scenario
    assert "Request one SQP artifact directly" in scenario
    assert "when seller-funnel calibration is wanted" not in scenario


def test_api_reference_remains_the_contract_source():
    reference = read("references/reference.md")

    assert "production capability whitelist" in reference
    assert "Billing is per `status=ok` item for `detail`, `market-profile`, `trend`, and timeline" in reference
    assert "`trend-profile` bills a keyword when at least one requested window row has `status=ok`" in reference
    assert "Do not estimate billing from request size" in read("references/execution-guide.md")
    assert "keywords/market-profile" in reference
    assert "keywords/product-traffic-terms-timeline" in reference
    assert "not an exhaustive root-keyword universe" in reference
    assert "do not sum their search counts" in reference
    assert "### Capability-to-contract matrix" in reference
    assert "### Access priority: metric first, data on demand" not in reference
    assert "tested batch currently returned HTTP 500" not in reference
    assert "Current service failure boundary" not in reference
    assert "| `keywords/market-profile` | metric | published and available |" in reference


def test_reference_stays_contract_local_and_scenarios_own_selection():
    skill = read("SKILL.md")
    reference = read("references/reference.md")

    assert "`reference.md` owns only production API and acquisition-surface facts" in skill
    assert "Scenario files own only scenario-specific capability selection" in skill
    assert "Apply each rule from its responsible owner module above" in skill
    assert "try `phrase` and `fuzzy`" not in reference
    assert "Use the routes in this order" not in reference
    assert "Aggregate usage by route" not in reference


def test_full_mode_scenario_shapes_align_with_top_level_output_order():
    expand = read("references/scenarios-expand.md")
    target = read("references/scenarios-keyword-analysis.md")
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## [Localized Data Notes title]" in expand
    assert "## [Localized Evidence title]" in expand
    assert "## [Localized Analysis title]" in expand
    assert "## [Localized Stage Conclusion title]" in expand
    assert "Data Notes, Evidence, Analysis, Stage Conclusion" in target
    assert "1. Data Notes." in reverse
    assert "2. Stage 1 traffic evidence." in reverse
    assert "3. Stage 1 analysis." in reverse
    assert "Data Notes, observed change/evidence, analysis or explanation status" in diagnosis


def test_supporting_acquisition_is_whitelisted_and_search_surfaces_stay_distinct():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    reference = read("references/reference.md")

    for route in (
        "`realtime/product`",
        "WebTools `/search`",
        "WebTools `/scrape`",
        "WebTools `/scrape-interactive`",
    ):
        assert route in reference

    assert "## Authorized supporting acquisition surfaces" in reference
    assert "`realtime/product` | `product`" in reference
    assert "exposed ZooData WebTools session/callable surface" in reference
    assert "WebTools `/search` is not `products/search`" in guide
    assert "Use WebTools `/search` only when the URL must first be discovered" in guide
    assert "WebTools `/search` is permitted URL discovery; it is not `products/search`" in skill
    assert "Never use `products/search`" in skill


def test_global_boundaries_remain_in_the_router():
    skill = read("SKILL.md")

    assert "`products/search`" in skill
    assert "external browser automation" in skill
    assert "ABA-SQP conversion funnel" in skill
    assert "status=empty" in skill


def test_seller_data_requests_use_progressive_artifact_guidance():
    guide = read("references/execution-guide.md")
    semantics = read("references/sqp-field-semantics.md")

    assert "Request one report or view at a time" in guide
    assert "Do not ask the user to provide SQP and Ads data in the same next-input step" in guide
    assert "ask for that artifact instead of making the user transcribe or assemble a field list" in guide
    assert "### User-facing SQP acquisition" in semantics
    assert "state the request directly in a separate next-input section" in semantics
    assert "not a choice about whether to continue" in semantics
    assert "Do not introduce the request with optional wording" in semantics
    assert "latest completed reporting week, and target-query scope" in semantics
    assert "click the page's `Download` control and upload the original CSV unchanged" in semantics
    assert "Do not enumerate the full SQP schema in the request" in semantics
    assert "One completed week is sufficient for the initial current-period funnel judgment" in semantics
    assert "Do not default to requesting 4–8 weeks" in semantics
    assert "### Later Ads acquisition" in semantics
    assert "Do not request Ads data together with SQP" in semantics
    assert "Measurement & Reporting → Sponsored ads reports → Create report" in semantics
    assert "Reporting → Create report" in semantics
    assert "`Sponsored Products` as the ad product/campaign type" in semantics
    assert "`Search term` as the report type" in semantics
    assert "After its status is complete, download the original CSV" in semantics


def test_usage_counts_discarded_calls_and_unsupported_seasonality_is_omitted():
    guide = read("references/execution-guide.md")
    market_semantics = read("references/metrics-market-profile.md")

    assert "Count every API call actually executed" in guide
    assert "whose output was later discarded" in guide
    assert "A local parse failure does not erase the preceding call" in guide
    assert "When `annualSeasonality` is unsupported" in market_semantics
    assert "omit seasonal timing and seasonal-cause narratives entirely" in market_semantics
    assert "Hedging with `may`, `might`, `possibly`, or `可能`" in market_semantics


def test_seller_acquisition_details_have_one_source():
    for relative_path in (
        "references/scenarios-expand.md",
        "references/scenarios-keyword-analysis.md",
        "references/scenarios-reverse-asin.md",
        "references/scenarios-keyword-traffic-diagnosis.md",
    ):
        scenario = read(relative_path)
        assert "sqp-field-semantics.md" in scenario
        assert "Measurement & Reporting → Sponsored ads reports → Create report" not in scenario
        assert "latest completed reporting week" not in scenario
        assert "upload either one screenshot" not in scenario
        assert "original downloaded CSV" not in scenario
