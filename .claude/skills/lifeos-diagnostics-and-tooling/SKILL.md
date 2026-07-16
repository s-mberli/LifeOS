---
name: lifeos-diagnostics-and-tooling
description: How to MEASURE this system instead of eyeballing it. Ships five tested diagnostic scripts (DB health, dual-tree layout divergence, index coverage, retrieval smoke probe, env-var drift) with interpretation guides — all read-only in their default modes (search_probe's opt-in --hybrid flag is the one exception; it makes a paid API call through the repo's own connection path). Load this skill whenever you need numbers about system state — before/after any risky change, when search "seems" wrong, when checking pipeline or index health, when auditing configuration drift, or whenever a claim starts with "it looks like" or "it seems".
---

# Diagnostics and Tooling

Rule number one here: **capture a baseline number before a change, re-measure after, and diff.** Claims without numbers are not evidence (see `lifeos-validation-and-qa`).

All five tools live in this skill's `scripts/` directory and are run from the repo root:

```
.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/<name>.py
```

They are strictly read-only. They open the live database with `sqlite3` URI `file:indexes/lifeos.db?mode=ro&immutable=1` — the `immutable=1` is REQUIRED (this is a WAL-mode database; a plain `mode=ro` URI fails with "unable to open database file"). They deliberately never use `src.core.db.get_db_connection`, because that function runs `init_db` (writes) and will silently DELETE a database that fails its integrity check.

Caveat of `immutable=1`: SQLite assumes the file cannot change, so counts read mid-write (e.g. while the 09:00 TLDR ingest runs) can be momentarily stale. Re-run if the timing is suspicious.

## When NOT to use this skill

- You need to interpret an ERROR, not measure state → `lifeos-debugging-playbook`.
- You need the meaning/schema of the tables → `lifeos-architecture-contract`; retrieval math → `lifeos-rag-reference`.
- You want to fix the layout divergence these tools reveal → `lifeos-data-layout-unification-campaign`.

## 1. db_stats.py — database health

Real output (2026-07-08):

```
DB file size:            350.0 MB
search_index rows:       50,671
doc_chunks rows:         50,671
vec_docs rows:           50,671
automation_outbox:       803 total, 73 unprocessed, 0 actionable-unstamped
ai_code_provenance rows: 5
user_memory rows:        0
agent_repair_logs rows:  367
    persistently_failing  ValueError   240  <-- TEST POLLUTION
    ...
  test-pollution rows:   322 of 367
stray DBs:
    PRESENT: indexes/markusos.db (376 KB)
    PRESENT: src/indexes/lifeos.db (24 KB)
```

| Observation | Meaning | Action |
|---|---|---|
| The three chunk tables have EQUAL counts | invariant: 1 chunk row ↔ 1 FTS row ↔ 1 vector | if unequal → a partial index write happened; investigate before trusting search |
| counts grow day over day (50,134 on 07-07 → 50,671 on 07-08) | daily TLDR ingest is indexing | normal |
| counts suddenly tiny / DB size collapsed | `get_db_connection` deleted a "corrupt" DB and recreated empty (src/core/db.py:21-31) | restore from backup; see debugging playbook trap #4 |
| unprocessed outbox keeps climbing | triage isn't running (it runs inside the weekly pipeline) | check `lifeos-run-and-operate` schedules |
| agent_repair_logs grew after a test run | tests are writing to the live DB (known defect) | never use the full suite as a probe; fix tracked in the layout campaign Phase 4 |
| repair-log names 'persistently_failing', 'flaky_json_parser', 'flacky_json_parser' (typo variant is REAL data) | test fixtures, not production events | only `run_weekly_pipeline` rows (~4) are real |
| stray DBs present | legacy fossils, NOT the live DB | never debug against them; removal needs change control |

## 2. layout_audit.py — dual-tree divergence (filesystem only, no DB)

The primary instrument of `lifeos-data-layout-unification-campaign`. Real output (2026-07-08): knowledge 736 (data/) vs 739 (root), inbox 1108 vs 476, private 76 vs 65; 39 files only in data/knowledge, 42 only in root knowledge/, 677 only in data/inbox; plus a repo-wide `*sync-conflict*` scan (real conflict files exist under data/inbox/content_drafts/).

| Observation | Meaning | Action |
|---|---|---|
| both sides of a pair non-zero | the June-21 half-migration is still open | expected until the campaign completes |
| a pair reaches 0 on one side | that pair is unified | campaign Phase-3 gate satisfied for it |
| newest-mtime advances on BOTH sides | two producers still write to different trees | consult the campaign's path inventory |
| sync-conflict files found | Syncthing (VPS↔Mac) double-write | resolve manually before any migration |

