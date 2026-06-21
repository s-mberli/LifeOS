#!/usr/bin/env python3
"""
scripts/ingest_lenny.py — Ingest Lenny's Podcast Transcripts

Clones the ChatPRD/lennys-podcast-transcripts repository to a temp directory,
parses the frontmatter of each transcript and index file, maps it to LifeOS
standards, and saves the outputs. Tracks idempotency via `lenny_ingest.json`.
"""

from __future__ import annotations

import datetime
import json
import logging
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root & importability
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.frontmatter import read_fm, write_fm
from src.core.db import get_db_connection, init_db

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_URL = "https://github.com/ChatPRD/lennys-podcast-transcripts.git"
TRACKING_FILE = ROOT / "tracking" / "lenny_ingest.json"
PODCAST_DIR = ROOT / "knowledge" / "lenny-podcast"
TOPICS_DIR = ROOT / "knowledge" / "lenny-topics"
LOG_FILE = ROOT / "logs" / "lenny_ingest.log"
DB_PATH = ROOT / "indexes" / "lifeos.db"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """Configure dual file + stdout logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ingest_lenny")
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
# Tracking State
# ---------------------------------------------------------------------------

def load_tracking() -> dict:
    """Load ingested state from disk."""
    if TRACKING_FILE.exists():
        try:
            return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_tracking(data: dict) -> None:
    """Atomically write tracking state to disk."""
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TRACKING_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(TRACKING_FILE)

# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Basic slugification: lowercase, alphanumeric + dashes."""
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")

def insert_outbox(conn, note_path: str, source_url: str, content_str: str) -> None:
    """Insert into the automation_outbox table for the triage worker."""
    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    word_count = len(content_str.split())
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO automation_outbox (note_path, source_url, word_count, added_at)
        VALUES (?, ?, ?, ?)
    """, (note_path, source_url, word_count, now_str))

# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------

def process_episodes(repo_dir: Path, logger: logging.Logger, tracking: dict, conn) -> int:
    """Process episode transcripts."""
    PODCAST_DIR.mkdir(parents=True, exist_ok=True)
    episodes_dir = repo_dir / "episodes"
    processed_count = 0

    if not episodes_dir.exists():
        logger.warning(f"Episodes dir not found in repo: {episodes_dir}")
        return 0

    for transcript_path in episodes_dir.glob("*/transcript.md"):
        parent_folder = transcript_path.parent.name
        
        # Parse existing frontmatter
        try:
            source_fm, body = read_fm(transcript_path)
        except Exception as e:
            logger.error(f"Failed to read {transcript_path}: {e}")
            continue

        # Check idempotency via video_id or folder name
        video_id = source_fm.get("video_id", parent_folder)
        if video_id in tracking:
            continue

        # Remap Fields
        title = source_fm.get("title", "")
        guest = source_fm.get("guest", "")
        publish_date = source_fm.get("publish_date", "")
        youtube_url = source_fm.get("youtube_url", "")
        duration = source_fm.get("duration", "")
        description = source_fm.get("description", "")

        # Fallback slug if guest is empty
        if guest:
            slug = slugify(guest)
        else:
            slug = slugify(parent_folder)

        dest_file = PODCAST_DIR / f"{slug}.md"
        
        # Ensure unique filenames if multiple episodes by same guest
        counter = 1
        while dest_file.exists() and dest_file.name != tracking.get(video_id, {}).get("dest_file", ""):
             dest_file = PODCAST_DIR / f"{slug}-{counter}.md"
             counter += 1

        new_fm = {
            "title": title,
            "guest": guest,
            "date": publish_date,
            "source_url": youtube_url,
            "type": "podcast_transcript",
            "expert": "lenny-rachitsky",
        }
        if duration:
            new_fm["duration"] = duration
        if description:
            new_fm["description"] = description
            
        try:
            write_fm(dest_file, new_fm, body)
            # Insert into Outbox
            relative_note_path = str(dest_file.relative_to(ROOT))
            insert_outbox(conn, relative_note_path, youtube_url, body)
            conn.commit()

            tracking[video_id] = {
                "dest_file": dest_file.name,
                "ingested_at": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
            }
            save_tracking(tracking)
            
            logger.info(f"Ingested episode: {dest_file.name}")
            processed_count += 1
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to process episode {parent_folder}: {e}")

    return processed_count


def process_topics(repo_dir: Path, logger: logging.Logger) -> int:
    """Copy topic indices."""
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    index_dir = repo_dir / "index"
    processed_count = 0

    if not index_dir.exists():
        logger.warning(f"Index dir not found in repo: {index_dir}")
        return 0

    for topic_path in index_dir.glob("*.md"):
        dest_file = TOPICS_DIR / topic_path.name
        try:
            shutil.copy2(topic_path, dest_file)
            processed_count += 1
            logger.info(f"Copied topic index: {dest_file.name}")
        except Exception as e:
            logger.error(f"Failed to copy topic {topic_path.name}: {e}")

    return processed_count

def main():
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Lenny Podcast Transcripts Ingestion — Starting")
    logger.info("=" * 60)

    tracking = load_tracking()

    # Create Database Connection
    try:
        conn = get_db_connection(DB_PATH)
        init_db(conn)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_dir = Path(tmpdir) / "repo"
            logger.info(f"Cloning repository to {tmpdir}...")
            
            git_bin = shutil.which("git") or "git"
            try:
                subprocess.run(
                    [git_bin, "clone", "--depth", "1", REPO_URL, str(repo_dir)],
                    check=True,
                    capture_output=True,
                    text=True
                )  # nosec B603
            except subprocess.CalledProcessError as e:
                logger.error(f"Git clone failed: {e.stderr}")
                return

            episodes_processed = process_episodes(repo_dir, logger, tracking, conn)
            topics_processed = process_topics(repo_dir, logger)

            if episodes_processed > 0 or topics_processed > 0:
                logger.info("Rebuilding search index...")
                try:
                    from src.core.build_fts_index import build_index
                    idx_res = build_index()
                    logger.info(f"Search index rebuilt: {idx_res}")
                except Exception as exc:
                    logger.error(f"Failed to rebuild search index: {exc}")

            logger.info("=" * 60)
            logger.info(f"Done! Processed Episodes: {episodes_processed} | Copied Topics: {topics_processed}")
            logger.info("=" * 60)
            
    finally:
        conn.close()

if __name__ == "__main__":
    main()
