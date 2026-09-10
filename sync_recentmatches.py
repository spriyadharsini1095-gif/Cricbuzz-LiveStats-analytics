from api.cricbuzz_client import get_recent_matches
from utils.db_writer import insert_team, insert_venue

def sync():
    data = get_recent_matches()
    for type_match in data.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            wrapper = series_match.get("seriesAdWrapper", {})
            for match in wrapper.get("matches", []):
                info = match["matchInfo"]

                # Insert team1 and team2
                for team_key in ("team1", "team2"):
                    team = info[team_key]
                    insert_team(team["teamId"], team["teamName"], team.get("teamSName", ""))

                # Insert venue
                venue = info.get("venueInfo")
                if venue:
                    insert_venue(
                        venue["id"], venue["ground"], venue.get("city", ""),
                        venue.get("timezone", ""),
                        float(venue.get("latitude", 0)), float(venue.get("longitude", 0))
                    )
                print(f"Synced match {info['matchId']}: {info.get('matchDesc', '')}")

if __name__ == "__main__":
    sync()
    from api.cricbuzz_client import get_recent_matches
from utils.db_writer import insert_team, insert_venue, insert_series, insert_match
from datetime import datetime

def epoch_to_date(ms):
    """Convert API epoch-milliseconds string to a Python datetime."""
    if not ms:
        return None
    return datetime.fromtimestamp(int(ms) / 1000)

def sync():
    data = get_recent_matches()
    for type_match in data.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            wrapper = series_match.get("seriesAdWrapper", {})
            series_id = wrapper.get("seriesId")
            series_name = wrapper.get("seriesName")

            for match in wrapper.get("matches", []):
                info = match["matchInfo"]

                for team_key in ("team1", "team2"):
                    team = info[team_key]
                    insert_team(team["teamId"], team["teamName"], team.get("teamSName", ""))

                venue = info.get("venueInfo")
                if venue:
                    insert_venue(
                        venue["id"], venue["ground"], venue.get("city", ""),
                        venue.get("timezone", ""),
                        float(venue.get("latitude", 0)), float(venue.get("longitude", 0))
                    )

                if series_id:
                    insert_series(series_id, series_name, None, None)

                insert_match(
                    match_id=info["matchId"],
                    series_id=series_id,
                    match_desc=info.get("matchDesc", ""),
                    match_format=info.get("matchFormat", ""),
                    team1_id=info["team1"]["teamId"],
                    team2_id=info["team2"]["teamId"],
                    venue_id=venue["id"] if venue else None,
                    start_date=epoch_to_date(info.get("startDate")),
                    end_date=epoch_to_date(info.get("endDate")),
                    status=info.get("state", ""),
                    result=info.get("status", "")
                )

                print(f"Synced match {info['matchId']}: {info.get('matchDesc', '')}")

if __name__ == "__main__":
    sync()