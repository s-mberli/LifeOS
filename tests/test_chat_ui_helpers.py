import pytest
from pathlib import Path
import sys

# Ensure import path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

APP_DIR = BASE_DIR / "apps" / "streamlit-chat"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# This will fail because the function doesn't exist yet!
from ui.helpers import build_allowed_paths

def test_build_allowed_paths_general_mode():
    """When no expert or scope is selected, it should default to general mode requiring insight notes."""
    paths, require_insight = build_allowed_paths(
        selected_scopes=[], 
        target_expert_dict=None, 
        options_map={}, 
        root_dir=Path("/tmp")
    )
    assert paths == set()
    assert require_insight is True
