# Future Feature: PDF & Book Ingestion

Currently, LifeOS focuses on YouTube videos, short articles, and raw text notes. In the future, the ingestion pipeline will be expanded to support full books and long-form PDFs.

## Proposed Workflow

Because LLM context windows are large but still struggle with "needle in a haystack" retrieval across entire books, we will use a chunked synthesis approach.

**Pipeline:**
`PDF / Book` → `Extracted Text` → `Chapter Summaries` → `Insight Notes` → `Attach to Expert`

1. **Extraction**: Parse the PDF text locally.
2. **Chunking**: Split the text logically by chapter or major section.
3. **Chapter Summaries**: The LLM processes each chapter into a standalone summary.
4. **Insight Extraction**: The LLM analyzes the chapter summaries to generate distinct, actionable `insight_note` files.
5. **Curation**: The user attaches those targeted Insight Notes to the relevant Expert Profile.

## Strict Rules & Constraints

- **No Raw PDFs in Context**: Experts should NOT consume raw PDFs directly during the `Ask Expert` phase. The retrieval engine should only load the curated, synthesized Insight Notes.
- **Copyright Protection**: Full copyrighted PDFs or raw text dumps must NEVER be committed to the GitHub repository. They belong strictly in `data/private/` or `data/knowledge/ai-resources/raw/`.
- **Legal Usage**: Only ingest PDFs and books that you have the legal right to use and process locally.
