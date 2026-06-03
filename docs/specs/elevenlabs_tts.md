# Spec: ElevenLabs TTS & Voice Personas

## Objective
Enable voice playback of assistant responses matching the persona of the active expert.
- User can click "🔊 Read Aloud" next to an assistant response.
- Response is spoken using the expert's ElevenLabs voice_id (or default voice if none).
- Audio is played back directly in the Streamlit UI.
- Avoid automatic generation to prevent unnecessary ElevenLabs API costs.

## Tech Stack
- Python 3.11+
- Streamlit
- `requests` (for lightweight API call to ElevenLabs)
- `pytest` (for tests)

## Commands
- Run tests: `.venv/bin/pytest tests/test_tts.py`
- Run all tests: `.venv/bin/pytest`
- Run Streamlit: `.venv/bin/streamlit run apps/streamlit-chat/app.py`

## Project Structure
- `src/core/tts.py` -> API interaction with ElevenLabs
- `src/core/experts.py` -> Parsing expert profile and metadata for `elevenlabs_voice_id`
- `apps/streamlit-chat/ui/chat.py` -> UI button and audio playback
- `tests/test_tts.py` -> Unit tests for TTS module and mock API responses
- `tests/test_experts_tts.py` -> Unit/Integration tests for voice ID retrieval

## Code Style
- Follow Python PEP 8.
- Type hints on all function signatures.
- Clean mock usage in tests.
Example:
```python
def generate_speech(text: str, voice_id: str | None = None) -> bytes:
    """Generate speech using ElevenLabs API."""
    ...
```

## Testing Strategy
- Unit tests: Mock `requests.post` to avoid actual API usage during tests.
- Verify fallback behavior when `voice_id` is empty/None.
- Verify error handling when API key is missing or ElevenLabs API returns an error.
- Verify expert profile parser retrieves `elevenlabs_voice_id` from frontmatter.

## Boundaries
- **Always**: Use `pathlib.Path` for pathing. Check if `ELEVENLABS_API_KEY` is present.
- **Ask first**: Adding new packages (use standard `requests` instead).
- **Never**: Commit api keys to git. Perform synchronous requests that block the whole app.

## Success Criteria
- [ ] Clicking "🔊 Read Aloud" triggers ElevenLabs API call with the correct `voice_id`.
- [ ] Fallback to default voice ID occurs if expert doesn't have one.
- [ ] Output audio plays successfully in Streamlit.
- [ ] No crash if API key is missing or API returns error; show `st.error` instead.
- [ ] Core TTS logic fully covered by unit tests.
