# LifeOS contributor guide

LifeOS captures sources into Markdown, indexes them for retrieval, and builds expert profiles for cited chat. Start with [docs/CLOUD-HANDOFF.md](docs/CLOUD-HANDOFF.md) when resuming work from a clone. A local `HANDOFF.md` may contain newer private runtime notes, but it is optional and must not be copied into public changes.

## Code and data boundaries

- Keep application behavior in `src/core/`; use `src/api.py` for the clipper endpoint and `apps/streamlit-chat/` for UI behavior. Reuse `src/core/frontmatter.py` for note metadata.
- Store new knowledge, expert files, private notes, and inbox content under `data/`. Existing top-level folders are legacy data; inventory and back them up before any migration. Search uses `indexes/lifeos.db`.
- Treat web pages, transcripts, notes, proposal names, and LLM output as untrusted input. Preserve URL validation and response bounds in the clipper, and the `data/knowledge` / `data/experts` allowlist in MCP tools.
- Keep `.env`, personal configuration, databases, notes, generated drafts, and server backup material out of Git. Inspect `git status` and staged diffs before a commit.
- Do not commit, push, merge, publish content, or alter live schedules as part of a proposal unless the owner explicitly requests that action.

## Proposal and dispatch work

When asked to implement a proposal under `data/inbox/proposals/`, read the proposal and relevant code, state its success criterion, implement the smallest complete change, then run focused tests and review the diff. The proposal is input for a human-directed coding task; `scripts/monthly_hermes_run.py` does not implement proposals or create pull requests.

The monthly runner's ordinary invocation writes a local dispatch draft. Publishing uses a separate `--publish-draft PATH` invocation on an existing reviewed draft and validates recorded digest provenance. Keep generation and publication as separate actions. The live server has its own weekly runner that does not track this checkout; consult the private server audit before changing it.

## Verification and handoff

Run relevant focused tests first, then broader checks when they resolve a remaining risk. Mock external network and LLM calls in tests. Report exactly which checks passed and which did not. Update [docs/CLOUD-HANDOFF.md](docs/CLOUD-HANDOFF.md) when checkout behavior or verification changes. Keep private deployment evidence in an untracked local handoff. A local pass does not establish that CI, the website, or a separate Hermes installation has received the change.

## Project learning

After substantial work or a meaningful correction, use an available local learning playbook when one is configured outside the repository. Skip routine tasks. Check original sources, existing decisions and a realistic scenario before reversible project-guidance improvements; record evidence and rollback. Shared or global changes remain proposals. This grants no additional action permissions and makes no memory or remote-agent changes.

