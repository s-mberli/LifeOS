---
name: lifeos-config-and-flags
description: Complete catalog of every LifeOS configuration axis — env vars, config files, flags, defaults, schedules. Load when touching env vars or config files, when a provider/model/schedule needs changing, when something reads the "wrong" config copy (root vs config/), when adding a new setting, when setting up .env from .env.example, or when auditing config drift. Covers LLM_PROVIDER_ORDER, per-provider model vars, dead vars (MAX_TOKENS, HERMES_BIN), the config/ vs root duplication, and drift-audit recipes.
---

# LifeOS Configuration and Flags

Catalog verified against the working tree **as of 2026-07-07**. Every row was grep-verified; flags drift, so re-run the commands in "Drift audit recipe" before trusting a row that matters. All commands are relative to the repo root.

Jargon, once: **Hermes** = the weekly dispatch pipeline (`scripts/weekly_hermes_run.py`) that generates a digest and pushes it to a website repo via PyGithub. **Provider cascade** = `src/core/llm_client.py` trying LLM providers in order until one succeeds.

## When NOT to use this skill

- Debugging *why* a pipeline fails → `lifeos-debugging-playbook`.
- RAG/index internals (chunking, sqlite-vec) → `lifeos-rag-reference`.
- Installing dependencies / venv setup → `lifeos-build-and-env`.
- Deciding whether a change is allowed at all → `lifeos-change-control` and `AGENTS.md`.
- Privacy *policy* questions → `lifeos-security-and-privacy` (this skill only records where `privacy.yml` lives and who reads it).

## 1. Environment variable catalog (master table)

Status legend: **production** = read by live code paths; **experimental** = read but off by default / niche; **DEAD** = present in `.env.example` (or lore) but no code reads it; **undocumented** = read by code but missing from `.env.example`.

