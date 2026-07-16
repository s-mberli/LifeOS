---
name: lifeos-debugging-playbook
description: >
  Symptom-to-triage playbook for LifeOS/MarkusOS failures. Load this whenever
  anything in this repo errors or behaves unexpectedly: failing pytest tests,
  empty or wrong search results, "no such module: vec0", "sqlite-vec not
  available" warnings, a suddenly tiny/empty lifeos.db, LLM provider cascade
  failures ("[!] ... call failed"), JSON parse failures, Streamlit stale-cache
  signature errors, ModuleNotFoundError for src, Syncthing *.sync-conflict-*
  files, launchd jobs not firing, embeddings 429 rate limits, template
  artifacts in weekly dispatches, notes routed to needs-review, or confusion
  about which SQLite DB file is live.
---

# LifeOS Debugging Playbook

Symptom-first triage for this repo's real failure modes. Every entry: symptom,
ranked causes, a cheap **discriminating experiment** (read-only), the fix or
the sibling skill that owns it. All commands run from the repo root. Facts
date-stamped "as of 2026-07-07" are volatile; re-verify per the Provenance
section.

**Glossary (once):** *live DB* = `indexes/lifeos.db` (350MB+, FTS5 + sqlite-vec).
*FTS* = SQLite FTS5 full-text index table `search_index`. *vec* = `vec_docs`
virtual table (768-dim embeddings, requires the `sqlite-vec` extension).
*Provider cascade* = `try_providers` in `src/core/llm_client.py`, ordered by
env var `LLM_PROVIDER_ORDER` (default `openrouter,gemini`).

## When NOT to use this skill

- Designing a change or asking "how should this work" → lifeos-architecture-contract.
- Making/approving edits, commit discipline → lifeos-change-control.
- How retrieval is *supposed* to work (RRF, chunking) → lifeos-rag-reference.
- Env/venv/dependency setup → lifeos-build-and-env.
- Normal operations (launchd install, Syncthing topology, VPS) → lifeos-run-and-operate.
- Config/env vars/flags reference → lifeos-config-and-flags.
- Past incidents' full write-ups → lifeos-failure-archaeology (check it FIRST
  for anything that smells familiar — don't re-fight settled battles).

## Master triage table

| # | Symptom | Most likely cause | First discriminating check |
|---|---------|-------------------|----------------------------|
| 1 | Tests fail on main (~10 failures) | Half-migrated data layout + one intentionally-red scaffold test | Run ONE cheap test file, never the full suite |
| 2 | `no such module: vec0` from sqlite3 CLI | Expected: CLI can't load sqlite-vec | Use `.venv/bin/python` + `get_db_connection` instead |
| 3 | `sqlite-vec not available, vector search disabled` | Package missing/broken in venv | `.venv/bin/python -c "import sqlite_vec"` |
| 4 | DB suddenly tiny/empty, search returns nothing | `get_db_connection` silently DELETED a corrupted DB | `ls -lh indexes/lifeos.db` — is it megabytes or kilobytes? |
| 5 | Search misses a specific/recent note | Note outside indexed dirs; FTS fallback ladder; stale index | Read-only SQL prefix counts (below) |
| 6 | `[!] <Provider> call failed: ...` lines | Provider outage/key/quota; cascade falling through | Which provider lines appear in stdout/log |
| 7 | `[!] Failed to parse JSON` | LLM returned non-JSON / fenced JSON | Read printed raw output; query `agent_repair_logs` |
| 8 | Streamlit TypeError about function arguments after a code change | Stale `st.cache` holding old function signature | Restart Streamlit / clear cache |
| 9 | `ModuleNotFoundError: No module named 'src'` | Script run from wrong cwd or wrong python | Run from repo root with `.venv/bin/python` |
| 10 | `*.sync-conflict-*` files appear | VPS and Mac both wrote the same file | `diff` original vs conflict copy |
| 11 | launchd job didn't fire | Plist not loaded / stale paths | `launchctl list \| grep lifeos`; read `logs/*_launchd*.log` |
| 12 | `Rate limit exceeded (429)` from embeddings | OpenRouter embeddings rate limit | Check batch size / retry later; beware zero-vector trap (below) |
| 13 | Template artifacts in published dispatch | LLM echoed sample/footer text | Check `strip_artifacts()` patterns in `scripts/weekly_hermes_run.py` |
| 14 | Ingested note landed in needs-review | `classify_input.classify` raised → fallback routing | Read ingestion log line "Warning: classify_input failed" |
| 15 | Debugging the wrong DB file | `indexes/markusos.db` or `src/indexes/lifeos.db` are NOT live | `ls -lh indexes/*.db src/indexes/*.db` |

