# Evaluation & Quality Assurance

To ensure LifeOS remains reliable, accurate, and faithful to its local sources, we define a hybrid evaluation workflow combining schema validations and manual quality evaluation questions.

---

## The 8 Evaluation Questions (Fidelity & Alignment)

Use these questions as a checklist when testing the performance of the system in the Streamlit UI:

1. **Source Fidelity**: When you ask an expert a question, does the output contain clear Markdown citations linking directly to the local source notes (e.g. `[Hickey Simplicity](file:///...)`)?
2. **Context Anchoring**: If you ask an expert a question that has *no answer* in its attached sources, does it politely decline to answer, or does it hallucinate? (Correct behavior: It must state it doesn't have sources covering that topic).
3. **Playbook Style Alignment**: Does the expert's tone and formatting match the instructions defined in `profile.md` and `playbook.md`?
4. **Metadata Schema Integrity**: Does every newly created Insight Note contain all required frontmatter metadata fields (specifically: `type`, `domain`, `tags`, `expert_status`, `suggested_experts`, `attached_experts`, `source_reliability`)?
5. **Separation of Raw Data**: Is the raw transcript saved separately in the private raw folder? (The main Insight Note must NOT contain raw transcripts, only synthesized insights).
6. **Strict Retrieval Scope**: When you set the query search scope to "Specific Expert", are FTS search results strictly limited *only* to the files linked by `-ref.md` inside that expert's sources directory?
7. **Suggestive Categorization**: Does the "Scan unattached insights" workflow accurately suggest existing expert slugs based on the tags and domain of the note?
8. **Update Synthesis Accuracy**: Does the `update-expert` suggestion capture new frameworks from the attached sources without wiping or degrading the existing playbook guidelines?

---

## Running Manual Evaluation Loops

### Ingestion & Search Flow Test
1. **Trigger**: Paste a YouTube video URL (e.g. a technology talk or system design breakdown) into the **Save Insight** tab.
2. **Verify Ingestion**:
   - Check that the notes file is created in `data/knowledge/` with `type: insight_note`.
   - Check that the transcript is saved separately.
3. **Verify Indexing**:
   - Click "Rebuild Search Index".
   - Search for a specific keyword from the video in the **Search Library** tab and verify the note appears.

### Expert Association & QA Test
1. **Trigger**: In the **Experts** tab, scan for unattached insights. Find the new note and attach it to a relevant Expert (e.g., `ai-systems-architect`).
2. **Verify Link**: Check that a matching `-ref.md` file appears in `data/experts/expert--ai-systems-architect/sources/`.
3. **Verify Chat Scoping**:
   - Go to the **Ask Expert** tab, select the expert.
   - Run a query relevant to the new note. Check that it successfully returns the answer and cites the note.
   - Run a query *unrelated* to any attached sources. Check that the expert flags the missing context.
