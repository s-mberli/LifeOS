# 🧭 LifeOS — Personal Expert Network

LifeOS is a **local-first personal knowledge operating system** that converts YouTube videos, web articles, and raw markdown notes into structured expert insights. It routes your natural language questions to curated AI experts built dynamically from your own knowledge library—with zero cloud databases, zero vector stores, and zero data amnesia.

All data persists locally as Markdown files with YAML frontmatter under `data/`. Search and retrieval are powered by a local SQLite FTS5 (Full-Text Search) index.

---

## 🛠️ Architecture

- **`scripts/core/`** — Pure Python business logic (ingestion pipeline, expert profile synthesis, YAML frontmatter parser, YouTube metadata & transcript downloader).
- **`apps/streamlit-chat/`** — Clean, modular Streamlit UI.
- **`data/knowledge/`** — Curated, structured insight notes (Markdown + YAML frontmatter).
- **`data/experts/`** — Synthesized expert profiles, playbooks, and principles.
- **`config/`** — Declarative system configurations (domain-to-expert mapping, models, profile templates).
- **`indexes/`** — Local SQLite FTS5 search index (automatically rebuilt at startup, gitignored).

---

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/s-mberli/LifeOS.git
cd LifeOS
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
cp config/profile.example.yml config/profile.yml
```
Edit the `.env` file and add your `OPENROUTER_API_KEY` or `AZURE_OPENAI_API_KEY`.

### 3. Run the App
```bash
streamlit run apps/streamlit-chat/app.py
```

---

## 📂 Project Structure

```
LifeOS/
├── apps/
│   └── streamlit-chat/
│       ├── app.py              # Streamlit entry point
│       └── ui/
│           ├── helpers.py      # Pure Python UI helpers (no Streamlit imports)
│           ├── modals.py       # Modal dialog definitions
│           ├── sidebar.py      # Sidebar forms & resource ingestion controls
│           └── chat.py         # Multi-turn chat interface with expert routing
├── config/
│   ├── domain_map.yaml         # Domain → expert slug routing mapping
│   ├── profile.example.yml     # User profile template
│   └── models.yml              # Model selection mappings
├── data/
│   ├── experts/                # Active AI Experts (committed)
│   └── knowledge/              # Insight Notes & public concepts (committed)
├── indexes/                    # SQLite search DB (gitignored, auto-rebuilt)
├── scripts/
│   └── core/
│       ├── frontmatter.py      # Canonical YAML frontmatter read/write utilities
│       ├── youtube.py          # yt-dlp wrapper & transcript fetcher
│       ├── web.py              # Web page fetching & metadata parser
│       ├── experts.py          # Expert management, persona synthesis
│       └── ingest.py           # Orchestrates the ingestion pipeline
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🧠 Creating & Using AI Experts

1. **Build an Expert**: Open the **Experts** tab in the UI. Paste a YouTube channel/video or article URL, and click **Build Expert**. The pipeline downloads transcripts/content, synthesises a unique persona profile, and writes it to `data/experts/`.
2. **Ingest Insights**: Paste any resource URL in the sidebar. LifeOS downloads it, parses it, structures it into an **Insight Note** with standardized YAML metadata, and saves it.
3. **Route & Query**: In the **Ask Expert** tab, select a specialized expert (or let the auto-router choose one). Ask questions and receive detailed answers strictly grounded in your local knowledge base, complete with clickable source citations.

---

## 🔒 Data Privacy & GitHub Safety

LifeOS is designed to be completely safe for public version control while maintaining full privacy for your personal journal or proprietary business notes:

| Path | Version Control | Reason |
|---|---|---|
| `data/knowledge/` | 🔒 Gitignored (except examples) | Your personal insights & research |
| `data/experts/` | 🔒 Gitignored (except examples) | Generated expert playbooks & sources |
| `data/private/` | 🔒 Gitignored | Personal diaries, goals, and business data |
| `.env` | 🔒 Gitignored | API keys and secrets |
| `config/profile.yml` | 🔒 Gitignored | Personal profile configuration |
| `indexes/*.db` | 🔒 Gitignored | SQLite FTS database containing private data |

---

## 🧪 Testing

```bash
# Run the entire test suite
pytest

# Run UI and integration tests specifically
pytest tests/test_ui.py -v
pytest tests/test_integration.py -v
```
All core business logic is isolated from the Streamlit UI layer under `scripts/core/`, making it highly testable and robust.
