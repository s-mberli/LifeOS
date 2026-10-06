import os
import tempfile
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pathlib import Path
from urllib.parse import urlsplit

# Adjust path if needed
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.core.ingest import process_one_file
from core.web import clipper_ingestion, validate_public_url
from core.youtube import extract_video_id

app = FastAPI(title="MarkusOS Ingestion API", version="1.0.0")

# Enable CORS strictly for browser extensions to prevent malicious websites
# from hitting localhost API and triggering unauthorized ingestions (SSRF).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "moz-extension://*",
        "chrome-extension://*",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    url: str

def run_ingestion(url: str):
    """Background task to run the ingestion pipeline."""
    # process_one_file expects a file path containing the content.
    # We create a temporary file with the URL in it.
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(url)
            temp_path = temp_file.name

        print(f"Starting ingestion for URL: {url} via temp file {temp_path}")
        with clipper_ingestion():
            result = process_one_file(temp_path, use_ai=True)
        print(f"Ingestion result: {result.get('success')} - {result.get('out_filepath') or result.get('error')}")
        
        # Cleanup temp file if it wasn't moved/deleted by the pipeline
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        print(f"Error during ingestion: {e}")

@app.post("/ingest")
async def ingest_url(request: IngestRequest, background_tasks: BackgroundTasks):
    try:
        url = validate_public_url(request.url, resolve=True)
        host = (urlsplit(url).hostname or "").rstrip(".").lower()
        # The ingestion pipeline routes YouTube-looking strings to yt-dlp.
        # Give it only a canonical watch URL with an extracted video ID.
        if "youtube.com" in host or "youtu.be" in host:
            if host not in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}:
                raise ValueError("Invalid YouTube URL.")
            video_id = extract_video_id(url)
            if not video_id:
                raise ValueError("Invalid YouTube video URL.")
            url = f"https://www.youtube.com/watch?v={video_id}"
            validate_public_url(url, resolve=True)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    # Run ingestion in the background so the extension gets an immediate response
    background_tasks.add_task(run_ingestion, url)
    return {"status": "accepted", "message": f"URL {url} accepted for ingestion"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
