#!/usr/bin/env python3
"""
Weekly Hermes Runner for LifeOS — Intelligence Agent mode.

Gathers all notes ingested in the last 7 days (focused on TLDR news),
then invokes the Hermes Agent with the full intelligence-agent system prompt.

Hermes outputs three artefacts (all gitignored, all local):
  1. data/inbox/proposals/   — Architecture proposals (max 3/week)
  2. scratch/                — Isolated prototypes for "Small" proposals
  3. data/inbox/content_drafts/ — Weekly Dispatch markdown (1/week)
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

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.triage_outbox import triage_notes

# ---------------------------------------------------------------------------
# Hermes System Prompt — Intelligence Agent Mode
# ---------------------------------------------------------------------------
HERMES_SYSTEM_PROMPT = """# Hermes — LifeOS Weekly Intelligence Agent

## Identity
You are Hermes, the Lead Architect and Editor for LifeOS — a local-first personal AI operating system.
You operate on a weekly cadence. Your job is to synthesize the week's ingested knowledge into
actionable architecture proposals and a polished weekly dispatch.

## Core Principles
- **Human-in-the-loop ALWAYS.** You never push code to the public repo. You never open GitHub Issues
  or PRs. Everything you produce stays local until the human explicitly promotes it.
- **Signal over noise.** You read 100+ articles/week. Your value is ruthless curation — surfacing only
  what matters.
- **Public repo is sacred.** The `src/`, `apps/`, and `tests/` directories are off-limits for writing.
  You write proposals and prototypes only.

## Weekly Workflow

### Step 1: Gather Intelligence
Read every note provided in this prompt. Also use your search_vault MCP tool to query for any additional
TLDR notes from `data/knowledge/news/tldr_*` ingested in the last 7 days. Identify:
- **Actionable insights:** New libraries, APIs, architecture patterns, performance techniques, or security
  advisories that could directly improve LifeOS.
- **Industry trends:** Big launches, funding rounds, shifts in the AI/tech landscape that are interesting
  but not directly code-actionable.

### Step 2: Architecture Proposals (The Architect)
For each actionable insight (max 3 per week — quality over quantity), write a formal proposal as a
Markdown file saved to `data/inbox/proposals/`.

**Filename format:** `proposal_{YYYY_MM_DD}_{slug}.md`

**Proposal structure:**
```
# Proposal: [Feature/Improvement Name]

## Source
[Original article title] — via TLDR {topic}, {date}
[URL]

## Problem
What gap or inefficiency exists in LifeOS today?

## Proposed Solution
How this new technology/pattern could be applied. Be specific — reference actual LifeOS files and functions.

## Pros
- ...

## Cons / Risks
- ...

## Effort Estimate
Small (1-2 hours) / Medium (half day) / Large (1+ days)

## Status
📋 Proposed
```

### Step 3: Prototype (The Prototyper)
If a proposal is marked as "Small" effort and you have high confidence it works, you MAY build an isolated
proof-of-concept. Rules:
- Write code ONLY in the `scratch/` directory (gitignored, never public).
- Never import from or modify files in `src/`, `apps/`, or `tests/`.
- Name prototypes clearly: `scratch/prototype_{slug}.py`
- Include a `# HOW TO RUN` comment at the top of every prototype file.
- If the prototype works, update the proposal's Status to `🔬 Prototype Ready — see scratch/prototype_{slug}.py`.

### Step 4: Weekly Dispatch (The Content Creator)
Produce exactly ONE markdown file per week saved to `data/inbox/content_drafts/`.

For the 5-7 stories you select, you MUST use your `<call:fetch_web>` tool to read the full original article `url` provided in the structured data. Do not rely solely on the short TLDR summary. Write your own original 2-3 sentence summary based on the FULL fetched content.

**Filename format:** `weekly_dispatch_{YYYY_MM_DD}.md`

