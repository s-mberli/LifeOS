---
name: lifeos-security-and-privacy
description: The PII/secrets regime for this public-portfolio repo that lives next to private journals — the leak incident behind it, the pre-commit gate stage by stage, the public/private boundary map (including the current gitignore GAP on root-level dirs), MCP sandbox rules, the VPS sync review protocol, and a leak-response runbook. Load this skill before committing or pushing ANYTHING, when the pre-commit hook blocks, when handling secrets or .env, when touching private data or MCP exposure, when reviewing Syncthing-synced changes, or the moment a leak is suspected.
---

# Security and Privacy

Why this regime is strict: this repo is simultaneously a **public portfolio** (published on GitHub) and the container of the operator's **private life** — journals, chat logs, transcripts, API keys sit in adjacent directories. The costliest failure in project history (owner interview, 2026-07-07) was PII and real-looking secrets reaching the public repo; remediation required a full git-history rewrite.

## The incident (June 2026) — why every rule below exists

Timeline reconstructed from evidence: pre-release audits and scrubs (commits `8980e99`, `832b56d` "prepare for public release", `2c86a96` name removed from LICENSE), SSRF/path-traversal hardening (`fb8902e` — the blocklist lives in src/core/chat_context.py and scripts/update_docs.py), plist/secret scrubbing + first hook (`51ba952`), name-scrub + hook hardening (`0bb27d4`), test-placeholder scrub (`5213801`), and finally the `git filter-repo` history rewrite with `.mailmap` (CHANGELOG 2026-06-26; early history now shows the rewritten author "Developer <developer@example.com>"). Lesson: prevention costs a hook run; remediation cost a history rewrite across every clone.

## When NOT to use this skill

- Process/approval gates in general → `lifeos-change-control` (it summarizes the gate; the depth is here).
- The incident's full chronicle → `lifeos-failure-archaeology`. Hook (re)installation on a fresh clone → `lifeos-build-and-env`.

## The pre-commit gate, stage by stage

Lives at `.git/hooks/pre-commit` — **local-only, NOT version-controlled** (`git ls-files | grep -i hook` is empty). A fresh clone has NO gate; install per `lifeos-build-and-env`. Stages, in order:

| # | Stage | What it scans | On failure |
|---|---|---|---|
| 1 | Hard regex, all staged files | the operator's absolute home-directory path prefix; the operator's bare first name (with an exception for the project brand name); the OpenRouter key prefix; the GitHub personal-access-token prefix; a real ElevenLabs key (placeholder allowed); the private Azure resource name; anything under `.agents/`; agent workspace files (ORIGINAL_REQUEST.md, PROJECT.md, TEST_INFRA.md, TEST_READY.md) | commit blocked; remove the string or unstage the file |
| 2 | pip-audit on requirements.txt | known CVEs, minus 16 pinned `--ignore-vuln` entries (litellm/aiohttp/python-dotenv — no installable fix wheels exist; each ignore is justified in a hook comment, and adding a new one requires the same) | commit blocked until fixed or justified-and-pinned |
| 3 | bandit `-c .bandit.yml -ll` on staged .py | static security analysis (config skips B101 assert-used; excludes tests/ and venvs) | commit blocked |
| 4 | AI Five-Axis reviewer (scripts/ai_code_reviewer.py) on staged .py | LLM review: Correctness/Readability/Architecture/Security/Performance; auto-fixes rewrite the file and get re-staged; `GIT_AUTHOR` env tags authorship (default "Human"); results logged to the `ai_code_provenance` table | flagged files need manual fixes; `SKIP_AI_REVIEW=1` bypass is EMERGENCY-ONLY — afterwards run the reviewer manually and record provenance |

**Why this file paraphrases the guarded literals instead of quoting them:** the hook rejects any staged file containing them — a document that quoted them could never be committed. The same applies to anything you write in this repo.

## Boundary map