| Name | Read by (file:line) | Default | Purpose | Status |
|---|---|---|---|---|
| `LLM_PROVIDER_ORDER` | `src/core/llm_client.py:187` (`try_providers`) | `"openrouter,gemini"` in code; `.env.example` line 5 says `azure,gemini,openrouter` — **the two disagree**; the code default wins when unset | Comma-separated provider cascade order | production |
| `OPENROUTER_API_KEY` | `src/core/llm_client.py` (openrouter path; also embeddings), `apps/streamlit-chat/ui/modals.py` | none (provider skipped if unset) | OpenRouter auth | production |
| `OPENROUTER_MODEL` | `src/core/llm_client.py:46` | `"openai/gpt-4o-mini"` | OpenRouter chat model | production |
| `GEMINI_API_KEY` | `src/core/llm_client.py` (gemini path), modals.py | none | Gemini auth | production |
| `GEMINI_MODEL` | `src/core/llm_client.py:73` | `"gemini-2.5-flash"` | Gemini chat model | production |
| `AZURE_OPENAI_API_KEY` | `src/core/llm_client.py` (azure path), modals.py | none | Azure OpenAI auth | production |
| `AZURE_OPENAI_ENDPOINT` | `src/core/llm_client.py` (azure path) | none | Azure endpoint URL | production |
| `AZURE_OPENAI_DEPLOYMENT` | `src/core/llm_client.py:138` | `"gpt-4o"` | Azure deployment name | production |
| `AZURE_OPENAI_API_VERSION` | `src/core/llm_client.py:139` | `"2024-02-15-preview"` | Azure API version | production (not in `.env.example`) |
| `AZURE_EXISTING_AIPROJECT_ENDPOINT` | **no reader found** (`grep -rn AZURE_EXISTING src/ scripts/ apps/` → empty) | — | leftover from an Azure template | **DEAD** (in `.env.example`) |
| `DEEPSEEK_API_KEY` | `src/core/llm_client.py:111` | none (provider errors if selected without it) | DeepSeek auth | production but **missing from `.env.example`** |
| `DEEPSEEK_MODEL` | `src/core/llm_client.py:114` | `"deepseek-chat"` | DeepSeek model | production, missing from `.env.example` |
| `DEEPSEEK_BASE_URL` | `src/core/llm_client.py:122` | `"https://api.deepseek.com/v1"` | DeepSeek endpoint | production, missing from `.env.example` |
| `AZURE_OPENAI_MAX_TOKENS`, `GEMINI_MAX_TOKENS`, `OPENROUTER_MAX_TOKENS` | **nothing reads them** — `grep -rn MAX_TOKENS src/ scripts/ apps/ tests/` finds only hard-coded constants (`scripts/ai_code_reviewer.py:39` `REVIEW_MAX_TOKENS = 4000`; `scripts/weekly_hermes_run.py:63` `DISPATCH_MAX_TOKENS = 7000`) | — | none | **DEAD / decorative** (present in both `.env` and `.env.example`) |
| `WEBSITE_GITHUB_TOKEN` | `scripts/weekly_hermes_run.py:202` (`push_to_github`) | none (push skipped/fails without it) | PAT for pushing the weekly digest to the website repo | production, **missing from `.env.example` — confirmed drift** |
| `WEBSITE_GITHUB_REPO` | `scripts/weekly_hermes_run.py:203` | none | `owner/repo` target for the digest push | production, **missing from `.env.example` — confirmed drift** |
| `GITHUB_TOKEN` | **no reader in `src/`, `scripts/`, or `apps/`** (grep across all three finds only the `.env.example` line 25 comment "required for Hermes") | — | Presumably consumed by the *external* Hermes agent binary or `gh` tooling, not by this repo's code | **DEAD within this repo** — keep only if the external agent needs it |
| `ELEVENLABS_API_KEY` | `src/core/tts.py:24` (raises `ValueError` if unset), modals.py | none (required for TTS) | ElevenLabs text-to-speech auth | production |
| `ELEVENLABS_DEFAULT_VOICE_ID` | `src/core/tts.py:29` | `"21m00Tcm4TlvDq8ikWAM"` (Rachel) | Default TTS voice | production |
| `HERMES_BIN`, `HERMES_SCRIPT` | **no reader found** — grepped `src/ scripts/ apps/` including `scripts/install_hermes.sh` and `scripts/weekly_hermes_run.sh` | — | intended paths to the external hermes agent | **DEAD** (in `.env.example` lines 33–34; not in `.env`) |
| `INCLUDE_PROPOSALS` | `scripts/weekly_hermes_run.py:583,661` | off (must equal `"true"`, case-insensitive) | Enables Phase 2a architecture-proposal generation in the weekly dispatch | experimental (undocumented in `.env.example`) |
| `SKIP_AI_REVIEW` | `scripts/ai_code_reviewer.py:154` (must equal `"1"`) | off | Bypasses the AI pre-commit review gate — **emergency use only** | production guard (undocumented) |
| `GIT_AUTHOR` | `.git/hooks/pre-commit:122` (`AUTHOR="${GIT_AUTHOR:-Human}"`) | `"Human"` | Authorship tagging in the pre-commit hook (set to e.g. `Claude` for agent commits) | production guard (undocumented) |
| `DEBUG` | `apps/streamlit-chat/ui/sidebar.py:34`, `ui/modals.py:21`, `ui/chat.py:42` | off (any truthy value enables) | Extra debug output in the Streamlit UI | experimental (undocumented) |

### dotenv loading precedence (important, two mechanisms)

1. `src/core/llm_client.py:18-25`: `load_dotenv(ROOT/".env", override=True)` — repo `.env` **overrides** already-exported shell vars — then `load_dotenv("/root/.hermes/.env", override=False)` as a VPS-only fallback that fills gaps without overriding.
2. `scripts/weekly_hermes_run.py:27-40`: its **own** hand-rolled `load_env()` parser reads repo `.env` at import time and unconditionally sets `os.environ[key]` (also override semantics; strips quotes; ignores comments). It runs before llm_client's loader is imported, so both end up agreeing, but remember there are two parsers to keep in sync.

## 2. Config file catalog — and which copy is live

The June-21 restructure left **duplicate trees**: root-level `domains.yaml` / `domain_map.yaml` / `privacy.yml` / `profile.yml` / `models.yml` AND a `config/` directory with the same names. **All verified code readers use `ROOT/config/` — the `config/` directory is live; the root-level copies are stale committed leftovers.** One exception/bug noted below.

