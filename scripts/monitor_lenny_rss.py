#!/usr/bin/env python3
"""
scripts/monitor_lenny_rss.py — Monitor Lenny's RSS feed for new episodes

Checks Substack RSS for new podcast episodes. If any are missing from
data/tracking/lenny_ingest.json, it runs `scripts/ingest_lenny.py`
to fetch new transcripts. Logs warnings if transcripts are missing in the repo.
"""

from __future__ import annotations

import datetime
import json
import logging
import re
import requests
import subprocess
import sys
import xml.etree.ElementTree as ET  # nosec B405
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root & importability
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

RSS_URL = "https://www.lennysnewsletter.com/feed"
TRACKING_FILE = ROOT / "data" / "tracking" / "lenny_ingest.json"
LOG_FILE = ROOT / "logs" / "lenny_rss.log"
INGEST_SCRIPT = ROOT / "scripts" / "ingest_lenny.py"

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("monitor_lenny_rss")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        try:
            return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def extract_youtube_ids(text: str) -> list[str]:
    """Find YouTube video IDs in a given text block."""
    if not text:
        return []
    # Match various youtube formats
    patterns = [
        r"youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/v/([a-zA-Z0-9_-]{11})"
    ]
    video_ids = []
    for pattern in patterns:
        video_ids.extend(re.findall(pattern, text))
    return list(set(video_ids))

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------
def main():
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Lenny Podcast RSS Monitor — Starting")
    logger.info("=" * 60)

    # 1. Fetch RSS Feed
    try:
        logger.info(f"Fetching RSS feed from {RSS_URL}...")
        response = requests.get(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        response.raise_for_status()
        xml_data = response.content
    except Exception as e:
        logger.error(f"Failed to fetch RSS feed: {e}")
        sys.exit(1)

    # 2. Parse RSS XML
    try:
        root = ET.fromstring(xml_data)  # nosec B314
    except Exception as e:

        logger.error(f"Failed to parse RSS XML: {e}")
        sys.exit(1)

    channel = root.find("channel")
    if channel is None:
        logger.error("Invalid RSS: <channel> element not found.")
        sys.exit(1)

    items = channel.findall("item")
    logger.info(f"Found {len(items)} total feed items.")

    # 3. Filter podcast items and extract metadata
    podcasts = []
    for item in items:
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
        enclosure = item.find("enclosure")
        
        # Substack podcasts have audio/mpeg enclosure
        is_podcast = enclosure is not None and enclosure.attrib.get("type") == "audio/mpeg"
        
        if is_podcast:
            content_el = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
            content_text = content_el.text if content_el is not None else ""
            desc_text = item.find("description").text if item.find("description") is not None else ""
            
            video_ids = extract_youtube_ids(desc_text + "\n" + content_text)
            
            podcasts.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "video_ids": video_ids
            })

    logger.info(f"Filtered {len(podcasts)} podcast episodes from feed.")

    # 4. Compare with existing tracking
    tracking = load_tracking()
    missing_episodes = []

    for pod in podcasts:
        # Check if any video ID of this podcast is already tracked
        tracked = False
        for vid in pod["video_ids"]:
            if vid in tracking:
                tracked = True
                break
        
        if not tracked and pod["video_ids"]:
            missing_episodes.append(pod)

    if not missing_episodes:
        logger.info("All podcast episodes in RSS feed are already tracked.")
        logger.info("=" * 60)
        return

    logger.info(f"Detected {len(missing_episodes)} new episode(s) in RSS feed:")
    for pod in missing_episodes:
        logger.info(f"  - {pod['title']} (YT: {pod['video_ids']})")

    # 5. Trigger Ingestion Script
    logger.info("Triggering ingest_lenny.py...")
    try:
        res = subprocess.run(
            [sys.executable, str(INGEST_SCRIPT)],
            capture_output=True,
            text=True,
            check=True
        )  # nosec B603
        logger.info("ingest_lenny.py completed successfully.")
        # Log its output at debug level or info if we want
        logger.debug(res.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"ingest_lenny.py failed with exit code {e.returncode}: {e.stderr}")
        # Continue to verify what got tracked anyway

    # 6. Re-check state to identify pending transcripts
    tracking = load_tracking()
    for pod in missing_episodes:
        still_missing = []
        for vid in pod["video_ids"]:
            if vid not in tracking:
                still_missing.append(vid)
        
        if still_missing:
            logger.warning(
                f"Transcript PENDING: Episode \"{pod['title']}\" (IDs: {still_missing}) "
                "is in RSS, but its transcript is not yet present in the Git transcripts repository."
            )
        else:
            logger.info(f"Success: Episode \"{pod['title']}\" has been successfully ingested.")

    logger.info("=" * 60)

if __name__ == "__main__":
    main()
