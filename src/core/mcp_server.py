import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Ensure we can import from src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.core.search_knowledge import fts_search

# Create the FastMCP server
mcp = FastMCP("MarkusOS")

@mcp.tool()
def search_vault(query: str, limit: int = 5) -> str:
    """
    Search the local MarkusOS knowledge vault (SQLite FTS database).
    Returns a list of architectural rules, snippets, and documents matching the query.
    """
    results = fts_search(query, limit)
    if not results:
        return f"No results found for: '{query}'"
    
    formatted = []
    for idx, (title, path, snippet, score) in enumerate(results, 1):
        formatted.append(f"Result {idx}:\nTitle: {title}\nPath: {path}\nScore: {score:.4f}\nSnippet: {snippet.strip()}\n")
    
    return "\n" + "-"*40 + "\n" + "\n".join(formatted)

@mcp.tool()
def read_vault_file(path: str) -> str:
    """
    Read the full content of a file from the vault (relative to the MarkusOS root).
    """
    full_path = BASE_DIR / path
    if not full_path.is_file():
        return f"Error: File not found at {path}"
    
    # Simple check to avoid reading huge binary files
    if full_path.suffix.lower() in [".db", ".sqlite", ".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav"]:
        return f"Error: Cannot read binary file type {full_path.suffix}"

    try:
        return full_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

if __name__ == "__main__":
    mcp.run()
