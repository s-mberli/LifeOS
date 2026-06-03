import pytest
from pathlib import Path
from src.core.frontmatter import read_fm, write_fm, update_fm

def test_read_fm_with_frontmatter(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("---\ntitle: Test\ntags:\n  - python\n---\nBody text here.")
    fm, body = read_fm(p)
    assert fm == {"title": "Test", "tags": ["python"]}
    assert body == "\nBody text here."

def test_read_fm_without_frontmatter(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("Just some text.\nNo frontmatter.")
    fm, body = read_fm(p)
    assert fm == {}
    assert body == "Just some text.\nNo frontmatter."

def test_read_fm_malformed(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("---\ntitle: Test\nBody text here.")
    fm, body = read_fm(p)
    assert fm == {}
    assert body == "---\ntitle: Test\nBody text here."

def test_write_fm(tmp_path):
    p = tmp_path / "test.md"
    write_fm(p, {"title": "Test", "draft": True}, "\nBody text.")
    text = p.read_text()
    assert text.startswith("---")
    assert "title: Test\n" in text
    assert "draft: true\n" in text
    assert "---" in text[3:]
    assert text.endswith("\nBody text.")

def test_update_fm_success(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("---\ntitle: Old\ncount: 1\n---\nBody")
    success = update_fm(p, title="New", extra="Added")
    assert success is True
    
    fm, body = read_fm(p)
    assert fm["title"] == "New"
    assert fm["count"] == 1
    assert fm["extra"] == "Added"
    assert body == "\nBody"

def test_update_fm_no_frontmatter(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("No frontmatter")
    success = update_fm(p, title="New")
    assert success is False

def test_update_fm_missing_file(tmp_path):
    p = tmp_path / "missing.md"
    success = update_fm(p, title="New")
    assert success is False
