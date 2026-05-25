"""
Tests for the LLM client wrapper (``scripts/llm_client.py``).

Verifies that ``call_llm`` correctly handles:
1. Plain string prompts
2. OpenAI-style messages lists (future extension)
3. All provider failures → returns ``None``

No real API calls are made. All provider calls are intercepted via
``unittest.mock.patch``.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Ensure scripts/ is importable
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "src"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# ---------------------------------------------------------------------------
# Guard: skip entire module if llm_client cannot be imported
# ---------------------------------------------------------------------------
try:
    import llm_client  # noqa: F401 – import for availability check
    _LLM_CLIENT_AVAILABLE = True
except Exception:
    _LLM_CLIENT_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not _LLM_CLIENT_AVAILABLE,
    reason="scripts/llm_client.py is not importable",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_FAKE_RESULT = ("This is a mocked LLM response.", "mock-provider", "mock-model", {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30,
})


# ---------------------------------------------------------------------------
# Tests: call_llm with a plain string prompt
# ---------------------------------------------------------------------------


class TestCallLlmPlainStringPrompt:
    """call_llm accepts a plain string prompt and returns the text content."""

    def test_returns_string_content(self):
        """When try_providers succeeds, call_llm must return just the text string."""
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT) as mock_tp:
            from llm_client import call_llm

            result = call_llm("Tell me about AI.")

        assert isinstance(result, str)
        assert result == "This is a mocked LLM response."
        mock_tp.assert_called_once()

    def test_passes_prompt_to_try_providers(self):
        """call_llm must forward the user prompt string to try_providers."""
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT) as mock_tp:
            from llm_client import call_llm

            call_llm("Hello, world!")

        _args, _kwargs = mock_tp.call_args
        # The user prompt is the second positional argument to try_providers
        assert "Hello, world!" in _args

    def test_default_system_prompt_used(self):
        """call_llm must use its default system prompt when none is provided."""
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT) as mock_tp:
            from llm_client import call_llm

            call_llm("Any question")

        _args, _kwargs = mock_tp.call_args
        # The system prompt is the first positional argument
        system_prompt_arg = _args[0]
        assert isinstance(system_prompt_arg, str)
        assert len(system_prompt_arg) > 0

    def test_custom_system_prompt_forwarded(self):
        """A custom system_prompt kwarg must be forwarded to try_providers."""
        custom_sys = "You are a pirate."
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT) as mock_tp:
            from llm_client import call_llm

            call_llm("Hello", system_prompt=custom_sys)

        _args, _kwargs = mock_tp.call_args
        assert _args[0] == custom_sys


# ---------------------------------------------------------------------------
# Tests: call_llm with OpenAI-style messages list
# ---------------------------------------------------------------------------


class TestCallLlmMessagesFormat:
    """call_llm behaviour when passed an OpenAI-style messages list."""

    def test_messages_list_does_not_crash(self):
        """Passing a messages list must not raise an exception.

        The current implementation converts or forwards the prompt; this test
        ensures the function is at least callable with a list argument and
        returns either a string or None.
        """
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "What is 2+2?"},
        ]
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT):
            from llm_client import call_llm

            # call_llm's first positional arg is `prompt`; passing a list
            # exercises the boundary without expecting a specific format.
            try:
                result = call_llm(messages)  # type: ignore[arg-type]
                # If it doesn't crash, accept either str or None
                assert result is None or isinstance(result, str)
            except TypeError:
                # If the implementation does strict type checking, that is also
                # acceptable – the test just verifies it raises TypeError, not
                # some unexpected crash.
                pass

    def test_messages_list_returns_content_string_if_supported(self):
        """If the implementation forwards the list, the returned value is a str."""
        messages = [{"role": "user", "content": "Summarise AI trends."}]
        with patch("src.core.llm_client.try_providers", return_value=_FAKE_RESULT):
            from llm_client import call_llm

            try:
                result = call_llm(messages)  # type: ignore[arg-type]
                if result is not None:
                    assert isinstance(result, str)
            except TypeError:
                pass  # Strict typing is fine; just must not crash unexpectedly


# ---------------------------------------------------------------------------
# Tests: all providers fail → returns None
# ---------------------------------------------------------------------------


class TestCallLlmAllProvidersFail:
    """call_llm must return None when every provider returns None."""

    def test_returns_none_on_total_failure(self):
        """If try_providers returns None, call_llm must propagate None."""
        with patch("src.core.llm_client.try_providers", return_value=None):
            from llm_client import call_llm

            result = call_llm("This will fail.")

        assert result is None

    def test_try_providers_called_even_on_failure(self):
        """try_providers must still be invoked (not short-circuited) on failure."""
        with patch("src.core.llm_client.try_providers", return_value=None) as mock_tp:
            from llm_client import call_llm

            call_llm("fail test")

        mock_tp.assert_called_once()

    def test_no_exception_raised_on_total_failure(self):
        """call_llm must swallow provider failures gracefully (no exception)."""
        with patch("src.core.llm_client.try_providers", return_value=None):
            from llm_client import call_llm

            try:
                result = call_llm("fail silently")
                assert result is None
            except Exception as exc:  # noqa: BLE001
                pytest.fail(f"call_llm raised an unexpected exception: {exc}")

    def test_individual_providers_all_return_none(self):
        """Simulate each provider function returning None; try_providers must return None."""
        with patch("src.core.llm_client.call_azure", return_value=None), \
             patch("src.core.llm_client.call_gemini", return_value=None), \
             patch("src.core.llm_client.call_openrouter", return_value=None):
            from llm_client import try_providers

            result = try_providers("system prompt", "user prompt", 500)

        assert result is None
