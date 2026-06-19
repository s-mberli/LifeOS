import sqlite3
from pathlib import Path
from typing import Union

# Base path resolving to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

def get_db_connection(db_path: Union[str, Path] = DB_PATH) -> sqlite3.Connection:
    """Opens a SQLite connection with the sqlite-vec extension loaded.
    
    Gracefully handles:
    - Corrupted database files (deletes and recreates)
    - Missing sqlite-vec extension (logs warning, continues without vector support)
    - Concurrent connections (WAL mode + busy_timeout)
    """
    import logging
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Handle corrupted database: try to open, if it fails delete and recreate
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA integrity_check")
    except (sqlite3.DatabaseError, sqlite3.OperationalError):
        conn.close() if 'conn' in dir() else None
        try:
            db_path.unlink(missing_ok=True)
        except OSError:
            pass
        conn = sqlite3.connect(db_path)
    
    conn.row_factory = sqlite3.Row
    
    # Configure WAL mode and busy timeout (non-fatal)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
    except sqlite3.Error as e:
        logging.warning(f"Failed to configure connection pragmas: {e}")
        
    # Load sqlite-vec extension (non-fatal if unavailable)
    try:
        import sqlite_vec
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
    except (ImportError, sqlite3.OperationalError, AttributeError) as e:
        logging.warning(f"sqlite-vec not available, vector search disabled: {e}")
        
    init_db(conn)
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    """Initializes all SQLite and sqlite-vec tables in an idempotent manner."""
    cursor = conn.cursor()
    
    # Check if doc_chunks needs upgrade (e.g. missing 'wiki_links' or 'title' column)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doc_chunks'")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(doc_chunks)")
        cols = [r[1] for r in cursor.fetchall()]
        if "wiki_links" not in cols or "title" not in cols or "path" not in cols:
            cursor.execute("DROP TABLE doc_chunks")
    
    # 1. Standard tables
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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_repair_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            function_name TEXT,
            mode TEXT,
            error_type TEXT,
            error_message TEXT,
            attempt INTEGER,
            repair_strategy TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_code_provenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            author_agent TEXT,
            model TEXT,
            created_at TEXT,
            review_status TEXT
        )
    """)
    
    # 2. Document Chunks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doc_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            title TEXT,
            chunk_index INTEGER,
            content TEXT,
            wiki_links TEXT
        )
    """)
    
    # 3. sqlite-vec Virtual Table (768 dimensions) — skipped if extension unavailable
    try:
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_docs USING vec0(
                chunk_id INTEGER PRIMARY KEY,
                embedding float[768]
            )
        """)
    except sqlite3.OperationalError:
        pass  # sqlite-vec extension not loaded; vector search will be unavailable
    
    # 4. FTS5 Virtual Table for full-text search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(
            path,
            title,
            content,
            tokenize='porter'
        )
    """)
    
    conn.commit()

