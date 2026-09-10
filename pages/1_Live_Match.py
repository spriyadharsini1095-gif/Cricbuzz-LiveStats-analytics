import streamlit as st
from api.cricbuzz_client import get_live_matches

st.set_page_config(page_title="Live Match", layout="wide")
st.title("🔴 Live Match")

if st.button("Refresh"):
    st.rerun()

try:
    data = get_live_matches()
except Exception as e:
    st.error(f"Could not fetch live matches: {e}")
    st.stop()

type_matches = data.get("typeMatches", [])

if not type_matches:
    st.info("No live matches right now.")
else:
    for type_match in type_matches:
        for series_match in type_match.get("seriesMatches", []):
            wrapper = series_match.get("seriesAdWrapper", {})
            series_name = wrapper.get("seriesName", "Unknown Series")

            for match in wrapper.get("matches", []):
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                with st.container(border=True):
                    st.subheader(f"{info.get('team1', {}).get('teamName', '')} vs {info.get('team2', {}).get('teamName', '')}")
                    st.caption(f"{series_name} — {info.get('matchDesc', '')} — {info.get('status', '')}")

                    col1, col2 = st.columns(2)
                    with col1:
                        t1_score = score.get("team1Score", {}).get("inngs1", {})
                        if t1_score:
                            st.metric(
                                info.get('team1', {}).get('teamSName', 'Team 1'),
                                f"{t1_score.get('runs', 0)}/{t1_score.get('wickets', 0)}",
                                f"{t1_score.get('overs', 0)} overs"
                            )
                    with col2:
                        t2_score = score.get("team2Score", {}).get("inngs1", {})
                        if t2_score:
                            st.metric(
                                info.get('team2', {}).get('teamSName', 'Team 2'),
                                f"{t2_score.get('runs', 0)}/{t2_score.get('wickets', 0)}",
                                f"{t2_score.get('overs', 0)} overs"
                            )