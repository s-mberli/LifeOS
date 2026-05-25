"""
LifeOS - Streamlit Application Entry Point.

Run from the project root:
    streamlit run apps/streamlit-chat/app.py
"""

import sys
from pathlib import Path

# ── Bootstrap import paths ────────────────────────────────────────────────────
# Resolve the project root (3 levels up from this file).
ROOT = Path(__file__).resolve().parent.parent.parent

# src/ must be on sys.path so ui/ modules can import project scripts.
sys.path.insert(0, str(ROOT))

# Add this file's directory so that `from ui.xxx import …` resolves correctly
# whether the app is launched from the project root or from this directory.
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

# Load .env if present (optional dependency)
try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

from ui.chat import render_chat_interface
from ui.sidebar import render_sidebar

# ── Page configuration (must be the first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="LifeOS",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).parent / "ui" / "assets" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Render ────────────────────────────────────────────────────────────────────
render_sidebar()
render_chat_interface()