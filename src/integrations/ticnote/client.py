import os
import requests
from typing import List, Dict, Any, Optional

class TicNoteClient:
    BASE_URLS = [
        ("tnovs_sit_sk_", "https://ainote-sit-api.mobvoi.com"),
        ("tnovs_sk_",     "https://ainote-api.mobvoi.com"),
        ("tncn_sit_sk_",  "https://voice-api-sit.ticnote.cn"),
        ("tncn_sk_",      "https://voice-api.ticnote.cn"),
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TICNOTE_API_KEY")
        if not self.api_key:
            raise ValueError("TICNOTE_API_KEY is not set in environment or constructor")
        
        self.base_url = self._resolve_base_url(self.api_key)
        self.token = None

    def _resolve_base_url(self, api_key: str) -> str:
        for prefix, url in self.BASE_URLS:
            if api_key.startswith(prefix):
                return url
        raise ValueError(
            f"Invalid API Key prefix: '{api_key[:15]}...'. "
            f"Must start with one of: {[p for p, _ in self.BASE_URLS]}"
        )

    def login(self) -> str:
        url = f"{self.base_url}/api/p1/appkey/login"
        payload = {"appkey": self.api_key}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"Login failed: {data.get('msg')} (code {data.get('code')})")
            
        self.token = data["data"]["token"]
        return self.token

    def _get_headers(self) -> dict:
        if not self.token:
            self.login()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def list_projects(self) -> List[Dict[str, Any]]:
        """GET /api/v2/file-index/chats"""
        url = f"{self.base_url}/api/v2/file-index/chats"
        response = requests.get(url, headers=self._get_headers(), timeout=15)
        response.raise_for_status()
        return response.json().get("chats", [])

    def list_files(self, project_id: str) -> List[Dict[str, Any]]:
        """GET /api/v1/file-index/file-tree?rootId={project_id}"""
        url = f"{self.base_url}/api/v1/file-index/file-tree"
        params = {"rootId": project_id}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=15)
        response.raise_for_status()
        return response.json().get("fileTree", [])

    def get_file_detail(self, record_id: str) -> Dict[str, Any]:
        """GET /api/v2/file-index/file-detail/{record_id}"""
        url = f"{self.base_url}/api/v2/file-index/file-detail/{record_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"Failed to fetch file detail: {data.get('msg')}")
        return data.get("data", {})
