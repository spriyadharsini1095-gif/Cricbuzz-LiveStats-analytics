import streamlit as st
import pandas as pd
from utils.db_connection import get_engine
from sqlalchemy import text

st.set_page_config(page_title="SQL Queries & Analytics", layout="wide")
st.title("📊 SQL Queries & Analytics")

engine = get_engine()

QUERIES = {
    "Q1: All teams": """
        SELECT team_id, team_name, team_s_name FROM teams ORDER BY team_name
    """,
    "Q2: Venues in a city": """
        SELECT venue_id, ground, city FROM venues WHERE city = 'Bengaluru'
    """,
    "Q3: Completed matches": """
        SELECT match_id, match_desc, status, result FROM matches WHERE status = 'Complete'
    """,
    "Q4: ODI format matches": """
        SELECT match_id, match_desc, match_format, start_date
        FROM matches WHERE match_format = 'ODI' ORDER BY start_date DESC
    """,
    "Q5: Matches per series": """
        SELECT series_id, COUNT(*) AS total_matches
        FROM matches GROUP BY series_id ORDER BY total_matches DESC
    """,
    "Q6: Top 10 highest individual scores": """
        SELECT p.player_name, b.runs, b.balls, b.match_id
        FROM batting_scorecard b
        JOIN players p ON b.player_id = p.player_id
        ORDER BY b.runs DESC LIMIT 10
    """,
    "Q7: Bowlers with 3+ wickets in an innings": """
        SELECT bw.player_id, p.player_name, bw.wickets, bw.runs_conceded, bw.match_id
        FROM bowling_scorecard bw
        JOIN players p ON bw.player_id = p.player_id
        WHERE bw.wickets >= 3 ORDER BY bw.wickets DESC
    """,
    "Q8: Venues sorted by matches hosted": """
        SELECT v.venue_id, v.ground, v.city, COUNT(m.match_id) AS matches_hosted
        FROM venues v
        JOIN matches m ON v.venue_id = m.venue_id
        GROUP BY v.venue_id, v.ground, v.city
        ORDER BY matches_hosted DESC
    """,
    "Q9: Matches with team names (JOIN)": """
        SELECT m.match_id, m.match_desc,
               t1.team_name AS team1, t2.team_name AS team2,
               m.status, m.result
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        ORDER BY m.start_date DESC
    """,
    "Q10: Total runs per player": """
        SELECT p.player_name, SUM(b.runs) AS total_runs,
               COUNT(DISTINCT b.match_id) AS matches_played
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_runs DESC LIMIT 20
    """,
    "Q11: Total wickets per bowler": """
        SELECT p.player_name, SUM(bw.wickets) AS total_wickets,
               COUNT(DISTINCT bw.match_id) AS matches_played
        FROM bowling_scorecard bw
        JOIN players p ON bw.player_id = p.player_id
        GROUP BY p.player_id, p.player_name
        ORDER BY total_wickets DESC LIMIT 20
    """,
    "Q12: Players who played for multiple teams": """
        SELECT player_id, COUNT(DISTINCT team_id) AS team_count
        FROM (
            SELECT player_id, team_id FROM batting_scorecard
            UNION
            SELECT player_id, team_id FROM bowling_scorecard
        ) combined
        GROUP BY player_id HAVING team_count > 1
    """,
    "Q13: Average strike rate (min 20 balls)": """
        SELECT p.player_name,
               ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate,
               SUM(b.balls) AS total_balls_faced
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        GROUP BY p.player_id, p.player_name
        HAVING total_balls_faced >= 20
        ORDER BY avg_strike_rate DESC LIMIT 20
    """,
    "Q14: Matches per venue": """
        SELECT v.ground, v.city, COUNT(m.match_id) AS total_matches
        FROM venues v
        LEFT JOIN matches m ON v.venue_id = m.venue_id
        GROUP BY v.venue_id, v.ground, v.city
        ORDER BY total_matches DESC
    """,
    "Q15: Series with most matches": """
        SELECT s.series_name, match_counts.total_matches
        FROM series s
        JOIN (
            SELECT series_id, COUNT(*) AS total_matches
            FROM matches GROUP BY series_id
        ) match_counts ON s.series_id = match_counts.series_id
        ORDER BY match_counts.total_matches DESC LIMIT 10
    """,
    "Q16: Players who batted and bowled in same match": """
        SELECT DISTINCT b.player_id, p.player_name, b.match_id
        FROM batting_scorecard b
        JOIN bowling_scorecard bw
            ON b.player_id = bw.player_id AND b.match_id = bw.match_id
        JOIN players p ON b.player_id = p.player_id
        ORDER BY b.match_id LIMIT 20
    """,
    "Q17: Running total of runs per player": """
        SELECT p.player_name, b.match_id, b.runs,
               SUM(b.runs) OVER (PARTITION BY b.player_id ORDER BY b.match_id) AS running_total
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        ORDER BY p.player_name, b.match_id
    """,
    "Q18: Rank players by total runs": """
        SELECT p.player_name, SUM(b.runs) AS total_runs,
               RANK() OVER (ORDER BY SUM(b.runs) DESC) AS run_rank
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        GROUP BY p.player_id, p.player_name LIMIT 20
    """,
    "Q19: Each player's best innings score": """
        SELECT * FROM (
            SELECT p.player_name, b.match_id, b.runs,
                   ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY b.runs DESC) AS rn
            FROM batting_scorecard b
            JOIN players p ON p.player_id = b.player_id
        ) ranked
        WHERE rn = 1 ORDER BY runs DESC LIMIT 20
    """,
    "Q20: Team-wise total runs (CTE)": """
        WITH team_runs AS (
            SELECT team_id, SUM(runs) AS total_runs
            FROM batting_scorecard GROUP BY team_id
        )
        SELECT t.team_name, tr.total_runs
        FROM team_runs tr
        JOIN teams t ON t.team_id = tr.team_id
        ORDER BY tr.total_runs DESC
    """,
    "Q21: Batting partnerships (approx.)": """
        SELECT b1.match_id, b1.innings_id,
               p1.player_name AS player1, b1.runs AS runs1,
               p2.player_name AS player2, b2.runs AS runs2,
               (b1.runs + b2.runs) AS partnership_runs
        FROM batting_scorecard b1
        JOIN batting_scorecard b2
            ON b1.match_id = b2.match_id AND b1.innings_id = b2.innings_id
            AND b1.player_id < b2.player_id
        JOIN players p1 ON p1.player_id = b1.player_id
        JOIN players p2 ON p2.player_id = b2.player_id
        ORDER BY partnership_runs DESC LIMIT 10
    """,
    "Q22: Total wins per team": """
        SELECT t.team_name, COUNT(*) AS total_wins
        FROM matches m
        JOIN teams t ON t.team_id = m.winner_team_id
        GROUP BY t.team_id, t.team_name
        ORDER BY total_wins DESC LIMIT 15
    """,
    "Q23: Bowling economy leaders (min 10 overs)": """
        WITH bowler_totals AS (
            SELECT player_id, SUM(overs) AS total_overs,
                   SUM(runs_conceded) AS total_runs, SUM(wickets) AS total_wickets
            FROM bowling_scorecard GROUP BY player_id
        )
        SELECT p.player_name, bt.total_overs, bt.total_runs, bt.total_wickets,
               ROUND(bt.total_runs / NULLIF(bt.total_overs, 0), 2) AS economy
        FROM bowler_totals bt
        JOIN players p ON p.player_id = bt.player_id
        WHERE bt.total_overs >= 10
        ORDER BY economy ASC LIMIT 15
    """,
    "Q24: Most consistent batters (lowest variance)": """
        SELECT p.player_name, COUNT(*) AS innings_played,
               ROUND(AVG(b.runs), 2) AS avg_runs,
               ROUND(STDDEV(b.runs), 2) AS run_stddev
        FROM batting_scorecard b
        JOIN players p ON p.player_id = b.player_id
        GROUP BY p.player_id, p.player_name
        HAVING innings_played >= 3
        ORDER BY run_stddev ASC LIMIT 15
    """,
    "Q25: Player form trend (last 3 innings vs career avg)": """
        WITH ranked_innings AS (
            SELECT p.player_id, p.player_name, b.match_id, b.runs,
                   ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY b.match_id DESC) AS recency_rank,
                   AVG(b.runs) OVER (PARTITION BY b.player_id) AS career_avg
            FROM batting_scorecard b
            JOIN players p ON p.player_id = b.player_id
        )
        SELECT player_name, match_id, runs, ROUND(career_avg, 2) AS career_avg
        FROM ranked_innings
        WHERE recency_rank <= 3
        ORDER BY player_name, recency_rank
    """,

}

selected = st.selectbox("Choose a query to run:", list(QUERIES.keys()))

st.code(QUERIES[selected], language="sql")

if st.button("Run Query"):
    with engine.connect() as conn:
        df = pd.read_sql(text(QUERIES[selected]), conn)
    st.dataframe(df, use_container_width=True)
    st.caption(f"{len(df)} rows returned")