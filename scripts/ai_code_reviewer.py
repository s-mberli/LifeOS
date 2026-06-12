#!/usr/bin/env python3
"""
scripts/ai_code_reviewer.py — AI Code Reviewer and Auto-Fixer

Set SKIP_AI_REVIEW=1 in env to bypass (emergency use only).

Performs a Five-Axis Code Review (Correctness, Readability, Architecture,
Security, Performance) on Python files. Auto-fixes issues when possible.
Logs results to the ai_code_provenance table in indexes/lifeos.db.

Usage:
    .venv/bin/python scripts/ai_code_reviewer.py <author> <file1.py> [file2.py ...]

    author: "Human" | "Hermes" | "Prototyper" | agent name
"""

from __future__ import annotations

import datetime
import sqlite3
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_FILE_SIZE = 50_000  # chars — skip files larger than this to avoid token bombs
REVIEW_MAX_TOKENS = 4000
REVIEW_TIMEOUT_SECS = 60  # abort if LLM takes longer

REVIEW_SYSTEM_PROMPT = "You are a world-class Python code reviewer and auto-fixer."

REVIEW_USER_PROMPT = """\
You are an elite Senior Staff Software Engineer and Security Auditor.
Perform a strict Five-Axis Code Review on the following Python file.

## Five Axes
1. **Correctness** — bugs, edge cases, off-by-one, error handling
2. **Readability** — naming, structure, dead code, unnecessary complexity
3. **Architecture** — module boundaries, dependency direction, duplication
4. **Security** — hardcoded secrets, injection, unsanitised input, auth gaps. **CRITICAL: NEVER allow clear-text logging/printing of `os.environ` or API keys.**
5. **Performance** — N+1 queries, unbounded loops, large allocations in hot paths

## Rules
- If the code passes all five axes, reply EXACTLY with: `[PASSED]`
- If issues exist:
  1. Output a brief `## Issues` section listing each problem (axis + description).
  2. Output the FULLY REWRITTEN, corrected file inside a single ```python block.
     Do NOT omit any part of the file. Return the entire corrected content.

## File: {file_path}
```python
{content}
```
"""

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def _ensure_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_code_provenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            author_agent TEXT,
            model TEXT,
            created_at TEXT,
            review_status TEXT
        )
    """)


def log_provenance(
    file_path: str,
    author_agent: str,
    review_status: str,
    *,
    db_path: Path = DB_PATH,
) -> None:
    """Upsert a provenance record for *file_path*."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        _ensure_table(cursor)
        cursor.execute(
            "SELECT id FROM ai_code_provenance WHERE file_path = ?",
            (file_path,),
        )
        row = cursor.fetchone()
        if row:
            cursor.execute(
                "UPDATE ai_code_provenance "
                "SET author_agent = ?, review_status = ?, created_at = ? "
                "WHERE id = ?",
                (author_agent, review_status, now, row[0]),
            )
        else:
            cursor.execute(
                "INSERT INTO ai_code_provenance "
                "(file_path, author_agent, model, created_at, review_status) "
                "VALUES (?, ?, ?, ?, ?)",
                (file_path, author_agent, "auto", now, review_status),
            )
        conn.commit()


# ---------------------------------------------------------------------------
# Review logic
# ---------------------------------------------------------------------------

def _extract_code_block(response: str) -> str | None:
    """Pull the first ```python ... ``` block from LLM response."""
    marker = "```python"
    idx = response.find(marker)
    if idx == -1:
        return None
    start = idx + len(marker)
    end = response.find("```", start)
    if end == -1:
        return None
    return response[start:end].strip()


def review_and_fix_file(
    file_path: Path,
    author: str = "Unknown",
    *,
    dry_run: bool = False,
    db_path: Path = DB_PATH,
) -> bool:
    """Review a single Python file. Returns True if passed (or auto-fixed)."""
    from src.core.llm_client import call_llm  # lazy import — keeps module testable

    if not file_path.exists():
        print(f"  File not found: {file_path}")
        return False

    rel = file_path.relative_to(BASE_DIR) if file_path.is_relative_to(BASE_DIR) else file_path
    content = file_path.read_text(encoding="utf-8")

    if len(content) > MAX_FILE_SIZE:
        print(f"  ⏭️  {rel} — skipped (>{MAX_FILE_SIZE} chars)")
        return True  # don't block commit for huge files

    print(f"  🔍 Reviewing {rel} ...")

    prompt = REVIEW_USER_PROMPT.format(file_path=rel, content=content)

    import os
    if os.environ.get("SKIP_AI_REVIEW") == "1":
        print(f"  ⏭️  {rel} — review skipped (SKIP_AI_REVIEW=1)")
        return True

    import signal

    def _timeout_handler(signum, frame):
        raise TimeoutError("LLM call exceeded timeout")

    try:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(REVIEW_TIMEOUT_SECS)
        response = call_llm(
            prompt=prompt,
            system_prompt=REVIEW_SYSTEM_PROMPT,
            max_tokens=REVIEW_MAX_TOKENS,
            temperature=0.2,
        )
        signal.alarm(0)  # cancel alarm
    except TimeoutError:
        print(f"  ⏰ {rel} — LLM timed out after {REVIEW_TIMEOUT_SECS}s, skipping")
        return True  # don't block commit on timeout
    except Exception as exc:
        print(f"  ❌ LLM call failed: {exc}")
        return True  # don't block commit on LLM errors

    if not response:
        print("  ❌ LLM returned empty response.")
        return False

    # --- Passed ---------------------------------------------------------
    if "[PASSED]" in response:
        print(f"  ✅ {rel} — passed Five-Axis Review")
        log_provenance(str(rel), author, "Passed", db_path=db_path)
        return True

    # --- Auto-fix -------------------------------------------------------
    fixed_code = _extract_code_block(response)
    if fixed_code:
        if dry_run:
            print(f"  🛠️  {rel} — issues found (dry-run, not overwriting)")
            log_provenance(str(rel), author, "Flagged (Dry-Run)", db_path=db_path)
            return False

        # Write backup
        backup = file_path.with_suffix(".py.bak")
        backup.write_text(content, encoding="utf-8")

        file_path.write_text(fixed_code + "\n", encoding="utf-8")
        print(f"  🛠️  {rel} — auto-fixed (backup: {backup.name})")
        log_provenance(str(rel), author, "Passed (Auto-Fixed)", db_path=db_path)
        return True

    # --- Could not parse fix --------------------------------------------
    print(f"  ⚠️  {rel} — issues found but couldn't parse auto-fix")
    log_provenance(str(rel), author, "Flagged (Manual Fix Required)", db_path=db_path)
    return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: .venv/bin/python scripts/ai_code_reviewer.py <author> <file1.py> [file2.py ...]")
        return 1

    author = sys.argv[1]
    files = sys.argv[2:]
    dry_run = "--dry-run" in sys.argv
    files = [f for f in files if f != "--dry-run"]

    all_passed = True
    for f in files:
        path = Path(f)
        if not path.is_absolute():
            path = BASE_DIR / f
        if path.exists() and path.suffix == ".py":
            if not review_and_fix_file(path, author, dry_run=dry_run):
                all_passed = False

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
