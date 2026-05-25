# 🧭 LifeOS Agents & Architecture

This document describes the agent system, prompt injection strategy, and modular core components of **LifeOS**.

---

## 🏛️ System Design Principles

LifeOS operates as a local-first cognitive assistant. It uses specialized **Experts** rather than a single monolithic chatbot. Each expert is a stateful persona grounded in specific subsets of your knowledge base.

### 1. Separation of Layers
- **System Layer**: Code, system prompts, schemas, and configurations (`scripts/`, `apps/`, `config/`, `modes/`).
- **User Layer**: Your curated knowledge base, expert profiles, and private resources (`data/`, `config/profile.yml`). The application reads the User Layer to construct context but never overwrites human-written files without explicit approval.

### 2. Retrieval-Augmented Generation (RAG) Flow
When you interact with an Expert, LifeOS executes the following pipeline:
```
User Query ──> Router ──> Retrieve Profile & Playbook ──> FTS SQLite Search ──> Grounded Prompt Injection ──> LLM Call ──> Answer with Citations
```

---

## 🗺️ Expert Routing & System Modes

LifeOS can route user queries to specific experts. Routing is governed by:
1. **Manual Selection**: Select a specific expert from the sidebar.
2. **Auto-Routing**: Natural language queries are routed to experts based on declarative mapping (`config/domain_map.yaml`) and frontmatter tags.

### Core System Modes
System modes guide the development assistant when operating within the workspace:
- **`router`**: Evaluates incoming queries, resolves the target domain, and selects the matching expert.
- **`research-resource`**: System mode for fetching web pages, downloading transcripts, and summarizing raw resources.
- **`creator-wisdom`**: Mode for reading multiple resource profiles from a single channel or creator and synthesizing an integrated expert playbook.
- **`ai-builder`**: Technical workspace mode for writing clean python code, scripts, and streamlit UI modules.

---

## 📦 Modular Directory Structure

### `scripts/core/` — Business Logic
- **`frontmatter.py`**: Reads and writes YAML frontmatter in Markdown notes. Always use this module to keep frontmatter format consistent.
- **`youtube.py`**: Downloads transcripts and queries metadata for YouTube videos and channels using `yt-dlp`.
- **`web.py`**: Fetches HTML web pages and extracts content/metadata safely.
- **`experts.py`**: Synthesizes expert profiles from ingested resources and manages references.
- **`ingest.py`**: Main pipeline entry point to coordinate fetching, summarizing, and saving resources.

### `apps/streamlit-chat/ui/` — Streamlit UI Modules
- **`helpers.py`**: Pure Python helper functions (no Streamlit imports), ensuring the core UI logic is fully testable.
- **`modals.py`**: Dialog overlays for configuration and library management.
- **`sidebar.py`**: Controls for resource ingestion and API configurations.
- **`chat.py`**: Chat rendering loop, message history management, and LLM chat client wrapping.
