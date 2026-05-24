# LifeOS MVP Scope

The goal of the Minimum Viable Product (MVP) is to establish a flawless, reliable **Personal Expert Network** pipeline without the brittle bloat of complex automation layers.

## What is Included in the MVP

The MVP focuses strictly on the local curation and retrieval of insights.

- **Ingestion Pipeline**: Reliable processing of YouTube URLs, web articles, and raw text.
- **Insight Notes**: LLM-driven synthesis of raw sources into structured, actionable markdown files (`type: insight_note`).
- **Expert Profiles**: Curation of specific experts into dedicated profiles containing their Playbook, Principles, and Evidence.
- **Local Search Engine**: Instant SQLite FTS5 full-text search across the knowledge base.
- **Ask Expert (Scoped Retrieval)**: The ability to ask the LLM questions using only the context of a specifically selected Expert, filtering out irrelevant noise.
- **Human-in-the-Loop Updates**: The system can suggest updates to an Expert's profile based on new sources, but a human must approve and apply them.

## What is Excluded (Deferred)

To maintain stability and portability, the following concepts are intentionally excluded from the current MVP:

- **Full LifeOS Tracking**: No habit trackers, daily dashboards, workout logs, or task managers.
- **n8n / Complex Automations**: No external automation dependencies that require complex orchestration.
- **Telegram / Voice Input**: The UI is strictly browser-based via Streamlit for now.
- **Autonomous Agents**: The system does not act on its own or modify source files without human intervention.
- **Deployment / Cloud Hosting**: This is a local-first application designed to run on your own machine.
- **Vector Databases**: Simple keyword and FTS search is sufficient for personal scale. We avoid the overhead of generating embeddings and running Qdrant/Chroma.
