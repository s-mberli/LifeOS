import os
import re
from pathlib import Path
from src.core.db import get_db_connection, init_db
from src.core.llm_client import get_embeddings

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INDEX_DIR = BASE_DIR / "indexes"
DB_PATH = INDEX_DIR / "lifeos.db"

# Directories to index
DIRECTORIES_TO_INDEX = [
    BASE_DIR / "data" / "knowledge",
    BASE_DIR / "data" / "private",
    BASE_DIR / "data" / "inbox",
    BASE_DIR / "data" / "experts",
    BASE_DIR / "data" / "business",
    BASE_DIR / "data" / "career",
    BASE_DIR / "outputs"
]

def extract_title(content: str, filename: str) -> str:
    """Attempt to extract title from frontmatter or H1. Fall back to filename."""
    # Check for title in simple frontmatter block (title: ...)
    title_match = re.search(r'^title:\s*(.+)$', content, flags=re.MULTILINE | re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip(" \"'")
    
    # Check for first H1 tag
    h1_match = re.search(r'^#\s+(.+)$', content, flags=re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return filename

def build_index():
    print("Building local FTS5 index...")
    
    # Ensure index directory exists
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    # Connect to SQLite using connection manager
    conn = get_db_connection(DB_PATH)
    cursor = conn.cursor()
    
    # Drop transient search and vector indexing tables to ensure full rebuild
    cursor.execute("DROP TABLE IF EXISTS search_index")
    cursor.execute("DROP TABLE IF EXISTS vec_docs")
    cursor.execute("DROP TABLE IF EXISTS doc_chunks")
    
    # Re-initialize the tables
    init_db(conn)
    
    indexed_count = 0
    skipped_count = 0
    
    for directory in DIRECTORIES_TO_INDEX:
        if not directory.exists():
            print(f"Skipping {directory} (does not exist)")
            continue
            
        # Iterate through all files in directory
        for filepath in directory.rglob("*"):
            if not filepath.is_file():
                continue
                
            path_str = str(filepath)
            
            # Exclusions
            if "/raw/" in path_str.replace('\\', '/'):
                skipped_count += 1
                continue
            if ".env" in filepath.name:
                skipped_count += 1
                continue
            if filepath.suffix.lower() not in ['.md', '.txt']:
                skipped_count += 1
                continue
                
            try:
                relative_path = str(filepath.relative_to(BASE_DIR))
                index_file(relative_path, conn)
                indexed_count += 1
            except Exception as e:
                print(f"Error indexing {filepath}: {e}")
                skipped_count += 1
                
    conn.commit()
    conn.close()
    
    print(f"Index build complete.")
    print(f"Files indexed: {indexed_count}")
    print(f"Files skipped (non-md, raw, etc): {skipped_count}")
    print("Folders indexed:")
    for d in DIRECTORIES_TO_INDEX:
        if d.exists():
            print(f"  - {d.relative_to(BASE_DIR)}")
    print(f"Database saved to: {DB_PATH}")
    return {"indexed": indexed_count, "skipped": skipped_count, "error": None}

def chunk_markdown(text: str, chunk_size: int = 1000, overlap: int | None = None) -> list[str]:
    if overlap is None:
        overlap = 200 if chunk_size > 200 else 0
    if overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk size")
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += chunk_size - overlap
    return chunks

def extract_wikilinks(text: str) -> list[str]:
    results = []
    i = 0
    n = len(text)
    while i < n:
        if text[i:i+2] == '[[':
            depth = 1
            j = i + 2
            content_start = j
            while j < n - 1:
                if text[j:j+2] == '[[':
                    depth += 1
                    j += 2
                elif text[j:j+2] == ']]':
                    depth -= 1
                    if depth == 0:
                        link_text = text[content_start:j]
                        results.append(link_text)
                        results.extend(extract_wikilinks(link_text))
                        break
                    j += 2
                else:
                    j += 1
            i = j + 2
        else:
            i += 1
            
    cleaned = []
    for r in results:
        c = r.strip()
        if c and c not in cleaned:
            cleaned.append(c)
    return cleaned

def index_file(db_path, filepath=None):
    import json
    import os
    import struct
    import time
    from pathlib import Path
    from src.core.db import get_db_connection

    # Determine signature
    is_conn = False
    if filepath is not None:
        if hasattr(filepath, 'cursor') or hasattr(filepath, 'execute'):
            is_conn = True

    if filepath is None or is_conn:
        # Signature: index_file(filepath, conn)
        conn = filepath
        filepath_val = str(db_path)
        should_close = False
    else:
        # Signature: index_file(db_path, filepath)
        filepath_val = str(filepath)
        conn = get_db_connection(db_path)
        should_close = True

    try:
        cursor = conn.cursor()
        
        # Resolve to absolute path for opening
        abs_path = Path(filepath_val)
        if not abs_path.is_absolute():
            abs_path = BASE_DIR / abs_path
            
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            relative_path = str(Path(filepath_val).relative_to(BASE_DIR))
        except ValueError:
            try:
                relative_path = str(Path(filepath_val).resolve().relative_to(BASE_DIR.resolve()))
            except ValueError:
                relative_path = filepath_val
            
        title = extract_title(content, os.path.basename(filepath_val))
        chunks = chunk_markdown(content, chunk_size=1000, overlap=200)
        
        # Fetch embeddings outside transaction to avoid database lock contention
        embeddings = []
        for chunk in chunks:
            try:
                emb = get_embeddings(chunk)
            except Exception:
                emb = [0.0] * 768
            embeddings.append(emb)
            
        # Write to DB with retry logic
        for attempt in range(5):
            try:
                cursor.execute("DELETE FROM vec_docs WHERE chunk_id IN (SELECT id FROM doc_chunks WHERE path = ?)", (relative_path,))
                cursor.execute("DELETE FROM doc_chunks WHERE path = ?", (relative_path,))
                cursor.execute("DELETE FROM search_index WHERE path = ?", (relative_path,))
                
                for idx, chunk in enumerate(chunks):
                    links = extract_wikilinks(chunk)
                    wiki_links_json = json.dumps(links)
                    cursor.execute(
                        "INSERT INTO doc_chunks (path, chunk_index, content, wiki_links) VALUES (?, ?, ?, ?)",
                        (relative_path, idx, chunk, wiki_links_json)
                    )
                    chunk_id = cursor.lastrowid
                    
                    emb_data = struct.pack(f"{len(embeddings[idx])}f", *embeddings[idx])
                    cursor.execute(
                        "INSERT INTO vec_docs (chunk_id, embedding) VALUES (?, ?)",
                        (chunk_id, emb_data)
                    )
                    
                    cursor.execute(
                        "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
                        (relative_path, title, chunk)
                    )
                conn.commit()
                break
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < 4:
                    time.sleep(0.05 * (attempt + 1))
                else:
                    raise
                    
        return {"chunks_indexed": len(chunks)}
    finally:
        if should_close and conn is not None:
            conn.close()

if __name__ == "__main__":
    build_index()

