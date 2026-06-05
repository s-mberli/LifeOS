#!/usr/bin/env python3
"""
scripts/auto_tldr.py — Automated TLDR Newsletter Ingestion

Scrapes all TLDR newsletter editions, processes them through the
MarkusOS ingestion pipeline, and updates the local knowledge vault.

Run manually:
    .venv/bin/python scripts/auto_tldr.py

Or silently via launchd (see com.markusos.tldr_ingest.plist).
"""

from __future__ import annotations

import datetime
import json
import logging
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Project root & importability
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BACKFILL_LIMIT: int = 15  # Max issues to process per topic per run

TLDR_TOPICS: dict[str, str] = {
    "tech":      "Tech",
    "ai":        "AI",
    "webdev":    "Web Dev",
    "infosec":   "InfoSec",
    "devops":    "DevOps",
    "founders":  "Founders",
    "design":    "Design",
    "marketing": "Marketing",
    "product":   "Product Management",
    "crypto":    "Crypto",
    "fintech":   "Fintech",
    "it":        "IT",
    "data":      "Data",
    "hardware":  "Hardware",
}

TRACKING_FILE: Path = ROOT / "data" / "tracking" / "tldr_ingest.json"
NEWS_DIR: Path = ROOT / "data" / "knowledge" / "news"
LOG_FILE: Path = ROOT / "logs" / "tldr_ingest.log"

ARCHIVE_URL_TEMPLATE = "https://tldr.tech/{slug}/archives"
ISSUE_URL_TEMPLATE = "https://tldr.tech/{slug}/{date}"

# Seconds between network requests (be polite)
FETCH_DELAY: float = 0.5



# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """Configure dual file + stdout logging."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("auto_tldr")
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
# Tracking  (flat dict keyed by issue URL)
# ---------------------------------------------------------------------------

def load_tracking() -> dict:
    """Load the tracking state from disk.

    Returns a dict like::

        {
          "https://tldr.tech/tech/2026-06-03": {
            "topic": "tech",
            "date": "2026-06-03",
            "ingested_at": "2026-06-04T10:00:00+10:00"
          }
        }
    """
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
# Archive Parsing
# ---------------------------------------------------------------------------

def get_issue_urls(slug: str, limit: int = BACKFILL_LIMIT) -> list[tuple[str, str]]:
    """Fetch archive page and extract up to *limit* issue URLs.

    Returns a list of ``(url, date)`` tuples, most-recent-first.
    """
    archive_url = ARCHIVE_URL_TEMPLATE.format(slug=slug)
    logger = logging.getLogger("auto_tldr")

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(archive_url, headers=headers, timeout=20)
        resp.raise_for_status()
        html = resp.text
    except Exception as exc:
        logger.error("Failed to fetch archive for %s: %s", slug, exc)
        return []

    # Extract dates from <a href="/{slug}/{YYYY-MM-DD}"> links
    pattern = rf'href="/{re.escape(slug)}/(\d{{4}}-\d{{2}}-\d{{2}})"'
    dates = re.findall(pattern, html)

    # Deduplicate while preserving order (most recent first)
    seen: set[str] = set()
    unique_dates: list[str] = []
    for d in dates:
        if d not in seen:
            seen.add(d)
            unique_dates.append(d)

    results: list[tuple[str, str]] = []
    for date in unique_dates[:limit]:
        url = ISSUE_URL_TEMPLATE.format(slug=slug, date=date)
        results.append((url, date))

    return results


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------

