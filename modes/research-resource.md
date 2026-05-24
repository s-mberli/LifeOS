# Mode: Research & Resource

## Purpose
Act as a universal ingestion and normalization mode. Process incoming raw information (AI, TCM, career, business, creator, or life resources) and integrate it correctly into the LifeOS knowledge base.

## Reads
- Incoming raw text or links
- `config/profile.yml` (to align with domains)
- Existing notes in the destination folder

## Outputs
- Markdown files using the `resource-note.md` template
- Summaries, extracted key points, and metadata tags

## Rules
1. Always format output using the `resource-note.md` template.
2. Recommend the correct domain storage path based on router classification:
   - AI resources → `data/knowledge/ai-resources/`
   - TCM / moxa / yoga / massage / sound healing → `data/business/flow-temple/` (or specific subfolder)
   - career resources → `data/career/`
   - creator resources → `data/knowledge/creator-profiles/`
   - life/personal resources → `data/private/`
3. Connect the resource to multiple relevant modes via metadata.
4. Suggest exactly ONE practical next step based on the resource.
