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

# scripts/ must be on sys.path so ui/ modules can import project scripts.
sys.path.insert(0, str(ROOT / "scripts"))

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

st.markdown(
    """
    <style>
    /* Center the main app block to 850px */
    .block-container {
        max-width: 850px !important;
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }

    /* Subtle typography improvements */
    p, div, span, label, li {
        line-height: 1.6;
    }

    /* Pill and Button hover animations */
    .stSegmentedControl label, .stButton button {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stSegmentedControl label:hover, .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    /* Glassmorphic Chat Input */
    [data-testid="stChatInput"] {
        background: rgba(30, 41, 59, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* Chat message bubbles */
    [data-testid="stChatMessage"] {
        background: #1E293B !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        margin-bottom: 1rem !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* Hide default streamlit branding in footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Render ────────────────────────────────────────────────────────────────────
render_sidebar()
render_chat_interface()