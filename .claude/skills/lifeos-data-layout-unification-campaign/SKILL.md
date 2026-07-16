---
name: lifeos-data-layout-unification-campaign
description: The executable, decision-gated campaign for this project's hardest live problem — the half-finished June-2026 migration that left TWO diverged data trees (old `data/*` vs new root-level `knowledge/`, `experts/`, `inbox/`, `private/`, ...). Load this skill when: fixing the failing test suite (10 red tests), unifying or deciding the canonical data layout, touching any path constant, resolving dual-tree divergence, investigating why search misses recent notes, or when any work is blocked by layout inconsistency. Do NOT improvise layout fixes without this skill.
---

# Data Layout Unification Campaign

**Status: OPEN as of 2026-07-08. Nothing below has been executed. Gate 1 requires owner sign-off.**

## The problem in one paragraph

Commit `9f4759a` (2026-06-21, 1192 files, "restructure: flatten data/ → root level") moved the tracked data tree to root-level directories, but the migration never finished. Both trees now exist and actively diverge (both received new files this month). Code path-constants are split roughly half-and-half between layouts. Consequences, all verified: 8+ of the 10 failing tests; the FTS index covers ZERO root-level notes (739 unindexed files in root `knowledge/`); the Streamlit UI reads `data/*` while newer pipelines write root dirs; proposals dirs diverged (39 vs 21 files); and — worst — root-level `private/`, `knowledge/`, `experts/`, `tracking/` are **not covered by .gitignore**, so one careless `git add -A` stages personal journals into a public portfolio repo. This split already caused one production bug (commit `86ef0ec`: Hermes "was finding 0 articles" because it read `data/knowledge/news` while TLDR wrote `knowledge/news`).

Jargon: "old layout" = paths under `data/` (e.g. `data/knowledge/...`). "New layout" = the same dirs at repo root (e.g. `knowledge/...`). "Live DB" = `indexes/lifeos.db` (~350 MB, ~50k embedded chunks; embeddings cost real API money — see cost fence).

## When NOT to use this skill

- Diagnosing an unrelated error → `lifeos-debugging-playbook`.
- Understanding why the layout matters architecturally → `lifeos-architecture-contract`.
- You just need to know which tree a component uses today → `lifeos-run-and-operate` artifact map.
- History of how this happened → `lifeos-failure-archaeology`.

## The path-constant inventory (the campaign's core asset)

Verified 2026-07-08 by `grep -rn '"data"\|"knowledge"\|"experts"\|"inbox"\|"private"\|"business"\|"career"\|"tracking"\|"tts_cache"' src/core scripts src/api.py apps/streamlit-chat --include='*.py'`. Re-run that grep at execution time; the table is the checklist for Phase 2.

### OLD layout (`data/*`) — 13 files

