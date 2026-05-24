# Skill: review-unattached-insights

Scan the library for unattached Insight Notes and suggest relevant Experts based on content categorization.

---

## Purpose
Help users triage incoming Insight Notes by surfacing unattached items and predicting target experts.

## When to use
Use when reviewing the library state, triaging newly processed resources, or doing routine database maintenance in the Experts dashboard.

## Technical Contract

### Inputs
- None (Global library scan).

### Outputs
- **List**: UI display of unattached notes.
- **Note Updates**: Suggestion list written to `suggested_experts` frontmatter.

---

## Workflow Steps

1. **Scan Library**:
   - Filter all notes under `data/knowledge/` with `type: insight_note` and `expert_status: unattached`.
2. **Match Experts**:
   - Compare tags and domain of each note with Expert profile metadata.
   - Run light LLM classification if no suggestions exist.
   - Save suggestions to note frontmatter: `suggested_experts`.
3. **User Triage UI**:
   - User reviews notes in UI and selects **Attach** (assigns to expert), **Ignore** (sets `expert_status: ignored`), or **Later** (leaves unattached).
4. **FTS Update**:
   - Re-run search index script.

---

## Rules
- Only scan files with `type: insight_note`. Exclude profiles, playbooks, and raw transcript files.
- Updating suggested experts must write directly to the note frontmatter.

## Edge Cases
- **No unattached notes found**: Display a friendly success message.

## Human Review Gates
- Full human control in the UI. No notes are attached to experts without explicit approval.

## Related Existing Scripts/Functions
- `scripts/ingest_resource.py` -> `scan_unattached_insights`.
- `apps/streamlit-chat/app.py` -> Triage buttons.

## Test Ideas
- Ingest a note (which defaults to unattached). Verify it shows up in "Scan for unattached insights". Ignore it, and verify it no longer shows up.
