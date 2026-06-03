---
name: lifeos-ingest
description: Ingests a new resource (YouTube URL, webpage, or local file) into the LifeOS local database.
---

# LifeOS Ingest Skill

Use this skill whenever the user asks you to "ingest", "download", or "add" a new YouTube video, web page, or document to their LifeOS system.

## Instructions
1. The user will provide a URL or a file path.
2. You must run the ingestion script using the `run_command` tool.
3. The command to run is: `python3 src/core/ingest.py "<URL_OR_PATH>"`
4. Do not attempt to summarize the video yourself. The ingestion pipeline handles transcript downloading, web fetching, and auto-synthesis of the expert.
5. Once the command completes, report to the user that the resource has been ingested and is available in the LifeOS database.

Example:
User: "/ingest https://www.youtube.com/watch?v=dQw4w9WgXcQ"
You: [Run `python3 src/core/ingest.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"`]
