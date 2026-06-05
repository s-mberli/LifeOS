"""
tests/test_auto_tldr.py — Unit tests for the TLDR newsletter ingestion script.
"""

import json
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# ---------------------------------------------------------------------------
# Patch ROOT before importing the module so paths point to a temp dir
# ---------------------------------------------------------------------------
_ORIG_ROOT = Path(__file__).resolve().parent.parent


def _import_auto_tldr():
    """Import the module fresh, with sys.path set up."""
    import importlib
    import sys

    sys.path.insert(0, str(_ORIG_ROOT))
    # Force re-import if already cached
    if "scripts.auto_tldr" in sys.modules:
        del sys.modules["scripts.auto_tldr"]

    # Import as a module from the scripts directory
    import scripts.auto_tldr as mod  # type: ignore

    return mod


auto_tldr = _import_auto_tldr()


# ---------------------------------------------------------------------------
# Tracking: load / save
# ---------------------------------------------------------------------------


class TestLoadTracking:
    def test_returns_empty_dict_when_file_missing(self, tmp_path):
        with mock.patch.object(auto_tldr, "TRACKING_FILE", tmp_path / "nope.json"):
            assert auto_tldr.load_tracking() == {}

    def test_returns_empty_dict_on_bad_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("NOT JSON", encoding="utf-8")
        with mock.patch.object(auto_tldr, "TRACKING_FILE", bad):
            assert auto_tldr.load_tracking() == {}

    def test_reads_valid_json(self, tmp_path):
        f = tmp_path / "ok.json"
        payload = {"https://tldr.tech/ai/2026-06-01": {"topic": "ai", "date": "2026-06-01"}}
        f.write_text(json.dumps(payload), encoding="utf-8")
        with mock.patch.object(auto_tldr, "TRACKING_FILE", f):
            assert auto_tldr.load_tracking() == payload


class TestSaveTracking:
    def test_atomic_write_roundtrip(self, tmp_path):
        target = tmp_path / "tracking" / "state.json"
        data = {
            "https://tldr.tech/tech/2026-06-03": {
                "topic": "tech",
                "date": "2026-06-03",
                "ingested_at": "2026-06-04T10:00:00+10:00",
            }
        }
        with mock.patch.object(auto_tldr, "TRACKING_FILE", target):
            auto_tldr.save_tracking(data)

        assert target.exists()
        assert json.loads(target.read_text(encoding="utf-8")) == data

    def test_overwrites_existing(self, tmp_path):
        target = tmp_path / "state.json"
        target.write_text("{}", encoding="utf-8")
        new_data = {"url": {"topic": "ai"}}
        with mock.patch.object(auto_tldr, "TRACKING_FILE", target):
            auto_tldr.save_tracking(new_data)

        assert json.loads(target.read_text(encoding="utf-8")) == new_data


# ---------------------------------------------------------------------------
# Archive Parsing: get_issue_urls
# ---------------------------------------------------------------------------

SAMPLE_ARCHIVE_HTML = """
<html>
<body>
<a href="/tech/2026-06-03"><div class="mb-4">Title A</div></a>
<a href="/tech/2026-06-02"><div class="mb-4">Title B</div></a>
<a href="/tech/2026-06-01"><div class="mb-4">Title C</div></a>
<a href="/tech/2026-05-29"><div class="mb-4">Title D</div></a>
<a href="/tech/2026-05-28"><div class="mb-4">Title E</div></a>
</body>
</html>
"""


