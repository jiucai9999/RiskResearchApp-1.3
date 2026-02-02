import sqlite3
import os

APP_NAME = "RiskResearchApp"

def get_db_path():
    base = os.path.join(os.path.expanduser("~"), "AppData", "Local", APP_NAME)
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "trades.db")

def get_conn():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        product TEXT,
        symbol TEXT,
        account REAL,
        risk_percent REAL,
        entry REAL,
        stop REAL,
        target REAL,
        position REAL,
        rr REAL,
        result REAL,
        reason TEXT,
        emotion TEXT,
        institution_prices TEXT,
        inst_avg REAL,
        inst_median REAL,
        inst_max REAL,
        inst_min REAL
    )
    """)
    conn.commit()
    conn.close()
