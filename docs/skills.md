# Skills Concept

In LifeOS, a **Skill** is a stateless, reusable workflow designed to execute a specific cognitive task. By separating workflows into declarative skills, we make the system modular, easy to audit, and prepared for future automation or tool-calling orchestration.

---

## Skill Directory Structure

Every skill is documented and configured in its own folder under `skills/`:

```
skills/<skill-name>/
├── SKILL.md
└── config.yml
```

### 1. `SKILL.md`
The contract. It documents:
- **Purpose**: Why this skill exists.
- **Inputs**: Expected arguments (e.g. `source_url`, `query`, `expert_slug`).
- **Outputs**: Generated files, database updates, or UI responses.
- **Workflow**: Step-by-step logic detailing how inputs map to outputs, including external scripts invoked.

### 2. `config.yml`
The parameters. A declarative configuration file defining:
- LLM models to use (e.g. `gemini-2.5-flash`).
- Model parameters (`temperature`, `max_tokens`).
- System prompts or guidelines specific to this skill.
- Defaults and limits (e.g., maximum search results).

---

## Core MVP Skills

LifeOS implements six primary skills:

### 1. `save-insight`
- **Goal**: Convert raw web pages, YouTube videos, or text notes into clean, structured Markdown Insight Notes.
- **Implements**: Ingestion, formatting, summarization.
- **Output**: `data/knowledge/<domain>/insight--<slug>.md`

### 2. `attach-insight-to-expert`
- **Goal**: Create a source reference link from an Insight Note to an Expert profile.
- **Implements**: Reference file creation, updating original note metadata.
- **Output**: `data/experts/<expert_slug>/sources/<insight_note_filename>-ref.md`

### 3. `ask-expert`
- **Goal**: Ask a targeted question to a specific Expert, using only their associated Knowledge base as context.
- **Implements**: Full-Text Search (FTS) filtering, context window injection, LLM completion.
- **Output**: Streamlit chat response with structured citations.

### 4. `update-expert`
- **Goal**: Analyze source references to synthesize updates for an Expert's playbook or principles.
- **Implements**: LLM-driven synthesis of differences.
- **Output**: A pending update candidate in `outputs/expert-updates/` for human review.

### 5. `review-unattached-insights`
- **Goal**: Scan the library for Insight Notes not yet attached to any Expert, and suggest potential matches.
- **Implements**: Frontmatter scanning, category matching, LLM-based categorization suggestions.
- **Output**: Suggested attachments in the Streamlit Experts dashboard.

### 6. `generate-portfolio-case-study` (Roadmap)
- **Goal**: Compile real actions and decisions into markdown portfolio proofs.
- **Implements**: Action log analysis, structured formatting.
- **Output**: A showcase-ready case study showing how LifeOS resolved a real problem.

