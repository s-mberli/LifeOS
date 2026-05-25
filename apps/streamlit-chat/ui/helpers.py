"""
LifeOS UI helpers.

Pure-Python utility functions — NO streamlit imports.
All functions are safe to call from outside a Streamlit execution context,
making them straightforward to unit-test.
"""

import sqlite3
import sys
from pathlib import Path
from typing import Optional

import yaml

# ── Path constants ────────────────────────────────────────────────────────────
# apps/streamlit-chat/ui/helpers.py  → resolve 3 levels up for project root
ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH: Path = ROOT / "indexes" / "lifeos.db"

# Ensure scripts/ is on the path so we can import project scripts.
_SCRIPTS_DIR = str(ROOT)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


# ── Expert helpers ────────────────────────────────────────────────────────────

def get_existing_experts() -> list[dict]:
    """Return a list of expert dicts found under data/experts/.

    Each dict has the keys:
      - ``slug``         : directory name (e.g. ``"expert--ali-abdaal"``)
      - ``display_name`` : human-readable title (e.g. ``"Ali Abdaal"``)

    Only directories that contain a ``profile.md`` file are included.
    """
    experts_dir = ROOT / "data" / "experts"
    experts: list[dict] = []
    if not experts_dir.exists():
        return experts

    for d in experts_dir.iterdir():
        if d.is_dir() and (d / "profile.md").exists():
            display_name = (
                d.name.replace("expert--", "").replace("-", " ").title()
            )
            experts.append({"slug": d.name, "display_name": display_name})

    return experts


def get_all_insight_files() -> list[dict]:
    """Return metadata for all insight notes in the knowledge base.

    Returns:
        List of dicts with keys ``title`` and ``path`` (relative to ROOT).
    """
    knowledge_dir = ROOT / "data" / "knowledge"
    private_dir = ROOT / "data" / "private"
    
    files = []
    if knowledge_dir.exists():
        files.extend(list(knowledge_dir.rglob("*.md")))
    if private_dir.exists():
        files.extend(list(private_dir.rglob("*.md")))
        
    results = []
    for fpath in files:
        if "raw" in fpath.parts:
            continue
        try:
            fm = read_insight_frontmatter(fpath)
            if fm.get("type") == "insight_note":
                title = fm.get("title", fpath.stem)
                rel_path = fpath.relative_to(ROOT)
                results.append({"title": title, "path": str(rel_path)})
        except Exception:
            continue
    return results


# ── Frontmatter parsing ───────────────────────────────────────────────────────

