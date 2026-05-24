import os
import sqlite3
import re
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE_DIR / "indexes"
DB_PATH = INDEX_DIR / "lifeos.db"

# Directories to index
DIRECTORIES_TO_INDEX = [
    BASE_DIR / "data" / "knowledge",
    BASE_DIR / "data" / "private",
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
    
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create FTS5 virtual table
    # We drop it first to ensure a full rebuild
    cursor.execute("DROP TABLE IF EXISTS search_index")
    cursor.execute("""
        CREATE VIRTUAL TABLE search_index USING fts5(
            path,
            title,
            content,
            tokenize='porter'
        )
    """)
    
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
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                title = extract_title(content, filepath.name)
                relative_path = str(filepath.relative_to(BASE_DIR))
                
                cursor.execute(
                    "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
                    (relative_path, title, content)
                )
                indexed_count += 1
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
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

if __name__ == "__main__":
    build_index()
