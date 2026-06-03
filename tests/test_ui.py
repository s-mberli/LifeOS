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
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
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
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
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
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project), \
         patch("core.chat_context.ask_llm_chat", return_value="I am a chatbot response.") as mock_ask, \
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


def test_ui_chat_save_insight_flow(tmp_project: Path):
    """Test that generated chat response renders Save Insight button, and clicking it works."""
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project), \
         patch("core.chat_context.ask_llm_chat", return_value="I am a chatbot response.") as mock_ask, \
         patch("ui.chat.auto_route_prompt", return_value={"primary_domain": "general"}), \
         patch("core.chat_persistence.save_message_as_insight", return_value=(True, "data/knowledge/chat-insights/some-note.md")) as mock_save:

        at = AppTest.from_file(APP_PATH)
        at.run()

        # Type message in chat input and run
        chat_input = at.chat_input[0]
        chat_input.set_value("Explain quantum physics simply.")
        at.run()

        assert not at.exception
        
        # Save Insight button should render in history
        save_buttons = [b for b in at.button if b.key and b.key.startswith("save_insight_")]
        assert len(save_buttons) == 1
        
        # Click the Save Insight button
        save_buttons[0].click()
        at.run()

        assert not at.exception
        mock_save.assert_called_once()
        # Verify index is added to saved msg indices in session state
        assert 1 in at.session_state.saved_msg_indices


# ── Date Added column formatting ──────────────────────────────────────────────

def _format_date_display(created_at: str) -> str:
    """Mirror of the formatting logic added to modals._library_modal_body."""
    date_display = ""
    if isinstance(created_at, str) and created_at:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(created_at)
            date_display = dt.strftime("%d %b %Y")
        except (ValueError, TypeError):
            date_display = created_at[:10] if len(created_at) >= 10 else created_at
    return date_display


def test_date_display_valid_iso_timestamp():
    """Valid ISO-8601 created_at should format as DD Mon YYYY."""
    result = _format_date_display("2026-05-26T11:28:53+10:00")
    assert result == "26 May 2026"


def test_date_display_missing_or_invalid():
    """Empty or non-ISO strings should return empty string or raw fallback without crashing."""
    assert _format_date_display("") == ""
    assert _format_date_display("not-a-date") == "not-a-date"  # exactly 10 chars, returned as-is
    assert _format_date_display("1748297200.123456") == "1748297200"  # mtime float fallback

def test_ui_memories_flow(tmp_project: Path):
    """Test the manual memory UI modal rendering."""
    # Ensure sys.path includes necessary directories for the runner
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    # Prepare a fresh DB so it's clean
    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project):

        at = AppTest.from_file(APP_PATH)
        at.run()
        assert not at.exception
        
        # Open the modal
        mem_btn = [b for b in at.sidebar.button if b.label == "🧠 Manual Personal Memory"]
        assert len(mem_btn) > 0, "Could not find modal button"
        mem_btn[0].click()
        at.run()
        
        assert not at.exception
        # Verify the modal rendered by checking for the Title text input
        titles = [ti for ti in at.text_input if ti.label == "Title (e.g. Coding Style)"]
        assert len(titles) > 0, "Modal did not render expected inputs"


def test_ui_polish(tmp_project: Path):
    """Test visual hierarchy, custom CSS injection, empty state, and tooltips."""
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project):

        at = AppTest.from_file(APP_PATH)
        at.run()

        assert not at.exception

        # 1. Verify CSS Injection
        style_markdowns = [m for m in at.markdown if "<style>" in m.value]
        assert len(style_markdowns) > 0, "Custom CSS block was not injected"
        assert "chat-role-user" in style_markdowns[0].value
        assert "chat-role-assistant" in style_markdowns[0].value

        # 2. Verify Empty State when history is empty
        assert len(at.session_state.messages) == 0
        welcome_markdowns = [m for m in at.markdown if "Onboarding Hints" in m.value]
        assert len(welcome_markdowns) > 0, "Welcome onboarding state was not rendered"

        # 3. Verify Tooltips on Active Context and Response Length
        multiselects = [ms for ms in at.multiselect if ms.label == "Active Context (Leave empty to search entire library)"]
        assert len(multiselects) == 1
        assert multiselects[0].help == "Select specific experts or files to narrow down the knowledge base. Leave empty to search everything."

        selectboxes = [sb for sb in at.selectbox if sb.label == "Response Length"]
        assert len(selectboxes) == 1
        assert selectboxes[0].help == "Choose how detailed the synthesized response should be."

        # 4. Verify Sidebar Ingestion Tabs
        assert len(at.sidebar.tabs) == 2


def test_ui_upload_file_flow(tmp_project: Path):
    """Test that uploading a file in the sidebar tab triggers processing."""
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
        sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

    mock_res = {"success": True, "file_path": "data/knowledge/general/file.md", "out_filepath": "data/knowledge/general/file.md"}

    with patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("ui.sidebar.ROOT", tmp_project), \
         patch("ui.chat.ROOT", tmp_project), \
         patch("core.ingest.process_one_file", return_value=mock_res) as mock_ingest, \
         patch("ui.sidebar.rebuild_search_index") as mock_rebuild:

        at = AppTest.from_file(APP_PATH)
        at.run()

        # Simulate file upload in the file uploader
        # In streamlit AppTest, we can use the .upload() method or set files directly
        # Since AppTest file_uploader has a type InitialValue, let's mock it
        uploader = at.sidebar.file_uploader[0]
        
        # Streamlit AppTest allows setting the value of the file_uploader
        # by passing a list of tuples: (filename, content, mime_type)
        uploader.set_value([("test_note.txt", b"Hello world", "text/plain")])
        at.run()

        assert not at.exception
        
        # Click the Save Insight(s) button (1st button in sidebar)
        at.sidebar.button[0].click()
        at.run()

        assert not at.exception
        mock_ingest.assert_called_once()
        mock_rebuild.assert_called_once()



