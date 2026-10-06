import sys
import time
import logging
import os
import re
import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Ensure we can import from src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

MCP_ROOT = os.environ.get("LIFEOS_MCP_ROOT")
if MCP_ROOT:
    # This mode runs from a small, approved copy of the vault. It must not
    # import the general search module, which points at the live vault index.
    BASE_DIR = Path(MCP_ROOT).resolve()
else:
    from src.core.search_knowledge import fts_search

# --- Security: Audit Logging (OWASP LLM06/07) ---
log_path = BASE_DIR / "data" / "private" / "mcp_audit.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(log_path),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp_server")

# --- Security: Rate Limiting (OWASP LLM04) ---
# Simple in-memory token bucket/sliding window for DoS protection
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW_SEC = 60
request_timestamps = []
ALLOWED_COLLECTIONS = {("data", "knowledge"), ("data", "experts")}
SEARCH_PREFIXES = (
    ("data/knowledge/david-deida/", "data/experts/expert--david-deida/")
    if MCP_ROOT else ("data/knowledge/", "data/experts/")
)
MAX_FILE_BYTES = 64 * 1024
MAX_SEARCH_RESULTS = 10
MAX_SEARCH_TEXT = 16 * 1024


def allowed_vault_file(path: str) -> Path | None:
    """Resolve a citable vault path without following links or leaving curated collections."""
    if not path or "\x00" in path:
        return None
    relative = Path(path)
    if relative.is_absolute() or any(part in (".", "..") for part in path.replace("\\", "/").split("/")):
        return None
    parts = relative.parts
    if len(parts) < 3 or parts[:2] not in ALLOWED_COLLECTIONS:
        return None
    if MCP_ROOT and not any(path.replace("\\", "/").startswith(prefix)
                            for prefix in SEARCH_PREFIXES):
        return None
    if any(part.casefold() == "raw" or part.startswith(".") for part in parts[2:]):
        return None
    if relative.suffix.lower() not in {".md", ".txt"}:
        return None

    root = BASE_DIR.resolve()
    candidate = root.joinpath(*parts)
    if any(root.joinpath(*parts[:index]).is_symlink() for index in range(1, len(parts) + 1)):
        return None
    try:
        candidate.resolve().relative_to(root)
    except ValueError:
        return None
    return candidate

def check_rate_limit() -> bool:
    global request_timestamps
    now = time.time()
    # Remove timestamps older than the window
    request_timestamps = [t for t in request_timestamps if now - t < RATE_LIMIT_WINDOW_SEC]
    if len(request_timestamps) >= RATE_LIMIT_REQUESTS:
        return False
    request_timestamps.append(now)
    return True

# Create the FastMCP server
mcp = FastMCP("MarkusOS")


def isolated_fts_search(query: str, limit: int) -> list[tuple]:
    """Search only the index in the approved MCP root, opened read-only."""
    db_path = BASE_DIR / "indexes" / "lifeos.db"
    if ((BASE_DIR / "indexes").is_symlink() or db_path.is_symlink()
            or not db_path.is_file()):
        return []
    tokens = re.findall(r"[\w]+", query.lower())
    if not tokens:
        return []
    # Quoted tokens prevent FTS operators in user input from changing scope.
    match_query = " OR ".join('"' + token.replace('"', '') + '"' for token in tokens[:20])
    connection = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "SELECT title, path, snippet(search_index, 2, '**', '**', '...', 40), "
            "bm25(search_index) FROM search_index WHERE search_index MATCH ? "
            "AND (path LIKE ? OR path LIKE ?) ORDER BY bm25(search_index) LIMIT ?",
            (match_query, *(prefix + "%" for prefix in SEARCH_PREFIXES), limit),
        ).fetchall()
        return rows
    finally:
        connection.close()


def source_url_for(path: Path) -> str:
    """Get the citable URL from an approved note without following a link."""
    with path.open("rb") as source:
        header = source.read(8192).decode("utf-8", errors="replace")
    match = re.search(r"(?im)^(?:source_url|Source URL):\s*['\"]?(https://[^\s'\"]+)", header)
    return match.group(1) if match else ""

@mcp.tool()
def search_vault(query: str, limit: int = 5) -> str:
    """
    Search the local MarkusOS knowledge vault (SQLite FTS database).
    Returns a list of architectural rules, snippets, and documents matching the query.
    """
    if not check_rate_limit():
        logger.warning("search_vault rate limit exceeded")
        return "Error: Rate limit exceeded. Try again later."
        
    # Security: Input Validation (OWASP LLM04/01)
    if not isinstance(query, str) or len(query) > 500:
        logger.warning("search_vault input validation failed: query too long")
        return "Error: Query length exceeds maximum allowed length of 500 characters."
    if type(limit) is not int or not 1 <= limit <= MAX_SEARCH_RESULTS:
        return f"Error: Limit must be between 1 and {MAX_SEARCH_RESULTS}."

    logger.info(f"search_vault called with query='{query}', limit={limit}")
    
    try:
        # Filter collections before the FTS ranking limit, then verify each
        # returned file again before exposing its indexed text.
        results = (isolated_fts_search(query, 50) if MCP_ROOT else
                   fts_search(query, 50, include_private=False, allowed_prefixes=SEARCH_PREFIXES))
        
        formatted = []
        for title, path, snippet, score in results:
            full_path = allowed_vault_file(path) if isinstance(path, str) and len(path) <= 1000 else None
            if (full_path is None or not full_path.is_file()
                    or full_path.stat().st_size > MAX_FILE_BYTES):
                continue
            source_url = source_url_for(full_path)
            entry = (f"Result {len(formatted) + 1}:\nTitle: {str(title)[:300]}\n"
                     f"Path: {path}\nSource URL: {source_url}\nScore: {score:.4f}\n"
                     f"Snippet: {str(snippet).strip()[:2000]}\n")
            if sum(map(len, formatted)) + len(entry) > MAX_SEARCH_TEXT:
                break
            formatted.append(entry)
            if len(formatted) >= limit:
                break
        if not formatted:
            return f"No results found for: '{query}'"
        
        return "\n" + "-"*40 + "\n" + "\n".join(formatted)
    except Exception as e:
        # Security: Error Sanitization (OWASP LLM06)
        logger.error(f"search_vault error: {e}")
        return "Error: Internal server error occurred."

@mcp.tool()
def read_vault_file(path: str) -> str:
    """
    Read the full content of a file from the vault (relative to the MarkusOS root).
    """
    if not check_rate_limit():
        logger.warning("read_vault_file rate limit exceeded")
        return "Error: Rate limit exceeded. Try again later."

    # Security: Input Validation (OWASP LLM04)
    if not isinstance(path, str) or len(path) > 1000:
        logger.warning("read_vault_file input validation failed: path too long")
        return "Error: Path length exceeds maximum allowed length of 1000 characters."

    logger.info(f"read_vault_file called for path='{path}'")
    
    try:
        full_path = allowed_vault_file(path)
        if full_path is None:
            return "Error: Security violation. Path is outside the readable vault collections."

        if not full_path.is_file():
            return f"Error: File not found at {path}"
        
        with full_path.open("rb") as vault_file:
            content = vault_file.read(MAX_FILE_BYTES + 1)
        if len(content) > MAX_FILE_BYTES:
            return f"Error: File exceeds the {MAX_FILE_BYTES}-byte read limit."
        return content.decode("utf-8")
    except Exception as e:
        # Security: Error Sanitization (OWASP LLM06)
        logger.error(f"read_vault_file read error: {e}")
        return "Error: Internal server error occurred while reading the file."

if __name__ == "__main__":
    mcp.run()
