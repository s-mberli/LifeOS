#!/usr/bin/env python3
"""
scripts/update_docs.py — Automatic Documentation Updater

Triggered after implementing a Hermes proposal. Reads the proposal file
and recent git diff, then uses the LLM to:
  1. Append a new entry to CHANGELOG.md
  2. Update README.md if the feature changes core architecture
  3. Generate a Mermaid architecture diagram for the new feature

Usage:
    .venv/bin/python scripts/update_docs.py <proposal_file> [--no-readme]

    proposal_file: path to data/inbox/proposals/proposal_*.md
    --no-readme:   skip README update (for minor features)
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHANGELOG = BASE_DIR / "CHANGELOG.md"
README = BASE_DIR / "README.md"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.llm_client import call_llm

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_recent_diff(max_chars: int = 8000) -> str:
    """Return the diff of the last commit (or staged changes)."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--stat", "--unified=2"],
            capture_output=True, text=True, cwd=str(BASE_DIR),
            timeout=30,
        )
        diff = result.stdout
        if len(diff) > max_chars:
            diff = diff[:max_chars] + "\n\n[... diff truncated ...]"
        return diff
    except Exception:
        return "(could not retrieve git diff)"


def get_current_readme() -> str:
    if README.exists():
        content = README.read_text(encoding="utf-8")
        return content[:4000] + ("\n\n[... truncated ...]" if len(content) > 4000 else "")
    return ""


# ---------------------------------------------------------------------------
# LLM tasks
# ---------------------------------------------------------------------------

def generate_changelog_entry(proposal: str, diff: str, today: str) -> str:
    import re
    # Programmatically extract source URL from the proposal markdown
    source_url = "N/A"
    source_match = re.search(r"## Source\s*\n+([^\n]+)", proposal)
    if source_match:
        line = source_match.group(1).strip()
        # Find the first http/https URL in the line
        url_match = re.search(r"https?://[^\s\)]+", line)
        if url_match:
            source_url = url_match.group(0)

    prompt = f"""You are a technical writer maintaining a software changelog.

A new feature was just implemented in MarkusOS based on the following proposal:

## Proposal
{proposal}

## Git Diff Summary
{diff}

Write a concise changelog entry for CHANGELOG.md. Format:
```
## [{today}]
### Added
- **Feature Name:** 1-2 sentence description of what was added and why it matters.
  - **Source:** {source_url}
```

Only include sections that apply. Keep it under 100 words total. Be specific, not generic.
"""
    return call_llm(
        prompt=prompt,
        system_prompt="You are a precise technical writer. Output only the changelog markdown, no preamble.",
        max_tokens=500,
        temperature=0.3,
    ) or f"## [{today}]\n### Added\n- New feature implemented from Hermes proposal.\n"


def generate_readme_section(proposal: str, diff: str, current_readme: str) -> str | None:
    prompt = f"""You are a senior software engineer updating a README for an open-source project.

A new feature was implemented. Here is the proposal and diff:

## Proposal
{proposal}

## Git Diff Summary
{diff}

## Current README (truncated)
{current_readme}

Does this feature warrant updating the README? It should only be updated if:
- It changes the core architecture
- It changes how users set up or run the project
- It adds a new major subsystem

If NO update is needed, reply EXACTLY: `[NO README UPDATE NEEDED]`

If YES, output ONLY the new/modified README section(s) as markdown. Do not rewrite the entire README.
Include a Mermaid diagram if the feature adds a new data flow or subsystem.
"""
    return call_llm(
        prompt=prompt,
        system_prompt="You are a technical writer. Be concise. Only update what truly changed.",
        max_tokens=1500,
        temperature=0.3,
    )


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def prepend_to_changelog(entry: str) -> None:
    """Insert new entry at the top of CHANGELOG.md (after any title line)."""
    if CHANGELOG.exists():
        existing = CHANGELOG.read_text(encoding="utf-8")
    else:
        existing = "# Changelog\n\n"

    lines = existing.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 2
            break

    lines.insert(insert_at, entry.strip() + "\n")
    CHANGELOG.write_text("\n".join(lines), encoding="utf-8")
    print("✅ CHANGELOG.md updated.")


def append_to_readme(section: str) -> None:
    """Append a new section to the end of README.md."""
    existing = README.read_text(encoding="utf-8") if README.exists() else ""
    README.write_text(existing.rstrip() + "\n\n---\n\n" + section.strip() + "\n", encoding="utf-8")
    print("✅ README.md updated.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("Usage: .venv/bin/python scripts/update_docs.py <proposal_file> [--no-readme]")
        return 1

    proposal_path = (BASE_DIR / args[0]).resolve()
    update_readme = "--no-readme" not in args

    expected_dir = (BASE_DIR / "data" / "inbox" / "proposals").resolve()
    if not str(proposal_path).startswith(str(expected_dir)):
        print(f"Error: Path traversal detected. {proposal_path} must be inside {expected_dir}")
        return 1

    if not proposal_path.exists():
        print(f"Proposal not found: {proposal_path}")
        return 1

    proposal = proposal_path.read_text(encoding="utf-8")
    diff = get_recent_diff()
    today = date.today().isoformat()

    print(f"📄 Proposal: {proposal_path.name}")
    print(f"📅 Date: {today}")
    print()

    # 1. Changelog
    print("Generating CHANGELOG entry...")
    entry = generate_changelog_entry(proposal, diff, today)
    prepend_to_changelog(entry)

    # 2. README (optional)
    if update_readme:
        print("Checking if README needs updating...")
        readme_section = generate_readme_section(proposal, diff, get_current_readme())
        if readme_section and "[NO README UPDATE NEEDED]" not in readme_section:
            append_to_readme(readme_section)
        else:
            print("ℹ️  README update not required for this feature.")

    # 3. Update proposal status
    updated = proposal.replace("## Status\nProposed", "## Status\n✅ Implemented")
    if updated != proposal:
        proposal_path.write_text(updated, encoding="utf-8")
        print("✅ Proposal status updated to ✅ Implemented.")

    print()
    print("🎉 Documentation update complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
