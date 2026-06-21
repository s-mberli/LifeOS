#!/usr/bin/env python3
"""
scripts/sync_outbox.py — Sync filesystem notes with SQLite automation_outbox

Scans `data/knowledge/` (specifically podcast transcripts) and registers any
unregistered notes into the local `automation_outbox` table. This ensures notes
synced from a VPS or other machine are correctly registered on the local Mac.
Normalizes all Unicode paths to NFC to avoid OS-specific encoding mismatches.
"""

from __future__ import annotations

import datetime
import sys
import unicodedata
from pathlib import Path

# Setup paths relative to script location
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.db import get_db_connection, DB_PATH
from src.core.frontmatter import read_fm

def sync_outbox():
    if not DB_PATH.exists():
        print(f"Database does not exist at {DB_PATH}. Exiting.")
        return

    conn = get_db_connection(DB_PATH)
    cursor = conn.cursor()

    # Get all registered note paths, normalized to NFC
    cursor.execute("SELECT note_path FROM automation_outbox")
    registered_paths = {
        unicodedata.normalize("NFC", row[0]) 
        for row in cursor.fetchall() if row[0]
    }

    podcast_dir = ROOT / "knowledge" / "lenny-podcast"
    if not podcast_dir.exists():
        print(f"Podcast directory {podcast_dir} does not exist. Skipping.")
        conn.close()
        return

    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    added_count = 0

    print("Scanning synced transcripts to verify outbox registry...")
    for fpath in podcast_dir.glob("*.md"):
        # Normalize relative path to NFC
        rel_path = str(fpath.relative_to(ROOT))
        rel_path_nfc = unicodedata.normalize("NFC", rel_path)
        
        if rel_path_nfc in registered_paths:
            continue

        try:
            fm, body = read_fm(fpath)
            source_url = fm.get("source_url", "")
            word_count = len(body.split())

            # Register missing outbox entry
            cursor.execute("""
                INSERT INTO automation_outbox (note_path, source_url, word_count, added_at)
                VALUES (?, ?, ?, ?)
            """, (rel_path_nfc, source_url, word_count, now_str))
            
            print(f"Registered synced note: {rel_path_nfc}")
            added_count += 1
        except Exception as e:
            print(f"Failed to read/register {fpath.name}: {e}")

    if added_count > 0:
        conn.commit()
        print(f"Successfully registered {added_count} synced note(s) into the outbox.")
    else:
        print("All synced transcripts are already registered.")

    conn.close()

if __name__ == "__main__":
    sync_outbox()