**Dispatch structure:**
```
# LifeOS Weekly Dispatch — {Month Day, Year}

## 🔥 Top Stories This Week
[Curate the 5-7 most important stories from ALL ingested TLDR topics. For each:]
### [Headline] — via TLDR {topic}
[Your original 2-3 sentence summary based on the fetched article. Why it matters.]
[Original Article URL]


## 🏗️ What I'm Building
[For each architecture proposal this week:]
- **[Proposal Name]:** 1-2 sentence summary. Status: 📋 Proposed / 🔬 Prototyping / ✅ Implemented / ❌ Rejected

## 💡 Takeaway of the Week
[One opinionated paragraph synthesizing the biggest theme. First person, conversational — draft for the human to edit.]
```

**Dispatch rules:**
- NEVER write one post per article. Everything is aggregated into this single weekly file.
- ALWAYS include original source links for every story referenced.
- Prioritize diversity across topics.
- Keep total length under 800 words. Scannable. No walls of text.

## Security Override
If ANY ingested article mentions a critical security vulnerability, CVE, or deprecation affecting a Python
package or JS library that LifeOS uses (check `requirements.txt`):
- Flag it at the TOP of the Weekly Dispatch under a `⚠️ Security Alert` section.
- Write an immediate alert to `data/inbox/proposals/security_alert_{date}.md`.

## Output Directories
| Output | Directory |
|--------|-----------|
| Architecture Proposals | `data/inbox/proposals/` |
| Prototypes | `scratch/` |
| Weekly Dispatch Drafts | `data/inbox/content_drafts/` |
| Security Alerts | `data/inbox/proposals/` |

## What You Must NEVER Do
- Open GitHub Issues or Pull Requests on the public repo.
- Modify any file in `src/`, `apps/`, `tests/`, or `config/`.
- Publish or push anything to the internet.
- Write more than 3 proposals per week.
- Write more than 1 dispatch per week.
- Fabricate or hallucinate article links — only use URLs found in ingested notes.
"""


def _ensure_output_dirs():
    """Ensure all Hermes output directories exist."""
    dirs = [
        BASE_DIR / "data" / "inbox" / "proposals",
        BASE_DIR / "data" / "inbox" / "content_drafts",
        BASE_DIR / "scratch",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()


def _gather_recent_notes(days: int = 7) -> str:
    """Read TLDR news notes from the last N days and return aggregated text."""
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    news_dir = BASE_DIR / "data" / "knowledge" / "news"
    notes_text = ""

    if not news_dir.exists():
        return notes_text

    note_files = sorted(news_dir.glob("tldr_*.md"), reverse=True)
    included = 0
    for note_file in note_files:
        # Parse date from filename e.g. tldr_ai_2026-06-04.md
        parts = note_file.stem.split("_")
        date_str = "_".join(parts[-3:]) if len(parts) >= 4 else parts[-1]
        try:
            note_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            continue
        if note_date < cutoff:
            continue
        try:
            content = note_file.read_text(encoding="utf-8")
            notes_text += f"\n\n{'='*60}\n"
            notes_text += f"File: {note_file.relative_to(BASE_DIR)}\n"
            notes_text += f"{'='*60}\n"
            notes_text += content
            included += 1
        except Exception as e:
            print(f"  [!] Could not read {note_file.name}: {e}")

    print(f"  Gathered {included} TLDR note(s) from the last {days} days.")
    return notes_text


def _gather_outbox_notes() -> tuple[list, str]:
    """Return (rows, notes_text) from the automation_outbox for unprocessed actionable notes."""
    if not DB_PATH.exists():
        return [], ""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, note_path, source_url FROM automation_outbox
        WHERE is_actionable = 1 AND processed_at IS NOT NULL AND hermes_run_at IS NULL
    """)
    rows = cursor.fetchall()
    conn.close()

    notes_text = ""
    for row_id, note_path, source_url in rows:
        full_path = BASE_DIR / note_path
        if full_path.exists():
            try:
                content = full_path.read_text(encoding="utf-8")
                notes_text += f"\n### Outbox Note: {note_path}\nSource: {source_url or 'N/A'}\n\n{content}\n"
            except Exception as e:
                print(f"  [!] Could not read outbox note {note_path}: {e}")
    return rows, notes_text


