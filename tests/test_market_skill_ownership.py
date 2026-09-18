"""Ownership and scenario routing for the unified market skill."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKET = ROOT / "amazon-market-analysis"


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

        for retired in (
            "amazon-market-entry-analyzer", "amazon-market-trend-scanner",
            "amazon-opportunity-discoverer",
        ):
            self.assertFalse((ROOT / retired / "SKILL.md").exists())

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

    def test_removed_overview_is_not_a_runnable_command(self):
        skill = (MARKET / "SKILL.md").read_text()
        manifest = (MARKET / "scripts" / "allowed-commands.json").read_text()
        self.assertIn("removed market overview endpoint", skill)
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
        self.assertIn("`categories --parent` to enumerate **all direct child IDs**", scenario)
        self.assertIn("`market --category-ids ID1,ID2,... --page-size 100`", scenario)
        self.assertIn("**every** enumerated child", scenario)
        self.assertIn("`category.ids` in one `markets/search` request", reference)
        self.assertIn("`meta.total` counts matching rows after filters", reference)
        self.assertNotIn("Select a bounded set of those IDs", scenario)

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
