import sys
from pathlib import Path
import os
import re

# Add src and apps to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

from core.chat_context import execute_agent_search_loop
from ui.helpers import construct_chat_prompts

# Load dotenv to ensure API keys are present
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

# Guard: Skip the entire module if no LLM API keys are set in the environment
import pytest
has_keys = (
    os.environ.get("GEMINI_API_KEY")
    or os.environ.get("AZURE_OPENAI_API_KEY")
    or os.environ.get("OPENROUTER_API_KEY")
)

pytestmark = pytest.mark.skipif(
    not has_keys,
    reason="No LLM API keys configured in environment. Skipping evaluation test."
)

# Mock FTS Data
SHORT_NOTE = "Principle: Eat the frog. Do the hardest thing first thing in the morning."
MEDIUM_NOTE = "Health Protocol: Sleep is the foundation. Aim for 8 hours. Principle: Consistency over intensity. Go to bed at the same time every day. Action: Set an alarm for bedtime."
LONG_NOTE = "Deep Dive into Existential Purpose: The meaning of life is what you make of it. Principle: Action precedes motivation. Often we wait to feel motivated before we act, but the reverse is true. If you start acting, the motivation follows. This concept is explored deeply in behavioral activation therapy. When you feel a 'man of zero', it implies a loss of intrinsic drive. The solution is not to wait for the drive to return, but to construct a series of small, undeniable wins. These wins serve as the bedrock for a new identity. Action: Commit to 5 minutes of a task. The inertia of starting is the hardest part."

def mock_fts_search_short(query, limit, allowed_paths):
    return [("Productivity", "prod.md", SHORT_NOTE, 0.9)]

def mock_fts_search_medium(query, limit, allowed_paths):
    return [("Health", "health.md", MEDIUM_NOTE, 0.9)]

def mock_fts_search_long(query, limit, allowed_paths):
    return [("Purpose", "purpose.md", LONG_NOTE, 0.9)]

def get_system_prompt():
    sys_prompt, _ = construct_chat_prompts(
        target_expert=None,
        prompt="",
        selected_scopes=[],
        options_map={},
        fts_results=[],
        root_dir=ROOT
    )
    return sys_prompt

def verify_response_quality(response: str, expected_keyword: str):
    # 1. Not cut off check
    assert re.search(r'[.!?]\s*$', response) is not None, f"Response appears cut off: {response[-50:]}"
    
    # 2. Length check
    assert len(response) > 200, f"Response is too short: {len(response)} chars. \nResponse: {response}"
    
    # 3. Formatting check (Markdown)
    assert re.search(r'(^|\n)\s*[\-\*]\s+', response) is not None, f"Response missing bullet points.\nResponse: {response}"
    assert "**" in response, f"Response missing bold text.\nResponse: {response}"
    
    # 4. Context Adherence
    assert expected_keyword.lower() in response.lower(), f"Response missing expected context keyword '{expected_keyword}'.\nResponse: {response}"
    
    # 5. Principle first check
    first_half = response[:len(response)//2].lower()
    assert "principle" in first_half or "concept" in first_half or "foundation" in first_half, f"Response did not explain the principle early on.\nResponse: {response}"

def test_short_context():
    sys_prompt = get_system_prompt()
    response, calls = execute_agent_search_loop(
        system_prompt=sys_prompt,
        user_prompt="How do I get things done early? (Search the vault first)",
        fts_search_fn=mock_fts_search_short
    )
    
    assert len(calls) > 0, "Agent failed to search."
    verify_response_quality(response, "frog")

def test_medium_context():
    sys_prompt = get_system_prompt()
    response, calls = execute_agent_search_loop(
        system_prompt=sys_prompt,
        user_prompt="What is a good health protocol for sleeping? (Search the vault first)",
        fts_search_fn=mock_fts_search_medium
    )
    
    assert len(calls) > 0, "Agent failed to search."
    verify_response_quality(response, "consistency")

def test_long_context():
    sys_prompt = get_system_prompt()
    response, calls = execute_agent_search_loop(
        system_prompt=sys_prompt,
        user_prompt="How to regain purpose after losing motivation? (Search the vault first)",
        fts_search_fn=mock_fts_search_long
    )
    
    assert len(calls) > 0, "Agent failed to search."
    verify_response_quality(response, "inertia")

def run_tests():
    print("Running short context test...")
    test_short_context()
    print("Running medium context test...")
    test_medium_context()
    print("Running long context test...")
    test_long_context()
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
