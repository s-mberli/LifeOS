#!/usr/bin/env python3
"""
scripts/event_tracker.py — Local event aggregator for Sydney/Epping area.

Scrapes Meetup, Eventbrite, Humanitix, and Facebook for events matching
configured categories (dance, yoga, wellness, music). Sends daily digest
via Telegram.

Usage:
    .venv/bin/python scripts/event_tracker.py           # run once
    .venv/bin/python scripts/event_tracker.py --dry-run # preview only

Cron: 0 8 * * * cd /root/markusos && .venv/bin/python scripts/event_tracker.py >> logs/events.log 2>&1
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import textwrap
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "config" / "event_sources.yaml"
TRACKING_FILE = ROOT / "tracking" / "events_seen.json"
LOG_FILE = ROOT / "logs" / "events.log"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def setup_logging(verbose: bool = False) -> logging.Logger:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("event_tracker")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def load_config() -> dict:
    if not CONFIG_FILE.exists():
        logger.error("Config not found: %s", CONFIG_FILE)
        sys.exit(1)
    raw = CONFIG_FILE.read_text(encoding="utf-8")
    # Expand ${ENV_VAR} references
    def expand_env(match):
        return os.environ.get(match.group(1), "")
    raw = re.sub(r"\$\{(\w+)\}", expand_env, raw)
    return yaml.safe_load(raw)

# ---------------------------------------------------------------------------
# Tracking (dedup)
# ---------------------------------------------------------------------------
def load_seen() -> dict:
    if TRACKING_FILE.exists():
        try:
            return json.loads(TRACKING_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_seen(seen: dict) -> None:
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = TRACKING_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(seen, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(TRACKING_FILE)

def event_key(source: str, url: str) -> str:
    return f"{source}:{url}"

def is_new(key: str, seen: dict) -> bool:
    return key not in seen

def mark_seen(key: str, seen: dict, title: str = "", date: str = "") -> None:
    seen[key] = {"title": title, "date": date, "seen_at": datetime.now(timezone.utc).isoformat()}

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-AU,en;q=0.9",
}

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def parse_date_flexible(date_str: str) -> datetime | None:
    """Try multiple date formats."""
    if not date_str:
        return None
    date_str = date_str.strip()
    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d/%m/%Y",
        "%Y-%m-%dT%H:%M:%S.%f%z",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def is_within_days(date_str: str, max_days: int) -> bool:
    dt = parse_date_flexible(date_str)
    if not dt:
        return True  # include if we can't parse
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = dt - now
    return timedelta(0) <= delta <= timedelta(days=max_days)

def matches_category(text: str, keywords: list[str]) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)

# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------
class EventScraper:
    """Base class for event scrapers."""

    def __init__(self, config: dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.location = config.get("location", {})
        self.days_ahead = config.get("days_ahead", 14)

    def search(self, category: str, keywords: list[str]) -> list[dict]:
        raise NotImplementedError


class EventbriteScraper(EventScraper):
    """Scrape Eventbrite via their public API."""

    def search(self, category: str, keywords: list[str]) -> list[dict]:
        api_key = self.config.get("sources", {}).get("eventbrite", {}).get("api_key", "")
        if not api_key:
            self.logger.warning("Eventbrite: no API key configured, skipping")
            return []

        events = []
        base_url = "https://www.eventbriteapi.com/v3/events/search"

        for keyword in keywords[:3]:  # ponytail: limit to 3 keywords per category
            params = {
                "q": keyword,
                "location.address": f"{self.location.get('city', 'Sydney')}, {self.location.get('region', 'NSW')}, {self.location.get('country', 'AU')}",
                "location.within": f"{self.location.get('radius_km', 30)}km",
                "start_date.range_start": datetime.now().strftime("%Y-%m-%dT00:00:00"),
                "start_date.range_end": (
                    datetime.now() + timedelta(days=self.days_ahead)
                ).strftime("%Y-%m-%dT23:59:59"),
                "sort_by": "date",
                "expand": "venue",
            }
            try:
                resp = requests.get(
                    base_url,
                    params=params,
                    headers={"Authorization": f"Bearer {api_key}", **HEADERS},
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                for ev in data.get("events", []):
                    events.append({
                        "title": ev.get("name", {}).get("text", ""),
                        "url": ev.get("url", ""),
                        "date": ev.get("start", {}).get("local", ""),
                        "venue": ev.get("venue", {}).get("name", "") if ev.get("venue") else "",
                        "description": clean_text(ev.get("description", {}).get("text", ""))[:200],
                        "source": "eventbrite",
                        "category": category,
                    })
            except Exception as exc:
                self.logger.error("Eventbrite error for '%s': %s", keyword, exc)

        return events


class MeetupScraper(EventScraper):
    """Scrape Meetup public search pages."""

    def search(self, category: str, keywords: list[str]) -> list[dict]:
        events = []
        city = self.location.get("city", "Sydney")
        region = self.location.get("region", "NSW")

        for keyword in keywords[:3]:
            url = (
                f"https://www.meetup.com/find/"
                f"?location={urllib.parse.quote(city + ', ' + region + ', AU')}"
                f"&source=EVENTS"
                f"&keywords={urllib.parse.quote(keyword)}"
            )
            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                # Meetup renders events in <a> cards with event links
                for link in soup.find_all("a", href=re.compile(r"/events/\d+")):
                    event_url = str(link.get("href", "") or "")
                    if not event_url.startswith("http"):
                        event_url = "https://www.meetup.com" + event_url

                    title_el = link.find(["h2", "h3", "h4", "span", "p"])
                    title = clean_text(title_el.get_text()) if title_el else ""

                    # Try to find date nearby
                    date_el = link.find_next(string=re.compile(
                        r"\w+ \d{1,2},? \d{4}|\d{1,2} \w+ \d{4}|"
                        r"\w+ \d{1,2}(?:st|nd|rd|th)"
                    ))
                    date_str = date_el.strip() if date_el else ""

                    if title and event_url:
                        events.append({
                            "title": title,
                            "url": event_url,
                            "date": date_str,
                            "venue": "",
                            "description": "",
                            "source": "meetup",
                            "category": category,
                        })
            except Exception as exc:
                self.logger.error("Meetup error for '%s': %s", keyword, exc)

        return events


class HumanitixScraper(EventScraper):
    """Scrape Humanitix event listings."""

    def search(self, category: str, keywords: list[str]) -> list[dict]:
        events = []
        base = "https://humanitix.com/au/events/au--nsw--sydney"

        for keyword in keywords[:3]:
            url = f"{base}?q={urllib.parse.quote(keyword)}"
            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                # Humanitix event cards
                for card in soup.find_all("a", href=re.compile(r"/au/events/")):
                    event_url = card.get("href", "")
                    if not event_url.startswith("http"):
                        event_url = "https://humanitix.com" + event_url

                    title_el = card.find(["h2", "h3", "h4", "span", "p"])
                    title = clean_text(title_el.get_text()) if title_el else ""

                    date_el = card.find(string=re.compile(
                        r"\d{1,2} \w+ \d{4}|\w+ \d{1,2}"
                    ))
                    date_str = date_el.strip() if date_el else ""

                    venue_el = card.find(string=re.compile(r"Sydney|Parramatta|Chatswood|Hornsby|Epping"))
                    venue = venue_el.strip() if venue_el else ""

                    if title and event_url:
                        events.append({
                            "title": title,
                            "url": event_url,
                            "date": date_str,
                            "venue": venue,
                            "description": "",
                            "source": "humanitix",
                            "category": category,
                        })
            except Exception as exc:
                self.logger.error("Humanitix error for '%s': %s", keyword, exc)

        return events


class FacebookScraper(EventScraper):
    """Monitor user-submitted Facebook event URLs for changes.

    Free FB scrape impossible without login. Instead:
    - User pastes FB event URLs in config
    - This checks if page is publicly accessible (some are)
    - If inaccessible (login-wall), logs a note once per URL
    """

    def search(self, category: str, keywords: list[str]) -> list[dict]:
        urls = self.config.get("sources", {}).get("facebook", {}).get("event_urls", [])
        if not urls:
            return []

        events = []
        for event_url in urls:
            key = f"facebook:{event_url}"
            if not is_new(key, {}):
                continue  # already tracked, skip poll
            try:
                resp = requests.get(event_url, headers=HEADERS, timeout=15, allow_redirects=True)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                title_el = soup.find(["h1", "h2", "title"])
                title = clean_text(title_el.get_text()) if title_el else event_url.split("/")[-1]

                date_el = soup.find(string=re.compile(r"\d{1,2} \w+ \d{4}|\w+ \d{1,2}, \d{4}"))
                date_str = date_el.strip() if date_el else ""

                events.append({
                    "title": title,
                    "url": event_url,
                    "date": date_str,
                    "venue": "",
                    "description": "",
                    "source": "facebook",
                    "category": category,
                })
            except requests.HTTPError as exc:
                if exc.response and exc.response.status_code in (401, 403):
                    self.logger.debug("FB event login-wall: %s", event_url)
                else:
                    self.logger.debug("FB event error %s: %s", event_url, exc)
            except Exception as exc:
                self.logger.debug("FB event error: %s — %s", event_url, exc)

        return events


# ---------------------------------------------------------------------------
# Telegram delivery
# ---------------------------------------------------------------------------
def send_telegram_digest(events_by_category: dict, config: dict, logger: logging.Logger) -> None:
    """Send formatted digest to Telegram via Hermes bot."""
    if not events_by_category:
        logger.info("No new events to send.")
        return

    # Build message
    lines = [f"🎪 **Events Digest** — {datetime.now().strftime('%a %d %B')}", ""]

    category_emojis = {
        "dance": "💃",
        "yoga": "🧘",
        "wellness": "🌿",
        "music": "🎵",
    }

    delivery_cfg = config.get("delivery", {}).get("telegram", {})
    max_per = delivery_cfg.get("max_per_category", 5)

    for category, events in sorted(events_by_category.items()):
        emoji = category_emojis.get(category, "📌")
        lines.append(f"{emoji} **{category.title()}** ({len(events)} new)")
        lines.append("")

        for ev in events[:max_per]:
            title = ev["title"][:80]
            date_str = ev.get("date", "")
            if date_str:
                dt = parse_date_flexible(date_str)
                if dt:
                    date_str = dt.strftime("%a %d %b")
            venue = f" @ {ev['venue']}" if ev.get("venue") else ""
            source = ev.get("source", "")

            lines.append(f"  • [{title}]({ev.get('url', '')})")
            if date_str:
                lines.append(f"    📅 {date_str}{venue} · {source}")
            lines.append("")

    message = "\n".join(lines)

    # Truncate to Telegram's 4096 char limit
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (truncated)"

    logger.info("Sending Telegram digest (%d chars)...", len(message))

    # Use Hermes CLI to send via Telegram
    try:
        result = subprocess.run(
            ["hermes", "telegram", "send", "--message", message],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            logger.info("✓ Telegram digest sent")
        else:
            logger.error("Telegram send failed: %s", result.stderr)
            # Fallback: just log the message
            logger.info("Digest content:\n%s", message)
    except FileNotFoundError:
        logger.warning("hermes CLI not found, logging digest instead")
        logger.info("Digest content:\n%s", message)
    except Exception as exc:
        logger.error("Telegram send error: %s", exc)
        logger.info("Digest content:\n%s", message)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Local event tracker")
    parser.add_argument("--dry-run", action="store_true", help="Don't send Telegram message")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    global logger
    logger = setup_logging(args.verbose)
    config = load_config()

    logger.info("=" * 60)
    logger.info("Event Tracker — Starting")
    logger.info("=" * 60)

    seen = load_seen()
    categories = config.get("categories", {})
    sources_cfg = config.get("sources", {})
    delivery_cfg = config.get("delivery", {}).get("telegram", {})
    max_days = delivery_cfg.get("max_days_ahead", 14)

    # Initialize scrapers
    scrapers = {}
    if sources_cfg.get("eventbrite", {}).get("enabled"):
        scrapers["eventbrite"] = EventbriteScraper(config, logger)
    if sources_cfg.get("meetup", {}).get("enabled"):
        scrapers["meetup"] = MeetupScraper(config, logger)
    if sources_cfg.get("humanitix", {}).get("enabled"):
        scrapers["humanitix"] = HumanitixScraper(config, logger)
    if sources_cfg.get("facebook", {}).get("enabled"):
        scrapers["facebook"] = FacebookScraper(config, logger)

    # Collect events per category
    events_by_category: dict[str, list[dict]] = {}
    total_new = 0

    for category, cat_cfg in categories.items():
        keywords = cat_cfg.get("keywords", [])
        if not keywords:
            continue

        logger.info("--- Category: %s (%d keywords) ---", category, len(keywords))

        for source_name, scraper in scrapers.items():
            try:
                found = scraper.search(category, keywords)
                logger.info("  %s: %d events found", source_name, len(found))

                for ev in found:
                    key = event_key(source_name, ev["url"])
                    if not is_new(key, seen):
                        continue
                    if not is_within_days(ev.get("date", ""), max_days):
                        continue

                    mark_seen(key, seen, ev["title"], ev.get("date", ""))
                    events_by_category.setdefault(category, []).append(ev)
                    total_new += 1

            except Exception as exc:
                logger.error("  %s: error — %s", source_name, exc)

    logger.info("Total new events: %d", total_new)

    # Deduplicate across sources (same title + date)
    for category in events_by_category:
        seen_titles = set()
        unique = []
        for ev in events_by_category[category]:
            dedup_key = ev["title"].lower()[:50]
            if dedup_key not in seen_titles:
                seen_titles.add(dedup_key)
                unique.append(ev)
        events_by_category[category] = unique

    # Save tracking
    save_seen(seen)

    # Send digest
    if not args.dry_run:
        send_telegram_digest(events_by_category, config, logger)
    else:
        logger.info("[DRY-RUN] Would send %d categories", len(events_by_category))
        for cat, evts in events_by_category.items():
            logger.info("  %s: %d events", cat, len(evts))
            for ev in evts[:3]:
                logger.info("    - %s (%s)", ev["title"][:60], ev.get("source", ""))

    logger.info("Done.")


if __name__ == "__main__":
    main()
