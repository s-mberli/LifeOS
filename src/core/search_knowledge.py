import os
import sys
import sqlite3
import argparse
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

def fts_search(
    query: str,
    limit: int = 5,
    allowed_paths: Optional[set] = None,
    require_insight_note: bool = False,
    include_private: bool = False,
) -> list[tuple]:
    if not DB_PATH.exists():
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        def run_fts_query(q_str: str) -> list[tuple]:
            cursor.execute(
                """
                SELECT path, title, snippet(search_index, 2, '**', '**', '...', 64),
                       bm25(search_index)
                FROM search_index
                WHERE content MATCH ?
                ORDER BY bm25(search_index)
                LIMIT 50
                """,
                (q_str,),
            )
            return cursor.fetchall()

        rows = []
        try:
            rows = run_fts_query(query)
        except sqlite3.OperationalError:
            pass

        if not rows:
            import re
            words = re.findall(r"\b\w+\b", query.lower())
            stopwords = {
                "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
                "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
                "but", "by", "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt",
                "doing", "dont", "down", "during", "each", "few", "for", "from", "further", "had", "hadnt",
                "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here",
                "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im",
                "ive", "if", "in", "into", "is", "isnt", "it", "its", "itself", "lets", "me", "more", "most",
                "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
                "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shant", "she", "shed",
                "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the",
                "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd",
                "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until",
                "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "werent", "what", "whats",
                "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys",
                "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours",
                "yourself", "yourselves"
            }
            tokens = [w for w in words if w not in stopwords]
            if tokens:
                and_query = " AND ".join(tokens)
                try:
                    rows = run_fts_query(and_query)
                except sqlite3.OperationalError:
                    pass

                if not rows:
                    or_query = " OR ".join(tokens)
                    try:
                        rows = run_fts_query(or_query)
                    except sqlite3.OperationalError:
                        pass

        results: list[tuple] = []
        for path, title, snippet, score in rows:
            if not include_private and path.startswith("data/private/"):
                continue
            if require_insight_note and not (path.startswith("data/knowledge/") or path.startswith("data/private/")):
                continue
            if allowed_paths is not None and path not in allowed_paths:
                continue

            results.append((title, path, snippet, score))
            if len(results) >= limit:
                break

        conn.close()
        return results

    except Exception as exc:  # pragma: no cover
        print(f"[helpers] fts_search error: {exc}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search local LifeOS knowledge base.")
    parser.add_argument("query", help="The text to search for")
    parser.add_argument("-n", "--limit", type=int, default=5, help="Number of results to show")
    
    args = parser.parse_args()
    results = fts_search(args.query, args.limit)
    if not results:
        print(f"No results found for: '{args.query}'")
    else:
        print(f"\nSearch Results for: '{args.query}'\n" + "="*50)
        for idx, row in enumerate(results, 1):
            title, path, snippet, score = row
            display_score = abs(score) * 1000
            print(f"{idx}. \033[94m{title}\033[0m (Score: {display_score:.4f})")
            print(f"   Path: \033[92m{path}\033[0m")
            clean_snippet = snippet.replace('\n', ' ').strip()
            print(f"   Snippet: {clean_snippet}")
            print("-" * 50)