---

## 0. Read-only SQLite access (prerequisite for many checks)

Canonical read-only CLI open (this is the form every skill in this library uses):

```
sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT COUNT(*) FROM search_index;"
# → 50134   (as of 2026-07-07; grows daily)
```

Why not plain `mode=ro`: observed (2026-07-07) it fails with
`Error: in prepare, unable to open database file (14)` because the DB is in
WAL mode and a read-only open still wants to map the `-shm` file. The
`immutable=1` flag avoids that.

Caveat: `immutable=1` assumes no concurrent writer; fine for quick counts,
don't trust it mid-rebuild. For anything involving `vec_docs`, the CLI cannot
help (see §2) — use:

```
.venv/bin/python -c "
from src.core.db import get_db_connection
c = get_db_connection()
print(c.execute('SELECT COUNT(*) FROM vec_docs').fetchone()[0])
c.close()"
# → 50134   (as of 2026-07-07)
```

**Warning:** `get_db_connection()` is NOT purely read-only — it runs
`init_db()` (idempotent CREATEs) and carries the corruption-delete trap (§4).
Only point it at the live DB when the DB is known-healthy, and only run SELECTs.

---

## 1. Failing tests on main

**Symptom (as of 2026-07-07):** suite is red — 10 failed / 188 passed.
This is a *known state*, not necessarily your change.

**Causes, ranked:**
1. **Half-migrated data layout (~8 failures).** `tests/conftest.py` builds tmp
   trees under `data/knowledge`, `data/experts`, `data/inbox/raw` (old layout),
   but `src/core/experts.py` reads root `experts/` (`experts_dir = root /
   "experts"`, line ~91) and `src/core/chat_persistence.py` writes root
   `private/chat-logs` (`log_dir = ROOT / "private" / "chat-logs"`, line ~40).
   Fixtures and code disagree; tests fail. Fix is owned by
   **lifeos-data-layout-unification-campaign** — do not patch piecemeal.
2. **`tests/test_debug.py` is permanently red by design.** It is a leftover
   debug scaffold whose single test ends with a literal `assert False`
   (verified). Ignore it or route its removal to lifeos-change-control.
3. Only after ruling out 1–2: your change actually broke something.

**Discriminating experiment — run ONE cheap test file, never the suite:**

```
.venv/bin/pytest tests/test_experts.py -x -q
```

**NEVER run the full suite casually.** Two reasons, both verified:
- it takes ~5 minutes;
- tests write rows into the **live** `indexes/lifeos.db` — `agent_repair_logs`
  contains 367 rows as of 2026-07-07, latest entries
  `persistently_failing | ui | ValueError | UnknownRepair` timestamped from a
  test run. `tests/test_agent_harness.py` is the main offender; never run it
  against the live DB.

Confirm test pollution read-only:

```
sqlite3 'file:indexes/lifeos.db?immutable=1' \
  "SELECT timestamp, function_name, mode, error_type FROM agent_repair_logs ORDER BY id DESC LIMIT 3;"
# 2026-07-07T01:55:24...|persistently_failing|ui|ValueError
```

---

## 2. `no such module: vec0` from the sqlite3 CLI

**Symptom (real output):**

```
$ sqlite3 'file:indexes/lifeos.db?immutable=1' "SELECT COUNT(*) FROM vec_docs;"
Error: in prepare, no such module: vec0
```