def ingest_newsletter(
    slug: str,
    label: str,
    url: str,
    date: str,
    logger: logging.Logger,
) -> bool:
    """Fetch a single newsletter issue and run it through the pipeline.

    1. Fetch clean markdown via Jina Reader (``src.core.web``).
    2. Save raw markdown to ``data/knowledge/news/``.
    3. Create a temp copy and feed it to ``process_one_file(use_ai=True)``.

    Returns ``True`` on success.
    """
    from src.core.web import fetch_webpage_content  # noqa: E402
    from src.core.ingest import process_one_file  # noqa: E402

    # 1. Fetch content -------------------------------------------------------
    logger.info("  Fetching content: %s", url)
    title, content = fetch_webpage_content(url)

    if not content:
        logger.warning("  Empty content for %s — skipping", url)
        return False

    # 2. Save raw markdown to news/ ------------------------------------------
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    raw_filename = f"tldr_{slug}_{date}.md"
    raw_path = NEWS_DIR / raw_filename

    raw_md = f"# TLDR {label} — {date}\n\nSource: {url}\n\n{content}"
    raw_path.write_text(raw_md, encoding="utf-8")
    logger.info("  Raw markdown saved: %s", raw_path.relative_to(ROOT))

    # 3. Temp copy → process_one_file ----------------------------------------
    #    process_one_file() moves the source file to processed/raw/,
    #    so we hand it a disposable temp copy (same pattern as
    #    process_directory in ingest.py).
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = Path(tmpdir) / raw_filename
        # Put the URL on the first line so _extract_metadata detects it.
        tmp_file.write_text(f"{url}\n\n# TLDR {label}\n\n{content}", encoding="utf-8")

        logger.info("  Running ingestion pipeline (use_ai=True)…")
        try:
            result = process_one_file(str(tmp_file), use_ai=True, rebuild_index_after=False)

            if result.get("success"):
                out = result.get("out_filepath", "?")
                logger.info("  ✓ Ingested → %s", out)
                return True

            logger.error("  ✗ Ingestion failed: %s", result.get("error"))
            return False
        except Exception as exc:
            logger.error("  ✗ Ingestion exception: %s", exc)
            return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("TLDR Newsletter Ingestion — Starting")
    logger.info(
        "Topics: %d | Backfill limit: %d",
        len(TLDR_TOPICS),
        BACKFILL_LIMIT,
    )
    logger.info("=" * 60)

    tracking = load_tracking()
    stats = {"processed": 0, "skipped": 0, "failed": 0, "errors": 0}

    for slug, label in TLDR_TOPICS.items():
        logger.info("")
        logger.info("--- [%s] (%s) ---", label, slug)

        try:
            issues = get_issue_urls(slug, limit=BACKFILL_LIMIT)
        except Exception as exc:
            logger.error("Failed to get issues for %s: %s", slug, exc)
            stats["errors"] += 1
            continue

        if not issues:
            logger.warning("No issues found for %s", slug)
            stats["errors"] += 1
            continue

        logger.info("Found %d issue(s)", len(issues))

        for url, date in issues:
            # Dedup check
            if url in tracking:
                logger.info("  Skip (already ingested): %s", date)
                stats["skipped"] += 1
                continue

            logger.info("  Processing: %s", date)
            success = ingest_newsletter(slug, label, url, date, logger)

            if success:
                tracking[url] = {
                    "topic": slug,
                    "date": date,
                    "ingested_at": datetime.datetime.now(
                        datetime.timezone.utc
                    ).astimezone().isoformat(),
                }
                save_tracking(tracking)  # persist after each success
                stats["processed"] += 1
            else:
                stats["failed"] += 1

            # Politeness delay
            time.sleep(FETCH_DELAY)

    # Rebuild FTS index once at the end of batch
    if stats["processed"] > 0:
        logger.info("")
        logger.info("Rebuilding search index...")
        try:
            from src.core.build_fts_index import build_index
            idx_res = build_index()
            logger.info("✓ Search index rebuilt: %s", idx_res)
        except Exception as exc:
            logger.error("Failed to rebuild search index: %s", exc)

    logger.info("")
    logger.info("=" * 60)
    logger.info(
        "Done! Processed: %d | Skipped: %d | Failed: %d | Errors: %d",
        stats["processed"],
        stats["skipped"],
        stats["failed"],
        stats["errors"],
    )
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
