import sqlite3

import pytest
from src.core import search_knowledge
from src.core import mcp_server
from src.core.mcp_server import search_vault, read_vault_file

def test_mcp_search_vault(tmp_path, monkeypatch):
    note = tmp_path / "data" / "knowledge" / "test_rule.md"
    note.parent.mkdir(parents=True)
    note.write_text("This is a test note")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
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
    assert "Error: Security violation" in result


def test_mcp_search_filters_sensitive_results_before_formatting(tmp_path, monkeypatch):
    allowed = tmp_path / "data" / "experts" / "profile.md"
    allowed.parent.mkdir(parents=True)
    allowed.write_text("Expert profile")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    rows = [
        ("SECRET TITLE", "data/business/secret.md", "SECRET SNIPPET", -2.0),
        ("Private", "data/private/note.md", "PRIVATE SNIPPET", -1.0),
        ("Expert", "data/experts/profile.md", "Safe snippet", -0.5),
    ]
    monkeypatch.setattr("src.core.mcp_server.fts_search", lambda q, l, **kw: rows)

    result = search_vault("topic", limit=1)

    assert "Path: data/experts/profile.md" in result
    assert "Safe snippet" in result
    assert "SECRET" not in result
    assert "PRIVATE" not in result


def test_mcp_search_finds_allowed_result_beyond_50_disallowed_hits(tmp_path, monkeypatch):
    db_path = tmp_path / "search.db"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE VIRTUAL TABLE search_index USING fts5(path, title, content)")
    conn.executemany(
        "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
        [(f"data/business/secret-{i}.md", f"SECRET {i}", "needle " * 10)
         for i in range(50)],
    )
    conn.execute(
        "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
        ("data/knowledge/allowed.md", "Allowed", "needle"),
    )
    conn.commit()
    conn.close()
    note = tmp_path / "data" / "knowledge" / "allowed.md"
    note.parent.mkdir(parents=True)
    note.write_text("needle")
    monkeypatch.setattr(search_knowledge, "DB_PATH", db_path)
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)

    unfiltered = search_knowledge.fts_search("needle", 50)
    assert len(unfiltered) == 50
    assert all(path.startswith("data/business/") for _, path, _, _ in unfiltered)

    result = search_vault("needle")
    assert "Path: data/knowledge/allowed.md" in result
    assert "SECRET" not in result


def test_fts_prefix_filter_accepts_windows_style_index_path(tmp_path, monkeypatch):
    db_path = tmp_path / "search.db"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE VIRTUAL TABLE search_index USING fts5(path, title, content)")
    conn.execute(
        "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
        (r"data\experts\profile.md", "Expert", "needle"),
    )
    conn.commit()
    conn.close()
    monkeypatch.setattr(search_knowledge, "DB_PATH", db_path)

    rows = search_knowledge.fts_search("needle", allowed_prefixes=("data/experts/",))
    assert [path for _, path, _, _ in rows] == [r"data\experts\profile.md"]


@pytest.mark.parametrize("path", [
    "data/private/note.md", "data/inbox/note.md", "data/business/note.md",
    "data/career/note.md", "outputs/note.md", "knowledge/note.md",
    "data/knowledge/raw/transcript.md", "data/knowledge/../private/note.md",
    "data/knowledge/hidden/.env.md", "data/knowledge/note.db",
])
def test_mcp_read_blocks_non_curated_paths(tmp_path, monkeypatch, path):
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    assert "Error: Security violation" in read_vault_file(path)


def test_mcp_read_blocks_absolute_path(tmp_path, monkeypatch):
    note = tmp_path / "data" / "knowledge" / "note.md"
    note.parent.mkdir(parents=True)
    note.write_text("Safe")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    assert "Error: Security violation" in read_vault_file(str(note))


