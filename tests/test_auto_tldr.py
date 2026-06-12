import pytest
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
