#!/usr/bin/env python
"""db_stats.py — READ-ONLY row counts and health stats for indexes/lifeos.db.

Opens the DB via a mode=ro URI. Never uses src.core.db.get_db_connection
(that function runs init_db, which writes, and can even DELETE a DB it
considers corrupted). Safe to run at any time.
"""
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_PATH = REPO_ROOT / "indexes" / "lifeos.db"

TEST_POLLUTION_NAMES = {
    "persistently_failing",
    "flaky_json_parser",
    "flacky_json_parser",  # historical typo variant, also a test fixture
}


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: DB not found at indexes/lifeos.db (resolved root: OK={REPO_ROOT.name})")
        return 1

    # immutable=1 is required: on this WAL-mode DB a plain mode=ro URI can
    # fail with "unable to open database file" (SQLite needs -wal/-shm access).
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
    cur = conn.cursor()

    def count(sql, params=()):
        return cur.execute(sql, params).fetchone()[0]

    print("=== lifeos.db stats (READ-ONLY) ===")
    size_mb = DB_PATH.stat().st_size / (1024 * 1024)
    print(f"DB file size:            {size_mb:,.1f} MB")

    print(f"search_index rows:       {count('SELECT count(*) FROM search_index'):,}")
    print(f"doc_chunks rows:         {count('SELECT count(*) FROM doc_chunks'):,}")

    # vec_docs needs the sqlite_vec extension loaded even for counting
    try:
        import sqlite_vec
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        print(f"vec_docs rows:           {count('SELECT count(*) FROM vec_docs'):,}")
    except Exception as e:  # noqa: BLE001 - diagnostic tool, report and continue
        print(f"vec_docs rows:           UNAVAILABLE (vec0 not loadable: {e})")

    total = count("SELECT count(*) FROM automation_outbox")
    unproc = count("SELECT count(*) FROM automation_outbox WHERE processed_at IS NULL")
    unstamped = count(
        "SELECT count(*) FROM automation_outbox WHERE is_actionable=1 AND hermes_run_at IS NULL"
    )
    print(f"automation_outbox:       {total} total, {unproc} unprocessed, "
          f"{unstamped} actionable-unstamped")

    print(f"ai_code_provenance rows: {count('SELECT count(*) FROM ai_code_provenance')}")
    print(f"user_memory rows:        {count('SELECT count(*) FROM user_memory')}")

    arl_total = count("SELECT count(*) FROM agent_repair_logs")
    print(f"agent_repair_logs rows:  {arl_total}")
    pollution = 0
    for fn, et, n in cur.execute(
        "SELECT function_name, error_type, count(*) FROM agent_repair_logs "
        "GROUP BY 1, 2 ORDER BY 3 DESC"
    ):
        flag = ""
        if fn in TEST_POLLUTION_NAMES:
            flag = "  <-- TEST POLLUTION"
            pollution += n
        print(f"    {fn:28s} {et:20s} {n:5d}{flag}")
    print(f"  test-pollution rows:   {pollution} of {arl_total}")

    # Stray database files from earlier layouts
    print("stray DBs:")
    for rel in ("indexes/markusos.db", "src/indexes/lifeos.db"):
        p = REPO_ROOT / rel
        if p.exists():
            print(f"    PRESENT: {rel} ({p.stat().st_size / 1024:,.0f} KB)")
        else:
            print(f"    absent:  {rel}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
