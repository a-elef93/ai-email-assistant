import sqlite3


class DatabaseManager:
    def __init__(self, db_path: str = "emails.db"):
        self.db_path = db_path

    def create_tables(self):
        with sqlite3.connect(self.db_path) as connection:
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
        with sqlite3.connect(self.db_path) as connection:
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
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                "SELECT * FROM email_results ORDER BY id"
            ).fetchall()

        return [dict(row) for row in rows]