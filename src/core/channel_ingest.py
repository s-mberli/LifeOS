"""
scripts/channel_ingest.py — Backwards-compatibility shim.

All logic has been moved into ``scripts/core/youtube.py`` and
``scripts/core/experts.py``.  This file re-exports everything that existing
callers depend on.

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
# Re-exports
# ---------------------------------------------------------------------------

from core.youtube import (  # noqa: F401
    clean_youtube_url,
    fetch_channel_metadata,
    fetch_recent_videos,
)
from core.experts import synthesize_creator_persona  # noqa: F401
