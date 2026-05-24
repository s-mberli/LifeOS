# LifeOS Agents & Architecture

## Mission
LifeOS is a routed knowledge operating system designed to turn resources into decisions and actions. It acts as a personal AI platform, reducing idea overload by ensuring every interaction results in a practical next step.

## User Layer vs System Layer
- **System Layer**: Instructions, logic, and configurations (`modes/`, `scripts/`, `config/`, `templates/`).
- **User Layer**: Markus's personal knowledge, notes, and outputs (`data/`, `outputs/`). The AI reads this but must be careful when modifying it.

## Source-of-Truth Order
When answering questions or making plans, prioritize context in this order:
1. `data/private/` and `data/business/` (Markus's actual current state and goals)
2. `config/profile.yml` (Core preferences and domains)
3. `data/knowledge/` (Saved resources and concepts)
4. External web search
5. AI's pre-trained knowledge

## Consent Edges
The AI must ask for explicit human approval before:
- Publishing or sending data externally (social media, email).
- Making paid API calls.
- Deleting files.
- Silently overwriting personal/user-layer files (always append or propose changes).

## Routing Rules
1. Every input is evaluated by the Router.
2. The Router determines the input type, primary domain, and primary mode.
3. The Router outputs its decision explicitly so Markus can correct it.
4. The system executes the selected mode with the relevant knowledge folders attached.

### Mode Directory
| Mode | Domain | Trigger Topics |
|------|--------|----------------|
| `research-resource` | AI Platform | AI, LLM, RAG, agents, embeddings, tools |
| `ai-builder` | AI Platform | Building AI projects, code, pipelines |
| `flow-temple-operator` | Flow Temple | TCM, moxa, yoga content, massage, business |
| `moxsensei-operator` | Flow Temple | MOXSensei brand specifically |
| `career-brand` | Career | CV, LinkedIn, portfolio, interviews |
| `creator-wisdom` | Creator Wisdom | Creators, channels, transcripts, multi-source profiles |
| `life-kompass` | Life Kompass | Focus, routines, emotions, reflections, family |
| `body-practice` | Body Practice | Training, strength, calisthenics, yoga skills, cut, mobility, recovery |

## Writeback Rules
1. Do not duplicate resources. Store a resource in one canonical location and connect it to multiple domains via YAML metadata (`related_modes`, `tags`).
2. Always suggest saving useful interactions.
3. Use templates when creating new files (e.g., `resource-note.md`).
4. Creator profiles under `creator-profiles/` are append-only. Never overwrite existing sections in `profile.md`, only add new evidence.

## Architecture (current)

### scripts/core/ - Business logic modules
- `frontmatter.py` - YAML frontmatter read/write. ALWAYS use this, never manual string parsing.
- `youtube.py` - All yt-dlp and YouTube transcript operations
- `web.py` - Web page fetching and metadata extraction
- `experts.py` - Expert profile management, persona synthesis, insight assignment
- `ingest.py` - Main ingestion pipeline entry point

### apps/streamlit-chat/ui/ - Streamlit UI modules
- `helpers.py` - Pure Python helpers (no st.* calls, safe to unit-test)
- `modals.py` - @st.dialog modal definitions
- `sidebar.py` - Sidebar rendering and URL form
- `chat.py` - Chat loop, expert routing, source attribution

### Key coding patterns
- **YAML**: Always use `from core.frontmatter import read_fm, write_fm, update_fm`
- **YouTube**: Always use `from core.youtube import ...` (not channel_ingest.py directly)
- **LLM**: `call_llm(prompt='...')` or `call_llm(messages=[...])`
- **Domain mapping**: Edit `config/domain_map.yaml` (not hardcoded)
- **No patching**: Never patch app.py with string replacement scripts
