"""
tests/test_ai_reviewer.py — Unit tests for scripts/ai_code_reviewer.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from unittest import mock

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import scripts.ai_code_reviewer as reviewer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CLEAN_CODE = '''\
def add(a: int, b: int) -> int:
    """Return sum of a and b."""
    return a + b
'''

DIRTY_CODE = '''\
import os
import sys

API_KEY = "sk-1234567890abcdef"  # hardcoded secret

def fetch(url):
    result = os.system("curl " + url)  # shell injection
    return result
'''


def _make_db(tmp_path: Path) -> Path:
    db = tmp_path / "test.db"
    return db


# ---------------------------------------------------------------------------
# log_provenance
# ---------------------------------------------------------------------------

class TestLogProvenance:
    def test_inserts_new_record(self, tmp_path):
        db = _make_db(tmp_path)
        reviewer.log_provenance("scripts/foo.py", "Human", "Passed", db_path=db)

        with sqlite3.connect(db) as conn:
            row = conn.execute(
                "SELECT file_path, author_agent, review_status FROM ai_code_provenance"
            ).fetchone()

        assert row == ("scripts/foo.py", "Human", "Passed")

    def test_upserts_existing_record(self, tmp_path):
        db = _make_db(tmp_path)
        reviewer.log_provenance("scripts/foo.py", "Human", "Passed", db_path=db)
        reviewer.log_provenance("scripts/foo.py", "Hermes", "Passed (Auto-Fixed)", db_path=db)

        with sqlite3.connect(db) as conn:
            rows = conn.execute(
                "SELECT * FROM ai_code_provenance WHERE file_path = 'scripts/foo.py'"
            ).fetchall()

        assert len(rows) == 1
        assert rows[0][2] == "Hermes"  # author_agent updated
        assert rows[0][5] == "Passed (Auto-Fixed)"  # review_status updated


# ---------------------------------------------------------------------------
# _extract_code_block
# ---------------------------------------------------------------------------

class TestExtractCodeBlock:
    def test_extracts_python_block(self):
        response = "Some text\n```python\nprint('hello')\n```\nMore text"
        assert reviewer._extract_code_block(response) == "print('hello')"

    def test_returns_none_if_no_block(self):
        assert reviewer._extract_code_block("[PASSED]") is None

    def test_returns_none_if_unclosed(self):
        assert reviewer._extract_code_block("```python\nprint('x')") is None


# ---------------------------------------------------------------------------
# review_and_fix_file
# ---------------------------------------------------------------------------

class TestReviewAndFixFile:
    def test_passes_clean_code(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text(CLEAN_CODE)
        db = _make_db(tmp_path)

        with mock.patch("src.core.llm_client.call_llm", return_value="[PASSED]"):
            result = reviewer.review_and_fix_file(f, "Human", db_path=db)

        assert result is True
        # File unchanged
        assert f.read_text() == CLEAN_CODE

        with sqlite3.connect(db) as conn:
            row = conn.execute("SELECT review_status FROM ai_code_provenance").fetchone()
        assert row[0] == "Passed"

    def test_auto_fixes_dirty_code(self, tmp_path):
        f = tmp_path / "dirty.py"
        f.write_text(DIRTY_CODE)
        db = _make_db(tmp_path)

        fixed = "def fetch(url: str) -> int:\n    return 0\n"
        llm_response = f"## Issues\n- Hardcoded secret\n```python\n{fixed}```"

        with mock.patch("src.core.llm_client.call_llm", return_value=llm_response):
            result = reviewer.review_and_fix_file(f, "Hermes", db_path=db)

        assert result is True
        assert f.read_text().strip() == fixed.strip()
        # Backup created
        assert (tmp_path / "dirty.py.bak").exists()

        with sqlite3.connect(db) as conn:
            row = conn.execute("SELECT review_status FROM ai_code_provenance").fetchone()
        assert row[0] == "Passed (Auto-Fixed)"

    def test_dry_run_does_not_overwrite(self, tmp_path):
        f = tmp_path / "dirty.py"
        f.write_text(DIRTY_CODE)
        db = _make_db(tmp_path)

        fixed = "def fetch(url: str) -> int:\n    return 0\n"
        llm_response = f"## Issues\n- secret\n```python\n{fixed}```"

        with mock.patch("src.core.llm_client.call_llm", return_value=llm_response):
            result = reviewer.review_and_fix_file(f, "Human", dry_run=True, db_path=db)

        assert result is False
        assert f.read_text() == DIRTY_CODE  # unchanged

    def test_skips_file_exceeding_size_limit(self, tmp_path):
        f = tmp_path / "huge.py"
        f.write_text("x = 1\n" * 10_000)  # ~60k chars
        db = _make_db(tmp_path)

        with mock.patch("src.core.llm_client.call_llm") as mock_llm:
            result = reviewer.review_and_fix_file(f, "Human", db_path=db)

        mock_llm.assert_not_called()
        assert result is True  # doesn't block commit

    def test_returns_false_on_llm_failure(self, tmp_path):
        f = tmp_path / "code.py"
        f.write_text(CLEAN_CODE)
        db = _make_db(tmp_path)

        with mock.patch("src.core.llm_client.call_llm", return_value=None):
            result = reviewer.review_and_fix_file(f, "Human", db_path=db)

        assert result is False

    def test_returns_false_missing_file(self, tmp_path):
        db = _make_db(tmp_path)
        result = reviewer.review_and_fix_file(tmp_path / "nope.py", "Human", db_path=db)
        assert result is False
