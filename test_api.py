from api.cricbuzz_client import get_recent_matches
import json

data = get_recent_matches()
print(json.dumps(data, indent=2)[:1000])