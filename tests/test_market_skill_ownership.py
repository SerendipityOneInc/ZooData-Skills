"""Ownership and scenario routing for the unified market skill."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "amazon-market-analysis"
RETIRED_MARKET_SOURCE_SKILLS = {
    "amazon-market-entry-analyzer",
    "amazon-market-trend-scanner",
    "amazon-opportunity-discoverer",
}


class TestMarketSkillOwnership(unittest.TestCase):
    def test_one_market_skill_dispatches_three_independent_scenarios(self):
        skill = (MARKET / "SKILL.md").read_text()
        self.assertIn("## Source-of-truth boundaries", skill)
        for module in (
            "reference.md", "execution-guide.md", "evidence-protocols.md",
            "market-metric-semantics.md", "seller-input-semantics.md",
            "output-rules.md", "scenarios-discover.md",
            "scenarios-evaluate.md", "scenarios-track.md",
        ):
            with self.subTest(module=module):
                self.assertTrue((MARKET / "references" / module).is_file())
                self.assertIn(f"references/{module}", skill)

        for scenario in ("discover", "evaluate", "track"):
            with self.subTest(scenario=scenario):
                text = (MARKET / "references" /
                        f"scenarios-{scenario}.md").read_text()
                self.assertIn("| Stage | Entry input | Evidence | Conclusion authority |", text)
                self.assertIn("## Section content requirements", text)

        for retired_source in RETIRED_MARKET_SOURCE_SKILLS:
            self.assertFalse((ROOT / retired_source / "SKILL.md").exists())
            retired = ROOT / retired_source / "RETIRED.md"
            self.assertTrue(retired.is_file())
            self.assertIn("**Retired:**", retired.read_text())

        sync_script = (ROOT / "scripts" / "sync-scripts.sh").read_text()
        self.assertNotIn("SKIP_SKILLS", sync_script)
        self.assertIn("without SKILL.md is retained source", sync_script)

    def test_only_active_skill_entrypoints_are_discoverable(self):
        expected = {
            "amazon-analysis", "amazon-competitor-intelligence-monitor",
            "amazon-daily-market-radar", "amazon-keyword-traffic-analysis",
            "amazon-listing-audit-pro", "amazon-market-analysis",
            "amazon-pricing-command-center",
            "amazon-review-intelligence-extractor", "web-extract", "zoodata",
        }
        discovered = {
            path.parent.name for path in ROOT.glob("*/SKILL.md")
        }
        self.assertEqual(discovered, expected)
        self.assertEqual(len(discovered), 10)

    def test_zoodata_market_schema_has_one_owner(self):
        skill = (ROOT / "zoodata" / "SKILL.md").read_text()
        summary = (ROOT / "zoodata" / "references" /
                   "reference.md").read_text()
        owner = (ROOT / "zoodata" / "references" /
                 "openapi-reference.md").read_text()
        self.assertIn("openapi-reference.md § 2", skill)
        self.assertIn("openapi-reference.md", summary)
        self.assertNotIn("### markets/search — discovery", summary)
        self.assertIn("## 2. markets/search", owner)
        self.assertIn("## 2b. markets/history", owner)

    def test_unavailable_overview_is_owned_by_reference_not_skill_router(self):
        skill = (MARKET / "SKILL.md").read_text()
        reference = (MARKET / "references" / "reference.md").read_text()
        manifest = (MARKET / "scripts" / "allowed-commands.json").read_text()
        self.assertNotIn("markets/overview", skill)
        self.assertIn("`markets/overview` is absent", reference)
        self.assertNotIn('"market-overview"', manifest)
        self.assertNotIn("market-overview --", skill)

    def test_market_modules_do_not_include_repo_process(self):
        for path in (MARKET / "references").glob("*.md"):
            if path.name == "cli-contract.md":
                continue
            with self.subTest(module=path.name):
                text = path.read_text().lower()
                for forbidden in ("contributing.md", "agents.md", "pull request",
                                  "ci check", "repository maintenance"):
                    self.assertNotIn(forbidden, text)

    def test_parent_scoped_discovery_uses_child_ids(self):
        scenario = (MARKET / "references" / "scenarios-discover.md").read_text()
        reference = (MARKET / "references" / "reference.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        shared_contract = (MARKET / "references" /
                           "analysis-contract.md").read_text()
        self.assertIn("every direct child", scenario)
        self.assertIn("A parent-wide top K requires complete", scenario)
        self.assertIn("`category.ids` in one `markets/search` request", reference)
        self.assertIn("`--parent` requires a nonempty JSON string array", reference)
        self.assertIn("`meta.total` counts matching rows after filters", reference)
        self.assertIn("compare returned IDs with the requested set", evidence)
        self.assertIn("transcript folding or truncation", shared_contract)
        for foreign_contract in ("--parent", "--category-ids", "page-size",
                                 "`meta.total`", "JSON string array"):
            self.assertNotIn(foreign_contract, scenario)

    def test_market_handoff_closes_a_stage_without_automatic_progression(self):
        guide = (MARKET / "references" / "execution-guide.md").read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        discover = (MARKET / "references" / "scenarios-discover.md").read_text()

        self.assertIn("### Handoff Gate", guide)
        self.assertIn("material remaining decision", guide)
        self.assertIn("### Stage-End Selection List Rule", guide)
        self.assertIn("Ask another question or end this analysis", guide)
        self.assertIn("A bare number selects only the most recent final-list item", guide)
        self.assertIn("Do not auto-select a route", guide)
        self.assertIn("one final numbered selection list", output)
        self.assertIn("material evidence gaps in `Conclusion`", discover)
        self.assertNotIn("the specific next validation question in `Conclusion`", discover)

    def test_market_history_renders_only_verified_completed_months(self):
        contract = (MARKET / "references" / "analysis-contract.md").read_text()
        scenario = (MARKET / "references" / "scenarios-track.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        semantics = (MARKET / "references" /
                     "market-metric-semantics.md").read_text()

        self.assertIn("two supplied compatible snapshots", scenario)
        self.assertIn("Persistent watch", scenario)
        self.assertIn("one-time comparison of supplied snapshots remains a historical trend", scenario)
        self.assertIn("Render history rows and missing-period treatment only through `output-rules.md`", scenario)
        self.assertNotIn("placeholder row", scenario)
        self.assertNotIn("current incomplete month", scenario)
        self.assertIn("project every returned `data.points[]` entry", evidence)
        self.assertIn("projected point count and dates equal", evidence)
        self.assertIn("is not an API coverage gap", evidence)
        self.assertIn("do not offer another paid query", evidence)
        self.assertIn("### Historical table rendering", output)
        self.assertIn("omit the current incomplete calendar month", output)
        self.assertIn("omit missingness commentary entirely", output)
        self.assertIn("Render valid zero values directly", output)
        self.assertIn("unless the requested range itself needs clarification", output)
        self.assertIn("The API did not return {field} for {YYYY-MM-DD}", output)
        self.assertIn("Vague placeholders", output)
        self.assertIn("localized equivalents are invalid", output)
        self.assertIn("current incomplete calendar month is outside", semantics)
        self.assertIn("**Local unread state**", contract)
        self.assertIn("do not use truthiness", contract)
        self.assertIn("documented business definition as the semantic identity", contract)
        self.assertIn("### Trust documented evidence", contract)
        self.assertIn("a concrete contradiction or contract violation", contract)

    def test_market_results_are_projected_from_cleaned_up_raw_files(self):
        contract = (ROOT / "zoodata" / "references" / "cli-contract.md").read_text()
        evidence = (MARKET / "references" / "evidence-protocols.md").read_text()
        guide = (MARKET / "references" / "execution-guide.md").read_text()

        self.assertIn("<YYYY-MM-DD>/run-<secure-random>/", contract)
        self.assertIn("`EXIT`, `HUP`, `INT`, and `TERM`", contract)
        self.assertIn("without waiting for it", contract)
        self.assertIn("whole date buckets older than 30 days", contract)
        self.assertIn("Delete the raw result as soon as classification", contract)
        self.assertIn("token-truncation marker", contract)
        self.assertIn("Projection is a local, zero-credit transformation", contract)
        self.assertIn("## Market result projection", evidence)
        self.assertIn("validate the requested ID set", evidence)
        self.assertIn("`success=true` and `meta.total=N`", evidence)
        self.assertIn("shared temporary-result procedure", guide)

    def test_market_output_gate_rejects_implementation_detail_leakage(self):
        canonical = (ROOT / "zoodata" / "references" /
                     "analysis-contract.md").read_bytes()
        contract_path = MARKET / "references" / "analysis-contract.md"
        shared_contract = contract_path.read_text()
        output = (MARKET / "references" / "output-rules.md").read_text()
        guide = (MARKET / "references" / "execution-guide.md").read_text()
        skill = (MARKET / "SKILL.md").read_text()

        self.assertEqual(contract_path.read_bytes(), canonical)
        self.assertIn("## Rule hierarchy", shared_contract)
        self.assertIn("### Keep implementation internal", shared_contract)
        self.assertIn("raw payload capture", shared_contract)
        self.assertIn("temporary paths", shared_contract)
        self.assertIn("projection, parsing, cleanup", shared_contract)
        self.assertIn("### 7. Final Response Gate", shared_contract)
        self.assertIn("discard the draft and render it again", shared_contract)
        self.assertIn("Do not patch a leaked sentence", shared_contract)
        self.assertIn("Read and apply `references/analysis-contract.md`", skill)
        self.assertIn("Apply `analysis-contract.md § 7. Final Response Gate`", guide)
        self.assertIn("owns market-specific language", output)
        self.assertNotIn("## User-Facing Output Boundary", output)
        self.assertNotIn("## Retrieval Progress Updates", output)

    def test_general_analysis_ownership_keeps_details_in_modules(self):
        root = ROOT / "amazon-analysis"
        skill = (root / "SKILL.md").read_text()
        guide = (root / "references" / "execution-guide.md").read_text()
        reference = (root / "references" / "reference.md").read_text()
        for heading in ("## Product Selection Mode Mapping", "## Market Health Assessment",
                        "## Output Standards — Full Specification"):
            self.assertIn(heading, guide)
            self.assertNotIn(heading, skill)
        self.assertIn("## Cross-endpoint field identity", reference)
        self.assertNotIn("## Interface Data Differences", guide)
        self.assertNotIn("## Output Spec", skill)

    def test_focused_market_discovery_routes_away_from_general_skill(self):
        general = (ROOT / "amazon-analysis" / "SKILL.md").read_text()
        general_description = general.split("description: >", 1)[1].split("metadata:", 1)[0]
        market_description = (MARKET / "SKILL.md").read_text().split(
            "description: >", 1)[1].split("metadata:", 1)[0]
        self.assertIn("category-market\n  discovery", general_description)
        self.assertIn("amazon-market-analysis", general_description)
        self.assertIn("discover\n  candidate niches and products", market_description)

    def test_market_field_and_history_names_match_current_response(self):
        owners = (
            ROOT / "zoodata" / "references" / "openapi-reference.md",
            MARKET / "references" / "reference.md",
            MARKET / "references" / "market-metric-semantics.md",
        )
        for path in owners:
            with self.subTest(module=path.name):
                text = path.read_text()
                self.assertIn("sampleNewProduct", text)
                self.assertIn("newProductPeriod", text)
                self.assertIsNone(re.search(r"sampleNewProduct\w*6m", text))
                self.assertNotIn("newProductMetrics", text)
                self.assertNotIn("sampleConservative", text)
        for path in ROOT.glob("amazon-*/references/*.md"):
            if path.parent.parent.name in RETIRED_MARKET_SOURCE_SKILLS:
                continue
            text = path.read_text()
            self.assertIsNone(re.search(r"sampleNewProduct\w*6m", text), str(path))
            self.assertNotIn("newProductMetrics", text, str(path))
            self.assertNotIn("sampleConservative", text, str(path))
            self.assertNotIn("actualStartDate", text, str(path))
            self.assertNotIn("actualEndDate", text, str(path))

        for skill_name in (
            "amazon-analysis", "amazon-competitor-intelligence-monitor",
            "amazon-daily-market-radar", "amazon-listing-audit-pro",
            "amazon-pricing-command-center",
            "amazon-review-intelligence-extractor",
        ):
            reference_text = (ROOT / skill_name / "references" / "reference.md").read_text()
            market_section = reference_text.split("## 2. Market endpoints", 1)[1].split("## 3.", 1)[0]
            self.assertNotIn("categoryScope", market_section, skill_name)
            self.assertNotIn("startDate", market_section, skill_name)
            self.assertNotIn("endDate", market_section, skill_name)
            self.assertIn("includeDescendantCategoryProducts", market_section)
            self.assertIn("dateFrom", market_section)
            self.assertIn("dateTo", market_section)

        owner = owners[0].read_text()
        reference = owners[1].read_text()
        semantics = owners[2].read_text()
        self.assertIn("`topSalesRateMin/Max`", owner)
        self.assertIn("`sampleTop10ProductSalesRateMin/Max`", owner)
        self.assertIn("`dateFrom`, and `dateTo`", owner)
        self.assertIn("`includeDescendantCategoryProducts`", reference)
        self.assertIn("Fixed `sampleTop10*` fields", semantics)
        self.assertNotIn("`startDate`, and `endDate`", reference)
        self.assertNotIn("Optional `categoryScope`", owner)

    def test_market_router_and_scenarios_respect_declared_ownership(self):
        skill = (MARKET / "SKILL.md").read_text()
        discover = (MARKET / "references" / "scenarios-discover.md").read_text()
        evaluate = (MARKET / "references" / "scenarios-evaluate.md").read_text()
        track = (MARKET / "references" / "scenarios-track.md").read_text()
        for foreign_definition in ("markets/overview", "`total*`", "`sample*`"):
            self.assertNotIn(foreign_definition, skill)
        for api_syntax in ("--parent", "--category-ids", "page-size", "`meta.total`"):
            self.assertNotIn(api_syntax, discover)
        for foreign_definition in ("page-size", "--dimension", "`total*`", "`sample*`"):
            self.assertNotIn(foreign_definition, evaluate)
        for rendering_rule in ("placeholder row", "current incomplete month"):
            self.assertNotIn(rendering_rule, track)

    def test_readme_endpoint_counts_and_reference_only_reviews_route_are_explicit(self):
        readme = (ROOT / "README.md").read_text()
        readme_zh = (ROOT / "README.zh-CN.md").read_text()
        self.assertNotIn("Amazon Commerce Data, 11 Endpoints", readme)
        self.assertNotIn("数据层概览，11 个 API 接口", readme_zh)
        for path in (
            ROOT / "zoodata" / "references" / "reference.md",
            ROOT / "zoodata" / "references" / "openapi-reference.md",
        ):
            text = path.read_text()
            section = text.split("## 6c. reviews/search", 1)[1].split("\n---", 1)[0]
            self.assertIn("direct API reference only", section)
            self.assertIn("has no\n`reviews/search` subcommand", section)
            self.assertIn("not counted in the 25 CLI-backed", section)

    def test_general_analysis_usage_uses_cli_accumulated_metadata(self):
        guide = (ROOT / "amazon-analysis" / "references" /
                 "execution-guide.md").read_text()
        for field in ("meta.apiCalls", "meta.creditsConsumed",
                      "meta.creditsRemaining"):
            self.assertIn(field, guide)
        self.assertNotIn("_credits.consumed", guide)
        self.assertNotIn("_credits.remaining", guide)
        self.assertNotIn("📊 **API Usage**", guide)

    def test_general_operations_routes_history_by_subject(self):
        ops = (ROOT / "amazon-analysis" / "references" /
               "scenarios-ops.md").read_text()
        self.assertIn("`history` for product-level ASIN history", ops)
        self.assertIn("`market-history` for category-market history", ops)
        self.assertIn("market-history --category-id", ops)
        self.assertIn("history --asins", ops)
        self.assertNotIn("snapshot data only (no historical comparison)", ops.lower())
        self.assertNotIn("compare results manually across snapshots", ops)

    def test_specialized_skill_descriptions_do_not_claim_total_endpoint_count(self):
        for skill_name in ("amazon-listing-audit-pro",
                           "amazon-review-intelligence-extractor"):
            skill = (ROOT / skill_name / "SKILL.md").read_text()
            description = skill.split("description: >", 1)[1].split("metadata:", 1)[0]
            self.assertIn("Uses up to 11 relevant ZooData endpoints", description)
            self.assertNotIn("Uses all 11 ZooData API endpoints", description)


if __name__ == "__main__":
    unittest.main()
