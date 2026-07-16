---
name: lifeos-change-control
description: Load this BEFORE making ANY change to this repo (LifeOS/MarkusOS) — code, docs, config, data-layer markdown, or skills. Also load when: you are about to commit or the pre-commit hook just blocked you; the user says "implement this proposal" or references a file in data/inbox/proposals/ or inbox/proposals/; you are deciding whether an action (merge, push, publish, paid API burst, overwriting user markdown) needs explicit human approval; you are reviewing files synced from the VPS via Syncthing; or you are tempted to bypass a gate (SKIP_AI_REVIEW, --no-verify). This is the definitive runbook for how changes are classified, gated, reviewed, and merged, plus the incident history behind each non-negotiable rule.
---

# LifeOS Change Control

The runbook for changing this repo safely. Every rule here is enforced by a hook, mandated by `AGENTS.md`, or paid for by a past incident. Verified against the repo as of 2026-07-07.

Jargon, defined once:
- **Hermes** — the autonomous weekly agent pipeline (`scripts/weekly_hermes_run.py`) that proposes changes as PRs and publishes a weekly dispatch.
- **Proposal** — a markdown file under `data/inbox/proposals/` (a diverged copy also exists at `inbox/proposals/` — see the data-layout note below) describing a candidate feature. Has a `## Status` field.
- **Five-Axis Review** — Correctness, Readability, Architecture, Security, Performance; performed by `scripts/ai_code_reviewer.py`.
- **User-layer markdown** — knowledge/expert/private notes (the data layer), as opposed to code.

## 1. Change classification — what am I touching?

| Class | Examples | Gates that apply |
|---|---|---|
| **Code** | `src/`, `scripts/`, `apps/`, `tests/` | Branch discipline → tests → AI Five-Axis review → full pre-commit hook (regex, pip-audit, bandit, AI reviewer) → user approval to merge/push |
| **Docs** | `README.md`, `CHANGELOG.md`, `docs/` | Branch discipline → pre-commit regex/PII scan → user approval to merge/push. Must not contradict `AGENTS.md` or `docs/architecture-principles.md` |
| **Config** | `requirements.txt`, `.env.example`, `privacy.yml`, `.bandit.yml`, workflows | Same as docs, plus pip-audit re-runs on `requirements.txt`. Real secrets NEVER enter git (see §5.2) |
| **Data layer** | `knowledge/`, `experts/`, `data/knowledge/`, `data/experts/`, `data/private/` | Mostly `.gitignore`d (architecture principle 3). Never silently overwrite user-layer markdown — append or propose (`privacy.yml`). VPS-synced: apply §7 before committing anything from here |
| **Skills** | `skills/`, `.claude/skills/` | Pre-commit regex/PII scan (skill files are staged files like any other) → user approval to merge/push |

Never stage anything from `.agents/` or agent workspace files (`ORIGINAL_REQUEST.md`, `PROJECT.md`, `TEST_INFRA.md`, `TEST_READY.md`) — the hook hard-rejects them (`.git/hooks/pre-commit` checks 7).

Data-layout caveat (as of 2026-07-07): a half-finished June-21 restructure (commit `9f4759a`) left BOTH `data/*` and root-level trees (`knowledge/`, `inbox/`, `experts/`, ...) in existence, diverged. Do not "fix" this opportunistically — it is the flagship campaign; see **lifeos-data-layout-unification-campaign**.

## 2. Hermes Proposal Implementation Workflow

**Trigger:** the user says "implement this proposal" or references a file in `data/inbox/proposals/` (or `inbox/proposals/`). Then this workflow is mandatory — no skipping steps (`AGENTS.md`, "Hermes Proposal Implementation Workflow").

**Step 0 — skills caveat.** `AGENTS.md` says to activate `/caveman`, `/spec-driven-development`, and `/code-review-and-quality`. **These skills do not exist as installed skills anywhere in the repo** — not in `skills/`, not in `.agents/skills/` (which contains only `ponytail`), not in `.claude/skills/`. Stray copies exist only inside untracked `.agents/worker_*/` workspaces, which must never be staged. Do not fail hunting for them; follow their intent instead:
- caveman → ultra-compressed communication, minimal token usage.
- spec-driven-development → write and get approval on a spec before code.
- code-review-and-quality → run the Five-Axis review (Step 4 does this via the hook anyway).