**Boundary 1 — local ↔ public GitHub.** Enforced by .gitignore + the hook. Committable: code (src/, scripts/, apps/), docs/, templates/, config *.example* files, this skills library. Never committable: .env*, data/private/, `**/raw/` (transcripts), indexes/*.db (contains indexed private content), logs/, outputs/, scratch/, .agents/, real plists, config/profile.yml and siblings.

**THE GAP (verified 2026-07-08):** .gitignore's protective patterns target `data/...` paths, but the June-21 restructure created root-level twins. Checked with `git check-ignore`: root `private/`, `knowledge/`, `experts/`, `inbox/`, `business/`, `tracking/` are **all NOT ignored** — they show as untracked in `git status`, which means `git add -A` would stage personal journals and daily notes for a public repo. The regex hook only catches specific strings, not journal prose. Until the layout campaign closes this (`lifeos-data-layout-unification-campaign` Phase 3): **never run `git add -A` / `git add .` in this repo; stage files explicitly.**

**Boundary 2 — local ↔ cloud LLM APIs.** privacy.yml (doctrine-only; no code enforcer): nothing from data/private to non-secure external APIs; prefer local/secure models for sensitive data; human approval before publishing to social media or sending emails (verbatim scope — the automated website push sits in an interpretive gap; see the open conflict in `lifeos-portfolio-and-positioning`), and before unusually large paid API calls. Code-level: the MCP `search_vault` hard-forces `include_private=False`; note the include_private filter matches the substring `data/private/` only — root `private/` files would bypass it if they were ever indexed (they currently aren't; the indexer doesn't cover root dirs).

**MCP sandbox** (src/core/mcp_server.py, mapping the README's OWASP claims to real code): query length cap 500 chars; `read_vault_file` resolves paths and rejects anything outside the repo, anything not under `data/`, anything under `data/private/`, `.env`/`.git` names, and binary suffixes; rate limit 60 req/min in-memory; every call and error logged to `data/private/mcp_audit.log`; errors sanitized before return. Memory poisoning: the `user_memory` table is human-managed only — no code path lets an agent write it.

## VPS Sync Review Protocol (AGENTS.md, checklist form)

Syncthing mirrors the data/ tree with a VPS that crawls RSS. Files arriving by sync are UNREVIEWED input:
1. Never assume synced files are safe or leak-free — `git diff` / read them before any commit that includes them.
2. Commit locally so the pre-commit hook scans them; never bypass it for synced content.
3. Functional changes synced from the VPS must be reflected in CHANGELOG/README like any other change.
4. Resolve `*.sync-conflict-*` files promptly (diff, keep the right copy, delete the conflict file).

## Leak-response runbook

1. **STOP.** No pushes, no publishes, from any machine.
2. **Scope it.** What string leaked, where, since when: `git log -S"<the-string>" --oneline --all`; `git diff origin/main..HEAD` for unpushed exposure.
3. **Not yet pushed?** Rewrite local history (amend/rebase) until `git log -S` is clean, then verify the hook catches the class of string going forward (add a pattern if not).
4. **Already pushed?** Rotate every exposed credential FIRST (provider dashboards) — assume it was scraped the moment it went public. Then history rewrite with `git filter-repo` (this project has done it — see `lifeos-failure-archaeology` entry 1), force-push only with explicit owner approval, and verify with a fresh clone + grep.
5. **Post-mortem:** add the incident to `lifeos-failure-archaeology`, add a hook pattern for the leaked class, note the CHANGELOG (Security section).

## Secrets handling rules

- .env is never committed; new vars go into .env.example with obviously-fake placeholders ("your-key" style). Test fixtures use obviously-fake values (the `5213801` lesson: realistic-looking dummy secrets trip scanners and reviewers alike).
- Never echo env values in code, logs, or diagnostics; read key NAMES only. Errors that might embed keys go through `sanitize_err` (src/core/llm_client.py:30-40) which masks provider keys — keep that behavior when touching llm_client.
- **Gitignored ≠ safe** — live example (verified 2026-07-08): `scratch/test_failed_gemini.py` contains hardcoded key-shaped material in the working tree. It can't be committed (scratch/ is ignored) but it sits on disk, syncs to backups, and pastes accidentally. Owner action item: rotate that Gemini key and delete the file. Rule: keys live in .env only, even in throwaway scripts.

## Pre-stage self-check (run before every commit you assemble)

```
git diff --cached --name-only                      # know exactly what you staged
git diff --cached --name-only -z | xargs -0 grep -l "$HOME" 2>/dev/null   # home-dir paths (space-safe; avoids quoting the banned literal)
# key-prefix scan: use the two prefixes listed in hook stage 1 (read them from
# .git/hooks/pre-commit locally — they are deliberately not reproduced here)
git diff --cached --name-only -z | xargs -0 grep -lE "<prefix1>|<prefix2>" 2>/dev/null
git check-ignore -q data/private && echo "data/private ignored OK"
```
Plus: no file from a private tree staged; no personal name in prose (say "the user"/"the operator"); synced files reviewed.

## Provenance and maintenance

- Hook stages: `sed -n '1,40p' .git/hooks/pre-commit` (read locally; never commit it verbatim). Ignore-pin count: `grep -c ignore-vuln .git/hooks/pre-commit` (16 as of 2026-07-08).
- The gitignore GAP: `git check-ignore private knowledge experts tracking; echo "exit=$? (1 means still NOT ignored)"` — this skill must be updated when the layout campaign closes it.
- MCP ACL: `sed -n '95,125p' src/core/mcp_server.py`. SSRF guards: `git show fb8902e --stat`.
- scratch key finding: `ls scratch/test_failed_gemini.py 2>/dev/null && echo "still present — rotate & delete"`.
- Incident commits/mailmap: `git log --oneline | grep -i "scrub\|security"`; CHANGELOG 2026-06-26.
