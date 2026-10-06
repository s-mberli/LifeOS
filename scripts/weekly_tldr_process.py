#!/usr/bin/env python3
"""Print a sourced TLDR roundup for Hermes to deliver once via Telegram."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
NEWS_DIR = ROOT / "data" / "knowledge" / "news"
SYDNEY = ZoneInfo("Australia/Sydney")
ARTICLE = re.compile(
    r"^### (?P<title>[^\n]+)\n- \*\*URL:\*\* (?P<url>[^\n]+)"
    r"(?:\n(?:- [^\n]+))*?\n- \*\*TLDR Summary:\*\* (?P<summary>[^\n]+)",
    re.MULTILINE,
)
ISSUE = re.compile(r"^tldr_[a-z0-9_-]+_(\d{4}-\d{2}-\d{2})\.md$")
PRIORITY = ("ai", "agent", "product", "software", "data", "security", "health", "business")


def collect_articles(news_dir: Path, today: dt.date) -> list[dict[str, str]]:
    """Read only issues from the preceding seven Sydney calendar days."""
    found: dict[str, dict[str, str]] = {}
    for path in sorted(news_dir.glob("tldr_*.md"), reverse=True):
        match = ISSUE.fullmatch(path.name)
        if not match:
            continue
        issue_date = dt.date.fromisoformat(match.group(1))
        if not 0 <= (today - issue_date).days < 7:
            continue
        for item in ARTICLE.finditer(path.read_text(encoding="utf-8")):
            url = item.group("url").strip()
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                continue
            title = item.group("title").strip()
            summary = item.group("summary").strip()
            if not title or not summary:
                continue
            found.setdefault(url, {"title": title, "url": url, "summary": summary, "date": issue_date.isoformat()})
    return list(found.values())


def rank_article(article: dict[str, str]) -> tuple[int, str]:
    content = (article["title"] + " " + article["summary"]).lower()
    score = sum(word in content for word in PRIORITY)
    return score, article["date"]


def digest(articles: list[dict[str, str]], today: dt.date) -> str:
    if not articles:
        return f"TLDR weekly digest · {today:%d %b %Y}\nNo sourced TLDR articles were captured in the past seven days."
    selected = sorted(articles, key=rank_article, reverse=True)[:5]
    lines = [f"TLDR weekly digest · {today:%d %b %Y}"]
    for article in selected:
        summary = article["summary"]
        if len(summary) > 220:
            summary = summary[:217].rsplit(" ", 1)[0] + "…"
        lines.extend(("", f"• {article['title']}", article["url"], f"Why it matters: {summary}"))
    if len(selected) < 5:
        lines.extend(("", f"Only {len(selected)} sourced item(s) were available this week."))
    return "\n".join(lines)


def main() -> None:
    today = dt.datetime.now(SYDNEY).date()
    print(digest(collect_articles(NEWS_DIR, today), today))


if __name__ == "__main__":
    main()
