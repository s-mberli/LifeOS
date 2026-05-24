"""
Shared pytest fixtures for LifeOS test suite.

Provides temporary project directory scaffolding and sample data fixtures
that are reused across all test modules.
"""
import pytest
from pathlib import Path


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a minimal LifeOS project directory structure for testing.

    Creates the standard data/, indexes/, config/, and scripts/core/ trees
    inside a pytest-managed temporary directory so tests never touch real data.
    """
    (tmp_path / "data" / "knowledge").mkdir(parents=True)
    (tmp_path / "data" / "experts").mkdir(parents=True)
    (tmp_path / "data" / "inbox" / "raw").mkdir(parents=True)
    (tmp_path / "indexes").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "scripts" / "core").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_insight(tmp_project: Path) -> Path:
    """Create a sample insight note with valid YAML frontmatter.

    Returns the Path to the created note so individual tests can read or
    mutate it without affecting other tests.
    """
    note = tmp_project / "data" / "knowledge" / "test-note.md"
    note.write_text(
        "---\n"
        'title: "Test Note"\n'
        "type: insight_note\n"
        "domain: ai-platform\n"
        'source_url: "https://example.com"\n'
        "tags:\n"
        "  - ai\n"
        "  - test\n"
        "expert_status: unattached\n"
        "attached_experts: []\n"
        "---\n\n"
        "# Test Note\n\nThis is a test note.\n",
        encoding="utf-8",
    )
    return note