| File:line | Constant |
|---|---|
| src/core/build_fts_index.py:14-19 | indexes data/knowledge, data/private, data/inbox, data/experts, data/business, data/career (+ outputs) |
| src/core/experts.py:333-335 | scans data/knowledge, data/private, data/inbox |
| src/core/ingest.py:285,298 | storage_location strings "data/inbox/processed/needs-review/", "data/knowledge/ai-resources/" |
| src/core/create_daily_note.py:7 | data/private/daily |
| src/core/mcp_server.py:17 | audit log data/private/mcp_audit.log; `read_vault_file` ACL is rooted at "data" (line ~107) |
| scripts/weekly_hermes_run.py:698,706 | writes data/inbox/content_drafts, data/inbox/proposals |
| scripts/update_docs.py:180 | expects proposals in data/inbox/proposals |
| scripts/process_ticnote_inbox.py:295-296 | data/inbox/ticnote, data/knowledge/ticnote |
| scripts/backfill_metadata.py:10, scripts/cleanup_duplicates.py:8, scripts/correct_metadata.py:12 | DATA_DIR = data/ |
| apps/streamlit-chat/ui/helpers.py:111,139-141,262,336,428 | UI reads data/experts, data/knowledge, data/private, data/inbox |
| apps/streamlit-chat/ui/modals.py:127-129,328,443,645 | UI writes/reads data/knowledge, data/private, data/inbox, data/experts |
| tests/conftest.py (tmp_project fixture) | builds data/* tmp trees |
| .gitignore | nearly all data-protection patterns target `data/...` |

### NEW layout (root) — 14 files

| File:line | Constant |
|---|---|
| src/core/experts.py:91,148,407,563,668 | root experts/ |
| src/core/chat_persistence.py:40,110 | root private/chat-logs, root knowledge/chat-insights |
| src/core/ingest.py:637,705 | root knowledge/ai-resources/raw, root inbox/processed/raw |
| src/core/auto_capture.py:89 | root private/raw-capture |
| src/core/cleanup_data.py:9 | root knowledge/ |
| src/core/tts.py:32 | root tts_cache/ |
| scripts/auto_tldr.py:65-66 | root tracking/tldr_ingest.json, root knowledge/news |
| scripts/weekly_hermes_run.py:60 | reads root knowledge/news (NOTE: this file straddles BOTH layouts) |
| scripts/ingest_lenny.py:36-38, scripts/monitor_lenny_rss.py:29 | root tracking/, root knowledge/lenny-* |
| scripts/sync_outbox.py:40 | root knowledge/lenny-podcast |
| scripts/backfill_expert_attachments.py:156 | root knowledge/ |
| scripts/cleanup_notes.py:28-30 | root inbox/, knowledge/, private/ |
| scripts/expert_chat.py:16 | root experts/ |
| scripts/event_tracker.py:40 | root tracking/events_seen.json |

Related latent defects to fix in the same campaign (verified):
- `src/core/classify_input.py:7` resolves to `src/config/domains.yaml`, which doesn't exist → silently loads `{}` (should be `config/domains.yaml` from repo root).
- `src/core/build_fts_index.py` `index_file()` references `sqlite3.OperationalError` (line ~240) but the module never imports `sqlite3` → a lock-retry would crash with NameError.
- Root-level committed-but-unread config twins (`domains.yaml`, `domain_map.yaml`, `privacy.yml`, `profile.yml`, `models.yml` at repo root); code reads only `config/` copies — see `lifeos-config-and-flags`.

## Measured divergence baseline (2026-07-08, via layout_audit.py)

| pair | data/* files | root files | newest data/* | newest root |
|---|---|---|---|---|
| knowledge | 736 | 739 | 2026-07-01 | 2026-07-07 |
| experts | 13 | 13 | 2026-06-21 | 2026-07-02 |
| inbox | 1108 | 476 | 2026-07-07 | 2026-07-07 |
| private | 76 | 65 | 2026-06-26 | 2026-07-07 |
| business | 0 | 1 | — | 2026-07-02 |
| tracking | 1 | 3 | 2026-06-20 | 2026-07-07 |

Both trees are LIVE: data/inbox received files on 2026-07-07 (Syncthing/VPS side) and root knowledge/ receives daily TLDR files. 39 files exist only in data/knowledge; 42 only in root knowledge/; 677 only in data/inbox. Sync-conflict artifacts exist under data/inbox/content_drafts/ (`*.sync-conflict-*`).

Test baseline (2026-07-07): 10 failed / 188 passed / ~315 s. Failing node ids:
- tests/test_chat_persistence.py::test_append_to_daily_chat_log, ::test_save_message_as_insight (layout: test builds tmp data/private, code writes root private/)
- tests/test_experts.py::TestGetExistingExperts::test_finds_expert_directories, ::test_result_dicts_have_expected_keys; TestCreateEmptyExpert::test_creates_empty_expert_scaffold, ::test_fails_if_expert_already_exists (layout: tmp data/experts vs root experts/)
- tests/test_experts_tts.py::test_core_get_existing_experts_with_voice_id (same)
- tests/test_debug.py::test_debug_imports (NOT layout — leftover scaffold ending `assert False`; delete via change control)
- tests/test_ui.py::test_ui_chat_input_flow, ::test_ui_chat_save_insight_flow (AppTest RuntimeError — root cause UNDIAGNOSED; the tests patch paths correctly; verify during campaign, do not assume layout)

DB baseline drifts daily (2026-07-08: 50,671 chunks; outbox 803/73/0) — re-capture at execution time with db_stats.py.

---

## Phase 0 — Preflight (no changes to anything)

1. Back up the live DB: `cp indexes/lifeos.db indexes/lifeos.db.bak-$(date +%Y%m%d)` (~350 MB; confirm disk space first with `df -h .`).
2. Snapshot state into a scratch note (not committed):
   - `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/db_stats.py`
   - `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/layout_audit.py`
   - `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/index_coverage.py`
   - `git status --porcelain | head -50`
   - Fallback if scripts are missing: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT COUNT(*) FROM doc_chunks"` and `find data/knowledge knowledge -name '*.md' | wc -l` per pair.
3. Record the failing-test baseline WITHOUT a full suite run: run each known-red file individually (`.venv/bin/pytest tests/test_experts.py tests/test_chat_persistence.py tests/test_experts_tts.py tests/test_debug.py -q`). Expected: 8 failed there (+2 in test_ui.py if you run it). If MORE fail → stop; the world changed; re-derive the baseline before proceeding.
4. **GATE: Pause Syncthing** on the shared `data/` folder (operator action in the Syncthing UI, both Mac and VPS sides). Do not proceed to Phase 3 while sync is active. Evidence this matters: existing `*.sync-conflict-*` files.

## Gate 1 — THE DECISION (requires owner sign-off, per lifeos-change-control)

Choose the canonical layout. Both options are viable; the cost is symmetrical in code but asymmetric in operations:

| Criterion | Option A: root-canonical | Option B: data/-canonical |
|---|---|---|
| Matches commit 9f4759a intent | yes | no (reverts it) |
| Code files to edit | ~13 (the old-layout table) | ~14 (the new-layout table) |
| Tests | conftest + failing tests updated to root | most tests already match; new-layout code re-pointed |
| .gitignore | full rewrite (all patterns re-rooted) + verify | already correct |
| Syncthing share | must re-point share root (VPS + Mac) | unchanged |
| MCP `read_vault_file` ACL | must re-root from "data" | unchanged |
| Index paths (50k rows say `data/...`) | must migrate paths (see Phase 5) | unchanged |
| File moves | data/* merged INTO root dirs | root dirs merged INTO data/* |

**Recommendation: Option B (data/-canonical).** Rationale: (1) the privacy blast-radius of Option A is larger — .gitignore, MCP ACL, and the index all assume `data/`, and getting any of them wrong leaks personal content or breaks retrieval; (2) Syncthing topology stays untouched; (3) the 50k-row index needs no path migration. Option A's only real advantage is honoring the June-21 intent, and that intent was never justified in writing anywhere. Present both options to the owner; do not proceed without an explicit decision recorded in a proposal file.

## Phase 2 — Code unification (on branch `feat/data-layout-unification`)

1. Follow the AGENTS.md 7-step workflow: branch, then write a spec proposing a single paths module (candidate design: `src/core/paths.py` exporting named constants like `KNOWLEDGE_DIR`, `PRIVATE_DIR`, `EXPERTS_DIR`, `INBOX_DIR`, `TRACKING_DIR`, `TTS_CACHE_DIR`, all derived from one `DATA_ROOT`). Get plan approval before editing.
2. Edit every file in the LOSING layout's table above to import from the paths module. Manual or IDE-assisted edits only.
3. Fix the two latent defects while there: classify_input.py config path; build_fts_index.py missing `import sqlite3`.
4. **Fenced off:** writing a script that regex-rewrites `.py` files (AGENTS.md Safety Rule 1 — programmatic patching is banned here, with history behind it); editing while Syncthing is unpaused.
5. Gate check after each module: run just that module's tests. Expected: `.venv/bin/pytest tests/test_experts.py -q` → 0 failed (was 4). If a test still fails → the inventory missed a constant; re-grep that file, don't patch the test to match broken code.

## Phase 3 — Data migration (Syncthing still paused)

1. Resolve every `*.sync-conflict-*` file first (diff against its sibling, keep the right one, delete the conflict copy): `find data -name "*sync-conflict*"`.
2. Merge the losing tree into the canonical tree, pair by pair. Rules: filename collision + identical content → drop duplicate; collision + different content → newer mtime wins, loser goes to a quarantine dir (do NOT delete); no collision → move. For proposals dirs specifically: union by filename (data/inbox/proposals has 39, inbox/proposals has 21; overlap is large).
   Dry-run first: `rsync -avn --ignore-existing <losing>/ <canonical>/` and review before removing `-n`.
3. **Only for Option A:** rewrite .gitignore patterns from `data/...` to root equivalents FIRST, then verify EVERY private dir: `git check-ignore private/ knowledge/ experts/ inbox/ business/ tracking/` must report ignored (as of 2026-07-08 none of these are ignored — that is the leak risk). **Only for Option B:** move root files into data/, then delete the empty root twins; verify `git status --porcelain` no longer shows untracked root md files.
4. Re-point Syncthing (Option A only) and unpause — LAST step of this phase.
5. Gate check: `layout_audit.py` → every pair shows one side at 0 files (or the dir gone). If both sides still populated → a producer is still writing to the losing tree; check the inventory for a missed writer (likely a launchd job that ran mid-migration — re-check schedules in `lifeos-run-and-operate`).

## Phase 4 — Test alignment

1. Update tests/conftest.py `tmp_project` to build the canonical layout.
2. Fix each failing test per its cause (listed in the baseline). For test_ui.py's two AppTest failures: diagnose first (they may be unrelated to layout — run them alone with `--tb=long`).
3. Delete tests/test_debug.py (change-control approval; it is a scaffold ending in `assert False`).
4. Fix the DB-pollution defect: `src/core/agent_harness.py` logs repair attempts without a db_path, defaulting to the live DB; tests/test_agent_harness.py therefore writes to `indexes/lifeos.db`. Candidate fix: make the decorator accept/propagate a db_path and have the test patch it to tmp (see the good pattern in tests/test_outbox.py). Evidence of the defect: 322 of 367 agent_repair_logs rows are test fixtures ('persistently_failing' 240, 'flaky_json_parser' 64, 'flacky_json_parser' 18 — note the typo variant is real data).
5. Gate check: repair-log count unchanged across a test run: capture `SELECT COUNT(*) FROM agent_repair_logs` before/after running tests/test_agent_harness.py. Expected delta: 0.

## Phase 5 — Index reconciliation

- **Option B (recommended):** index paths already say `data/...` — nothing to migrate. Just index the merged-in files: the cheapest correct move is per-file `index_file()` calls for the ~42 files that lived only in root knowledge/ (each file's chunks get embedded — small, bounded cost), NOT a full rebuild.
- **Option A:** the 50k rows in search_index/doc_chunks say `data/...`. A full rebuild (`build_index()`) **drops all three tables and re-embeds every chunk** (verified: src/core/build_fts_index.py:48-50 and per-chunk `get_embeddings` at :207) — that is the expensive path. Cost formula before choosing it: cost ≈ 50,671 chunks × (~1000 chars/4 =) ~250 tokens × current OpenRouter embedding rate. Cheaper alternative to evaluate at execution time: `UPDATE doc_chunks SET path = replace(path,'data/','')` + delete/reinsert of search_index rows (FTS5 rows can't be UPDATEd in place) reusing existing content, leaving vec_docs untouched (chunk_ids stable). Prototype on a COPY of the DB, never the live file.
- Gate check: `index_coverage.py` → coverage ≥ baseline (data/knowledge 98.1%, data/private 100%, data/experts 100% as of 2026-07-08) and root-knowledge-unindexed = 0 (or n/a).

## Phase 6 — Full verification

1. Full suite ONCE, on the branch, AFTER the Phase-4 pollution fix: `.venv/bin/pytest`. Expected: **0 failed, 197 passed** (198 baseline − deleted test_debug). If test_ui.py still fails → its cause was never layout; file it as its own investigation (archaeology entry), don't block the campaign on it — but then expected becomes 2 failed with a documented reason.
2. `layout_audit.py` → single tree. `db_stats.py` → repair-log count unchanged. `git status` → clean or intentionally staged.
3. Grep gate: the inventory grep returns zero references to the losing layout.

## Phase 7 — Promotion (through lifeos-change-control)

Five-Axis review on all modified .py; CHANGELOG + README updates per `lifeos-docs-and-writing` (README's Project Structure section currently shows the data/ layout — align it with the decision); proposal file status updated; **explicit owner approval before merge and before any push**. Success is measurable, never judged by eye: green suite, single tree on disk, index coverage ≥ baseline, zero test writes to the live DB, `git check-ignore` proof for every private dir.

## Known wrong paths — fenced off

| Wrong path | Why it's wrong |
|---|---|
| Delete either tree wholesale | Syncthing resurrects it or conflicts; 39/42/677 unique files would be lost |
| Run the full suite "to check" before Phase 4 | ~5 min, and it pollutes the live DB, contaminating your own baseline |
| Mass regex-rewrite of path strings in .py files | Banned by AGENTS.md Safety Rule 1 (programmatic patching has burned this project before) |
| Full index rebuild "to be safe" | Re-embeds 50k+ chunks — real money (see Phase 5 formula) |
| Work on main | AGENTS.md branch discipline |
| `git add -A` before the ignore rules are verified | Stages personal journals into a public repo (root private/ is NOT ignored as of 2026-07-08) |
| Make tests pass by writing to BOTH trees | Entrenches the split; the campaign exists to end it |

## Provenance and maintenance

- Re-derive the inventory: the grep at the top of "The path-constant inventory".
- Re-measure divergence: `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/layout_audit.py`
- Re-check ignore gap: `git check-ignore private knowledge experts tracking; echo "exit=$? (1 = NOT ignored)"`
- Re-check red tests without a full run: `.venv/bin/pytest tests/test_experts.py tests/test_chat_persistence.py tests/test_experts_tts.py tests/test_debug.py -q`
- Re-check index rebuild cost driver: `grep -n "get_embeddings\|DROP TABLE" src/core/build_fts_index.py`
- Baselines in this file measured 2026-07-07/08; the DB and trees move daily — always re-capture in Phase 0.
