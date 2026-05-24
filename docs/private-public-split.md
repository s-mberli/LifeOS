# Public vs. Private Data Split

LifeOS is designed to be a GitHub-safe repository that you can share as a portfolio piece, while keeping your actual journal entries, API keys, and copyrighted transcripts strictly private.

The `.gitignore` file enforces this split.

## Public-Safe (Committed to GitHub)

These folders contain the structural framework, code, and curated knowledge graph.

- `README.md`
- `docs/` — Architectural documentation and roadmap.
- `templates/` — Markdown templates used by the ingestion pipeline.
- `scripts/` — Core Python backend logic.
- `apps/` — Streamlit UI code.
- `.env.example` — A blank template showing what keys are needed.
- `config/profile.example.yml` — A dummy profile config if needed.
- `data/knowledge/insights/` — Your synthesized Insight Notes (safe to share).
- `data/experts/` — Your curated Expert Profiles and synthesized principles (safe to share).

## Private / Local Only (Ignored by Git)

These folders and files remain exclusively on your local machine.

- `.env` — Contains your Anthropic/OpenAI API keys.
- `config/profile.yml` — Your actual user config.
- `data/private/` — Daily notes, personal journal entries, or private captures.
- `data/inbox/` — Raw unverified captures.
- `data/knowledge/ai-resources/raw/` — Raw YouTube transcripts and copyrighted material. **Never commit full transcripts to GitHub.**
- `indexes/` — The SQLite FTS5 database (`lifeos.db`), as it contains indexed private data.
