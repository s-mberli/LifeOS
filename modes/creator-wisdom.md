# Mode: Creator Wisdom

## Purpose
Study successful creators deeply by accumulating evidence from many sources into one evolving creator profile.
Each creator gets a single canonical folder. Sources accumulate. Synthesis grows over time.

## Architecture: Many Sources → One Profile

```
data/knowledge/creator-profiles/
  creator--santiago-ferreiro/
    profile.md              ← master card (append-only, never blindly overwritten)
    sources/                ← one note per ingested source
      2024-05-22-tweet-thread.md
      2024-08-10-youtube-talk.md
    synthesis/              ← evolving summaries, updated as sources grow
      worldview.md
      playbook.md
      content-style.md
      business-model.md
      evidence-index.md     ← auto-updated by ingest_resource.py on every new source
```

## Folder Naming Convention
Creator names are slugified: `"Santiago Ferreiro"` → `creator--santiago-ferreiro`

## Reads
- `data/knowledge/creator-profiles/` (all creator folders, profile + synthesis)
- Individual source notes under `sources/`

## Outputs
- Source notes: `data/knowledge/creator-profiles/creator--{slug}/sources/{note}.md`
- Profile updates: `profile.md` (evidence appended, existing content preserved)
- Synthesis files: `worldview.md`, `playbook.md`, `content-style.md` (human-updated)
- Evidence log: `synthesis/evidence-index.md` (auto-updated)

## Rules
1. **Never create separate creator profiles per resource.** All sources for the same creator accumulate in one folder.
2. **Never overwrite profile.md sections blindly.** Always append new evidence blocks. Bump `source_count` in frontmatter.
3. **Scaffold synthesis/ on first source.** Create blank `worldview.md`, `playbook.md`, `content-style.md`, `business-model.md`, `evidence-index.md` if they do not exist.
4. **Auto-log to evidence-index.md** on every ingest. Manual synthesis updates happen after reflection.
5. Look beyond surface-level tips — extract the deeper worldview and repeated frameworks.
6. Always map the creator's advice to the user's domains (Flow Temple, AI Platform, Career).
7. Always suggest ONE practical way to apply their wisdom today.
8. When asked about a creator: read `profile.md` first, then synthesis files, then dive into `sources/` for evidence.

## Ingestion Workflow
1. Resource routed to `creator-wisdom` domain.
2. Creator name inferred (from YouTube channel, URL, content) or asked via CLI / Streamlit field.
3. Name slugified → `creator--slug`.
4. Source note saved to `sources/` subdirectory.
5. `profile.md` created (first source) or appended (subsequent sources).
6. `synthesis/evidence-index.md` updated automatically.
7. Synthesis files (`worldview.md`, `playbook.md`, etc.) scaffolded if missing — fill manually.

## Synthesis Workflow (Ask LifeOS)
When the user asks about a creator in Creator Wisdom mode:
1. Load `profile.md` for the creator → quick take and source count.
2. Load all `synthesis/*.md` files for the accumulated worldview and playbook.
3. If deep-dive needed: load relevant source notes from `sources/`.
4. Answer using the synthesis, not just one source.
5. End with: "What synthesis file should we update based on this?"
