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

import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHANGELOG = BASE_DIR / "CHANGELOG.md"
README = BASE_DIR / "README.md"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.llm_client import call_llm

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GIT_TIMEOUT_SECONDS = 30
MAX_PROMPT_CHARS = 12000
CHANGELOGOG_MAX_CHARS = 8000
README_MAX_CHARS = 4000

# Pattern to match various proposal status formats
STATUS_PATTERN = re.compile(
    r"(##\s+Status\s*[:\\n])\s*Proposed",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_recent_diff(max_chars: int = CHANGELOG_MAX_CHARS) -> str:
    """Return the diff of the last commit (or staged changes)."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD~1", "HEAD", "--stat", "--unified=2"],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR),
            timeout=GIT_TIMEOUT_SECONDS,
        )
        diff = result.stdout
        if len(diff) > max_chars:
            diff = diff[:max_chars] + "\n\n[... diff truncated ...]"
        return diff
    except subprocess.TimeoutExpired:
        return "(git diff timed out)"
    except Exception:
        return "(could not retrieve git diff)"


def get_current_readme() -> str:
    if README.exists():
        content = README.read_text(encoding="utf-8")
        # Only pass first README_MAX_CHARS chars to avoid token bomb
        return content[:README_MAX_CHARS] + (
            "\n\n[... truncated ...]" if len(content) > README_MAX_CHARS else ""
        )
    return ""


# ---------------------------------------------------------------------------
# LLM output validation
# ---------------------------------------------------------------------------

def _validate_llm_output(text: str, max_length: int = 5000) -> str:
    """Basic sanitization of LLM output before writing to files."""
    if not text or not text.strip():
        return ""
    # Truncate excessively long output
    if len(text) > max_length:
        text = text[:max_length] + "\n\n[... output truncated ...]"
    # Strip common LLM preamble artifacts
    text = text.strip()
    if text.startswith("
