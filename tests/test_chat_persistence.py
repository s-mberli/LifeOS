"""
Tests for scripts/core/chat_persistence.py.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.core.chat_persistence import append_to_daily_chat_log, save_message_as_insight
from src.core.frontmatter import read_fm


def test_append_to_daily_chat_log(tmp_project: Path):
    """Test that chat logs are appended correctly and write valid frontmatter."""
    with patch("src.core.chat_persistence.ROOT", tmp_project):
        success = append_to_daily_chat_log(
            user_prompt="Who is David Deida?",
            assistant_response="He is a spiritual teacher.",
            expert_slugs=["expert--david-deida"]
        )
        assert success is True

        # Check that file exists
        date_str = datetime.date.today().isoformat()
        log_file = tmp_project / "data" / "private" / "chat-logs" / f"chat-{date_str}.md"
        assert log_file.exists()

        # Read back frontmatter and body
        fm, body = read_fm(log_file)
        assert fm["type"] == "daily_chat_log"
        assert fm["date"] == date_str
        assert "Who is David Deida?" in body
        assert "He is a spiritual teacher." in body
        assert "expert--david-deida" in body

        # Append another message and verify it's added
        success2 = append_to_daily_chat_log(
            user_prompt="What is his main concept?",
            assistant_response="Masculine and feminine polarity.",
        )
        assert success2 is True
        fm2, body2 = read_fm(log_file)
        assert "What is his main concept?" in body2
        assert "Masculine and feminine polarity." in body2


def test_save_message_as_insight(tmp_project: Path):
    """Test that saving a message creates an insight note and assigns it to an expert."""
    expert_slug = "expert--david-deida"
    expert_name = "David Deida"

    # Set up expert directory and scaffolds
    expert_dir = tmp_project / "data" / "experts" / expert_slug
    expert_dir.mkdir(parents=True, exist_ok=True)
    (expert_dir / "profile.md").write_text("# Profile", encoding="utf-8")

    with patch("src.core.chat_persistence.ROOT", tmp_project), \
         patch("src.core.experts.ROOT", tmp_project), \
         patch("src.core.build_fts_index.build_index", return_value={"indexed": 1, "skipped": 0}):

        success, out_path_str = save_message_as_insight(
            user_prompt="Explain intimacy practices",
            assistant_response="Intimacy practices include breathing together.",
            expert_slugs=[expert_slug],
            expert_names=[expert_name]
        )

        assert success is True
        assert out_path_str != ""
        out_path = Path(out_path_str)
        assert out_path.exists()

        # Verify frontmatter and body
        fm, body = read_fm(out_path)
        assert fm["type"] == "insight_note"
        assert fm["expert_status"] == "attached"
        assert expert_slug in fm["attached_experts"]
        assert "intimacy" in fm["title"].lower()

        assert "Explain intimacy practices" in body
        assert "Intimacy practices include breathing together." in body

        # Verify expert reference file was created
        sources_dir = expert_dir / "sources"
        assert sources_dir.exists()
        ref_files = list(sources_dir.glob("*-ref.md"))
        assert len(ref_files) == 1
        ref_fm, ref_body = read_fm(ref_files[0])
        assert ref_fm["type"] == "expert_source_reference"
        assert ref_fm["expert_slug"] == expert_slug


def test_save_message_as_insight_empty_history(tmp_project: Path):
    """Test that saving a message works even if user question is empty/blank."""
    with patch("src.core.chat_persistence.ROOT", tmp_project), \
         patch("src.core.build_fts_index.build_index", return_value={"indexed": 1, "skipped": 0}):

        success, out_path_str = save_message_as_insight(
            user_prompt="",
            assistant_response="Direct answer without question."
        )

        assert success is True
        assert out_path_str != ""
        out_path = Path(out_path_str)
        assert out_path.exists()

        fm, body = read_fm(out_path)
        assert fm["title"] == "Saved Chat Insight"
        assert "Direct answer without question." in body


def test_save_message_as_insight_write_error(tmp_project: Path):
    """Test that saving handles file write errors gracefully by returning success=False."""
    with patch("src.core.chat_persistence.ROOT", tmp_project), \
         patch("src.core.frontmatter.write_fm", side_effect=OSError("Disk full")):

        success, out_path_str = save_message_as_insight(
            user_prompt="Write error test",
            assistant_response="Response."
        )

        assert success is False
        assert out_path_str == ""

