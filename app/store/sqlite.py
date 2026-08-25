import sqlite3
from datetime import datetime

from .base import Store, Link, CodeCollision


class SqliteStore(Store):

    def __init__(self, settings):
        self.db_url = settings.db_url
        self.connection = sqlite3.connect(self.db_url)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0
            )
        """)

        self.connection.commit()

    async def put(self, link: Link) -> None:
        try:
            self.connection.execute(
                """
                INSERT INTO links (code, target_url, created_at, clicks)
                VALUES (?, ?, ?, ?)
                """,
                (
                    link.code,
                    link.target_url,
                    link.created_at.isoformat(),
                    link.clicks
                )
            )
            self.connection.commit()

        except sqlite3.IntegrityError:
            raise CodeCollision()

    async def get(self, code: str) -> Link | None:
        cursor = self.connection.execute(
            """
            SELECT code, target_url, created_at, clicks
            FROM links
            WHERE code = ?
            """,
            (code,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Link(
            code=row[0],
            target_url=row[1],
            created_at=datetime.fromisoformat(row[2]),
            clicks=row[3]
        )

    async def increment_clicks(self, code: str) -> None:
        self.connection.execute(
            """
            UPDATE links
            SET clicks = clicks + 1
            WHERE code = ?
            """,
            (code,)
        )

        self.connection.commit()

    async def health(self) -> bool:
        try:
            self.connection.execute("SELECT 1")
            return True
        except sqlite3.Error:
            return False