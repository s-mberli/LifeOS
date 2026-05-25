# 🗺️ LifeOS Platform Roadmap

This document outlines the product direction and upcoming features for the **LifeOS** platform. As a local-first system, development prioritizes speed, privacy, and modularity.

> **Our Philosophy:** LifeOS is built in phases. The math and data foundations form the floor. The personalized multi-agent intelligence forms the roof.

---

## 📅 Phase 1 — Ingestion & Expert Profiles (MVP)
> *Get the raw data in and start conversing.*

* [x] **Core Ingestion Pipeline**: Auto-download YouTube transcripts, clean web pages, and ingest raw notes.
* [x] **Expert Profile Synthesis**: Automatically generate a structured expert persona (profile, playbook, and principles) based on channel/content uploads.
* [x] **Local SQLite Search**: SQLite FTS5 database setup to perform rapid keyword-based retrieval.
* [x] **Grounded Chat Interface**: A multi-turn chat experience that routes queries to selected experts and provides exact source citations.

---

## 🚀 Phase 2 — Testing, Refactoring & Cleanup
> *Stabilizing the foundation.*

* [x] **Modular Architecture**: Split the heavy monolithic streamlit script into clean logic modules (`core/`) and UI modules (`ui/`).
* [x] **Strict Domain Routing**: Connect domains to experts using declarative configurations (`config/domain_map.yaml`).
* [x] **Robust Test Coverage**: Added pytest fixtures and coverage for frontmatter reading/writing, YouTube transcript downloading, and integration testing.
* [x] **Repository Packaging**: Purged private notes/databases from Git history and established a secure public-private split.

---

## 🏃 Phase 3 — Enhanced Expert Management & Local Bulk Ingestion
> *Bringing in the archives and tweaking the personas.*

* [ ] **Playbook Editing**: Allow users to edit expert profiles, principles, and playbooks directly from the Streamlit UI.
* [ ] **Local Folder Bulk Ingestion**: Add support for selecting a local directory containing `.txt` or `.md` files (such as journal/transcript backups) and batch-ingesting them into the knowledge base.
* [ ] **Improved Audio Ingestion**: Integration of local Whisper APIs to transcribe voice notes and local audio files.

---

## 🔮 Phase 4 — Hybrid Retrieval & Offline LLMs
> *100% offline, fully autonomous.*

* [ ] **Hybrid Search**: Combine keyword-based SQLite FTS5 search with dense vector embeddings (e.g., using Chromadb or SQLite-vec) for semantic retrieval.
* [ ] **Local LLM Execution**: Native support for running lightweight models locally (via Ollama or Llama.cpp) to enable 100% offline usage.
* [ ] **Self-Improvement Candidates**: Enable the system to propose architecture, configuration, or playbook updates to itself based on new insights (requiring manual human approval).
