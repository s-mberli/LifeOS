# Skill: attach-insight-to-expert

Create a lightweight reference linking an Insight Note to an Expert Profile and updating the note's status.

---

## Purpose
Attach an ingested Insight Note to a specific Expert's source list.

## When to use
Use whenever the user reviews unattached insights and decides to assign a note to an Expert, or when doing manual curation of an Expert's knowledge base.

## Technical Contract

### Inputs
- `insight_note_path` (string, required): The absolute or relative path to the Insight Note file.
- `expert_slug` (string, required): The slug of the target Expert (e.g. `expert--ai-systems-architect`).

### Outputs
- **Reference File**: Created at `data/experts/<expert_slug>/sources/<insight_note_filename>-ref.md`.
- **Note Update**: Modifies the original Insight Note frontmatter:
  - Updates `expert_status` to `attached`.
  - Appends `expert_slug` to `attached_experts` array.

---

## Workflow Steps

1. **Path Resolving**:
   - Verify that the target Insight Note exists and has `type: insight_note`.
   - Verify that the target Expert directory exists.
2. **Duplicate Prevention**:
   - Check if a `-ref.md` file for this note already exists in the expert's `sources/` subdirectory. If so, abort with "Already attached."
3. **Reference Creation**:
   - Write a lightweight Markdown reference file containing frontmatter metadata:
     - `type: expert_source_reference`
     - `expert_slug`
     - `source_path`
     - `source_title`
     - `source_url`
     - `attached_at`
   - The body of the reference note remains empty or contains minor notes, without copying the full transcript.
4. **Frontmatter Update**:
   - Read the original Insight Note.
   - Update `expert_status` to `attached`.
   - Add the expert's folder slug to `attached_experts`.
   - Save the updated original note.
5. **Search Index Rebuild**:
   - Rebuild SQLite FTS index to reflect the updated note metadata.

---

## Rules
- Never move or delete the original Insight Note.
- Do not copy the full transcript text into the reference file.
- Prevent duplicate attachments.

## Edge Cases
- **Expert slug directory doesn't exist**: Create the expert folders if necessary or throw an error.
- **Original note has corrupted frontmatter**: Parse and repair the frontmatter, or log a warning and fallback.

## Human Review Gates
- Direct trigger from the Streamlit UI button clicks by the user.

## Related Existing Scripts/Functions
- `src/ingest_resource.py` -> `assign_insight_to_expert`.
- `apps/streamlit-chat/app.py` -> Attach button handlers.

## Test Ideas
- Run the attachment function on a test note. Check that `sources/<note_name>-ref.md` is created and that the note's frontmatter lists the expert. Check that calling attach again yields a warning/message and doesn't recreate the file.
