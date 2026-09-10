import os
from dotenv import load_dotenv

load_dotenv()

CRICBUZZ_API_KEY = os.getenv("CRICBUZZ_API_KEY")
CRICBUZZ_API_HOST = os.getenv("CRICBUZZ_API_HOST")
print("DEBUG - API_KEY:", CRICBUZZ_API_KEY)
print("DEBUG - API_HOST:", CRICBUZZ_API_HOST)
DB_TYPE = os.getenv("DB_TYPE", "mysql")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "cricbuzz_livestats")