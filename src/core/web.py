"""
scripts/core/web.py — Web content fetching utilities for LifeOS.

Fetches page titles and body text from arbitrary URLs using the
``requests`` + ``beautifulsoup4`` stack.  Both packages are treated as
optional; graceful degradation occurs when they are not installed.
"""

from __future__ import annotations

import ipaddress
import socket
from contextlib import contextmanager
from contextvars import ContextVar
from urllib.parse import urljoin, urlsplit

_clipper_ingestion = ContextVar("clipper_ingestion", default=False)
_MAX_RESPONSE_BYTES = 2_000_000


@contextmanager
def clipper_ingestion():
    """Keep browser execution out of the API's untrusted URL path."""
    token = _clipper_ingestion.set(True)
    try:
        yield
    finally:
        _clipper_ingestion.reset(token)


def validate_public_url(url: str, *, resolve: bool = False) -> str:
    """Reject non-web, local, and non-public destinations before fetching."""
    if not isinstance(url, str) or url != url.strip() or "\\" in url or any(ord(c) < 33 for c in url):
        raise ValueError("Invalid URL format.")
    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Invalid URL format.") from exc
    if parsed.scheme.lower() not in {"http", "https"} or not host or parsed.username or parsed.password:
        raise ValueError("Invalid URL format.")
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("Invalid URL format.")
    host = host.rstrip(".").lower()
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        if not host or "." not in host or host.endswith((".localhost", ".local", ".internal")):
            raise ValueError("Private URL target.")
        if not all(part and part.replace("-", "").isalnum() for part in host.split(".")):
            raise ValueError("Invalid URL format.")
        addresses = []
    if resolve and not addresses:
        addresses = _resolve_addresses(host, port or (443 if parsed.scheme.lower() == "https" else 80))
    if any(not address.is_global for address in addresses):
        raise ValueError("Private URL target.")
    return url


