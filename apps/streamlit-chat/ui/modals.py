import os
import re
import traceback
from pathlib import Path

import streamlit as st
import pandas as pd

from .helpers import (
    ROOT,
    get_existing_experts,
    read_insight_frontmatter,
    rebuild_search_index,
)


# ── Shared error reporter ─────────────────────────────────────────────────────

def _show_modal_error(context: str, exc: Exception) -> None:
    st.error(f"[{context}] An unexpected error occurred: {exc}")
    if os.environ.get("DEBUG"):
        st.code(traceback.format_exc(), language="python")


# ── Settings modal ────────────────────────────────────────────────────────────

@st.dialog("⚙️ System Configuration", width="large")
def settings_modal() -> None:
    try:
        _settings_modal_body()
    except Exception as exc:
        _show_modal_error("Settings", exc)


def _settings_modal_body() -> None:
    st.subheader("API Keys")
    st.markdown("Update your API keys here. Changes are saved to `.env`.")

    env_path = ROOT / ".env"
    current_env = env_path.read_text(encoding="utf-8") if env_path.exists() else ""

    def get_env_val(key: str) -> str:
        for line in current_env.splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip("\"'")
        return ""

    openrouter_key = st.text_input("OpenRouter API Key", value=get_env_val("OPENROUTER_API_KEY"), type="password")
    azure_endpoint = st.text_input("Azure Endpoint", value=get_env_val("AZURE_OPENAI_ENDPOINT"))
    azure_key = st.text_input("Azure API Key", value=get_env_val("AZURE_OPENAI_API_KEY"), type="password")

    if st.button("Save Settings"):
        new_env = current_env

        def update_or_add(text: str, key: str, val: str) -> str:
            if val:
                pattern = f"^{key}=.*$"
                if re.search(pattern, text, flags=re.MULTILINE):
                    return re.sub(pattern, f'{key}="{val}"', text, flags=re.MULTILINE)
                return text + f'\n{key}="{val}"'
            return text

        new_env = update_or_add(new_env, "OPENROUTER_API_KEY", openrouter_key)
        new_env = update_or_add(new_env, "AZURE_OPENAI_ENDPOINT", azure_endpoint)
        new_env = update_or_add(new_env, "AZURE_OPENAI_API_KEY", azure_key)

        env_path.write_text(new_env, encoding="utf-8")
        st.success("Saved to .env!")
        st.rerun()

    st.divider()
    st.subheader("Database Maintenance")

    if st.button("Rebuild Search Index"):
        with st.spinner("Rebuilding..."):
            res = rebuild_search_index()
            if "error" in res:
                st.error(f"Error: {res['error']}")
            else:
                st.success(f"Index rebuilt! Indexed {res['indexed']} files. Skipped {res['skipped']}.")


# ── Library modal ─────────────────────────────────────────────────────────────

def _enforce_single_checkbox() -> None:
    if "library_editor" not in st.session_state:
        return
    state = st.session_state["library_editor"].get("edited_rows", {})
    
    for idx_str, row in list(state.items()):
        if "View" in row:
            idx = int(idx_str)
            if row["View"] is True:
                st.session_state["last_viewed_id"] = idx
            elif row["View"] is False:
                if st.session_state.get("last_viewed_id") == idx:
                    st.session_state["last_viewed_id"] = None
            
            # Clear View from edited_rows so it doesn't stick
            del state[idx_str]["View"]
            if not state[idx_str]:
                del state[idx_str]

@st.dialog("📚 Knowledge Library", width="large")
def library_modal() -> None:
    try:
        _library_modal_body()
    except Exception as exc:
        _show_modal_error("Library", exc)

