# Scripts

This folder contains the Python scripts and automation logic for LifeOS.

## Planned Scripts
- `ingest_resource.py`: Script to parse incoming text, summarize it via LLM, and save a markdown note.
- `classify_input.py`: The router script that decides which mode should handle an input.
- `build_fts_index.py`: Script to chunk markdown files and build a full-text search database (SQLite).
- `search_knowledge.py`: CLI or library to query the FTS index.
- `chat_with_mode.py`: Interface to interact directly with a specific mode (e.g. `python chat_with_mode.py --mode flow-temple-operator "What should I post today?"`).

> **Note**: Start by building the "Resource Inbox Workflow" using `ingest_resource.py` and `classify_input.py`.
