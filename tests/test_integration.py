"""
Integration tests for the LifeOS E2E pipeline (Ingestion -> Indexing -> Search).
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Ensure scripts directory is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
if str(ROOT / "apps" / "streamlit-chat") not in sys.path:
    sys.path.insert(0, str(ROOT / "apps" / "streamlit-chat"))

from src.core.ingest import process_one_file
from src.core.frontmatter import read_fm
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
         patch("src.core.classify_input.classify", return_value=mock_decision), \
         patch("src.core.llm_client.call_llm", return_value="David Deida interview summary, polarity, sexual polarity."), \
         patch("src.core.build_fts_index.BASE_DIR", tmp_project), \
         patch("src.core.build_fts_index.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.build_fts_index.DIRECTORIES_TO_INDEX", [
             tmp_project / "data" / "knowledge",
             tmp_project / "data" / "private",
             tmp_project / "data" / "experts",
         ]), \
         patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.search_knowledge.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.ingest.ROOT", tmp_project):

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
        results = fts_search("David Deida", include_private=True)
        print("DEBUG RESULTS:", results)
        assert len(results) > 0
        assert results[0][0] == "The New Way Of The Superior Man - David Deida (1st interview in a decade)"

        # 5. Search via natural language containing stopwords (e.g. what, does, say)
        results_nl = fts_search("What does david deida say about polarity", include_private=True)
        assert len(results_nl) > 0
        assert results_nl[0][0] == "The New Way Of The Superior Man - David Deida (1st interview in a decade)"

        # 6. Search for unrelated content
        results_none = fts_search("xyzabcqwe", include_private=True)
        assert len(results_none) == 0


def test_reddit_and_jina_ingestion_e2e(tmp_project: Path):
    """
    Test that Reddit JSON fetching and Jina Reader API work E2E:
    1. Write Reddit URL and general URL to raw files.
    2. Mock requests.get for Reddit JSON and Jina Reader.
    3. Run process_one_file for both.
    4. Verify markdown files contain the correct post and comment threads.
    5. Rebuild search index.
    6. Verify we can chat (search) with the content.
    """
    # 1. Create raw input files
    reddit_file = tmp_project / "data" / "inbox" / "raw" / "reddit_post.txt"
    reddit_file.write_text("https://www.reddit.com/r/python/comments/xyz/python_is_awesome/", encoding="utf-8")

    jina_file = tmp_project / "data" / "inbox" / "raw" / "jina_post.txt"
    jina_file.write_text("https://example.com/some-cool-article", encoding="utf-8")

    mock_reddit_response = [
        {
            "kind": "Listing",
            "data": {
                "children": [
                    {
                        "kind": "t3",
                        "data": {
                            "title": "Python is awesome",
                            "author": "guido",
                            "subreddit": "python",
                            "score": 420,
                            "selftext": "This is a post about python."
                        }
                    }
                ]
            }
        },
        {
            "kind": "Listing",
            "data": {
                "children": [
                    {
                        "kind": "t1",
                        "data": {
                            "author": "linus",
                            "score": 69,
                            "body": "I prefer C but Python is okay.",
                            "replies": {
                                "kind": "Listing",
                                "data": {
                                    "children": [
                                        {
                                            "kind": "t1",
                                            "data": {
                                                "author": "guido",
                                                "score": 10,
                                                "body": "C is great too!",
                                                "replies": ""
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
    ]

    def mock_requests_get(url, *args, **kwargs):
        resp = MagicMock()
        resp.status_code = 200
        if "reddit.com" in url or "redd.it" in url:
            resp.json.return_value = mock_reddit_response
        elif "r.jina.ai" in url:
            resp.headers = {"X-Title": "Jina Scraped Article"}
            resp.text = "# Jina Scraped Article\nThis is content from Jina Reader."
        else:
            resp.status_code = 404
        return resp

    mock_decision = {
        "primary_domain": "general",
        "primary_mode": "router",
        "secondary_modes": [],
        "storage_location": "data/knowledge/",
        "suggested_tags": ["test"],
        "one_next_action": "Review manually.",
        "privacy": "public",
    }

    # Patches to redirect files and DBs to the temporary project folder
    with patch("requests.get", side_effect=mock_requests_get), \
         patch("src.core.classify_input.classify", return_value=mock_decision), \
         patch("src.core.llm_client.call_llm", return_value="Summary of Python or Jina post"), \
         patch("src.core.build_fts_index.BASE_DIR", tmp_project), \
         patch("src.core.build_fts_index.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.build_fts_index.DIRECTORIES_TO_INDEX", [
             tmp_project / "data" / "knowledge",
         ]), \
         patch("ui.helpers.ROOT", tmp_project), \
         patch("ui.helpers.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.search_knowledge.DB_PATH", tmp_project / "indexes" / "lifeos.db"), \
         patch("src.core.ingest.ROOT", tmp_project):

        # Ingest Reddit Post
        res_reddit = process_one_file(str(reddit_file), use_ai=True)
        assert res_reddit["success"] is True
        assert res_reddit["out_filepath"] is not None
        
        reddit_out = Path(res_reddit["out_filepath"])
        assert reddit_out.exists()
        reddit_fm, reddit_body = read_fm(reddit_out)
        
        # Verify title & formatting
        assert reddit_fm["title"] == "Python is awesome"
        # Check main post content
        assert "This is a post about python." in reddit_body
        # Check comment thread hierarchy blockquotes
        assert "> **u/linus** (69 points):" in reddit_body
        assert "> I prefer C but Python is okay." in reddit_body
        assert "> > **u/guido** (10 points):" in reddit_body
        assert "> > C is great too!" in reddit_body

        # Ingest Jina General Post
        res_jina = process_one_file(str(jina_file), use_ai=True)
        assert res_jina["success"] is True
        
        jina_out = Path(res_jina["out_filepath"])
        assert jina_out.exists()
        jina_fm, jina_body = read_fm(jina_out)
        
        assert jina_fm["title"] == "Jina Scraped Article"
        assert "This is content from Jina Reader." in jina_body

        # Rebuild Search Index
        idx_res = rebuild_search_index()
        assert idx_res["indexed"] == 2

        # Search / Chat test
        results_reddit = fts_search("prefer C but Python")
        assert len(results_reddit) > 0
        assert results_reddit[0][0] == "Python is awesome"

        results_jina = fts_search("content from Jina Reader")
        assert len(results_jina) > 0
        assert results_jina[0][0] == "Jina Scraped Article"

