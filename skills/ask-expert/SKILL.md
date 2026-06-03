# Skill: ask-expert

Consult a specific Expert Profile, scoped tightly to the local Insight Notes attached to that expert. Answers must be grounded in the sources and reflect the expert's playbook/principles.

---

## Purpose
Run scoped search retrieval and generation using specific expert contexts and source references.

## When to use
Use whenever the user wants to consult their local expert network on a specific query or task, limiting the context window to curated evidence.

## Technical Contract

### Inputs
- `expert_slug` (string, optional): The ID of the expert profile to consult.
- `query` (string, required): The user's query or problem statement.
- `search_scope` (string, optional): One of `Specific Expert`, `All Experts`, `General Library`. Default is `Specific Expert`.
- `limit` (int, optional): The maximum number of sources to inject (default 5).
- `include_playbook` (boolean, optional): Whether to inject profile/playbook documents (default true).

### Outputs
- **Response**: Synthesis string formatted in Markdown with source citations.
- **Audit Logs**: Retrieval logs in UI.

---

## Workflow Steps

1. **Context Resolution**:
   - If `search_scope` is `Specific Expert`:
     - Load `data/experts/expert--<expert_slug>/sources/*.-ref.md`.
     - Extract `source_path` properties to build an `allowed_paths` set.
   - If `search_scope` is `All Experts`:
     - Scan all expert folders to extract paths from all source reference files.
   - If `search_scope` is `General Library`:
     - Allow FTS search across all files with `type: insight_note` in the library.
2. **Retrieval**:
   - Run Full-Text Search (SQLite FTS5 query) using the filtered path list. Retrieve the top `$limit` matching Insight Notes.
3. **Context Construction**:
   - If `include_playbook` is enabled, append the selected Expert's `profile.md`, `playbook.md`, and `principles.md`.
   - Format context window:
     ```
     [Expert Profile & Playbook]
     [Grounding Evidence: Source notes contents]
     [User Query]
     ```
4. **Synthesis (LLM Request)**:
   - Call the LLM with the context, instructing it to answer using ONLY the grounding evidence, citing source file paths as links.
5. **Delivery**:
   - Render the response dynamically in the Streamlit chat UI.

---

## Rules
- Answers must be grounded in the sources; if the sources don't contain the answer, state that.
- Always include markdown citations pointing to original notes.
- Do not use profile/playbook content as grounding evidence unless explicitly enabled.

## Edge Cases
- **No sources attached to expert**: Explain that no sources exist, and offer fallback suggestions.
- **No FTS search results match**: Return a clear message explaining that the search index was queried but returned no matches, and suggest rebuilding index.

## Human Review Gates
- Direct trigger by the user in the Ask Expert chat UI. No files are modified.

## Related Existing Scripts/Functions
- `apps/streamlit-chat/app.py` -> `fts_search` and chat execution flow.
- `src/llm_client.py` -> LLM API calls.

## Test Ideas
- Query an expert with a question whose answer is present in a single attached source. Verify the answer is generated and includes the citation.
- Query an expert with a question whose answer is NOT present. Verify it politely declines to answer.
