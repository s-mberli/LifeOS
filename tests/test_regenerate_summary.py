"""
Tests for regenerate_insight_summary.
"""
from pathlib import Path
import pytest
from unittest.mock import patch

from src.core.ingest import regenerate_insight_summary
import src.core.ingest as ingest_mod


def test_regenerate_insight_summary_success(tmp_project: Path, sample_insight: Path):
    """Verify that regenerate_insight_summary successfully updates the note with LLM data."""
    # Redirect ROOT to tmp_project
    original_root = ingest_mod.ROOT
    ingest_mod.ROOT = tmp_project

    # Setup fake raw content under Original Content in sample_insight
    sample_insight.write_text(
        "---\n"
        'title: "Test Note"\n'
        "type: insight_note\n"
        "domain: ai-platform\n"
        'source_url: "https://example.com"\n'
        "tags:\n"
        "  - ai\n"
        "  - test\n"
        "expert_status: unattached\n"
        "attached_experts: []\n"
        "---\n\n"
        "# Test Note\n\n"
        "## Original Content\n"
        "### Raw User Input\n"
        "This is the raw content that needs to be summarized.\n",
        encoding="utf-8",
    )

    fake_ai_data = {
        "summary": "This is a new regenerated summary.",
        "key_ideas": ["Regenerated idea 1", "Regenerated idea 2"],
        "why_this_matters_for_markus": ["Matters because X"],
        "related_modes": ["Mode A"],
        "next_action": "Do the next thing",
        "suggested_tags": ["new-tag", "ai"],
        "is_chunked": False,
        "provider_used": "TestProvider",
        "model_used": "TestModel",
        "source_reliability": "Highly reliable test resource",
    }

    try:
        with patch("src.core.ingest.generate_resource_summary", return_value=fake_ai_data):
            res = regenerate_insight_summary(sample_insight)
            assert res["success"] is True

        # Read back frontmatter and body
        from src.core.frontmatter import read_fm
        fm, body = read_fm(sample_insight)

        # Tags should be merged
        assert "new-tag" in fm["tags"]
        assert "ai" in fm["tags"]
        assert "test" in fm["tags"]

        # Body should contain new summary sections
        assert "This is a new regenerated summary." in body
        assert "Regenerated idea 1" in body
        assert "Matters because X" in body
        assert "Do the next thing" in body
        assert "Highly reliable test resource" in body
        
        # Original content section must be preserved
        assert "## Original Content" in body
        assert "This is the raw content that needs to be summarized." in body

    finally:
        ingest_mod.ROOT = original_root


def test_regenerate_insight_summary_no_file(tmp_project: Path):
    """Verify that it fails gracefully when file does not exist."""
    res = regenerate_insight_summary(tmp_project / "non-existent-note.md")
    assert res["success"] is False
    assert "does not exist" in res["error"]
