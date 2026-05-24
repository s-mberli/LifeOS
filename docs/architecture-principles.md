# Architecture Principles

## 1. Markdown Source of Truth
All knowledge, profiles, and configuration are stored as plain-text Markdown and YAML. This ensures maximum portability, longevity, and ease of human readability without database lock-in.

## 2. Local-First
Compute, storage, and search (SQLite FTS5) happen locally. The system relies on local directories rather than cloud databases, ensuring speed, privacy, and full control over the data lifecycle.

## 3. Public/Private Split
The repository is designed to be GitHub-safe. System prompts, architecture, and UI code are public. All personal data, captured insights, and expert profiles (`data/knowledge`, `data/experts`, `data/private`) are strictly `.gitignore`d to protect privacy while allowing the engineering portfolio to be showcased.

## 4. Insight Notes Over Raw Sources
Instead of dumping raw transcripts into the retrieval engine, LifeOS processes resources into dense, synthesized "Insight Notes". The raw transcript is preserved, but the system operates primarily on the high-signal insight layer.

## 5. Expert Profiles Built From Many Sources
Experts are not 1:1 with sources. An expert profile is a living synthesis (a playbook and worldview) constructed over time by continuously attaching numerous specific insight notes.

## 6. Human Approval Before Profile/Memory Promotion
There is no fully autonomous "hallucination loop". The system auto-captures raw input, but a human explicitly curates and approves what gets attached to an expert or promoted to long-term memory. 

## 7. No Broad Autonomy in MVP
The MVP explicitly defers complex autonomous agent loops (e.g., executing arbitrary code, modifying its own infrastructure). The focus is entirely on strict retrieval, synthesis, and structured human-in-the-loop workflows.

## 8. Safe Self-Improvement (Insight-to-Impact)
LifeOS may suggest improvements to its own architecture, prompts, or roadmap based on ingested insights, following the **Insight-to-Impact** pipeline (`Resource → Insight Note → Impact Analysis → Improvement Candidate → Human Review → Approved Patch`). 
- The system must *never* automatically modify architecture, prompts, or profile memory without approval. 
- Candidates are saved to `outputs/improvement-candidates/`.
- Each candidate must strictly include: the source insight, the proposed change, affected files, expected benefit, risk of overbuilding, and a priority score (now / next / later / ignore).
