"""
Tests to verify retrieval of elevenlabs_voice_id from expert profiles.
"""
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
    sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

from src.core.experts import get_existing_experts as get_existing_experts_core
from ui.helpers import get_existing_experts as get_existing_experts_ui


def test_core_get_existing_experts_with_voice_id(tmp_project: Path):
    """Verify that get_existing_experts from core loads elevenlabs_voice_id."""
    from src.core.frontmatter import write_fm

    experts_dir = tmp_project / "data" / "experts"
    expert_dir = experts_dir / "expert--test-creator"
    expert_dir.mkdir(parents=True)
    
    # Write profile.md with elevenlabs_voice_id in frontmatter
    profile_path = expert_dir / "profile.md"
    write_fm(
        profile_path,
        {
            "type": "expert_profile",
            "elevenlabs_voice_id": "test_voice_123",
            "insight_count": 0,
        },
        "# Test Profile"
    )

    results = get_existing_experts_core(tmp_project)
    assert len(results) == 1
    assert results[0]["slug"] == "expert--test-creator"
    assert results[0].get("elevenlabs_voice_id") == "test_voice_123"


def test_ui_get_existing_experts_with_voice_id(tmp_project: Path, monkeypatch):
    """Verify that get_existing_experts from UI helpers loads elevenlabs_voice_id."""
    from src.core.frontmatter import write_fm

    # Mock ROOT in ui.helpers
    monkeypatch.setattr("ui.helpers.ROOT", tmp_project)

    experts_dir = tmp_project / "data" / "experts"
    expert_dir = experts_dir / "expert--test-creator"
    expert_dir.mkdir(parents=True)
    
    # Write profile.md with elevenlabs_voice_id in frontmatter
    profile_path = expert_dir / "profile.md"
    write_fm(
        profile_path,
        {
            "type": "expert_profile",
            "elevenlabs_voice_id": "test_voice_456",
            "insight_count": 0,
        },
        "# Test Profile"
    )

    results = get_existing_experts_ui()
    assert len(results) == 1
    assert results[0]["slug"] == "expert--test-creator"
    assert results[0].get("elevenlabs_voice_id") == "test_voice_456"
