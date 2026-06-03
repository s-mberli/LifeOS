import os

def get_env(key: str, default=None):
    """
    Get an environment variable securely.
    First checks Streamlit secrets (st.secrets) if running in Streamlit Cloud,
    then falls back to os.environ.
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except (ImportError, Exception):
        pass
        
    return os.environ.get(key, default)
