# LifeOS Roadmap

**Positioning:** Local-first Personal Insight Library with Expert Modes.
**Interaction Layer:** Personal Expert Network.
**Core Pipeline:** Resource → Insight Note → Expert Profile/Mode → Ask Expert Network → Action/Decision → Portfolio Proof.
**Primary MVP:** YouTube / Creator Wisdom Expert Network.

## Phase 0: Current cleanup/refocus
- Remove generic LifeOS features and complex developer cockpits.
- Simplify UI to focus strictly on ingestion, searching, and expert networks.
- Finalize public/private safe repository structure.

## Phase 1: Save Insight pipeline
- Robust ingestion of YouTube/articles into structured Insight Notes.
- Auto-extract transcripts, metadata, and AI summaries.
- Route to global library by default.

## Phase 2: Expert Profiles
- Scaffold `synthesis_expert` and `creator_expert` profiles.
- Implement post-processing workflows to effortlessly attach existing insights.
- Generate lightweight `expert_source_reference` YAML files to avoid duplicating heavy transcripts.

## Phase 3: Ask Expert with sources
- Enable routing natural language queries to specific expert profiles.
- Use FTS and retrieval to pull from an expert's evidence log.
- Generate answers strictly grounded in the curated source material.

## Phase 4: 5–10 eval questions
- Curate a benchmark suite of 5-10 core user questions.
- Measure and refine retrieval accuracy and answer quality against the expert network.

## Phase 5: GitHub/portfolio packaging
- Polish documentation and READMEs.
- Clean up architecture.
- Finalize the repository for public portfolio display (ensuring private data is strictly `.gitignore`d).

## Phase 6 later
- Bulk channel ingestion (Playlists / Channels).
- PDF document parsing.
- Advanced automations (n8n, Telegram, Hermes).
- **Insight-to-Impact and Self-Improvement Candidates**:
  - *Workflow:* Resource → Insight Note → Impact Analysis → Improvement Candidate → Human Review → Approved Patch
  - When ingesting an Insight Note, LifeOS will identify affected experts, projects, roadmap updates, and self-improvement architecture/prompt patches.
  - Candidates are saved to `outputs/improvement-candidates/` for human review prior to any system modification.
