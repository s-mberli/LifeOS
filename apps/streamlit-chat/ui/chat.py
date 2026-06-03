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

    if not st.session_state.messages:
        with messages_container:
            st.markdown(
                """
                <div style="padding: 1.25rem; border-radius: 8px; background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255, 255, 255, 0.05); margin: 1rem 0 2rem 0;">
                    <div style="display: flex; flex-direction: column; gap: 0.5rem; text-align: left;">
                        <span style="font-size: 0.9rem; color: #e2e8f0; font-weight: 500; margin-bottom: 0.25rem;">💡 Onboarding Hints:</span>
                        <span style="font-size: 0.85rem; color: #94a3b8;">• Ask any question to query your entire knowledge library.</span>
                        <span style="font-size: 0.85rem; color: #94a3b8;">• Type <b>@</b> in the input to summon a specific expert.</span>
                        <span style="font-size: 0.85rem; color: #94a3b8;">• Select specific files or experts in the active context below.</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    for idx, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        with messages_container.chat_message(role):
            st.markdown(f'<span class="chat-role-{role}"></span>', unsafe_allow_html=True)
            st.write(msg["content"])
            if msg["role"] == "assistant" and not msg["content"].startswith("[LLM Error]"):
                # Source attribution popover
                if msg.get("sources"):
                    with st.popover(f"📚 Sources Referenced ({len(msg['sources'])})"):
                        for i, (title, path, snippet, score) in enumerate(msg["sources"], 1):
                            display_score = abs(score) * 1000
                            st.markdown(
                                f"**[{i}] {title}** (`{path}`) — Score: `{display_score:.2f}`"
                            )
                
                action_cols = st.columns([1.5, 1.2, 4.3])
                with action_cols[0]:
                    if idx in st.session_state.saved_msg_indices:
                        st.caption("✅ Saved to Library")
                    else:
                        user_prompt = msg.get("user_prompt", "")
                        if st.button("✨ Save Insight", key=f"save_insight_{idx}"):
                            from core.chat_persistence import save_message_as_insight
                            success, file_path = save_message_as_insight(
                                user_prompt=user_prompt,
                                assistant_response=msg["content"],
                                expert_slugs=msg.get("expert_slugs") or ([msg.get("expert_slug")] if msg.get("expert_slug") else None),
                                expert_names=msg.get("expert_names") or ([msg.get("expert_name")] if msg.get("expert_name") else None),
                            )
                            if success:
                                st.session_state.saved_msg_indices.add(idx)
                                cached_get_all_insight_files.clear()
                                st.success("Saved as insight note!")
                                st.rerun()
                            else:
                                st.error("Failed to save insight.")
                with action_cols[1]:
                    if st.button("🎧 Listen", key=f"tts_{idx}"):
                        try:
                            from core.tts import generate_speech
                            expert_slugs = msg.get("expert_slugs")
                            legacy_slug = msg.get("expert_slug")
                            voice_id = None
                            if expert_slugs:
                                voice_id = expert_voice_map.get(expert_slugs[0])
                            elif legacy_slug:
                                voice_id = expert_voice_map.get(legacy_slug)
                            
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

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_scopes = st.multiselect(
            "Active Context (Leave empty to search entire library)",
            options=list(options_map.keys()),
            default=[],
            placeholder="Select Experts or Files...",
            help="Select specific experts or files to narrow down the knowledge base. Leave empty to search everything.",
            label_visibility="collapsed",
        )
    with col2:
        response_length = st.selectbox(
            "Response Length",
            options=["Concise", "Standard", "Detailed"],
            index=1,
            help="Choose how detailed the synthesized response should be.",
            label_visibility="collapsed"
        )

    # ── Chat input ───────────────────────────────────────────────────────────
    prompt = st.chat_input("Ask anything or use @ to summon an expert...")
    if not prompt:
        return

    # 1. Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with messages_container.chat_message("user"):
        st.markdown('<span class="chat-role-user"></span>', unsafe_allow_html=True)
        st.write(prompt)

    # 2. Resolve @mention overrides
    from core.chat_context import extract_mention
    target_expert_dict_from_at_mention = extract_mention(prompt, existing_experts)
    if target_expert_dict_from_at_mention:
        st.toast(f"Routed to {target_expert_dict_from_at_mention['display_name']}")

    # 3. Build the set of allowed document paths for FTS filtering
    from .helpers import build_allowed_paths
    allowed_paths, require_insight_note = build_allowed_paths(
        selected_scopes=selected_scopes,
        target_expert_dict=target_expert_dict_from_at_mention,
        options_map=options_map,
        root_dir=ROOT,
    )

    # 4. Search, synthesise, and stream the response
    with messages_container.chat_message("assistant"):
        st.markdown('<span class="chat-role-assistant"></span>', unsafe_allow_html=True)
        with st.spinner("Searching and synthesizing..."):

            # Auto-route for domain classification (also updates memory log)
            decision = auto_route_prompt(prompt)
            try:
                from auto_capture import capture_input  # noqa: PLC0415

                capture_input(prompt, decision)
            except Exception:
                pass  # auto_capture is best-effort

            # Determine active target experts
            target_experts = []
            if target_expert_dict_from_at_mention:
                target_experts.append(target_expert_dict_from_at_mention)
            elif selected_scopes:
                for scope in selected_scopes:
                    item = options_map[scope]
                    if item["type"] == "expert":
                        target_experts.append(item["data"])

            # FTS retrieval
            results = fts_search(
                prompt,
                limit=5,
                allowed_paths=allowed_paths if allowed_paths else None,
                require_insight_note=require_insight_note,
                include_private=True,
            )

            from .helpers import construct_chat_prompts
            system_prompt, user_prompt = construct_chat_prompts(
                target_experts=target_experts,
                prompt=prompt,
                selected_scopes=selected_scopes,
                options_map=options_map,
                fts_results=results,
                root_dir=ROOT,
                response_length=response_length,
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
                include_private=True,
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
                if target_experts:
                    assistant_msg["expert_slugs"] = [e["slug"] for e in target_experts]
                    assistant_msg["expert_names"] = [e["display_name"] for e in target_experts]
                if results:
                    assistant_msg["sources"] = results
                st.session_state.messages.append(assistant_msg)

                # Auto-log to daily chat logs
                try:
                    from core.chat_persistence import append_to_daily_chat_log
                    append_to_daily_chat_log(
                        user_prompt=prompt,
                        assistant_response=answer_text,
                        expert_slugs=[e["slug"] for e in target_experts] if target_experts else None,
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
