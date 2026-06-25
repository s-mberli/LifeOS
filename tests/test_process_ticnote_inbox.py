import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.process_ticnote_inbox import process_inbox, sanitize_filename

@patch("scripts.process_ticnote_inbox.write_fm")
@patch("scripts.process_ticnote_inbox.call_llm")
@patch("pathlib.Path.unlink")
def test_process_inbox_markdown(mock_unlink, mock_call_llm, mock_write_fm, tmp_path):
    # Setup mock inbox and knowledge base dirs
    inbox_dir = tmp_path / "inbox"
    base_dir = tmp_path / "knowledge"
    
    project_dir = inbox_dir / "Project_A"
    project_dir.mkdir(parents=True)
    
    # Create test markdown transcript file in inbox
    test_file = project_dir / "meeting_one.md"
    test_file.write_text("Hello this is speaker one speaking. We decided to build a product.", encoding="utf-8")
    
    # Mock LLM summary
    mock_call_llm.return_value = "## Summary\nDecided to build a product."
    
    # Execute processing
    process_inbox(inbox_dir, base_dir)
    
    # Check that write_fm was called twice (once for raw, once for insights)
    assert mock_write_fm.call_count == 2
    
    # Raw write verification
    args_raw = mock_write_fm.call_args_list[0][0]
    raw_path = args_raw[0]
    raw_fm = args_raw[1]
    raw_body = args_raw[2]
    
    assert raw_path.parent.name == "raw"
    assert raw_path.parent.parent.name == "Project_A"
    assert raw_fm["project"] == "Project_A"
    assert raw_fm["title"] == "Raw: Meeting One"
    assert "Hello this is speaker one" in raw_body
    
    # Insights write verification
    args_insights = mock_write_fm.call_args_list[1][0]
    insights_path = args_insights[0]
    insights_fm = args_insights[1]
    insights_body = args_insights[2]
    
    assert insights_path.parent.name == "Project_A"
    assert insights_fm["project"] == "Project_A"
    assert insights_fm["title"] == "Insights: Meeting One"
    assert "Decided to build a product." in insights_body
    
    # Verify the original inbox file unlink was called
    mock_unlink.assert_called_once()


@patch("scripts.process_ticnote_inbox.write_fm")
@patch("scripts.process_ticnote_inbox.call_llm")
@patch("pathlib.Path.unlink")
def test_process_inbox_json(mock_unlink, mock_call_llm, mock_write_fm, tmp_path):
    # Setup mock inbox and knowledge base dirs
    inbox_dir = tmp_path / "inbox"
    base_dir = tmp_path / "knowledge"
    
    inbox_dir.mkdir(parents=True)
    
    # Create test JSON file in inbox root (should default to project "Inbox")
    test_file = inbox_dir / "meeting_two.json"
    json_data = {
        "transcribeJson": json.dumps([{"speaker": "Alice", "text": "Let's do this."}]),
        "summaryJson": json.dumps({
            "title": "Discussion",
            "summary": "Alice proposed doing it.",
            "keyPoints": ["Agreed to start."]
        })
    }
    test_file.write_text(json.dumps(json_data), encoding="utf-8")
    
    # Run inbox processing
    process_inbox(inbox_dir, base_dir)
    
    # Check that write_fm was called twice
    assert mock_write_fm.call_count == 2
    
    # Raw write verification
    args_raw = mock_write_fm.call_args_list[0][0]
    raw_path = args_raw[0]
    raw_fm = args_raw[1]
    raw_body = args_raw[2]
    
    assert raw_path.parent.name == "raw"
    assert raw_path.parent.parent.name == "Inbox"
    assert raw_fm["project"] == "Inbox"
    assert "**Alice**: Let's do this." in raw_body
    
    # Insights write verification (from pre-generated summary JSON, no LLM call)
    mock_call_llm.assert_not_called()
    args_insights = mock_write_fm.call_args_list[1][0]
    insights_path = args_insights[0]
    insights_fm = args_insights[1]
    insights_body = args_insights[2]
    
    assert insights_path.parent.name == "Inbox"
    assert "Alice proposed doing it." in insights_body
    assert "Agreed to start." in insights_body
