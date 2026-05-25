import os
import sys
import sqlite3
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

def search(query: str, limit: int = 5):
    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        print("Please run 'python scripts/build_fts_index.py' first.")
        sys.exit(1)
        
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We use snippet() for content (column index 2: path=0, title=1, content=2)
    # \033[1m and \033[0m are ANSI escape codes for bold text
    sql = """
        SELECT 
            title, 
            path, 
            snippet(search_index, 2, '\033[1m', '\033[0m', '...', 30) AS matched_snippet,
            bm25(search_index) AS score
        FROM search_index 
        WHERE search_index MATCH ?
        ORDER BY score
        LIMIT ?
    """
    
    try:
        # FTS5 matches can use prefixes, e.g., if query is 'agent*', so we can just pass it directly
        # or we could append * to each word for simpler prefix matching, but let's just pass raw query first
        cursor.execute(sql, (query, limit))
        results = cursor.fetchall()
        
        if not results:
            print(f"No results found for: '{query}'")
            return
            
        print(f"\nSearch Results for: '{query}'\n" + "="*50)
        
        for idx, row in enumerate(results, 1):
            title, path, snippet, score = row
            # FTS5 bm25 score is typically negative (more negative is better).
            # It can be very small for small datasets, so we multiply by a scaling factor for readability.
            display_score = abs(score) * 1000
            print(f"{idx}. \033[94m{title}\033[0m (Score: {display_score:.4f})")
            print(f"   Path: \033[92m{path}\033[0m")
            # Replace newlines in snippet to make it cleaner to display
            clean_snippet = snippet.replace('\n', ' ').strip()
            print(f"   Snippet: {clean_snippet}")
            print("-" * 50)
            
    except sqlite3.OperationalError as e:
        print(f"Search query error: {e}")
        print("Tip: You might need to use quotes for exact phrases, or avoid special characters.")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search local LifeOS knowledge base.")
    parser.add_argument("query", help="The text to search for")
    parser.add_argument("-n", "--limit", type=int, default=5, help="Number of results to show")
    
    args = parser.parse_args()
    search(args.query, args.limit)
