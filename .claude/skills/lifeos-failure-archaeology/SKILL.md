---
name: lifeos-failure-archaeology
description: The chronicle of every major investigation, dead end, rejected approach, and revert in MarkusOS/LifeOS history. Load BEFORE starting any investigation, refactor, or debugging campaign to check whether the battle was already fought; when a symptom feels familiar; when tempted to revert a change or re-try an old approach (API sync, threaded re-indexing, path "fixes"); when git history, branches, or stale artifacts look confusing. Prevents re-fighting settled battles.
---

# LifeOS Failure Archaeology

As of **2026-07-07**. Every entry is grounded in commit hashes, files, or local artifacts. Repo root is the project root; all paths and commands are relative to it. Anything under `.agents/` is a **local-only artifact (gitignored)** — never commit it.

**When NOT to use this skill:** live incident triage (→ `lifeos-debugging-playbook`), making a new change safely (→ `lifeos-change-control`), fixing the data-layout split (→ `lifeos-data-layout-unification-campaign`), security prevention rules (→ `lifeos-security-and-privacy`), RAG internals (→ `lifeos-rag-reference`).

## Index

| # | Battle | Status | One-line lesson |
|---|--------|--------|-----------------|
| 1 | PII/secrets leak → git history rewrite | settled | Scrub before you publish; history rewrites are the costliest fix. Prevention now lives in the pre-commit hard-gate. |
| 2 | data/ restructure fallout | **still-live** | A tree move without a code-path sweep splits the codebase into two realities. |
| 3 | M1–M5 RAG scaling campaign | settled | Multi-agent orchestration converged, but burned 5 orchestrator generations on one sort-math test. |
| 4 | Test-suite indexing hang | settled | Tests that trigger real index rebuilds hang; mock `build_index`. |
| 5 | TicNote API sync → manual inbox pivot | settled (approach rejected) | Background API sync was removed same day it landed; manual file drops won. |
| 6 | CodeQL dead branch | superseded | `feat/fix-codeql-tests` is pre-restructure; its useful idea re-landed on main. |
| 7 | Weekly dispatch quality battles | **partially-fixed / still-live gap** | Path bug + template leaks fixed; the "digest-first" primary path points at a producer that never existed. |
| 8 | event_tracker in/out | settled | Out-of-scope features get extracted, not accreted (one commit in, one commit out). |
| 9 | litellm CVE bypass | accepted risk | 16 CVEs pinned in pre-commit pip-audit; revisit when fix wheels ship. |
| 10 | Streamlit cache/import battles | recurring class (settled instances) | `st.cache_*` pins old function signatures/import paths across refactors. |
| 11 | Legacy artifacts as fossils | still-live (hygiene) | Stale DBs, .bak files, dead branches, sync-conflict files each mark a past battle. |
| 12 | Self-repairing agent harness | settled, with live hygiene defect | Harness works; test fixtures pollute the live DB's repair log (240+ rows). |

---

## Entry format ("how to add an entry")

```markdown
### N. <Battle name>
- **Symptom/Trigger:** what was observed or what prompted the work
- **Root cause:** the actual mechanism
- **Evidence:** commit hashes (`git show <hash>`), file paths, local artifacts (mark gitignored ones)
- **Resolution:** what was done (or rejected, and why)
- **Status:** settled / still-live / partially-fixed — and which skill owns follow-up
```
Update the Index table too. If a story cannot be confirmed, label it "inferred — verify with `<command>`".

---

## The Chronicle

