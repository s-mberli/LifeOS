from unittest.mock import Mock

from scripts import auto_tldr
from scripts.auto_tldr import extract_articles_from_html

SAMPLE_HTML = """
<html><body>
<article class="mt-3">
  <a class="font-bold" href="https://example.com/sponsor" rel="noopener noreferrer" target="_blank">
    <h3>Awesome AI Tool (Sponsor)</h3>
  </a>
  <div class="newsletter-html">Buy this tool now.</div>
</article>

<article class="mt-3">
  <a class="font-bold" href="https://example.com/real-article" rel="noopener noreferrer" target="_blank">
    <h3>GPT-6 Released Early (12 minute read)</h3>
  </a>
  <div class="newsletter-html">OpenAI surprised everyone today.</div>
</article>

<article class="mt-3">
  <a class="font-bold" href="https://example.com/broken">
    <h3>)</h3>
  </a>
  <div class="newsletter-html"></div>
</article>

<article class="mt-3">
  <a class="font-bold" href="https://example.com/no-read-time">
    <h3>Just a short update</h3>
  </a>
  <div class="newsletter-html">This is a short update without read time.</div>
</article>
</body></html>
"""

def test_extract_articles_from_html():
    results = extract_articles_from_html(SAMPLE_HTML, "https://tldr.tech/ai/2026-06-04", "AI", "2026-06-04")
    
    # Sponsor and broken ')' article should be skipped. 4 total - 2 skipped = 2 remaining.
    assert len(results) == 2
    
    art1 = results[0]
    assert art1["title"] == "GPT-6 Released Early"
    assert art1["url"] == "https://example.com/real-article"
    assert art1["read_time"] == "12 minute read"
    assert "OpenAI surprised" in art1["tldr_summary"]
    assert art1["via"] == "TLDR AI, 2026-06-04"
    
    art2 = results[1]
    assert art2["title"] == "Just a short update"
    assert art2["url"] == "https://example.com/no-read-time"
    assert art2["read_time"] == "Unknown"
    assert "short update without" in art2["tldr_summary"]


def test_ingest_saves_searchable_raw_note_without_ai(tmp_path, monkeypatch):
    monkeypatch.setattr(auto_tldr, "ROOT", tmp_path)
    monkeypatch.setattr(auto_tldr, "NEWS_DIR", tmp_path / "data/knowledge/news")
    monkeypatch.setattr(auto_tldr.requests, "get", lambda *args, **kwargs: Mock(text=SAMPLE_HTML))
    monkeypatch.setattr(auto_tldr, "get_clean_markdown", lambda html: "Newsletter text")
    assert auto_tldr.ingest_newsletter(
        "ai", "AI", "https://tldr.tech/ai/2026-06-04", "2026-06-04", Mock()
    )
    note = (tmp_path / "data/knowledge/news/tldr_ai_2026-06-04.md").read_text(encoding="utf-8")
    assert "https://example.com/real-article" in note
    assert "OpenAI surprised" in note
