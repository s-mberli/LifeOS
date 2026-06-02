import pytest
from src.core.mcp_server import search_vault, read_vault_file

def test_mcp_search_vault(monkeypatch):
    # Mock fts_search to return a predictable result.
    # Must accept **kwargs because mcp_server passes include_private=False.
    def mock_fts_search(query, limit, **kwargs):
        return [
            ("Test Title", "data/knowledge/test_rule.md", "This is a **test** snippet", -1.234)
        ]
    
    # Patch the function imported inside mcp_server
    monkeypatch.setattr("src.core.mcp_server.fts_search", mock_fts_search)

    result = search_vault("test query", limit=1)
    
    assert "Result 1:" in result
    assert "Title: Test Title" in result
    assert "Path: data/knowledge/test_rule.md" in result
    assert "This is a **test** snippet" in result

def test_mcp_search_vault_no_results(monkeypatch):
    monkeypatch.setattr("src.core.mcp_server.fts_search", lambda q, l, **kw: [])
    result = search_vault("empty", limit=1)
    assert result == "No results found for: 'empty'"

def test_mcp_read_vault_file(tmp_path, monkeypatch):
    # The MCP server restricts access to paths under data/ — create file there.
    data_dir = tmp_path / "data" / "knowledge"
    data_dir.mkdir(parents=True)
    test_file = data_dir / "test_read.md"
    test_file.write_text("Hello MCP")

    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)

    result = read_vault_file("data/knowledge/test_read.md")
    assert result == "Hello MCP"

def test_mcp_read_vault_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    # Path is under data/ (passes security check) but file doesn't exist
    result = read_vault_file("data/knowledge/missing.md")
    assert "Error: File not found" in result

def test_mcp_read_vault_file_binary(tmp_path, monkeypatch):
    data_dir = tmp_path / "data" / "knowledge"
    data_dir.mkdir(parents=True)
    test_file = data_dir / "test.db"
    test_file.write_text("fake binary")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    
    result = read_vault_file("data/knowledge/test.db")
    assert "Error: Cannot read binary file type" in result

