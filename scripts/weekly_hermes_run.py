#!/usr/bin/env python3
"""
Weekly Hermes Runner for LifeOS
Synthesizes TLDR newsletters using execute_agent_search_loop.
Generates Architecture Proposals and a Weekly Dispatch blog post.

Two-phase approach to stay within LLM token limits:
  Phase 1: Feed article metadata only → LLM picks top 5-7 stories.
  Phase 2: Fetch full text of selected URLs → LLM writes dispatch.
"""

import sys
import os
import re
import sqlite3
import datetime
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
from src.core.llm_client import call_llm
from src.core.web import fetch_webpage_content


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def collect_articles_from_notes(days: int = 7) -> list[dict]:
    """Scan TLDR notes from last N days and extract article metadata."""
    news_dir = BASE_DIR / "data" / "knowledge" / "news"
    if not news_dir.exists():
        return []

    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days)
    articles = []

    for f in sorted(news_dir.glob("tldr_*.md")):
        mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            continue

        content = f.read_text(encoding="utf-8")
        source_match = re.search(r"Source:\s*(https?://\S+)", content)
        source_url = source_match.group(1) if source_match else f.name

        # Try NEW structured format first (## Articles with ### blocks)
        structured = re.findall(
            r"### (.+?)\n- \*\*URL:\*\* (.+?)\n.*?- \*\*Read time:\*\* (.+?)\n- \*\*TLDR Summary:\*\* (.+?)(?=\n###|\n## |$)",
            content, re.DOTALL
        )
        if structured:
            for title, url, read_time, summary in structured:
                articles.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "read_time": read_time.strip(),
                    "summary": summary.strip()[:300],
                    "source": source_url,
                })
        else:
            # OLD format: extract what we can from flat text
            # Try to find linked article references with markdown links
            links = re.findall(r"\[([^\]]+)\]\((https?://[^\)]+)\)", content)
            for text, url in links:
                # Skip TLDR internal links and sponsor links
                if "tldr.tech" in url or "sponsor" in text.lower():
                    continue
                articles.append({
                    "title": text.strip()[:120],
                    "url": url.strip(),
                    "read_time": "Unknown",
                    "summary": "",
                    "source": source_url,
                })

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)

    return unique


