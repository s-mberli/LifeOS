# Experts Concept

In LifeOS, an **Expert** is not a simple folder of text, nor is it a chatbot template. An Expert is a **stateful cognitive prism** that sits on top of your local Markdown knowledge base.

It translates raw information (Insight Notes) into actionable strategies and playbooks, tailored to a specific domain or perspective (e.g., *AI Systems Architect*, *Flow Strategist*).

---

## Directory Structure

Each Expert is isolated in its own folder under `data/experts/`:

```
data/experts/expert--<expert-slug>/
├── profile.md
├── playbook.md
├── principles.md
└── sources/
    ├── <insight-note-filename>-ref.md
    └── ...
```

### 1. `profile.md`
Describes the expert's role, identity, goals, and focus areas. It serves as the baseline system prompt fragment for the LLM when executing queries in this Expert's mode.

### 2. `playbook.md`
Actionable workflows, standard operating procedures (SOPs), and strategies that this expert uses to get results.

### 3. `principles.md`
Core beliefs, evaluation criteria, and architectural heuristics that this expert adheres to.

### 4. `sources/`
A folder containing lightweight **Source Reference Files** (`*-ref.md`). Instead of copying large Insight Notes directly into the expert folder, we create a reference file.

---

## The Source Reference Mechanism

To decouple raw information from the cognitive profiles, LifeOS uses a reference file format. This allows a single Insight Note to be attached to multiple experts without duplicating content or breaking indexes.

### Reference File Format (`-ref.md`):

```markdown
---
type: expert_source_reference
expert_slug: ai-systems-architect
source_path: data/knowledge/youtube/insight--rich-hickey-design-simplicity.md
source_title: "Design, Composition, and Performance - Rich Hickey"
source_url: https://www.youtube.com/watch?v=MCZ3YPnnclU
attached_at: 2026-05-24T10:49:00+10:00
---

# Reference Notes
This source outlines the core values of simplicity vs. easy, and composition of simple components.
```

When you perform an **"Ask Expert"** query, LifeOS dynamically:
1. Scans `data/experts/expert--<slug>/sources/` for all `-ref.md` files.
2. Extracts the `source_path` pointers.
3. Builds an `allowed_paths` filter.
4. Executes a SQLite FTS search scoped *only* to those allowed files, and injects the retrieved insight content along with the Expert's profile, playbook, and principles into the LLM context.

---

## Expert Playbook Updates

As you attach more Insight Notes to an Expert, the expert's knowledge base grows. Periodically, you can trigger the **`update-expert`** skill, which:
1. Synthesizes new insight notes attached to the Expert.
2. Generates proposed additions or refinements for `playbook.md` and `principles.md`.
3. Saves these suggestions as a file under `outputs/expert-updates/`.
4. Alerts you in the Streamlit UI to review, edit, and approve the update. **The system will never overwrite your profiles autonomously.**
