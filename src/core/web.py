"""
scripts/core/web.py — Web content fetching utilities for LifeOS.

Fetches page titles and body text from arbitrary URLs using the
``requests`` + ``beautifulsoup4`` stack.  Both packages are treated as
optional; graceful degradation occurs when they are not installed.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_webpage_content(url: str) -> tuple[str, str]:
    """Fetch a web page and return its title and main text content.

    Args:
        url: The URL to fetch.

    Returns:
        A tuple of ``(title, content_text)``.  Both strings may be empty if
        the request fails or the packages are not installed.
    """
    try:
        import requests  # type: ignore
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        print(
            "  [!] 'requests' or 'beautifulsoup4' not installed. "
            "Web content extraction unavailable."
        )
        return "", ""

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Remove script/style noise before extracting text
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        content_text = soup.get_text(separator="\n", strip=True)

        return title, content_text
    except Exception as exc:
        print(f"  [!] Failed to fetch web content from {url}: {exc}")
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
        response = requests.get(url, headers=headers, timeout=5)
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
