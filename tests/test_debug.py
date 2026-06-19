import sys
import sqlite3
from src.core.db import get_db_connection

def test_debug_imports():
    from src.core.db import get_db_connection
    conn = get_db_connection(":memory:")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(doc_chunks)")
    cols = [row[1] for row in cursor.fetchall()]
    print("DEBUG DOC_CHUNKS COLS:", cols)
    conn.close()
    assert False

