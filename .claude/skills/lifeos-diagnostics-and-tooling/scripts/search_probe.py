#!/usr/bin/env python
"""search_probe.py — retrieval smoke probe against the golden query list.

Default mode runs FTS5 MATCH queries directly against a READ-ONLY
(mode=ro&immutable=1) connection — no API calls, no cost, no writes.
It deliberately does NOT import src.core.db.get_db_connection (that
function runs init_db writes and can delete a DB it considers corrupted).

`--hybrid` additionally runs src.core.search_knowledge.hybrid_search,
which makes a real PAID OpenRouter embeddings API call per query and uses
the repo's own (non-read-only) DB connection — opt-in only. Do not use
--hybrid while an index rebuild is in progress.

Privacy: prints titles, paths and scores only. Never prints note bodies.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_PATH = REPO_ROOT / "indexes" / "lifeos.db"

# Golden queries: verified to return FTS results as of 2026-07-07.
GOLDEN_QUERIES = ["sqlite", "agent", "architecture", "pipeline"]


def rel(path: str) -> str:
    try:
        return str(Path(path).relative_to(REPO_ROOT))
    except ValueError:
        return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hybrid", action="store_true",
                        help="ALSO run hybrid_search (MAKES A PAID OPENROUTER "
                             "EMBEDDINGS API CALL PER QUERY)")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    if not DB_PATH.exists():
        print("ERROR: indexes/lifeos.db not found")
        return 1

    # immutable=1 required: plain mode=ro can fail on this WAL-mode DB.
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
    cur = conn.cursor()

    print("=== retrieval smoke probe (FTS-only by default, READ-ONLY) ===")
    failures = 0
    for q in GOLDEN_QUERIES:
        rows = cur.execute(
            """
            SELECT title, path, bm25(search_index)
            FROM search_index
            WHERE content MATCH ?
            ORDER BY bm25(search_index)
            LIMIT ?
            """,
            (q, args.limit),
        ).fetchall()
        print(f"\nquery: {q!r} -> {len(rows)} results")
        if not rows:
            failures += 1
            print("    !! ZERO RESULTS — golden query regression")
            continue
        print(f"    {'bm25':>8}  {'title':<45} path")
        for title, path, score in rows:
            print(f"    {score:>8.3f}  {(title or '')[:45]:<45} {rel(path)}")
    conn.close()

    if args.hybrid:
        print("\n" + "!" * 70)
        print("!! --hybrid: making PAID OpenRouter embeddings API calls now !!")
        print("!! (uses repo DB connection code — not the ro/immutable path) !!")
        print("!" * 70)
        sys.path.insert(0, str(REPO_ROOT))
        from src.core.search_knowledge import hybrid_search
        for q in GOLDEN_QUERIES:
            results = hybrid_search(str(DB_PATH), query=q, limit=args.limit)
            print(f"\nhybrid query: {q!r} -> {len(results)} results")
            for r in results[:args.limit]:
                title = str(r.get("title", ""))[:45]
                path = rel(str(r.get("path", "")))
                score = r.get("score", r.get("similarity", ""))
                print(f"    {score}  {title:<45} {path}")

    if failures:
        print(f"\nFAIL: {failures} golden queries returned zero results")
        return 1
    print("\nOK: all golden queries returned results")
    return 0


if __name__ == "__main__":
    sys.exit(main())