def build_candidates_prompt(articles: list[dict]) -> str:
    """Build a compact article list for LLM selection."""
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. **{a['title']}**")
        lines.append(f"   Source: {a['source']}")
        lines.append(f"   URL: {a['url']}")
        if a["summary"]:
            lines.append(f"   Summary: {a['summary'][:200]}")
        if a["read_time"] != "Unknown":
            lines.append(f"   Read time: {a['read_time']}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def run_weekly_pipeline():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print("--- Starting Weekly Hermes Pipeline ---")

    # 1. Run outbox triage
    print("Running outbox triage...")
    triage_notes()

    # 2. Collect article candidates
    print("Collecting articles from last 7 days...")
    articles = collect_articles_from_notes(days=7)
    print(f"Found {len(articles)} unique article candidates.")

    if not articles:
        print("No articles found. Exiting.")
        return

    # 3. Phase 1: LLM selects top 5-7 stories
    candidates_text = build_candidates_prompt(articles)
    # Cap candidates to ~60k chars (~15k tokens) to stay safe
    if len(candidates_text) > 60000:
        candidates_text = candidates_text[:60000] + "\n\n[... truncated ...]"

    selection_prompt = f"""You are Hermes, a senior tech intelligence analyst.

Below is a list of {len(articles)} articles from this week's tech newsletters.

Pick the 5-7 most important, high-signal stories that a senior software engineer and CTO would care about. 

CRITICAL DIVERSITY RULE: You MUST select stories from at least 4 different newsletter sources/topics (look at the Source URL). Do not let AI and Tech dominate the entire list. Pick from InfoSec, Web Dev, Founders, Design, Data, etc.

Prioritize:
- Breakthrough research or paradigm shifts
- Security advisories or CVEs
- Major product launches or API changes
- Architectural patterns or best practices

Respond with ONLY a JSON array of the selected article numbers (1-indexed). Example: [3, 7, 12, 15, 22]

Articles:
{candidates_text}"""

    print("Phase 1: Asking LLM to select top stories...")
    selection_response = call_llm(
        prompt=selection_prompt,
        system_prompt="You are a tech analyst. Respond with only a JSON array of numbers.",
        max_tokens=200,
        temperature=0.2,
    )

    import random
    if not selection_response:
        print("LLM selection failed. Falling back to 5 random articles.")
        selected_articles = random.sample(articles, min(5, len(articles)))
    else:
        print(f"LLM response: {selection_response}")
        try:
            # Parse JSON array from response
            nums_match = re.search(r"\[[\d,\s]+\]", selection_response)
            if nums_match:
                indices = [int(x) for x in re.findall(r"\d+", nums_match.group())]
                selected_articles = [articles[i - 1] for i in indices if 0 < i <= len(articles)]
            else:
                selected_articles = random.sample(articles, min(5, len(articles)))
        except Exception:
            selected_articles = random.sample(articles, min(5, len(articles)))

    print(f"Selected {len(selected_articles)} articles for deep fetch.")

    # 4. Phase 2: Fetch full text of selected articles
    enriched = []
    for art in selected_articles:
        print(f"  Fetching: {art['title'][:60]}...")
        try:
            title, full_text = fetch_webpage_content(art["url"])
            # Cap to 1000 chars per article to fit inside gpt-5-nano's tiny context window
            if full_text and len(full_text) > 1000:
                full_text = full_text[:1000] + "\n\n[... truncated ...]"
            art["full_text"] = full_text or art.get("summary", "")
            enriched.append(art)
        except Exception as exc:
            print(f"    Failed: {exc}")
            art["full_text"] = art.get("summary", "No content available.")
            enriched.append(art)

    # 5. Phase 2: LLM writes Proposals
    articles_block = ""
    for i, art in enumerate(enriched, 1):
        articles_block += f"\n--- Article {i} ---\n"
        articles_block += f"Title: {art['title']}\n"
        articles_block += f"Source: {art['source']}\n"
        articles_block += f"URL: {art['url']}\n"
        articles_block += f"Full Text:\n{art['full_text']}\n"

    proposal_prompt = f"""You are Hermes, the LifeOS Intelligence Agent and private CTO.
Review the following {len(enriched)} articles.
Write up to 3 short Architecture Proposals for LifeOS improvements based on insights from these articles.

You MUST respond with a valid JSON array of objects. Do NOT wrap the JSON in markdown code blocks, just raw JSON.
If no articles provide actionable architecture insights, return an empty array: []

Each object in the array must have two keys:
1. "filename": A short, snake_case filename for the proposal (e.g., "proposal_agent_judge.md").
2. "content": The full Markdown content of the proposal.

The Markdown content MUST strictly follow this exact template:

# [Proposal Title]

## Problem
[Description of the problem based on the article]

## Proposed Solution
[How LifeOS can implement this]

## Source
[URL from the article]

## Status
Proposed

## Effort
[Small/Medium/Large]

Articles:
{articles_block}"""

    print("Phase 2a: Generating architecture proposals...")
    from src.core.llm_client import parse_json_safely
    proposals_raw = call_llm(
        prompt=proposal_prompt,
        system_prompt="You are Hermes, a brilliant CTO. Respond ONLY with valid JSON.",
        max_tokens=3000,
        temperature=0.2,
    )
    
    proposals_list = []
    if proposals_raw:
        proposals_list = parse_json_safely(proposals_raw)
        if not isinstance(proposals_list, list):
            proposals_list = []

    # 6. Phase 2: LLM writes the Dispatch
    dispatch_prompt = f"""You are Hermes, the LifeOS Intelligence Agent and private CTO.
Write a Weekly Dispatch blog post for the week of {today}.

You have the full text of {len(enriched)} carefully selected articles below.
For each article, write your OWN original 2-3 sentence summary based on the full content (NOT the TLDR blurb).

CRITICAL INSTRUCTIONS:
1. Top Stories: Curate the 5-7 most important stories. You MUST pull from at least 4 different topics (e.g., AI, Web Dev, InfoSec, Founders, Design). Do not let AI and Tech dominate the entire list.
2. Simplicity: When writing the Architecture Case Studies, explain the process simply and accessibly, as if teaching a junior developer. Make it easy to understand how one could apply it.
3. LifeOS Context: Do not hallucinate fake agents (like "Planner Agent"). LifeOS currently only has "Hermes" (analyst) and "Prototyper" (coder). Keep your design explorations grounded.

Structure your output EXACTLY matching this Markdown template:

# LifeOS Weekly Dispatch — {today}

> *Sample dispatch generated for format review — this is what Hermes will produce automatically each Sunday.*

---

## 🔥 Top Stories This Week
*Curated from the excellent daily [TLDR Newsletters](https://tldr.tech/).*

- **[[Article Title]](Original Article URL)**
  [Your original 2-3 sentence summary. Why it matters.]

[Repeat for each article]

---

## 🏗️ Architecture Case Studies

[For exactly 2 actionable insights this week, write a technical case study. Make the theory universal, but use LifeOS as the practical implementation example.]

### [Concept/Pattern Name]
*Inspired by: [[Article Name]](Original Article URL)*

#### The Core Concept
[2-3 paragraphs of accessible, easy-to-understand technical prose explaining the mechanism thoroughly. Make the theory universal so any developer can learn from it.]

#### Architecture Diagram
```mermaid
[Mermaid block diagram illustrating the flow or architecture of this concept. Keep it simple and clean. IMPORTANT: Do not use parentheses `()` or special characters inside node labels unless you wrap the label in double quotes (e.g., `A["Node Label (extra)"]`).]
```

#### LifeOS Application
[1-2 paragraphs of clear prose explaining how this applies to LifeOS. This is a design exploration, serving as a blueprint for how one might implement this pattern in a real-world system without hallucinating fake agents.]

#### Trade-offs
[Brief paragraph discussing pros and cons]

[Repeat for exactly 2 case studies]

---

## 💡 Takeaway of the Week
[One opinionated paragraph synthesizing the biggest theme across all the week's news. Written in first person, conversational tone.]

---

*Generated by Hermes — LifeOS Weekly Intelligence Agent*
*Review, edit, and publish at your discretion. Nothing here goes public automatically.*

Here are the articles:
{articles_block}"""

    print("Phase 2b: Generating dispatch...")
    dispatch = call_llm(
        prompt=dispatch_prompt,
        system_prompt="You are Hermes, a brilliant CTO writing a weekly newsletter. Do not include literal instructions in your output.",
        max_tokens=4000,
        temperature=0.4,
    )

    if not proposals_list:
        print("WARNING: LLM failed to generate proposals (or returned empty list). Skipping proposals.")

    if not dispatch:
        print("WARNING: LLM failed to generate dispatch (possible content filter). Using placeholder.")
        dispatch = "_No dispatch generated this week due to content filters or API errors._"

    # 7. Save outputs separately
    out_dir = BASE_DIR / "data" / "inbox" / "content_drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"weekly_dispatch_{today}.md"
    out_file.write_text(dispatch, encoding="utf-8")
    print(f"✓ Weekly dispatch saved: {out_file.relative_to(BASE_DIR)}")

    prop_dir = BASE_DIR / "data" / "inbox" / "proposals"
    prop_dir.mkdir(parents=True, exist_ok=True)
    if proposals_list:
        for prop in proposals_list:
            filename = prop.get("filename", f"proposal_{today}.md")
            if not filename.endswith(".md"): 
                filename += ".md"
            prop_file = prop_dir / filename
            prop_file.write_text(prop.get("content", ""), encoding="utf-8")
            print(f"✓ Proposal saved: {prop_file.relative_to(BASE_DIR)}")

    # 7. Update outbox DB
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM automation_outbox
            WHERE is_actionable = 1 AND processed_at IS NOT NULL AND hermes_run_at IS NULL
        """)
        row_ids = [r[0] for r in cursor.fetchall()]
        if row_ids:
            now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
            cursor.execute(
                f"UPDATE automation_outbox SET hermes_run_at = ? WHERE id IN ({','.join('?' for _ in row_ids)})",
                [now_str] + row_ids,
            )
            conn.commit()
            print(f"✓ Marked {len(row_ids)} outbox items as processed.")
        conn.close()

    print("--- Pipeline Complete ---")


if __name__ == "__main__":
    run_weekly_pipeline()
