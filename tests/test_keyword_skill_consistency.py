"""Behavioral guardrails for the amazon keyword traffic skill documentation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "amazon-keyword-traffic-analysis"


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def section(text, start_heading, end_heading=None):
    body = text.split(start_heading, 1)[1]
    if end_heading:
        body = body.split(end_heading, 1)[0]
    return body


def test_standalone_and_asin_expansion_are_separate_routes():
    text = read("references/scenarios-expand.md")
    standalone = section(
        text,
        "## Route A: standalone expansion",
        "## Route B: staged ASIN candidate validation",
    )
    staged = section(
        text,
        "## Route B: staged ASIN candidate validation",
        "## Output templates",
    )

    assert "request the user's asin" in standalone.lower()
    assert "Do not request ABA-SQP" in standalone
    assert "request seller-side ABA-SQP" in staged
    assert "product fit × current ASIN performance/posture × keyword market profile" in staged


def test_market_profile_contract_uses_scoring_spec_and_dimension_status():
    skill = read("SKILL.md")
    reference = read("references/reference.md")

    assert "context.scoringSpec" in skill
    assert "calculationStatus" in skill
    assert "marketCharacteristics" in skill
    assert "levelEvidence.score.{value,direction}" in skill
    assert "status=available" in skill
    assert "status=not_found" in skill
    assert "unavailableReason" in skill
    assert "context.scoringSpec" in reference
    assert "no aggregate `calculationCoverage` object" in reference
    assert "marketCharacteristics" in reference
    assert "levelEvidence.score.{value,direction}" in reference
    assert "status=available|not_found" in reference
    assert "unavailableReason=keyword_not_observed" in reference
    assert "marketContext" not in skill
    assert "marketContext" not in reference
    assert "scoreDirection" not in skill
    assert "scoreDirection" not in reference
    assert "threshold/version" not in skill
    assert "thresholdBasis" not in skill


def test_market_profile_keeps_seasonality_evidence_independent_and_handles_batch_500():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    reference = read("references/reference.md")

    assert "independent evidence objects" in skill
    assert "do not manufacture peak periods" in guide
    assert "seasonalPeakPatternDetected=true" in reference
    assert "HTTP 500" in skill
    assert "at most one diagnostic split" in reference


def test_action_gate_covers_uninspected_assets_and_campaign_settings():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    expansion = read("references/scenarios-expand.md")

    assert "If the target was not directly inspected, stop at `Inspect`" in skill
    assert "downgrade the action itself" in skill
    assert "Ads economics before scaling" in guide
    assert "Do not output `Auto / Broad / Phrase / Exact`" in expansion


def test_named_cross_references_exist():
    skill = read("SKILL.md")
    guide = read("references/execution-guide.md")
    reverse_asin = read("references/scenarios-reverse-asin.md")

    assert "## Evidence-Level Progression" in guide
    assert "§ Evidence-Level Progression" in skill
    assert "## Seller Data Contract" in guide
    assert "§ Seller Data Contract" in reverse_asin
    assert "Conversational Evidence Ladder" not in skill
    assert "Stage 4 contract" not in reverse_asin


def test_readme_lists_metric_profiles_and_current_endpoint_count():
    readme = read("README.md")
    assert "ten ZooData keyword endpoints" in readme
    assert "/openapi/v2/keywords/market-profile" in readme
    assert "/openapi/v2/keywords/trend-profile" in readme
    assert "mcp__zoodata__openapi_v2_keyword_market_profile" in readme
