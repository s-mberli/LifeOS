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
        response = requests.get(json_url, headers=headers, timeout=15)
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
        response = requests.get(jina_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        title = response.headers.get("X-Title", "").strip()
        content = response.text.strip()
        
        if not title:
            for line in content.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

        return title, content
    except Exception as exc:
        print(f"  [!] Jina Reader failed for {url}: {exc}")
        return "", ""


def _fetch_webpage_content_bs4(url: str) -> tuple[str, str]:
    """Fallback scraper using requests and BeautifulSoup4."""
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

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        content_text = soup.get_text(separator="\n", strip=True)

        return title, content_text
    except Exception as exc:
        print(f"  [!] Failed to fetch web content from {url} via BeautifulSoup: {exc}")
        return "", ""


def fetch_webpage_content(url: str) -> tuple[str, str]:
    """Fetch a web page and return its title and main text content.

    Args:
        url: The URL to fetch.

    Returns:
        A tuple of ``(title, content_text)``. Both strings may be empty if
        the request fails.
    """
    lower_url = url.lower()
    
    # 1. Reddit routing
    if "reddit.com" in lower_url or "redd.it" in lower_url:
        title, content = fetch_reddit_json(url)
        if title or content:
            return title, content

    # 2. General web page routing (Jina Reader API)
    title, content = fetch_jina_reader(url)
    if title or content:
        return title, content

    # 3. Fallback to BeautifulSoup
    return _fetch_webpage_content_bs4(url)


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
