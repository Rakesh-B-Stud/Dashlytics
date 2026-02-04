import sqlite3
from datetime import datetime

DB = "history.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS history(
        dataset TEXT,
        model TEXT,
        accuracy REAL,
        time TEXT
    )
    """)
    conn.commit()
    conn.close()


def insert_record(dataset, model, acc):
    conn = sqlite3.connect(DB)

    conn.execute(
        "INSERT INTO history VALUES (?,?,?,?)",
        (dataset, model, float(acc),
         datetime.now().strftime("%d-%m-%Y %H:%M"))
    )

    conn.commit()
    conn.close()


def fetch_all():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT * FROM history ORDER BY rowid DESC").fetchall()
    conn.close()
    return rows
