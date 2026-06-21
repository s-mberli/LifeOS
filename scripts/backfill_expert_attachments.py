#!/usr/bin/env python3
"""
scripts/backfill_expert_attachments.py — Backfill expert attachments for all unattached insight notes.

Scans knowledge directories, enriches files with domain/channel metadata based on
their source directory, then attaches them to the appropriate expert.

Usage:
    .venv/bin/python scripts/backfill_expert_attachments.py [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import datetime
import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root & importability
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=True)
    hermes_env = Path("/root/.hermes/.env")
    if hermes_env.exists():
        load_dotenv(hermes_env, override=False)
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Configuration: directory → expert mapping
# ---------------------------------------------------------------------------
DIR_TO_EXPERT: dict[str, dict] = {
    "lenny-podcast": {
        "slug": "expert--lenny-rachitsky",
        "name": "Lenny Rachitsky",
        "domain": "creator-wisdom",
        "channel": "Lenny's Podcast",
    },
    "lenny-topics": {
        "slug": "expert--lenny-rachitsky",
        "name": "Lenny Rachitsky",
        "domain": "creator-wisdom",
        "channel": "Lenny's Newsletter",
    },
    "news": {
        "slug": "expert--tldr-expert",
        "name": "TLDR Expert",
        "domain": "tldr",
        "channel": "TLDR Newsletter",
    },
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    logger = logging.getLogger("backfill_experts")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger

# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------
def process_file(
    fpath: Path,
    dir_key: str,
    expert_info: dict,
    dry_run: bool,
    logger: logging.Logger,
) -> bool:
    """Enrich a single file and attach to expert. Returns True on success."""
    from src.core.frontmatter import read_fm, write_fm
    from src.core.experts import assign_insight_to_expert

    try:
        fm, body = read_fm(fpath)
    except Exception as exc:
        logger.warning("  Cannot read %s: %s", fpath.name, exc)
        return False

    # Skip non-insight files
    fm_type = fm.get("type", "")
    if fm_type not in ("podcast_transcript", "insight_note", "newsletter", None, ""):
        logger.debug("  Skip (type=%s): %s", fm_type, fpath.name)
        return False

    # Skip already attached
    if fm.get("expert_status") == "attached":
        logger.debug("  Skip (already attached): %s", fpath.name)
        return False

    slug = expert_info["slug"]
    name = expert_info["name"]
    domain = expert_info["domain"]
    channel = expert_info["channel"]

    if dry_run:
        logger.info("  [DRY-RUN] Would attach: %s → %s", fpath.name, slug)
        return True

    # Step 1: Enrich frontmatter with domain/channel
    fm["domain"] = domain
    fm["channel"] = channel
    if not fm.get("type"):
        fm["type"] = "insight_note"
    fm["updated_at"] = datetime.datetime.now(
        datetime.timezone.utc
    ).astimezone().isoformat()

    try:
        write_fm(fpath, fm, body)
        logger.info("  Enriched: %s (domain=%s)", fpath.name, domain)
    except Exception as exc:
        logger.error("  Failed to write frontmatter: %s: %s", fpath.name, exc)
        return False

    # Step 2: Attach to expert
    try:
        result = assign_insight_to_expert(
            fpath, slug, name, reason="backfill_script"
        )
        if result.get("success"):
            logger.info("  ✓ Attached: %s → %s", fpath.name, slug)
            return True
        else:
            logger.warning("  ✗ Attachment failed: %s: %s", fpath.name, result.get("error"))
            return False
    except Exception as exc:
        logger.error("  ✗ Attachment exception: %s: %s", fpath.name, exc)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill expert attachments")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--limit", type=int, default=0, help="Max files to process (0=all)")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Expert Attachment Backfill")
    logger.info("Dry run: %s", args.dry_run)
    logger.info("=" * 60)

    knowledge_dir = ROOT / "knowledge"
    stats = {"processed": 0, "skipped": 0, "failed": 0}

    for dir_key, expert_info in DIR_TO_EXPERT.items():
        target_dir = knowledge_dir / dir_key
        if not target_dir.is_dir():
            logger.warning("Directory not found: %s", target_dir)
            continue

        logger.info("")
        logger.info("--- [%s] → %s ---", dir_key, expert_info["slug"])

        files = sorted(target_dir.rglob("*.md"))
        # Filter out README, .gitkeep, etc.
        files = [f for f in files if f.suffix == ".md" and not f.name.startswith(".")]
        # Filter out raw transcript folders
        files = [f for f in files if "raw" not in f.parts]

        logger.info("Found %d files", len(files))

        for fpath in files:
            if args.limit and stats["processed"] >= args.limit:
                logger.info("Limit reached (%d)", args.limit)
                break

            success = process_file(fpath, dir_key, expert_info, args.dry_run, logger)
            if success:
                stats["processed"] += 1
            else:
                stats["skipped"] += 1

    # Rebuild FTS index
    if stats["processed"] > 0 and not args.dry_run:
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
        "Done! Processed: %d | Skipped: %d | Failed: %d",
        stats["processed"],
        stats["skipped"],
        stats["failed"],
    )
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
