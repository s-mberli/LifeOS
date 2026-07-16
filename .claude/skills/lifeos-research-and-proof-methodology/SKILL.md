---
name: lifeos-research-and-proof-methodology
description: The discipline that turns a hunch into an accepted result here — the evidence bar (one mechanism must explain ALL observations and survive adversarial refutation), the hypothesis-predicts-numbers-first template, six prove-it recipes each with a worked example from this repo's history, and the idea lifecycle from ingested article to shipped feature or documented retirement. Load this skill when forming a hypothesis about system behavior, designing an experiment, judging whether evidence is sufficient, proposing a new idea or feature, or deciding to adopt or retire an approach.
---

# Research and Proof Methodology

"Prove it, don't just install it." In this project a result is accepted only when it clears the bar below — eyeballing, vibes, and "the LLM said so" are not evidence (`lifeos-validation-and-qa` holds the test-level version of this rule).

## The evidence bar

A claim (a diagnosis, a fix, an improvement) is ACCEPTED when:
1. **One mechanism explains ALL observations — including the negative ones.** If your explanation covers the failure but not why the adjacent case works, it's incomplete.
2. **It survived adversarial refutation.** House pattern: the June-2026 RAG scaling campaign staffed explorer → worker → reviewer → **challenger** → forensic-auditor roles (.agents/orchestrator/BRIEFING.md — a local, gitignored artifact). Solo version: write the claim, write the three strongest attacks on it, run the attack-experiments before believing yourself.
3. **The confirming numbers were predicted BEFORE the run.** Post-hoc rationalization of whatever number appeared is the failure mode this rule exists to kill.

### Hypothesis template (fill in before running anything)

```
Hypothesis:  <one sentence>
Mechanism:   <why it would be true, in terms of this codebase>
Prediction:  <a NUMBER or exact observable, written now>
Experiment:  <read-only first; command(s)>
Actual:      <filled after>
Verdict:     confirmed / refuted / inconclusive (+ what changed your mind)
```

## When NOT to use this skill

- Simple triage of a known symptom → `lifeos-debugging-playbook`. Checking if the battle was already fought → `lifeos-failure-archaeology` FIRST.
- Getting measurements → `lifeos-diagnostics-and-tooling`. Getting a change adopted → `lifeos-change-control`.

## Prove-it recipes (each with a worked example from this repo)