def _library_modal_body() -> None:
    try:
        from core.ingest_resource import assign_insight_to_expert, update_insight_frontmatter
    except ImportError as exc:
        st.error(f"Could not import core.ingest_resource: {exc}")
        return

    st.subheader("Saved Insights")
    st.markdown("Browse, edit, and assign your knowledge. Check 'View' to read.")

    knowledge_dir = ROOT / "data" / "knowledge"
    private_dir = ROOT / "data" / "private"
    inbox_dir = ROOT / "data" / "inbox"

    md_files = []
    if knowledge_dir.exists(): md_files.extend(list(knowledge_dir.rglob("*.md")))
    if private_dir.exists(): md_files.extend(list(private_dir.rglob("*.md")))
    if inbox_dir.exists(): md_files.extend(list(inbox_dir.rglob("*.md")))
    md_files = [f for f in md_files if "raw" not in f.parts]

    if not md_files:
        st.info("No notes saved yet.")
        return

    experts = get_existing_experts()
    expert_names = ["Unattached"] + [e["display_name"] for e in experts]
    expert_slug_map = {e["display_name"]: e["slug"] for e in experts}
    slug_to_name_map = {e["slug"]: e["display_name"] for e in experts}

    raw_data = []
    for f in md_files:
        fm = read_insight_frontmatter(f)
        attached = fm.get("attached_experts", [])
        if isinstance(attached, str):
            attached = [attached.strip("[]").strip()] if attached.strip("[]").strip() else []
        
        expert_col = slug_to_name_map.get(attached[0], "Unattached") if attached else "Unattached"
        
        raw_tags = fm.get("tags", "")
        tags_str = ", ".join(map(str, raw_tags)) if isinstance(raw_tags, list) else str(raw_tags)

        # Retrieve created_at for sorting, fallback to filesystem mtime
        created_at = fm.get("created_at")
        if not isinstance(created_at, str):
            try:
                created_at = str(f.stat().st_mtime)
            except Exception:
                created_at = ""

        # Format created_at for human-readable display
        date_display = ""
        if isinstance(created_at, str) and created_at:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(created_at)
                date_display = dt.strftime("%d %b %Y")  # e.g. "26 May 2026"
            except (ValueError, TypeError):
                date_display = created_at[:10] if len(created_at) >= 10 else created_at

        raw_data.append({
            "Title": fm.get("title", f.name),
            "Domain": fm.get("domain", "Unknown"),
            "Expert": expert_col,
            "Tags": tags_str,
            "created_at": created_at,
            "date_display": date_display,
            "path": str(f),
        })

    # Sort descending so newest is at the top
    raw_data.sort(key=lambda x: x["created_at"], reverse=True)

    data = []
    path_map = {}
    for i, item in enumerate(raw_data):
        data.append({
            "_id": i,
            "View": (st.session_state.get("last_viewed_id") == i),
            "Title": item["Title"],
            "Domain": item["Domain"],
            "Expert": item["Expert"],
            "Tags": item["Tags"],
            "Added": item["date_display"],
        })
        path_map[i] = item["path"]

    df = pd.DataFrame(data)

    col1, col2 = st.columns([6, 4])

    with col1:
        st.data_editor(
            df,
            column_config={
                "_id": None,
                "View": st.column_config.CheckboxColumn("📖 View", default=False),
                "Title": st.column_config.TextColumn("Title"),
                "Domain": st.column_config.TextColumn("Domain"),
                "Expert": st.column_config.SelectboxColumn("Expert", options=expert_names, required=True),
                "Tags": st.column_config.TextColumn("Tags"),
                "Added": st.column_config.TextColumn("📅 Added"),
            },
            use_container_width=True,
            hide_index=True,
            key="library_editor",
            on_change=_enforce_single_checkbox,
        )
        
        with st.expander("➕ Create New Expert", expanded=False):
            new_expert_name = st.text_input("Expert Name", key="new_expert_name_input")
            if st.button("Create Expert", key="create_expert_btn"):
                if new_expert_name.strip():
                    from core.experts import create_empty_expert
                    res = create_empty_expert(new_expert_name.strip())
                    if res.get("success"):
                        st.success(f"Expert '{new_expert_name}' created successfully!")
                    else:
                        st.error(f"Error: {res.get('error')}")
                else:
                    st.warning("Please enter a valid expert name.")

    with col2:
        st.subheader("📖 Insight Viewer")
        view_id = st.session_state.get("last_viewed_id")
        if view_id is not None and view_id in path_map:
            file_path = path_map[view_id]
            content = Path(file_path).read_text(encoding="utf-8")
            st.caption(f"**Path:** `{Path(file_path).relative_to(ROOT)}`")
            
            # Button for regenerating summary
            if st.button("🔄 Regenerate AI Summary", key=f"regen_summary_{view_id}"):
                with st.spinner("Regenerating AI Summary..."):
                    from core.ingest import regenerate_insight_summary
                    res = regenerate_insight_summary(Path(file_path))
                    if res.get("success"):
                        st.success("Summary regenerated successfully!")
                    else:
                        st.error(f"Error: {res.get('error')}")
            
            with st.container(height=500):
                import re
                parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
                if len(parts) >= 3:
                    body = parts[2]
                else:
                    body = content
                
                summary_part = body
                raw_part = ""
                
                match = re.search(r"\n(## Original Content|## AI Raw Output|### Raw User Input)", body)
                if match:
                    summary_part = body[:match.start()]
                    raw_part = body[match.start() + 1:]
                
                tab1, tab2, tab3 = st.tabs(["📝 Summary & Insights", "📄 Source & Raw", "⚙️ Metadata"])
                
                with tab1:
                    st.markdown(summary_part)
                    
                with tab2:
                    if raw_part:
                        st.markdown(raw_part)
                    else:
                        st.info("No raw data sections found.")
                        
                with tab3:
                    # fm is available in the loop scope, but wait, fm is from the loop which is the LAST file!
                    # We need to parse it for the CURRENT file_path!
                    fm_current = read_insight_frontmatter(Path(file_path))
                    st.json(fm_current)

        else:
            st.info("Check the '📖 View' box on any note to read its contents here.")

    # Process edits from session state
    if "library_editor" in st.session_state:
        edited_rows = st.session_state["library_editor"].get("edited_rows", {})
        changes_made = False
        
        for idx_str, edits in edited_rows.items():
            idx = int(idx_str)
            file_path = path_map[idx]
            
            updates = {}
            if "Title" in edits: updates["title"] = edits["Title"]
            if "Domain" in edits: updates["domain"] = edits["Domain"]
            if "Tags" in edits: updates["tags"] = edits["Tags"]

            if updates:
                update_insight_frontmatter(file_path, **updates)
                changes_made = True

            if "Expert" in edits:
                new_expert = edits["Expert"]
                if new_expert == "Unattached":
                    update_insight_frontmatter(file_path, expert_status="Unattached", attached_experts=[])
                    for e in experts:
                        ref_path = ROOT / "data" / "experts" / e["slug"] / "sources" / f"{Path(file_path).stem}-ref.md"
                        if ref_path.exists():
                            ref_path.unlink()
                else:
                    target_slug = expert_slug_map.get(new_expert)
                    if target_slug:
                        assign_insight_to_expert(
                            insight_path=Path(file_path),
                            expert_slug=target_slug,
                            expert_name=new_expert,
                            reason="attach",
                        )
                changes_made = True

        if changes_made:
            st.success("Changes saved! They will be reflected in the Library.")
            # Clear edits so we don't re-save them on every rerun
            st.session_state["library_editor"]["edited_rows"] = {}


