---
name: lifeos-rag-reference
description: The retrieval/RAG theory pack for this repo — FTS5/BM25, porter stemming, the query fallback ladder, nomic embeddings via OpenRouter, sqlite-vec KNN, chunking, and Reciprocal Rank Fusion, each taught with the actual implementation (file:line) and worked numbers. Load this skill when working on search, retrieval, embeddings, indexing, RRF, or chunking; when search results look wrong or empty; when adding a retrieval feature; or when reasoning about FTS5/sqlite-vec behavior.
---

# RAG Reference (as implemented here)

The retrieval core is a hybrid of keyword search (SQLite FTS5) and semantic search (sqlite-vec KNN over 768-dim embeddings), fused with Reciprocal Rank Fusion. Everything lives in `indexes/lifeos.db` and four modules: src/core/db.py (schema), src/core/build_fts_index.py (indexer), src/core/search_knowledge.py (search + fusion), src/core/llm_client.py (embeddings).

Read-only DB access from a shell requires `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "..."` — plain `mode=ro` fails on this WAL database, and the `vec_docs` table is only queryable from Python with the sqlite-vec extension loaded ("no such module: vec0" in the CLI is expected, not a bug).

## When NOT to use this skill

- An error/empty result needs triage → `lifeos-debugging-playbook` (esp. entries 2-5, 12).
- You want to measure current index state → `lifeos-diagnostics-and-tooling`.
- You're deciding whether a change is allowed → `lifeos-change-control`; design invariants → `lifeos-architecture-contract`.

## 1. FTS5 keyword search

Schema (src/core/db.py:140-147): `CREATE VIRTUAL TABLE search_index USING fts5(path, title, content, tokenize='porter')`.

- **FTS5** = SQLite's full-text engine; you query it with `content MATCH ?`.
- **Porter stemming** reduces words to stems at index AND query time ("architectures" ≈ "architecture" ≈ "architectural"). Consequence: exact-phrase precision is limited; you cannot force an unstemmed match without changing the tokenizer.
- **BM25** = the ranking function; `bm25(search_index)` returns a score where LOWER (more negative) = better. `fts_search` orders by it (search_knowledge.py:55-56). The CLI pretty-printer displays `abs(score)*1000` (search_knowledge.py:412) — don't confuse the display number with raw bm25.
- `snippet(search_index, 2, '**', '**', '...', 64)` returns a highlighted excerpt of column 2 (content).

## 2. The query fallback ladder

Both `fts_search` (:48-84) and `hybrid_search` (:150-202) degrade gracefully rather than erroring:

1. Raw query as MATCH (may throw `sqlite3.OperationalError` on characters like `'` or `-` — caught silently).
2. Tokenized AND query: lowercase word tokens, minus STOPWORDS (module constant, ~170 words, :13-30), minus digit-only tokens, minus single-char tokens. The code comment at :152-154 records why: digit tokens (e.g. from `1'='1`) made the AND query fail and the OR query over-match.
3. OR query over the same tokens.
4. Phrase MATCH of the original string (hybrid only).
5. `LIKE %token%` scan (hybrid only, :190-202) — slow, last resort.

There is also an injection-pattern guard (:141-143) returning `[]` for inputs like `' OR ` — parameterized queries already prevent real injection; the guard prevents garbage OR-broadened matches. Failure mode to remember: every ladder step swallows `OperationalError`, so a syntactically cursed query returns few/none results with NO error anywhere.

## 3. Embeddings

`get_embeddings` (llm_client.py:286-341): POSTs to OpenRouter `/embeddings` with model hard-coded `nomic-ai/nomic-embed-text-v1.5`, 768 dimensions, batch_size 500, inputs truncated to 8000 chars, raises on 429 ("Rate limit exceeded"). Shape quirk: a `str` input returns one vector; a `list` returns a list of vectors — callers must handle both (hybrid_search does, :217-218).

**The zero-vector trap (critical):**
- `hybrid_search` wraps the query embedding in try/except and on ANY failure substitutes `[0.0]*768` (:219-220). KNN then still "works" but distances are meaningless — semantic ranking silently degrades to noise while FTS carries the result. Detect it: no embedding-related log line + results identical to FTS-only.
- The indexer does the same per chunk (build_fts_index.py:206-209): failed chunk embeddings are stored as zero vectors permanently, invisible to KNN forever (cosine guard returns 0.0 for zero norms, search_knowledge.py:108-115).
- Also every test run: conftest.py autouse-mocks `get_embeddings` to zero vectors.

## 4. sqlite-vec

Schema (db.py:129-137): `CREATE VIRTUAL TABLE vec_docs USING vec0(chunk_id INTEGER PRIMARY KEY, embedding float[768])`.

- KNN query syntax: `SELECT chunk_id, distance FROM vec_docs WHERE embedding MATCH ? AND k = ?` (search_knowledge.py:239-243), with the query vector packed as little-endian float32 blob: `struct.pack("768f", *vec)` → 3072 bytes (the fallback reader checks `len(emb_blob) == 3072`, :263).
- Extension loading happens per-connection in db.py:42-49 via `sqlite_vec.load(conn)`; if the Python build lacks `enable_load_extension`, it logs "sqlite-vec not available, vector search disabled" and continues.
- Without the extension, hybrid_search falls back to a pure-Python cosine scan over ALL vec rows (:254-299) — O(n) over 50k rows; correct but slow. That fallback is why results can differ subtly between machines.

## 5. Chunking and indexing

