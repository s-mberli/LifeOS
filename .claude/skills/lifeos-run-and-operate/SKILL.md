---
name: lifeos-run-and-operate
description: The operations manual — how to run every component (Streamlit UI, FastAPI clipper sidecar, MCP server, CLI search, Telegram expert chat), what each scheduled pipeline does (daily TLDR ingest, weekly Hermes dispatch, VPS Lenny RSS + Syncthing), where every artifact lands, and what "healthy" looks like. Load this skill when starting or running any component, checking pipeline health, finding where an output landed, understanding schedules, or BEFORE manually triggering any pipeline.
---

# Run and Operate

**Prime caution:** several pipelines write state or PUBLISH publicly. Manual runs are never casual — read the pipeline's section first. All commands run from the repo root with the project venv.

## When NOT to use this skill

- Something errored → `lifeos-debugging-playbook`. Environment won't build → `lifeos-build-and-env`.
- Which env var controls what → `lifeos-config-and-flags`. Measuring health with numbers → `lifeos-diagnostics-and-tooling`.

## Runnable inventory

| Component | Command | Notes / health check |
|---|---|---|
| Streamlit chat UI | `streamlit run apps/streamlit-chat/app.py` | main UI (chat, ingestion, experts, library); needs .env keys for LLM features; healthy = browser opens, sidebar renders experts |
| Clipper API sidecar | `./start_api.sh` | uvicorn `src.api:app` on 127.0.0.1:8000; endpoint `POST /ingest` `{"url": "..."}` → runs `process_one_file` (verified src/api.py:56); consumed by the Firefox extension (apps/firefox-clipper); test: the curl line the script itself prints |
| MCP server | `.venv/bin/python src/core/mcp_server.py` | tools: `search_vault` (FTS, query ≤500 chars, private always excluded) and `read_vault_file` (data/-only ACL; data/private, .env, .git, binaries blocked); rate limit 60 req/min; every call audited to data/private/mcp_audit.log |
| CLI search | `.venv/bin/python -m src.core.search_knowledge "your query" -n 5` | read-only FTS probe; run from repo root (module imports require it) |
| Telegram expert chat helper | `.venv/bin/python scripts/expert_chat.py list \| load <slug> \| sources <slug>` | prints expert system prompts/sources for the Telegram mode (verified docstring scripts/expert_chat.py:1-9); reads ROOT-level experts/ |
| Manual pipeline entry points | see next section | ALL state-writing — cautions apply |

## Scheduled pipelines

### Daily TLDR ingest — launchd `com.lifeos.tldr_ingest`, 09:00 daily
`scripts/auto_tldr.py`. Steps: scrape tldr.tech archives for 14 topics (tech, ai, webdev, infosec, devops, founders, design, marketing, product, crypto, fintech, it, data, hardware — auto_tldr.py:48-63) → dedup against `tracking/tldr_ingest.json` (keyed by issue URL; deleting a key causes re-ingest) → write raw markdown to `knowledge/news/tldr_<slug>_<date>.md` → run `process_one_file(use_ai=True)` per issue (LLM summarization — **each issue costs LLM calls**; cost discipline applies) → insight notes land in `data/inbox/processed/needs-review/` or `data/knowledge/ai-resources/` per classification → full index rebuild at the end IF anything was processed. Logs: logs/tldr_ingest.log (+ logs/tldr_launchd*.log). Healthy signature: `--- [Topic] (slug) ---` blocks ending in `Done! Processed: N | Skipped: M | Failed: 0 | Errors: 0`.
Manual run: `.venv/bin/python scripts/auto_tldr.py` — writes tracking state, notes, DB rows, and spends LLM money.

### Weekly Hermes dispatch — launchd `com.lifeos.hermes_weekly`, Friday 08:00
`scripts/weekly_hermes_run.sh` → weekly_hermes_run.py. Steps: `triage_notes()` scores pending outbox rows (keyword scan: AI, Architecture, Github, Python, SQLite, Performance, Agent, LLM — triage_outbox.py:22; no LLM) → looks for a weekly digest in `knowledge/news/digest/` (**aspirational: that dir and its producer weekly_tldr_process.py have never existed — the fallback ALWAYS runs**) → fallback: collect articles from knowledge/news last 7 days → LLM selects 5-7 stories → fetches their full text → LLM writes the dispatch → `strip_artifacts()` → saves `data/inbox/content_drafts/weekly_dispatch_<date>.md` → optional architecture proposals to `data/inbox/proposals/` only when `INCLUDE_PROPOSALS=true` → stamps outbox rows `hermes_run_at` → `push_to_github` uploads to the TinaCMS website repo (`WEBSITE_GITHUB_TOKEN`/`WEBSITE_GITHUB_REPO`; path `src/content/notes/LifeOS-Weekly-Dispatch--<date>.md`, branch master; idempotent update-or-create).
**CAUTION: a manual run PUBLISHES to the public website if those env vars are set.** There is no human-approval gate inside the script — a known doctrine tension (privacy.yml says ask before publishing); see `lifeos-portfolio-and-positioning`. Logs: logs/weekly_hermes.log, logs/hermes_launchd*.log.

