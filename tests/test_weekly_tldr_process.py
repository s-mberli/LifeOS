import datetime as dt

from scripts.weekly_tldr_process import collect_articles, digest


def test_digest_uses_only_recent_linked_articles(tmp_path):
    today = dt.date(2026, 9, 24)
    for date, title in (("2026-09-23", "Useful AI update"), ("2026-09-16", "Stale update")):
        (tmp_path / f"tldr_ai_{date}.md").write_text(
            f"# TLDR\nSource: https://tldr.tech/ai/{date}\n\n## Articles\n\n"
            f"### {title}\n- **URL:** https://example.com/{date}\n"
            "- **Via:** TLDR AI\n- **Read time:** 4 minute read\n"
            "- **TLDR Summary:** This changes how teams plan software.\n"
            "\n### Unlinked update\n- **URL:** mailto:test@example.com\n"
            "- **TLDR Summary:** Unusable.\n", encoding="utf-8"
        )
    articles = collect_articles(tmp_path, today)
    result = digest(articles, today)
    assert len(articles) == 1
    assert "Useful AI update" in result
    assert "https://example.com/2026-09-23" in result
    assert "Why it matters: This changes" in result
    assert "Stale update" not in result
    assert "Unlinked update" not in result


def test_digest_reports_no_sources():
    assert "No sourced TLDR articles" in digest([], dt.date(2026, 9, 24))