Checklist:

1. **Branch** — `git checkout -b feat/<proposal-slug>`. NEVER work on `main`. (Convention verified: existing branches include `feat/ai-code-reviewer`, `feat/ticnote-sync`, `feat/vps-sync-review-rules`.)
2. **Spec & plan** — read the proposal file; write a spec (Objective, Commands, Structure, Boundaries, Success Criteria); **present the plan to the user for approval before writing any code**.
3. **Implement** — incrementally, one task at a time; unit tests in `tests/` with mocked network/LLM calls. `AGENTS.md` says run `.venv/bin/pytest` after each change — but as of 2026-07-07 the full suite is 10 failed / 188 passed, ~315 s, and **writes to the live DB**. Run only the targeted tests for your change against a temp DB copy (see §6.1). This is an **owner-approved deviation from AGENTS.md** (interview 2026-07-07), standing until the layout campaign lands and AGENTS.md's testing section is amended through this very workflow; the failing-suite situation is owned by **lifeos-data-layout-unification-campaign** and **lifeos-validation-and-qa**.
4. **Code review** — `.venv/bin/python scripts/ai_code_reviewer.py "<Author>" <files...>` on modified `.py` files (Five-Axis; auto-fixes applied, manual fixes flagged). Committing triggers it via the hook regardless.
5. **Document** — `scripts/update_docs.py` appends to `CHANGELOG.md`, updates `README.md`, generates a Mermaid diagram. It mutates docs — run it deliberately and review its output.
6. **Merge — approval gate** — commit on the branch, present a summary, **WAIT for explicit user approval before merging to `main`. NEVER push to GitHub without explicit user approval.**
7. **Proposal status** — after merge, update the proposal's `## Status`: `Proposed` → `✅ Implemented` (or `❌ Rejected` with reason).

## 3. Branch discipline

- Never commit on `main`. If you find yourself there with changes: `git switch -c feat/<slug>` first.
- Naming: `feat/<slug>` for features/fixes (verified from `git branch -a`).
- Merging to `main` and pushing to any remote each require explicit user approval — separately (`AGENTS.md` Step 6).

## 4. The pre-commit gate (`.git/hooks/pre-commit`)

Four stages, in order; any failure aborts the commit:

| # | Stage | What it does | Fails on |
|---|---|---|---|
| 1 | Hard regex scan (all staged files) | Instant grep-based PII/secret scan | (a) the operator's absolute home-directory path prefix; (b) the operator's bare first name (the "MarkusOS" brand is allowed); (c) OpenRouter/OpenAI key prefix (`.env.example` exempt); (d) GitHub personal-access-token prefix (`.env.example` exempt); (e) a real ElevenLabs key assignment (placeholder value allowed); (f) the private Azure resource name; (g) any staged path under `.agents/`; (h) agent workspace files `ORIGINAL_REQUEST.md`, `PROJECT.md`, `TEST_INFRA.md`, `TEST_READY.md` at repo root |
| 2 | `pip-audit -r requirements.txt` | Dependency CVE audit | Any vuln not in the ignore list. 16 CVEs are pinned `--ignore-vuln` (litellm: no installable fix wheel exists; aiohttp/python-dotenv: transitive deps pinned by litellm, upgrade causes resolution conflict). **Policy: adding a new ignore requires documenting why in the hook's comment block** |
| 3 | `bandit -c .bandit.yml -ll -q <staged .py>` | SAST on staged Python | Medium+ severity findings |
| 4 | AI Five-Axis reviewer (`scripts/ai_code_reviewer.py`) on staged `.py` | LLM review; **auto-fixes files and re-stages them** (`git add`) so fixes land in your commit; logs to the `ai_code_provenance` table in `indexes/lifeos.db` | Issues needing manual fixes — fix and re-run `git commit` |

