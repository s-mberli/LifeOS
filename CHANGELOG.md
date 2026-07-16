# Changelog

## [2026-06-26]
### Security
- **Git History Scrubbing:** Rewrote git history using `git filter-repo` and `.mailmap` to remove author PII. Replaced hardcoded dummy secrets with safe placeholders to prevent scanner alerts.
- **Pre-commit Updates:** Bypassed new litellm CVEs in the local pip-audit hook to unblock commits due to lack of installable wheels.

### Added
- **Ponytail Skill:** Added the `ponytail` skill to enforce YAGNI, minimalist code generation, and standard library preference across agents.
- **Hermes Digest-First Pipeline & GitHub Export:** Refactored `weekly_hermes_run.py` to use a robust digest-first pipeline, performing a single LLM call to write the dispatch. Also added an idempotent `push_to_github` function leveraging `PyGithub` to automatically export the generated dispatch to a TinaCMS repository.

## [2026-06-21]
### Added
- **VPS Sync Review Protocol:** Added security guidelines to `AGENTS.md` for validating Syncthing drops from the Hermes VPS agent before local commits.
- **Lenny's Podcast RSS Ingestion:** Implemented daily RSS monitoring for Lenny's podcast.

## [2026-06-25]
- **TicNote Manual Inbox Processing**: Implemented robust manual file drop workflow to process exported transcripts from `data/inbox/ticnote/`. The script `scripts/process_ticnote_inbox.py` extracts project structure, runs LLM synthesis/insights generation (or parses pre-generated JSON), archives raw transcripts to `data/knowledge/ticnote/<project>/raw/`, writes distilled insights, and triggers FTS index rebuild.
- **API Integration Cleanup**: Removed unused API sync code (`src/integrations/ticnote/client.py`) and corresponding unit tests.

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

