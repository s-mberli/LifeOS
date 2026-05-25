"""
Persona-based tests for Curator Chris.

Curator Chris wants the agent to be able to search the Vault on-demand
via full-text search (FTS) when asked questions about stored insights,
using a robust provider-agnostic XML tool calling loop.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure scripts and ui folders are in python path
ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT / "apps" / "streamlit-chat"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(UI_DIR) not in sys.path:
    sys.path.insert(0, str(UI_DIR))

from ui.helpers import execute_agent_search_loop


def test_execute_agent_search_loop_no_tool_call():
    """If the LLM response has no XML tool calls, return the response directly."""
    mock_ask_llm = MagicMock(return_value="Ali Abdaal says productivity is about feeling good.")
    
    with patch("ui.helpers.ask_llm_chat", mock_ask_llm):
        final_answer, calls_made = execute_agent_search_loop(
            system_prompt="You are an assistant.",
            user_prompt="Explain Ali Abdaal's view on productivity.",
            history=[],
            allowed_paths=None,
        )
        
    assert final_answer == "Ali Abdaal says productivity is about feeling good."
    assert len(calls_made) == 0
    mock_ask_llm.assert_called_once()


def test_execute_agent_search_loop_with_tool_call():
    """If the LLM outputs <call:fts_search>, execute the search and call the LLM again with results."""
    # First response triggers the tool call
    # Second response gives the final answer
    llm_responses = [
        "I need to search the database.\n<call:fts_search>Ali Abdaal productivity</call:fts_search>",
        "Based on the search results, Ali Abdaal suggests that feeling good leads to productivity."
    ]
    mock_ask_llm = MagicMock(side_effect=llm_responses)
    
    # Mock fts_search to return a test result
    mock_fts = MagicMock(return_value=[
        ("Ali Abdaal note", "data/knowledge/ali.md", "feeling good leads to productivity", -1.2)
    ])
    
    with patch("ui.helpers.ask_llm_chat", mock_ask_llm), \
         patch("ui.helpers.fts_search", mock_fts):
         
        final_answer, calls_made = execute_agent_search_loop(
            system_prompt="You are an assistant.",
            user_prompt="Explain Ali Abdaal's view on productivity.",
            history=[],
            allowed_paths=None,
        )
        
    assert final_answer == "Based on the search results, Ali Abdaal suggests that feeling good leads to productivity."
    assert len(calls_made) == 1
    assert calls_made[0] == ("Ali Abdaal productivity", "Ali Abdaal note (data/knowledge/ali.md):\nfeeling good leads to productivity")
    
    # Verify LLM was called twice
    assert mock_ask_llm.call_count == 2
    
    # Verify first call had the original user prompt
    first_call_args = mock_ask_llm.call_args_list[0][0]
    assert "Explain Ali Abdaal's view on productivity." in first_call_args[1]
    
    # Verify second call included the search results in history
    second_call_kwargs = mock_ask_llm.call_args_list[1][1]
    history_sent = second_call_kwargs.get("history", [])
    assert any("feeling good leads to productivity" in msg["content"] for msg in history_sent)

