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
        "- Be comprehensive and detailed. Explore the nuances of the topic and provide practical examples or context, ensuring your response is thorough (aim for depth).\n"
        "- When an insight contains a core principle, clearly explain the principle first so the user understands the foundation. Then, provide highly CONCRETE and ACTIONABLE advice on how they can practically apply that principle to their life.\n"
        "- Use clear markdown formatting. Break up large walls of text using bullet points, bold text for key concepts, and short paragraphs to make your answer highly readable and scannable.\n"
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


# ── Compatibility Re-exports for Tests ───────────────────────────────────────
from src.core.search_knowledge import fts_search  # noqa: F401
from src.core.chat_context import (  # noqa: F401
    execute_agent_search_loop,
    ask_llm_chat,
)