**Cause:** expected behavior, not corruption. `vec_docs` is a `vec0` virtual
table; the stock sqlite3 CLI has no sqlite-vec extension loaded. The loader
lives in `src/core/db.py` lines 42–49: `import sqlite_vec` →
`conn.enable_load_extension(True)` → `sqlite_vec.load(conn)`.

**Fix:** query vec tables via `.venv/bin/python` with
`src.core.db.get_db_connection` (see §0). Use the CLI only for non-vec tables
(`search_index`, `doc_chunks`, `agent_repair_logs`, ...).

## 3. Warning: `sqlite-vec not available, vector search disabled`

**Symptom:** that logging.warning at connection time (emitted by the
except-clause in `src/core/db.py:48-49` on ImportError/OperationalError/
AttributeError). Connection still succeeds — graceful degradation.

**Consequences (verified in `src/core/search_knowledge.py` `hybrid_search`):**
the `vec_docs MATCH` query raises OperationalError → fallback loads **ALL**
rows of `vec_docs` and computes cosine similarity in Python (slow, ~50k rows),
or if `vec_docs` itself is unreadable, results become FTS-only. Search still
"works", just slow and/or lexical-only.

**Discriminating experiment:**

```
.venv/bin/python -c "import sqlite_vec; print('ok')"
```

`ok` → extension importable; the warning came from a different interpreter
(system python, CI's 3.11, wrong venv). ImportError → reinstall in the venv
(see lifeos-build-and-env).

## 4. DANGEROUS trap: `get_db_connection` silently deletes a corrupted DB

**Symptom:** `indexes/lifeos.db` suddenly kilobytes instead of ~350MB; all
search results gone; no error anywhere.

**Cause (verified, `src/core/db.py:21-31`):** on open, the connection runs
`PRAGMA integrity_check`; if `sqlite3.DatabaseError`/`OperationalError` is
raised it **unlinks the DB file and recreates it empty**. Any code path that
calls `get_db_connection` — tests, Streamlit, scripts — can trigger this.

**Discriminating experiment:**

```
ls -lh indexes/lifeos.db
# healthy as of 2026-07-07: ~350M. Kilobytes = it was deleted and recreated.
```

**Prevention (owner rule):** back up `indexes/lifeos.db` before risky
operations; NEVER point experimental code at the live DB — pass a scratch
`db_path` (the function accepts one). Recovery: restore from backup or rebuild
via `src/core/build_fts_index.py` (state-writing — coordinate per
lifeos-change-control; embeddings rebuild costs API calls, see §12).

## 5. Search returns nothing / misses recent notes

Root-cause tree, ranked:

**(a) Note is outside the indexed directories.** `src/core/build_fts_index.py`
`DIRECTORIES_TO_INDEX` (verified at top of file) covers only:
`data/knowledge`, `data/private`, `data/inbox`, `data/experts`,
`data/business`, `data/career`, and `outputs`. A note saved to the root
`knowledge/` tree (which exists and receives TLDR ingests as of 2026-07-07) is
**never indexed**. This is the same half-migration as §1; fixes route to
lifeos-data-layout-unification-campaign.

Discriminator (real output, 2026-07-07):

```
sqlite3 'file:indexes/lifeos.db?immutable=1' \
  "SELECT COUNT(*) FROM search_index WHERE path LIKE 'data/knowledge/%';"   # → 34287
sqlite3 'file:indexes/lifeos.db?immutable=1' \
  "SELECT COUNT(*) FROM search_index WHERE path LIKE 'knowledge/%';"        # → 0
# All indexed prefixes: data/ (49130 rows) and outputs/ (1004 rows). Nothing else.
```

**(b) FTS query syntax error is swallowed.** In `search_knowledge.py`, every
`OperationalError` from a MATCH is caught with `pass` and the code walks a
silent fallback ladder: raw query → tokens joined with AND → OR → single
phrase MATCH → LIKE. You never see the syntax error; you just see different
(often worse) results.

**(c) Stopword/short-token filtering emptied the query.** `hybrid_search`
drops STOPWORDS, digit-only tokens, and single-character tokens. A query like
"what is it" tokenizes to nothing → FTS branch skipped entirely. Also note the
injection-pattern guard: queries containing `'=`, `'; `, `; --`, `' OR `,
`' AND ` return `[]` immediately.

**(d) Index is stale** — note is in an indexed dir but was added after the
last rebuild. Discriminator: `sqlite3 ... "SELECT COUNT(*) FROM search_index
WHERE path LIKE '%<slug-fragment>%';"`. Rebuild owner: build_fts_index (do NOT
run it as part of debugging — it drops and rebuilds all three tables).

Also remember: results with `data/private/` in the path are filtered out
unless `include_private=True`.

## 6. LLM provider cascade failures

**Symptom:** stdout/log lines like

```
  [Openrouter] Attempting call | Max Tokens: 4096
    [!] Openrouter call failed: ...
  [Gemini] Attempting call | Max Tokens: 4096
```

**Mechanics (verified, `src/core/llm_client.py` `try_providers`):** providers
tried in `LLM_PROVIDER_ORDER` (default `openrouter,gemini`; also supports
`deepseek`, `azure`). Empty/filtered content raises
`ValueError("Provider returned empty or filtered content")` and falls through
to the next provider. All fail → returns `None` → callers degrade differently;
notably the weekly pipeline writes a placeholder dispatch containing
"No dispatch generated this week due to content filters or API errors." and
`push_to_github` refuses to push placeholders (verified in
`scripts/weekly_hermes_run.py`).

**Discriminator:** which `[!] <Provider> call failed:` lines appear tells you
where in the cascade it died. API keys are masked to `[MASKED]` in these
errors by `sanitize_err` — if you see a raw key, that's a security bug (route
to lifeos-security-and-privacy). Key/model config reference:
lifeos-config-and-flags.

