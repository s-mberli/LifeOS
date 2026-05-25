"""
Tests for scripts/core/ingest.py's process_directory function.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from scripts.core.ingest import process_directory


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

    with patch("scripts.core.ingest.ROOT", tmp_project), \
         patch("classify_input.classify", return_value=mock_decision), \
         patch("build_fts_index.build_index", return_value={"indexed": 3, "skipped": 0}):

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

    with patch("scripts.core.ingest.ROOT", tmp_project), \
         patch("classify_input.classify", return_value=mock_decision), \
         patch("build_fts_index.build_index", return_value={"indexed": 1, "skipped": 0}):

        res = process_directory(src_dir, use_ai=False)

        assert res["success"] is True
        assert len(res["processed"]) == 1
        assert len(res["failed"]) == 0
        assert res["processed"][0]["original_path"] == str(file_txt)