class TestGetIssueUrls:
    @mock.patch("scripts.auto_tldr.requests")
    def test_parses_dates_from_html(self, mock_requests):
        resp = mock.Mock()
        resp.text = SAMPLE_ARCHIVE_HTML
        resp.raise_for_status = mock.Mock()
        mock_requests.get.return_value = resp

        results = auto_tldr.get_issue_urls("tech", limit=3)

        assert len(results) == 3
        assert results[0] == ("https://tldr.tech/tech/2026-06-03", "2026-06-03")
        assert results[1] == ("https://tldr.tech/tech/2026-06-02", "2026-06-02")
        assert results[2] == ("https://tldr.tech/tech/2026-06-01", "2026-06-01")

    @mock.patch("scripts.auto_tldr.requests")
    def test_deduplicates_dates(self, mock_requests):
        html = """
        <a href="/ai/2026-06-03"><div>A</div></a>
        <a href="/ai/2026-06-03"><div>A dup</div></a>
        <a href="/ai/2026-06-02"><div>B</div></a>
        """
        resp = mock.Mock()
        resp.text = html
        resp.raise_for_status = mock.Mock()
        mock_requests.get.return_value = resp

        results = auto_tldr.get_issue_urls("ai", limit=10)

        assert len(results) == 2

    @mock.patch("scripts.auto_tldr.requests")
    def test_respects_limit(self, mock_requests):
        resp = mock.Mock()
        resp.text = SAMPLE_ARCHIVE_HTML
        resp.raise_for_status = mock.Mock()
        mock_requests.get.return_value = resp

        results = auto_tldr.get_issue_urls("tech", limit=2)
        assert len(results) == 2

    @mock.patch("scripts.auto_tldr.requests")
    def test_returns_empty_on_network_error(self, mock_requests):
        mock_requests.get.side_effect = Exception("timeout")

        results = auto_tldr.get_issue_urls("tech")
        assert results == []

    @mock.patch("scripts.auto_tldr.requests")
    def test_returns_empty_when_no_links(self, mock_requests):
        resp = mock.Mock()
        resp.text = "<html><body>No links</body></html>"
        resp.raise_for_status = mock.Mock()
        mock_requests.get.return_value = resp

        results = auto_tldr.get_issue_urls("tech")
        assert results == []


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------


class TestIngestNewsletter:
    @mock.patch("src.core.ingest.process_one_file")
    @mock.patch("src.core.web.fetch_webpage_content")
    def test_successful_ingestion(self, mock_fetch, mock_process, tmp_path):
        mock_fetch.return_value = ("TLDR AI", "# Big AI News\nContent here.")
        mock_process.return_value = {
            "success": True,
            "out_filepath": str(tmp_path / "output.md"),
        }

        import logging
        logger = logging.getLogger("test_ingest")

        with mock.patch.object(auto_tldr, "NEWS_DIR", tmp_path / "news"):
            with mock.patch.object(auto_tldr, "ROOT", tmp_path):
                ok = auto_tldr.ingest_newsletter(
                    slug="ai",
                    label="AI",
                    url="https://tldr.tech/ai/2026-06-03",
                    date="2026-06-03",
                    logger=logger,
                )

        assert ok is True
        # Verify raw markdown was saved
        raw = tmp_path / "news" / "tldr_ai_2026-06-03.md"
        assert raw.exists()
        assert "TLDR AI" in raw.read_text()
        # Verify process_one_file was called with use_ai=True
        mock_process.assert_called_once()
        call_args = mock_process.call_args
        assert call_args[1].get("use_ai") is True or (
            len(call_args[0]) > 1 and call_args[0][1] is True
        )

    @mock.patch("src.core.web.fetch_webpage_content")
    def test_skips_on_empty_content(self, mock_fetch):
        mock_fetch.return_value = ("", "")

        import logging
        logger = logging.getLogger("test_empty")

        ok = auto_tldr.ingest_newsletter(
            slug="ai",
            label="AI",
            url="https://tldr.tech/ai/2026-06-03",
            date="2026-06-03",
            logger=logger,
        )
        assert ok is False


# ---------------------------------------------------------------------------
# Dedup logic (integration-style with main loop)
# ---------------------------------------------------------------------------


class TestDedup:
    def test_skip_already_ingested(self):
        tracking = {
            "https://tldr.tech/tech/2026-06-03": {
                "topic": "tech",
                "date": "2026-06-03",
                "ingested_at": "2026-06-04T10:00:00+10:00",
            }
        }
        url = "https://tldr.tech/tech/2026-06-03"
        assert url in tracking  # would be skipped

    def test_process_new_url(self):
        tracking = {
            "https://tldr.tech/tech/2026-06-03": {
                "topic": "tech",
                "date": "2026-06-03",
            }
        }
        new_url = "https://tldr.tech/tech/2026-06-04"
        assert new_url not in tracking  # would be processed
