from utils.db_connection import get_engine
from sqlalchemy import text

engine = get_engine()

def backfill_winners():
    with engine.connect() as conn:
        # Pull all matches with team names
        rows = conn.execute(text("""
            SELECT m.match_id, m.result, m.team1_id, t1.team_name AS team1_name,
                   m.team2_id, t2.team_name AS team2_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
        """)).fetchall()

        updated = 0
        unmatched = 0

        for row in rows:
            result_text = (row.result or "").lower()
            winner_id = None

            if row.team1_name.lower() in result_text and "won" in result_text:
                winner_id = row.team1_id
            elif row.team2_name.lower() in result_text and "won" in result_text:
                winner_id = row.team2_id

            if winner_id:
                conn.execute(text("""
                    UPDATE matches SET winner_team_id = :winner_id WHERE match_id = :match_id
                """), {"winner_id": winner_id, "match_id": row.match_id})
                updated += 1
            else:
                unmatched += 1  # draw, abandoned, no-result, or unrecognized phrasing

        conn.commit()
        print(f"Updated: {updated} matches")
        print(f"Unmatched (draw/abandoned/no result): {unmatched} matches")

if __name__ == "__main__":
    backfill_winners()