### 1. PII/secrets leak → git history rewrite (the costliest failure)
- **Symptom/Trigger:** Preparing the repo for public release surfaced the operator's personal name, email, and secret-looking strings baked into commits, files, and git author metadata.
- **Root cause:** The project began as a private vault; identity and dummy-secret hygiene was never enforced, so PII accumulated in tracked files and in commit authorship itself.
- **Evidence:** Pre-release audits `8980e99` (pre-release security audit), `832b56d` (remove sensitive files), `2c86a96` (remove personal name from LICENSE); hardening `fb8902e` (SSRF blocklist + path-traversal protection in `src/core/chat_context.py`, `scripts/update_docs.py`); scrub commits `0bb27d4` (scrub all personal name references, untrack `.git-mailmap`), `51ba952` (scrub plists, pre-commit hook), `5213801` (scrub author PII, replace hardcoded secret placeholder in tests); CHANGELOG.md `[2026-06-26]` "Git History Scrubbing: Rewrote git history using `git filter-repo` and `.mailmap`". Early history now shows the rewritten author `Developer <developer@example.com>`.
- **Resolution:** Full `git filter-repo` history rewrite + `.mailmap`, hardcoded dummy secrets replaced with scanner-safe placeholders, and a pre-commit hard-gate (`.git/hooks/pre-commit`) enforcing secret/PII scanning ever since.
- **Status:** **settled.** Prevention rules live in `lifeos-security-and-privacy`. Do not weaken the pre-commit gate; a second rewrite would be even costlier now that the repo is public.

### 2. The data/ restructure fallout — STILL LIVE
- **Symptom/Trigger:** Commit `9f4759a` "restructure: flatten data/ → root level (sync from Mac)" (1192 files, ~257k insertions) moved `data/experts/` → `experts/`, `data/knowledge/` → `knowledge/`, etc. It also **overwrote README.md**, restored later from history in `46727db`.
- **Root cause:** A bulk tree move synced from another machine, with no accompanying sweep of code path constants and no dedupe of the old tree. Both layouts now coexist and code disagrees about which is real.
- **Evidence:**
  - `src/core/build_fts_index.py` — all-old layout (`BASE_DIR / "data" / "knowledge"` etc., lines 14–19).
  - `src/core/experts.py` — **mixed**: `root / "experts"` (new, lines 91/148/407) vs `root / "data" / "knowledge|private|inbox"` (old, lines 333–335).
  - `src/core/chat_persistence.py` — new layout (`ROOT / "knowledge" / "chat-insights"`).
  - `scripts/auto_tldr.py` — new layout (`ROOT / "knowledge" / "news"`).
  - `scripts/weekly_hermes_run.py` — **mixed**: `NEWS_DIR = BASE_DIR / "knowledge" / "news"` (fixed in `86ef0ec`) but `data/inbox/content_drafts` and `data/inbox/proposals` (lines 698, 706) still old.
  - Diverged twins: `data/inbox/proposals/` has **39** files vs `inbox/proposals/` **21** files.
  - Test suite: ~8–10 failures attributable to layout split (suite currently 10 failed / 188 passed — do not run it casually).
- **Resolution:** none yet. README restored (`46727db`); the systematic fix is a dedicated campaign.
- **Status:** **still-live** → owned by `lifeos-data-layout-unification-campaign`. Do NOT "fix" individual path constants ad hoc; you will move the split, not close it.

### 3. The M1–M5 RAG scaling campaign (June 2026)
- **Symptom/Trigger:** Need to scale retrieval to 10,000+ documents. A multi-agent orchestration (Project Orchestrator pattern per AGENTS.md) decomposed it into: M1 sqlite-vec install, M2 embeddings integration, M3 chunker/indexing pipeline, M4 hybrid search + RRF, M5 E2E test suite pass.
- **Root cause of the pain:** Coordination overhead and one stubborn test. The orchestrator went through **5 generations** (branches `subagent-Project-Orchestrator[-Gen-2..5]-…`; local dirs `.agents/orchestrator`, `.agents/orchestrator_gen2` — local-only artifacts, gitignored). Workers reached gen5 (`.agents/worker_m1_gen5`, `worker_m2_gen5`, `worker_m2_m4_rag_gen5`), sub-orchestrators to gen4 (`sub_orch_m2_m4_rag_gen4`). The endgame per `.agents/orchestrator/BRIEFING.md` and `progress.md` (iteration 5/32, 2026-06-13) was **one failing test: `test_rrf_math_sorting`** in `tests/test_retrieval_scale.py` — RRF score sort-order math.
- **Evidence:** Commits `ec0b431` (unified sqlite-vec + FTS5 memory core, hybrid RAG, RRF, summary compression), `5e39fa4` (unified memory core), `ae72ef7` (removed redundant threaded re-indexing in `triage_outbox.py` — a dead end: threading gave no benefit and complicated indexing), `f6bc4f0` (docs). `cc229d8` added `.agents/` to .gitignore. Debug fossils: `scratch/debug_rrf.py` (standalone RRF/hybrid_search reproduction harness), `scratch/old_search.py` (the pre-RRF FTS-only search kept for comparison).
- **Resolution:** Campaign converged. `test_rrf_math_sorting` exists at `tests/test_retrieval_scale.py:540` alongside `test_rrf_math_calculation/only_fts/only_knn/identical_ranks`; as of 2026-07-07 `test_retrieval_scale.py` passes fully. The live index is `indexes/lifeos.db` (FTS5 + `vec_docs` + `doc_chunks`, ~50k chunks, ~350 MB).
- **Status:** **settled.** Lessons: (a) 5 orchestrator generations and gen5 workers for one sort-math test means E2E-test acceptance criteria should be verified per-milestone, not at the end; (b) threaded re-indexing was tried and rejected (`ae72ef7`) — don't re-add it; (c) RAG internals now documented in `lifeos-rag-reference`.

