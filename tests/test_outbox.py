import os
import sqlite3
import re
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.core.ingest import process_one_file
from src.core.build_fts_index import build_index
from scripts.triage_outbox import triage_notes

def test_outbox_ingest_and_triage(tmp_project: Path):
    # 1. Verify build_index creates table
    db_path = tmp_project / "indexes" / "lifeos.db"
    
    # Standard directories to index, relative to tmp_project
    dirs_to_index = [
        tmp_project / "data" / "knowledge",
        tmp_project / "data" / "private",
        tmp_project / "data" / "inbox",
        tmp_project / "data" / "experts",
    ]
    for d in dirs_to_index:
        d.mkdir(parents=True, exist_ok=True)
        
    with patch("src.core.build_fts_index.BASE_DIR", tmp_project), \
         patch("src.core.build_fts_index.DIRECTORIES_TO_INDEX", dirs_to_index), \
         patch("src.core.build_fts_index.DB_PATH", db_path):
        build_index()
        
    # Check table existence
    assert db_path.exists()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='automation_outbox'")
    assert cursor.fetchone() is not None
    conn.close()

    # 2. Verify ingest inserts into table
    # Create a raw input file
    input_file = tmp_project / "data" / "inbox" / "raw" / "test_outbox_note.txt"
    input_file.write_text("https://example.com/ai-agents\nSome content mentioning AI architecture and python code.", encoding="utf-8")

    mock_decision = {
        "primary_domain": "general",
        "primary_mode": "router",
        "secondary_modes": [],
        "storage_location": "data/knowledge/",
        "suggested_tags": ["python", "ai"],
        "one_next_action": "Review manually.",
        "privacy": "public",
    }

    with patch("src.core.classify_input.classify", return_value=mock_decision), \
         patch("src.core.llm_client.call_llm", return_value="Test summary"), \
         patch("src.core.build_fts_index.BASE_DIR", tmp_project), \
         patch("src.core.build_fts_index.DIRECTORIES_TO_INDEX", dirs_to_index), \
         patch("src.core.build_fts_index.DB_PATH", db_path), \
         patch("src.core.ingest.ROOT", tmp_project):
        
        res = process_one_file(str(input_file), use_ai=True)
        assert res["success"] is True

        # Check outbox entries
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT note_path, word_count, score, is_actionable, processed_at, hermes_run_at FROM automation_outbox")
        rows = cursor.fetchall()
        assert len(rows) == 1
        note_path, word_count, score, is_actionable, processed_at, hermes_run_at = rows[0]
        assert "test_outbox_note.md" in note_path
        assert word_count > 0
        assert score is None
        assert is_actionable is None
        assert processed_at is None
        assert hermes_run_at is None
        conn.close()

        # 3. Test triage_outbox script
        with patch("scripts.triage_outbox.BASE_DIR", tmp_project), \
             patch("scripts.triage_outbox.DB_PATH", db_path):
            triage_notes()

        # Check that it updated the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT score, is_actionable, processed_at FROM automation_outbox")
        rows = cursor.fetchall()
        assert len(rows) == 1
        score, is_actionable, processed_at = rows[0]
        assert score >= 1 # matched keywords "ai", "architecture", "python"
        assert is_actionable == 1
        assert processed_at is not None
        conn.close()

def test_weekly_hermes_run(tmp_project: Path):
    from scripts.weekly_hermes_run import run_weekly_pipeline

    db_path = tmp_project / "indexes" / "lifeos.db"
    
    # Create the db and table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_outbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_path TEXT,
            source_url TEXT,
            word_count INTEGER,
            added_at TEXT,
            processed_at TEXT,
            score INTEGER,
            is_actionable INTEGER,
            hermes_run_at TEXT
        )
    """)
    # Insert an actionable, triaged note that Hermes hasn't run on yet
    cursor.execute("""
        INSERT INTO automation_outbox (note_path, source_url, word_count, added_at, processed_at, score, is_actionable)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("data/knowledge/arch_note.md", "http://example.com/rule", 200, "2026-05-27T00:00:00", "2026-05-27T00:01:00", 3, 1))
    conn.commit()
    conn.close()

    # Create the mock file
    note_file = tmp_project / "data" / "knowledge" / "arch_note.md"
    note_file.parent.mkdir(parents=True, exist_ok=True)
    note_file.write_text("Use pathlib instead of os.path across the codebase.", encoding="utf-8")

    # Mock subprocess.run
    mock_run = MagicMock()
    mock_run.return_value = MagicMock(returncode=0, stdout="Mocked Hermes Success Output", stderr="")

    # Mock os.path.exists so it thinks the hermes executable exists
    original_exists = os.path.exists
    def mock_exists(path):
        if "hermes" in str(path):
            return True
        return original_exists(path)

    with patch("scripts.weekly_hermes_run.BASE_DIR", tmp_project), \
         patch("scripts.weekly_hermes_run.DB_PATH", db_path), \
         patch("scripts.triage_outbox.BASE_DIR", tmp_project), \
         patch("scripts.triage_outbox.DB_PATH", db_path), \
         patch("os.path.exists", side_effect=mock_exists), \
         patch("subprocess.run", mock_run):
         
        run_weekly_pipeline()

    # Verify subprocess.run was called with correct command
    assert mock_run.called
    cmd_args = mock_run.call_args[0][0]
    assert "--oneshot" in cmd_args
    assert "Use pathlib instead of os" in cmd_args[3]

    # Verify that the DB was updated with hermes_run_at
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT hermes_run_at FROM automation_outbox WHERE id = 1")
    row = cursor.fetchone()
    assert row[0] is not None
    conn.close()

