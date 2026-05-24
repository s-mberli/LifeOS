# LifeOS Data Directory

This directory holds all LifeOS runtime data. It is split into **public-safe** and **private** sections.

## ⚠️ Privacy Boundaries

| Folder | Status | Contains |
|--------|--------|----------|
| `data/knowledge/` | ⚠️ Review before committing | Processed resource notes (AI, TCM, etc.) |
| `data/business/` | ⚠️ Review before committing | Business strategy notes |
| `data/career/` | ⚠️ Review before committing | Career notes |
| `data/inbox/raw/` | 🔒 **IGNORED** by git | Unprocessed input files |
| `data/inbox/processed/raw/` | 🔒 **IGNORED** by git | Raw files after processing |
| `data/inbox/imports/` | 🔒 **IGNORED** by git | Imported chat logs |
| `data/inbox/voice/` | 🔒 **IGNORED** by git | Voice note files |
| `data/private/` | 🔒 **IGNORED** by git | All personal reflections, daily notes, emotions, family, body, finance |
| `**/raw/` | 🔒 **IGNORED** by git | All raw transcript folders |

## What is SAFE to commit in a public repo

- `data/README.md` — This file.
- Any curated, non-personal resource notes you have deliberately decided to share as examples.

## What you MUST NOT commit

- Anything in `data/private/` — these contain personal reflections, emotions, relationships, body notes, finance feelings, daily notes.
- Raw inbox files — `data/inbox/raw/`, `data/inbox/processed/raw/`.
- Raw transcript files — inside `**/raw/`.
- Personal notes about real people (family, relationships).

## How to Safely Publish LifeOS

1. Run `git status` and review **everything** before committing.
2. Use `git diff --staged` to inspect content.
3. If you want to include example notes, curate them deliberately and move them to a `data/examples/` folder.
4. Run `git check-ignore -v data/private/` to verify that private folders are properly excluded.
