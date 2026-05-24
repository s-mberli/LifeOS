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
    currently_checked = [idx for idx, row in state.items() if row.get("View") is True]

    last_viewed = st.session_state.get("last_viewed_id")
    
    if len(currently_checked) > 1:
        newly_checked = [idx for idx in currently_checked if idx != last_viewed]
        active_idx = newly_checked[0] if newly_checked else currently_checked[0]
        for idx in currently_checked:
            if idx != active_idx:
                state[idx]["View"] = False
        st.session_state["last_viewed_id"] = active_idx
    elif len(currently_checked) == 1:
        st.session_state["last_viewed_id"] = currently_checked[0]
    else:
        st.session_state["last_viewed_id"] = None

@st.dialog("📚 Knowledge Library", width="large")
def library_modal() -> None:
    try:
        _library_modal_body()
    except Exception as exc:
        _show_modal_error("Library", exc)

def _library_modal_body() -> None:
    try:
        from ingest_resource import assign_insight_to_expert, update_insight_frontmatter
    except ImportError as exc:
        st.error(f"Could not import ingest_resource: {exc}")
        return

    st.subheader("Saved Insights")
    st.markdown("Browse, edit, and assign your knowledge. Check 'View' to read.")

    knowledge_dir = ROOT / "data" / "knowledge"
    private_dir = ROOT / "data" / "private"

    md_files = []
    if knowledge_dir.exists(): md_files.extend(list(knowledge_dir.rglob("*.md")))
    if private_dir.exists(): md_files.extend(list(private_dir.rglob("*.md")))
    md_files = [f for f in md_files if "raw" not in f.parts]

    if not md_files:
        st.info("No notes saved yet.")
        return

    experts = get_existing_experts()
    expert_names = ["Unattached"] + [e["display_name"] for e in experts]
    expert_slug_map = {e["display_name"]: e["slug"] for e in experts}
    slug_to_name_map = {e["slug"]: e["display_name"] for e in experts}

    data = []
    path_map = {}

    for i, f in enumerate(md_files):
        fm = read_insight_frontmatter(f)
        attached = fm.get("attached_experts", [])
        if isinstance(attached, str):
            attached = [attached.strip("[]").strip()] if attached.strip("[]").strip() else []
        
        expert_col = slug_to_name_map.get(attached[0], "Unattached") if attached else "Unattached"
        
        raw_tags = fm.get("tags", "")
        tags_str = ", ".join(map(str, raw_tags)) if isinstance(raw_tags, list) else str(raw_tags)

        data.append({
            "_id": i,
            "View": False,
            "Title": fm.get("title", f.name),
            "Domain": fm.get("domain", "Unknown"),
            "Expert": expert_col,
            "Tags": tags_str,
        })
        path_map[i] = str(f)

    df = pd.DataFrame(data)

    col1, col2 = st.columns([6, 4])

    with col1:
        st.data_editor(
            df,
            column_config={
                "_id": None,
                "View": st.column_config.CheckboxColumn("📖 View", default=False),
                "Expert": st.column_config.SelectboxColumn("Expert", options=expert_names, required=True),
                "Title": st.column_config.TextColumn("Title"),
                "Domain": st.column_config.TextColumn("Domain"),
                "Tags": st.column_config.TextColumn("Tags"),
            },
            use_container_width=True,
            hide_index=True,
            key="library_editor",
            on_change=_enforce_single_checkbox,
        )

    with col2:
        st.subheader("📖 Insight Viewer")
        view_id = st.session_state.get("last_viewed_id")
        if view_id is not None and view_id in path_map:
            file_path = path_map[view_id]
            content = Path(file_path).read_text(encoding="utf-8")
            st.caption(f"**Path:** `{Path(file_path).relative_to(ROOT)}`")
            with st.container(height=500):
                st.markdown(content)
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
        from core.experts import assign_insight_to_expert, synthesize_creator_persona
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
        max_videos = st.number_input("How many recent videos?", min_value=1, max_value=10, value=5)

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
        slug = f"expert--{re.sub(r'[^a-zA-Z0-9-]', '-', uploader.lower())}"
        slug = re.sub(r"-+", "-", slug).strip("-")

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
                            res = process_url_directly(vid_url, use_ai=False)
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
