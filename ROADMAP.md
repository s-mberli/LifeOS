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
* [x] **Manual Personal Memory**: User-controlled UI to inject persistent context, preferences, and custom instructions into chat sessions.
* [ ] **Local Folder Bulk Ingestion**: Add support for selecting a local directory containing `.txt` or `.md` files (such as journal/transcript backups) and batch-ingesting them into the knowledge base.
* [ ] **Improved Audio Ingestion**: Integration of local Whisper APIs to transcribe voice notes and local audio files.

---

## 🔮 Phase 4 — Hybrid Retrieval & Offline LLMs
> *Broader retrieval and an optional offline inference path.*

* [x] **Hybrid Search**: Combine keyword-based SQLite FTS5 search with dense vector embeddings (using `sqlite-vec`) for semantic retrieval combined via Reciprocal Rank Fusion (RRF).
* [ ] **Local LLM Execution**: Native support for running lightweight models locally (via Ollama or Llama.cpp) to enable 100% offline usage.
* [x] **Reviewable Improvement Candidates**: The LifeOS runner can draft architecture proposals from triaged notes for a person to assess.
* [ ] **Proposal-to-PR Workflow**: Implement, test, review, and open a pull request from an approved proposal. This is a future capability, not part of the current runner.