## 3. index_coverage.py — disk vs search index

Real output (2026-07-08): distinct indexed paths 1501; data/knowledge 98.1%, data/private 100%, data/inbox 53.1%, data/experts 100%, outputs 100%; stale entries 0; **root knowledge/ 739 files, 739 NOT indexed** (the indexer at src/core/build_fts_index.py:13-21 only covers data/* + outputs).

| Observation | Meaning | Action |
|---|---|---|
| root knowledge/ unindexed count > 0 | search cannot see those notes at all | known gap; campaign fixes it; per-file `index_file()` is the cheap interim |
| data/inbox coverage ~53% | inbox holds many non-.md/raw files the indexer skips + files added after last index | acceptable; investigate only if it drops |
| stale entries > 0 | files deleted after indexing | harmless for search precision, rebuild eventually |
| coverage drops after your change | you broke indexing | diff against your Phase-0 baseline |

## 4. search_probe.py — retrieval smoke test

FTS-only by default (zero cost, zero writes). Prints bm25-ranked title/path/score for a fixed golden query list ('sqlite', 'agent', 'architecture', 'pipeline'). Real output shape (2026-07-08): each query returns 3 hits with bm25 around −3 to −10 (more negative = better match). `--hybrid` exists but makes a PAID OpenRouter embeddings call — use only with cost sign-off (owner rule: cost estimate before paid calls).

| Observation | Meaning | Action |
|---|---|---|
| a golden query returns 0 rows | index empty/stale or FTS syntax swallow | run db_stats + index_coverage; see debugging playbook #5 |
| results all from one directory | scoping or coverage skew | check index_coverage |
| bm25 magnitudes shift wildly after a change | ranking behavior changed | that's your before/after evidence — attach it to the PR |

Note: it prints titles and paths only, never note bodies (the vault contains personal content).

## 5. env_audit.py — configuration drift (reads key NAMES only, never values)

Real output (2026-07-08): 9 vars read in code but missing from .env.example (incl. WEBSITE_GITHUB_TOKEN/REPO, DEEPSEEK_*, INCLUDE_PROPOSALS, SKIP_AI_REVIEW, and DEBUG read by the Streamlit UI); 7 vars in .env.example never read by any code (GITHUB_TOKEN, HERMES_BIN, HERMES_SCRIPT, *_MAX_TOKENS, AZURE_EXISTING_AIPROJECT_ENDPOINT). The scan covers src/, scripts/, tests/, and apps/. Full catalog and statuses: `lifeos-config-and-flags`.

| Observation | Meaning | Action |
|---|---|---|
| "in CODE but NOT in .env.example" grows | someone added a var without updating the template | fix .env.example via change control |
| "in .env.example but NEVER read" | dead documentation misleading newcomers | candidates for removal (change control) |

## Non-scripted diagnostics

- **Logs map**: logs/tldr_ingest.log + tldr_launchd*.log (daily TLDR), logs/weekly_hermes.log + hermes_launchd*.log (weekly dispatch), logs/lenny_ingest.log + lenny_rss.log (VPS pipeline), logs/ingestion.log (core ingest). `tail -30 logs/<file>` and compare against the healthy signatures in `lifeos-run-and-operate`.
- **Scheduler check**: `launchctl list | grep lifeos` from a real user terminal (sandboxed shells may show nothing even when jobs are loaded — absence here is NOT proof of absence).
- **Git hygiene read**: `git status --porcelain | head -30`. As of 2026-07-08 the persistent set is: modified README/CHANGELOG/requirements/tracking; untracked `data/` and root `knowledge/news/*.md`. Untracked root-level note files are a privacy hazard (not gitignored) — see `lifeos-security-and-privacy`.
- **Tests are NOT a diagnostic probe**: the full suite takes ~5 min and WRITES to the live DB. Use single files (`.venv/bin/pytest tests/test_frontmatter.py -q`) per `lifeos-validation-and-qa`.

## Provenance and maintenance

- All expected numbers above were captured 2026-07-07/08 on the primary machine and drift daily — treat them as reference magnitudes, not constants; re-run the script to refresh.
- Scripts' read-only invariant: `grep -L "immutable=1" .claude/skills/lifeos-diagnostics-and-tooling/scripts/*.py` should list only the two filesystem-only scripts (layout_audit.py, env_audit.py).
- Indexer coverage list may change: `sed -n '13,21p' src/core/build_fts_index.py` — if DIRECTORIES_TO_INDEX changes, update index_coverage.py to match.
- Golden queries live at the top of search_probe.py; keep them stable so before/after comparisons stay meaningful.
