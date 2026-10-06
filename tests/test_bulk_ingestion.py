"""
Tests for scripts/core/ingest.py's process_directory function.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.core.ingest import process_directory, process_one_file


def test_process_directory(tmp_project: Path):
    """Test process_directory scans correctly and leaves original files untouched."""
    # Create a source folder to ingest from
    src_dir = tmp_project / "external_ticnotes"
    src_dir.mkdir()

    file1 = src_dir / "note1.txt"
    file1.write_text("Some note content without a URL", encoding="utf-8")

    file2 = src_dir / "note2.md"
    file2.write_text("Another content without URL", encoding="utf-8")

    # A nested directory
    nested_dir = src_dir / "nested"
    nested_dir.mkdir()
    file3 = nested_dir / "note3.md"
    file3.write_text("Nested content", encoding="utf-8")

    # Mocks for build_index and classify_input
    mock_decision = {
        "primary_domain": "general",
        "primary_mode": "router",
        "secondary_modes": [],
        "storage_location": "data/knowledge/general/",
        "suggested_tags": ["test"],
        "one_next_action": "Review manually.",
        "privacy": "public",
    }

    # Ensure target storage location exists in tmp_project
    (tmp_project / "data" / "knowledge" / "general").mkdir(parents=True, exist_ok=True)

    with patch("src.core.ingest.ROOT", tmp_project), \
         patch("src.core.classify_input.classify", return_value=mock_decision), \
         patch("src.core.build_fts_index.build_index", return_value={"indexed": 3, "skipped": 0}):

        res = process_directory(src_dir, use_ai=False)

        assert res["success"] is True
        assert len(res["processed"]) == 3
        assert len(res["failed"]) == 0

        # Verify original files still exist (process_directory copies them, process_one_file moves the copy, original is untouched)
        assert file1.exists()
        assert file2.exists()
        assert file3.exists()

        # Check that output notes were created under the destination general folder
        dest_dir = tmp_project / "data" / "knowledge" / "general"
        assert dest_dir.exists()
        dest_files = list(dest_dir.glob("*.md"))
        assert len(dest_files) == 3


def test_process_directory_empty(tmp_project: Path):
    """Test that process_directory handles empty directories gracefully."""
    src_dir = tmp_project / "empty_dir"
    src_dir.mkdir()

    callback_messages = []
    def callback(msg):
        callback_messages.append(msg)

    res = process_directory(src_dir, use_ai=False, status_callback=callback)

    assert res["success"] is True
    assert len(res["processed"]) == 0
    assert len(res["failed"]) == 0
    assert any("no .txt or .md files found" in msg.lower() for msg in callback_messages)


def test_process_directory_mixed_extensions(tmp_project: Path):
    """Test that process_directory only ingests .txt and .md files, ignoring others."""
    src_dir = tmp_project / "mixed_dir"
    src_dir.mkdir()

    file_txt = src_dir / "note.txt"
    file_txt.write_text("Hello text", encoding="utf-8")

    file_pdf = src_dir / "doc.pdf"
    file_pdf.write_text("Binary pdf data", encoding="utf-8")

    file_png = src_dir / "image.png"
    file_png.write_text("Binary image data", encoding="utf-8")

    mock_decision = {
        "primary_domain": "general",
        "primary_mode": "router",
        "secondary_modes": [],
        "storage_location": "data/knowledge/general/",
        "suggested_tags": ["test"],
        "one_next_action": "Review manually.",
        "privacy": "public",
    }
    (tmp_project / "data" / "knowledge" / "general").mkdir(parents=True, exist_ok=True)

    with patch("src.core.ingest.ROOT", tmp_project), \
         patch("src.core.classify_input.classify", return_value=mock_decision), \
         patch("src.core.build_fts_index.build_index", return_value={"indexed": 1, "skipped": 0}):

        res = process_directory(src_dir, use_ai=False)

        assert res["success"] is True
        assert len(res["processed"]) == 1
        assert len(res["failed"]) == 0
        assert res["processed"][0]["original_path"] == str(file_txt)


def test_youtube_transcript_uses_canonical_knowledge_dir(tmp_project: Path):
    source = tmp_project / "data" / "inbox" / "raw" / "video.txt"
    source.write_text("https://www.youtube.com/watch?v=example", encoding="utf-8")
    decision = {
        "primary_domain": "general",
        "primary_mode": "router",
        "secondary_modes": [],
        "storage_location": "data/knowledge/general/",
        "suggested_tags": [],
        "one_next_action": "Review manually.",
        "privacy": "public",
    }
    metadata = {
        "title": "Example video",
        "source_url": "https://www.youtube.com/watch?v=example",
        "is_youtube": True,
        "transcript": "Example transcript",
        "channel": "Example Channel",
        "fetched_web_text": "",
    }

    with patch("src.core.ingest.ROOT", tmp_project), \
         patch("src.core.ingest._extract_metadata", return_value=metadata), \
         patch("src.core.ingest._get_routing_decision", return_value=decision), \
         patch("src.core.ingest._run_cheap_triage", return_value=None), \
         patch("core.youtube.save_transcript") as save_transcript, \
         patch("src.core.build_fts_index.build_index"):
        save_transcript.return_value = tmp_project / "data" / "knowledge" / "ai-resources" / "raw" / "video_transcript.md"
        result = process_one_file(str(source), use_ai=False)

    assert result["success"] is True
    assert save_transcript.call_args.args[2] == tmp_project / "data" / "knowledge" / "ai-resources" / "raw"

