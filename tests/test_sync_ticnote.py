import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.sync_ticnote import process_file_tree

@patch("scripts.sync_ticnote.write_fm")
@patch("scripts.sync_ticnote.call_llm")
def test_process_file_tree(mock_call_llm, mock_write_fm):
    # Mock LLM response
    mock_call_llm.return_value = "This is a mock summary of the meeting."
    
    # Mock client
    mock_client = MagicMock()
    mock_client.get_file_detail.return_value = {
        "recordId": "123",
        "fileId": "456",
        "fileName": "meeting.mp3",
        "status": 2,  # COMPLETED
        "transcribeJson": json.dumps([{"speaker": "A", "text": "Hello world"}]),
        "summaryJson": None
    }
    
    file_tree = [
        {
            "type": "file",
            "id": "123",
            "name": "meeting.mp3"
        }
    ]
    
    base_dir = Path("/tmp/mock_ticnote_dir")
    
    # Run
    process_file_tree(mock_client, "Project X", file_tree, base_dir)
    
    # Verify raw file and insights file were written
    assert mock_write_fm.call_count == 2
    
    # Check raw call arguments
    args1 = mock_write_fm.call_args_list[0]
    raw_path = args1[0][0]
    raw_fm = args1[0][1]
    raw_body = args1[0][2]
    
    assert str(raw_path).endswith("123_raw.md")
    assert raw_fm["recordId"] == "123"
    assert "**A**: Hello world" in raw_body
    
    # Check insights call arguments
    args2 = mock_write_fm.call_args_list[1]
    insights_path = args2[0][0]
    insights_fm = args2[0][1]
    insights_body = args2[0][2]
    
    assert str(insights_path).endswith("123_insights.md")
    assert insights_fm["recordId"] == "123"
    assert "This is a mock summary" in insights_body
