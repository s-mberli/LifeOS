# Changelog

## [2026-06-20]
### Added
- **Unified Memory Core (sqlite-vec + FTS5 RRF hybrid RAG):** Re-architected storage and retrieval layer for scale. Added dynamic loading of `sqlite-vec` extension and schema definitions for vector/chunk mapping (`vec_docs` and `doc_chunks` tables). Implemented hybrid search combining FTS5 keyword and sqlite-vec KNN queries with Reciprocal Rank Fusion (RRF). Added OpenRouter-based embedding generation (`nomic-embed-text-v1.5`) and LLM context briefing synthesis. Removed redundant threaded re-indexing in `triage_outbox.py`.
  - **Source:** [X.com Post: mem0ai unified memory](https://x.com/mem0ai/status/2061822612398014782?utm_source=tldrai)

## [2026-06-12]
### Added
- **Self-Repairing Agent Harness:** New `src/core/agent_harness.py` module with `execute_with_repair` decorator that catches agent failures (JSON parsing errors, timeouts) and applies repair strategies. Supports `background` mode (exponential backoff, up to 3 retries) for unattended scripts and `ui` mode (fast-fail, 1 retry) for interactive apps. Repair logs stored in `agent_repair_logs` SQLite table.
  - **Source:** [X.com Post: Self-repairing agent harness](https://x.com/akshay_pachaar/status/2064051835636498924?utm_source=tldrai)

### Changed
- `.gitignore` updated to exclude `*.plist` files while tracking `*.example.plist` templates.
- Added `com.lifeos.hermes_weekly.example.plist` and `com.lifeos.tldr_ingest.example.plist` as macOS LaunchAgent configuration templates for scheduled weekly Hermes runs and daily TLDR ingestion.

## [2026-06-12]
### Added
- **AI Code Review Pipeline:** Automated Five-Axis code review (Correctness, Readability, Architecture, Security, Performance) via `scripts/ai_code_reviewer.py`, with auto-fix capability and provenance logging to `ai_code_provenance` in `lifeos.db`.
  - **Source:** [VentureBeat: Anthropic says 80% of its new production code is now authored by Claude](https://venturebeat.com/technology/anthropic-says-80-of-its-new-production-code-is-now-authored-by-claude-how-your-enterprise-can-keep-up?utm_source=tldrai)
- **Hermes Proposal Workflow:** Standardized 7-step implementation workflow added to `AGENTS.md` — branch, spec, implement, review, document, merge, status update — triggered by "implement this proposal".
- **Auto-documentation:** `scripts/update_docs.py` auto-updates `CHANGELOG.md`, `README.md`, and generates Mermaid diagrams on feature completion.

