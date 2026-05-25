"""
scripts/core/youtube.py — All YouTube-related I/O for LifeOS.

Consolidates YouTube fetching logic from ingest_resource.py and
channel_ingest.py into a single authoritative module.

All subprocess calls have explicit ``timeout`` and ``capture_output=True``.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_VIDEO_ID_RE = re.compile(
    r"(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)"
    r"([^\"&?/ ]{11})"
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_yt_dlp(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    """Run ``yt-dlp`` with the given extra arguments.

    Always sets ``capture_output=True`` and ``text=True``.  Never raises on
    non-zero exit — callers inspect ``returncode`` themselves.

    Args:
        args:    Additional command-line arguments appended after ``yt-dlp``.
        timeout: Maximum seconds to wait before raising
                 :class:`subprocess.TimeoutExpired`.

    Returns:
        A :class:`subprocess.CompletedProcess` instance.

    Raises:
        subprocess.TimeoutExpired: If the process runs longer than *timeout*.
    """
    cmd = ["yt-dlp"] + args
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def clean_youtube_url(url: str) -> str:
    """Normalise a YouTube channel URL to its ``/videos`` tab.

    For channel URLs (containing ``@``), appends ``/videos`` so that
    yt-dlp retrieves standard uploads rather than shorts.

    Args:
        url: Raw channel or video URL.

    Returns:
        Cleaned URL string.
    """
    url = url.strip()
    if "@" in url and not url.endswith("/videos"):
        url = url.rstrip("/") + "/videos"
    return url


def extract_video_id(url: str) -> str | None:
    """Extract the 11-character YouTube video ID from a URL.

    Args:
        url: Any YouTube watch/short/embed URL.

    Returns:
        The 11-character video ID, or ``None`` if the URL is not recognised.
    """
    url = url.strip().strip(' "\'.,;!)]>')
    match = _VIDEO_ID_RE.search(url)
    return match.group(1) if match else None


def fetch_video_metadata(url: str) -> dict:
    """Fetch title, uploader, and channel for a single YouTube video.

    Uses ``yt-dlp -j`` to retrieve JSON metadata without downloading.

    Args:
        url: YouTube video URL.

    Returns:
        Dict with keys ``title``, ``uploader``, ``channel``, plus ``error``
        if something went wrong.
    """
    url = url.strip().strip(' "\'.,;!)]>')
    try:
        result = run_yt_dlp(["-j", "--no-warnings", url], timeout=15)
        if result.returncode != 0:
            return {"title": "", "uploader": "", "channel": "", "error": result.stderr.strip()}
        data: dict = json.loads(result.stdout)
        return {
            "title": data.get("title", ""),
            "uploader": data.get("uploader", ""),
            "channel": data.get("channel", data.get("uploader", "")),
        }
    except subprocess.TimeoutExpired:
        return {"title": "", "uploader": "", "channel": "", "error": "yt-dlp timed out (15 s)"}
    except Exception as exc:
        return {"title": "", "uploader": "", "channel": "", "error": str(exc)}


def fetch_channel_metadata(channel_url: str) -> dict:
    """Fetch the creator/uploader name from a YouTube channel URL.

    Args:
        channel_url: YouTube channel URL (e.g. ``https://youtube.com/@handle``).

    Returns:
        Dict with key ``uploader`` and optionally ``error``.
    """
    try:
        result = run_yt_dlp(
            ["--print", "%(uploader)s", "--playlist-items", "1", channel_url],
            timeout=30,
        )
        if result.returncode != 0:
            return {"uploader": "Unknown Creator", "error": result.stderr.strip()}

        lines = [
            line.strip()
            for line in result.stdout.split("\n")
            if line.strip() and not line.startswith("WARNING")
        ]
        uploader = "Unknown Creator"
        for line in lines:
            if "urllib3" not in line and "Deprecated" not in line:
                uploader = line
                break
        return {"uploader": uploader}
    except subprocess.TimeoutExpired:
        return {"uploader": "Unknown Creator", "error": "yt-dlp timed out (30 s)"}
    except Exception as exc:
        return {"uploader": "Unknown Creator", "error": str(exc)}


def fetch_recent_videos(channel_url: str, max_videos: int = 5) -> list[str]:
    """Return up to *max_videos* recent video URLs from a YouTube channel.

    Args:
        channel_url: YouTube channel URL.
        max_videos:  Maximum number of video URLs to return.

    Returns:
        List of YouTube video URLs (may be empty on error).
    """
    try:
        result = run_yt_dlp(
            [
                "--flat-playlist",
                "--print", "webpage_url",
                "--playlist-end", str(max_videos),
                channel_url,
            ],
            timeout=60,
        )
        urls: list[str] = []
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line.startswith("http"):
                urls.append(line)
                if len(urls) >= max_videos:
                    break
        return urls
    except Exception:
        return []


def fetch_transcript(url: str) -> str | None:
    """Fetch the auto-generated or manual transcript for a YouTube video.

    Uses the ``youtube_transcript_api`` library.  Returns ``None`` if the
    transcript is unavailable or the library is not installed.

    Args:
        url: YouTube video URL.

    Returns:
        Plain-text transcript joined by spaces, or ``None``.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore

        srt = YouTubeTranscriptApi().fetch(video_id)
        return " ".join(entry.text for entry in srt)
    except Exception as exc:
        print(f"  [!] Failed to fetch YouTube transcript: {exc}")
        return None


def save_transcript(transcript: str, video_id: str, out_dir: Path) -> Path:
    """Write a raw transcript to ``<out_dir>/<video_id>_transcript.txt``.

    Creates *out_dir* if it does not exist.

    Args:
        transcript: Plain-text transcript string.
        video_id:   YouTube video ID (used as filename prefix).
        out_dir:    Directory to write the transcript file into.

    Returns:
        Path to the saved transcript file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{video_id}_transcript.txt"
    dest.write_text(transcript, encoding="utf-8")
    return dest
