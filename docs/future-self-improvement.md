# Future: LifeOS Self-Improvement

> **Status:** Future roadmap concept. Do not implement in MVP.
> **Last updated:** 2026-05-24

---

## Concept

LifeOS should eventually suggest improvements to itself when new insights are saved.
The user decides what to approve. The system never modifies itself autonomously.

---

## Future Workflow

```
Resource → Insight Note → Impact Analysis → Improvement Candidate → Human Review → Approved Patch
```

When a new Insight Note is created, LifeOS may later analyse it and identify:

- **Affected experts** — which Expert profiles may need updating based on the new source
- **Affected projects** — which active projects or roadmap items relate to this insight
- **Possible roadmap updates** — is there a new phase or task worth adding?
- **Possible prompt/mode improvements** — should a system prompt or routing rule be refined?
- **Possible architecture improvements** — does the insight reveal a better structural approach?
- **Possible UI/UX improvements** — is there a friction point worth fixing?
- **One next action** — the single most important thing Markus could do with this insight

---

## Improvement Candidate Format

Each candidate is saved as a markdown file to:

```
outputs/improvement-candidates/
```

### File naming convention
```
outputs/improvement-candidates/YYYY-MM-DD--<short-slug>.md
```

### Required fields (YAML frontmatter)

```yaml
---
type: improvement_candidate
source_insight: <path to the Insight Note that triggered this>
proposed_change: "<one-sentence description>"
affected_files:
  - <file or folder path>
expected_benefit: "<what improves if this is applied>"
risk_of_overbuilding: "<what could go wrong or grow too complex>"
priority: now | next | later | ignore
human_approval_required: true
status: pending_review
created_at: <ISO timestamp>
---
```

### Body template

```markdown
# Improvement Candidate: <proposed change title>

## What to change
<Specific description of the proposed improvement>

## Why
<Rationale based on the source insight>

## Affected files / areas
- <list>

## Expected benefit
<What becomes better>

## Risk of overbuilding
<What to avoid>

## Priority
now / next / later / ignore

---
> ⚠️ Human review required. LifeOS does not apply this automatically.
```

---

## Rules

1. **LifeOS may suggest** improvements to its own architecture, prompts, Expert profiles, or roadmap.
2. **LifeOS must not automatically modify** architecture, prompts, Expert profiles, or memory without explicit human approval.
3. **No autonomous self-editing in MVP.** All suggested patches require a deliberate human decision.
4. **Candidates are proposals, not patches.** They describe a change; they do not apply it.
5. **Priority scoring is a signal, not a command.** `now` means worth doing soon; `ignore` means the cost outweighs the benefit.

---

## What Stays MVP

The core loop that ships first:

```
Save Insight → Search Library → Attach to Expert → Ask Expert
```

This loop is local, fast, markdown-based, and fully human-controlled.

---

## What Waits

The following capabilities are explicitly deferred until after MVP is stable and validated:

| Deferred capability          | Reason                                              |
|------------------------------|-----------------------------------------------------|
| n8n automation               | External dependency, adds operational complexity    |
| Telegram / voice input       | New interaction layer, out of scope for core loop   |
| Auto-watchers / file agents  | Autonomous triggers without human initiation        |
| Deployment / hosting         | Portfolio-ready local build comes first             |
| Autonomous agents            | No self-acting systems without approval gates       |
| Self-patching                | LifeOS proposes; Markus applies                   |
| Vector DB                    | SQLite FTS5 sufficient for current scale            |

---

## Connection to Architecture Principles

This concept extends **Principle 8: Safe Self-Improvement (Insight-to-Impact)** documented in:
[`docs/architecture-principles.md`](./architecture-principles.md)

The full pipeline (`Resource → Insight Note → Impact Analysis → Improvement Candidate → Human Review → Approved Patch`) is the long-term vision. The improvement candidate format above is the concrete data structure that makes it reviewable and auditable.
