"""Ownership and scenario routing for the unified market skill."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "amazon-market-analysis"
RETAINED_MARKET_SOURCE_SKILLS = {
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

        for retained_source in RETAINED_MARKET_SOURCE_SKILLS:
            self.assertTrue((ROOT / retained_source / "SKILL.md").is_file())

        sync_script = (ROOT / "scripts" / "sync-scripts.sh").read_text()
        self.assertIn("retained source package", sync_script)

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

    def test_unpublished_experimental_overview_is_not_a_runnable_command(self):
        skill = (MARKET / "SKILL.md").read_text()
        manifest = (MARKET / "scripts" / "allowed-commands.json").read_text()
        self.assertIn("were never published", skill)
        self.assertIn("outside the supported interface", skill)
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
        shared_contract = (MARKET / "references" /
                           "analysis-contract.md").read_text()
        self.assertIn("one `categories --parent", scenario)
        self.assertIn("to enumerate **all direct child IDs**", scenario)
        self.assertIn("one `categories` call plus one `markets/search` call", scenario)
        self.assertIn("`market --category-ids ID1,ID2,... --page-size 100`", scenario)
        self.assertIn("**every** enumerated child", scenario)
        self.assertIn("`category.ids` in one `markets/search` request", reference)
        self.assertIn("`--parent` requires a nonempty JSON string array", reference)
        self.assertIn("`meta.total` counts matching rows after filters", reference)
        self.assertIn("transcript folding or truncation", shared_contract)
        self.assertNotIn("Select a bounded set of those IDs", scenario)

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
                self.assertNotIn("sampleConservative", text)
        for path in (ROOT / "zoodata" / "references").glob("*.md"):
            self.assertNotIn("topSalesRate", path.read_text(), path.name)
        for path in ROOT.glob("amazon-*/references/*.md"):
            if path.parent.parent.name in RETAINED_MARKET_SOURCE_SKILLS:
                continue
            text = path.read_text()
            self.assertNotIn("topSalesRate", text, str(path))
            self.assertNotIn("sampleConservative", text, str(path))
            self.assertNotIn("actualStartDate", text, str(path))
            self.assertNotIn("actualEndDate", text, str(path))

    def test_general_analysis_usage_uses_cli_accumulated_metadata(self):
        guide = (ROOT / "amazon-analysis" / "references" /
                 "execution-guide.md").read_text()
        for field in ("meta.apiCalls", "meta.creditsConsumed",
                      "meta.creditsRemaining"):
            self.assertIn(field, guide)
        self.assertNotIn("_credits.consumed", guide)
        self.assertNotIn("_credits.remaining", guide)
        self.assertNotIn("📊 **API Usage**", guide)


if __name__ == "__main__":
    unittest.main()