def _resolve_addresses(host: str, port: int) -> list[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    try:
        addresses = [ipaddress.ip_address(item[4][0]) for item in socket.getaddrinfo(host, port)]
    except (OSError, ValueError) as exc:
        raise ValueError("URL host could not be resolved.") from exc
    if not addresses:
        raise ValueError("URL host could not be resolved.")
    if any(not address.is_global for address in addresses):
        raise ValueError("Private URL target.")
    return addresses


def _public_get(url: str, *, headers: dict | None = None, timeout: int = 15):
    """Fetch through a validated, pinned public IP with bounded response bytes."""
    import requests
    import urllib3

    for _ in range(6):
        validate_public_url(url)
        parsed = urlsplit(url)
        host = parsed.hostname.rstrip(".").lower()
        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = _resolve_addresses(host, port)[0]
        else:
            if not address.is_global:
                raise ValueError("Private URL target.")

        pool_class = urllib3.HTTPSConnectionPool if parsed.scheme.lower() == "https" else urllib3.HTTPConnectionPool
        pool_options = {"assert_hostname": host, "server_hostname": host} if parsed.scheme.lower() == "https" else {}
        pool = pool_class(str(address), port=port, **pool_options)
        request_headers = dict(headers or {})
        request_headers["Host"] = parsed.netloc
        target = parsed.path or "/"
        if parsed.query:
            target += "?" + parsed.query
        try:
            raw = pool.request(
                "GET", target, headers=request_headers, timeout=urllib3.Timeout(total=timeout),
                redirect=False, retries=False, preload_content=False,
            )
            try:
                response = requests.Response()
                response.status_code = raw.status
                response.headers.update(raw.headers)
                response.url = url
                if raw.status in {301, 302, 303, 307, 308} and raw.headers.get("Location"):
                    response._content = b""
                else:
                    if int(raw.headers.get("Content-Length", 0)) > _MAX_RESPONSE_BYTES:
                        raise ValueError("Web response exceeds size limit.")
                    body = raw.read(_MAX_RESPONSE_BYTES + 1, decode_content=True)
                    if len(body) > _MAX_RESPONSE_BYTES:
                        raise ValueError("Web response exceeds size limit.")
                    response._content = body
            finally:
                raw.release_conn()
        finally:
            pool.close()
        if response.status_code not in {301, 302, 303, 307, 308}:
            return response
        location = response.headers.get("Location")
        if not location:
            return response
        url = urljoin(url, location)
    raise ValueError("Too many URL redirects.")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_reddit_json(url: str) -> tuple[str, str]:
    """Fetch a Reddit thread via its native JSON endpoint and build a structured Markdown comment tree.

    Args:
        url: The Reddit URL.

    Returns:
        A tuple of (title, markdown_content).
    """
    try:
        import requests
    except ImportError:
        return "", ""

    try:
        clean_url = url.split("?")[0].rstrip("/")
        json_url = clean_url + ".json"
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = _public_get(json_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        if not isinstance(data, list) or len(data) < 2:
            return "", ""

        post_list = data[0].get("data", {}).get("children", [])
        if not post_list:
            return "", ""
        
        post_data = post_list[0].get("data", {})
        title = post_data.get("title", "Reddit Thread").strip()
        author = post_data.get("author", "[deleted]")
        subreddit = post_data.get("subreddit", "unknown")
        score = post_data.get("score", 0)
        selftext = post_data.get("selftext", "")

        md = []
        md.append(f"# {title}")
        md.append(f"Posted by u/{author} in r/{subreddit} (Score: {score})")
        md.append("")
        if selftext:
            md.append(selftext)
            md.append("")
        md.append("## Comments")
        md.append("")

        def format_comment(comment_node: dict, depth: int, max_depth: int = 3) -> list[str]:
            if depth > max_depth:
                return []
            c_data = comment_node.get("data", {})
            if not c_data:
                return []
            
            c_author = c_data.get("author", "[deleted]")
            c_body = c_data.get("body", "")
            c_score = c_data.get("score", 0)
            
            lines = []
            prefix = "> " * depth
            lines.append(f"{prefix}**u/{c_author}** ({c_score} points):")
            for line in c_body.splitlines():
                lines.append(f"{prefix}{line}")
            lines.append(prefix)
            
            replies = c_data.get("replies")
            if isinstance(replies, dict):
                children = replies.get("data", {}).get("children", [])
                for child in children:
                    if child.get("kind") == "t1":
                        lines.extend(format_comment(child, depth + 1, max_depth))
            return lines

        comments_list = data[1].get("data", {}).get("children", [])
        thread_count = 0
        for child in comments_list:
            if child.get("kind") == "t1":
                md.extend(format_comment(child, depth=1))
                thread_count += 1
                if thread_count >= 30:
                    break

        return title, "\n".join(md)
    except Exception as exc:
        print(f"  [!] Failed to parse Reddit json for {url}: {exc}")
        return "", ""


def fetch_jina_reader(url: str) -> tuple[str, str]:
    """Fetch webpage content as clean markdown via the Jina Reader API.

    Args:
        url: The URL to fetch.

    Returns:
        A tuple of (title, markdown_content).
    """
    try:
        import requests
    except ImportError:
        return "", ""

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        jina_url = f"https://r.jina.ai/{url}"
        validate_public_url(url, resolve=True)
        response = _public_get(jina_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        title = response.headers.get("X-Title", "").strip()
        content = response.text.strip()
        
        if not title:
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
                if line.startswith("Title: "):
                    title = line[7:].strip()
                    break

        return title, content
    except Exception as exc:
        # Silently fail — Playwright is primary fetcher now
        return "", ""


def _fetch_webpage_content_bs4(url: str) -> tuple[str, str]:
    """Fetch webpage using Playwright (headless Chromium) — bypasses most bot blocks."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [!] playwright not installed. Run: pip install playwright && playwright install chromium")
        return "", ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1280, 'height': 720},
            )
            page = context.new_page()
            page.goto(url, timeout=15000, wait_until='domcontentloaded')
            page.wait_for_timeout(2000)  # Let JS render

            title = page.title()

            # Remove junk elements
            page.evaluate("""() => {
                for (const el of document.querySelectorAll('script, style, nav, footer, header, aside, .ad, .ads, .cookie, .popup, .modal, [role=banner], [role=complementary]')) {
                    el.remove();
                }
            }""")

            content = page.inner_text('body')
            browser.close()

            if not content or len(content.strip()) < 100:
                return "", ""

            return title.strip(), content.strip()
    except Exception as exc:
        # Silent fail
        return "", ""


def _fetch_public_text(url: str) -> tuple[str, str]:
    """Read clipper pages without executing scripts or loading subresources."""
    try:
        from bs4 import BeautifulSoup

        response = _public_get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        for element in soup.select("script, style, nav, footer, header, aside"):
            element.decompose()
        return title, soup.get_text(" ", strip=True)
    except Exception:
        return "", ""


def fetch_tldr_direct(url: str) -> tuple[str, str]:
    """Fetch TLDR newsletter content directly via BeautifulSoup (extremely fast)."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return "", ""

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = _public_get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title_el = soup.find("title")
        title = title_el.get_text().strip() if title_el else "TLDR Newsletter"

        # Extract articles
        articles = soup.find_all("article")
        if not articles:
            return "", ""

        content_parts = []
        for art in articles:
            # Preserve original article URLs by converting <a> tags to Markdown
            for a in art.find_all("a"):
                href = a.get("href", "")
                text = a.get_text(strip=True)
                if href and text:
                    a.replace_with(f"[{text}]({href})")

            text = art.get_text(separator=" ").strip()
            if text:
                content_parts.append(text)

        return title, "\n\n".join(content_parts)
    except Exception as exc:
        print(f"  [!] Direct TLDR fetch failed for {url}: {exc}")
        return "", ""


def fetch_webpage_content(url: str) -> tuple[str, str]:
    """Fetch a web page and return its title and main text content.

    Args:
        url: The URL to fetch.

    Returns:
        A tuple of ``(title, content_text)``. Both strings may be empty if
        the request fails.
    """
    validate_public_url(url, resolve=True)
    lower_url = url.lower()
    
    import urllib.parse
    parsed = urllib.parse.urlparse(lower_url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    
    # 0. TLDR specific fast path
    if "tldr.tech" in hostname and "/archives" not in path:
        title, content = fetch_tldr_direct(url)
        if title or content:
            return title, content

    # 1. Reddit routing
    if "reddit.com" in hostname or "redd.it" in hostname:
        title, content = fetch_reddit_json(url)
        if title or content:
            return title, content

    # 2. Try direct fetch first (faster on VPS, works for most sites)
    title, content = _fetch_public_text(url) if _clipper_ingestion.get() else _fetch_webpage_content_bs4(url)
    if title or content:
        return title, content

    # 3. Fallback to Jina Reader API
    title, content = fetch_jina_reader(url)
    if title or content:
        return title, content

    return "", ""



def fetch_webpage_metadata(url: str) -> dict:
    """Fetch basic metadata (title, description) from a web page.

    Args:
        url: The URL to fetch.

    Returns:
        Dict with keys ``title`` and ``description``.  Values may be empty.
    """
    try:
        import requests  # type: ignore
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        print(
            "  [!] 'requests' or 'beautifulsoup4' not installed. "
            "Web metadata extraction unavailable."
        )
        return {"title": "", "description": ""}

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = _public_get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()

        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if not description and og_desc and og_desc.get("content"):
            description = og_desc["content"].strip()

        return {"title": title, "description": description}
    except Exception as exc:
        print(f"  [!] Failed to fetch webpage metadata from {url}: {exc}")
        return {"title": "", "description": ""}
