"""
Streamlit AppTest integration tests for LifeOS UI layout and actions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from streamlit.testing.v1 import AppTest

# Resolve paths
ROOT = Path(__file__).resolve().parent.parent
APP_PATH = str(ROOT / "apps" / "streamlit-chat" / "app.py")


def test_ui_render_default(tmp_project: Path):
    """Test that the Streamlit app loads and renders elements correctly in default state."""
    # Ensure sys.path includes necessary directories for the runner
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project):

        at = AppTest.from_file(APP_PATH)
        at.run()

        # Should not raise any unhandled exception
        assert not at.exception

        # Verify title & captions render in main chat body
        # Since we use st.title("🧭 LifeOS"), AppTest will find it in title elements
        assert len(at.title) > 0
        assert "LifeOS" in at.title[0].value

        # Verify sidebars render header / Quick Actions title
        # In streamlit-1.32.0, AppTest collects sidebar elements separately
        sidebar_text = [elem.value for elem in at.sidebar if hasattr(elem, "value")]
        assert any("Quick Actions" in val for val in sidebar_text if isinstance(val, str))

        # Check for inputs like URL input field
        url_inputs = [elem for elem in at.sidebar if hasattr(elem, "label") and elem.label == "Or paste URL, raw text, or transcript:"]
        assert len(url_inputs) == 1


def test_ui_submit_url_form(tmp_project: Path):
    """Test that submitting a URL in the sidebar form triggers the ingestion pipeline."""
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    mock_res = {"success": True, "file_path": "data/knowledge/general/note.md", "out_filepath": "data/knowledge/general/note.md"}

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project), \
         patch("core.ingest.process_one_file", return_value=mock_res) as mock_ingest, \
         patch("ui.sidebar.rebuild_search_index") as mock_rebuild:

        at = AppTest.from_file(APP_PATH)
        at.run()

        # Set URL in the text area by index
        at.sidebar.text_area[0].set_value("https://example.com/test-article")
        
        # Click the "Save Insight(s)" button (it's now the 1st button in the sidebar)
        at.sidebar.button[0].click()
        at.run()

        assert not at.exception
        mock_ingest.assert_called_once()
        mock_rebuild.assert_called_once()



def test_ui_chat_input_flow(tmp_project: Path):
    """Test typing into chat input streams response and updates message list."""
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project), \
         patch("ui.helpers.ask_llm_chat", return_value="I am a chatbot response.") as mock_ask, \
         patch("ui.chat.auto_route_prompt", return_value={"primary_domain": "general"}):

        at = AppTest.from_file(APP_PATH)
        at.run()

        # Type message in chat input and run (setting value and running submits it)
        chat_input = at.chat_input[0]
        chat_input.set_value("What is AI?")
        at.run()

        assert not at.exception
        # LLM client mock should be called with user prompt
        mock_ask.assert_called_once()
        
        # Session state messages should contain the user prompt and assistant response
        messages = at.session_state.messages
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "What is AI?"
        assert messages[1]["role"] == "assistant"
        assert messages[1]["content"] == "I am a chatbot response."

