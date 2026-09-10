from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from utils.config import DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_engine():
    if DB_TYPE == "mysql":
        password = quote_plus(DB_PASSWORD)
        conn_str = f"mysql+mysqlconnector://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        conn_str = f"sqlite:///{DB_NAME}.db"
    return create_engine(conn_str)

def test_connection():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB connection OK:", result.fetchone())