def test_mcp_read_and_search_block_raw_case_alias(tmp_path, monkeypatch):
    transcript = tmp_path / "data" / "knowledge" / "RAW" / "transcript.md"
    transcript.parent.mkdir(parents=True)
    transcript.write_text("SECRET")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    monkeypatch.setattr("src.core.mcp_server.fts_search", lambda q, l, **kw: [
        ("Transcript", "data/knowledge/RAW/transcript.md", "SECRET", -1.0)
    ])

    assert "Error: Security violation" in read_vault_file("data/knowledge/RAW/transcript.md")
    assert "SECRET" not in search_vault("topic")


def test_mcp_read_and_search_block_symlink_escape(tmp_path, monkeypatch):
    outside = tmp_path / "data" / "private" / "secret.md"
    outside.parent.mkdir(parents=True)
    outside.write_text("SECRET")
    link = tmp_path / "data" / "knowledge" / "link.md"
    link.parent.mkdir(parents=True)
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation unavailable")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    monkeypatch.setattr("src.core.mcp_server.fts_search", lambda q, l, **kw: [
        ("Secret", "data/knowledge/link.md", "SECRET", -1.0)
    ])

    assert "Error: Security violation" in read_vault_file("data/knowledge/link.md")
    assert "SECRET" not in search_vault("topic")


def test_mcp_read_rejects_symlinked_collection(tmp_path, monkeypatch):
    collection = tmp_path / "data" / "knowledge"
    collection.mkdir(parents=True)
    (collection / "note.md").write_text("Sensitive")
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    original_is_symlink = type(collection).is_symlink
    monkeypatch.setattr(type(collection), "is_symlink", lambda self: self == collection or original_is_symlink(self))

    assert "Error: Security violation" in read_vault_file("data/knowledge/note.md")


def test_mcp_read_rejects_oversized_file(tmp_path, monkeypatch):
    note = tmp_path / "data" / "knowledge" / "large.md"
    note.parent.mkdir(parents=True)
    note.write_bytes(b"x" * (64 * 1024 + 1))
    monkeypatch.setattr("src.core.mcp_server.BASE_DIR", tmp_path)
    assert "read limit" in read_vault_file("data/knowledge/large.md")


def test_mcp_search_rejects_excessive_limit(monkeypatch):
    monkeypatch.setattr("src.core.mcp_server.fts_search", lambda *a, **kw: pytest.fail("FTS called"))
    assert "Limit must be between" in search_vault("topic", limit=100)


def test_isolated_deida_search_and_private_path_denial(tmp_path, monkeypatch):
    note = tmp_path / "data" / "knowledge" / "david-deida" / "presence.md"
    note.parent.mkdir(parents=True)
    note.write_text("Title: Staying present\nSource URL: https://example.org/deida-ch2\n"
                    "Source idea: Open the heart when hurt; keep breathing and present.")
    other = tmp_path / "data" / "knowledge" / "other" / "secret.md"
    other.parent.mkdir(parents=True)
    other.write_text("SECRET presence")
    db_path = tmp_path / "indexes" / "lifeos.db"
    db_path.parent.mkdir()
    connection = sqlite3.connect(db_path)
    connection.execute("CREATE VIRTUAL TABLE search_index USING fts5(path, title, content)")
    connection.executemany(
        "INSERT INTO search_index (path, title, content) VALUES (?, ?, ?)",
        [("data/knowledge/david-deida/presence.md", "Staying present", note.read_text()),
         ("data/knowledge/other/secret.md", "Secret", other.read_text())],
    )
    connection.commit()
    connection.close()
    monkeypatch.setattr(mcp_server, "MCP_ROOT", str(tmp_path))
    monkeypatch.setattr(mcp_server, "BASE_DIR", tmp_path)
    monkeypatch.setattr(mcp_server, "SEARCH_PREFIXES", (
        "data/knowledge/david-deida/", "data/experts/expert--david-deida/"))

    result = search_vault("presence")
    assert "Staying present" in result
    assert "https://example.org/deida-ch2" in result
    assert "SECRET" not in result
    assert "Error: Security violation" in read_vault_file("data/knowledge/other/secret.md")
    assert "Error: Security violation" in read_vault_file("data/knowledge/david-deida/../../private/secret.md")
    assert "No results" in search_vault("unobtainium")

