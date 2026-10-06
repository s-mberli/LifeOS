from src.core.db import get_db_connection

def test_doc_chunks_schema_is_initialized(tmp_path):
    conn = get_db_connection(tmp_path / "lifeos.db")
    try:
        cols = {row[1] for row in conn.execute("PRAGMA table_info(doc_chunks)")}
    finally:
        conn.close()
    assert {"id", "path", "title", "chunk_index", "content", "wiki_links"} <= cols

