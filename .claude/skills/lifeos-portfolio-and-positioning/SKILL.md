---
name: lifeos-portfolio-and-positioning
description: Governs the repo's public face — the positioning narrative, the audited truth-status of every README claim (verified-real vs partial vs aspirational), claims discipline and reproducibility standards, and the showcase roadmap. Load this skill when editing README or public docs, preparing releases or demos, making or checking any public claim, planning showcase work, reviewing the weekly dispatch, or deciding whether something may be published.
---

# Portfolio and Positioning

Owner's definition of "beyond state of the art" for this project (interview 2026-07-07): **portfolio/demonstration value — impeccable, honest, reproducible engineering.** Not novel research. Every public word is therefore an engineering artifact with a truth status.

## Positioning brief (from docs/research-verdict.md + docs/portfolio-positioning.md)

The framing is a **Personal Expert Network**, deliberately not a generic "LifeOS dashboard" (dilutes AI focus), not a chatbot wrapper (no grounding), not NotebookLM/Obsidian (closed ecosystem / no agentic loop). The narrative the repo must support, per docs/portfolio-positioning.md: (1) end-to-end AI systems architecture (Resource → Insight → Expert → Ask → Action); (2) human-in-the-loop governance — AI synthesizes, humans approve; (3) local-first knowledge engineering (SQLite FTS5 + Markdown, no cloud lock-in); (4) advanced RAG with strict source-grounding; (5) pragmatic MVP scoping. Everything published should reinforce one of those five, honestly.

## When NOT to use this skill

- Prose mechanics/templates → `lifeos-docs-and-writing`. What may NEVER be public (PII) → `lifeos-security-and-privacy`.
- Proving a claim before making it → `lifeos-research-and-proof-methodology`.

## The claims audit (README vs code, verified 2026-07-08)

| README claim | Status | Evidence |
|---|---|---|
| Expert synthesis (profile/playbook/principles) | REAL | src/core/experts.py; experts/ dirs |
| Multi-turn chat with citations | REAL | apps/streamlit-chat, src/core/chat_context.py |
| YouTube & web ingestion | REAL | src/core/youtube.py, web.py, ingest.py |
| Hybrid RAG: FTS5 + sqlite-vec + RRF at 10k+ scale | REAL | src/core/search_knowledge.py; 50,671 live chunks; tests/test_retrieval_scale.py |
| "Autonomous Self-Improvement ... opens GitHub PRs" | **PARTIAL** | zero PR-opening code exists in this repo (`grep -rn "create_pull\|PullRequest" src scripts` → empty). What's real: weekly dispatch generation + content push to the website repo (weekly_hermes_run.py push_to_github) + optional proposal files. PR-opening is delegated to an EXTERNAL Hermes agent binary (README install step 5) not present here |
| Five-Axis AI code review + provenance ledger | REAL but thin | scripts/ai_code_reviewer.py + ai_code_provenance table (5 rows — barely exercised) |
| "Adaptive Review Gates — higher AI ratio → more rigorous threshold" | **ASPIRATIONAL** | no ratio/adaptive logic anywhere in ai_code_reviewer.py — the reviewer is uniform |
| Digest-first weekly pipeline (docstrings/design) | **ASPIRATIONAL** | knowledge/news/digest/ and producer weekly_tldr_process.py never existed in git; fallback always runs |
| MCP server (search_vault, read_vault_file) + OWASP mitigations | REAL (minor overstatement risk) | src/core/mcp_server.py; mapping in `lifeos-security-and-privacy` |
| Manual Personal Memory | REAL, unused | user_memory table exists; 0 rows |
| Browser clipper | REAL | apps/firefox-clipper + src/api.py /ingest |
| Multi-provider LLM cascade | REAL | llm_client.try_providers (openrouter/gemini/azure/deepseek) |
| ElevenLabs TTS voice personas | REAL | src/core/tts.py |
| Providers "never store or train on" your data | **UNVERIFIABLE marketing** | soften to "per provider policies" |
| ROADMAP checkboxes | ACCURATE | Phase 4 hybrid [x] true; local LLM [ ] true |

