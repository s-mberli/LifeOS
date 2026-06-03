"""
Unit tests for SevenLabs Text-to-Speech (src/core/tts.py).
"""
import os
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

# We import generate_speech from src.core.tts
# Since the module does not exist yet, we wrap imports or expect it to fail
# during the RED phase of TDD.
try:
    from src.core.tts import generate_speech
except ImportError:
    generate_speech = None


@pytest.fixture
def clean_env():
    """Ensure environment is controlled."""
    old_key = os.environ.get("ELEVENLABS_API_KEY")
    old_default = os.environ.get("ELEVENLABS_DEFAULT_VOICE_ID")
    
    if "ELEVENLABS_API_KEY" in os.environ:
        del os.environ["ELEVENLABS_API_KEY"]
    if "ELEVENLABS_DEFAULT_VOICE_ID" in os.environ:
        del os.environ["ELEVENLABS_DEFAULT_VOICE_ID"]
        
    yield
    
    if old_key is not None:
        os.environ["ELEVENLABS_API_KEY"] = old_key
    if old_default is not None:
        os.environ["ELEVENLABS_DEFAULT_VOICE_ID"] = old_default


def test_generate_speech_missing_api_key(clean_env):
    """ValueError must be raised if ELEVENLABS_API_KEY is not set."""
    if generate_speech is None:
        pytest.skip("src/core/tts.py not implemented yet")
        
    with pytest.raises(ValueError, match="ELEVENLABS_API_KEY not set"):
        generate_speech("Hello world")


@patch("requests.post")
def test_generate_speech_success(mock_post, tmp_path, clean_env):
    """Verify correct API call headers, payload, and response content."""
    if generate_speech is None:
        pytest.skip("src/core/tts.py not implemented yet")

    os.environ["ELEVENLABS_API_KEY"] = "fake_key"
    mock_response = MagicMock()
    mock_response.content = b"fake_audio_bytes"
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    with patch("src.core.tts.ROOT", tmp_path):
        res = generate_speech("Hello test", voice_id="custom_voice")
        
        assert res == b"fake_audio_bytes"
        mock_post.assert_called_once()
        
        url, kwargs = mock_post.call_args
        assert "https://api.elevenlabs.io/v1/text-to-speech/custom_voice" in url[0]
        assert kwargs["headers"]["xi-api-key"] == "fake_key"
        assert kwargs["json"]["text"] == "Hello test"


@patch("requests.post")
def test_generate_speech_fallback_voice(mock_post, tmp_path, clean_env):
    """Verify fallback to ELEVENLABS_DEFAULT_VOICE_ID then default constant."""
    if generate_speech is None:
        pytest.skip("src/core/tts.py not implemented yet")

    os.environ["ELEVENLABS_API_KEY"] = "fake_key"
    mock_response = MagicMock()
    mock_response.content = b"fake_audio_bytes"
    mock_post.return_value = mock_response

    with patch("src.core.tts.ROOT", tmp_path):
        # Fallback to ELEVENLABS_DEFAULT_VOICE_ID
        os.environ["ELEVENLABS_DEFAULT_VOICE_ID"] = "env_voice_id"
        generate_speech("Hello fallback")
        url1 = mock_post.call_args[0][0]
        assert "env_voice_id" in url1

        # Fallback to hardcoded default if env var is missing
        del os.environ["ELEVENLABS_DEFAULT_VOICE_ID"]
        generate_speech("Hello default fallback")
        url2 = mock_post.call_args[0][0]
        assert "21m00Tcm4TlvDq8ikWAM" in url2


@patch("requests.post")
def test_generate_speech_caching(mock_post, tmp_path, clean_env):
    """Verify that generate_speech uses disk cache on subsequent calls."""
    if generate_speech is None:
        pytest.skip("src/core/tts.py not implemented yet")

    os.environ["ELEVENLABS_API_KEY"] = "fake_key"
    mock_response = MagicMock()
    mock_response.content = b"cached_audio_bytes"
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    # Patch ROOT to use tmp_path
    with patch("src.core.tts.ROOT", tmp_path):
        # First call: hits API and writes cache
        res1 = generate_speech("Hello cache", voice_id="custom_voice")
        assert res1 == b"cached_audio_bytes"
        assert mock_post.call_count == 1

        # Second call: hits cache, bypasses API
        res2 = generate_speech("Hello cache", voice_id="custom_voice")
        assert res2 == b"cached_audio_bytes"
        assert mock_post.call_count == 1  # Still 1

