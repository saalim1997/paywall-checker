import sqlite3
from datetime import datetime

DB_NAME = "/data/links.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY,
            url TEXT,
            date_saved TEXT,
            paywall_status TEXT,
            last_checked TEXT,
            user_email TEXT
        )
        """)


def add_link(url, user_email):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """INSERT INTO links (
            url, date_saved, paywall_status, last_checked, user_email
            )
            VALUES (?, ?, ?, ?, ?)""",
            (url, datetime.now().isoformat(), "paywalled", None, user_email),
        )


def get_links(user_email, status=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        if status:
            cursor.execute(
                """SELECT id, url, date_saved, paywall_status
                FROM links
                WHERE paywall_status=? AND user_email=?""",
                (status, user_email),
            )
        else:
            cursor.execute(
                """SELECT id, url, date_saved, paywall_status
                FROM links
                WHERE user_email=?""",
                (user_email,),
            )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "url": row[1],
                "date_saved": row[2],
                "paywall_status": row[3],
            }
            for row in rows
        ]


def update_status(link_id, status):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE links SET paywall_status=?, last_checked=? WHERE id=?",
            (status, datetime.now().isoformat(), link_id),
        )
