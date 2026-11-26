import sqlite3
from contextlib import closing

from websockets import connection


class DatabaseManager:
    def __init__(self, db_path: str = "emails.db"):
        self.db_path = db_path

    def create_tables(self):
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
        # Existing SQL code here
                connection.execute("""
                CREATE TABLE IF NOT EXISTS email_results (
                    id INTEGER PRIMARY KEY,
                    sender TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    reason TEXT NOT NULL
                )
            """)

    def save_result(self, result: dict):
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.execute("""
                    INSERT INTO email_results
                        (id, sender, subject, category, priority, reason)
                    VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    sender = excluded.sender,
                    subject = excluded.subject,
                    category = excluded.category,
                    priority = excluded.priority,
                    reason = excluded.reason
            """, (
                result["id"],
                result["sender"],
                result["subject"],
                result["category"],
                result["priority"],
                result["reason"]
            ))

    def get_all_results(self) -> list[dict]:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(
                    "SELECT * FROM email_results ORDER BY id"
                ).fetchall()

        return [dict(row) for row in rows]