### VPS Lenny RSS + Syncthing + local sync — daily
Per docs/vps_deployment_guide.md: the VPS runs `scripts/monitor_lenny_rss.py` (cron 10:00) which triggers `scripts/ingest_lenny.py` for new episodes (no LLM calls); transcripts land in the shared tree and Syncthing mirrors between VPS and Mac; the Mac runs `scripts/sync_outbox.py` (cron 11:00) which scans root `knowledge/lenny-podcast/` and registers unregistered notes into automation_outbox (NFC-normalizing paths — verified sync_outbox.py:36-40). Sync conflicts produce `*.sync-conflict-*` files (real ones exist under data/inbox/content_drafts/) — resolve by diffing and deleting the conflict copy. Owner rule: the data/ tree is Syncthing territory; don't bulk-edit it locally while sync is active.
Note the layout wrinkle: the VPS guide describes syncing `data/`, while lenny files are read from root `knowledge/lenny-podcast` — part of the half-migration; see `lifeos-data-layout-unification-campaign`.

### Outbox lifecycle (the automation spine)
`src/core/ingest.py` inserts a row into `automation_outbox` on every note save → `triage_outbox.py` scores it and FTS-indexes actionable notes → the weekly run stamps `hermes_run_at`. State as of 2026-07-08: 803 rows, 73 unprocessed, 0 actionable-unstamped. Backlog check: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT COUNT(*) FROM automation_outbox WHERE processed_at IS NULL"`.

## Artifact map (which tree — verified per file, 2026-07-08)

| Artifact | Directory | Producer → Consumer |
|---|---|---|
| Raw TLDR issues | `knowledge/news/` (root) | auto_tldr → weekly hermes |
| Insight notes | `data/knowledge/ai-resources/` + `data/inbox/processed/needs-review/` | ingest.py → index, UI |
| Raw transcripts | `knowledge/ai-resources/raw/` (root; excluded from index & git) | ingest.py → archival |
| Weekly dispatches | `data/inbox/content_drafts/` | weekly hermes → owner review / website push |
| Proposals | `data/inbox/proposals/` (39 files) AND `inbox/proposals/` (21) — DIVERGED twins | hermes → owner → AGENTS.md workflow |
| Expert profiles | root `experts/` is what code reads (experts.py:91); `data/experts/` is what the indexer scans — the split in one row | experts.py / UI |
| Chat logs / insights | root `private/chat-logs/`, `knowledge/chat-insights/` | chat_persistence.py |
| Chunk reports | `outputs/reports/` | ingest.py |
| Dedup state | root `tracking/*.json` (tldr, lenny, events) | pipelines; atomic .tmp writes |
| TTS audio cache | root `tts_cache/` (tts.py:32); `data/tts_cache/` is a stale twin | tts.py |
| THE live DB | `indexes/lifeos.db` (~350 MB) | everything. `indexes/markusos.db` and `src/indexes/lifeos.db` are strays — never use them |

Log inventory: tldr_ingest.log, tldr_launchd(.err).log, weekly_hermes.log, hermes_launchd(_err).log, lenny_ingest.log, lenny_rss.log, ingestion.log — all under logs/ (gitignored).

State-file semantics: tracking/tldr_ingest.json — URL-keyed dict with topic/date/ingested_at; written atomically via .tmp+rename; deleting an entry re-ingests that issue on the next run. tracking/events_seen.json is a fossil of the removed event_tracker feature (scripts/event_tracker.py still present but the feature "moved to a separate project", commit 686c95d) — treat as legacy.

## Weekly health checklist (5 minutes)

1. `launchctl list | grep lifeos` from a real user terminal (sandboxed/agent shells often show nothing even when jobs are loaded — absence there proves nothing).
2. `ls -lt knowledge/news/ | head -3` — newest TLDR file should be ≤1 weekday old.
3. `ls -lt data/inbox/content_drafts/ | head -3` — newest dispatch ≤7 days old (Fridays).
4. `tail -15 logs/tldr_ingest.log logs/weekly_hermes.log` — look for the healthy signatures above; `[!]` lines mean provider failures (see `lifeos-debugging-playbook` #6).
5. Outbox backlog SQL (above) — unprocessed should drop to ~0 after each weekly run.
6. `find . -name "*sync-conflict*" -not -path "./.git/*"` — should be empty; if not, resolve.
7. `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/db_stats.py` — counts move up, never sharply down.

## Provenance and maintenance

- Schedules: `grep -A3 StartCalendarInterval com.lifeos.*.example.plist` (TLDR Hour 9; Hermes Weekday 5 = Friday, Hour 8).
- TLDR topic list: `sed -n '48,63p' scripts/auto_tldr.py`. Triage keywords: `grep -n "KEYWORDS" scripts/triage_outbox.py`.
- Dispatch destination: `grep -n "WEBSITE_GITHUB_REPO\|src/content/notes" scripts/weekly_hermes_run.py`.
- Digest-path status (aspirational as of 2026-07-08): `ls knowledge/news/digest 2>/dev/null || echo "still absent"` and `git log --all --oneline -- '*weekly_tldr_process*'` (empty).
- Artifact-map tree assignments drift with the layout campaign — re-verify with the campaign's inventory grep after any layout work.
- Outbox counts, file counts date-stamped 2026-07-08; they move daily.
