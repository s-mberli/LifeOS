#!/usr/bin/env python3
"""
Triage Worker for MarkusOS Ingest Outbox
Scores unprocessed notes in automation_outbox cheaply without using an LLM.
"""

import os
import re
import sqlite3
import datetime
from pathlib import Path

# Setup paths relative to script location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

KEYWORDS = ["AI", "Architecture", "Github", "Python", "SQLite", "Performance", "Agent", "LLM"]

def triage_notes():
    if not DB_PATH.exists():
        print(f"Database does not exist at {DB_PATH}. Exiting.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get unprocessed items
    cursor.execute("""
        SELECT id, note_path, source_url, word_count FROM automation_outbox
        WHERE processed_at IS NULL
    """)
    rows = cursor.fetchall()
    
    if not rows:
        print("No pending notes to triage.")
        conn.close()
        return

    print(f"Found {len(rows)} pending note(s) to triage.")
    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

    for row_id, note_path, source_url, word_count in rows:
        full_path = BASE_DIR / note_path
        score = 0
        is_actionable = 0
        matching_keywords = []

        if full_path.exists() and full_path.is_file():
            try:
                content = full_path.read_text(encoding="utf-8")
                content_lower = content.lower()
                
                # Check for keywords
                for kw in KEYWORDS:
                    # Match word boundaries or substring depending on needs, word boundaries \b is safer
                    pattern = r'\b' + re.escape(kw.lower()) + r'\b'
                    if re.search(pattern, content_lower):
                        matching_keywords.append(kw)
                
                # Scoring: 1 point per matching keyword, plus 1 point if word count is substantial (>150 words)
                score = len(matching_keywords)
                if word_count and word_count > 150:
                    score += 1
                
                # Determine actionable: must have at least one code/architecture keyword match
                if len(matching_keywords) >= 1:
                    is_actionable = 1
                    
                print(f"Triaged '{note_path}': score={score}, is_actionable={is_actionable}, keywords={matching_keywords}")
            except Exception as e:
                print(f"Error reading note file {full_path}: {e}")
        else:
            print(f"Note file not found: {full_path}")
            # If the file doesn't exist, we skip scoring but mark processed to avoid hanging
            score = 0
            is_actionable = 0

        # Update row
        cursor.execute("""
            UPDATE automation_outbox
            SET processed_at = ?, score = ?, is_actionable = ?
            WHERE id = ?
        """, (now_str, score, is_actionable, row_id))

    conn.commit()
    conn.close()
    print("Triage run completed.")

if __name__ == "__main__":
    triage_notes()