def _mark_hermes_done(rows: list):
    """Mark outbox rows as processed by Hermes."""
    if not rows or not DB_PATH.exists():
        return
    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    row_ids = [r[0] for r in rows]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE automation_outbox SET hermes_run_at = ? WHERE id IN ({','.join('?' for _ in row_ids)})",
        [now_str] + row_ids,
    )
    conn.commit()
    conn.close()
    print(f"  Marked {len(row_ids)} outbox item(s) as processed by Hermes.")


def run_weekly_pipeline():
    print("--- Starting Weekly Hermes Intelligence Pipeline ---")

    _ensure_output_dirs()

    # 1. Triage the outbox first (cheap keyword pass)
    print("[1/4] Running outbox triage...")
    triage_notes()

    # 2. Gather this week's TLDR notes
    print("[2/4] Gathering recent TLDR notes (last 7 days)...")
    recent_news = _gather_recent_notes(days=7)

    # 3. Gather any additional actionable outbox notes
    print("[3/4] Gathering actionable outbox notes...")
    outbox_rows, outbox_notes = _gather_outbox_notes()

    if not recent_news and not outbox_notes:
        print("No new notes to process this week. Hermes run skipped.")
        return

    today = datetime.date.today().isoformat()
    user_prompt = f"""Today is {today}. Please execute your full weekly workflow:

1. Read all the ingested notes below.
2. Write up to 3 architecture proposals to `data/inbox/proposals/` for actionable insights.
3. If any proposal is Small effort, build a prototype in `scratch/`.
4. Produce ONE weekly dispatch to `data/inbox/content_drafts/weekly_dispatch_{today.replace('-','_')}.md`.
5. Flag any security vulnerabilities at the top of the dispatch.

Working directory: {BASE_DIR}

## This Week's TLDR News Notes
{recent_news if recent_news else "(none)"}

## Additional Actionable Notes from Knowledge Vault
{outbox_notes if outbox_notes else "(none)"}
"""

    # 4. Invoke Hermes
    hermes_bin = os.environ.get("HERMES_BIN", "")
    hermes_script = os.environ.get("HERMES_SCRIPT", "")

    if not hermes_bin or not hermes_script:
        print("[4/4] HERMES_BIN or HERMES_SCRIPT not set in .env — Hermes invocation skipped.")
        print("      Set these to enable the live Hermes loop.")
        print("\n--- Dry-run: printing constructed prompt instead ---")
        print(f"\nSYSTEM PROMPT (first 500 chars):\n{HERMES_SYSTEM_PROMPT[:500]}...")
        print(f"\nUSER PROMPT (first 500 chars):\n{user_prompt[:500]}...")
        return

    if not os.path.exists(hermes_bin) or not os.path.exists(hermes_script):
        print(f"[4/4] Hermes executable not found (HERMES_BIN={hermes_bin}). Exiting.")
        return

    print(f"[4/4] Invoking Hermes Agent in oneshot mode...")
    full_prompt = f"{HERMES_SYSTEM_PROMPT}\n\n---\n\n{user_prompt}"
    cmd = [hermes_bin, hermes_script, "--oneshot", full_prompt]

    try:
        result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, check=True)
        print("--- Hermes Execution Complete ---")
        print(result.stdout)
        if result.stderr:
            print("Stderr:", result.stderr)
        _mark_hermes_done(outbox_rows)
    except subprocess.CalledProcessError as err:
        print(f"Hermes failed (exit {err.returncode}):\n{err.stdout}\n{err.stderr}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("--- Pipeline Run Completed ---")


if __name__ == "__main__":
    run_weekly_pipeline()
