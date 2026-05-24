"""
LifeOS UI chat interface.

Renders the main chat panel: the scrollable message history, the expert
context pill selector, the chat input bar, and the RAG-backed response loop
with source attribution.
"""

import traceback

import streamlit as st

from .helpers import (
    ROOT,
    ask_llm_chat,
    auto_route_prompt,
    fts_search,
    get_existing_experts,
    get_all_insight_files,
    read_insight_frontmatter,
)


def render_chat_interface() -> None:
    """Render the full chat panel including message history and input bar.

    This is the single public entry-point for the chat module.  Wraps all
    rendering in a try/except so that an error in the chat loop never causes
    an unhandled exception at the app level.
    """
    try:
        _render_chat_body()
    except Exception as exc:
        import os

        st.error(f"[Chat] Unexpected error: {exc}")
        if os.environ.get("DEBUG"):
            st.code(traceback.format_exc(), language="python")


def _render_chat_body() -> None:
    """Inner implementation of the chat interface (no error boundary here)."""
    st.title("🧭 LifeOS")
    st.caption("Local-first personal expert network")

    # ── Session state initialisation ────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── Message history ──────────────────────────────────────────────────────
    messages_container = st.container()
    for msg in st.session_state.messages:
        messages_container.chat_message(msg["role"]).write(msg["content"])

    # ── Context Selection ────────────────────────────────────────────────────
    existing_experts = get_existing_experts()
    all_files = get_all_insight_files()
    
    options_map: dict = {}
    for e in existing_experts:
        options_map[f"Expert: {e['display_name']}"] = {"type": "expert", "data": e}
        
    for f in all_files:
        options_map[f"File: {f['title']}"] = {"type": "file", "data": f}

    selected_scopes = st.multiselect(
        "Active Context (Leave empty to search entire library)",
        options=list(options_map.keys()),
        default=[],
        placeholder="Select Experts or Files...",
        label_visibility="collapsed",
    )

    # ── Chat input ───────────────────────────────────────────────────────────
    prompt = st.chat_input("Ask anything or use @ to call an expert")
    if not prompt:
        return

    # 1. Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages_container.chat_message("user").write(prompt)

    # 2. Resolve @mention overrides
    target_expert_dict_from_at_mention = None
    for e in existing_experts:
        slug_without_prefix = e["slug"].replace("expert--", "")
        if (
            f"@{e['display_name'].lower()}" in prompt.lower()
            or f"@{slug_without_prefix}" in prompt.lower()
        ):
            target_expert_dict_from_at_mention = e
            st.toast(f"Routed to {e['display_name']}")
            break

    # 3. Build the set of allowed document paths for FTS filtering
    allowed_paths: set = set()
    require_insight_note = False

    if not selected_scopes and not target_expert_dict_from_at_mention:
        # General Library mode
        require_insight_note = True
    else:
        # Add paths from multiselect
        for scope in selected_scopes:
            item = options_map[scope]
            if item["type"] == "expert":
                slug = item["data"]["slug"]
                sources_dir = ROOT / "data" / "experts" / slug / "sources"
                if sources_dir.exists():
                    for ref_file in sources_dir.glob("*-ref.md"):
                        fm = read_insight_frontmatter(ref_file)
                        if fm.get("source_path"):
                            allowed_paths.add(fm["source_path"])
                for doc in ("profile.md", "playbook.md", "principles.md", "evidence.md"):
                    allowed_paths.add(f"data/experts/{slug}/{doc}")
            elif item["type"] == "file":
                allowed_paths.add(item["data"]["path"])
                
        # Handle @mention
        if target_expert_dict_from_at_mention:
            slug = target_expert_dict_from_at_mention["slug"]
            sources_dir = ROOT / "data" / "experts" / slug / "sources"
            if sources_dir.exists():
                for ref_file in sources_dir.glob("*-ref.md"):
                    fm = read_insight_frontmatter(ref_file)
                    if fm.get("source_path"):
                        allowed_paths.add(fm["source_path"])
            for doc in ("profile.md", "playbook.md", "principles.md", "evidence.md"):
                allowed_paths.add(f"data/experts/{slug}/{doc}")

    # 4. Search, synthesise, and stream the response
    with messages_container.chat_message("assistant"):
        with st.spinner("Searching and synthesizing..."):

            # Auto-route for domain classification (also updates memory log)
            decision = auto_route_prompt(prompt)
            try:
                from auto_capture import capture_input  # noqa: PLC0415

                capture_input(prompt, decision)
            except Exception:
                pass  # auto_capture is best-effort

            # FTS retrieval
            results = fts_search(
                prompt,
                limit=5,
                allowed_paths=allowed_paths if allowed_paths else None,
                require_insight_note=require_insight_note,
            )

            # Build context blocks from retrieved notes
            context_blocks: list[str] = []
            for title, path, snippet, _ in results:
                full_path = ROOT / path
                if full_path.exists():
                    note_content = full_path.read_text(encoding="utf-8")[:15000]
                else:
                    note_content = snippet
                context_blocks.append(
                    f"### {title}\nPath: {path}\n\n{note_content}"
                )

            retrieved_context = (
                "\n\n---\n\n".join(context_blocks)
                if context_blocks
                else "No relevant notes found in knowledge base."
            )

            # Build system + user prompts
            target_expert = target_expert_dict_from_at_mention
            if not target_expert and selected_scopes:
                for scope in selected_scopes:
                    item = options_map[scope]
                    if item["type"] == "expert":
                        target_expert = item["data"]
                        break

            if target_expert:
                system_prompt = (
                    f"You are LifeOS operating as "
                    f"{target_expert['display_name']}."
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
                "- If the context contains a summary rather than the full raw transcript, answer based on the summary. Do NOT ask the user to provide the link or transcript to you."
            )

            user_prompt = (
                f"Question: {prompt}\n\n"
                f"Relevant Notes from Knowledge Base:\n{retrieved_context}\n\n"
                "Please answer based on the above context."
            )

            # Provide the last 5 prior messages as conversation history
            history = st.session_state.get("messages", [])[-6:-1]

            answer_text = ask_llm_chat(system_prompt, user_prompt, history=history)

            if answer_text and not answer_text.startswith("[LLM Error]"):
                st.write(answer_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer_text}
                )

                # Source attribution popover
                if results:
                    with st.popover(f"📚 Sources Referenced ({len(results)})"):
                        for title, path, snippet, score in results:
                            display_score = abs(score) * 1000
                            st.markdown(
                                f"**{title}** (`{path}`) — Score: `{display_score:.2f}`"
                            )
            else:
                err_msg = answer_text if answer_text else "Unknown LLM error."
                st.error(err_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err_msg}
                )
