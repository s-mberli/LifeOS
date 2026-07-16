---
name: lifeos-validation-and-qa
description: LifeOS testing and evidence discipline. Load BEFORE running any tests, when writing new tests, when judging whether TEST OUTPUT actually proves a change (for the general evidence bar and experiment design, use lifeos-research-and-proof-methodology), when interpreting test failures (especially the 10 known-red tests), and before claiming any change is "done". Covers safe pytest recipes, the live-DB pollution trap in test_agent_harness.py, conftest fixtures, mocking rules, the red-count baseline, manual eval questions, and CI status.
---

# LifeOS Validation & QA

Ground truth as of **2026-07-07**. Baseline: **198 tests collected, 188 passed, 10 failed, ~315s** for a full run — but see the DB-pollution trap before you ever consider a full run.

## When NOT to use this skill

- Diagnosing a runtime bug in the app itself → `lifeos-debugging-playbook`.
- Deciding whether a change is allowed at all → `lifeos-change-control`.
- Fixing the data/ vs root layout mismatch that causes most red tests → `lifeos-data-layout-unification-campaign` (owns those failures; do not "fix" them piecemeal).
- General research/proof standards beyond tests → `lifeos-research-and-proof-methodology`.

## 1. Evidence standards

Acceptable evidence for "it works":

| Evidence | Example |
|---|---|
| Exact pytest node id + pass/fail output | `tests/test_frontmatter.py::test_write_fm PASSED` |
| Before/after counts from **read-only** SQL | `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' 'SELECT COUNT(*) FROM agent_repair_logs'` (plain `mode=ro` fails on this WAL DB) |
| Artifact diffs | diff of a generated Markdown note before/after |

NOT acceptable: "looks right", eyeballing the Streamlit app, an LLM saying it's fine, or "the code should do X".

Hard rule: **a change must not increase the red count.** Baseline is 10 failed / 188 passed (2026-07-07). State the delta vs baseline in every PR. Full evidence bar: `lifeos-research-and-proof-methodology`.

## 2. Suite anatomy — the 10 known-red tests

All verified by reading test + source on 2026-07-07:

| Test node | Cause | Owner |
|---|---|---|
| `tests/test_chat_persistence.py::test_append_to_daily_chat_log` | Test patches `ROOT` to tmp and asserts `data/private/chat-logs/...`; `src/core/chat_persistence.py:40` writes `ROOT / "private" / "chat-logs"` (root layout). Writes land in tmp, just the wrong subdir — no live pollution. | layout campaign |
| `tests/test_chat_persistence.py::test_save_message_as_insight` | Same data/ vs root layout mismatch. | layout campaign |
| `tests/test_debug.py::test_debug_imports` | Debug scaffold ending in literal `assert False` — **permanently red by construction**. Deletion candidate via change control. | change control |
| `tests/test_experts.py` — 4 failures in `TestGetExistingExperts` / `TestCreateEmptyExpert` | Tests build tmp `data/experts/`; `src/core/experts.py:91` reads `root / "experts"` (root layout). | layout campaign |
| `tests/test_experts_tts.py::test_core_get_existing_experts_with_voice_id` | Same `experts.py:91` root-layout read (verified: same `get_existing_experts`). | layout campaign |
| `tests/test_ui.py::test_ui_chat_input_flow`, `::test_ui_chat_save_insight_flow` | `RuntimeError` from Streamlit `AppTest.from_file(...).run()`. Tests correctly patch `ROOT`/`DB_PATH` to tmp; failure is in the AppTest harness/environment, not data pollution. Root cause not fully diagnosed — treat as "AppTest environment incompatibility" until characterized. | unassigned |

Do not "fix" layout failures locally — they are owned by `lifeos-data-layout-unification-campaign`. A green suite is that campaign's exit gate.

## 3. THE DB-POLLUTION TRAP (read before any suite run)

`tests/test_agent_harness.py` exercises `src/core/agent_harness.py`. The decorator `execute_with_repair` calls `log_repair_attempt(...)` **without passing `db_path`**, so it uses the module default:

```python
DB_PATH = BASE_DIR / "indexes" / "lifeos.db"   # the LIVE database
def log_repair_attempt(..., db_path: Path = DB_PATH) -> None:
```

The tests define throwaway functions (`flaky_json_parser`, `persistently_failing`, `flaky_timeout`) and let the decorator log their failures — **into the live `indexes/lifeos.db`**. Every full-suite run adds rows to `agent_repair_logs`. As of 2026-07-07 that table has 367 rows; ~363 are test pollution: `persistently_failing` 240, `flaky_json_parser` 64, `flacky_json_parser` 18 (typo variant from an older test revision — the typo exists in the data, not current code), `flaky_timeout` 41.

