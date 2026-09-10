import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Cricbuzz LiveStats")
st.markdown("### Real-Time Cricket Insights & SQL-Based Analytics")

st.write("""
Welcome! Use the sidebar to navigate between:
- **Live Match** — real-time scorecards
- **Top Player Stats** — batting/bowling leaderboards
- **SQL Queries & Analytics** — run the 25 practice queries
- **CRUD Operations** — add, update, delete records
""")