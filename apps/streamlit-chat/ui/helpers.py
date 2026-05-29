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


# ── User Memory Helpers ───────────────────────────────────────────────────────

def _get_db_conn():
    """Get a SQLite connection and ensure the user_memory table exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def get_user_memories(active_only: bool = False) -> list[dict]:
    """Fetch user manual memories from the SQLite DB."""
    if not DB_PATH.exists():
        return []
    try:
        conn = _get_db_conn()
        cursor = conn.cursor()
        if active_only:
            cursor.execute("SELECT * FROM user_memory WHERE is_active = 1 ORDER BY created_at DESC")
        else:
            cursor.execute("SELECT * FROM user_memory ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[helpers] Error fetching user memories: {e}")
        return []

def add_user_memory(title: str, content: str) -> bool:
    """Add a new user memory to the DB."""
    try:
        conn = _get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_memory (title, content, is_active) VALUES (?, ?, 1)",
            (title, content)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[helpers] Error adding user memory: {e}")
        return False

def toggle_user_memory(memory_id: int, is_active: bool) -> bool:
    """Toggle the active state of a user memory."""
    try:
        conn = _get_db_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_memory SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (1 if is_active else 0, memory_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[helpers] Error toggling user memory: {e}")
        return False

def delete_user_memory(memory_id: int) -> bool:
    """Delete a user memory from the DB."""
    try:
        conn = _get_db_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_memory WHERE id = ?", (memory_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[helpers] Error deleting user memory: {e}")
        return False


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
        profile_path = d / "profile.md"
        if d.is_dir() and profile_path.exists():
            display_name = (
                d.name.replace("expert--", "").replace("-", " ").title()
            )
            fm = read_insight_frontmatter(profile_path)
            voice_id = fm.get("elevenlabs_voice_id")
            experts.append({
                "slug": d.name, 
                "display_name": display_name,
                "elevenlabs_voice_id": voice_id
            })

    return experts


def get_all_insight_files() -> list[dict]:
    """Return metadata for all insight notes in the knowledge base.

    Returns:
        List of dicts with keys ``title`` and ``path`` (relative to ROOT).
    """
    knowledge_dir = ROOT / "data" / "knowledge"
    private_dir = ROOT / "data" / "private"
    inbox_dir = ROOT / "data" / "inbox"
    
    files = []
    if knowledge_dir.exists():
        files.extend(list(knowledge_dir.rglob("*.md")))
    if private_dir.exists():
        files.extend(list(private_dir.rglob("*.md")))
    if inbox_dir.exists():
        files.extend(list(inbox_dir.rglob("*.md")))
        
    results = []
    for fpath in files:
        if "raw" in fpath.parts:
            continue
        try:
            fm = read_insight_frontmatter(fpath)
            if fm.get("type") == "insight_note":
                title = fm.get("title", fpath.stem)
                rel_path = fpath.relative_to(ROOT)
                
                # Extract created_at for sorting, fallback to filesystem mtime
                created_at = fm.get("created_at")
                if not isinstance(created_at, str):
                    try:
                        created_at = str(fpath.stat().st_mtime)
                    except Exception:
                        created_at = ""
                        
                results.append({
                    "title": title,
                    "path": str(rel_path),
                    "created_at": created_at
                })
        except Exception:
            continue
            
    # Sort descending so newest files are at the top
    results.sort(key=lambda x: x["created_at"], reverse=True)
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
    response_length: str = "Standard",
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

    active_memories = get_user_memories(active_only=True)
    if active_memories:
        memory_blocks = []
        for mem in active_memories:
            memory_blocks.append(f"[{mem['title']}]\n{mem['content']}")
        system_prompt += "\n\n=== User Context & Preferences ===\n" + "\n\n".join(memory_blocks) + "\n\n"

    system_prompt += (
        "\n\nYour job:\n"
        "- Answer the user's question using the retrieved notes as context.\n"
        "- Be comprehensive and detailed. Explore the nuances of the topic and provide practical examples or context, ensuring your response is thorough (aim for depth).\n"
        "- When an insight contains a core principle, clearly explain the principle first so the user understands the foundation. Then, provide highly CONCRETE and ACTIONABLE advice on how they can practically apply that principle to their life.\n"
        "- Use clear markdown formatting. Break up large walls of text using bullet points, bold text for key concepts, and short paragraphs to make your answer highly readable and scannable.\n"
        "- **Cite your sources**: Always use inline citations (e.g., [1], [2]) referring to the specific notes/paths provided in the context so the user knows where each insight came from.\n"
        "- Do NOT invent facts.\n"
        "- Adopt the style, tone, and directives of the active expert profile (if loaded).\n"
        "- If the context contains a summary rather than the full raw transcript, answer based on the summary. Do NOT ask the user to provide the link or transcript to you."
    )

    if response_length == "Concise":
        system_prompt += "\n- Keep your response extremely concise. Aim for a short summary (1-2 paragraphs max)."
    elif response_length == "Detailed":
        system_prompt += "\n- Provide a highly detailed and comprehensive answer, exploring all nuances deeply."
    else:
        system_prompt += "\n- Provide a standard length response that balances detail and readability."

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

    length_reminder = ""
    if response_length == "Concise":
        length_reminder = "\n\nCRITICAL REQUIREMENT: Keep your response extremely concise. Give me a short summary (1-2 paragraphs maximum) regardless of prior message length."
    elif response_length == "Detailed":
        length_reminder = "\n\nCRITICAL REQUIREMENT: Provide a highly detailed and comprehensive answer."

    user_prompt = (
        f"Question: {prompt}\n\n"
        f"Relevant Notes from Knowledge Base:\n{retrieved_context}\n\n"
        f"Please answer based on the above context.{length_reminder}"
    )

    return system_prompt, user_prompt


# ── Compatibility Re-exports for Tests ───────────────────────────────────────
from src.core.search_knowledge import fts_search  # noqa: F401
from src.core.chat_context import (  # noqa: F401
    execute_agent_search_loop,
    ask_llm_chat,
)


def build_allowed_paths(
    selected_scopes: list, 
    target_expert_dict: Optional[dict], 
    options_map: dict, 
    root_dir: Path
) -> tuple[set, bool]:
    """
    Build the set of allowed document paths for FTS filtering based on selected scopes.
    Returns a tuple of (allowed_paths_set, require_insight_note_boolean).
    """
    allowed_paths: set = set()
    require_insight_note = False

    def _add_expert_paths(expert_slug: str, paths_set: set) -> None:
        sources_dir = root_dir / "data" / "experts" / expert_slug / "sources"
        if sources_dir.exists():
            for ref_file in sources_dir.glob("*-ref.md"):
                fm = read_insight_frontmatter(ref_file)
                src_path = fm.get("source_path")
                if src_path:
                    # Handle if cleanup_data.py renamed the file
                    if "tmp" in src_path and not (root_dir / src_path).exists():
                        import re
                        title = fm.get("source_title", "")
                        safe_title = re.sub(r"[^a-z0-9\-]", "", title.lower().replace(" ", "-"))
                        possible_path = f"data/knowledge/ai-resources/{safe_title}.md"
                        if (root_dir / possible_path).exists():
                            src_path = possible_path
                    paths_set.add(src_path)
                    
                    # Also allow searching the raw transcript file
                    try:
                        real_p = root_dir / src_path
                        if real_p.exists():
                            real_fm = read_insight_frontmatter(real_p)
                            t_path = real_fm.get("transcript_path", "")
                            if "data/knowledge" in str(t_path):
                                rel_path = str(t_path)[str(t_path).find("data/knowledge"):]
                                paths_set.add(rel_path)
                    except Exception:
                        pass

        for doc in ("profile.md", "playbook.md", "principles.md", "evidence.md"):
            paths_set.add(f"data/experts/{expert_slug}/{doc}")

    if not selected_scopes and not target_expert_dict:
        # General Library mode
        require_insight_note = True
    else:
        # Add paths from multiselect
        for scope in selected_scopes:
            item = options_map.get(scope)
            if item:
                if item["type"] == "expert":
                    _add_expert_paths(item["data"]["slug"], allowed_paths)
                elif item["type"] == "file":
                    allowed_paths.add(item["data"]["path"])
                
        # Handle @mention
        if target_expert_dict:
            _add_expert_paths(target_expert_dict["slug"], allowed_paths)

    return allowed_paths, require_insight_note
