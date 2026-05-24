# Skill: update-expert

Synthesize newly attached Insight Notes into recommendations for updating an Expert's profile, playbook, or principles.

---

## Purpose
Synthesize new insights attached to an Expert to evolve their cognitive frameworks without overwriting profiles autonomously.

## When to use
Use when multiple new source references have been attached to an Expert and the user wants to synthesize those lessons into updates for their playbook and principles.

## Technical Contract

### Inputs
- `expert_slug` (string, required): The ID of the expert profile to update.

### Outputs
- **Update Suggestion**: Saved as a markdown file at `outputs/expert-updates/expert-update--<expert_slug>--<timestamp>.md` with `status: pending_review`.

---

## Workflow Steps

1. **Information Ingestion**:
   - Read the Expert's current `playbook.md` and `principles.md`.
   - Read all attached source notes (`data/experts/expert--<expert_slug>/sources/*-ref.md`).
2. **Analysis & Synthesis (LLM)**:
   - Compare current playbooks/principles with new attached notes.
   - Detect new heuristics, workflows, and insights that should be added.
   - Draft proposed additions/refinements.
3. **Draft Serialization**:
   - Write the proposal file to `outputs/expert-updates/` with `status: pending_review` in frontmatter.
4. **Human Review Gate (Trigger)**:
   - Show the draft in the Streamlit UI, allowing the user to view, edit, and click "Apply" to commit the changes to the Expert's actual playbook/principles.

---

## Rules
- **NEVER** overwrite `profile.md`, `playbook.md`, `principles.md`, or `evidence.md` automatically.
- Only generate candidate updates in `outputs/expert-updates/` with `pending_review` status.

## Edge Cases
- **No new sources attached**: Alert the user and do not run synthesis.

## Human Review Gates
- Full human approval required before changes are written to the actual expert folder.

## Related Existing Scripts/Functions
- `scripts/ingest_resource.py` -> `generate_expert_update_suggestion`.

## Test Ideas
- Attach 2 new notes to an expert, run update-expert, check that an update candidate file is created under `outputs/expert-updates/` and the actual expert files are unchanged.