Rules:
- **Never run the full suite as a casual probe.** Run individual files.
- Any test touching a DB must point at a `tmp_path` DB. The good pattern, from `tests/test_db_sqlite_vec.py`:

```python
def test_get_db_connection_success(tmp_path):
    db_path = tmp_path / "test.db"
    conn = get_db_connection(db_path)
```

and from `tests/test_outbox.py` (patching a module-level default):

```python
db_path = tmp_project / "indexes" / "lifeos.db"
with ..., patch("src.core.build_fts_index.DB_PATH", db_path):
```

## 4. Safe-run recipes

```bash
# One file (verified 2026-07-07: 7 passed, ~0.5s, tmp_path-only)
.venv/bin/pytest tests/test_frontmatter.py -q

# One node
.venv/bin/pytest "tests/test_experts.py::TestGetExistingExperts::test_finds_expert_directories" -q

# Curated safe smoke set — fast, DB-free, network-mocked, currently green
# (verified by reading + running: 17 passed in 0.56s)
.venv/bin/pytest tests/test_frontmatter.py tests/test_youtube.py tests/test_url_title_extraction.py -q
```

- Slowest file: `tests/test_retrieval_scale.py` dominates the ~315s full run — never run it casually.
- Never run `tests/test_agent_harness.py` (live-DB pollution, section 3).
- `pytest.ini` defaults: `testpaths = tests`, `python_files = test_*.py`, `addopts = -v --tb=short`. So bare `pytest` == full suite == forbidden casual probe.

## 5. Mocking discipline (conftest.py fixtures)

`tests/conftest.py` provides:

- **`tmp_project`** — builds the OLD `data/*` layout, which is the known mismatch with post-June-21 root-layout code:

  ```python
  (tmp_path / "data" / "knowledge").mkdir(parents=True)
  (tmp_path / "data" / "experts").mkdir(parents=True)
  (tmp_path / "data" / "inbox" / "raw").mkdir(parents=True)
  (tmp_path / "indexes").mkdir()
  ```

- **`sample_insight`** — a valid frontmatter note under `tmp_project/data/knowledge/`.
- **`mock_embeddings`** — `autouse=True`; patches `get_embeddings` to a 768-dim zero vector in three modules:

  ```python
  with patch("src.core.llm_client.get_embeddings", return_value=_zero), \
       patch("src.core.build_fts_index.get_embeddings", return_value=_zero, create=True), \
       patch("src.core.search_knowledge.get_embeddings", return_value=_zero, create=True):
  ```

  Precedence note (from its own docstring): a test needing specific embedding values applies its own `patch(...)` inside the test body, which takes precedence over this autouse fixture.

External network/LLM calls **must** be mocked (AGENTS.md: "Mock external network/LLM calls"). Canonical examples:
- `tests/test_llm_client.py`: `patch("llm_client.try_providers", return_value=_FAKE_RESULT)` and stacking `patch("llm_client.call_azure", return_value=None)` etc.
- `tests/test_url_title_extraction.py`: `with patch("requests.get", return_value=mock_response):` for raw HTTP.

## 6. Checklist: adding a test

