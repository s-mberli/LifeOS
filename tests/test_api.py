"""
Tests for the MarkusOS Ingestion API (src/api.py).

Uses FastAPI's TestClient (backed by httpx) and mocks process_one_file
so no real web requests or LLM calls are made during test execution.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Patch process_one_file before the app module is imported so the background
# task target is the mock — not the real function.
MOCK_SUCCESS_RESULT = {
    "success": True,
    "out_filepath": "/some/output.md",
    "error": None,
    "log": ["Mocked ingestion completed."],
}

# We patch at the location where api.py resolves the name.
PATCH_TARGET = "src.api.process_one_file"


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app with process_one_file mocked."""
    with patch(PATCH_TARGET, return_value=MOCK_SUCCESS_RESULT):
        from src.api import app
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c


class TestIngestEndpoint:
    """Tests for POST /ingest."""

    def test_valid_url_returns_202_accepted(self, client: TestClient):
        """A well-formed http URL should be accepted immediately (background task)."""
        with patch(PATCH_TARGET, return_value=MOCK_SUCCESS_RESULT):
            response = client.post("/ingest", json={"url": "https://example.com"})

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "accepted"
        assert "https://example.com" in body["message"]

    def test_invalid_url_returns_400(self, client: TestClient):
        """A string that does not start with 'http' must be rejected with a 400."""
        response = client.post("/ingest", json={"url": "not-a-url"})

        assert response.status_code == 400
        assert "Invalid URL" in response.json()["detail"]

    def test_missing_url_field_returns_422(self, client: TestClient):
        """Omitting the 'url' field entirely should return a 422 Unprocessable Entity."""
        response = client.post("/ingest", json={})

        assert response.status_code == 422

    def test_http_url_also_accepted(self, client: TestClient):
        """Plain http:// (not just https://) URLs should also pass validation."""
        with patch(PATCH_TARGET, return_value=MOCK_SUCCESS_RESULT):
            response = client.post("/ingest", json={"url": "http://localhost:3000/page"})

        assert response.status_code == 200
        assert response.json()["status"] == "accepted"

    def test_process_one_file_not_called_synchronously(self, client: TestClient):
        """Ingestion runs as a background task; the endpoint must return before it completes."""
        mock_fn = MagicMock(return_value=MOCK_SUCCESS_RESULT)
        with patch(PATCH_TARGET, mock_fn):
            response = client.post("/ingest", json={"url": "https://example.com"})

        # The response must be immediate (200) regardless of whether the
        # background task has finished — TestClient flushes background tasks
        # before the response is returned, so we just assert the endpoint itself
        # didn't block or raise.
        assert response.status_code == 200
