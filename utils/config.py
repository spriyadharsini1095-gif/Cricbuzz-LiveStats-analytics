import os
from dotenv import load_dotenv

load_dotenv()

def get_config(key, default=None):
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    # Fall back to environment variables (for local development)
    return os.getenv(key, default)

CRICBUZZ_API_KEY = get_config("CRICBUZZ_API_KEY")
CRICBUZZ_API_HOST = get_config("CRICBUZZ_API_HOST")

DB_TYPE = get_config("DB_TYPE", "mysql")
DB_HOST = get_config("DB_HOST", "localhost")
DB_PORT = get_config("DB_PORT", "3306")
DB_USER = get_config("DB_USER", "root")
DB_PASSWORD = get_config("DB_PASSWORD")
DB_NAME = get_config("DB_NAME", "cricket")