import pytest
from unittest.mock import patch, MagicMock
from src.integrations.ticnote.client import TicNoteClient

def test_client_init_and_url_resolving():
    # Test valid key prefixes
    client_cn = TicNoteClient(api_key="tncn_sk_abc123")
    assert client_cn.base_url == "https://voice-api.ticnote.cn"
    
    client_overseas = TicNoteClient(api_key="tnovs_sk_abc123")
    assert client_overseas.base_url == "https://ainote-api.mobvoi.com"
    
    # Test invalid key prefix
    with pytest.raises(ValueError, match="Invalid API Key prefix"):
        TicNoteClient(api_key="invalid_prefix_sk_123")

@patch("requests.post")
def test_login_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "code": 0,
        "data": {
            "token": "mock_bearer_token_123"
        }
    }
    mock_post.return_value = mock_response
    
    client = TicNoteClient(api_key="tncn_sk_123")
    token = client.login()
    
    assert token == "mock_bearer_token_123"
    assert client.token == "mock_bearer_token_123"
    mock_post.assert_called_once_with(
        "https://voice-api.ticnote.cn/api/p1/appkey/login",
        json={"appkey": "tncn_sk_123"},
        timeout=10
    )

@patch("requests.post")
def test_login_failure(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "code": 11865,
        "msg": "Appkey not found"
    }
    mock_post.return_value = mock_response
    
    client = TicNoteClient(api_key="tncn_sk_123")
    with pytest.raises(Exception, match="Login failed: Appkey not found"):
        client.login()

@patch("requests.get")
@patch("requests.post")
def test_list_projects(mock_post, mock_get):
    # Mock login first
    mock_login_resp = MagicMock()
    mock_login_resp.json.return_value = {"code": 0, "data": {"token": "tkn"}}
    mock_post.return_value = mock_login_resp
    
    # Mock list projects
    mock_get_resp = MagicMock()
    mock_get_resp.json.return_value = {
        "chats": [{"id": "1", "name": "Project A"}]
    }
    mock_get.return_value = mock_get_resp
    
    client = TicNoteClient(api_key="tncn_sk_123")
    projects = client.list_projects()
    
    assert len(projects) == 1
    assert projects[0]["name"] == "Project A"
    mock_get.assert_called_with(
        "https://voice-api.ticnote.cn/api/v2/file-index/chats",
        headers={"Authorization": "Bearer tkn", "Content-Type": "application/json"},
        timeout=15
    )
