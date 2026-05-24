"""
LifeOS UI sidebar.

Renders the Streamlit sidebar: resource ingestion form, library browser
button, and system configuration button.  Modal dialogs are imported from
``ui.modals`` and triggered when the corresponding buttons are clicked or
when a pending channel URL is detected in session state.
"""

import traceback

import streamlit as st

from .helpers import ROOT, rebuild_search_index
from .modals import creator_expert_modal, library_modal, settings_modal


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
    import tempfile  # noqa: PLC0415

    with st.sidebar:
        st.title("🧭 Quick Actions")
        st.markdown("Drop a URL here to ingest it in the background.")

        with st.form("ingest_form", clear_on_submit=True):
            url_input = st.text_input("Resource URL (YouTube or Article)")

            col1, col2 = st.columns(2)
            with col1:
                submit_ingest = st.form_submit_button(
                    "Save Insight", use_container_width=True
                )
            with col2:
                submit_expert = st.form_submit_button(
                    "🪄 Build Expert", use_container_width=True
                )

            if (submit_ingest or submit_expert) and url_input.strip():
                is_youtube = (
                    "youtube.com" in url_input or "youtu.be" in url_input
                )
                is_channel = False
                if is_youtube:
                    is_channel = (
                        "/watch" not in url_input
                        and "/shorts" not in url_input
                        and (
                            "@" in url_input
                            or "/c/" in url_input
                            or "/channel/" in url_input
                            or "/user/" in url_input
                        )
                    )

                if submit_expert and is_youtube:
                    # Trigger the creator expert builder modal
                    st.session_state.pending_channel_url = url_input
                    st.session_state.channel_meta = None
                    st.session_state.build_done = False
                    st.rerun()

                elif is_channel and not submit_expert:
                    # Auto-trigger creator expert modal for channel URLs
                    st.session_state.pending_channel_url = url_input
                    st.session_state.channel_meta = None
                    st.session_state.build_done = False
                    st.rerun()

                else:
                    # Synchronous ingestion path
                    with st.status("Ingesting resource...", expanded=True) as status:
                        st.write(f"Downloading: {url_input}")
                        try:
                            from ingest_resource import process_one_file  # noqa: PLC0415

                            with tempfile.NamedTemporaryFile(
                                mode="w", delete=False, suffix=".txt"
                            ) as tmp:
                                tmp.write(url_input)
                                tmp_path = tmp.name

                            res = process_one_file(tmp_path, use_ai=False)
                            try:
                                os.remove(tmp_path)
                            except FileNotFoundError:
                                pass

                            if res.get("success"):
                                rebuild_search_index()
                                status.update(
                                    label="Insight saved & Index rebuilt!",
                                    state="complete",
                                    expanded=False,
                                )
                                st.success(f"Saved: {res.get('file_path')}")
                            else:
                                status.update(
                                    label="Ingestion failed", state="error"
                                )
                                st.error(res.get("error"))

                        except Exception as exc:
                            status.update(
                                label="Ingestion failed", state="error"
                            )
                            st.error(str(exc))

        # Show the creator expert modal if a pending URL is set
        if st.session_state.get("pending_channel_url"):
            creator_expert_modal()

        st.divider()

        if st.button("📚 Browse Library", use_container_width=True):
            library_modal()

        if st.button("⚙️ System Configuration", use_container_width=True):
            settings_modal()
