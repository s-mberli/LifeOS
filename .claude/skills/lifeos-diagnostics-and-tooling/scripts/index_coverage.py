#!/usr/bin/env python
"""index_coverage.py — READ-ONLY comparison of files on disk vs search_index.

Mirrors DIRECTORIES_TO_INDEX from src/core/build_fts_index.py. For each
covered directory: .md files on disk vs DISTINCT indexed paths with that
prefix, coverage %, plus stale index entries (indexed path no longer on
disk) and the known gap: root-level knowledge/ files not in the index.
"""
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_PATH = REPO_ROOT / "indexes" / "lifeos.db"

# Keep in sync with DIRECTORIES_TO_INDEX in src/core/build_fts_index.py
INDEXED_DIRS = [
    "data/knowledge",
    "data/private",
    "data/inbox",
    "data/experts",
    "data/business",
    "data/career",
    "outputs",
]


def md_files(root: Path) -> set:
    """Repo-relative path strings, matching how search_index stores paths."""
    if not root.exists():
        return set()
    return {str(p.relative_to(REPO_ROOT)) for p in root.rglob("*.md") if p.is_file()}


def main() -> int:
    if not DB_PATH.exists():
        print("ERROR: indexes/lifeos.db not found")
        return 1
    # immutable=1 required: plain mode=ro can fail on this WAL-mode DB.
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
    cur = conn.cursor()
    indexed_paths = {r[0] for r in cur.execute("SELECT DISTINCT path FROM search_index")}
    conn.close()

    print("=== index coverage: disk vs search_index (READ-ONLY) ===")
    print(f"distinct indexed paths total: {len(indexed_paths)}")
    print(f"{'directory':<16} {'on disk':>8} {'indexed':>8} {'coverage':>9}")

    for rel in INDEXED_DIRS:
        disk = md_files(REPO_ROOT / rel)
        idx = {p for p in indexed_paths if p.startswith(rel + "/")}
        pct = f"{100 * len(idx & disk) / len(disk):.1f}%" if disk else "n/a"
        print(f"{rel:<16} {len(disk):>8} {len(idx):>8} {pct:>9}")

    stale = [p for p in indexed_paths if not (REPO_ROOT / p).exists()]
    print(f"\nstale index entries (file gone): {len(stale)}")
    for p in sorted(stale)[:5]:
        print(f"    {p}")

    # Known gap: auto_tldr writes to root-level knowledge/, which the
    # indexer does NOT cover.
    root_knowledge = md_files(REPO_ROOT / "knowledge")
    unindexed = [p for p in root_knowledge if p not in indexed_paths]
    # NOTE: auto_tldr writes to root knowledge/, which is not in the list above.
    print(f"\nroot-level knowledge/ .md files: {len(root_knowledge)}, "
          f"NOT in index: {len(unindexed)}  (known gap: indexer only covers data/*)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