## 7. JSON parse failures from LLMs

**Symptom:**

```
  [!] Failed to parse JSON: ...
  [!] Raw output was: '...'
```

**Mechanics (verified):** `parse_json_safely` strips leading ```` ```json ````
or ```` ``` ```` fences (and trailing fence) before `json.loads`; on failure
it prints both lines above and returns `None`. Callers wrapped in
`src/core/agent_harness.py` `execute_with_repair` retry:
`background` mode = up to `max_attempts` retries (default 3, i.e. 4 total
attempts) with exponential backoff `2**(attempt-1)`s applied only for
TimeoutError; `ui` mode = 1 fast retry (2 total attempts). Every failed
attempt is logged to `agent_repair_logs` in the live DB; exhaustion raises
`AgentEscalationError("Agent failed after N attempt(s) in <mode> mode: ...")`.

**Read the repair history (read-only):**

```
sqlite3 'file:indexes/lifeos.db?immutable=1' \
  "SELECT timestamp, function_name, mode, error_type, repair_strategy
   FROM agent_repair_logs ORDER BY id DESC LIMIT 10;"
```

Strategy names: `SchemaCorrectionRepair` (JSONDecodeError),
`ExponentialBackoffRepair` (TimeoutError), `UnknownRepair` (everything else).

## 8. Streamlit stale-cache signature errors

**Symptom:** after editing a cached function's signature, the running
Streamlit app throws TypeError/argument-mismatch errors on calls into
`fts_search` or `execute_agent_search_loop`.

