"""
LifeOS UI sidebar.

Renders the Streamlit sidebar: resource ingestion form, library browser
button, and system configuration button.  Modal dialogs are imported from
``ui.modals`` and triggered when the corresponding buttons are clicked or
when a pending channel URL is detected in session state.
"""

import traceback

import streamlit as st

from .helpers import (
    ROOT, rebuild_search_index
)
from .modals import creator_expert_modal, library_modal, settings_modal, memories_modal, experts_modal


def render_sidebar() -> None:
    """Render the full sidebar including the ingest form and action buttons.

    This is the single public entry-point for the sidebar module.  Wraps
    all rendering in a try/except so that a broken sidebar never prevents
    the rest of the app from loading.
    """
    try:
        _render_sidebar_body()
    except Exception as exc:
        with st.sidebar:
            st.error(f"[Sidebar] Unexpected error: {exc}")
            import os

            if os.environ.get("DEBUG"):
                st.code(traceback.format_exc(), language="python")


def _render_sidebar_body() -> None:
    """Inner implementation of the sidebar (no error boundary here)."""
    import os  # noqa: PLC0415
    import re  # noqa: PLC0415
    import tempfile  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    with st.sidebar:
        st.title("🧭 Quick Actions")
        st.markdown("Ingest URLs, files, or raw text transcripts into your library.")

        # Ingest via tabs to declutter sidebar
        tabs = st.tabs(["📝 Paste URL/Text", "📤 Upload Files"])
        with tabs[0]:
            pasted_text = st.text_area(
                "Or paste URL, raw text, or transcript:",
                height=150,
                key="unified_text",
                label_visibility="collapsed",
            ).strip()
        with tabs[1]:
            uploaded_files = st.file_uploader(
                "Drag & drop files (.txt, .md):",
                accept_multiple_files=True,
                type=["txt", "md"],
                key="bulk_uploader",
                label_visibility="collapsed",
            )

        # Check if the pasted text looks like a single-line YouTube URL
        is_yt_url = False
        if pasted_text:
            is_yt_url = (
                ("youtube.com" in pasted_text or "youtu.be" in pasted_text)
                and "\n" not in pasted_text
            )

        use_ai_bulk = st.checkbox("Run AI Summaries", value=True, key="use_ai_bulk")
        st.markdown(
            "ℹ️ *AI summaries generate searchable metadata (tags, key ideas, next actions) "
            "for the library. Skip if you only want raw content immediately available for chat search.*"
        )

        # Action Buttons
        has_input = bool(pasted_text or uploaded_files)
        
        col1, col2 = st.columns(2)
        with col1:
            submit_ingest = st.button(
                "Save Insight(s)",
                use_container_width=True,
                disabled=not has_input,
                type="primary",
            )
        with col2:
            submit_expert = st.button(
                "🪄 Build Expert",
                use_container_width=True,
                disabled=not is_yt_url,
            )

        # Logic handler
        if submit_expert and is_yt_url:
            st.session_state.pending_channel_url = pasted_text
            st.session_state.channel_meta = None
            st.session_state.build_done = False
            st.rerun()

        elif submit_ingest and has_input:
            with st.status("Ingesting resource(s)...", expanded=True) as status:
                success_count = 0
                failed_count = 0

                # Process pasted URL or text
                if pasted_text:
                    is_url = re.match(r"^https?://[^\s]+$", pasted_text) is not None
                    if is_url:
                        st.write(f"Downloading URL: {pasted_text}")
                    else:
                        st.write("Processing pasted text/transcript...")

                    try:
                        try:
                            from core.ingest import process_one_file
                        except ImportError:
                            from ingest_resource import process_one_file  # Fallback

                        # Write the URL or raw text to a temp file
                        with tempfile.NamedTemporaryFile(
                            mode="w", delete=False, suffix=".txt", encoding="utf-8"
                        ) as tmp:
                            tmp.write(pasted_text)
                            tmp_path = tmp.name

                        res = process_one_file(tmp_path, use_ai=use_ai_bulk)
                        try:
                            os.remove(tmp_path)
                        except FileNotFoundError:
                            pass

                        if res.get("success"):
                            st.success(
                                f"Saved: {res.get('out_filepath', res.get('file_path', 'unknown'))}"
                            )
                            success_count += 1
                        else:
                            st.error(res.get("error"))
                            failed_count += 1
                    except Exception as exc:
                        st.error(str(exc))
                        failed_count += 1

                # Process Uploaded Files
                if uploaded_files:
                    try:
                        from core.ingest import process_one_file
                    except ImportError:
                        from ingest_resource import process_one_file  # Fallback
                    
                    st.write(f"Processing {len(uploaded_files)} uploaded files...")
                    for up_file in uploaded_files:
                        try:
                            suffix = Path(up_file.name).suffix
                            with tempfile.NamedTemporaryFile(
                                mode="wb", delete=False, suffix=suffix
                            ) as tmp:
                                tmp.write(up_file.read())
                                tmp_path = tmp.name

                            tmp_dir = Path(tempfile.gettempdir()) / "bulk_ingest"
                            tmp_dir.mkdir(parents=True, exist_ok=True)
                            target_tmp_file = tmp_dir / up_file.name
                            import shutil
                            shutil.move(tmp_path, target_tmp_file)

                            st.write(f"Ingesting: {up_file.name}")
                            res = process_one_file(str(target_tmp_file), use_ai=use_ai_bulk)
                            if res.get("success"):
                                success_count += 1
                            else:
                                st.error(f"Failed {up_file.name}: {res.get('error')}")
                                failed_count += 1
                        except Exception as up_exc:
                            st.error(f"Failed {up_file.name}: {up_exc}")
                            failed_count += 1

                st.write("Rebuilding search index...")
                rebuild_search_index()
                try:
                    from .chat import cached_get_all_insight_files
                    cached_get_all_insight_files.clear()
                except Exception:
                    pass
                
                status.update(
                    label=f"Ingestion complete. {success_count} succeeded, {failed_count} failed.",
                    state="complete",
                )
                if success_count > 0:
                    st.success(f"Successfully processed {success_count} item(s)!")
                if failed_count > 0:
                    st.warning(f"Failed to process {failed_count} item(s). Check logs for details.")

        # Show the creator expert modal if a pending URL is set
        if st.session_state.get("pending_channel_url"):
            creator_expert_modal()

        st.divider()

        if st.button("📚 Browse Library", use_container_width=True):
            library_modal()

        if st.button("🧑‍🏫 View Experts", use_container_width=True):
            experts_modal()

        if st.button("🧠 Manual Personal Memory", use_container_width=True):
            memories_modal()

        if st.button("⚙️ System Configuration", use_container_width=True):
            settings_modal()
