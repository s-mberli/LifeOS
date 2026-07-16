---
name: lifeos-build-and-env
description: Recreate the LifeOS working environment from scratch. Load when setting up the project on a new machine, fixing a broken venv, onboarding a new engineer or agent, diagnosing dependency or CI issues, installing the launchd scheduled jobs or the VPS/Syncthing leg, or when Python imports or the sqlite-vec extension fail ("sqlite-vec not available"). Covers Python version skew, .env setup, the untracked pre-commit gate, pip-audit CVE pins, and smoke tests.
---

# LifeOS build and environment recreation

All facts verified against the live repo as of **2026-07-07**. All commands are run from the repo root.

Glossary (defined once): **venv** = Python virtual environment at `.venv/`; **sqlite-vec** = loadable SQLite extension providing vector search; **live DB** = `indexes/lifeos.db`; **launchd** = macOS scheduled-job system; **Syncthing** = file-sync daemon linking `data/` between Mac and VPS.

## 1. Prerequisites and the Python version reality

There is a real version skew — state it, don't paper over it:

- README says **Python 3.11+**.
- CI (`.github/workflows/tests.yml`) pins **3.11** (ubuntu-latest, `pip install -r requirements.txt`, `pytest tests/`).
- The actual local venv on the primary machine runs **Python 3.14.6 (Homebrew)** — verified.

**Guidance:** use **3.11 to match CI** for reproducibility, unless you are deliberately replicating the primary box (3.14). All pins in `requirements.txt` are floors or old-but-working exact pins; the ones most likely to interact with 3.14 are the exact pins built before 3.14 existed (`streamlit==1.57.0`, `pandas==2.2.1`, `beautifulsoup4==4.12.3`, `PyYAML==6.0.1`, `youtube-transcript-api==0.6.2`) — they install fine on the local 3.14.6 box today, but a fresh resolve on 3.14 may need newer wheels. Full pin list (verified):

```
streamlit==1.57.0
pandas==2.2.1
pyarrow>=16.0.0
openai>=1.14.0
google-genai>=0.4.0
youtube-transcript-api==0.6.2
yt-dlp>=2024.04.09
beautifulsoup4==4.12.3
requests>=2.32.0
PyYAML==6.0.1
pytest>=8.2.0
litellm>=1.83.7
fastapi>=0.110.0
uvicorn>=0.29.0
httpx>=0.27.0
mcp>=1.0.0
pillow>=12.2.0
sqlite-vec>=0.1.3
PyGithub>=2.3.0
```

**Do NOT use the macOS system Python** — see the sqlite extension trap (step 4). Use Homebrew or python.org Python.

## 2. Install runbook

1. Clone the repo and `cd` into the repo root.
2. Create the venv with a Homebrew/python.org interpreter:
   ```sh
   python3.11 -m venv .venv        # or python3 if replicating the local 3.14 box
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -r requirements.txt
   ```
3. Configure environment:
   ```sh
   cp .env.example .env
   ```
   Fill the keys (names only listed here): `LLM_PROVIDER_ORDER`, Azure OpenAI block, `GEMINI_API_KEY`/`GEMINI_MODEL`, `OPENROUTER_API_KEY`/`OPENROUTER_MODEL`, `GITHUB_TOKEN`, ElevenLabs keys, `HERMES_BIN`/`HERMES_SCRIPT`.

   **KNOWN GAP (verified):** `.env.example` is missing **`WEBSITE_GITHUB_TOKEN`** and **`WEBSITE_GITHUB_REPO`**, which `scripts/weekly_hermes_run.py` reads for the weekly dispatch GitHub push. Add them to `.env` manually. Full config catalog: see **lifeos-config-and-flags**.
4. Install the pre-commit gate (step 5) and run the smoke tests (step 6).

## 3. Fresh clone reality check

