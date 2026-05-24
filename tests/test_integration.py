"""
Integration tests for the LifeOS E2E pipeline (Ingestion -> Indexing -> Search).
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Ensure scripts directory is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
    sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

from scripts.core.ingest import process_one_file
from scripts.core.frontmatter import read_fm
from ui.helpers import fts_search, rebuild_search_index


def test_youtube_to_chat_e2e(tmp_project: Path):
    """
    Simulates the E2E flow:
    1. Write YouTube URL to a raw inbox file.
    2. Mock metadata and transcript fetching.
    3. Run process_one_file (ingests URL, creates note, auto-rebuilds index).
    4. Search for content via fts_search (validates exact and natural language/stopword queries).
    """
    # Create the raw input file
    input_file = tmp_project / "data" / "inbox" / "raw" / "new_video.txt"
    input_file.write_text("https://www.youtube.com/watch?v=c4LSX-R2nJo", encoding="utf-8")

    # Mocks for external YouTube scraping and LLM summaries
    mock_metadata = {
        "title": "The New Way Of The Superior Man - David Deida (1st interview in a decade)",
        "uploader": "Chris Williamson",
        "channel": "Chris Williamson",
        "video_id": "c4LSX-R2nJo",
    }
    mock_transcript = (
        "What's happening people? Today we discuss David Deida's philosophy. "
        "The way of the superior man involves masculine and feminine polarity, "
        "spiritual sequence of sexual energies, and intimacy practices."
    )
    mock_decision = {
        "primary_domain": "life-kompass",
        "primary_mode": "life-kompass",
        "secondary_modes": [],
        "storage_location": "data/private/emotions/",
        "suggested_tags": ["feeling", "interview", "ai"],
        "one_next_action": "Review manually.",
        "privacy": "private",
    }

    # Ensure the target directory for private emotions exists in tmp_project
    (tmp_project / "data" / "private" / "emotions").mkdir(parents=True, exist_ok=True)

    # Patches to redirect files and DBs to the temporary project folder
    with patch("core.youtube.fetch_video_metadata", return_value=mock_metadata), \
         patch("core.youtube.fetch_transcript", return_value=mock_transcript), \
         patch("core.youtube.run_yt_dlp", return_value=MagicMock(returncode=0)), \
         patch("classify_input.classify", return_value=mock_decision), \
         patch("llm_client.call_llm", return_value="David Deida interview summary, polarity, sexual polarity."), \
         patch("build_fts_index.BASE_DIR", tmp_project), \
         patch("build_fts_index.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("build_fts_index.DIRECTORIES_TO_INDEX", [
             tmp_project / "data" / "knowledge",
             tmp_project / "data" / "private",
             tmp_project / "data" / "experts",
         ]), \
         patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("scripts.core.ingest.ROOT", tmp_project):

        # 1. Run the ingestion pipeline
        res = process_one_file(str(input_file), use_ai=True)
        assert res["success"] is True
        assert res["out_filepath"] is not None
        
        out_path = Path(res["out_filepath"])
        assert out_path.exists()

        # 2. Re-read the generated note and verify metadata and frontmatter
        fm, body = read_fm(out_path)
        assert fm["title"] == "The New Way Of The Superior Man - David Deida (1st interview in a decade)"
        assert fm["source_type"] == "youtube_video"
        assert fm["privacy"] == "private"  # life-kompass default is private
        assert "c4LSX-R2nJo" in body

        # 3. Rebuild search index manually to be sure it is updated
        idx_res = rebuild_search_index()
        assert idx_res["indexed"] > 0

        # 4. Search via exact term match
        results = fts_search("David Deida")
        assert len(results) > 0
        assert results[0][0] == "The New Way Of The Superior Man - David Deida (1st interview in a decade)"

        # 5. Search via natural language containing stopwords (e.g. what, does, say)
        results_nl = fts_search("What does david deida say about polarity")
        assert len(results_nl) > 0
        assert results_nl[0][0] == "The New Way Of The Superior Man - David Deida (1st interview in a decade)"

        # 6. Search for unrelated content
        results_none = fts_search("xyzabcqwe")
        assert len(results_none) == 0