Notes:
- `GIT_AUTHOR` env var sets reviewer authorship (defaults to `Human`): `GIT_AUTHOR=Hermes git commit ...`
- `SKIP_AI_REVIEW=1` bypasses stage 4 only. **Emergency use only.** After using it: run the reviewer manually on the affected files (Step 4 command above) so a provenance record exists, and note the bypass in the commit/PR description.
- Because stage 4 rewrites files, diff your working tree after a commit attempt — the file you committed may differ from what you wrote.
- Do NOT paste the guarded literals from stage 1 into any file (including docs about the hook) — the hook will reject your commit. Paraphrase, as this file does.

**Known gap: the hook is NOT version-controlled.** `git ls-files | grep -i hook` returns nothing and there is no copy in `scripts/`. It lives only in the local `.git/hooks/pre-commit`. A fresh clone has **no security gate at all**. If you're on a fresh clone, install/verify the hook first — see **lifeos-build-and-env**.

## 5. Non-negotiables (`AGENTS.md` "Safety & Invariant Rules")

1. **No programmatic patching of Python** via `.replace()`/regex-in-scripts.
   RATIONALE: string surgery on source produces syntax errors and fragile builds; use git tools or real edits.
   EVIDENCE: codified as rule #1 in `AGENTS.md`; the AI reviewer rewrites whole files rather than patching for the same reason.
2. **Never commit `.env`, keys, or private data** (`data/private/`).
   RATIONALE: this repo is published publicly as a portfolio.
   INCIDENT: a PII/secrets leak forced a **full git-history rewrite** with `git filter-repo` + `.mailmap` across 2026-06-12..26 — commits `51ba952`, `0bb27d4` (scrub personal-name references, untrack mailmap), `5213801` (scrub author PII, replace hardcoded secret placeholders in tests), and CHANGELOG entry 2026-06-26 ("Git History Scrubbing"). The costliest failure in project history per the owner. The pre-commit hook's stage 1 exists because of this. Full details: **lifeos-security-and-privacy** and **lifeos-failure-archaeology**.
3. **Always `pathlib.Path`**, never string path joins; locate directories relative to repo root.
   RATIONALE: the code runs on Mac + VPS with different homes; hardcoded string paths are also exactly what the hook's path scan rejects.
4. **Always the `src/core/frontmatter.py` API** for YAML frontmatter — never hand-rolled `---` splitting.
   RATIONALE: thousands of data-layer notes depend on consistent frontmatter round-tripping; ad-hoc splitters corrupt notes silently.

## 6. Owner's rules, now written (interview 2026-07-07)

1. **Never write to the live `indexes/lifeos.db` from tests or ad-hoc scripts.** Copy it to a temp path first (use the session scratchpad or `tempfile`) and point your code at the copy. Rebuilding embeddings costs real API money; the DB is ~350 MB with ~50k embedded chunks (exact numbers: db_stats.py in **lifeos-diagnostics-and-tooling**). Read-only inspection is fine: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT ..."` (`immutable=1` is required — plain `mode=ro` fails on this WAL database; vector-table queries fail in the CLI regardless — expected, the sqlite-vec extension isn't loaded there). Evidence this matters: a full pytest run added 240+ rows to `agent_repair_logs` in the live DB.
2. **The `data/` tree is Syncthing-synced with a VPS.** Treat it as machine-shared territory: another machine writes there. Apply §7 before committing anything from it.
3. **LLM cost discipline.** No bulk LLM or embedding jobs without a cost estimate presented first (also `privacy.yml`: "Ask before making paid API calls above a certain threshold").

## 7. VPS Sync Review Protocol (`AGENTS.md`)

Before committing files that arrived via Syncthing from the VPS:

1. `git status` + `git diff` the synced files — never assume VPS-originated content is safe or leak-free.
2. Commit them locally so the pre-commit hook (§4) scans them for PII/secrets/paths. **Do not bypass the hook for synced files.**
3. Verify functional changes from the VPS are reflected in `CHANGELOG.md` / `README.md`.

## 8. Actions requiring explicit human approval

Never do these autonomously (sources: `AGENTS.md` Step 6; `privacy.yml`; `docs/architecture-principles.md` principles 6–8):

