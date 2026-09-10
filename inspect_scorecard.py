from api.cricbuzz_client import get_match_scorecard
import json

# Pick any real match_id you saw in your synced matches table
match_id = 170397  

data = get_match_scorecard(match_id)
print(json.dumps(data, indent=2)[:3000])
from api.cricbuzz_client import get_match_scorecard
import json

match_id = 170397
data = get_match_scorecard(match_id)

# 1. See the top-level structure
print("TOP LEVEL KEYS:", list(data.keys()))
print()

# 2. Look at the first scorecard entry's structure (usually a list of innings)
if "scorecard" in data:
    first_innings = data["scorecard"][0]
    print("INNINGS KEYS:", list(first_innings.keys()))
    print()
    print(json.dumps(first_innings, indent=2)[:2500])
    from api.cricbuzz_client import get_match_scorecard
import json

match_id = 170397
data = get_match_scorecard(match_id)

first_innings = data["scorecard"][0]

print("BOWLER SAMPLE:")
print(json.dumps(first_innings["bowler"][0], indent=2))