Score: 10 real, 1 partial, 2 aspirational, 1 unverifiable. The partial/aspirational rows are the README-fix worklist (through change control). All 6 images referenced by README exist in docs/assets/ + docs/banner.png (verified).

## Claims discipline rules

1. A public claim must be **reproducible by a stranger from a fresh clone**, or be explicitly labeled planned/roadmap. Known fresh-clone gaps that currently break this standard (be honest anywhere it matters): red test suite (10 failures), no pre-commit hook on clones, .env.example drift — details in `lifeos-build-and-env`.
2. Numbers in public text come from `lifeos-diagnostics-and-tooling` scripts at writing time, never from memory, and get a date.
3. Demos must be re-runnable; screenshots must match current UI.
4. Nothing personal ever appears (see the boundary map + the `git add -A` hazard in `lifeos-security-and-privacy`).
5. Every claims-audit fix is a normal change: branch, review, approval.

## A real doctrine conflict — surfaced for owner decision

privacy.yml's verbatim rule is "Always ask for human approval before publishing anything **to social media or sending emails**." The weekly launchd run of weekly_hermes_run.py **pushes the dispatch to the public website repo automatically** — no approval gate exists in the script (verified; push_to_github runs unconditionally when env is configured). A website-repo push is arguably neither social media nor email, so this is an interpretive tension rather than a verbatim violation — but the spirit of the rule (nothing goes public without a human) is plainly in question. Options: (a) accept and amend privacy.yml with an explicit carve-out for the dispatch, or (b) add a review gate (e.g. push only with a `--publish` flag; cron writes draft only). Until decided, treat MANUAL runs as publishing events requiring approval. Status: OPEN as of 2026-07-08.

## Weekly dispatch quality rules (it is public-facing)

From the prompts in weekly_hermes_run.py (verified): only two agents may be named — "Hermes" (analyst) and "Prototyper" (coder); never invent others. No meta-commentary ("Sample dispatch...", generation notes) — strip_artifacts() exists because exactly that leaked into published posts (commits 2b7b529 → 86ef0ec); if new artifacts appear, extend it. Diversity rule: ≥4 topic areas, AI/Tech must not dominate. Mermaid labels: no unquoted parentheses.

## Showcase roadmap (candidates — labeled, not commitments)

1. **Green suite + CI badge.** Exit of `lifeos-data-layout-unification-campaign`. Result when: CI passes on main and the README badge is real.
2. **Reproducible retrieval eval.** Golden queries + docs/evals.md questions turned into a scripted eval with published numbers. Result when: a stranger runs one command and gets the same table.
3. **Honest-README pass.** Apply the claims audit. Result when: every table row above reads REAL or is labeled planned.
4. **End-to-end demo recording.** Clip a URL → ingest → ask-expert with citations, on a clean profile. Result when: the recording reproduces on a fresh clone.
5. **Digest-first pipeline: implement or delete.** Result when: either knowledge/news/digest/ has a real producer and the path executes, or all references to it are gone.
6. **Provenance ledger in anger.** Route real work through GIT_AUTHOR tagging until ai_code_provenance tells a story (>5 rows). Result when: a README section can show the ledger truthfully.

## Provenance and maintenance

- Re-run the claims audit after any feature merge: `grep -rn "create_pull\|PullRequest" src scripts` (PR claim); `grep -n "adaptive\|ratio" scripts/ai_code_reviewer.py` (gates claim); `ls knowledge/news/digest 2>/dev/null` (digest claim); `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT COUNT(*) FROM ai_code_provenance;"`.
- Image refs vs files: `grep -o 'docs/[a-z/-]*\.png' README.md | sort -u` vs `ls docs/assets docs/banner.png`.
- The doctrine conflict: `grep -n "approval" privacy.yml` vs `grep -n "push_to_github(dispatch" scripts/weekly_hermes_run.py` — update this section when the owner decides.
- Audit dated 2026-07-08; re-verify rows before quoting them publicly.
