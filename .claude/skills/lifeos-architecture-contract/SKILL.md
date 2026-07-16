---
name: lifeos-architecture-contract
description: The load-bearing design decisions of this system and WHY they were made, the invariants every change must preserve, and the known weak points stated plainly with file:line evidence. Load this skill when DESIGNING or evaluating an approach — "why is it built this way", "would this violate an invariant", resolving contradictions between docs, or onboarding to the codebase. (For the process gates of executing a change — branch, review, approval — use lifeos-change-control instead.)
---

# Architecture Contract

## System map

```
INGESTION                      STORAGE                       CONSUMPTION
tldr.tech ──auto_tldr──┐
Lenny RSS (VPS+Syncthing)─┤    Markdown + YAML frontmatter   Streamlit chat UI
TicNote inbox drops ──────┼──► (knowledge/, data/knowledge,  (apps/streamlit-chat)
YouTube/web URLs (UI) ────┤     experts/, private/, ...)     MCP server (external
Firefox clipper ─►src/api ┘        │                          agents, read-only)
                                   ▼                              ▲
                        indexes/lifeos.db (SQLite)                │
                        FTS5 + doc_chunks + sqlite-vec ───hybrid──┘
                                   │                      search + RRF
                        automation_outbox ──triage──► weekly Hermes
                                              (keywords)   │
                                                           ▼
                                          dispatch → TinaCMS website repo
```

Module responsibilities (AGENTS.md §Architecture, verified): pure business logic in `src/core/` only; the Streamlit app is thin UI (`app.py` entry + `ui/{sidebar,chat,modals,helpers}.py`); `scripts/` holds pipeline orchestration; `src/api.py` is the clipper sidecar.

## When NOT to use this skill

- Retrieval internals/math → `lifeos-rag-reference` (this skill owns the contract; that one owns the theory).
- Process gates for changing things → `lifeos-change-control`. Current measured state → `lifeos-diagnostics-and-tooling`.
- The story of how a weak point came to be → `lifeos-failure-archaeology`.

## Load-bearing decisions (DECISION — WHY — IF VIOLATED)

1. **Markdown + YAML frontmatter is the source of truth** (docs/architecture-principles.md §1). Portability, longevity, human-readable, no DB lock-in. The SQLite DB is a rebuildable INDEX, not the record. If violated: knowledge becomes hostage to a binary file that (see weak point d) can be silently deleted.
2. **Local-first** (§2). Speed, privacy, full data control; cloud LLM APIs are the only external dependency. If violated: the privacy model and portfolio narrative both collapse.
3. **Public/private split** (§3, docs/private-public-split.md). The repo doubles as a public portfolio; personal data lives in gitignored trees. If violated: PII leak → history rewrite (already happened once; costliest incident on record — `lifeos-security-and-privacy`).
4. **Insight notes over raw sources** (§4). The system retrieves from dense synthesized notes; raw transcripts are archived under `**/raw/` (excluded from index and git). If violated: retrieval quality drowns in transcript noise and copyrighted text risks going public.
5. **Experts are syntheses, not mirrors of one source** (§5) — built by attaching many `-ref.md` source links under `experts/expert--<slug>/sources/`; retrieval for an expert is scoped to exactly those paths.
6. **Human approval before promotion / no autonomous self-modification** (§6-8, docs/future-self-improvement.md). The system proposes (proposal files, update candidates); a human applies. If violated: the "hallucination loop" the design exists to prevent.
7. **The outbox pattern for automation** (README "Why this design?"): every ingested note writes a row to `automation_outbox`; a keyword triage (no LLM, milliseconds — scripts/triage_outbox.py) filters; the expensive LLM work batches into ONE weekly Hermes run. WHY: cost. If violated: per-note LLM calls multiply spend by ~100×.
8. **No framework lock-in** (README): pure Python, no LangChain/LlamaIndex — every prompt and orchestration line is owned. Keep it that way; adding an orchestration framework is an architecture change requiring a proposal.
9. **Provider cascade** (src/core/llm_client.py `try_providers`): providers tried in `LLM_PROVIDER_ORDER` (openrouter/gemini/azure/deepseek), fall through on any failure, return None only if all fail. Callers MUST tolerate None.
10. **External agents get read-only, scoped access** via the MCP server ACL (src/core/mcp_server.py:107-121: data/-only, private blocked, .env/.git blocked, rate-limited, audited).

## Invariants (testable statements)

| # | Invariant | Status 2026-07-08 |
|---|---|---|
| 1 | System code never overwrites user-layer markdown without approval (privacy.yml; principle 6) | holds |
| 2 | Nothing under data/private (or root private/) is committed, sent to MCP clients, or quoted in public docs | holds in code; **git-side at risk**: root private/ is NOT gitignored — see `lifeos-security-and-privacy` |
| 3 | All YAML frontmatter goes through src/core/frontmatter.py (AGENTS.md rule 4) | holds |
| 4 | Paths via pathlib, relative to repo root (AGENTS.md rule 3) | holds |
| 5 | Business logic lives in src/core/, never in Streamlit files (AGENTS.md §1) | holds |
| 6 | Tests never write to the live indexes/lifeos.db | **VIOLATED**: tests/test_agent_harness.py logs to the live DB (322 of 367 agent_repair_logs rows are test fixtures); fix tracked in the layout campaign Phase 4 |
| 7 | .env and secrets never committed (pre-commit gate) | holds |
| 8 | DB schema creation is idempotent (`CREATE ... IF NOT EXISTS` in db.py init_db) | holds, with one sharp edge: init_db DROPS doc_chunks if expected columns are missing (db.py:58-64) — a "column upgrade" that discards all chunk rows; any schema change must account for it |
| 9 | search_index, doc_chunks, vec_docs row counts are equal | holds (50,671 each) |

