# 🤖 MarkusOS Agent Guidelines & Architecture

This document outlines the architecture, coding patterns, and rules that autonomous coding agents (and human developers) must follow when modifying the **MarkusOS** codebase.

---

## 🏛️ Codebase Architecture

### 1. `src/core/` — Business Logic (Pure Python)
All core capabilities are modularized inside `src/core/`. Do not write business logic directly inside Streamlit files or standalone root scripts.

- [frontmatter.py](src/core/frontmatter.py): Reading, writing, and updating YAML frontmatter. **Always use this module** instead of hand-rolled string split parsers.
- [youtube.py](src/core/youtube.py): Centralized yt-dlp execution and YouTube metadata/transcript fetching.
- [web.py](src/core/web.py): BeautifulSoup/Jina/Reddit fetching and parsing helpers.
- [experts.py](src/core/experts.py): Managing expert directories, reference files (`*-ref.md`), and synthesizing playbooks.
- [ingest.py](src/core/ingest.py): The main entry point orchestrating resource ingestion.
- [llm_client.py](src/core/llm_client.py): Unified LLM wrapper supporting simple prompts or messages.
### 2. `apps/streamlit-chat/` — Streamlit UI
The Streamlit app is split into decoupled UI components.

- `app.py`: A lightweight entry point orchestrating the sidebar and chat components.
- `ui/sidebar.py`: Side navigation and URL ingestion form.
- `ui/chat.py`: Chat dialog body, routing to experts, and citations.
- `ui/modals.py`: Dialog modals for settings, the knowledge library, and expert creation.
- `ui/helpers.py`: Pure Python helpers for database/search (no Streamlit UI calls, fully unit-testable).

### 3. `scripts/` & `automation_outbox` — Event-Driven Automation Pipeline
MarkusOS implements an event-driven automation outbox to bridge note ingestion and autonomous actions (like weekly code reviews and PR generation by the Hermes agent) without calling heavy LLMs on every single ingestion.

- **Outbox Ingestion Hook**: Inside `src/core/ingest.py` (after saving a note), a record is inserted into `automation_outbox` in `indexes/lifeos.db`.
- **Triage Worker (`scripts/triage_outbox.py`)**: A lightweight keyword-based scanner (AI, Architecture, Github, Python, etc.) that filters and scores notes cheaply.
- **Weekly Hermes Runner (`scripts/weekly_hermes_run.py`)**: A weekly pipeline orchestrated by cron that aggregates all triaged actionable notes, feeds them to the Hermes Agent in `--oneshot` mode, runs the test suite, and opens Pull Requests to propose changes.

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

---

## 🚀 Hermes Proposal Implementation Workflow

When the user says **"implement this proposal"** (or references a file in `data/inbox/proposals/`), you MUST follow this exact workflow. No skipping steps.

### Step 0: Activate Skills
1. Activate `/caveman` — ultra-compressed communication to reduce token usage.
2. Activate `/spec-driven-development` — validate architecture before writing code.
3. Activate `/code-review-and-quality` — Five-Axis Review on all code produced.

### Step 1: Branch
- **NEVER work on `main` directly.**
- Create a feature branch: `git checkout -b feat/<proposal-slug>`
- All work happens on this branch until the user approves the merge.

### Step 2: Spec & Plan
- Read the proposal file from `data/inbox/proposals/`.
- Write a formal spec following the spec-driven-development template (Objective, Commands, Structure, Boundaries, Success Criteria).
- Present the implementation plan to the user for approval before writing any code.

### Step 3: Implement
- Build the feature incrementally (one task at a time).
- Write unit tests for all new logic in `tests/`. Mock external calls.
- Run `.venv/bin/pytest` after each change to confirm nothing breaks.

### Step 4: Code Review
- Run `scripts/ai_code_reviewer.py` on all modified `.py` files.
- The reviewer performs a Five-Axis Review (Correctness, Readability, Architecture, Security, Performance).
- Auto-fixes are applied automatically. Manual fixes are flagged.

### Step 5: Documentation
- Run `scripts/update_docs.py` to automatically:
  - Append the new feature to `CHANGELOG.md`.
  - Update `README.md` if the feature changes the core architecture.
  - Generate a Mermaid architecture diagram for the new feature.

### Step 6: Merge
- Commit all changes on the feature branch.
- Present a summary to the user.
- **WAIT for explicit user approval** before merging to `main`.
- **NEVER push to GitHub** without explicit user approval.

### Step 7: Proposal Status Update
- After merge, update the proposal file's `## Status` from `Proposed` to `✅ Implemented`.
- If the proposal was rejected during review, update to `❌ Rejected` with a reason.
