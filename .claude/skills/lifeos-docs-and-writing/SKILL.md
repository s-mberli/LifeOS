---
name: lifeos-docs-and-writing
description: How the docs of record are maintained — which document is authoritative for what (temporal layering doctrine), CHANGELOG/README house style with copy-paste templates, the update_docs.py automation, the templates/ inventory, and note-frontmatter schema. Load this skill when updating README/CHANGELOG/docs, documenting a feature, resolving a contradiction between docs, creating notes or templates, or checking which document wins.
---

# Docs and Writing

The owner's definition of excellence for this project is portfolio-grade, honest documentation — docs quality is a first-class engineering goal here, not an afterthought (`lifeos-portfolio-and-positioning` owns truth-of-claims; this skill owns mechanics and style).

## When NOT to use this skill

- Deciding whether a public claim is TRUE → `lifeos-portfolio-and-positioning`.
- What may never appear in public docs (PII rules) → `lifeos-security-and-privacy`.
- Whether the change itself is allowed → `lifeos-change-control`.

## Docs-of-record inventory and authority

| File | Role | Authority | Updated when |
|---|---|---|---|
| AGENTS.md | agent/developer rulebook | **highest for behavior** | rules change (change control) |
| ROADMAP.md | phase checkboxes | arbiter of what's current/planned | feature ships or plan changes |
| CHANGELOG.md | what shipped when | arbiter of what happened | every merged feature (AGENTS.md step 5) |
| README.md | public face | must match code reality | architecture-visible changes only |
| docs/architecture-principles.md | design doctrine | high (with the contract skill) | rarely; via proposal |
| docs/{mvp-scope, threat-model, research-verdict, portfolio-positioning, evals, private-public-split, future-self-improvement, vps_deployment_guide}.md | **era documents** | historical context | see layering rule below |
| docs/skills.md + root skills/ | the LifeOS **user-workflow** skill system (save-insight, ask-expert, ...) — a DIFFERENT system from this .claude/skills/ library; don't confuse them | — | when those workflows change |
| apps/streamlit-chat/spec.md, docs/specs/ | feature specs | per-feature | with the feature |

**Temporal layering doctrine:** docs are era-stamped snapshots. docs/mvp-scope.md says "no vector DBs"; Phase 4 shipped sqlite-vec anyway — that's history, not an error. When docs conflict: ROADMAP checkboxes + CHANGELOG + the code win. Never rewrite an era doc to match the present; if it actively misleads, add a dated note ("*Update 2026-07-08: superseded by ...*") through change control. Cautionary tale: the June-21 restructure overwrote README wholesale; it had to be restored from git history (commits 9f4759a → 46727db).

## CHANGELOG house style (derived from the file)

```markdown
## [YYYY-MM-DD]
### Added   (or Changed / Security / Fixed)
- **Feature Name:** One-to-three sentences, concrete, past tense. What and why.
  - **Source:** [Article title](https://original-url?utm_source=...)   <- only for insight-driven features
```

Rules: newest section at the top (note: the current file has one out-of-order block — 2026-06-25 sits below 2026-06-21; keep new entries strictly newest-first and fix ordering opportunistically); bold feature names; a `**Source:**` line whenever the feature traces to an ingested article (this is the project's idea-provenance chain — see `lifeos-research-and-proof-methodology` §4).

## README conventions

Badges + hero images at top (assets in docs/assets/ — verify a referenced image exists before referencing it); mermaid diagrams use the project's dark init-theme block (copy an existing one); emoji section headers are house style in README and AGENTS.md; footer attribution stays. Hard rules: no personal name (the pre-commit hook rejects it — write "the user"/"the operator"; the brand "MarkusOS" is allowed), no absolute local paths, and **no aspirational feature described as shipped** — as of 2026-07-08 the known truth gaps are the digest-first pipeline and the "Adaptive Review Gates" claim; the full audit lives in `lifeos-portfolio-and-positioning`.

## update_docs.py (the docs automation — state-writing, don't run casually)

`.venv/bin/python scripts/update_docs.py <proposal_file> [--no-readme]` — invoked at AGENTS.md workflow step 5 after implementing a proposal. Verified behavior (scripts/update_docs.py): reads the proposal + the last commit's diff (8000-char cap), LLM-drafts a CHANGELOG entry (extracting the real Source URL programmatically — commits a6dbec3/d3c91a4 fixed "N/A" sources), optionally LLM-updates README when the feature is architecture-visible, and generates a mermaid diagram. It validates the proposal path against data/inbox/proposals/ (:180). Failure modes: LLM cascade returns None → no entry written (write it by hand from the template above); README edits are LLM-authored → always diff-review before committing. `update_docs.py.bak` alongside it is a fossil — ignore.

## templates/ inventory

Twenty scaffolds under templates/, **no programmatic consumers** (verified: `grep -rn "templates/" src scripts apps --include='*.py'` → empty) — they are human/agent-facing authoring guides: insight-note, thought-note, voice-note, imported-chat-note (note capture); creator-profile + creator-source-note + creator-synthesis-{playbook, worldview, business-model, content-style, evidence-index} (expert building); content-brief, project-brief, decision-log, experiment-log, focus-log, daily-focus, weekly-review, skill-progression, training-log (workflows). Use them as the starting shape when creating the corresponding artifact.

**Frontmatter schema drift (honest note):** docs/evals.md Q4 requires insight notes to carry YAML frontmatter fields `type, domain, tags, expert_status, suggested_experts, attached_experts, source_reliability` — and src/core/ingest.py writes YAML frontmatter accordingly — but templates/insight-note.md uses inline bold fields (`**Tags**:`) with no YAML block. The pipeline's output, not the template, matches the eval schema. If you touch either, reconcile them via change control rather than silently picking one.

## How to document a change (checklist)

1. CHANGELOG entry (template above) — always.
2. README — only if the feature is visible in the architecture/capability tables; keep claims verifiable.
3. ROADMAP checkbox if a phase item shipped.
4. Era docs — dated note only, never rewrites.
5. Screenshots → docs/assets/, referenced with relative paths.
6. If it came from a proposal: flip the proposal's `## Status` (✅ Implemented / ❌ Rejected + reason).
7. Everything through the change-control gates; the pre-commit hook will scan your prose too.

## Obsidian note

The repo root is an Obsidian vault (.obsidian/ present). Wiki-links (`[[...]]`) in notes are extracted at index time into doc_chunks.wiki_links (build_fts_index.py extract_wikilinks) but nothing consumes them yet — a labeled-open capability, not a feature to document as real.

## Provenance and maintenance

- Authority table: re-skim AGENTS.md/ROADMAP.md headers after any commit touching them.
- update_docs behavior: `sed -n '1,30p' scripts/update_docs.py`.
- Template consumers (should stay empty): `grep -rn "templates/" src scripts apps --include='*.py'`.
- Frontmatter drift: compare `head -20 templates/insight-note.md` with the fields written in src/core/ingest.py (`grep -n "expert_status\|source_reliability" src/core/ingest.py`).
- README truth gaps: see the claims audit in `lifeos-portfolio-and-positioning` (dated 2026-07-08).
