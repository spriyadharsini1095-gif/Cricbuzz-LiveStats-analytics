import streamlit as st
import pandas as pd
from utils.db_connection import get_engine
from sqlalchemy import text

st.set_page_config(page_title="CRUD Operations", layout="wide")
st.title("🛠️ CRUD Operations")

engine = get_engine()

tab1, tab2 = st.tabs(["Players", "Teams"])

# ---------- PLAYERS TAB ----------
with tab1:
    st.subheader("Manage Players")

    action = st.radio("Action", ["View", "Add", "Update", "Delete"], horizontal=True, key="player_action")

    if action == "View":
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT * FROM players ORDER BY player_name LIMIT 100"), conn)
        st.dataframe(df, use_container_width=True)

    elif action == "Add":
        with st.form("add_player_form"):
            new_id = st.number_input("Player ID", min_value=1, step=1)
            new_name = st.text_input("Player Name")
            submitted = st.form_submit_button("Add Player")
            if submitted:
                if not new_name.strip():
                    st.error("Player name cannot be empty.")
                else:
                    try:
                        with engine.connect() as conn:
                            conn.execute(text("""
                                INSERT INTO players (player_id, player_name)
                                VALUES (:pid, :pname)
                            """), {"pid": new_id, "pname": new_name.strip()})
                            conn.commit()
                        st.success(f"Added player: {new_name} (ID {new_id})")
                    except Exception as e:
                        st.error(f"Failed to add player: {e}")

    elif action == "Update":
        with engine.connect() as conn:
            players_df = pd.read_sql(text("SELECT player_id, player_name FROM players ORDER BY player_name"), conn)
        selected = st.selectbox("Select player", players_df["player_name"] + " (ID " + players_df["player_id"].astype(str) + ")")
        selected_id = int(selected.split("ID ")[1].rstrip(")"))
        new_name = st.text_input("New name", value=players_df[players_df["player_id"] == selected_id]["player_name"].values[0])
        if st.button("Update Player"):
            try:
                with engine.connect() as conn:
                    conn.execute(text("UPDATE players SET player_name = :name WHERE player_id = :pid"),
                                 {"name": new_name.strip(), "pid": selected_id})
                    conn.commit()
                st.success("Player updated.")
            except Exception as e:
                st.error(f"Failed to update: {e}")

    elif action == "Delete":
        with engine.connect() as conn:
            players_df = pd.read_sql(text("SELECT player_id, player_name FROM players ORDER BY player_name"), conn)
        selected = st.selectbox("Select player to delete", players_df["player_name"] + " (ID " + players_df["player_id"].astype(str) + ")")
        selected_id = int(selected.split("ID ")[1].rstrip(")"))
        st.warning("This will also fail if the player has batting/bowling records (foreign key constraint) — that's expected behavior to protect data integrity.")
        if st.button("Delete Player", type="primary"):
            try:
                with engine.connect() as conn:
                    conn.execute(text("DELETE FROM players WHERE player_id = :pid"), {"pid": selected_id})
                    conn.commit()
                st.success("Player deleted.")
            except Exception as e:
                st.error(f"Failed to delete (likely has related scorecard records): {e}")

# ---------- TEAMS TAB ----------
with tab2:
    st.subheader("Manage Teams")

    action = st.radio("Action", ["View", "Add", "Update"], horizontal=True, key="team_action")

    if action == "View":
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT * FROM teams ORDER BY team_name"), conn)
        st.dataframe(df, use_container_width=True)

    elif action == "Add":
        with st.form("add_team_form"):
            new_id = st.number_input("Team ID", min_value=1, step=1)
            new_name = st.text_input("Team Name")
            new_sname = st.text_input("Short Name")
            submitted = st.form_submit_button("Add Team")
            if submitted:
                try:
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO teams (team_id, team_name, team_s_name)
                            VALUES (:tid, :tname, :tsname)
                        """), {"tid": new_id, "tname": new_name.strip(), "tsname": new_sname.strip()})
                        conn.commit()
                    st.success(f"Added team: {new_name}")
                except Exception as e:
                    st.error(f"Failed to add team: {e}")

    elif action == "Update":
        with engine.connect() as conn:
            teams_df = pd.read_sql(text("SELECT team_id, team_name FROM teams ORDER BY team_name"), conn)
        selected = st.selectbox("Select team", teams_df["team_name"] + " (ID " + teams_df["team_id"].astype(str) + ")")