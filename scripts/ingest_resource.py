"""
scripts/ingest_resource.py — Backwards-compatibility shim.

All logic has been moved into ``scripts/core/``.  This file re-exports
everything that existing callers depend on so that ``import ingest_resource``
continues to work without modification.

New code should import directly from the relevant ``scripts/core/*`` module.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure scripts/ is on sys.path so core sub-modules resolve correctly
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# ---------------------------------------------------------------------------
# Re-exports from core modules
# ---------------------------------------------------------------------------

from core.frontmatter import read_fm, write_fm, update_fm  # noqa: F401
from core.youtube import (  # noqa: F401
    clean_youtube_url,
    extract_video_id,
    fetch_video_metadata,
    fetch_transcript,
    save_transcript,
)
from core.web import fetch_webpage_content, fetch_webpage_metadata  # noqa: F401
from core.experts import (  # noqa: F401
    slugify_expert_name,
    get_existing_experts,
    assign_insight_to_expert,
    scan_unattached_insights,
    generate_expert_update_suggestion,
    _suggest_experts_for_domain,
)
from core.ingest import process_one_file  # noqa: F401

# ---------------------------------------------------------------------------
# Legacy aliases — kept for code that still calls the old names
# ---------------------------------------------------------------------------

def update_insight_frontmatter(path: str, **kwargs) -> bool:
    """Legacy wrapper around ``core.frontmatter.update_fm``.

    Args:
        path:    Path to the Markdown file (string accepted for compatibility).
        **kwargs: Key/value pairs to patch in the frontmatter.

    Returns:
        ``True`` on success, ``False`` on failure.
    """
    return update_fm(Path(path), **kwargs)


def fetch_youtube_metadata(url: str) -> tuple[str, str]:
    """Legacy wrapper — returns (title, uploader) for a YouTube video URL."""
    meta = fetch_video_metadata(url)
    return meta.get("title", ""), meta.get("uploader", "")


def extract_youtube_video_id(url: str) -> str | None:
    """Legacy alias for ``core.youtube.extract_video_id``."""
    return extract_video_id(url)


def fetch_youtube_transcript(url: str) -> str | None:
    """Legacy alias for ``core.youtube.fetch_transcript``."""
    return fetch_transcript(url)


def clean_url(url: str) -> str:
    """Legacy URL cleaner — strips trailing punctuation."""
    return url.strip().strip(' "\'.,;!)]>')