Actual chunking at index time is `chunk_markdown(text, chunk_size=1000, overlap=200)` in build_fts_index.py:102-120 — NOT `llm_client.split_text` (12000/1000), which is used for LLM summarization contexts elsewhere. Each chunk becomes one row in each of doc_chunks (path, title, chunk_index, content, wiki_links JSON), vec_docs (keyed by the doc_chunks rowid), and search_index. Invariant: the three tables have equal row counts (50,671 each as of 2026-07-08).

`index_file` (build_fts_index.py:156-249) is idempotent per file: it DELETEs the file's old rows then re-inserts, re-embedding that file's chunks only. `build_index()` (:37-100) however **drops all three tables and re-embeds EVERYTHING** in DIRECTORIES_TO_INDEX — a full rebuild costs ~50k chunks × ~250 tokens of embedding API usage. Never trigger it casually (owner cost rule); prefer per-file `index_file`.

Two warts, verified: `index_file` has a signature-overloading shim accepting both (path, conn) and (db_path, path) (:164-179); and its lock-retry references `sqlite3.OperationalError` (:240) while the module never imports sqlite3 — a latent NameError, tracked in the layout campaign.

DIRECTORIES_TO_INDEX (:13-21) covers only `data/*` + `outputs/` — root-level `knowledge/` (739 files) is invisible to search as of 2026-07-08. That's the layout half-migration; see `lifeos-data-layout-unification-campaign`.

## 6. Reciprocal Rank Fusion (RRF)

Implementation (search_knowledge.py:301-313): each result list (FTS ranked by bm25, KNN ranked by distance) contributes `1/(60 + rank)` per document key `(path, content)`; scores sum across lists; sort by score descending, tie-break ascending by path (:313).

k=60 is the standard damping constant from the IR literature — it keeps a rank-1 appearance from dominating everything while still rewarding agreement between the two lists.

Worked example (compute it yourself to the 5th decimal; this is the exact arithmetic the code does):

| doc | FTS rank | KNN rank | score |
|---|---|---|---|
| A | 1 | 3 | 1/61 + 1/63 = 0.016393 + 0.015873 = **0.032266** |
| B | 2 | 1 | 1/62 + 1/61 = 0.016129 + 0.016393 = **0.032522** |
| C | — | 2 | 1/62 = **0.016129** |
| D | 3 | — | 1/63 = **0.015873** |

Final order: B, A, C, D. Note B beats A despite A's FTS-rank-1: two good ranks beat one great one — that's RRF's point.

History: getting this sort exactly right was the endgame of the June-2026 multi-agent RAG scaling campaign; the canonical spec is the test `test_rrf_math_sorting` (tests/test_retrieval_scale.py:540) — read it before touching the fusion code, and treat it as the contract.

## 7. Retrieval scoping

- `allowed_paths` (fts_search param): the ask-expert flow builds a set of paths from an expert's `sources/*-ref.md` files and filters hits to it — that's how expert answers stay grounded in curated evidence only.
- `include_private=False` filters hits whose path contains the substring `"data/private/"` (fts_search :89, hybrid :204-205, :250). Honest caveat: a file indexed under root `private/...` would NOT match that substring and would leak past the filter — currently moot only because the indexer doesn't cover root dirs at all. The layout campaign must keep filter and layout consistent.
- `require_insight_note=True` restricts to paths under data/knowledge/ or data/private/ (:90).
- The MCP server (`search_vault`) hard-forces `include_private=False` for external agents.

## 8. Scale facts (as of 2026-07-08, drift daily)

50,671 rows in each chunk table; DB ~350 MB; 1,501 distinct indexed documents; indexed prefixes: `data/` and `outputs/` only. Certified scale properties live in tests/test_retrieval_scale.py (E2E hybrid retrieval, RRF math, scale behavior — passing) and tests/stress_test_sqlite_vec.py (not collected by default `pytest tests/` since its name doesn't match `test_*.py`).

## 9. Context assembly (short — details live in the code)

`synthesize_briefing` (search_knowledge.py:335-396): stuffs results into a 16,000-char context, calls the LLM, then appends any citation paths the model omitted. Wart: it temporarily swaps models by mutating `os.environ` (OPENROUTER_MODEL → "openrouter/owl-alpha", etc.) — a cost hack flagged in `lifeos-architecture-contract`. Chat context building and the agent search loop (with a fetch_web tool, added in commit f4259ee) live in src/core/chat_context.py.

## Glossary

| Term | Meaning here |
|---|---|
| FTS5 | SQLite full-text search engine (virtual table `search_index`) |
| BM25 | keyword relevance score; lower/more negative = better |
| porter | stemming tokenizer (word → stem at index and query time) |
| embedding | 768-dim float vector of a text chunk (nomic-embed-text-v1.5) |
| vec0 / sqlite-vec | SQLite extension + virtual table for vector KNN |
| KNN | k-nearest-neighbors by vector distance |
| chunk | ~1000-char slice of a note (200 overlap); unit of indexing |
| RRF | Reciprocal Rank Fusion: score = Σ 1/(60+rank) across result lists |
| cosine | similarity fallback when vec0 is unavailable |

## Provenance and maintenance

- Row counts / prefixes: `.venv/bin/python .claude/skills/lifeos-diagnostics-and-tooling/scripts/db_stats.py` and `index_coverage.py`.
- k=60 and tie-break: `grep -n "60.0\|x\[0\]\[0\]" src/core/search_knowledge.py`.
- Chunk size: `grep -n "chunk_size" src/core/build_fts_index.py` (1000/200 as of 2026-07-08).
- Embedding model/dims: `grep -n "nomic\|768" src/core/llm_client.py src/core/db.py`.
- Full-rebuild cost driver: `grep -n "DROP TABLE\|get_embeddings" src/core/build_fts_index.py`.
- RRF contract test: `grep -n "def test_rrf_math_sorting" tests/test_retrieval_scale.py`.