# ── Creator / YouTube expert modal ────────────────────────────────────────────

@st.dialog("🎥 YouTube Detected!", width="large")
def creator_expert_modal() -> None:
    try:
        _creator_expert_modal_body()
    except Exception as exc:
        _show_modal_error("Creator Expert", exc)


def _creator_expert_modal_body() -> None:
    import os as _os
    import tempfile

    try:
        from core.youtube import fetch_channel_metadata, fetch_recent_videos, fetch_video_metadata
        from core.experts import assign_insight_to_expert, synthesize_creator_persona, slugify_expert_name
        from core.ingest import process_one_file
    except ImportError as exc:
        st.error(f"Could not import required modules: {exc}")
        return

    def process_url_directly(url: str, use_ai: bool = False) -> dict:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp:
            tmp.write(url)
            tmp_path = tmp.name

        result = process_one_file(tmp_path, use_ai=use_ai)
        try:
            _os.remove(tmp_path)
        except FileNotFoundError:
            pass
        return result

    channel_url: str = st.session_state.get("pending_channel_url") or ""

    is_single_video = ("/watch" in channel_url or "/shorts" in channel_url or 
                      ("youtu.be/" in channel_url and len(channel_url.split("youtu.be/")[1]) <= 15))

    st.text_input("YouTube URL", value=channel_url, disabled=True)

    if is_single_video:
        max_videos = 1
        st.info("Single video detected. We will clone the persona from this specific video.")
    else:
        max_videos = st.number_input("How many recent videos?", min_value=1, max_value=50, value=5)

    run_ai_summaries = st.checkbox("Run AI Summarization on all videos (Takes longer)", value=False)

    if "channel_meta" not in st.session_state:
        st.session_state.channel_meta = None

    if "build_done" not in st.session_state:
        st.session_state.build_done = False

    if st.session_state.channel_meta is None and channel_url:
        with st.spinner("Fetching metadata..."):
            meta = fetch_video_metadata(channel_url) if is_single_video else fetch_channel_metadata(channel_url)
            if meta.get("error"):
                st.error(f"Error fetching channel: {meta['error']}")
            else:
                st.session_state.channel_meta = meta
                st.rerun()

    if st.session_state.channel_meta:
        uploader: str = st.session_state.channel_meta["uploader"]
        slug = slugify_expert_name(uploader)

        st.success(f"Detected Creator: **{uploader}**")
        if is_single_video:
            st.info(f"This will create/update the expert profile: `{slug}` and download the transcript for this video.")
        else:
            st.info(f"This will create/update the expert profile: `{slug}` and download transcripts for the {max_videos} most recent videos.")

        col1, col2 = st.columns(2)

        with col1:
            if not st.session_state.build_done:
                if st.button("Confirm & Build Expert"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    if is_single_video:
                        video_urls = [channel_url]
                    else:
                        status_text.text("Fetching video list...")
                        video_urls = fetch_recent_videos(channel_url, max_videos)

                    if not video_urls:
                        st.error("Could not find any videos.")
                        return

                    success_count = 0
                    fail_count = 0

                    expert_dir = ROOT / "data" / "experts" / slug
                    expert_exists = expert_dir.exists() and (expert_dir / "profile.md").exists()

                    for i, vid_url in enumerate(video_urls):
                        status_text.text(f"Processing ({i + 1}/{len(video_urls)}): {vid_url}")
                        try:
                            res = process_url_directly(vid_url, use_ai=run_ai_summaries)
                            if res.get("success") and res.get("out_filepath"):
                                assign_insight_to_expert(
                                    insight_path=Path(res["out_filepath"]),
                                    expert_slug=slug,
                                    expert_name=uploader,
                                    reason="Auto-ingested from Channel builder",
                                )
                                success_count += 1

                                if i == 0 and not expert_exists and res.get("transcript_path"):
                                    t_path = Path(res["transcript_path"])
                                    if t_path.exists():
                                        status_text.text("Synthesizing Creator Persona...")
                                        t_text = t_path.read_text(encoding="utf-8")[:15000]
                                        persona = synthesize_creator_persona(uploader, t_text)
                                        expert_dir.mkdir(parents=True, exist_ok=True)
                                        if persona.get("profile"):
                                            (expert_dir / "profile.md").write_text(
                                                f"---\ntype: expert_profile\nstatus: cloned\n---\n\n# Profile\n\n{persona['profile']}",
                                                encoding="utf-8",
                                            )
                                        if persona.get("playbook"):
                                            (expert_dir / "playbook.md").write_text(
                                                f"---\ntype: expert_playbook\n---\n\n# Playbook & Style\n\n{persona['playbook']}",
                                                encoding="utf-8",
                                            )
                                        if persona.get("principles"):
                                            (expert_dir / "principles.md").write_text(
                                                f"---\ntype: expert_principles\n---\n\n# Core Principles\n\n{persona['principles']}",
                                                encoding="utf-8",
                                            )
                            else:
                                fail_count += 1

                        except Exception as exc:
                            fail_count += 1
                            print(f"[creator_expert_modal] Error on {vid_url}: {exc}")

                        progress_bar.progress((i + 1) / len(video_urls))

                    if success_count > 0:
                        status_text.text("Rebuilding Search Index...")
                        rebuild_search_index()
                        progress_bar.empty()
                        status_text.empty()
                        st.session_state.build_done = True
                        st.rerun()
                    else:
                        st.error("Failed to process any videos for this creator. Please try again.")
                        progress_bar.empty()
                        status_text.empty()
            else:
                st.success("✅ **Expert Built!**")
                st.markdown(f"**Next Action:** Close this window to start chatting with **{uploader}**!")

        with col2:
            if st.session_state.build_done:
                if st.button("Close"):
                    st.session_state.pending_channel_url = None
                    st.session_state.channel_meta = None
                    st.session_state.build_done = False
                    st.rerun()
            else:
                if st.button("Cancel & Close"):
                    st.session_state.pending_channel_url = None
                    st.session_state.channel_meta = None
                    st.session_state.build_done = False
                    st.rerun()

# ── Memories modal ────────────────────────────────────────────────────────────

@st.dialog("🧠 Manual Personal Memory", width="large")
def memories_modal() -> None:
    try:
        _memories_modal_body()
    except Exception as exc:
        _show_modal_error("Memories", exc)

def _memories_modal_body() -> None:
    from .helpers import add_user_memory, get_user_memories, toggle_user_memory, delete_user_memory
    
    st.markdown("Inject custom context into chat.")
    
    if st.session_state.pop("memory_added", False):
        st.success("Memory added!")
    if st.session_state.pop("memory_warning", False):
        st.warning("Warning: The memory you just added is very large (>2000 tokens) and will consume a lot of the context window.")
    
    with st.form("add_memory_form", clear_on_submit=True):
        new_title = st.text_input("Title (e.g. Coding Style)", key="new_mem_title")
        new_content = st.text_area("Content", height=100, key="new_mem_content")
        submitted = st.form_submit_button("Add Memory")
        if submitted and new_title and new_content:
            if add_user_memory(new_title, new_content):
                st.session_state.memory_added = True
                if len(new_content) > 8000:
                    st.session_state.memory_warning = True

    def _delete_cb(mid):
        delete_user_memory(mid)

    def _toggle_cb(mid, tkey):
        toggle_user_memory(mid, st.session_state[tkey])

    memories = get_user_memories()
    if memories:
        st.markdown("### Saved Memories")
        for mem in memories:
            with st.container(border=True):
                st.markdown(f"**{mem['title']}**")
                display_content = mem['content'] if len(mem['content']) < 100 else mem['content'][:100] + "..."
                st.caption(display_content)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    tkey = f"mem_toggle_{mem['id']}"
                    st.toggle("Active", value=bool(mem['is_active']), key=tkey, on_change=_toggle_cb, args=(mem['id'], tkey))
                with col2:
                    st.button("🗑️", key=f"mem_del_{mem['id']}", help="Delete", on_click=_delete_cb, args=(mem['id'],))