**History (verified via `git show`):** commits `4b8430a` ("fix: handle cached
fts_search signature in Streamlit UI") and `53d8c14` ("fix: handle cached
execute_agent_search_loop signature in Streamlit UI") — both touch
`apps/streamlit-chat/ui/chat.py`, which now defends by handling both old and
new cached signatures.

**Fix:** restart the Streamlit process / clear its cache after signature
changes. If the defensive shims in `ui/chat.py` don't cover a new signature,
extend them the same way those commits did.

## 9. Import path errors (`ModuleNotFoundError: No module named 'src'`)

**Cause:** repo code imports `from src.core...`; scripts bootstrap with
`sys.path.insert(0, str(ROOT))` (verified pattern in `scripts/auto_tldr.py`,
`scripts/backfill_metadata.py`, `scripts/monitor_lenny_rss.py`, etc.). Running
from the wrong cwd or with a python that isn't the venv breaks this. History:
commits `6138c99`, `8e3fc80`, `3a2a218` all fixed variants of this.

**Rule:** run scripts **from the repo root** with `.venv/bin/python`, e.g.
`.venv/bin/python scripts/<name>.py`, or `.venv/bin/python -m src.core.<mod>`.

## 10. Syncthing conflict files

**Symptom:** files like (real examples, verified present):

```
data/inbox/content_drafts/weekly_dispatch_2026-06-28.sync-conflict-20260628-162458-LSJLSB6.md
data/inbox/content_drafts/weekly_dispatch_2026-07-05.sync-conflict-20260705-131728-IUNZ2HY.md
```

**Cause:** the VPS and the Mac both wrote the same file between syncs;
Syncthing keeps both. **Handling:** `diff` the original against the conflict
copy, merge manually into the original, then delete the conflict file.
**Prevention (owner rule):** `data/` is machine-shared territory — one writer
per file. Sync topology and which machine owns what:
**lifeos-run-and-operate**.

Find them all: `find data -name '*.sync-conflict-*'`

## 11. launchd job didn't fire

**Symptom:** no new TLDR/Lenny/Hermes output at the scheduled time.

**Checks:**

```
launchctl list | grep lifeos          # empty ⇒ plists not loaded for this user session
tail -20 logs/tldr_launchd.log logs/tldr_launchd_err.log
tail -20 logs/hermes_launchd.log logs/hermes_launchd_err.log
```

Healthy tldr log tail looks like (real output, 2026-07-06 run):
`Done! Processed: 57 | Skipped: 123 | Failed: 0 | Errors: 2`.

Plists are user-installed from the three `*.example.plist` templates at repo
root (`com.lifeos.tldr_ingest`, `com.lifeos.lenny_ingest`,
`com.lifeos.hermes_weekly`) with real absolute paths filled in — a template
copied verbatim will have placeholder paths and silently fail. Install
procedure: **lifeos-run-and-operate**.

## 12. Embeddings 429 rate limit — and the zero-vector trap

**Symptom:** `Exception: Rate limit exceeded (429)` from `get_embeddings`
(verified: raised on HTTP 429 from the OpenRouter `/embeddings` endpoint,
model `nomic-ai/nomic-embed-text-v1.5`, batch_size 500, inputs truncated to
8000 chars).

**The subtle trap (verified in `hybrid_search`):** when embedding the *query*,
any exception — including this 429 — is swallowed:

```python
except Exception:
    query_emb = [0.0] * 768
```

Search does NOT error. It proceeds with a zero vector, so KNN
distances/similarities are meaningless — semantic ranking silently degrades to
noise while results still look plausible (FTS half of the RRF fusion still
works). **If semantic search seems oddly lexical, suspect a failed query
embedding first.** Discriminator: run
`.venv/bin/python -c "from src.core.llm_client import get_embeddings; print(len(get_embeddings('test')))"`
(costs one tiny API call) — an exception here means every hybrid_search query
is currently running on zero vectors.

## 13. Weekly dispatch content problems (template artifacts)

**Symptom:** published posts containing "Sample dispatch generated for format
review", "Generated by Hermes...", or "Review, edit, and publish at your
discretion...".

**History (verified via git log):** `2b7b529` introduced the Hermes 3-output
workflow with a sample dispatch; the LLM then echoed the sample banner and
footer into real posts; `99313eb` and `86ef0ec` hardened the pipeline, and
`strip_artifacts()` (`scripts/weekly_hermes_run.py:172`) now regex-strips
exactly those three patterns before publishing.

**Fix for new artifacts:** extend the regex patterns in `strip_artifacts()` —
that function is the single home for output sanitization. Prompt-side fixes:
lifeos-docs-and-writing owns dispatch templates.

## 14. Ingestion: note went to needs-review

**Symptom:** an ingested note lands in `data/inbox/processed/needs-review/`
instead of a knowledge folder.

**Mechanics (verified, `src/core/ingest.py` `_get_routing_decision`):**
1. Normal path: `src.core.classify_input.classify(combined_text)` returns the
   routing decision including `storage_location`.
2. If `classify` **raises**, the log shows
   `Warning: classify_input failed (<exc>), using fallback routing` and the
   fallback decision hard-codes `storage_location:
   "data/inbox/processed/needs-review/"` with `primary_mode: "router"`.
3. YouTube override: if the title contains an AI keyword (deepseek, ai, llm,
   model, openai, gemini, claude, rag, agent, embedding), the decision is
   overridden to `data/knowledge/ai-resources/` regardless of classify output.

**Discriminator:** grep the ingestion log for the warning line. Present →
debug `classify_input` (often an LLM/JSON failure, see §6/§7). Absent → the
classifier itself chose needs-review; inspect its prompt/logic.

## 15. Two suspicious DB files — don't debug the wrong one

Verified layout as of 2026-07-07:

```
indexes/lifeos.db       350M  ← THE LIVE DB (FTS + vec_docs + doc_chunks + logs tables)
indexes/markusos.db     376K  ← legacy (last touched May 25); FTS-only tables
src/indexes/lifeos.db    24K  ← stray artifact; FTS-only tables
```

Both non-live files contain only `search_index*` FTS shadow tables — no
`vec_docs`, no `doc_chunks`, no `agent_repair_logs` (verified with `.tables`).
All code paths resolve `BASE_DIR / "indexes" / "lifeos.db"` from
`src/core/db.py`, so the live one is `indexes/lifeos.db`. If your counts look
absurdly small, check which file you opened. Whether the two strays should be
deleted is **open** — route to lifeos-change-control.

---

## Escalation

If the discriminating experiments don't resolve it:
1. Check **lifeos-failure-archaeology** — the failure may be a settled battle
   with a known verdict.
2. Record your symptom, experiments, and observations per
   **lifeos-research-and-proof-methodology** before trying fixes, so the next
   person (or agent) doesn't repeat the triage.
3. Fixes that touch the data layout, live DB, or pipelines go through
   **lifeos-change-control**; layout-migration fixes belong to
   **lifeos-data-layout-unification-campaign**.

## Provenance and maintenance

All claims verified by direct code inspection and read-only experiments on
2026-07-07. One-line re-verification commands (repo root):

- Corruption-delete trap: `sed -n '21,31p' src/core/db.py`
- vec loader: `sed -n '42,49p' src/core/db.py`
- Indexed dirs: `sed -n '13,21p' src/core/build_fts_index.py`
- Zero-vector trap: `grep -n '0.0] \* 768' src/core/search_knowledge.py`
- Fallback ladder: `grep -n 'OperationalError' src/core/search_knowledge.py`
- Provider cascade: `grep -n 'call failed\|LLM_PROVIDER_ORDER' src/core/llm_client.py`
- Repair harness: `grep -n 'limit = max_attempts' src/core/agent_harness.py`
- Layout split: `grep -n '"experts"' src/core/experts.py; grep -n 'chat-logs' src/core/chat_persistence.py; grep -n 'data' tests/conftest.py | head`
- Red scaffold: `tail -1 tests/test_debug.py`  (→ `assert False`)
- Live DB size/counts: `ls -lh indexes/*.db src/indexes/*.db` and the §0 queries
- strip_artifacts: `sed -n '172,190p' scripts/weekly_hermes_run.py`
- needs-review fallback: `grep -n 'needs-review' src/core/ingest.py`
- History: `git show --stat 4b8430a 53d8c14 6138c99 8e3fc80 3a2a218 86ef0ec 99313eb 2b7b529`

Failure counts ("10 failed / 188 passed") and row counts (50134 chunks, 367
repair-log rows) are as-of-2026-07-07 snapshots; expect drift.
