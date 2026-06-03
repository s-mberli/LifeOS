"""
Tests for user manual memory helpers in ui/helpers.py.
"""
import sqlite3
import pytest
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
    sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

from ui.helpers import (
    add_user_memory, get_user_memories, toggle_user_memory, delete_user_memory
)

@pytest.fixture
def memory_db(tmp_path):
    """Fixture to provide a temporary database for testing memory functions."""
    db_path = tmp_path / "lifeos.db"
    
    # Mock the DB_PATH used by the helpers to point to our temp DB
    with patch("ui.helpers.DB_PATH", db_path):
        # We need to initialize the table. get_user_memories() does this automatically.
        get_user_memories()
        yield db_path

def test_add_and_get_user_memories(memory_db):
    """Test adding a memory and retrieving it."""
    assert add_user_memory("Test Title", "Test Content") is True
    
    memories = get_user_memories()
    assert len(memories) == 1
    assert memories[0]["title"] == "Test Title"
    assert memories[0]["content"] == "Test Content"
    assert memories[0]["is_active"] == 1

def test_get_active_only(memory_db):
    """Test retrieving only active memories."""
    add_user_memory("Active Mem", "Content 1")
    add_user_memory("Inactive Mem", "Content 2")
    
    memories = get_user_memories()
    assert len(memories) == 2
    
    # Set the second memory to inactive
    inactive_id = memories[0]["id"] if memories[0]["title"] == "Inactive Mem" else memories[1]["id"]
    assert toggle_user_memory(inactive_id, False) is True
    
    # Get all memories again
    all_memories = get_user_memories()
    assert len(all_memories) == 2
    
    # Get active only
    active_memories = get_user_memories(active_only=True)
    assert len(active_memories) == 1
    assert active_memories[0]["title"] == "Active Mem"

def test_delete_user_memory(memory_db):
    """Test deleting a memory."""
    add_user_memory("To Delete", "Content")
    memories = get_user_memories()
    assert len(memories) == 1
    
    assert delete_user_memory(memories[0]["id"]) is True
    
    assert len(get_user_memories()) == 0

def test_no_db_returns_empty(tmp_path):
    """Test when DB_PATH doesn't exist."""
    db_path = tmp_path / "does_not_exist.db"
    with patch("ui.helpers.DB_PATH", db_path):
        assert get_user_memories() == []