## DB schema contract (src/core/db.py; counts 2026-07-08)

| Table | Purpose | Rows |
|---|---|---|
| search_index | FTS5(path, title, content, porter) — keyword search | 50,671 |
| doc_chunks | chunk text + path/title/chunk_index/wiki_links | 50,671 |
| vec_docs | vec0(chunk_id, float[768]) — semantic KNN | 50,671 |
| automation_outbox | ingested-note queue for the Hermes loop | 803 |
| user_memory | manually curated persistent memory (OWASP: no autonomous writes) | 0 |
| agent_repair_logs | self-repair harness events (src/core/agent_harness.py) | 367 (mostly test pollution) |
| ai_code_provenance | Five-Axis review ledger per file | 5 |

## Docs temporal layering (read this before "fixing" a doc)

Docs are era-documents. docs/mvp-scope.md says "no vector DBs" — yet ROADMAP Phase 4 shipped sqlite-vec. That is not a contradiction to repair; it's history. **Arbiters of what's current: ROADMAP.md checkboxes, CHANGELOG.md, and the code — in that order of intent vs fact.** README is the public face and must stay honest (`lifeos-portfolio-and-positioning`). Newcomer reading order: README → AGENTS.md → this skill → ROADMAP → CHANGELOG → docs/architecture-principles.md → the rest of docs/ as historical context. Never rewrite an era doc to match the present without change control; add a dated note instead (`lifeos-docs-and-writing`).

## Known weak points — stated plainly (WEAKNESS — RISK — STATUS)

a. **Dual data layout** (the big one): path constants split ~13 files old `data/*` vs ~14 files root layout (full inventory in `lifeos-data-layout-unification-campaign`). Risk: search misses root notes (739 unindexed files), UI and pipelines see different worlds, git can stage personal files. Status: OPEN; owner-confirmed hardest live problem.
b. **hybrid_search signature-overloading shim** (search_knowledge.py:117-128) accepts legacy argument orders by type-sniffing. Risk: silent mis-binding on new call sites. Status: accepted wart; don't extend the pattern.
c. **synthesize_briefing mutates os.environ to swap models** (search_knowledge.py:358-390). Risk: not thread-safe; concurrent calls can leak the cheap-model override. Status: accepted wart; candidate for a model-param refactor.
d. **get_db_connection silently DELETES a corrupted DB** (db.py:21-31: failed integrity check → unlink → fresh empty DB). Risk: unnoticed ~350 MB index loss + re-embed cost. Status: OPEN; mitigate with backups before risky ops.
e. **Tests write to the live DB** (invariant 6). Status: OPEN, fix specified in campaign Phase 4.
f. **Stray artifacts**: indexes/markusos.db (pre-rename fossil), src/indexes/lifeos.db, src/data/private. Risk: debugging against the wrong DB. Status: cleanup candidates (change control).
g. **llm_client.py duplicate imports/dotenv loads** (os/Path imported twice; .env loaded with override=True plus a VPS fallback path /root/.hermes/.env). Risk: confusing precedence. Status: cosmetic-plus; documented in `lifeos-config-and-flags`.
h. **Digest-first Hermes path is aspirational**: knowledge/news/digest/ and its producer weekly_tldr_process.py never existed in git; the fallback always runs. Risk: docs overstate reality. Status: OPEN (implement or remove — `lifeos-portfolio-and-positioning`).
i. **CI red + Python skew**: CI pins 3.11 and runs the full suite (currently 10 red); local venv is 3.14.6. Status: OPEN; green suite is the campaign exit gate.
j. **Zero-vector embedding fallbacks** at query time (search_knowledge.py:219-220) and index time (build_fts_index.py:206-209) silently degrade semantic ranking. Status: accepted trade-off; detection notes in `lifeos-rag-reference` §3.
k. **classify_input.py:7 resolves src/config/domains.yaml** (nonexistent) → silently loads `{}`. Status: OPEN bug, bundled into the campaign.
l. **build_fts_index.index_file references sqlite3.OperationalError without importing sqlite3** (:240) → latent NameError on a lock-retry. Status: OPEN bug, bundled into the campaign.

## Change compatibility rules

Before any change: (1) name which invariants it touches; (2) if it touches layout, config, schema, or publishing, it needs the corresponding sibling skill AND change control; (3) never add a second home for a fact another skill owns; (4) aspirational features stay labeled aspirational in every doc they appear in.

## Provenance and maintenance

- Invariant 9 / row counts: `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/db_stats.py`.
- Weak-point line numbers: `grep -n "def hybrid_search" src/core/search_knowledge.py`; `sed -n '21,31p;58,64p' src/core/db.py`; `grep -n "sqlite3.OperationalError" src/core/build_fts_index.py` vs `grep -n "^import sqlite3" src/core/build_fts_index.py`; `sed -n '5,9p' src/core/classify_input.py`.
- Doctrine sources: AGENTS.md, docs/architecture-principles.md, privacy.yml — re-read after any commit touching them.
- Table counts and weak-point statuses date-stamped 2026-07-08; statuses flip as the campaign executes — check `lifeos-failure-archaeology` for updates.