| File | Live? | Read by (verified) | Committed? (`.gitignore`) | Notes |
|---|---|---|---|---|
| `config/domains.yaml` | **LIVE** | `src/core/ingest.py:504`, `scripts/correct_metadata.py:15` (both `ROOT/"config"/"domains.yaml"`) | gitignored (`.gitignore:90`); template `config/domains.example.yaml` committed | Valid ingestion domains; ingest falls back to a hard-coded 6-domain list if missing |
| `src/config/domains.yaml` | **does not exist — BUG** | `src/core/classify_input.py:7` computes `parent.parent/'config'/domains.yaml` = `src/config/…`, which is absent, so `DOMAINS_CONFIG` silently loads `{}` | n/a | classify_input always runs with empty domain config; fix the path to `ROOT/config` |
| `config/domain_map.yaml` | **LIVE** | `src/core/experts.py:33` (loaded fresh per call, no cache) | committed (`.gitignore:113` un-ignores it) | domain → expert-slug mapping; new domains need no code change |
| `config/profile.yml` | **LIVE** | `src/core/ingest.py:304`, `apps/streamlit-chat/ui/modals.py:589` | gitignored (`.gitignore:87`); `config/profile.example.yml` committed | Personal profile injected into pipelines |
| `config/privacy.yml` | gitignored (`.gitignore:89`) | **no code reader found** (`grep -rn privacy.yml src/ scripts/ apps/` → empty) | root `privacy.yml` IS committed | **Doctrine-only**: consumed by agents/humans reading the repo, not enforced by code. Say so honestly when reasoning about privacy guarantees. |
| `models.yml` (root) + `models.example.yml` | **DEAD / aspirational** | **no reader anywhere** (`grep -rn "models.yml\|models.yaml" src/ scripts/ apps/ tests/` → empty) | root copies committed; `config/models.yml` gitignored (`.gitignore:88`) | Declares `default_model: gemini-3.1-pro` — nothing honors it. Real model selection is env-var driven (section 3). |
| root `domains.yaml`, `domain_map.yaml`, `profile.yml`, `privacy.yml` | **STALE** (root copies committed but unread — all readers use `config/`) | none | committed | Candidates for the `lifeos-data-layout-unification-campaign` cleanup |
| `.env` / `.env.example` | live | see section 1 | `.env` gitignored (`.gitignore:6`); `.env.example` committed (`:114`) | Drift summary in section 5 |
| `pytest.ini` | live | pytest | committed | `testpaths = tests`, `addopts = -v --tb=short` |
| `.bandit.yml` | live | bandit (security lint) | committed | excludes `tests/`, venvs; skips `B101` (assert) |
| `.stignore` | live | Syncthing (Mac ↔ VPS sync) | committed | excludes `.git/`, venvs, `__pycache__`, `indexes/*.db` etc. |
| `.streamlit/config.toml` | live | Streamlit chat app | committed | dark theme, `toolbarMode = "minimal"` |
| `com.lifeos.tldr_ingest.example.plist` | template | launchd (after copy + install) | committed | daily at **Hour 9, Minute 0** (verified integers) |
| `com.lifeos.hermes_weekly.example.plist` | template | launchd | committed | **Weekday 5 (Friday), Hour 8, Minute 0** (verified integers) |
| `com.lifeos.lenny_ingest.example.plist` | template | launchd | committed | daily at Hour 10, Minute 0 |
| `.github/workflows/tests.yml` | live | GitHub Actions | committed | Python **3.11**, plain `pytest tests/` — **currently red** (10 failed / 188 passed as of 2026-07-07); do not "fix" by weakening the workflow |
| `requirements.txt` | live | pip | committed | mixed pinning: exact (`streamlit==1.57.0`, `PyYAML==6.0.1`, `beautifulsoup4==4.12.3`) and floors (`openai>=1.14.0`, `litellm>=1.83.7`, `PyGithub>=2.3.0`, `sqlite-vec>=0.1.3`) |

## 3. Model configuration: what is actually real