- A fresh clone has **no database**. `indexes/*.db` is git-ignored and Syncthing-ignored. `get_db_connection()` in `src/core/db.py` creates the schema on first use, so nothing crashes — but search returns nothing until content is indexed.
- **Cost warning:** populating embeddings calls OpenRouter and costs real money (the live DB holds ~50k embedded chunks, ~350 MB — exact numbers via db_stats.py in **lifeos-diagnostics-and-tooling**). Never trigger mass re-embedding casually. See **lifeos-rag-reference**.
- **Stray DB files trap:** `indexes/markusos.db` and `src/indexes/lifeos.db` exist but are **NOT** the live DB. The live DB is `indexes/lifeos.db` only.

## 4. The sqlite extension trap (most common silent failure)

`src/core/db.py` loads sqlite-vec via `conn.enable_load_extension(True)` inside a try/except; on failure it merely logs `"sqlite-vec not available, vector search disabled"` and continues — **vector search silently disappears**. The macOS *system* Python is compiled without loadable-extension support (`enable_load_extension` raises `AttributeError`), which is exactly this failure mode. Remedy: build the venv with Homebrew or python.org Python.

One-line smoke test (verified passing on the local 3.14.6 venv, prints `vec OK`):

```sh
.venv/bin/python -c "import sqlite3,sqlite_vec; c=sqlite3.connect(':memory:'); c.enable_load_extension(True); sqlite_vec.load(c); print('vec OK')"
```

## 5. Pre-commit gate installation — CRITICAL TRAP

The security hook lives **only** in `.git/hooks/pre-commit` — it is **not tracked** (verified: `git ls-files | grep -i hook` is empty). **A fresh clone has NO gate.**

- Copy the hook from an existing machine into `.git/hooks/pre-commit` and `chmod +x` it.
- Stages, briefly: secret/guarded-string scanning of the staged diff, plus `bandit` static-analysis and `pip-audit` dependency-audit passes. Do not reproduce its guarded strings anywhere; details live in **lifeos-security-and-privacy**.
- The hook requires **pip-audit and bandit in the venv**. Verified installed locally (`bandit 1.9.4`, `pip_audit 2.10.1`) but they are **NOT in requirements.txt** — install them separately:
  ```sh
  .venv/bin/pip install bandit pip-audit
  ```

### pip-audit CVE situation

The hook pins **16 `--ignore-vuln` CVEs** (verified count) affecting litellm / aiohttp / python-dotenv — advisories with no installable fix wheels. Consequence for env recreation: a fresh `pip install -r requirements.txt` may pull versions carrying the same advisories; that is expected and accepted. The ignore-list policy lives in **lifeos-change-control**.

## 6. Smoke tests after build

Cheap, safe, in order:

1. Import check: `.venv/bin/python -c "import src.core.db, src.core.frontmatter; print('imports OK')"`
2. sqlite-vec check (step 4) — expect `vec OK`.
3. One safe pytest slice — DB-free (uses only `tmp_path`, no network; verified by reading it):
   ```sh
   .venv/bin/pytest tests/test_frontmatter.py -q
   ```
   Verified result: **7 passed in 0.53s**.
4. DB sanity (only meaningful on a machine that has the live DB):
   ```sh
   sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT COUNT(*) FROM search_index"
   ```
   (`immutable=1` is required — plain `mode=ro` fails on this WAL database.) Verified: **50134** on the primary machine as of 2026-07-07; the count grows daily. A fresh clone has no DB (step 3).

**WARNING — never run the full pytest suite casually.** As of 2026-07-07 it has **10 known failures** out of 198 (dual data-layout half-migration; owned by **lifeos-data-layout-unification-campaign**), takes ~5 minutes, and **writes to the live DB** via `test_agent_harness`.

## 7. Scheduled jobs (local Mac, launchd)

Templates in the repo root (verified): `com.lifeos.tldr_ingest.example.plist`, `com.lifeos.hermes_weekly.example.plist` (plus `com.lifeos.lenny_ingest.example.plist`). Placeholders are literally `/path/to/LifeOS`.

1. Copy each to `~/Library/LaunchAgents/` (drop `.example`) and replace every `/path/to/LifeOS` with the real repo root.
2. `launchctl load ~/Library/LaunchAgents/com.lifeos.tldr_ingest.plist` (and hermes_weekly).
3. Verify: `launchctl list | grep lifeos`.