- Merge any branch to `main`.
- Push to GitHub (any remote, any branch).
- Publish anything externally: social media, email, the TinaCMS website repo push in the Hermes pipeline. (Caveat: the SCHEDULED weekly run currently pushes automatically with no approval gate — a surfaced open doctrine conflict awaiting an owner decision; see **lifeos-portfolio-and-positioning**. Manual runs remain approval-gated.)
- Paid API calls above a modest threshold — bulk LLM/embedding runs need a cost estimate + go-ahead first.
- Overwriting user-layer markdown — append or propose, never silently overwrite (`privacy.yml`).
- Promoting content to expert profiles or long-term memory (principle 6); the system never auto-modifies its own architecture, prompts, or profile memory (principles 7–8: improvement candidates go to `outputs/improvement-candidates/` for human review).
- Sending `data/private/` content to non-secure external APIs (never, approval or not — `privacy.yml`).

## 9. Decision table: "I want to change X"

| Change | Gates, in order |
|---|---|
| Python in `src/`, `scripts/`, `apps/` | feat branch → spec if non-trivial → targeted tests (temp DB copy) → commit (full hook: regex → pip-audit → bandit → AI review) → user approval to merge → user approval to push |
| `requirements.txt` | feat branch → commit; pip-audit re-runs; new CVE ignore requires a documented reason in the hook comment |
| `README.md` / `CHANGELOG.md` / `docs/` | feat branch → check against `AGENTS.md` + architecture principles → commit (regex scan) → approval to merge/push |
| A skill in `skills/` or `.claude/skills/` | feat branch → commit (regex scan — no PII/paths/name in skill text) → approval to merge/push |
| Knowledge/expert markdown | Usually `.gitignore`d — do not force-add. Never overwrite; append/propose. If VPS-synced, run §7 |
| Anything under `data/` | §7 (VPS sync review) first, then class-appropriate gates |
| Implement a proposal | Full §2 workflow, steps 0–7 |
| Tests touching the DB | Temp copy of `indexes/lifeos.db`, never the live file (§6.1) |
| Bulk LLM/embedding job | Cost estimate → user approval → run |
| Hook blocked my commit | Read the failure line; fix the content (do not weaken the hook); `--no-verify` is forbidden; `SKIP_AI_REVIEW=1` only for stage-4 emergencies, then manual review + provenance note |

## When NOT to use this skill

- Recreating the environment / installing the pre-commit hook on a fresh clone → **lifeos-build-and-env**
- Running the apps/pipelines day-to-day → **lifeos-run-and-operate**
- Something is broken and you're triaging → **lifeos-debugging-playbook**
- The security incident's full story and the PII regime → **lifeos-security-and-privacy**
- What counts as evidence / test standards, the red suite → **lifeos-validation-and-qa**
- The `data/` vs root-tree divergence itself → **lifeos-data-layout-unification-campaign**
- Env vars and config knobs → **lifeos-config-and-flags**
- Design invariants and why the architecture is shaped this way → **lifeos-architecture-contract**

## Provenance and maintenance

Re-verify volatile facts (all commands from repo root):

- Workflow & invariants: `grep -n "Hermes Proposal" AGENTS.md` and read the "Safety & Invariant Rules" section.
- Hook stages & guarded patterns: `cat .git/hooks/pre-commit` (read locally; do not quote its literals into tracked files).
- Hook still untracked: `git ls-files | grep -i hook` (empty ⇒ gap stands).
- CVE ignore count: `grep -c ignore-vuln .git/hooks/pre-commit` (16 as of 2026-07-07).
- Bypass flag: `grep -n SKIP_AI_REVIEW scripts/ai_code_reviewer.py`.
- Branch naming: `git branch -a | grep feat/`.
- Referenced-but-missing skills: `ls skills/ .agents/skills/` (no caveman/spec-driven-development/code-review-and-quality as of 2026-07-07).
- Incident commits: `git log --oneline | grep -iE "security|scrub"` (expect `51ba952`, `0bb27d4`, `5213801`); CHANGELOG 2026-06-26 entry.
- DB size/chunks: `ls -lh indexes/lifeos.db` and `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT count(*) FROM doc_chunks;"`.
- Approval rules: `cat privacy.yml` and `docs/architecture-principles.md` principles 6–8.
