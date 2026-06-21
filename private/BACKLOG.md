# 📋 LifeOS Development Backlog

This backlog lists planned technical improvements, features, and optimizations for the **LifeOS** codebase.

---

## 💻 Streamlit UI & UX
- [ ] **Dynamic Expert Editor**: Build a dedicated interface inside the "Experts" tab to view and modify generated playbooks, principles, and profiles.
- [ ] **File Ingest Dropzone**: Add a Streamlit file-uploader component to easily drag-and-drop local `.txt`, `.md`, or `.pdf` files.
- [ ] **Progress Indicators**: Refine the loading spinners and progress bars during multi-video YouTube channel downloads.
- [ ] **Interactive Citation Previews**: Show a preview snippet of references directly in a tooltip or popover when hovering over source citations in Chat.

## 🚀 Core Engine & Ingestion
- [ ] **Local Folder Watcher**: Implement a script that watches a designated directory (e.g., `data/inbox/`) and automatically ingests new files.
- [ ] **Whisper Audio Ingestion**: Add offline transcription capabilities for audio files using local Whisper integrations.
- [ ] **PDF Parser Refinement**: Integrate `pypdf` or `pdfplumber` to handle layouts, headers, and footnotes in long documents.
- [ ] **Semantic Chunking**: Optimize YouTube transcript splitting by grouping sentences logically rather than by fixed token sizes.

## 🔍 Retrieval & Search
- [ ] **FTS & Vector Hybrid Search**: Integrate a lightweight vector store (like `chromadb` or `sqlite-vec`) to support semantic search in addition to FTS5 keywords.
- [ ] **Temporal Query Boosting**: Rank search results higher if they match the date/time range implied by user queries (e.g., "What did I learn last week?").
- [ ] **Expert Domain Filters**: Add multi-select dropdowns in the Library tab to filter search results by specific expert slugs or tags.

## 🧪 Testing & Code Quality
- [ ] **End-to-End AppTest Coverage**: Expand integration tests to simulate complete user journeys (ingesting -> indexing -> chatting).
- [ ] **LLM Output Assertions**: Implement LLM assertions using lightweight evaluation frameworks to measure RAG faithfulness and recall.
- [ ] **Linter & Type Checker Integration**: Add `ruff` and `mypy` configurations to the test suite.

## 🤖 MVP Auditor Suggestions

### 1. Code Refactoring (Slimmer & Professional)
*   **LLM Client Consolidation:** `src/llm_client.py` contains heavy duplication across `call_azure`, `call_gemini`, and `call_openrouter` functions. Refactor to use the Adapter pattern or adopt a unified library like `litellm` to drastically reduce boilerplate and token-counting redundancy.
*   **Decouple Script Logic:** The `src/` directory is cluttered with core business logic (`classify_input.py`, `llm_client.py`, `auto_capture.py`). Move these into a proper `src/core/` or `src/services/` package structure to separate one-off scripts from application infrastructure.
*   **Dynamic Categorization:** `src/classify_input.py` relies on brittle, hardcoded keyword lists for domain routing. Transition to a configuration-driven approach (`config/domains.yaml`) or a lightweight LLM zero-shot classifier for more robust routing.

### 2. UI/UX Improvements for Streamlit
*   **Externalize CSS:** Remove the large inline `<style>` block in `apps/streamlit-chat/app.py`. Extract it into a dedicated `style.css` file and load it via `st.markdown(..., unsafe_allow_html=True)` to clean up the entry point.
*   **Component Modularity:** `ui/chat.py` is monolithic. Break down `_render_chat_body()` into distinct render functions like `render_message_history()`, `render_context_selector()`, and `render_chat_input()` for better maintainability.
*   **Performance & Feedback:** Utilize Streamlit fragments (`@st.fragment`) to prevent full-page reruns during granular interactions (like saving an insight). Introduce a proper Light/Dark mode toggle instead of hardcoded dark themes.

### 3. Missing Features (Modern "Personal AI" Parity)
*   **Semantic Search Engine:** Currently, the system relies on SQLite FTS5 (keyword search). Implement local vector embeddings (using ChromaDB, LanceDB, or SQLite-vec) to enable true semantic, intent-based retrieval.
*   **Continuous Memory:** Integrate an active long-term memory system (like Mem0) that automatically extracts and updates facts about the user from daily conversations, beyond just saving static insight notes.
*   **Multimodal & Voice Input:** Add drag-and-drop support for images and PDFs in the chat. Integrate an audio recorder widget paired with local Whisper for voice-first interactions.
*   **Web Grounding:** Add real-time web search capabilities (e.g., Tavily or DuckDuckGo) to supplement local data when the user asks about recent events.
