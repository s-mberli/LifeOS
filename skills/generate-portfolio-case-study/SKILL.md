# Skill: generate-portfolio-case-study (Roadmap Concept)

Compile real-world actions, expert advice, and decision outcomes documented in LifeOS into structured, markdown **Portfolio Case Studies** to showcase domain expertise.

---

## Purpose
Convert a series of internal action logs and insight notes into an outward-facing, professional portfolio case study.

## When to use
Use when preparing technical case studies for public consumption (e.g. personal website, resume, GitHub portfolio) based on real problems solved.

## Technical Contract

### Inputs
- `expert_slug` (string, required): The expert profile whose frameworks were utilized.
- `problem_statement` (string, required): The challenge faced.
- `evidence_paths` (list of strings, required): Paths to Insight Notes or evidence logs documenting the action taken and output generated.

### Outputs
- **Portfolio Case Study**: Saved to `outputs/portfolio-case-studies/case-study--<slug>.md`.

---

## Workflow Steps

1. **Log Gathering**:
   - Collect the designated expert profile files and the referenced evidence/notes.
2. **Analysis & Structure (LLM)**:
   - Synthesize the timeline:
     - What was the initial state?
     - What frameworks from the expert's playbook were applied?
     - How did these frameworks shape the final design or code?
     - What was the resulting impact?
3. **Drafting Case Study**:
   - Write the case study using professional STAR/Action-Result formats, outputting a polished markdown artifact.
4. **Human Review**:
   - Save to a pending outputs folder for final human polish before uploading/publishing.

---

## Rules
- Focus on authentic, quantitative outcomes (if available).
- Avoid generic marketing buzzwords; keep the tone grounded and technical.

## Edge Cases
- **Insufficient evidence provided**: The skill should flag missing data and suggest specific types of evidence (e.g. unit tests, metrics) to make the case study convincing.

## Human Review Gates
- Core requirement. The generated markdown case study is saved to a drafts directory and must never be pushed to a public channel automatically.

## Related Existing Scripts/Functions
- None (Future Roadmap).

## Test Ideas
- Run on a sample project description and verify that it references the Expert playbook heuristics and outputs structured sections.