- [ ] File named `test_*.py` under `tests/` (else pytest won't collect it — see stress_test note below).
- [ ] All filesystem work via `tmp_path` / `tmp_project`.
- [ ] **Never the live DB** — tmp DB path or `patch(..., "DB_PATH", tmp_db)` (section 3 patterns).
- [ ] All network/LLM calls mocked.
- [ ] Run the single file: `.venv/bin/pytest tests/test_yourfile.py -q` — show node ids + result as evidence.
- [ ] Red count must not grow vs baseline (10).
- [ ] Change control applies (`lifeos-change-control`).

## 7. Test-file inventory (as of 2026-07-07)

| File | Purpose | Status |
|---|---|---|
| test_agent_harness.py | execute_with_repair retry/escalation | green but **pollutes live DB — do not run** |
| test_ai_reviewer.py | AI code reviewer script | green |
| test_api.py | FastAPI ingestion API (TestClient, mocked) | green |
| test_auto_tldr.py | TLDR newsletter HTML article extraction | green |
| test_bulk_ingestion.py | ingest.py process_directory | green |
| test_chat_persistence.py | chat log + insight persistence | **red x2** (layout) |
| test_chat_ui_helpers.py | chat UI helper functions | green |
| test_db_sqlite_vec.py | DB connection/init, sqlite-vec fallback | green (model tmp-DB citizen) |
| test_debug.py | debug scaffold | **red-by-scaffold** (`assert False`) |
| test_eval_chat.py | chat evaluation helpers | green |
| test_experts.py | expert slug/profile utilities | **red x4** (layout) |
| test_experts_tts.py | voice_id from expert profiles | **red x1** (layout) |
| test_frontmatter.py | YAML frontmatter read/write | green (smoke set) |
| test_integration.py | E2E ingestion→index→search | green |
| test_llm_client.py | LLM provider fallback chain (mocked) | green (model mocking citizen) |
| test_mcp_server.py | MCP vault search/read tools | green |
| test_outbox.py | outbox/triage DB flow (tmp DB) | green (model tmp-DB citizen) |
| test_persona_chris.py / test_persona_dan.py | persona-based agent behavior | green |
| test_process_ticnote_inbox.py | TicNote inbox processing | green |
| test_regenerate_summary.py | insight summary regeneration | green |
| test_retrieval_scale.py | retrieval at scale | green but **slow — dominates run time** |
| test_tts.py | ElevenLabs TTS unit tests | green |
| test_ui.py | Streamlit AppTest UI flows | **red x2** (AppTest RuntimeError) |
| test_ui_helpers_memory.py | manual memory helpers | green |
| test_url_title_extraction.py | Jina reader title/content parsing | green (smoke set) |
| test_youtube.py | YouTube URL/id parsing | green (smoke set) |
| stress_test_sqlite_vec.py | sqlite-vec stress script | **not collected** by `pytest tests/` (filename fails `test_*.py` pattern); IS collected when named explicitly (`pytest tests/stress_test_sqlite_vec.py` collects 1 test — verified via `--collect-only`). Don't run: stress workload. |

"Green" statuses above are inferred from the 2026-07-07 baseline (10 known-red enumerated); only the smoke set was individually re-run.

## 8. Manual eval layer (`docs/evals.md`)

Automated tests don't cover UX fidelity. `docs/evals.md` defines the acceptance layer — 8 questions, checked manually in the Streamlit UI:

1. **Source Fidelity** — expert answers cite local source notes with Markdown links.
2. **Context Anchoring** — with no covering sources, the expert declines rather than hallucinates.
3. **Playbook Style Alignment** — tone/formatting match `profile.md` and `playbook.md`.
4. **Metadata Schema Integrity** — new insight notes carry all required frontmatter fields.
5. **Separation of Raw Data** — raw transcripts stay in the private raw folder, not the note.
6. **Strict Retrieval Scope** — "Specific Expert" scope limits FTS to that expert's `-ref.md` sources.
7. **Suggestive Categorization** — unattached-insight scan suggests correct expert slugs.
8. **Update Synthesis Accuracy** — update-expert captures new frameworks without degrading the playbook.

Plus two manual loop recipes: **Ingestion & Search Flow Test** (paste YouTube URL → verify note + transcript separation → rebuild index → keyword search finds it) and **Expert Association & QA Test** (attach note to expert → verify `-ref.md` link → scoped chat cites it; unrelated query is flagged as out-of-scope).

## 9. CI reality

`.github/workflows/tests.yml`: on push/PR, ubuntu-latest, Python 3.11, `pip install -r requirements.txt`, then plain `pytest tests/` — i.e. the full suite, so **CI is currently RED** (the 10 known-red tests). Open caveat: CI lacks the local `data/` tree and `.env` (both gitignored), so failure sets/behavior may differ from local runs — do not assume CI red == local red without comparing output.

## 10. Baseline discipline

- Recorded baseline: **10 failed / 188 passed** (2026-07-07).
- Every PR states its delta vs this baseline; increases are rejected.
- A fully green suite is the exit gate for `lifeos-data-layout-unification-campaign`.
- If the baseline legitimately changes (e.g. `test_debug.py` deleted via change control), update this file's counts and date.

## Provenance and maintenance

Derived 2026-07-07 by reading conftest.py, pytest.ini, the workflow file, docs/evals.md, and each cited test + source file; smoke set verified by actually running it (17 passed, 0.56s). To re-derive the red list **without a full run**: run each known-red file individually, EXCEPT never run test_agent_harness.py or test_retrieval_scale.py —

```bash
.venv/bin/pytest tests/test_chat_persistence.py tests/test_debug.py \
  tests/test_experts.py tests/test_experts_tts.py tests/test_ui.py -q
```

(All five are tmp_path-based; the chat/experts failures write only to tmp.) Re-check DB pollution counts read-only: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT function_name, COUNT(*) FROM agent_repair_logs GROUP BY 1"`. Update section 2's cause table if source line numbers (`chat_persistence.py:40`, `experts.py:91`) move.
