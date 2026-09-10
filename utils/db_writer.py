from utils.db_connection import get_engine
from sqlalchemy import text

engine = get_engine()

def insert_team(team_id: int, team_name: str, team_s_name: str):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO teams (team_id, team_name, team_s_name)
            VALUES (:team_id, :team_name, :team_s_name)
            ON DUPLICATE KEY UPDATE
                team_name = VALUES(team_name),
                team_s_name = VALUES(team_s_name)
        """), {"team_id": team_id, "team_name": team_name, "team_s_name": team_s_name})
        conn.commit()

def insert_venue(venue_id: int, ground: str, city: str, timezone: str, latitude: float, longitude: float):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO venues (venue_id, ground, city, timezone, latitude, longitude)
            VALUES (:venue_id, :ground, :city, :timezone, :latitude, :longitude)
            ON DUPLICATE KEY UPDATE
                ground = VALUES(ground),
                city = VALUES(city)
        """), {
            "venue_id": venue_id, "ground": ground, "city": city,
            "timezone": timezone, "latitude": latitude, "longitude": longitude
        })
        conn.commit()
def insert_series(series_id: int, series_name: str, start_date, end_date):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO series (series_id, series_name, start_date, end_date)
            VALUES (:series_id, :series_name, :start_date, :end_date)
            ON DUPLICATE KEY UPDATE series_name = VALUES(series_name)
        """), {
            "series_id": series_id, "series_name": series_name,
            "start_date": start_date, "end_date": end_date
        })
        conn.commit()

def insert_match(match_id, series_id, match_desc, match_format,
                  team1_id, team2_id, venue_id, start_date, end_date, status, result):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO matches
                (match_id, series_id, match_desc, match_format, team1_id, team2_id,
                 venue_id, start_date, end_date, status, result)
            VALUES
                (:match_id, :series_id, :match_desc, :match_format, :team1_id, :team2_id,
                 :venue_id, :start_date, :end_date, :status, :result)
            ON DUPLICATE KEY UPDATE
                status = VALUES(status), result = VALUES(result)
        """), {
            "match_id": match_id, "series_id": series_id, "match_desc": match_desc,
            "match_format": match_format, "team1_id": team1_id, "team2_id": team2_id,
            "venue_id": venue_id, "start_date": start_date, "end_date": end_date,
            "status": status, "result": result
        })
        conn.commit()
def insert_player(player_id: int, player_name: str):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO players (player_id, player_name)
            VALUES (:player_id, :player_name)
            ON DUPLICATE KEY UPDATE player_name = VALUES(player_name)
        """), {"player_id": player_id, "player_name": player_name})
        conn.commit()

def insert_batting_scorecard(match_id, innings_id, player_id, team_id,
                              runs, balls, fours, sixes, strike_rate, dismissal_type):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO batting_scorecard
                (match_id, innings_id, player_id, team_id, runs, balls, fours, sixes,
                 strike_rate, dismissal_type)
            VALUES
                (:match_id, :innings_id, :player_id, :team_id, :runs, :balls, :fours, :sixes,
                 :strike_rate, :dismissal_type)
        """), {
            "match_id": match_id, "innings_id": innings_id, "player_id": player_id,
            "team_id": team_id, "runs": runs, "balls": balls, "fours": fours,
            "sixes": sixes, "strike_rate": strike_rate, "dismissal_type": dismissal_type
        })
        conn.commit()

def insert_bowling_scorecard(match_id, innings_id, player_id, team_id,
                              overs, maidens, runs_conceded, wickets, economy):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO bowling_scorecard
                (match_id, innings_id, player_id, team_id, overs, maidens,
                 runs_conceded, wickets, economy)
            VALUES
                (:match_id, :innings_id, :player_id, :team_id, :overs, :maidens,
                 :runs_conceded, :wickets, :economy)
        """), {
            "match_id": match_id, "innings_id": innings_id, "player_id": player_id,
            "team_id": team_id, "overs": overs, "maidens": maidens,
            "runs_conceded": runs_conceded, "wickets": wickets, "economy": economy
        })
        conn.commit()