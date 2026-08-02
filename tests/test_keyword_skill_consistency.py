"""Structural and safety guardrails for the keyword-analysis skill."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "amazon-keyword-traffic-analysis"


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_keyword_skill_source_contains_no_cjk_text():
    cjk = re.compile(r"[\u4e00-\u9fff]")

    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        assert not cjk.search(text), path.relative_to(ROOT)


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
    assert "references/evidence-protocols.md" in skill
    assert "references/diagnosis-action-protocols.md" in skill
    assert "references/output-rules.md" in skill
    assert "For a single lookup, also load only" in skill
    assert "For every full-mode request, load the complete" in skill
    assert "use `output-rules.md § Quick Mode Output`" in skill
    assert "do not load a scenario unless the follow-up broadens the request" in skill
    assert "The guide is the sole scenario/stage and Gate contract" in skill
    assert "Do not load it for a non-diagnostic stage" in skill
    assert "for every request handled by this skill, including a single lookup" not in skill
    assert "### Two-Pass Metric Interpretation Gate" not in skill
    assert "### Evidence-to-Action Authorization Gate" not in skill
    assert "### Candidate Validation Rule" not in skill
    assert "current traffic terms, traffic-source structure, candidate discovery" in skill
    assert "This diagnosis route takes precedence" in skill
    assert "ASIN traffic-structure diagnosis through reverse ASIN" in skill
    assert "ASIN traffic-change diagnosis" in skill
    assert "First apply the ambiguity check to every generic ASIN-scoped keyword-traffic diagnosis request" in skill
    assert "analyze this ASIN from a keyword-traffic angle" in skill
    assert "Exact phrase matching is not required" in skill
    assert "The absence of change language does not imply traffic-structure intent" in skill
    assert "Before emitting any user-facing text or making any evidence call" in skill
    assert "output-rules.md § Retrieval Progress Updates" in skill
    assert "Make those reference reads the first actions" in skill
    assert "without a preceding or interstitial assistant message" in skill
    assert "never announce that a clarification rule or reference must be loaded" in skill
    assert "without an intervening progress update" in skill
    assert "Do not select or load either diagnosis scenario until the user chooses a route" in skill
    assert "This check does not apply when the user names a target keyword" in skill
    assert "Route an explicit target keyword + ASIN question" in skill
    assert "to target-keyword analysis" in skill
    assert "ASIN-wide change/anomaly diagnosis without a named keyword" in skill
    assert "Route to one applicable scenario, or multiple non-exclusive scenarios" in skill
    assert "Load exactly one scenario" not in skill
    assert "Before requesting or interpreting a seller artifact" in skill
    assert "Without `--endpoints` or `--keyword-endpoints`, it makes no evidence calls" in skill


def test_source_of_truth_boundaries_define_exclusive_module_ownership():
    skill = read("SKILL.md")
    output = read("references/output-rules.md")

    assert "This file owns only trigger classification, reference loading, scenario routing" in skill
    assert "must not define endpoint contracts, shared workflow procedures, field semantics" in skill
    assert "`reference.md` owns only production API and acquisition-surface facts" in skill
    assert "must not define Agent workflow, action/output policy, business interpretation" in skill
    assert "`execution-guide.md` owns only the shared scenario/stage schema" in skill
    assert "Gate order/decisions, evidence-level conclusion ceilings" in skill
    assert "must not redefine API contracts, field meanings, detailed evidence procedures" in skill
    assert "`evidence-protocols.md` owns only shared evidence planning" in skill
    assert "must not select stages, define Gate outcomes, render handoff lists" in skill
    assert "`diagnosis-action-protocols.md` owns only the detailed causal-diagnosis" in skill
    assert "must not select stages, define the Diagnostic Closure Gate result" in skill
    assert "`output-rules.md` owns only user-facing language, progress updates" in skill
    assert "must not select stages, define Gate outcomes, change conclusion authority" in skill
    assert "`traffic-observation-semantics.md`) own only" in skill
    assert "must not define production availability or request parameters, shared workflow policy" in skill
    assert "`sqp-field-semantics.md` owns seller-artifact acquisition order, schema identity" in skill
    assert "must not define ZooData API contracts or scenario-specific stage triggers and conclusions" in skill
    assert "Scenario files own only scenario-specific stage entry requirements, capability selection, conclusion authority, and section-content requirements" in skill
    assert "They define evidence levels, not report headings/order, workflow-completion states" in skill
    assert "must not restate, relax, replace, or create exceptions" in skill
    assert "For the documented keyword endpoints and `realtime/product` used by this skill" in skill
    assert "`{skill_base_dir}/scripts/zoodata.py` owns deterministic transport retries" in skill
    assert "machine-readable Agent-control signal vocabulary" in skill
    assert "Within those command paths, it must not define field meaning" in skill
    assert "Other commands bundled in the shared CLI remain outside this skill's responsibility map" in skill
    assert "must not define field meaning, stage selection, evidence interpretation" in skill
    assert "`execution-guide.md` owns the Gate behavior and `output-rules.md` owns rendered prose" in skill
    assert "The credential-only `check` path and opt-in endpoint probes are diagnostic utilities outside this evidence-command contract" in skill
    assert "`README.md` is a human-facing package overview and module index only" in skill
    assert "must not define or modify runtime routing" in skill
    assert "Cross-module references are allowed; cross-module redefinition and duplicated policy are not" in skill
    assert "split API fact, shared workflow consequence, field interpretation, and scenario application" in skill
    assert "Apply each rule from its responsible owner module above" in skill
    assert "A downstream module may narrow behavior but must not override an owner contract" in skill
    assert "surface it for discussion" not in skill
    assert "changing a top-level owner contract" not in skill
    assert "maintainer" not in skill.lower()
    assert "Do not load or render a scenario stage" not in output
    assert "Do not combine multiple stage conclusions" not in output
    assert "insert future-stage evidence" not in output


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
    evidence_headings = headings("references/evidence-protocols.md")
    diagnosis_headings = headings("references/diagnosis-action-protocols.md")
    output_headings = headings("references/output-rules.md")
    semantic_paths = (
        "references/metrics-market-profile.md",
        "references/metrics-trend-profile.md",
        "references/serp-and-rollover.md",
        "references/traffic-observation-semantics.md",
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
        "Required Validation Handoff Rule",
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
        "Cross-Metric Reconciliation Protocol",
        "Evidence Coverage Protocol",
        "Evidence-to-Action Protocol",
        "Quick Mode Output",
        "Usage Accounting Rule",
    })
    assert "Cross-Metric Reconciliation Protocol" in evidence_headings
    assert "Evidence Coverage Protocol" in evidence_headings
    assert "Evidence-to-Action Protocol" in diagnosis_headings
    assert "User-Facing Output Boundary" in output_headings
    assert "Usage Accounting Rule" in output_headings
    assert evidence_headings.isdisjoint({
        "Interactive Stage Gate",
        "Interface Failure Stop Gate",
        "Stage-End Selection List Rule",
        "Diagnostic Closure Gate",
    })
    assert diagnosis_headings.isdisjoint({
        "Interactive Stage Gate",
        "Diagnostic Closure Gate",
        "Stage-End Selection List Rule",
    })
    assert output_headings.isdisjoint({
        "Interactive Stage Gate",
        "Interface Failure Stop Gate",
        "Stage-End Selection List Rule",
    })
    for path in semantic_paths:
        assert headings(path).isdisjoint({
            "Production availability",
            "Common keyword endpoint contract",
            "Cross-metric reconciliation framework",
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
    assert "preserves the authoritative outer status for every parsed HTTP response" in reference
    assert "Response-body or nested status-like fields do not override it" in reference
    assert "HTTP 422 means request validation failed" in reference
    assert "HTTP 5xx after the client's built-in retries means the service is currently unavailable" in reference
    assert "preserves the outer HTTP status in `error.status`" in reference
    assert "sets `error.retryExhausted=true` when that retry budget is consumed" in reference
    assert "Response-body text or a nested non-5xx-like error does not change" in reference
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
    assert "#### HTTP 5xx Decision Blacklist" in guide
    assert "Inspect the authoritative HTTP transport status before interpreting any response-body field" in guide
    assert "If that status is in the `500–599` range" in guide
    assert "Only a result whose authoritative transport status is outside the `500–599` range" in guide
    assert "the outer transport status controls classification" in guide
    assert "A response body that resembles a validation, credential, credit, parameter" in guide
    assert "Never use response-body content to reinterpret a 5xx" in guide
    assert "Do not execute any subsequent API or tool command in that turn" in guide
    assert "Parameter correction is available only after the authoritative HTTP transport status" in guide
    assert "outside `500–599`" in guide
    assert "A valid `status=empty` may justify a separately supported alternate query or period" in guide
    assert "Route credential failure, credit failure, and the reference-classified validation response" not in guide
    assert "`error.retryExhausted=true`" not in guide
    assert "HTTP 422 is a parameter validation error" not in guide

    # The CLI owns deterministic retry mechanics, technical failure state, and
    # control-signal vocabulary; the guide owns triggered behavior and output.
    assert '"STOP_CURRENT_TURN. APPLY_SKILL_INTERFACE_FAILURE_TEMPLATE. "' in script
    assert '"DO_NOT_SELECT_ANOTHER_COMMAND."' in script
    assert 'result["error"]["retryExhausted"] = True' in script
    assert 'data["_transport"] = {"status": transport_status}' in script
    assert "workflowDisposition" not in script
    assert "retryPolicy" not in script
    assert "parameterMutationAllowed" not in script

    # Scenarios inherit the shared gate and cannot redefine transport recovery.
    for scenario in scenarios:
        assert "workflowDisposition" not in scenario
        assert "retryPolicy" not in scenario
        assert "parameterMutationAllowed" not in scenario
        assert "HTTP 5xx" not in scenario


def test_execution_guide_is_the_core_stage_and_gate_source():
    guide = read("references/execution-guide.md")
    output = read("references/output-rules.md")

    assert "## Authority and routing" in guide
    assert guide.index("## Contents") < guide.index("## Authority and routing")
    assert "## Scenario contract" in guide
    assert "## Stage schema" in guide
    assert "## Shared evidence levels" in guide
    assert "## Stage execution sequence" in guide
    assert "## Gate order" in guide
    assert "[Structured Field Identity Gate](#structured-field-identity-gate)" in guide
    assert "[ASIN Traffic Diagnosis Intent Clarification Gate](#asin-traffic-diagnosis-intent-clarification-gate)" in guide
    assert "[Stage Handoff Closure Gate](#stage-handoff-closure-gate)" in guide
    assert "[Stage-End Selection List Rule](#stage-end-selection-list-rule)" in guide
    assert "[Final Output Gate](#final-output-gate)" in guide
    assert "[Pending Handoff Reclassification Rule](#pending-handoff-reclassification-rule)" in guide
    assert "[Interface Failure Stop Gate](#interface-failure-stop-gate)" in guide
    assert "[HTTP Validation Rule](#http-validation-rule)" in guide
    assert "[Credential and Credit Failures](#credential-and-credit-failures)" in guide
    assert "question → scenario → active stage → stage evidence → Gate checks" in guide
    assert "shared scenario/stage structure, Gate order and decisions" in guide
    assert "Scenario files define scenario-specific stage entry requirements" in guide
    assert "workflow-completion states, automatic progression, Gate exceptions" in guide
    assert "Every scenario stage row must contain exactly these runtime roles" in guide
    assert "| `Stage` |" in guide
    assert "| `Entry input` |" in guide
    assert "| `Evidence` |" in guide
    assert "| `Conclusion authority` |" in guide
    assert "Do not add a transition, completion, next-stage trigger" in guide
    assert "Retrieval and interpretation remain separate operations inside the stage" in guide
    assert "Two-Pass" not in guide
    assert "### ASIN Traffic Diagnosis Intent Clarification Gate" in guide
    assert "lacking an explicit desired output that distinguishes the two valid diagnosis types" in guide
    assert "Do not select a scenario, inspect product/keyword evidence, or execute an API/tool evidence call" in guide
    assert "Make the localized clarification question or heading and the following numbered list the first user-visible content" in guide
    assert "Omit progress preambles and internal process explanations" in guide
    assert "Do not expose the skill, Gate, scenario/module names" in guide
    assert "Traffic-structure diagnosis" in guide
    assert "Traffic-change diagnosis" in guide
    assert "Ask another question or end this analysis" in guide
    assert "with no description or explanatory suffix" in guide
    assert "enter a different question or state that no further analysis is needed" not in guide
    assert "Do not mark a diagnosis route as recommended" in guide
    assert "Treat the user's displayed final-list number, localized label, or equivalent natural-language reply" in guide
    assert "### Interactive Stage Gate" in guide
    assert "### Stage Handoff Closure Gate" in guide
    assert "Re-read the user's still-current question and the current stage conclusion" in guide
    assert "current decision still requires another evidence level or subject" in guide
    assert "a scenario stage names the exact `Entry input`" in guide
    assert "If one ASIN, candidate-set confirmation, report, file, or field is required" in guide
    assert "Do not assume that every stage must be visited" in guide
    assert "### Stage-End Selection List Rule" in guide
    assert "Every normally completed full-mode stage must end with one concise localized numbered selection list" in guide
    assert "Use the list even when there is only one supported continuation" in guide
    assert "For one required ASIN, confirmation, report, file, or field" in guide
    assert "`1` is the only item and is the fixed new-question/exit choice" in guide
    assert "reply with the displayed final-list number or label" in guide
    assert "one or more final-list numbers or the displayed select-all item when set selection is supported" in guide
    assert "recommended" in guide
    assert "Do not auto-select an item" in guide
    assert "This list is an interaction contract, not a workflow status" in guide
    assert "The user is never required to continue" in guide
    assert "### Final Output Gate" in guide
    assert "immediately before every user-facing send" in guide
    assert "Validate the entire draft from its first emitted character through its last emitted character" in guide
    assert "discard the entire draft and render the selected route again" in guide
    assert "validate the complete draft exclusively against `output-rules.md § Interface Failure Output`" in guide
    assert "exactly three localized non-empty plain-text lines" not in guide
    assert "Do not send until the complete assistant draft passes the selected route" in guide
    assert "Client-generated task notifications are outside this assistant-output validation boundary" in guide
    for obsolete_state in ("`complete`", "`advance`", "`unresolved`"):
        assert obsolete_state not in guide
    assert "### Pending Handoff Reclassification Rule" in guide
    assert "does not reserve the next turn" in guide
    assert "classify the user's actual latest message through `SKILL.md`" in guide
    assert "Continue a pending validation only when the message selects its item" in guide
    assert "If a selected item still lacks its ASIN, artifact, candidate set, or field" in guide
    assert "Re-render the smallest executable selection list" in guide
    assert "If the user selects the fixed final item, asks a new question" in guide
    assert "leave the previous handoff inactive" in guide
    assert "Do not treat arbitrary prose as an ASIN/artifact" in guide
    assert "Complete at most one user-decision stage per assistant turn" in guide
    assert "Do not combine several stage conclusions" in guide
    assert "Retain compatible later-stage data supplied early without interpreting it" in guide
    assert "### Cross-Metric Reconciliation Protocol" not in guide
    assert "### Evidence-to-Action Protocol" not in guide
    assert "## Quick Mode Output" not in guide
    assert "## Usage Accounting Rule" not in guide
    assert "### Candidate Validation Rule" in guide
    assert "### Interface Failure Stop Gate" in guide
    assert "Stop the workflow immediately" in guide
    assert "Do not call another endpoint" in guide
    assert "do not request asin, price, margin, sqp, ads" in guide.lower()
    assert "local parsing, transformation, extraction, or formatting command that fails" in guide
    assert "Never call the same paid endpoint again merely to change output format" in guide
    assert "HTTP 5xx User-Facing Template" not in guide
    assert "`output-rules.md § Interface Failure Output`" in guide
    assert "## Interface Failure Output" in output
    assert "`Service is currently unavailable. Please try again later.`" in output
    assert "Do not execute any subsequent API or tool command in that turn" in guide
    assert "select another date, marketplace, subject, filter, pagination value, endpoint, or surface" in guide
    assert "Parameter correction is available only after the authoritative HTTP transport status is outside" in guide
    assert "A valid `status=empty` may justify a separately supported alternate query or period" in guide
    assert "Never transfer either behavior to HTTP 5xx" in guide
    assert "evidence → analysis → stage conclusion" in guide
    assert "Treat traffic-structure diagnosis through reverse ASIN and traffic-change diagnosis as mutually exclusive active routes" in guide
    assert "Apply the clarification gate when neither meaning is explicit" in guide
    assert "give traffic-change diagnosis precedence" in guide
    assert "Combine scenario capabilities only when scenario boundaries are non-exclusive" in guide


def test_support_protocols_are_progressively_loaded_and_do_not_own_stage_flow():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    evidence = read("references/evidence-protocols.md")
    diagnosis = read("references/diagnosis-action-protocols.md")
    output = read("references/output-rules.md")

    assert len(guide.splitlines()) < 350
    assert "For every full-mode request" in skill
    assert "For a causal, anomaly, or action question" in skill
    assert "Load `references/output-rules.md`" in skill

    assert "owns shared evidence planning, retrieval, interpretation" in evidence
    assert "does not select stages, define Gate outcomes" in evidence
    assert "## Cross-Metric Reconciliation Protocol" in evidence
    assert "## Cross-Stage Evidence Continuity Protocol" in evidence
    assert "Stage-End Selection List Rule" not in evidence

    assert "owns detailed causal-diagnosis and evidence-to-action procedures" in diagnosis
    assert "returns its result to the Gate system" in diagnosis
    assert "## Evidence-Seeking Diagnosis Protocol" in diagnosis
    assert "## Evidence-to-Action Protocol" in diagnosis
    assert "Diagnostic Closure Gate" not in {
        line.lstrip("#").strip()
        for line in diagnosis.splitlines()
        if line.startswith("#")
    }

    assert "owns user-facing language, progress updates, report rendering" in output
    assert "does not define stage selection, conclusion authority, Gate outcomes" in output
    assert "## Full-Mode Stage Output" in output
    assert "## Usage Accounting Rule" in output
    assert "Stage-End Selection List Rule" not in {
        line.lstrip("#").strip()
        for line in output.splitlines()
        if line.startswith("#")
    }


def test_user_facing_output_boundary_hides_internal_failure_policy():
    guide = read("references/execution-guide.md")
    output = read("references/output-rules.md")
    scenarios = [
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "references").glob("scenarios-*.md"))
    ]

    assert "## User-Facing Output Boundary" in output
    assert "### CLI Error Isolation" in output
    assert "Keep execution control separate from user communication" in output
    assert "Do not expose rule names, ownership, Gate decisions" in output
    assert "Surface technical diagnostics only when the user asks" in output
    assert "Treat CLI/tool error payloads as Agent-only diagnostics" in output
    assert "Do not quote or paraphrase internal `message`, `action`" in output
    assert "The CLI never owns final prose" in output
    assert "When no specific template exists, state the smallest localized outcome" in output
    assert "## Interface Failure Output" in output
    assert "For any hard interface-failure stop selected by `execution-guide.md`" in output
    assert "For an HTTP 5xx hard stop" not in output
    assert "`Service is currently unavailable. Please try again later.`" in output
    assert "`Succeeded interfaces: {comma-separated endpoint identifiers, or None}`" in output
    assert "`Failed interfaces: {comma-separated endpoint identifiers}`" in output
    assert "Preserve endpoint identifiers exactly as documented" in output
    assert "only from calls completed in the current turn" in output
    assert "exactly three non-empty plain-text lines with no blank lines" in output
    assert "The first emitted character must belong to the localized first line" in output
    assert "the last emitted character must belong to the failed-interface identifier on the third line" in output
    assert "Add no content before or after the template" in output
    assert "Do not add Markdown headings, emphasis, code formatting" in output
    assert "suggestion to ask another question" in output
    assert "`error.retryExhausted=true`" not in guide
    assert "Do not add a heading, HTTP status, retry count" in output
    assert "successful-interface data, partial analysis, API-usage section" in output
    assert "action guidance, or stage-end list" in output
    assert "bypasses normal stage rendering and the stage-end list" in output
    assert "report the interface error" not in "\n".join(scenarios)


def test_final_output_gate_is_loaded_on_every_rendering_path():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    evidence = read("references/evidence-protocols.md")

    assert "`execution-guide.md § Final Output Gate`" in skill
    assert "`Final Output Gate`" in skill
    assert "For every full-mode request, load the complete `references/execution-guide.md`" in skill
    assert "Quick Mode still applies the Structured Field Identity Gate, Interface Failure Stop Gate, and Final Output Gate" in guide
    assert "Apply the Final Output Gate to the complete rendered response immediately before sending it" in guide
    assert "invoke `Monitor`" not in evidence
    assert "Never background a CLI evidence command" not in evidence


def test_final_output_gate_rejects_internal_stage_identifier_leakage():
    guide = read("references/execution-guide.md")
    output = read("references/output-rules.md")

    assert "## Internal Identifier Rewrite" in output
    assert "A user-facing rendering is invalid" in output
    assert "`Stage 1B direct ASIN evidence` as `ASIN traffic-term observations`" in output
    assert "`Stage 2 product-fit evidence` as `candidate keyword market and product-fit evidence`" in output
    assert "explicit whole-draft rejection check" in guide
    assert "Keep all identifier definitions, examples, and rewrite requirements authoritative in that output owner" in guide
    assert "even when embedded in a longer evidence description or parenthetical" not in guide
    assert "then repeat the check from the first character" not in guide

    internal_stage_identifier = re.compile(
        r"(?i)(?:\bstage|\u9636\u6bb5)\s*\d+[a-z]?(?:\s*[\u2013-]\s*\d*[a-z]?)?"
    )
    leaked_drafts = (
        "Validated with Stage 1B direct ASIN evidence.",
        "Evidence (Stage 1B): direct ASIN appearance.",
        "\u57fa\u4e8e\u5e02\u573a\u753b\u50cf\u4e0e Stage 1B \u76f4\u63a5 ASIN \u51fa\u73b0\u8bc1\u636e\u8fdb\u884c\u7efc\u5408\u9a8c\u8bc1\u3002",
        "\u9636\u6bb5 1B \u7684 ASIN \u6d41\u91cf\u8bcd\u8bc1\u636e\u3002",
        "Carried evidence from Stage 1B\u20132.",
    )
    safe_drafts = (
        "Validated with ASIN traffic-term observations.",
        "\u7efc\u5408\u5e02\u573a\u753b\u50cf\u4e0e ASIN \u6d41\u91cf\u8bcd\u89c2\u5bdf\u8fdb\u884c\u9a8c\u8bc1\u3002",
        "Candidate keyword market and product-fit evidence remains incomplete.",
    )

    assert all(internal_stage_identifier.search(draft) for draft in leaked_drafts)
    assert all(not internal_stage_identifier.search(draft) for draft in safe_drafts)


def test_retrieval_progress_describes_actions_without_exposing_control_flow():
    output = read("references/output-rules.md")
    progress = output.split("## Retrieval Progress Updates", 1)[1].split("\n## ", 1)[0]

    assert "may say only what is being done for the user's question" in output
    assert "which internal condition fired" in output
    assert "which instruction selected the action" in output
    assert "`observation → control decision → action` narrative" in output
    assert "Complete internal preparation silently" in progress
    assert "Never announce the loading, selection, or application of internal instructions or resources" in progress
    assert "request it directly without a progress preamble" in progress
    assert "Keep intermediate control flow silent" in progress
    assert "caused the next method, parameter, source, scope, or action" in progress
    assert "only when it is requested evidence, materially affects the completed answer, or requires user action" in progress
    assert "Never use it as process justification for the next internal action" in progress
    assert "state only the direct user-domain action" in progress
    assert "Natural examples" not in progress
    assert "Forbidden example" not in progress
    for special_case in (
        "clarification",
        "reference reads",
        "marketplace",
        "seller-calibration",
        "Stage 1",
        "product-traffic-terms",
        "realtime/product",
    ):
        assert special_case not in progress


def test_top_level_localization_preserves_exact_enums_and_localizes_usage_labels():
    output = read("references/output-rules.md")

    assert "human-readable statuses" in output
    assert "Retain an enum such as `status=empty` exactly" in output
    assert "| [Localized endpoint header] | [Localized calls header] | [Localized credits header] |" in output
    assert "| [Localized total label] | 1 | 1 |" in output
    assert "localized credits-remaining label" in output
    assert "localized `not returned`" in output
    assert "`| Endpoint | Calls | Credits |`" not in output
    assert "`Credits remaining: N`" not in output


def test_interface_failure_never_descends_to_data_layer():
    guide = read("references/execution-guide.md")
    evidence = read("references/evidence-protocols.md")
    reference = read("references/reference.md")

    assert "Do not call another endpoint" in guide
    assert "descend to a data layer" in guide
    assert "Descend only after a successful metric response" in evidence
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


def test_all_scenarios_inherit_stage_handoff_closure_gate():
    scenarios = sorted((ROOT / "references").glob("scenarios-*.md"))
    assert len(scenarios) == 4

    for path in scenarios:
        text = path.read_text(encoding="utf-8")
        assert "`Stage Handoff Closure Gate`" in text, path.name
        assert "`Stage-End Selection List Rule`" in text, path.name
        assert "`Required Validation Handoff Rule`" not in text, path.name
        assert "`Next-Input Choice List Rule`" not in text, path.name
        assert "Other instruction" not in text, path.name
        assert "user must finish" not in text, path.name
        assert not re.search(r"[\u4e00-\u9fff]", text), path.name
        assert "partial successful-response data" not in text, path.name
        assert "Succeeded interfaces:" not in text, path.name
        assert "Failed interfaces:" not in text, path.name
        assert "if wanted" not in text, path.name
        assert "if needed" not in text, path.name
        assert "## Evidence stages" in text, path.name
        assert "| Stage | Entry input | Evidence | Conclusion authority |" in text, path.name
        assert "| Transition |" not in text, path.name
        assert "## User journey" not in text, path.name
        assert "automatic loop" not in text, path.name
        assert "pending queue" not in text, path.name


def test_scenarios_define_evidence_stages_and_conclusion_authority():
    target = read("references/scenarios-keyword-analysis.md")
    expand = read("references/scenarios-expand.md")
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## Evidence stages" in target
    assert "target ASIN" in target
    assert "ABA-SQP" in target
    assert "### Stage application constraints" in target
    assert "Do not request price, contribution margin" in target
    for scenario in (target, expand, reverse, diagnosis):
        assert "Use the canonical Full-Mode Stage Output template" in scenario
        assert "## Section content requirements" in scenario
    assert "4. Seller-funnel calibration" in target
    assert "5. Ads-performance calibration" in target
    assert "6. Profitability calibration" in target
    assert "7. Advertising-control decision" in target
    assert "Stage 1 supports only the market-screen conclusion" in target
    assert "Stage 3 applies only to an explicit multi-term comparison" in target
    assert "A known target term may use Stage 4 after compatible Stage 1 and Stage 2 evidence exists" in target
    assert "do not require candidate expansion or candidate-list confirmation first" in target
    assert "sqp-field-semantics.md" in target
    assert "### Seller-data input guidance" not in target
    assert "acquisition, sequencing, sufficiency, and field-interpretation rules" in target
    assert "worth targeting" in target
    assert "`keywords/product-traffic-terms` filtered to the target keyword" in target
    assert "the exact target-keyword row returned by `keywords/product-traffic-terms`" in target
    assert "do not substitute `keywords/competitor-product-keywords` for the target-ASIN route" in target
    assert "current placement/traffic evidence" not in target
    assert "`product-traffic-terms-timeline`" not in target
    assert "Route movement, anomaly, and causal questions" in target
    assert "movement posture" not in target
    for text in (expand, reverse, diagnosis):
        assert "## Evidence stages" in text
        assert "sqp-field-semantics.md" in text

    for text in (target, expand, reverse, diagnosis):
        assert "Interactive Stage Gate" in text
        assert "Stage-End Selection List Rule" in text


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
    assert "Do not interpret SQP before compatible market and ASIN candidate-validation evidence exists" in scenario
    assert "sqp-field-semantics.md" in scenario
    assert "| 1. Candidate recall" in scenario
    assert "| 2. Market screening" in scenario
    assert "Do not call `market-profile` before the Stage 1 candidate list is confirmed" in scenario
    assert "do not combine candidate recall, market screening, and ASIN validation into one report" in scenario
    assert "they are not workflow states" in scenario
    assert "current product-specific priority remains provisional below seller-funnel evidence" in scenario
    assert "The rows above are evidence levels, not a required end-to-end traversal" in scenario
    assert "Use only the stage whose entry input is available" in scenario
    assert "if product-specific prioritization is wanted" not in scenario
    assert "If seller calibration is needed" not in scenario


def test_reverse_asin_defines_evidence_levels_without_required_progression():
    scenario = read("references/scenarios-reverse-asin.md")

    assert "| 1A. Aggregate channel structure" in scenario
    assert "| 1B. Traffic-term discovery" in scenario
    assert "| 2. Candidate keyword examination" in scenario
    assert "| 3. Seller-funnel calibration" in scenario
    assert "| 4. Ads-performance calibration" in scenario
    assert "| 5. Profitability calibration" in scenario
    assert "| 6. Advertising-control decision" in scenario
    assert "Seller-data handoff" not in scenario
    assert "### Stage application constraints" in scenario
    assert "A raw-list-only request uses only the returned-list conclusion authority and must be explicit" in scenario
    assert "Stages 1A and 1B are mutually exclusive active entries" in scenario
    assert "Stage 1A follows metric-first access" in scenario
    assert "complete Stage 1A first under metric-first access" in scenario
    assert "expose Stage 1B only as a supported continuation" in scenario
    assert "Label the lists with the returned current period" in scenario
    assert "disclose the unavailable previous-period boundary" in scenario
    assert "never infer the missing dates" in scenario
    assert "use numeric Top-N wording only when N is verified" in scenario
    assert "Do not make numeric `*Prev` comparisons" in scenario
    assert "Stage 1B may use Top-N wording when the shared ranked-detail protocol verifies" in scenario
    assert "Otherwise describe only the returned rows" in scenario
    assert "Stage 1B is discovery, not keyword judgment" in scenario
    assert "Do not call `realtime/product` or page acquisition during Stage 1A or Stage 1B" in scenario
    assert "Retain any compatible carried product evidence without rendering or interpreting it during either stage" in scenario
    assert "Stage 2 entry requires a candidate list explicitly supplied or confirmed" in scenario
    assert "Do not call `market-profile` before the Stage 2 candidate list is supplied or confirmed" in scenario
    assert "Bare `continue` or `analyze these terms` satisfies that entry input only when" in scenario
    assert "Do not retrieve new market or SERP evidence before candidate confirmation" in scenario
    assert "Every candidate included in the Stage 2 posture conclusion must have completed market-profile validation" in scenario
    assert "`realtime/product` for the target ASIN" in scenario
    assert "sufficient directly observed ASIN/product-fit evidence" in scenario
    assert "`Headroom validation` remains provisional below Stage 3 seller-funnel evidence" in scenario
    assert "never a `Final calibrated conclusion`" in scenario
    assert "For aggregate channel structure" in scenario
    assert "For traffic-term discovery" in scenario
    assert "For candidate examination" in scenario
    assert "Do not repeat the full discovery report" in scenario
    assert "Do not collapse Stage 1A, Stage 1B, or Stage 2 evidence or conclusions into one response" in scenario
    assert "## Posture labels" in scenario
    assert "Use these labels only after Stage 2 candidate market validation" in scenario
    for label in ("`Established posture`", "`Headroom validation`", "`Observe`", "`No current support`"):
        assert label in scenario
    for action_label in ("`Defend`", "`Expand`", "`Avoid`"):
        assert action_label not in scenario
    assert "sole source for acquisition, sequencing, sufficiency, and field interpretation" in scenario
    assert "Interpret Stage 1A and Stage 1B traffic, placement, contribution, and coverage fields only through `traffic-observation-semantics.md`" in scenario
    assert "sponsored-only row" not in scenario
    assert "Do not call coverage" not in scenario


def test_reverse_and_diagnosis_have_exclusive_question_boundaries():
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## Scenario boundary" in reverse
    assert "# Reverse-ASIN Traffic-Structure Diagnosis Capability Guide" in reverse
    assert "diagnoses the ASIN's current observed traffic structure" in reverse
    assert "does not diagnose broader temporal movement, anomalies, or causes" in reverse
    assert "Do not claim a broad ASIN keyword-traffic analysis" in reverse
    assert "shared clarification gate must disambiguate it" in reverse
    assert "`analyze this ASIN's keyword traffic`" not in reverse
    assert "`map this ASIN's current traffic terms`" in reverse
    assert "Route them to `scenarios-keyword-traffic-diagnosis.md`" in reverse
    assert "Do not call `product-traffic-terms-timeline`" in reverse
    assert "Use `product-traffic-terms-overview` for its current ORG/SP/SB/SBV/SPR fields" in reverse
    assert "first-three-page organic entry/exit lists" in reverse
    assert "bounded Top-N set membership changes" in reverse
    assert "| ASIN × keyword movement |" not in reverse
    assert "Aggregate ASIN traffic movement" not in reverse
    assert "returned listing-event signals" not in reverse

    assert "## Scenario boundary" in diagnosis
    assert "# ASIN Keyword Traffic-Change Diagnosis Capability Guide" in diagnosis
    assert "owns traffic-change diagnosis" in diagnosis
    assert "temporal movement, anomaly, and causal questions" in diagnosis
    assert "Do not produce a full current traffic-term map, candidate pool" in diagnosis
    assert "| 1A. ASIN-wide change triage" in diagnosis
    assert "| 1B. ASIN × keyword diagnosis" in diagnosis
    assert "A keyword-level explanation belongs to Stage 1B" in diagnosis
    assert "requires one named keyword as its entry input" in diagnosis
    assert "Stage 1A does not authorize SQP interpretation" in diagnosis


def test_diagnosis_defers_thresholds_and_keeps_artifact_guidance():
    scenario = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "## Alert-level meaning" not in scenario
    assert "`High`:" not in scenario
    assert "`Medium`:" not in scenario
    assert "`Low`:" not in scenario
    assert "description of the observed movement's magnitude and persistence" in scenario
    assert "sqp-field-semantics.md" in scenario
    assert "instead of redefining them here" in scenario
    assert "SQP artifact for the named ASIN × keyword question" in scenario
    assert "Update only the funnel or conversion conclusion supported" in scenario
    assert "Stage-End Selection List Rule" in scenario
    assert "observed movement and its supporting signals in Evidence" in scenario
    assert "unresolved diagnostic boundaries in Analysis" in scenario


def test_stage_end_selection_lists_are_unified_even_for_one_route():
    guide = read("references/execution-guide.md")
    scenarios = [
        read("references/scenarios-expand.md"),
        read("references/scenarios-keyword-analysis.md"),
        read("references/scenarios-reverse-asin.md"),
        read("references/scenarios-keyword-traffic-diagnosis.md"),
    ]

    assert "### Stage-End Selection List Rule" in guide
    assert "Every normally completed full-mode stage must end" in guide
    assert "Use the list even when there is only one supported continuation" in guide
    assert "For one required ASIN, confirmation, report, file, or field" in guide
    assert "render that single continuation as one numbered item rather than a prose request" in guide
    assert "do not expose internal workflow identity, ordering, progression claims" in guide
    assert "when set selection is supported" in guide
    assert "Ask another question or end this analysis" in guide
    assert "`1` is the only item and is the fixed new-question/exit choice" in guide
    assert "The user is never required to continue" in guide
    for scenario in scenarios:
        assert "Stage-End Selection List Rule" in scenario
        assert "Other instruction" not in scenario

    diagnosis = scenarios[-1]
    assert "A keyword-level explanation belongs to Stage 1B" in diagnosis


def test_all_selectable_subjects_are_merged_into_one_final_numbered_list():
    guide = read("references/execution-guide.md")
    output = read("references/output-rules.md")
    reverse = read("references/scenarios-reverse-asin.md")

    assert "Keep every user-selectable subject and action out of separate lists in Evidence, Analysis, and Conclusion" in guide
    assert "must not assign selection keys, present a candidate/action menu" in guide
    assert "Merge every supported selectable subject and action directly into this one final list" in guide
    assert "Number the final selection list sequentially with bare integers `1`, `2`, `3`, ..." in guide
    assert "it is the only user-selectable list in the response" in guide
    assert "Each item must contain the exact subject label and action" in guide
    assert "A bare integer refers only to the most recent final numbered selection list" in guide
    assert "numeric ranks or metric values elsewhere in the report are not selectable identifiers" in guide
    assert "first give every subject its own numbered item" in guide
    assert "append exactly one numbered `select all` equivalent" in guide
    assert "Do not emit a select-all item for one subject" in guide
    assert "Do not render a candidate menu, action menu, selection key" in output
    assert "place every user-selectable subject and action only in the single final numbered selection list" in output
    assert "Do not render a separate candidate shortlist or selection keys" in reverse
    assert "Apply the shared rule for individual items, set selection, and the select-all item" in reverse
    for obsolete_pattern in (
        "stable lowercase alphabetic identifier",
        "assign stable lowercase alphabetic identifiers",
        "one final-list number containing that identifier",
    ):
        assert obsolete_pattern not in "\n".join((guide, output, reverse))


def test_stage_handoff_closure_populates_but_does_not_force_continuation():
    guide = read("references/execution-guide.md")
    scenarios = [
        read("references/scenarios-expand.md"),
        read("references/scenarios-keyword-analysis.md"),
        read("references/scenarios-reverse-asin.md"),
        read("references/scenarios-keyword-traffic-diagnosis.md"),
    ]
    semantics = read("references/sqp-field-semantics.md")

    assert "### Stage Handoff Closure Gate" in guide
    assert "current decision still requires another evidence level or subject" in guide
    assert "a scenario stage names the exact `Entry input`" in guide
    assert "add one continuation item containing that exact action" in guide
    assert "If no further evidence is required, do not manufacture a deeper analysis" in guide
    assert "If the decision remains unresolved but no authorized evidence/input can resolve it" in guide

    for scenario in scenarios:
        assert "Other instruction" not in scenario
        assert "optional exploration" not in scenario

    assert "Do not assume that every stage must be visited" in guide
    assert "create an automatic loop" in guide
    assert "The user is never required to continue" in guide
    for scenario in scenarios:
        assert "| Transition |" not in scenario
        assert "workflow-completion" not in scenario
    assert "selectable route" not in semantics
    assert "Other instruction" not in semantics


def test_generic_asin_traffic_diagnosis_requires_intent_choice_before_calls():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    reverse = read("references/scenarios-reverse-asin.md")

    for generic_scope in (
        "broad analysis",
        "overview",
        "health check",
        "perspective",
        "analyze this ASIN from a keyword-traffic angle",
    ):
        assert generic_scope in skill
    assert "without explicitly requesting either current traffic terms/source/placement/candidates or temporal change/trend/cause/anomaly" in skill
    assert "Exact phrase matching is not required" in skill
    assert "The absence of change language does not imply traffic-structure intent" in skill
    assert "an ASIN plus a generic keyword-traffic framing does not supply that intent" in skill
    assert "This check does not apply when the user names a target keyword" in skill
    assert "current fit, relevance, or targeting value for the ASIN" in skill
    assert "Route an explicit target keyword + ASIN question" in skill
    assert "Before emitting any user-facing text or making any evidence call" in skill
    assert "Make those reference reads the first actions" in skill
    assert "without a preceding or interstitial assistant message" in skill
    assert "never announce that a clarification rule or reference must be loaded" in skill
    assert "ASIN Traffic Diagnosis Intent Clarification Gate" in skill

    assert "### ASIN Traffic Diagnosis Intent Clarification Gate" in guide
    assert "Apply this gate before any user-visible progress or classification prose" in guide
    assert "Perform any reference reads needed to load this gate silently" in guide
    assert "without announcing their purpose" in guide
    assert "Do not select a scenario" in guide
    assert "execute an API/tool evidence call before clarification" in guide
    assert "Traffic-structure diagnosis" in guide
    assert "Traffic-change diagnosis" in guide
    assert "start only the selected scenario" in guide
    assert "Broad requests for an analysis, overview, health check, or keyword-traffic perspective remain ambiguous" in guide
    assert "absence of change intent is not traffic-structure intent" in guide
    assert "An explicit named-keyword question about current ASIN fit, relevance, or targeting value" in guide
    assert "not an ambiguous diagnosis request" in guide

    assert "Do not claim a broad ASIN keyword-traffic analysis" in reverse
    assert "merely because it lacks change language" in reverse
    assert "must disambiguate it before this scenario is loaded" in reverse


def test_asin_diagnosis_clarification_output_is_direct_and_process_free():
    guide = read("references/execution-guide.md")
    section = guide.split(
        "### ASIN Traffic Diagnosis Intent Clarification Gate", 1
    )[1].split("\n## ", 1)[0]
    option_lines = [
        line.strip()
        for line in section.splitlines()
        if re.match(r"- `[12]` \*\*Traffic-(structure|change) diagnosis\*\*", line.strip())
    ]

    assert len(option_lines) == 2
    assert "Make the localized clarification question or heading and the following numbered list the first user-visible content" in section
    assert "Ask another question or end this analysis" in section
    assert "- `3` **Ask another question or end this analysis**\n" in section
    assert "`A1`" not in section
    assert "`A2`" not in section
    assert "`X`" not in section
    assert "enter a different question or state that no further analysis is needed" not in section
    assert "Omit progress preambles" in section
    assert "Do not expose the skill, Gate, scenario/module names" in section
    assert "credits, or quota" in section
    for line in option_lines:
        assert "scenario" not in line.lower()
        assert "module" not in line.lower()
        assert "api" not in line.lower()
        assert "credit" not in line.lower()
        assert ".md" not in line.lower()


def test_clarification_reference_loading_is_silent():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    output = read("references/output-rules.md")

    assert "Make those reference reads the first actions" in skill
    assert "without a preceding or interstitial assistant message" in skill
    assert "never announce that a clarification rule or reference must be loaded" in skill
    assert "Perform any reference reads needed to load this gate silently" in guide
    assert "Complete internal preparation silently" in output
    assert "Never announce the loading, selection, or application of internal instructions or resources" in output


def test_target_keyword_seller_calibration_does_not_require_candidate_expansion():
    scenario = read("references/scenarios-keyword-analysis.md")

    assert "Stage 3 applies only to an explicit multi-term comparison" in scenario
    assert "A known target term may use Stage 4 after compatible Stage 1 and Stage 2 evidence exists" in scenario
    assert "do not require candidate expansion or candidate-list confirmation first" in scenario
    assert "SQP artifact for one named target term" in scenario
    assert "product-specific funnel and priority conclusion supported for that target term" in scenario
    assert "when seller-funnel calibration is wanted" not in scenario
    assert "after a usable market conclusion request the target ASIN" not in scenario
    assert "market-only" not in scenario


def test_pending_asin_handoffs_reclassify_non_asin_follow_ups():
    guide = read("references/execution-guide.md")
    target = read("references/scenarios-keyword-analysis.md")
    expand = read("references/scenarios-expand.md")

    assert "### Pending Handoff Reclassification Rule" in guide
    assert "At every follow-up" in guide
    assert "before continuing a displayed route" in guide
    assert "If the user selects the fixed final item, asks a new question" in guide
    assert "leave the previous handoff inactive" in guide

    assert "target ASIN" in target
    assert "target ASIN" in expand
    assert "A stage-end list closes the current turn" in guide
    assert "does not reserve the next turn" in guide

    for scenario in (target, expand):
        assert "market-only" not in scenario
        assert "| Transition |" not in scenario


def test_readme_is_preserved_as_a_non_normative_package_index():
    skill = read("SKILL.md")
    readme = read("README.md")

    assert "`README.md` is a human-facing package overview and module index only" in skill
    assert "This README is a human-facing overview and module index" in readme
    assert "this file does not add or override skill policy" in readme
    assert "[`SKILL.md`](SKILL.md)" in readme
    assert "[`references/reference.md`](references/reference.md)" in readme
    assert "[`references/execution-guide.md`](references/execution-guide.md)" in readme
    assert "[`references/evidence-protocols.md`](references/evidence-protocols.md)" in readme
    assert "[`references/diagnosis-action-protocols.md`](references/diagnosis-action-protocols.md)" in readme
    assert "[`references/output-rules.md`](references/output-rules.md)" in readme
    for forbidden_runtime_definition in (
        "## Requirements",
        "ZOODATA_API_KEY",
        "Inspect the router",
        "python scripts/zoodata.py",
        "CONTRIBUTING.md",
        "## User journey",
        "### Interface Failure Stop Gate",
        "## Posture labels",
        "## Non-negotiable boundaries",
    ):
        assert forbidden_runtime_definition not in readme


def test_api_reference_remains_the_contract_source():
    reference = read("references/reference.md")
    evidence = read("references/evidence-protocols.md")

    assert "production capability whitelist" in reference
    assert "Billing is per `status=ok` item for `detail`, `market-profile`, `trend`, and timeline" in reference
    assert "`trend-profile` bills a keyword when at least one requested window row has `status=ok`" in reference
    assert "do not estimate billing from request size or batch width" in evidence
    assert "keywords/market-profile" in reference
    assert "keywords/product-traffic-terms-timeline" in reference
    assert "paginated related-term recall" in reference
    assert "does not define them as an exhaustive root-keyword universe" in reference
    assert "return a root-universe aggregate demand field" in reference
    assert "### Capability-to-contract matrix" in reference
    assert "### Access priority: metric first, data on demand" not in reference
    assert "tested batch currently returned HTTP 500" not in reference
    assert "Current service failure boundary" not in reference
    assert "| `keywords/market-profile` | metric | published and available |" in reference


def test_reference_stays_contract_local_and_scenarios_own_selection():
    skill = read("SKILL.md")
    reference = read("references/reference.md")
    serp_semantics = read("references/serp-and-rollover.md")

    assert "`reference.md` owns only production API and acquisition-surface facts" in skill
    assert "Scenario files own only scenario-specific stage entry requirements, capability selection" in skill
    assert "Apply each rule from its responsible owner module above" in skill
    assert "try `phrase` and `fuzzy`" not in reference
    assert "Use the routes in this order" not in reference
    assert "Use this endpoint first" not in reference
    assert "Use this as the primary observed SERP source" not in reference
    assert "You may calculate simple current-minus-previous" not in reference
    assert "Use returned period boundaries exactly" not in reference
    assert "Use `python {skill_base_dir}/scripts/zoodata.py` after reading subcommand help" not in reference
    assert "Aggregate usage by route" not in reference
    assert "Counts of rows by `exploreType` describe placement-record mix" not in reference
    assert "Use `estimateImpressionPoint` for disclosed returned-row exposure comparisons" not in reference
    assert "Never sum the repeated keyword-level `keywordTotalEstimateImpressionPoint`" not in reference
    assert "Do not relabel it as Top-10/Top-20 set turnover" not in reference
    assert "Use it only when weekly points or fields omitted by `trend-profile` are required" not in reference
    assert "Do not let either seasonality object overwrite the other" not in reference
    assert "Interpretation, comparison, aggregation, and inference limits" in reference
    assert "owned by `serp-and-rollover.md`" in reference
    assert "A market-level run may decide only whether ASIN-level validation is warranted" not in serp_semantics


def test_traffic_observation_semantics_have_one_progressively_loaded_owner():
    skill = read("SKILL.md")
    reference = read("references/reference.md")
    evidence = read("references/evidence-protocols.md")
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")
    semantics = read("references/traffic-observation-semantics.md")
    readme = read("README.md")

    assert "`references/traffic-observation-semantics.md` for traffic-term lists" in skill
    assert "`traffic-observation-semantics.md`) own only documented field meaning" in skill
    assert "[`traffic-observation-semantics.md`](references/traffic-observation-semantics.md)" in readme
    assert "stage entry requirements, capability selection, conclusion authority, and report-section content" in readme
    assert "stage transitions" not in readme
    assert "Load the field-semantic owner routed by `SKILL.md`" in evidence

    assert "Interpret `trafficShare`, placement, contribution, and coverage fields through `traffic-observation-semantics.md`" in reference
    assert "Interpret the series' snapshot, weekly-period, metric-window" in reference
    assert "sampled share within the returned ASIN traffic period" not in reference
    assert "Keep time grains separate" not in reference

    assert "high `adCount`" not in evidence
    assert "low `daysCoverageRate`" not in evidence
    assert "sponsored-only row" not in reverse
    assert "co-movement into causality" not in diagnosis

    for owned_semantic in (
        "`trafficShare` is the row's sampled share",
        "A sponsored-only row or one selected page of returned rows",
        "`daysCoverageRate`, `observationCount`",
        "`asinSnapshot` is tied to the series date",
        "`adActivity` counts and coverage describe observed ad participation",
        "Time-aligned co-movement can narrow an explanation",
        "Current ORG/SP/SB/SBV/SPR impression-point fields support",
        "channel impression points ÷ sum of included current channel impression points",
        "membership changes in the endpoint-defined first-three-page organic Top-N set",
        "Use a numeric `Top N` label only when returned context",
        "The overview has no keyword contribution rows",
    ):
        assert owned_semantic in semantics

    assert "Repeated brands or parent-ASIN families" not in semantics


def test_ranked_and_change_explanations_require_explicit_scope():
    evidence = read("references/evidence-protocols.md")
    output = read("references/output-rules.md")
    semantics = read("references/traffic-observation-semantics.md")

    assert "## Claim Scope and Ranked Detail Protocol" in evidence
    assert "Every interpretation must carry a resolved scope tuple" in evidence
    for scope_component in (
        "source",
        "subject",
        "requested and resolved period",
        "population or returned coverage",
        "filters/channels",
        "sort field",
        "sort direction",
        "page size",
    ):
        assert scope_component in evidence
    assert "A Top-N statement is allowed when" in evidence
    assert "Top N by <exact metric> <direction>" in evidence
    assert "the N returned rows" in evidence
    assert "Do not relabel them Top N" in evidence
    assert "Top N describes an ordered slice under one metric and request scope" in evidence
    assert "Terms such as `share`, `new`, `lost`, `increase`, and `decrease`" in evidence

    assert "At first use, every ranked, aggregate, comparative, entry/exit, growth, or decline explanation" in output
    assert "population/Top-N or returned-row coverage" in output
    assert "label that boundary unavailable instead of deriving it" in output
    assert "A ranking must also name its sort direction" in output
    assert "Do not render unqualified labels such as `top keywords`" in output

    assert "returned traffic-term rows may be described as Top N by that exact field and direction" in semantics
    assert "Top N by trafficShare descending" in semantics
    assert "Report those arrays with the returned current period" in semantics
    assert "previous-period boundary is not returned" in semantics
    assert "Do not infer the missing previous dates" in semantics
    assert "Entry or exit does not establish per-keyword traffic gain/loss" in semantics


def test_missing_previous_period_evidence_is_not_inferred_or_replaced_by_wrong_grain():
    reference = read("references/reference.md")
    evidence = read("references/evidence-protocols.md")
    semantics = read("references/traffic-observation-semantics.md")

    assert "does not return separate previous-period date boundaries" in reference
    assert "A `*Prev` field may also be null or absent" in reference
    assert "only if it preserves the claim's subject, grain, marketplace, and comparison meaning" in evidence
    assert "cannot replace an ASIN-wide aggregate overview" in evidence
    assert "leave the comparison unavailable and do not infer" in evidence
    assert "label that boundary unavailable and never derive it from weekly cadence" in semantics
    assert "the movement comparison for that channel is unavailable" in semantics


def test_full_mode_scenario_shapes_align_with_top_level_output_order():
    output = read("references/output-rules.md")
    expand = read("references/scenarios-expand.md")
    target = read("references/scenarios-keyword-analysis.md")
    reverse = read("references/scenarios-reverse-asin.md")
    diagnosis = read("references/scenarios-keyword-traffic-diagnosis.md")

    assert "exactly this canonical top-level template" in output
    for label in ("`Data Notes`", "`Evidence`", "`Analysis`", "`Conclusion`", "`API Usage`"):
        assert label in output
    assert "`Stage Conclusion`" not in output
    assert "Do not expose internal workflow identifiers, labels, ordinals, or progression claims anywhere in user-facing text" in output
    assert "Name current scope and any continuation by their user-domain subject and action" in output
    assert "Apply the User-Facing Output Boundary to the entire response" in output
    assert "including titles, headings, body text, usage reporting, and the selection list" in output
    assert "instead of exposing its internal workflow identity" in output
    assert "Do not rename `Evidence` to a scenario-specific heading" in output
    assert "discovery, posture, or calibration results inside `Conclusion`" in output

    canonical_contract = (
        "Use the canonical Full-Mode Stage Output template from `output-rules.md` "
        "without renaming, adding, removing, or reordering its report sections."
    )
    for scenario in (expand, target, reverse, diagnosis):
        assert canonical_contract in scenario
        assert "## Section content requirements" in scenario
        assert "## Output shape" not in scenario
        assert "## Report shape" not in scenario

    assert "candidate terms" in expand
    assert "active target-keyword stage's observations in Evidence" in target
    assert "authorized judgment in Conclusion" in target
    assert "current overview fields and any material, explicitly scoped" in reverse
    assert "current keyword-row observations and selection basis in Evidence" in reverse
    assert "supported discovery conclusion in Conclusion" in reverse
    assert "observed movement and its supporting signals in Evidence" in diagnosis
    assert "active stage's new evidence and compatible prior-stage evidence in Conclusion" in diagnosis
    assert "Stage 1 discovery conclusion" not in reverse
    assert "observed change/evidence" not in diagnosis


def test_seller_decision_stages_are_explicit_separate_and_cumulative():
    guide = read("references/execution-guide.md")

    assert "only when the user's latest request explicitly asks for the corresponding report or decision" in guide
    assert "does not make any later seller-data stage mandatory" in guide
    assert "the user's latest request asks for a report or decision within that stage's `Conclusion authority`" in guide
    assert "Possession of compatible data does not by itself select a stage" in guide
    assert "new evidence together with compatible prior-stage evidence" in guide

    for relative_path in (
        "references/scenarios-expand.md",
        "references/scenarios-keyword-analysis.md",
        "references/scenarios-reverse-asin.md",
        "references/scenarios-keyword-traffic-diagnosis.md",
    ):
        scenario = read(relative_path)
        assert "Ads-performance calibration" in scenario, relative_path
        assert "Explicit Ads-performance request" in scenario, relative_path
        assert "Give only the attributed Ads-performance conclusion" in scenario, relative_path
        assert "Do not infer profitability or recommend a bid or budget" in scenario, relative_path
        assert "Profitability calibration" in scenario, relative_path
        assert "Explicit profitability request" in scenario, relative_path
        assert "seller-supplied unit economics or an economics-grounded break-even/target ACOS or ROAS" in scenario, relative_path
        assert "Advertising-control decision" in scenario, relative_path
        assert "Explicit exact bid or budget request" in scenario, relative_path
        assert "compatible carried evidence" in scenario.lower(), relative_path
        assert "Ads-economics calibration" not in scenario, relative_path
        assert "Update only the profitability or execution conclusion supported" not in scenario, relative_path


def test_public_keyword_endpoint_inventory_and_sqp_routing_are_consistent():
    root_readme = (ROOT.parent / "README.md").read_text(encoding="utf-8")
    zoodata_readme = (ROOT.parent / "zoodata" / "README.md").read_text(encoding="utf-8")
    zoodata_skill = (ROOT.parent / "zoodata" / "SKILL.md").read_text(encoding="utf-8")
    openapi_reference = (
        ROOT.parent / "zoodata" / "references" / "openapi-reference.md"
    ).read_text(encoding="utf-8")

    assert "Direct access to all 22 API endpoints" in root_readme
    assert "200M+ Amazon products. 22 endpoints. One API key." in zoodata_readme
    assert "| 14 | `keywords/market-profile`" in zoodata_readme
    assert "| 22 | `keywords/product-traffic-terms-timeline`" in zoodata_readme
    assert "20 endpoints" not in zoodata_readme

    for text in (zoodata_readme, zoodata_skill, openapi_reference):
        assert "every traffic-related conclusion" not in text
        assert "\u5efa\u8bae\u7ed3\u5408 Amazon \u540e\u53f0 ABA-SQP" not in text
    assert "does not prescribe a blanket caveat or one seller view for every subject" in zoodata_skill
    assert "belong to the `amazon-keyword-traffic-analysis` skill" in openapi_reference


def test_zoodata_credential_and_credit_contract_matches_cli_output():
    zoodata_skill = (ROOT.parent / "zoodata" / "SKILL.md").read_text(encoding="utf-8")

    for status in (401, 402):
        assert f"`_transport.status={status}`" in zoodata_skill
        assert f"`error.status={status}`" in zoodata_skill
        assert f'{{"code": {status}' not in zoodata_skill
    assert "API Budget table" not in zoodata_skill
    assert "if it is absent, say it was not returned rather than estimating it" in zoodata_skill


def test_numeric_ads_recommendations_require_explicit_request_and_sufficient_evidence():
    guide = read("references/execution-guide.md")
    actions = read("references/diagnosis-action-protocols.md")
    semantics = read("references/sqp-field-semantics.md")

    assert "Never volunteer a numeric bid, bid range, bid-change percentage, budget amount" in guide
    assert "only when the user's latest request explicitly asks for that exact advertising decision" in guide
    assert "An explicit request is not action authorization" in guide
    assert "`diagnosis-action-protocols.md` authorizes a `Change`" in guide
    assert "seller evidence interpreted through `sqp-field-semantics.md`" in guide
    assert "do not infer profitability from either source alone" in guide
    assert "seller-supplied unit economics or an explicit break-even/target ACOS or ROAS" in guide

    assert "## Numeric advertising decision protocol" in actions
    assert "Never introduce a numeric advertising action as an unsolicited optimization" in actions
    for required_dimension in (
        "Exact controlled target",
        "Compatible performance evidence",
        "Current control state",
        "Seller objective and economics",
        "Observation sufficiency",
        "Bounded validation",
    ):
        assert required_dimension in actions
    assert "do not output a bid, budget, range, default amount, formula-derived amount, or percentage change" in actions
    assert "cannot establish product profitability without the seller economics above" in actions

    assert "# Seller Artifact Field Semantics — ABA-SQP and Amazon Ads" in semantics
    assert "## Amazon Ads schema identity" in semantics
    assert "search term is the shopper query" in semantics
    assert "A keyword/product target is the advertiser-controlled target" in semantics
    for formula in (
        "`Spend ÷ Clicks`",
        "`Orders ÷ Clicks`",
        "`Spend ÷ Sales`",
        "`Sales ÷ Spend`",
    ):
        assert formula in semantics
    assert "Do not average row-level CPC, CVR, ACOS, or ROAS" in semantics
    assert "CPC does not reveal the current bid" in semantics
    assert "Product profitability requires seller-supplied unit economics" in semantics
    assert "Bid-control identity is incomplete unless the exact current bid" in semantics
    assert "Budget-control identity is incomplete unless the exact current budget" in semantics
    assert "None of those fields by itself encodes a recommended bid" in semantics
    assert "None of those fields by itself encodes a recommended budget or allocation" in semantics
    assert "they never authorize a guessed number" in semantics


def test_supporting_acquisition_is_whitelisted_and_search_surfaces_stay_distinct():
    skill = read("SKILL.md")
    evidence = read("references/evidence-protocols.md")
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
    assert "WebTools `/search` is not `products/search`" in evidence
    assert "Use WebTools `/search` only when the URL must first be discovered" in evidence
    assert "WebTools `/search` is permitted URL discovery; it is not `products/search`" in skill
    assert "Never use `products/search`" in skill


def test_global_boundaries_remain_in_the_router():
    skill = read("SKILL.md")

    assert "`products/search`" in skill
    assert "external browser automation" in skill
    assert "ABA-SQP conversion funnel" in skill
    assert "status=empty" in skill


def test_seller_data_requests_use_progressive_artifact_guidance():
    semantics = read("references/sqp-field-semantics.md")

    assert "Request one seller report or view at a time" in semantics
    assert "Do not request SQP and Ads artifacts in the same stage-end list" in semantics
    assert "instead of asking the user to assemble fields manually" in semantics
    assert "### User-facing SQP acquisition" in semantics
    assert "when the shared workflow requests a seller-funnel artifact as the one exact next input" in semantics
    assert "after the active scenario has requested seller-funnel evidence" not in semantics
    assert "When the active scenario later requests Ads evidence" not in semantics
    assert "Render the artifact request as one continuation item under the shared Stage-End Selection List Rule" in semantics
    assert "not separate list items" in semantics
    assert "Screenshot and CSV are format alternatives for supplying the same requested evidence" in semantics
    assert "Next-Input Choice List Rule" not in semantics
    assert "Other instruction" not in semantics
    assert "selectable route" not in semantics
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
    output = read("references/output-rules.md")
    market_semantics = read("references/metrics-market-profile.md")

    assert "Count every executed API call" in output
    assert "duplicate/diagnostic/discarded calls" in output
    assert "calls followed by local parse failure" in output
    assert "When `annualSeasonality` is unsupported" in market_semantics
    assert "omit seasonal timing and seasonal-cause narratives entirely" in market_semantics
    assert "Hedging with `may`, `might`, `possibly`, or an equivalent in any language" in market_semantics


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
