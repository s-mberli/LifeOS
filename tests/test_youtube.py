import pytest
from scripts.core.youtube import extract_video_id, clean_youtube_url

def test_extract_video_id_watch_url():
    assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_short_url():
    assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert extract_video_id("youtu.be/dQw4w9WgXcQ?t=10") == "dQw4w9WgXcQ"

def test_extract_video_id_embed_url():
    assert extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_invalid_url():
    assert extract_video_id("https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw") is None
    assert extract_video_id("https://example.com") is None
    assert extract_video_id("just some text") is None

def test_clean_youtube_url_channel():
    assert clean_youtube_url("https://www.youtube.com/@mkbhd") == "https://www.youtube.com/@mkbhd/videos"
    assert clean_youtube_url("https://youtube.com/@mkbhd/") == "https://youtube.com/@mkbhd/videos"

def test_clean_youtube_url_channel_already_has_videos():
    assert clean_youtube_url("https://www.youtube.com/@mkbhd/videos") == "https://www.youtube.com/@mkbhd/videos"

def test_clean_youtube_url_non_channel():
    assert clean_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
