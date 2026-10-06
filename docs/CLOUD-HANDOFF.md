# LifeOS cloud continuation

This guide is the safe starting point for a fresh clone. It describes the checked-in application only. Private notes, expert content, inboxes, indexes, generated drafts, credentials, deployment records, and server backups are intentionally absent.

## Product path and boundaries

LifeOS captures a source, writes a Markdown note, indexes it for retrieval, and supports cited expert chat. Application code lives in `src/`, `scripts/`, and `apps/`; user content belongs under `data/` and is mostly ignored by Git.

Do not infer deployment state from this repository. A separate agent installation, website, scheduler, or messaging service may run different code and needs its own current evidence. Keep provider secrets in an untracked `.env`. Tests must mock network and LLM calls.

The current checkout includes these reviewable boundaries:

- The clipper accepts public HTTP(S) targets, pins validated addresses during text fetches, validates redirects, and caps response size.
- MCP reads are limited to text and Markdown under `data/knowledge/` and `data/experts/`; private, inbox, raw, hidden, oversized, traversal, and symlink escape paths are rejected.
- Dispatch generation writes a local draft and source record. Website publishing is a separate command for an existing reviewed draft whose source digest still matches and is recent.
- `LIFEOS_FTS_ONLY=1` skips embedding writes during indexing. Do not run a full index rebuild against a private database as a routine verification step.

## Local verification

Create an isolated virtual environment and install `requirements.txt`. Run focused tests first:

```bash
python -m pytest \
  tests/test_api.py \
  tests/test_web_url_safety.py \
  tests/test_mcp_server.py \
  tests/test_monthly_dispatch_publishing.py \
  tests/test_monthly_proposal_paths.py \
  tests/test_llm_client_env.py \
  tests/test_weekly_tldr_process.py -q
```

Then run the broader mocked suite without the known live-database-polluting harness:

```bash
python -m pytest tests -q --ignore=tests/test_agent_harness.py
python -m compileall -q src scripts tests
git diff --check
```

On Windows, if pytest cannot use the account temp directory, add `-p no:cacheprovider --basetemp <new-empty-directory>` to the pytest command. Use a new throwaway directory for each run.

Verified locally on 6 October 2026 with Python 3.12: the committable suite passed 263 tests with 7 skipped after excluding `tests/test_agent_harness.py`, which is known to write to the live default database. Python 3.11 CI, a real provider call, browser extension acceptance, deployed MCP integration, and website publication were not exercised by that result.

## Safe continuation order

1. Read `AGENTS.md`, this guide, and the relevant source and tests.
2. Inspect `git status` before staging. Stage explicit code, tests, and public documentation paths only; never use a broad add command in a checkout beside private data.
3. Keep external calls mocked during verification. Generating a dispatch, rebuilding embeddings, publishing a draft, or changing a schedule is a separate authorized action.
4. Report the exact tests run and preserve the distinction between local code, CI, and any deployed system.

Known follow-up work is to confirm the full suite on Python 3.11 CI and separately test real integrations in their own approved environments.