### 1. Prove a retrieval change helps
Fix a golden query set (search_probe.py's list); capture ranked results before; predict the after-ranking; change; re-run; diff. The math must check out by hand: RRF score = Σ 1/(60+rank) per result list. Worked example — the canonical contract is `test_rrf_math_sorting` (tests/test_retrieval_scale.py:540), the final battle of the M1–M5 campaign: given FTS ranks and KNN ranks, compute e.g. rank-2+rank-1 → 1/62+1/61 = 0.032522 vs rank-1+rank-3 → 1/61+1/63 = 0.032266 — agreement across lists beats a single first place, and the sort order is checkable to five decimals before you run anything.

### 2. Prove idempotency
Run twice; the second run must be a no-op or a clean update, proven by identical end-state. Worked example: `push_to_github` (scripts/weekly_hermes_run.py:196-283) exists in its current form because `create_file` threw 422 on rerun; it now checks-then-updates. Pattern for any pipeline: state file + artifact after run 2 == after run 1.

### 3. Prove isolation (no side effects on shared state)
Count the shared resource before and after; predict delta 0. Worked example — this is how the test-pollution defect was PROVEN, not guessed: `agent_repair_logs` count before/after a suite run showed +N rows with fixture names (`persistently_failing` 240, `flaky_json_parser` 64, `flacky_json_parser` 18 — note the typo variant is real data; a query filtering only the correctly-spelled name undercounts). Read-only check: `sqlite3 'file:indexes/lifeos.db?mode=ro&immutable=1' "SELECT function_name, COUNT(*) FROM agent_repair_logs GROUP BY 1 ORDER BY 2 DESC"` (the `immutable=1` is required on this WAL DB).

### 4. Prove a pipeline actually ran end-to-end
Triple-check: log line + state file + artifact. Worked example (daily TLDR): `tail logs/tldr_ingest.log` shows the Done! summary; `grep '2026-07-08' tracking/tldr_ingest.json` shows today's keys; `ls -lt knowledge/news | head -3` shows today's files. Any one alone can lie (logs without artifacts = crashed mid-run; artifacts without tracking = dedup will re-ingest).

### 5. Cost analysis BEFORE bulk LLM operations (owner rule)
Write the estimate first: tokens ≈ chars/4; cost ≈ calls × avg_tokens × provider rate. Worked example — "just rebuild the index": build_index() re-embeds everything, so cost ≈ 50,671 chunks × (~1000 chars → ~250 tokens) ≈ 12.7M embedding tokens × current OpenRouter nomic rate. Whatever the rate is today, the point is the number existed BEFORE the decision — and it's why per-file `index_file` is the default and full rebuilds need justification.

### 6. Prove a fix addresses the mechanism, not the symptom
Green ≠ proven. Worked example: tests/test_experts.py::TestGetExistingExperts::test_finds_expert_directories fails because the test builds tmp `data/experts` while src/core/experts.py:91 reads root `experts/`. TWO changes make it green — edit the test, or edit the code — and they encode OPPOSITE layout decisions. Only Gate 1 of `lifeos-data-layout-unification-campaign` (an owner decision) determines which is the fix and which is damage. When a fix candidate is ambiguous like this, escalate to the decision that disambiguates it; don't pick whichever is easier.

## The idea lifecycle (how a hunch becomes a shipped feature here)

Verified chain: external article (TLDR/X.com) → ingested note (src/core/ingest.py) → `automation_outbox` row → keyword triage score (scripts/triage_outbox.py: AI, Architecture, Github, Python, SQLite, Performance, Agent, LLM) → weekly Hermes run → proposal file in data/inbox/proposals/ with `## Status` = Proposed (template in weekly_hermes_run.py `_build_proposal_prompt`: Problem / Proposed Solution / Source / Status / Effort) → owner reads → "implement this proposal" triggers the AGENTS.md 7-step workflow → merge + CHANGELOG entry with a `**Source:**` URL → Status flipped ✅ Implemented (or ❌ Rejected + reason).

Corpus reality (2026-07-08): data/inbox/proposals holds 39 proposals — 4 ✅ Implemented, 35 Proposed, 0 ❌ Rejected. (A diverged twin dir inbox/proposals holds 21 — layout campaign artifact.) The zero-rejections number is itself a finding: ideas currently die silently instead of being retired with reasons — when you decide against a proposal, WRITE the ❌ and the reason; that's what keeps successors from re-proposing it.

Shipped examples of the full chain: self-repairing agent harness (proposal → src/core/agent_harness.py, commit 72fa9da, X.com source in CHANGELOG 2026-06-12); AI code review pipeline (VentureBeat source → scripts/ai_code_reviewer.py, CHANGELOG 2026-06-12); unified memory core (X.com/mem0ai source → sqlite-vec hybrid RAG, CHANGELOG 2026-06-20). Retirement example: the TicNote API client shipped and was removed 48 minutes later in favor of a manual inbox (commits 6e00603 → f55c3f1) — retiring shipped-but-wrong code fast, with the reason in the CHANGELOG, is house practice.

## Experiment hygiene

- Read-only experiments first; escalate to writes only with a rollback plan.
- Never against the live DB: `cp indexes/lifeos.db scratch/experiment.db` and point your code at the copy (scratch/ is gitignored; still no secrets in it — see `lifeos-security-and-privacy`).
- Cost estimate before any bulk LLM/embedding call (recipe 5).
- Record negative results — they're load-bearing for evidence-bar rule 1, and they become `lifeos-failure-archaeology` entries so nobody re-runs them.
- Baseline before, measure after, diff (`lifeos-diagnostics-and-tooling`).

## Provenance and maintenance

- Proposal corpus counts: `ls data/inbox/proposals/*.md | wc -l; grep -l "✅ Implemented" data/inbox/proposals/*.md | wc -l` (39/4 as of 2026-07-08).
- Triage keywords: `grep -n "KEYWORDS" scripts/triage_outbox.py`.
- RRF contract: `grep -n "def test_rrf_math_sorting" tests/test_retrieval_scale.py`.
- Pollution counts (recipe 3 SQL) drift with every full suite run until campaign Phase 4 lands.
- Rebuild-cost driver: `grep -n "get_embeddings" src/core/build_fts_index.py`.
