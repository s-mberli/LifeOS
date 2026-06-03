import sys
from pathlib import Path
import pytest

# Ensure src/ is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.core.ingest import _extract_title_from_url
from src.core.web import fetch_jina_reader
from unittest.mock import patch, MagicMock

def test_extract_title_from_url_twitter():
    url = "https://x.com/varickagents/status/2059397823674958265?utm_source=tldrfounders"
    title = _extract_title_from_url(url)
    assert title == "X Post by @varickagents"

    url_twitter = "https://twitter.com/cyberfund/status/2058950286324986294"
    title_twitter = _extract_title_from_url(url_twitter)
    assert title_twitter == "X Post by @cyberfund"

def test_extract_title_from_url_general():
    url = "https://thenextweb.com/news/deepseek-v4-pro-75-percent-price-cut-permanent?utm_source=tldrai"
    title = _extract_title_from_url(url)
    assert title == "Deepseek V4 Pro 75 Percent Price Cut Permanent"

    url_no_path = "https://google.com/"
    title_no_path = _extract_title_from_url(url_no_path)
    assert title_no_path == "Google"

def test_jina_reader_title_extraction_with_prefix():
    mock_response = MagicMock()
    mock_response.headers = {}
    mock_response.text = "Title: Varick Agents on X: \"How to Transform a Company With AI\" / X\n\nURL Source: https://x.com/varickagents/status/2059397823674958265\n\nMarkdown Content:\nSome content"
    mock_response.status_code = 200

    with patch("requests.get", return_value=mock_response):
        title, content = fetch_jina_reader("https://x.com/varickagents/status/2059397823674958265")
        assert title == "Varick Agents on X: \"How to Transform a Company With AI\" / X"