### 4. Test-suite indexing hang
- **Symptom/Trigger:** Test runs hung indefinitely.
- **Root cause:** `tests/test_experts.py` (`TestCreateEmptyExpert`) called `create_empty_expert`, which triggered a **real FTS index rebuild** (`src.core.build_fts_index.build_index`) against the actual corpus inside a unit test.
- **Evidence:** `4b9da79` "…fix test indexing hang" — the diff adds `patch("src.core.build_fts_index.build_index")` as an autouse fixture in `tests/test_experts.py`, plus a similar guard in `tests/test_regenerate_summary.py`. Same commit also fixed a `monitor_lenny_rss.py` SSL-context bypass and gitignored Syncthing meta files.
- **Resolution:** Mock index rebuilds in tests.
- **Status:** **settled.** Rule of thumb: any test path touching `build_index` or `indexes/lifeos.db` must be mocked or use `tmp_project`.

### 5. TicNote API integration → manual inbox pivot
- **Symptom/Trigger:** `6e00603` (2026-06-25 20:41) added a TicNote background sync script + API client (`src/integrations/ticnote/client.py`, `scripts/sync_ticnote.py`). **48 minutes later**, `f55c3f1` (21:29) removed the API client and pivoted.
- **Root cause:** Background API sync was the wrong shape for the device workflow; CHANGELOG `[2026-06-25]` frames the replacement as a "robust manual file drop workflow" and calls the removed code "unused API sync code" — the API path never earned its keep.
- **Evidence:** `git show 6e00603` / `git show f55c3f1` (renames `sync_ticnote.py` → `process_ticnote_inbox.py`, deletes `client.py`, `test_ticnote_client.py`, `test_sync_ticnote.py`); CHANGELOG `[2026-06-25]`; dead branch `feat/ticnote-sync`; stash `stash@{1}` ("WIP on main: d787598 feat(ticnote): pivot to manual…") is leftover WIP from this pivot.
- **Resolution:** Manual drops into `data/inbox/ticnote/`, processed by `scripts/process_ticnote_inbox.py` (extract → LLM synthesis → archive raw → rebuild index).
- **Status:** **settled — background API sync is a rejected approach.** Don't rebuild the API client without new evidence the device API is usable.

