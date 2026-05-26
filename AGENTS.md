# 🤖 MarkusOS Agent Guidelines & Architecture

This document outlines the architecture, coding patterns, and rules that autonomous coding agents (and human developers) must follow when modifying the **MarkusOS** codebase.

---

## 🏛️ Codebase Architecture

### 1. `src/core/` — Business Logic (Pure Python)
All core capabilities are modularized inside `src/core/`. Do not write business logic directly inside Streamlit files or standalone root scripts.

- [frontmatter.py](file:///Users/markus/markusos/src/core/frontmatter.py): Reading, writing, and updating YAML frontmatter. **Always use this module** instead of hand-rolled string split parsers.
- [youtube.py](file:///Users/markus/markusos/src/core/youtube.py): Centralized yt-dlp execution and YouTube metadata/transcript fetching.
- [web.py](file:///Users/markus/markusos/src/core/web.py): BeautifulSoup/Jina/Reddit fetching and parsing helpers.
- [experts.py](file:///Users/markus/markusos/src/core/experts.py): Managing expert directories, reference files (`*-ref.md`), and synthesizing playbooks.
- [ingest.py](file:///Users/markus/markusos/src/core/ingest.py): The main entry point orchestrating resource ingestion.
- [llm_client.py](file:///Users/markus/markusos/src/core/llm_client.py): Unified LLM wrapper supporting simple prompts or messages.

### 2. `apps/streamlit-chat/` — Streamlit UI
The Streamlit app is split into decoupled UI components.

- `app.py`: A lightweight entry point orchestrating the sidebar and chat components.
- `ui/sidebar.py`: Side navigation and URL ingestion form.
- `ui/chat.py`: Chat dialog body, routing to experts, and citations.
- `ui/modals.py`: Dialog modals for settings, the knowledge library, and expert creation.
- `ui/helpers.py`: Pure Python helpers for database/search (no Streamlit UI calls, fully unit-testable).

---

## ⚠️ Safety & Invariant Rules

1. **NO Programmatic Patching**: Never write scripts that modify Python source code using `.replace()` or regex replacements. Modifying Python files programmatically leads to syntax errors and fragile builds. Use standard git tools or manual edits.
2. **Environment & Secrets**: Never commit `.env` or files containing keys to Git. Private user files under `data/private/` must also be kept out of Git.
3. **Paths**: Always use `pathlib.Path` instead of string path joins. Locate directories relative to the repository root.
4. **YAML parsing**: Never split files manually to extract YAML. Use the core `frontmatter` API.

---

## 🧪 Development & Testing

Run all unit and integration tests before submitting changes:
```bash
.venv/bin/pytest
```
All new core logic must include unit tests in the `tests/` directory. Mock external network/LLM calls.
