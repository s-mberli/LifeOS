import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.core.db import get_db_connection, init_db

def test_get_db_connection_success(tmp_path):
    db_path = tmp_path / "test.db"
    conn = get_db_connection(db_path)
    assert isinstance(conn, sqlite3.Connection)
    
    # Verify row_factory is set
    assert conn.row_factory == sqlite3.Row
    
    # Verify we can run vec_version
    cursor = conn.cursor()
    cursor.execute("select vec_version()")
    row = cursor.fetchone()
    assert row is not None
    version = row[0]
    assert isinstance(version, str)
    assert len(version) > 0
    conn.close()

def test_init_db_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    conn = get_db_connection(db_path)
    
    # Run init_db
    init_db(conn)
    
    # Verify tables exist
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cursor.fetchall()]
    
    expected_tables = [
        "automation_outbox",
        "user_memory",
        "agent_repair_logs",
        "ai_code_provenance",
        "doc_chunks",
        "vec_docs",
        "search_index"
    ]
    for table in expected_tables:
        assert table in tables
        
    # Test idempotency - running it again doesn't fail
    init_db(conn)
    conn.close()

def test_get_db_connection_graceful_on_missing_extension(tmp_path):
    """Missing sqlite-vec logs warning but does NOT crash — graceful degradation."""
    db_path = tmp_path / "test.db"
    mock_sqlite_vec = MagicMock()
    mock_sqlite_vec.load.side_effect = sqlite3.OperationalError("mock error")
    with patch.dict("sys.modules", {"sqlite_vec": mock_sqlite_vec}):
        try:
            conn = get_db_connection(db_path)
            assert isinstance(conn, sqlite3.Connection)
            conn.close()
        except RuntimeError:
            pytest.fail("Should not raise RuntimeError on missing sqlite-vec")


def test_get_db_connection_graceful_on_import_error(tmp_path):
    """ImportError for sqlite_vec logs warning but returns a usable connection."""
    db_path = tmp_path / "test2.db"
    with patch.dict("sys.modules", {"sqlite_vec": None}):
        try:
            conn = get_db_connection(db_path)
            assert isinstance(conn, sqlite3.Connection)
            conn.close()
        except RuntimeError:
            pytest.fail("Should not raise RuntimeError on import error")
