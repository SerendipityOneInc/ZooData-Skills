"""CLI routing and shared-contract consistency for non-keyword ZooData skills."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "amazon-market-entry-analyzer" / "SKILL.md"
CONTRACT_PATH = ROOT / "zoodata" / "references" / "cli-contract.md"
NON_KEYWORD_SKILLS = (
    "amazon-analysis",
    "amazon-competitor-intelligence-monitor",
    "amazon-daily-market-radar",
    "amazon-listing-audit-pro",
    "amazon-market-entry-analyzer",
    "amazon-market-trend-scanner",
    "amazon-opportunity-discoverer",
    "amazon-pricing-command-center",
    "amazon-review-intelligence-extractor",
)


def test_market_entry_cli_routing_uses_only_verified_literal_subcommands():
    skill = SKILL_PATH.read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "### CLI Route Selection" in skill
    assert "An API endpoint identifier or composite result key is not a CLI subcommand" not in skill
    assert "Never derive a command from data identity or invent an alias" not in skill
    assert "Treat API endpoint identifiers and composite result keys as data identities" in contract
    assert "Never derive a subcommand from either identity or invent an alias" in contract
    assert "Inspect the bundled CLI's top-level `--help` and the selected subcommand's `--help`" in contract

    expected_routes = {
        "categories": "categories",
        "markets/search": "market",
        "products/search": "products",
        "products/competitors": "competitors",
        "realtime/product": "product",
        "reviews/analysis": "analyze",
        "products/price-band-overview": "price-band-overview",
        "products/price-band-detail": "price-band-detail",
        "products/brand-overview": "brand-overview",
        "products/brand-detail": "brand-detail",
        "products/history": "history",
    }
    for endpoint, command in expected_routes.items():
        assert f"| `{endpoint}` | `{command}` |" in skill

    assert "| `products/price-band-detail` | `price-band` |" not in skill


def test_successful_composite_output_is_extracted_locally_without_refetching():
    skill = SKILL_PATH.read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "Treat a successful composite command's structured output as the evidence bundle" in contract
    assert "Perform selection, narrowing, transformation, extraction, and formatting locally" in contract
    assert "Do not make an additional API call solely to reread, reshape, or narrow evidence" in contract
    assert "A granular call after a composite is allowed only for evidence absent from the bundle" in contract
    assert "Apply `references/cli-contract.md` to its invocation and returned composite bundle" in skill
    assert "use targeted extraction, not full read" not in skill


def test_shared_contract_owns_cross_skill_cli_usage_and_behavior():
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "# ZooData CLI Contract" in contract
    assert "## Invocation interface" in contract
    assert "## Command identity and composite reuse" in contract
    assert "## Execution-environment permission gate" in contract
    assert "## Result acquisition" in contract
    assert "## Classification order" in contract
    assert "## Retry and terminal behavior" in contract
    assert "## Composite and partial results" in contract
    assert "shared invocation form, command-identity validation, execution-environment permission handling" in contract
    assert "It does not own skill-specific command allowlists" in contract


def test_caller_delegates_credential_resolution_to_cli():
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "Credential resolution is owned by the bundled CLI" in contract
    assert "do not inspect local credential stores or pre-resolve, compare, export, or override credential values" in contract


def test_environment_network_restrictions_request_permission_before_failure_output():
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "before classifying a connection or network failure as a CLI/API interface failure" in contract
    assert "host sandbox or network policy blocked the request" in contract
    assert "Use the execution tool's permission or escalation mechanism to request access" in contract
    assert "rerun the exact unchanged CLI command" in contract
    assert "Do not first emit the skill's interface-failure notice" in contract
    assert "A permission-approved rerun is environment recovery, not an external transport retry" in contract
    assert "Do not label endpoints as failed" in contract
    assert "Do not use this gate to bypass a returned HTTP status" in contract

    for name in NON_KEYWORD_SKILLS:
        skill = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        assert "The shared CLI exposes ALL ZooData endpoints as subcommands" not in skill, name
        assert "## Shared CLI Contract" in skill, name
        assert "Before selecting or invoking the first command, read and apply the local `references/cli-contract.md`" in skill, name
        assert "Reapply it after every granular or composite result" in skill, name
        assert "An API endpoint identifier or composite result key is not a CLI subcommand" not in skill, name
        assert "After a successful composite invocation" not in skill, name


def test_documented_non_keyword_cli_commands_exist_in_bundled_client():
    script = (ROOT / "zoodata" / "scripts" / "zoodata.py").read_text(encoding="utf-8")
    available = set(re.findall(r'sub\.add_parser\("([a-z0-9-]+)"', script))
    assert available

    for name in NON_KEYWORD_SKILLS:
        skill = (ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"zoodata\.py\s+([a-z0-9-]+)", skill))
        missing = documented - available
        assert not missing, f"{name} documents unavailable CLI commands: {sorted(missing)}"
