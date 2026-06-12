# Changelog

## [2026-06-12]
### Added
- **AI Code Review Pipeline:** Automated Five-Axis code review (Correctness, Readability, Architecture, Security, Performance) via `scripts/ai_code_reviewer.py`, with auto-fix capability and provenance logging to `ai_code_provenance` in `lifeos.db`.
  - **Source:** [VentureBeat: Anthropic says 80% of its new production code is now authored by Claude](https://venturebeat.com/technology/anthropic-says-80-of-its-new-production-code-is-now-authored-by-claude-how-your-enterprise-can-keep-up?utm_source=tldrai)
- **Hermes Proposal Workflow:** Standardized 7-step implementation workflow added to `AGENTS.md` — branch, spec, implement, review, document, merge, status update — triggered by "implement this proposal".
- **Auto-documentation:** `scripts/update_docs.py` auto-updates `CHANGELOG.md`, `README.md`, and generates Mermaid diagrams on feature completion.

