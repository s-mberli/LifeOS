"""
Persona-based tests for Developer Dan.

Developer Dan is a chat-first user who selects an expert (e.g. "Ali Abdaal")
and expects them to adopt their correct tone, playbook rules, and principles
as "Hot Memory" (system prompt), while searching and referencing evidence files
as "Vault Memory" (user prompt / RAG context).
"""
import sys
from pathlib import Path

import pytest

# Ensure scripts and ui folders are in python path
ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT / "apps" / "streamlit-chat"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(UI_DIR) not in sys.path:
    sys.path.insert(0, str(UI_DIR))

from ui.helpers import construct_chat_prompts


@pytest.fixture
def expert_fixture(tmp_project: Path) -> dict:
    """Create an expert with profile, playbook, principles, and evidence."""
    expert_dir = tmp_project / "data" / "experts" / "expert--dan-helper"
    expert_dir.mkdir(parents=True)
    
    (expert_dir / "profile.md").write_text(
        "### Profile\n"
        "Name: Dan Helper\n"
        "Role: Software consultant.\n",
        encoding="utf-8",
    )
    (expert_dir / "playbook.md").write_text(
        "### Playbook\n"
        "Rule 1: Always be concise.\n"
        "Rule 2: Speak like a caveman.\n",
        encoding="utf-8",
    )
    (expert_dir / "principles.md").write_text(
        "### Principles\n"
        "1. Extreme clarity.\n",
        encoding="utf-8",
    )
    (expert_dir / "evidence.md").write_text(
        "### Evidence Log\n"
        "- 2026-05-24: Fixed production database latency bug by indexing ID.\n",
        encoding="utf-8",
    )
    
    return {
        "slug": "expert--dan-helper",
        "display_name": "Dan Helper",
    }


def test_persona_dan_prompts_separation(tmp_project: Path, expert_fixture: dict):
    """Verify system_prompt contains behavior files (Hot) and user_prompt contains evidence (Vault)."""
    options_map = {
        "Expert: Dan Helper": {"type": "expert", "data": expert_fixture}
    }
    
    fts_results = [
        ("FTS Result Note", "data/knowledge/fts-note.md", "Found something in FTS index", 0.5)
    ]
    
    system_prompt, user_prompt = construct_chat_prompts(
        target_expert=expert_fixture,
        prompt="How do I fix database latency?",
        selected_scopes=["Expert: Dan Helper"],
        options_map=options_map,
        fts_results=fts_results,
        root_dir=tmp_project,
    )
    
    # 1. Check Tier 1 (Hot Memory / System Prompt)
    assert "You are LifeOS operating as the expert: Dan Helper." in system_prompt
    assert "Always be concise." in system_prompt  # From playbook.md
    assert "Extreme clarity." in system_prompt   # From principles.md
    assert "Software consultant." in system_prompt # From profile.md
    
    # Behavior files should NOT be in user_prompt (to save tokens and prevent confusion)
    assert "Always be concise." not in user_prompt
    assert "Extreme clarity." not in user_prompt
    
    # 2. Check Tier 2 (Vault Memory / User Prompt)
    assert "Fixed production database latency bug" in user_prompt  # From evidence.md
    assert "FTS Result Note" in user_prompt
    assert "How do I fix database latency?" in user_prompt
