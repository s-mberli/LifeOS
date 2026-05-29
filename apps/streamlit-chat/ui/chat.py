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
    auto_route_prompt,
    get_existing_experts,
    get_all_insight_files,
    read_insight_frontmatter,
)
from core.search_knowledge import fts_search


@st.cache_data(ttl=60)
def cached_get_all_insight_files() -> list[dict]:
    return get_all_insight_files()



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
    if "saved_msg_indices" not in st.session_state:
        st.session_state.saved_msg_indices = set()

    # Load experts early to have voice map available
    existing_experts = get_existing_experts()
    expert_voice_map = {e["slug"]: e.get("elevenlabs_voice_id") for e in existing_experts}

    # ── Message history ──────────────────────────────────────────────────────
    messages_container = st.container()
    for idx, msg in enumerate(st.session_state.messages):
        with messages_container.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant" and not msg["content"].startswith("[LLM Error]"):
                # Source attribution popover
                if msg.get("sources"):
                    with st.popover(f"📚 Sources Referenced ({len(msg['sources'])})"):
                        for title, path, snippet, score in msg["sources"]:
                            display_score = abs(score) * 1000
                            st.markdown(
                                f"**{title}** (`{path}`) — Score: `{display_score:.2f}`"
                            )
                
                action_cols = st.columns([1, 1, 2])
                with action_cols[0]:
                    if idx in st.session_state.saved_msg_indices:
                        st.caption("✅ Saved to Library")
                    else:
                        user_prompt = msg.get("user_prompt", "")
                        if st.button("💾 Save Insight", key=f"save_insight_{idx}"):
                            from core.chat_persistence import save_message_as_insight
                            success, file_path = save_message_as_insight(
                                user_prompt=user_prompt,
                                assistant_response=msg["content"],
                                expert_slug=msg.get("expert_slug"),
                                expert_name=msg.get("expert_name"),
                            )
                            if success:
                                st.session_state.saved_msg_indices.add(idx)
                                cached_get_all_insight_files.clear()
                                st.success("Saved as insight note!")
                                st.rerun()
                            else:
                                st.error("Failed to save insight.")
                with action_cols[1]:
                    if st.button("🔊 Read Aloud", key=f"tts_{idx}"):
                        try:
                            from core.tts import generate_speech
                            expert_slug = msg.get("expert_slug")
                            voice_id = None
                            if expert_slug:
                                voice_id = expert_voice_map.get(expert_slug)
                            
                            with st.spinner("Generating speech..."):
                                audio_bytes = generate_speech(msg["content"], voice_id=voice_id)
                            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                        except Exception as tts_exc:
                            st.error(f"TTS Failed: {tts_exc}")
    all_files = cached_get_all_insight_files()
    
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
    # 2. Resolve @mention overrides
    from core.chat_context import extract_mention
    target_expert_dict_from_at_mention = extract_mention(prompt, existing_experts)
    if target_expert_dict_from_at_mention:
        st.toast(f"Routed to {target_expert_dict_from_at_mention['display_name']}")

    # 3. Build the set of allowed document paths for FTS filtering
    allowed_paths: set = set()
    require_insight_note = False

    def _add_expert_paths(expert_slug: str, paths_set: set) -> None:
        sources_dir = ROOT / "data" / "experts" / expert_slug / "sources"
        if sources_dir.exists():
            for ref_file in sources_dir.glob("*-ref.md"):
                fm = read_insight_frontmatter(ref_file)
                src_path = fm.get("source_path")
                if src_path:
                    # Handle if cleanup_data.py renamed the file
                    if "tmp" in src_path and not (ROOT / src_path).exists():
                        import re
                        title = fm.get("source_title", "")
                        safe_title = re.sub(r"[^a-z0-9\-]", "", title.lower().replace(" ", "-"))
                        possible_path = f"data/knowledge/ai-resources/{safe_title}.md"
                        if (ROOT / possible_path).exists():
                            src_path = possible_path
                    paths_set.add(src_path)
                    
                    # Also allow searching the raw transcript file
                    try:
                        real_p = ROOT / src_path
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

    if not selected_scopes and not target_expert_dict_from_at_mention:
        # General Library mode
        require_insight_note = True
    else:
        # Add paths from multiselect
        for scope in selected_scopes:
            item = options_map[scope]
            if item["type"] == "expert":
                _add_expert_paths(item["data"]["slug"], allowed_paths)
            elif item["type"] == "file":
                allowed_paths.add(item["data"]["path"])
                
        # Handle @mention
        if target_expert_dict_from_at_mention:
            _add_expert_paths(target_expert_dict_from_at_mention["slug"], allowed_paths)

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

            # Determine active target expert
            target_expert = target_expert_dict_from_at_mention
            if not target_expert and selected_scopes:
                for scope in selected_scopes:
                    item = options_map[scope]
                    if item["type"] == "expert":
                        target_expert = item["data"]
                        break

            # FTS retrieval
            results = fts_search(
                prompt,
                limit=5,
                allowed_paths=allowed_paths if allowed_paths else None,
                require_insight_note=require_insight_note,
            )

            from .helpers import construct_chat_prompts
            system_prompt, user_prompt = construct_chat_prompts(
                target_expert=target_expert,
                prompt=prompt,
                selected_scopes=selected_scopes,
                options_map=options_map,
                fts_results=results,
                root_dir=ROOT,
            )

            # Provide the last 5 prior messages as conversation history
            history = st.session_state.get("messages", [])[-6:-1]

            from core.chat_context import execute_agent_search_loop
            answer_text, calls_made = execute_agent_search_loop(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                fts_search_fn=fts_search,
                history=history,
                allowed_paths=allowed_paths if allowed_paths else None,
            )

            # Show visual indicators of agent searches
            if calls_made:
                for q, _ in calls_made:
                    st.toast(f"🔍 Agent searched: '{q}'")

            if answer_text and not answer_text.startswith("[LLM Error]"):
                st.write(answer_text)
                assistant_msg = {
                    "role": "assistant",
                    "content": answer_text,
                    "user_prompt": prompt
                }
                if target_expert:
                    assistant_msg["expert_slug"] = target_expert["slug"]
                    assistant_msg["expert_name"] = target_expert["display_name"]
                if results:
                    assistant_msg["sources"] = results
                st.session_state.messages.append(assistant_msg)

                # Auto-log to daily chat logs
                try:
                    from core.chat_persistence import append_to_daily_chat_log
                    append_to_daily_chat_log(
                        user_prompt=prompt,
                        assistant_response=answer_text,
                        expert_slug=target_expert["slug"] if target_expert else None,
                    )
                except Exception as log_exc:
                    print(f"Auto-log failed: {log_exc}")

                st.rerun()
            else:
                err_msg = answer_text if answer_text else "Unknown LLM error."
                st.error(err_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": err_msg}
                )
                st.rerun()
