#!/usr/bin/env python3
"""
Weekly Hermes Runner for MarkusOS
Queries automation_outbox for actionable notes, builds a consolidated prompt,
invokes the Hermes Agent to perform codebase reviews and generate PRs, and updates DB.
"""

import sys
import os
import sqlite3
import datetime
import subprocess
from pathlib import Path

def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("'\"")
                    os.environ[key] = val

load_env()

# Setup paths relative to script location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

# Ensure src/ is on the path so we can import triage_outbox
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.triage_outbox import triage_notes

def run_weekly_pipeline():
    print("--- Starting Weekly Hermes Pipeline ---")
    
    # 1. Run outbox triage first
    print("Running outbox triage...")
    triage_notes()
    
    if not DB_PATH.exists():
        print(f"Database does not exist at {DB_PATH}. Exiting.")
        return

    # 2. Query for actionable notes that Hermes has not yet processed
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, note_path, source_url FROM automation_outbox
        WHERE is_actionable = 1 AND processed_at IS NOT NULL AND hermes_run_at IS NULL
    """)
    rows = cursor.fetchall()
    
    if not rows:
        print("No new actionable notes to process. Weekly Hermes run skipped.")
        conn.close()
        return

    print(f"Found {len(rows)} new actionable note(s) for codebase review.")
    
    # 3. Read contents of actionable notes and aggregate them
    notes_text = ""
    for row_id, note_path, source_url in rows:
        full_path = BASE_DIR / note_path
        if full_path.exists() and full_path.is_file():
            try:
                content = full_path.read_text(encoding="utf-8")
                notes_text += f"### Note Path: {note_path}\n"
                notes_text += f"Source URL: {source_url or 'N/A'}\n\n"
                notes_text += f"{content}\n"
                notes_text += "\n" + "="*40 + "\n\n"
            except Exception as e:
                print(f"Error reading note {note_path}: {e}")
        else:
            print(f"Note file not found at {full_path}")
            
    if not notes_text.strip():
        print("Warning: Actionable notes list was empty or files could not be read. Exiting.")
        conn.close()
        return

    # 4. Construct prompt for Hermes
    prompt = f"""You are the MarkusOS Architecture Reviewer.
We have ingested some new guidelines, ideas, or architectural rules this week that may suggest improvements to our codebase:

{notes_text}

Your task:
1. Review the existing codebase at {BASE_DIR}/ using the search_vault MCP tool or reading files.
2. Identify if there are any violations, refactoring opportunities, or new features we should implement to align with these new guidelines (while respecting rules in AGENTS.md).
3. If you find clear, valuable codebase improvements:
   a. Create a new git branch (e.g., 'hermes-auto-improvement-...').
   b. Implement the changes cleanly in the codebase.
   c. Run the test suite (`.venv/bin/pytest`) to ensure no regressions are introduced.
   d. Open a Pull Request on Github (using the GITHUB_TOKEN configured in your environment) detailing the improvements and reference the notes.
4. If no code changes are necessary, output a summary of your analysis explaining why the codebase is already aligned.
"""

    # 5. Invoke Hermes
    # Paths configured via HERMES_BIN / HERMES_SCRIPT env vars (see .env.example)
    hermes_bin = os.environ.get("HERMES_BIN", "")
    hermes_script = os.environ.get("HERMES_SCRIPT", "")
    
    if not hermes_bin or not hermes_script:
        print("HERMES_BIN or HERMES_SCRIPT not set in environment. Set them in .env to enable the Hermes loop. Exiting.")
        conn.close()
        return

    if not os.path.exists(hermes_bin) or not os.path.exists(hermes_script):
        print(f"Hermes executable not found (HERMES_BIN={hermes_bin}). Exiting.")
        conn.close()
        return

    print("Invoking Hermes Agent in oneshot mode...")
    
    cmd = [hermes_bin, hermes_script, "--oneshot", prompt]
    
    # We execute Hermes and wait for completion.
    try:
        # We run in BASE_DIR (repository root) so Hermes resolves paths correctly
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, check=True)
        print("--- Hermes Execution Complete ---")
        print("Stdout:")
        print(result.stdout)
        print("Stderr:")
        print(result.stderr)
        
        # 6. Mark notes as successfully processed by Hermes
        now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
        row_ids = [r[0] for r in rows]
        
        cursor.execute(f"""
            UPDATE automation_outbox
            SET hermes_run_at = ?
            WHERE id IN ({",".join("?" for _ in row_ids)})
        """, [now_str] + row_ids)
        
        conn.commit()
        print(f"Successfully marked {len(row_ids)} outbox items as processed by Hermes.")
        
    except subprocess.CalledProcessError as err:
        print(f"Error: Hermes execution failed with exit code {err.returncode}")
        print("Stdout:")
        print(err.stdout)
        print("Stderr:")
        print(err.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during Hermes pipeline run: {e}")
        
    conn.close()
    print("--- Pipeline Run Completed ---")

if __name__ == "__main__":
    run_weekly_pipeline()
