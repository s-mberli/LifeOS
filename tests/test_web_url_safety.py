"""The clipper must not fetch local addresses or unbounded page bodies."""

from unittest.mock import Mock, patch

import pytest

from src.core import web


def public_dns(host, port):
    return [(2, 1, 6, "", ("93.184.215.14", port))]


def fake_raw(status=200, headers=None, body=b"okay"):
    raw = Mock(status=status, headers=headers or {})
    raw.read.return_value = body
    return raw


def test_public_get_pins_validated_ip_and_preserves_https_identity():
    raw = fake_raw()
    pool = Mock()
    pool.request.return_value = raw
    with patch("src.core.web.socket.getaddrinfo", side_effect=public_dns) as dns, \
         patch("urllib3.HTTPSConnectionPool", return_value=pool) as pool_factory:
        response = web._public_get("https://example.com/article", timeout=5)
    assert response.text == "okay"
    dns.assert_called_once()
    pool_factory.assert_called_once_with("93.184.215.14", port=443, assert_hostname="example.com", server_hostname="example.com")
    assert pool.request.call_args.kwargs["headers"]["Host"] == "example.com"
    assert pool.request.call_args.kwargs["redirect"] is False
    assert pool.request.call_args.kwargs["preload_content"] is False
    raw.release_conn.assert_called_once()
    pool.close.assert_called_once()


def test_public_get_rejects_redirect_to_metadata_without_second_connection():
    raw = fake_raw(status=302, headers={"Location": "http://169.254.169.254/latest/meta-data/"})
    pool = Mock()
    pool.request.return_value = raw
    with patch("src.core.web.socket.getaddrinfo", side_effect=public_dns), \
         patch("urllib3.HTTPSConnectionPool", return_value=pool), \
         patch("urllib3.HTTPConnectionPool") as http_pool:
        with pytest.raises(ValueError, match="Private URL"):
            web._public_get("https://example.com/article", timeout=5)
    pool.request.assert_called_once()
    http_pool.assert_not_called()


def test_public_get_rejects_private_dns_answer_after_public_precheck():
    answers = [public_dns("public.example", 443), [(2, 1, 6, "", ("127.0.0.1", 443))]]
    with patch("src.core.web.socket.getaddrinfo", side_effect=answers), \
         patch("urllib3.HTTPSConnectionPool") as pool:
        web.validate_public_url("https://public.example/article", resolve=True)
        with pytest.raises(ValueError, match="Private URL"):
            web._public_get("https://public.example/article")
    pool.assert_not_called()


def test_public_get_rejects_body_above_cap_before_materializing_text():
    raw = fake_raw(body=b"x" * (web._MAX_RESPONSE_BYTES + 1))
    pool = Mock()
    pool.request.return_value = raw
    with patch("src.core.web.socket.getaddrinfo", side_effect=public_dns), \
         patch("urllib3.HTTPSConnectionPool", return_value=pool):
        with pytest.raises(ValueError, match="size limit"):
            web._public_get("https://example.com/large")
    raw.read.assert_called_once_with(web._MAX_RESPONSE_BYTES + 1, decode_content=True)
    raw.release_conn.assert_called_once()
    pool.close.assert_called_once()


def test_clipper_fetch_does_not_launch_browser_or_load_subresources():
    html = b"<html><head><title>Article</title></head><body><script src='http://127.0.0.1/x'></script><p>Public text</p></body></html>"
    raw = fake_raw(body=html)
    pool = Mock()
    pool.request.return_value = raw
    with patch("src.core.web.socket.getaddrinfo", side_effect=public_dns), \
         patch("urllib3.HTTPSConnectionPool", return_value=pool), \
         patch("src.core.web._fetch_webpage_content_bs4") as browser:
        with web.clipper_ingestion():
            title, content = web.fetch_webpage_content("https://example.com/article")
    assert (title, content) == ("Article", "Article Public text")
    browser.assert_not_called()
    pool.request.assert_called_once()


def test_public_redirect_chain_is_allowed():
    raws = [fake_raw(status=302, headers={"Location": "/new"}), fake_raw()]
    pool = Mock()
    pool.request.side_effect = raws
    with patch("src.core.web.socket.getaddrinfo", side_effect=public_dns), \
         patch("urllib3.HTTPSConnectionPool", return_value=pool):
        response = web._public_get("https://example.com/old")
    assert response.url == "https://example.com/new"
    assert pool.request.call_count == 2
    assert pool.request.call_args.args[:2] == ("GET", "/new")
