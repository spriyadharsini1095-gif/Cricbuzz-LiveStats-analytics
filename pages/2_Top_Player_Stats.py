import streamlit as st
import pandas as pd
from utils.db_connection import get_engine
from sqlalchemy import text

st.set_page_config(page_title="Top Player Stats", layout="wide")
st.title("🏏 Top Player Stats")

engine = get_engine()
tab1, tab2 = st.tabs(["Top Run Scorers", "Top Wicket Takers"])

with tab1:
    st.subheader("Top 20 Run Scorers")
    query = """
        SELECT p.player_name, SUM(b.runs) AS total_runs,
               COUNT(DISTINCT b.match_id) AS matches_played,
               ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC
        LIMIT 20
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("player_name")["total_runs"])

with tab2:
    st.subheader("Top 20 Wicket Takers")
    query = """
        SELECT p.player_name, SUM(bw.wickets) AS total_wickets,
               COUNT(DISTINCT bw.match_id) AS matches_played,
               ROUND(AVG(bw.economy), 2) AS avg_economy
        FROM bowling_scorecard bw
        JOIN players p ON p.player_id = bw.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_wickets DESC
        LIMIT 20
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("player_name")["total_wickets"])