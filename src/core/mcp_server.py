import os
import sys
import time
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Ensure we can import from src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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
    if len(query) > 500:
        logger.warning("search_vault input validation failed: query too long")
        return "Error: Query length exceeds maximum allowed length of 500 characters."

    logger.info(f"search_vault called with query='{query}', limit={limit}")
    
    try:
        # Security: Force include_private=False to prevent external agents from reading private data
        results = fts_search(query, limit, include_private=False)
        if not results:
            return f"No results found for: '{query}'"
        
        formatted = []
        for idx, (title, path, snippet, score) in enumerate(results, 1):
            formatted.append(f"Result {idx}:\nTitle: {title}\nPath: {path}\nScore: {score:.4f}\nSnippet: {snippet.strip()}\n")
        
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
    if len(path) > 1000:
        logger.warning("read_vault_file input validation failed: path too long")
        return "Error: Path length exceeds maximum allowed length of 1000 characters."

    logger.info(f"read_vault_file called for path='{path}'")
    
    try:
        try:
            # Resolve path to prevent directory traversal
            full_path = (BASE_DIR / path).resolve()
            rel_path = full_path.relative_to(BASE_DIR)
        except ValueError:
            return "Error: Security violation. Path must be within the MarkusOS directory."
        except Exception as e:
            logger.error(f"read_vault_file resolution error: {e}")
            return "Error: Internal server error resolving path."

        # Strict access control list
        path_parts = rel_path.parts
        if not path_parts or path_parts[0] != "data":
            return "Error: Security violation. External agents may only access the 'data/' directory."
            
        if len(path_parts) > 1 and path_parts[1] == "private":
            return "Error: Security violation. Access to private data is strictly forbidden."

        if ".env" in full_path.name or ".git" in str(full_path):
            return "Error: Security violation. System files are protected."

        if not full_path.is_file():
            return f"Error: File not found at {path}"
        
        # Simple check to avoid reading huge binary files
        if full_path.suffix.lower() in [".db", ".sqlite", ".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav", ".zip"]:
            return f"Error: Cannot read binary file type {full_path.suffix}"

        return full_path.read_text(encoding="utf-8")
    except Exception as e:
        # Security: Error Sanitization (OWASP LLM06)
        logger.error(f"read_vault_file read error: {e}")
        return "Error: Internal server error occurred while reading the file."

if __name__ == "__main__":
    mcp.run()
