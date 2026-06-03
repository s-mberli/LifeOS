import hashlib
import os
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent.parent


def generate_speech(text: str, voice_id: str | None = None) -> bytes:
    """Generate speech from text using the ElevenLabs API, caching results on disk.

    Args:
        text: The text to speak.
        voice_id: Cloned voice ID from ElevenLabs. If None, falls back to the
            default voice ID.

    Returns:
        bytes: MP3 audio data.

    Raises:
        ValueError: If ELEVENLABS_API_KEY is not set.
        requests.RequestException: If the API request fails.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set.")

    # Fallback default voice (Rachel)
    voice_id = voice_id or os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    # Check local cache first
    cache_dir = ROOT / "data" / "tts_cache"
    cache_key = hashlib.sha256(f"{voice_id}:{text}".encode("utf-8")).hexdigest()
    cache_path = cache_dir / f"{cache_key}.mp3"

    if cache_path.exists():
        try:
            return cache_path.read_bytes()
        except Exception:
            pass

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    audio_bytes = response.content

    # Save to cache
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path.write_bytes(audio_bytes)
    except Exception:
        pass

    return audio_bytes

