# Skill: save-insight

Convert third-party materials (YouTube videos, articles, web pages) or personal text notes into structured, local Markdown **Insight Notes** with unified frontmatter.

---

## Purpose
Stateless ingestion and standardization of raw text or URLs into processed Insight Notes.

## When to use
Use whenever the user inputs a new YouTube link, article URL, or raw text chunk via the UI or capture scripts, and wants to process it into a structured Insight Note.

## Technical Contract

### Inputs
- `source_url` (string, optional): A valid YouTube or article web link.
- `raw_content` (string, optional): Direct text input if no URL is provided.
- `manual_tags` (list of strings, optional): User-provided tags.

### Outputs
- **Insight Note**: Created at `data/knowledge/insights/` or matching domain subfolders.
- **Raw Transcript / Source**: Saved to `data/private/transrc/` or raw subfolders.
- **Search Index Update**: Appends/rebuilds FTS5 search index database.

---

## Workflow Steps

1. **Extraction (Connector)**:
   - YouTube: Extract transcript text using the YouTube Transcript API.
   - Web Article: Clean HTML to extract main readable text.
   - Text Input: Use the provided raw content.
2. **Analysis (LLM Synthesis)**:
   - Feed raw text/transcript to LLM with the custom summary prompt.
   - Extract: Core Summary, Key Ideas, Why it matters, Suggested Experts, Tags, Source Reliability, and Next Action.
3. **Serialization**:
   - Write raw transcript/source text to the ignored raw transcripts folder.
   - Compile markdown file with YAML frontmatter containing metadata:
     - `title`, `source_url`, `type: insight_note`, `domain`, `tags`, `expert_status: unattached`, `suggested_experts`, `attached_experts: []`, `source_reliability`, `created_at`.
   - Write note file to knowledge directory.
4. **Trigger Database Update**:
   - Re-run search indexer (`build_fts_index.py`).

---

## Rules
- Never inline the raw transcript inside the main Insight Note.
- Set `type: insight_note` inside the frontmatter.
- Default `expert_status` to `unattached`.

## Edge Cases
- **No transcript found on YouTube**: Log error, save a clear failure/error note, and preserve raw URL/metadata without crashing.
- **Scraper blocked by Cloudflare**: Fall back to saving the raw URL and raw input as a placeholder note, notifying the user.

## Human Review Gates
- The user reviews the generated Insight Note under "Search Library" or "Review Unattached Insights" tabs. No expert files or cognitive profiles are modified automatically.

## Related Existing Scripts/Functions
- `src/ingest_resource.py` -> `process_one_file` and parser helpers.
- `src/llm_client.py` -> LLM API calls.
- `src/build_fts_index.py` -> FTS search index rebuilds.

## Test Ideas
- Run ingestion script with a known YouTube URL containing a valid transcript. Check that the generated note has `type: insight_note` and the transcript is in the raw subfolder.
- Try ingesting an invalid URL and check that it creates a stub file with an error log instead of crashing.
