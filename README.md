# LifeOS — Personal Expert Network

LifeOS is a **local-first personal knowledge OS** that turns YouTube videos, articles, and raw notes into structured expert insights. It routes your questions to curated AI experts built from your own knowledge library — no cloud databases, no vector stores, no amnesia.

All data persists as Markdown files with YAML frontmatter in `data/`. Search is powered by SQLite FTS5.

![LifeOS UI Screenshot](/Users/markus/.gemini/antigravity/scratch/lifeos/docs/screenshot.png)

---

## Architecture

- **`scripts/core/`** — Pure Python business logic (ingestion, experts, YAML, YouTube)
- **`apps/streamlit-chat/`** — Streamlit UI, split into modular `ui/` sub-modules
- **`data/knowledge/`** — Insight notes (Markdown + YAML frontmatter)
- **`data/experts/`** — Expert profiles, playbooks, and principles
- **`config/`** — Declarative config files (domain map, profile, models)
- **`indexes/`** — SQLite FTS5 search index (auto-rebuilt, not committed)

---

## Quick Start

```bash
# 1. Clone and install
git clone <your-repo-url>
cd lifeos
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
cp config/profile.example.yml config/profile.yml
# Edit .env and add your OpenRouter / Azure OpenAI API key

# 3. Run the app
streamlit run apps/streamlit-chat/app.py
```

---

## Project Structure

```
lifeos/
├── apps/
│   └── streamlit-chat/
│       ├── app.py              # Main Streamlit entry point
│       └── ui/
│           ├── helpers.py      # Pure Python helpers (no st.* calls)
│           ├── modals.py       # @st.dialog modal definitions
│           ├── sidebar.py      # Sidebar rendering and URL form
│           └── chat.py         # Chat loop, expert routing, attribution
├── config/
│   ├── domain_map.yaml         # Domain → expert slug routing (edit here)
│   ├── profile.example.yml     # Template — copy to profile.yml
│   └── models.yml              # LLM model config (gitignored)
├── data/
│   ├── experts/                # Expert directories (committed)
│   └── knowledge/              # Insight notes (committed)
├── indexes/                    # SQLite FTS5 DB (gitignored, auto-rebuilt)
├── scripts/
│   └── core/
│       ├── frontmatter.py      # YAML frontmatter read/write
│       ├── youtube.py          # yt-dlp and transcript operations
│       ├── web.py              # Web page fetching and metadata
│       ├── experts.py          # Expert management and synthesis
│       └── ingest.py           # Ingestion pipeline entry point
├── .env.example
├── requirements.txt
└── README.md
```

---

## How to Add an Expert

1. In the Streamlit UI, open the **Experts** tab
2. Paste a YouTube channel URL or video URL
3. Click **Build Expert** — LifeOS fetches the transcript, synthesises a persona, and writes the expert profile to `data/experts/`
4. Review the generated profile and playbook, then start chatting

---

## Configuration

### `config/domain_map.yaml`

Controls which expert is auto-suggested when an insight is ingested. Keys are the `domain` field values from insight frontmatter; values are expert directory slugs under `data/experts/`.

```yaml
ai-platform: expert--ai-systems-architect
flow-temple: expert--flow-temple-strategist
```

Add new entries here when creating new experts — **no code changes needed**.

### Environment Variables (`.env`)

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key (alternative) |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint URL |

---

## Data Privacy

| Path | Status | Reason |
|---|---|---|
| `data/knowledge/` | ✅ Committed | Curated public insights |
| `data/experts/` | ✅ Committed | Expert profiles and playbooks |
| `data/private/` | 🔒 Gitignored | Personal/sensitive data |
| `.env` | 🔒 Gitignored | API keys and secrets |
| `config/profile.yml` | 🔒 Gitignored | Personal profile info |
| `indexes/*.db` | 🔒 Gitignored | Auto-rebuilt SQLite index |

---

## Development

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_frontmatter.py -v

# Rebuild the search index
python scripts/core/ingest.py --rebuild-index
```

All business logic lives in `scripts/core/` as pure Python modules — no Streamlit imports, fully unit-testable.