Schedules (verified from plist integers): TLDR ingest daily **09:00** (`Hour 9, Minute 0`); Hermes weekly **Friday 08:00** (`Weekday 5, Hour 8, Minute 0` — launchd Weekday 5 = Friday). Stdout/stderr land in `logs/`.

## 8. VPS + Syncthing leg

Summary of `docs/vps_deployment_guide.md` (verified):

- **VPS**: runs `scripts/monitor_lenny_rss.py` daily via cron (guide suggests 10:00); new episodes trigger `scripts/ingest_lenny.py` on the VPS; transcripts land in the shared `data/` directory.
- **Sync**: `data/` syncs Mac↔VPS via Syncthing. `.stignore` excludes `.git/`, `.venv/`, `indexes/*.db` (+journal/wal/shm), `logs/`, caches, editor dirs.
- **Mac**: local cron runs `scripts/sync_outbox.py` at **11:00** (shortly after the VPS run) to pull synced transcripts into the automation outbox and FTS index.
- **KNOWN DOC BUG (verified):** the guide's venv step says `python3 -m venv .env` — that should be `.venv` (the very next line uses `.venv/bin/pip`). Following it literally creates a venv named `.env` that collides conceptually with the secrets file.
- **Owner rule:** `data/` is Syncthing territory — never bulk-edit it locally while sync is active.

## 9. Optional components

- **Ingestion API sidecar**: `./start_api.sh` — activates `.venv` and runs `uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload` (FastAPI backend for the Firefox clipper; test with `POST /ingest`).
- **Firefox clipper**: `apps/firefox-clipper/` (manifest + background.js) — see its `README.md` for install.
- **MCP server**: see **lifeos-run-and-operate**.
- **Obsidian**: `.obsidian/` exists — the repo root opens directly as an Obsidian vault.

## 10. Known traps recap

| Trap | Symptom | Fix |
|---|---|---|
| System-Python extension loading | `sqlite-vec not available` warning; vector search silently off | Rebuild venv with Homebrew/python.org Python; run the `vec OK` one-liner |
| Missing hook on fresh clone | Commits bypass the security gate with no error | Copy `.git/hooks/pre-commit` from an existing machine, `chmod +x`, install bandit + pip-audit |
| `.env.example` drift | Weekly dispatch GitHub push fails | Add `WEBSITE_GITHUB_TOKEN` / `WEBSITE_GITHUB_REPO` manually (lifeos-config-and-flags) |
| Full suite pollutes DB | Live-DB writes via `test_agent_harness`; 10 known failures, ~5 min | Run targeted safe test files only |
| Python version skew | Local 3.14.6 vs CI 3.11 → resolver differences | Pin to 3.11 for reproducibility unless replicating the local box |
| Fresh clone empty DB | Searches return nothing; schema auto-created on first use | Index content deliberately — embedding costs real API money (lifeos-rag-reference) |
| Stray DB files | Confusion over which DB is live | `indexes/markusos.db` and `src/indexes/lifeos.db` are NOT the live DB; only `indexes/lifeos.db` is |

## When NOT to use this skill

- Debugging application/runtime failures once the env works → **lifeos-debugging-playbook** / **lifeos-run-and-operate**.
- Config key semantics and flags → **lifeos-config-and-flags**.
- RAG/index internals, re-embedding cost decisions → **lifeos-rag-reference**.
- Hook contents, secret policy → **lifeos-security-and-privacy**.
- CVE ignore-list changes → **lifeos-change-control**.
- The 10 failing tests → **lifeos-data-layout-unification-campaign**.

## Provenance and maintenance

- Verified against the live repo and venv on 2026-07-07; smoke tests in step 6 were actually run (vec OK; 7 passed; 50134 rows).
- Re-verify after: Python or requirements changes, hook edits, plist schedule changes, or the data-layout unification landing.
- Unverified items are labeled inline; everything else is ground truth from this audit.
