from utils.db_connection import get_engine
from sqlalchemy import text
import pandas as pd

engine = get_engine()

def load_table(table_name: str) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)

def check_nulls(df: pd.DataFrame, table_name: str):
    print(f"\n--- Null check: {table_name} ---")
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if nulls.empty:
        print("No nulls found.")
    else:
        print(nulls)

def check_duplicates(df: pd.DataFrame, table_name: str, subset=None):
    print(f"\n--- Duplicate check: {table_name} ---")
    dupes = df[df.duplicated(subset=subset, keep=False)]
    print(f"{len(dupes)} duplicate rows found." if not dupes.empty else "No duplicates found.")
    return dupes

def check_orphaned_foreign_keys():
    print("\n--- Orphaned foreign key check ---")
    queries = {
        "matches with missing team1": """
            SELECT match_id FROM matches m
            LEFT JOIN teams t ON m.team1_id = t.team_id
            WHERE t.team_id IS NULL
        """,
        "matches with missing venue": """
            SELECT match_id FROM matches m
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.venue_id IS NOT NULL AND v.venue_id IS NULL
        """,
        "batting rows with missing player": """
            SELECT scorecard_id FROM batting_scorecard b
            LEFT JOIN players p ON b.player_id = p.player_id
            WHERE p.player_id IS NULL
        """,
    }
    with engine.connect() as conn:
        for label, query in queries.items():
            result = conn.execute(text(query)).fetchall()
            print(f"{label}: {len(result)} orphaned rows")

def check_outliers():
    print("\n--- Outlier check ---")
    with engine.connect() as conn:
        # Batting: strike rate above 600 is essentially impossible in real cricket
        result = conn.execute(text("""
            SELECT scorecard_id, match_id, player_id, runs, balls, strike_rate
            FROM batting_scorecard
            WHERE strike_rate > 600 OR (balls = 0 AND runs > 0)
        """)).fetchall()
        print(f"Suspicious batting strike rates: {len(result)}")

        # Bowling: economy above 30 or negative values
        result = conn.execute(text("""
            SELECT scorecard_id, match_id, player_id, overs, runs_conceded, economy
            FROM bowling_scorecard
            WHERE economy > 30 OR economy < 0
        """)).fetchall()
        print(f"Suspicious bowling economy rates: {len(result)}")

def run_all_checks():
    tables = ["teams", "venues", "series", "matches", "players",
              "batting_scorecard", "bowling_scorecard"]

    for t in tables:
        df = load_table(t)
        check_nulls(df, t)

    players_df = load_table("players")
    check_duplicates(players_df, "players", subset=["player_id"])

    check_orphaned_foreign_keys()
    check_outliers()

if __name__ == "__main__":
    run_all_checks()