- **Real selection is env-var driven** in `src/core/llm_client.py`: `LLM_PROVIDER_ORDER` picks the cascade; each provider reads its own `*_MODEL`/`*_DEPLOYMENT` var with the defaults in the table above. `models.yml` is read by nothing — ignore it when changing models.
- **Hard-coded override hack**: `src/core/search_knowledge.py:362-364` (`synthesize_briefing`) temporarily mutates `os.environ` to force `OPENROUTER_MODEL="openrouter/owl-alpha"`, `GEMINI_MODEL="gemini-2.0-flash-exp:free"`, `LLM_PROVIDER_ORDER="openrouter,gemini"` (originals saved and restored in a try/finally). This is a cost-discipline hack and a known weak point — cross-ref `lifeos-architecture-contract`. Changing model env vars will NOT affect briefing synthesis until this is removed.
- **Embeddings model is hard-coded**: `"nomic-ai/nomic-embed-text-v1.5"` at `src/core/llm_client.py:321` (`get_embeddings`, via OpenRouter). No env var controls it; changing it invalidates the existing vector index — see `lifeos-rag-reference`.

## 4. Checklist: adding a new configuration axis

1. Name it `SCREAMING_SNAKE` with a component prefix (`FOO_API_KEY`, not `KEY`).
2. Read it via `os.environ.get("NAME", "sensible-default")` — never crash on absence unless it is a secret a feature genuinely requires (follow `tts.py`'s explicit `ValueError` pattern then).
3. Add it to `.env.example` with a placeholder (`your-key-here`) and a one-line comment. **Never commit real values**; `.env` is gitignored — keep it that way.
4. If a script has its own env loader (`weekly_hermes_run.load_env`), confirm your var flows through it too.
5. Consider `config/privacy.yml` doctrine if the value touches personal data.
6. Add a row to the master table in **this skill** and re-run the drift audit below.
7. Pass the pre-commit gate (AI reviewer runs unless `SKIP_AI_REVIEW=1`; authorship via `GIT_AUTHOR`). See `lifeos-change-control`.

## 5. Drift audit recipe (re-verify before trusting this skill)

Compare `.env` key **names** to `.env.example` — **never print values**:

```sh
diff <(grep -o '^[A-Z_]*' .env | sort -u) <(grep -o '^[A-Z_]*' .env.example | sort -u)
```

Find every env read in code:

```sh
grep -rn "os\.environ\|os\.getenv" --include="*.py" src/ scripts/ apps/ | grep -oE '(environ\.get|getenv)\("([A-Z_]+)' | sort -u
```

Find config-file readers:

```sh
grep -rn "domains.yaml\|domain_map\|privacy.yml\|profile.yml\|models.yml" src/ scripts/ apps/ | grep -v pyc
```

**Known drift as of 2026-07-07:**
- `.env` has `WEBSITE_GITHUB_TOKEN` / `WEBSITE_GITHUB_REPO`; `.env.example` does not → add them to the example (placeholders only).
- `.env.example` has `HERMES_BIN` / `HERMES_SCRIPT` / `AZURE_EXISTING_AIPROJECT_ENDPOINT` with **no code reader** → dead; re-verify with the grep above before deleting.
- `*_MAX_TOKENS` vars exist in both files but nothing reads them → decorative.
- `.env.example` default `LLM_PROVIDER_ORDER=azure,gemini,openrouter` disagrees with the code default `openrouter,gemini`.
- Code reads `DEEPSEEK_*`, `AZURE_OPENAI_API_VERSION`, `INCLUDE_PROPOSALS`, `SKIP_AI_REVIEW`, `DEBUG`, `GIT_AUTHOR` that the example never mentions.

## Provenance and maintenance

- Author: principal-engineer audit of the working tree, 2026-07-07; every row grep-verified at the cited file:line.
- Line numbers rot: trust the symbol names and re-grep; update this file when a table row changes.
- Sibling skills: `lifeos-architecture-contract` (model-override weak point), `lifeos-data-layout-unification-campaign` (root-vs-config duplication), `lifeos-build-and-env` (installing), `lifeos-security-and-privacy` (privacy doctrine), `lifeos-change-control` (commit gates).
