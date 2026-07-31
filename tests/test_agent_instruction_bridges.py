"""Repository-agent entrypoints must bridge to the canonical review contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_instruction_files_are_thin_canonical_bridges():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    for name, text in (("AGENTS.md", agents), ("CLAUDE.md", claude)):
        flat = " ".join(text.split())
        assert "CONTRIBUTING.md" in flat, name
        assert "Skill Specification Ownership" in flat, name
        assert "affected skill's `SKILL.md`" in flat, name
        assert "responsibility map declared there" in flat, name
        assert "relevant consistency tests" in flat, name
        assert "instruction bridge" in flat, name
        assert "Do not copy skill-specific contracts" in flat, name
        assert len(text.splitlines()) < 20, name

        for duplicated_runtime_detail in (
            "HTTP 5xx",
            "HTTP 422",
            "status=empty",
            "workflowDisposition",
            "retryPolicy",
            "parameterMutationAllowed",
            "Stage Handoff Closure Gate",
        ):
            assert duplicated_runtime_detail not in text, (
                name,
                duplicated_runtime_detail,
            )

    assert agents.replace("Repository Agent", "Claude Code Repository") == claude
