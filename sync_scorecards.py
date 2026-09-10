from api.cricbuzz_client import get_match_scorecard
from utils.db_writer import insert_player, insert_batting_scorecard, insert_bowling_scorecard
from utils.db_connection import get_engine
from sqlalchemy import text
import time


def get_synced_match_ids(limit=5):
    """Pull a small batch of match_ids already in your matches table, to test first."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT match_id, team1_id, team2_id FROM matches LIMIT :limit"),
                               {"limit": limit})
        return result.fetchall()


def sync_match_scorecard(match_id, team1_id, team2_id):
    data = get_match_scorecard(match_id)
    if "scorecard" not in data:
        print(f"No scorecard for match {match_id}, skipping.")
        return

    engine = get_engine()

    for innings in data["scorecard"]:
        innings_id = innings.get("inningsid")
        bat_team_name = innings.get("batteamname", "").strip().lower()

        # Look up the correct team_id by matching batteamname against teams table
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT team_id FROM teams
                WHERE LOWER(team_name) = :name OR LOWER(team_s_name) = :name
                LIMIT 1
            """), {"name": bat_team_name})
            row = result.fetchone()
            batting_team_id = row[0] if row else team1_id  # fallback if no match found

        # Bowling team is whichever of team1/team2 is NOT the batting team
        if batting_team_id == team1_id:
            bowling_team_id = team2_id
        elif batting_team_id == team2_id:
            bowling_team_id = team1_id
        else:
            bowling_team_id = team2_id  # fallback

        for batsman in innings.get("batsman", []):
            insert_player(batsman["id"], batsman["name"])
            insert_batting_scorecard(
                match_id=match_id,
                innings_id=innings_id,
                player_id=batsman["id"],
                team_id=batting_team_id,
                runs=batsman.get("runs", 0),
                balls=batsman.get("balls", 0),
                fours=batsman.get("fours", 0),
                sixes=batsman.get("sixes", 0),
                strike_rate=float(batsman.get("strkrate", 0) or 0),
                dismissal_type=batsman.get("outdec", "")
            )

        for bowler in innings.get("bowler", []):
            insert_player(bowler["id"], bowler["name"])
            insert_bowling_scorecard(
                match_id=match_id,
                innings_id=innings_id,
                player_id=bowler["id"],
                team_id=bowling_team_id,
                overs=float(bowler.get("overs", 0) or 0),
                maidens=bowler.get("maidens", 0),
                runs_conceded=bowler.get("runs", 0),
                wickets=bowler.get("wickets", 0),
                economy=float(bowler.get("economy", 0) or 0)
            )

    print(f"Synced scorecard for match {match_id}")


def sync():
    matches = get_synced_match_ids(limit=83)  # start small, only 5 matches
    for match_id, team1_id, team2_id in matches:
        try:
            sync_match_scorecard(match_id, team1_id, team2_id)
        except Exception as e:
            print(f"Failed match {match_id}: {e}")
        time.sleep(1)  # be gentle on the free-tier rate limit


if __name__ == "__main__":
    sync()