### 6. The CodeQL dead branch
- **Symptom/Trigger:** `feat/fix-codeql-tests` (also on origin) holds `8f9e73a` (CodeQL URL sanitization, exception-logging alerts, tests) and `90158cd` (push weekly newsletter directly to TinaCMS GitHub repo), plus `stash@{0}` (WIP on that branch).
- **Root cause of death:** The branch predates the `9f4759a` data/ restructure; `git diff main feat/fix-codeql-tests --stat` shows 1206 files / ~259k deletions — it's a different world, unmergeable as-is.
- **Evidence:** `git log --oneline main..feat/fix-codeql-tests`; the diff stat above. The TinaCMS-push idea **re-landed on main** via `86ef0ec` (idempotent `get_contents()` → `update_file()`/`create_file()` push).
- **Resolution:** Superseded. Any still-wanted CodeQL sanitization fixes in `8f9e73a` should be cherry-picked conceptually (re-implemented against main's layout), never merged.
- **Status:** **superseded.** Branch + `stash@{0}` are deletable fossils (owner's call).

### 7. Weekly dispatch quality battles
- **Symptom/Trigger:** Published weekly posts contained template artifacts and a manual-review footer; then the pipeline started finding **0 articles**.
- **Root causes & fixes (all in `86ef0ec`, `scripts/weekly_hermes_run.py`):**
  - **The path bug:** `NEWS_DIR` pointed at `data/knowledge/news` — a casualty of entry 2's restructure — so the article glob matched nothing. Fixed to `knowledge/news`.
  - **Template/footer leaks:** fixed by `strip_artifacts()` (removes template leak + manual review footer); auto-generated frontmatter description; idempotent GitHub push.
  - **Digest-first design:** the dispatch now prefers a weekly digest from `weekly_tldr_process.py` writing to `knowledge/news/digest/`, falling back to raw articles. **Neither the script nor the digest directory has ever existed in git** (`git log --all -- scripts/weekly_tldr_process.py knowledge/news/digest` → empty; the directory is absent on disk). The primary path is aspirational; **the fallback always runs**.
- **Evidence:** `git show 86ef0ec` (full itemized message); Syncthing conflict fossils of dispatch drafts under `data/inbox/content_drafts/` (see entry 11). Note lines 698/706 of the script still use old `data/inbox/...` paths (entry 2).
- **Status:** **partially-fixed; the missing digest producer is a still-live gap.** Either build `weekly_tldr_process.py` or delete the digest-first branch.

### 8. event_tracker in/out — scope discipline
- **Symptom/Trigger:** `be81698` added a local event aggregator (Sydney/Epping); `686c95d` removed it: "moved to separate project".
- **Root cause:** Feature didn't belong in a knowledge platform.
- **Evidence:** the two adjacent commits on main.
- **Resolution/Status:** **settled.** The precedent: extract out-of-scope features promptly instead of letting them accrete.

### 9. litellm CVE bypass — accepted risk
- **Symptom/Trigger:** pip-audit in the pre-commit hook started blocking all commits on new litellm CVEs.
- **Root cause:** No installable fix wheels exist (hook comment: "litellm CVEs: no installable fix wheel exists (>=1.83.10 unavailable)"; aiohttp/python-dotenv CVEs are transitive deps pinned by litellm, unupgradable without resolution conflict).
- **Evidence:** `.git/hooks/pre-commit` carries **16 `--ignore-vuln` pins** (`grep -c "ignore-vuln" .git/hooks/pre-commit`); CHANGELOG `[2026-06-26]` "Bypassed new litellm CVEs in the local pip-audit hook to unblock commits".
- **Status:** **accepted risk — revisit when litellm ships fix wheels.** Don't silently add new pins; each one is a decision.

### 10. Streamlit cache/import battles — a recurring class
- **Symptom/Trigger:** After refactors, the Streamlit UI broke with signature mismatches and import errors even though tests of the underlying code passed.
- **Root cause:** `st.cache_*` memoizes functions by old signatures across reruns, and Streamlit's module reloading pins stale import paths; any refactor of a cached function or a moved module breaks the UI at runtime only.
- **Evidence:** `4b8430a` (cached `fts_search` signature), `53d8c14` (cached `execute_agent_search_loop` signature), `2fc01fa` (chat context import caching), `6138c99` (import path + test unpacking for chat_context), `8e3fc80` (import path in `modals.py` for `read_fm`), `3a2a218` (test/import alignment after `weekly_hermes_run.py` refactor). Related: `85503cc` (force dotenv override on rerun — same "Streamlit holds stale state" family).
- **Resolution:** Each instance fixed individually; the pattern is the lesson.
- **Status:** **settled instances, live pattern.** When refactoring anything reachable from the UI: change the signature of cached functions deliberately, clear caches, and smoke-test the app — unit tests will not catch this.

### 11. Legacy artifacts as fossils (field guide)
Each stale artifact marks a past battle. Don't "clean up" without knowing which:
- `indexes/markusos.db` (May 25, 376 KB) — pre-rename index from the MarkusOS→LifeOS naming transition (`223eae6` era). Superseded by `indexes/lifeos.db`.
- `src/indexes/lifeos.db` (May 28, 24KB) and `src/data/private/` (May 29) — strays from before scripts resolved paths to repo root; created by running code with the wrong cwd.
- `scratch/` one-offs (gitignored): `debug_rrf.py` (entry 3's RRF debugging), `old_search.py` (pre-RRF FTS-only search, kept for comparison), `test_failed_gemini.py` (debugging a failed Gemini summarization call against an inbox file — **contains a hardcoded key-like string; treat as sensitive, do not commit or quote**), `vulnerable_test.py(.bak)` (security-scanner test bait).
- `scripts/update_docs.py.bak` — pre-refactor backup of the changelog/docs updater (`a6dbec3`/`d3c91a4` era).
- Branches: `main-backup` (pre-rewrite safety copy — inferred; verify with `git log main-backup -1`), `demo-public` (public demo snapshot), five `subagent-Project-Orchestrator-*` worktree branches (entry 3), plus the feature branches already merged or superseded (entries 5, 6).
- Syncthing conflict files under `data/inbox/content_drafts/` (`weekly_dispatch_*.sync-conflict-*.md`) — two-machine sync collisions on dispatch drafts; also why `4b9da79` gitignored Syncthing meta files.
- `.agents/**` — entire multi-agent campaign record (entry 3, 12). Local-only, gitignored (`cc229d8`); cite, never commit.

### 12. Self-repairing agent harness — and its self-inflicted noise
- **Symptom/Trigger:** LLM calls in pipelines intermittently returned malformed JSON or timed out, failing whole runs.
- **Root cause:** No retry/repair layer around LLM I/O.
- **Evidence:** `72fa9da` adds `src/core/agent_harness.py` (`execute_with_repair`, UI + background modes) and wires it into `weekly_hermes_run.py` / `chat_context.py`; proposal `data/inbox/proposals/proposal_self_repairing_agent_harness.md`; changelog/source-URL follow-ups `89a6f62`, `a6dbec3`.
- **The live hygiene defect:** repair attempts log to `agent_repair_logs` in the **live** `indexes/lifeos.db`, and tests exercised fixtures against it. As of 2026-07-07 the table holds **367 rows**, of which 240 are `persistently_failing`, 64 `flaky_json_parser`, 18 `flacky_json_parser` (sic), 41 `flaky_timeout` — i.e. ~363 rows are test noise; only 4 (`run_weekly_pipeline`) are real.
- **Status:** harness **settled**; the test-rows-in-live-DB pollution is a **still-live** hygiene defect (tests should point the harness at a tmp DB, and the noise rows should be purged — a write operation, so route via `lifeos-change-control`).

---

## Provenance and maintenance

Re-verification one-liners (all read-only, from repo root):
- Full history / branches / stashes: `git log --oneline --all | head -80`, `git branch -a`, `git stash list`
- Any entry's commit: `git show <hash> --stat` then `git show <hash>`
- Proposals divergence + counts: `ls data/inbox/proposals | wc -l; ls inbox/proposals | wc -l` (39 vs 21 as of 2026-07-07); statuses: `grep -A2 "^## Status" data/inbox/proposals/*.md | grep -cE "Proposed"` etc. (data/: 35 Proposed / 4 ✅ Implemented / 0 ❌ Rejected; inbox/: 18 / 3 / 0)
- Path-split spot check: `grep -n '"data"' src/core/*.py scripts/*.py | grep -v '#'`
- Digest gap: `git log --all --oneline -- scripts/weekly_tldr_process.py knowledge/news/digest` (empty = still a gap); `ls knowledge/news/digest` (absent = fallback still always runs)
- CodeQL branch status: `git log --oneline main..feat/fix-codeql-tests` and `git diff main feat/fix-codeql-tests --stat | tail -1`
- CVE pins: `grep -c "ignore-vuln" .git/hooks/pre-commit` (16 as of 2026-07-07)
- Repair-log noise: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "select function_name,count(*) from agent_repair_logs group by 1 order by 2 desc"`
- RRF endgame test: `grep -n test_rrf_math_sorting tests/test_retrieval_scale.py` (do NOT run the full suite casually; 10 failures are known layout-split casualties, entry 2)

When a still-live entry gets fixed, flip its Status here and in the Index the same day the fix lands.