def read_insight_frontmatter(file_path: Path) -> dict:
    """Parse YAML front-matter from a Markdown file and return it as a dict.

    Uses ``yaml.safe_load`` — never manual string splitting — so structured
    values (lists, booleans, etc.) are returned with their correct types.

    Args:
        file_path: Absolute path to a Markdown file.

    Returns:
        A dict of front-matter keys/values, or an empty dict if the file
        has no front-matter or it cannot be parsed.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        return {}

    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    fm_str = parts[1]
    try:
        parsed = yaml.safe_load(fm_str)
        return parsed if isinstance(parsed, dict) else {}
    except yaml.YAMLError:
        return {}


# ── Full-text search ──────────────────────────────────────────────────────────

def fts_search(
    query: str,
    limit: int = 5,
    allowed_paths: Optional[set] = None,
    require_insight_note: bool = False,
) -> list[tuple]:
    """Run a full-text search against the SQLite FTS5 index.

    Args:
        query:               Search query string.
        limit:               Maximum number of results to return.
        allowed_paths:       When provided, only results whose ``path``
                             column is in this set are included.
        require_insight_note: When ``True``, only rows whose path starts
                              with ``data/knowledge/`` or ``data/private/`` are included.

    Returns:
        A list of ``(title, path, snippet, score)`` tuples ordered by
        relevance (best first).  Returns an empty list if the database
        does not exist or the query fails.
    """
    if not DB_PATH.exists():
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        def run_fts_query(q_str: str) -> list[tuple]:
            cursor.execute(
                """
                SELECT path, title, snippet(search_index, 2, '**', '**', '...', 64),
                       bm25(search_index)
                FROM search_index
                WHERE content MATCH ?
                ORDER BY bm25(search_index)
                LIMIT 50
                """,
                (q_str,),
            )
            return cursor.fetchall()

        rows = []
        try:
            rows = run_fts_query(query)
        except sqlite3.OperationalError:
            pass

        if not rows:
            import re
            words = re.findall(r"\b\w+\b", query.lower())
            stopwords = {
                "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
                "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
                "but", "by", "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt",
                "doing", "dont", "down", "during", "each", "few", "for", "from", "further", "had", "hadnt",
                "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here",
                "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im",
                "ive", "if", "in", "into", "is", "isnt", "it", "its", "itself", "lets", "me", "more", "most",
                "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
                "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shant", "she", "shed",
                "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the",
                "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd",
                "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until",
                "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "werent", "what", "whats",
                "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys",
                "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours",
                "yourself", "yourselves"
            }
            tokens = [w for w in words if w not in stopwords]
            if tokens:
                and_query = " AND ".join(tokens)
                try:
                    rows = run_fts_query(and_query)
                except sqlite3.OperationalError:
                    pass

                if not rows:
                    or_query = " OR ".join(tokens)
                    try:
                        rows = run_fts_query(or_query)
                    except sqlite3.OperationalError:
                        pass

        results: list[tuple] = []
        for path, title, snippet, score in rows:
            if require_insight_note and not (path.startswith("data/knowledge/") or path.startswith("data/private/")):
                continue
            if allowed_paths is not None and path not in allowed_paths:
                continue

            results.append((title, path, snippet, score))
            if len(results) >= limit:
                break

        conn.close()
        return results

    except Exception as exc:  # pragma: no cover
        print(f"[helpers] fts_search error: {exc}")
        return []


# ── Search index rebuild ──────────────────────────────────────────────────────

def rebuild_search_index() -> dict:
    """Rebuild the FTS search index by calling the project's build script.

    Returns:
        The result dict returned by ``build_fts_index.build_index()``, which
        includes keys such as ``indexed``, ``skipped``, and optionally
        ``error``.
    """
    from src.core import build_fts_index  # noqa: PLC0415 – imported here to keep module-level imports clean

    return build_fts_index.build_index()


# ── LLM interaction ───────────────────────────────────────────────────────────

def ask_llm_chat(
    system_prompt: str,
    user_prompt: str,
    history: Optional[list] = None,
) -> str:
    """Call the project's LLM client and return the response as a string.

    Constructs a ``messages`` list with the system prompt, any provided
    conversation history, and the current user prompt, then delegates to
    ``llm_client.call_llm``.

    Args:
        system_prompt: The system-level instruction for the model.
        user_prompt:   The user's current message / question.
        history:       Optional list of prior ``{"role": …, "content": …}``
                       dicts to include as conversation context.

    Returns:
        The model's response text, or an ``"[LLM Error] …"`` string on
        failure.
    """
    try:
        from src.core.llm_client import call_llm  # noqa: PLC0415

        messages: list[dict] = [{"role": "system", "content": system_prompt}]

        if history:
            for msg in history:
                if msg.get("role") in ("user", "assistant"):
                    messages.append(msg)

        messages.append({"role": "user", "content": user_prompt})

        result = call_llm(messages=messages, model_type="smart", json_mode=False)
        return result[0] if isinstance(result, tuple) else result

    except Exception as exc:  # pragma: no cover
        return f"[LLM Error] {exc}"


# ── Auto-router ───────────────────────────────────────────────────────────────

def auto_route_prompt(prompt: str) -> dict:
    """Route a user prompt to the appropriate domain via the auto-router.

    Args:
        prompt: The raw user input string.

    Returns:
        A routing decision dict as returned by ``auto_router.route_input``.
        Falls back to ``{"domain": "general", "error": str(exc)}`` on failure.
    """
    try:
        from src.core.classify_input import route_input  # noqa: PLC0415

        return route_input(prompt)
    except Exception as exc:  # pragma: no cover
        return {"domain": "general", "error": str(exc)}


def construct_chat_prompts(
    target_expert: Optional[dict],
    prompt: str,
    selected_scopes: list,
    options_map: dict,
    fts_results: list[tuple],
    root_dir: Path,
) -> tuple[str, str]:
    """Build the system_prompt and user_prompt separating Hot vs Vault memory.

    Tier 1 (Hot Memory) -> system_prompt (Expert profile, playbook, principles).
    Tier 2 (Vault Memory) -> user_prompt (Expert evidence, selected files, FTS results).
    """
    # ── Hot Memory: Expert Persona/Playbook/Principles ────────────────────────
    expert_instructions = []
    if target_expert:
        slug = target_expert["slug"]
        for doc in ("profile.md", "playbook.md", "principles.md"):
            doc_path = root_dir / "data" / "experts" / slug / doc
            if doc_path.exists():
                try:
                    note_content = doc_path.read_text(encoding="utf-8")[:10000]
                    expert_instructions.append(
                        f"=== Expert {doc.split('.')[0].upper()} ===\n"
                        f"{note_content}"
                    )
                except Exception:
                    pass

    if target_expert:
        system_prompt = (
            f"You are LifeOS operating as the expert: {target_expert['display_name']}.\n\n"
        )
        if expert_instructions:
            system_prompt += (
                "Adopt the persona, values, and guidelines defined in your expert profile:\n"
                + "\n\n".join(expert_instructions) + "\n\n"
            )
    else:
        system_prompt = (
            "You are LifeOS, a local-first personal AI operating system."
        )

    system_prompt += (
        "\n\nYour job:\n"
        "- Answer the user's question using the retrieved notes as context.\n"
        "- Be concise and practical.\n"
        "- Do NOT invent facts.\n"
        "- Adopt the style, tone, and directives of the active expert profile (if loaded).\n"
        "- If the context contains a summary rather than the full raw transcript, answer based on the summary. Do NOT ask the user to provide the link or transcript to you."
    )

    # ── Vault Memory: Facts and Context ───────────────────────────────────────
    context_blocks: list[str] = []
    loaded_paths: set[str] = set()

    # 1. Load active expert evidence (Tier 2 Vault, NOT Hot memory instructions)
    if target_expert:
        slug = target_expert["slug"]
        evidence_path = root_dir / "data" / "experts" / slug / "evidence.md"
        if evidence_path.exists():
            try:
                note_content = evidence_path.read_text(encoding="utf-8")[:15000]
                context_blocks.append(
                    f"### Expert Core Profile (evidence.md)\n"
                    f"Path: data/experts/{slug}/evidence.md\n\n"
                    f"{note_content}"
                )
                loaded_paths.add(f"data/experts/{slug}/evidence.md")
            except Exception:
                pass

    # 2. Load explicitly selected file scopes
    if selected_scopes:
        for scope in selected_scopes:
            item = options_map.get(scope)
            if item and item["type"] == "file":
                file_path = item["data"]["path"]
                if file_path not in loaded_paths:
                    full_path = root_dir / file_path
                    if full_path.exists():
                        try:
                            note_content = full_path.read_text(encoding="utf-8")[:15000]
                            context_blocks.append(
                                f"### Selected Note: {item['data'].get('title', file_path)}\n"
                                f"Path: {file_path}\n\n"
                                f"{note_content}"
                            )
                            loaded_paths.add(file_path)
                        except Exception:
                            pass

    # 3. Append FTS results
    for title, path, snippet, _ in fts_results:
        if path not in loaded_paths:
            full_path = root_dir / path
            if full_path.exists():
                try:
                    note_content = full_path.read_text(encoding="utf-8")[:15000]
                except Exception:
                    note_content = snippet
            else:
                note_content = snippet
            context_blocks.append(
                f"### {title}\nPath: {path}\n\n{note_content}"
            )
            loaded_paths.add(path)

    retrieved_context = (
        "\n\n---\n\n".join(context_blocks)
        if context_blocks
        else "No relevant notes found in knowledge base."
    )

    user_prompt = (
        f"Question: {prompt}\n\n"
        f"Relevant Notes from Knowledge Base:\n{retrieved_context}\n\n"
        "Please answer based on the above context."
    )

    return system_prompt, user_prompt


def execute_agent_search_loop(
    system_prompt: str,
    user_prompt: str,
    history: Optional[list] = None,
    allowed_paths: Optional[set] = None,
    max_turns: int = 3,
) -> tuple[str, list[tuple[str, str]]]:
    """Execute an agentic loop allowing the LLM to call the FTS search tool.

    Uses a robust, provider-agnostic XML format:
    <call:fts_search>search query</call:fts_search>

    Args:
        system_prompt: The initial system prompt.
        user_prompt:   The user prompt / question.
        history:       Conversation history.
        allowed_paths: Optional filter paths for FTS search.
        max_turns:     Max number of tool call iterations.

    Returns:
        A tuple of (final_response_text, list_of_tool_calls_made).
        Each tool call is a tuple of (search_query, formatted_results).
    """
    import re

    # Inject tool-use instructions into the system prompt
    tool_instructions = (
        "\n\n=== Tool Access ===\n"
        "You have access to a search tool: fts_search.\n"
        "If you need to query the database/vault for specific facts, insights, or details "
        "not present in your active context, output an XML tag exactly like this:\n"
        "<call:fts_search>your query here</call:fts_search>\n"
        "Do not explain the call, do not output any other text when calling a tool.\n"
        "After you output the tag, the system will execute it and provide the results.\n"
    )
    augmented_system = system_prompt + tool_instructions
    
    current_history = list(history) if history else []
    calls_made = []

    for _ in range(max_turns):
        response = ask_llm_chat(augmented_system, user_prompt, history=current_history)
        if not response:
            break

        # Check for tool call pattern
        match = re.search(r"<call:fts_search>(.*?)</call:fts_search>", response, re.DOTALL)
        if not match:
            # No tool call; return this as final response
            return response, calls_made

        # We found a tool call! Extract query and execute it
        query = match.group(1).strip()
        
        # Execute FTS search
        results = fts_search(query, limit=3, allowed_paths=allowed_paths)
        
        # Format results
        if results:
            formatted_list = []
            for r_title, r_path, r_snippet, _ in results:
                formatted_list.append(f"{r_title} ({r_path}):\n{r_snippet}")
            results_str = "\n\n".join(formatted_list)
        else:
            results_str = "No results found in knowledge base."

        # Record the call
        calls_made.append((query, results_str))

        # Append assistant's tool invocation and user's tool response to history
        current_history.append({"role": "assistant", "content": response})
        current_history.append({
            "role": "user",
            "content": (
                f"<response:fts_search>\n{results_str}\n</response:fts_search>\n"
                f"Use the above search results to complete your answer."
            )
        })

    # Fallback/exhausted turns: get final answer
    final_response = ask_llm_chat(augmented_system, user_prompt, history=current_history)
    return final_response, calls_made


