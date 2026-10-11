import sqlite3
from typing import List, Optional

from src.config.settings import settings


class RequestRepository:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DB_PATH

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create(self, request: Request) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """INSERT INTO Requests
                   (number, title, description, author_id, category_id,
                    status_id, priority_id, assignee_id, plan_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (request.number, request.title, request.description,
                 request.author_id, request.category_id, request.status_id,
                 request.priority_id, request.assignee_id, request.plan_date)
            )
            conn.commit()
            return cursor.lastrowid

    def get_by_id(self, request_id: int) -> Optional[Request]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM Requests WHERE id = ?", (request_id,)
            ).fetchone()
            return Request(**dict(row)) if row else None

    def get_all(self) -> List[Request]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM Requests ORDER BY created_at DESC"
            ).fetchall()
            return [Request(**dict(row)) for row in rows]

    def update(self, request: Request) -> None:
        with self._connect() as conn:
            conn.execute(
                """UPDATE Requests SET title = ?, description = ?,
                   status_id = ?, assignee_id = ?
                   WHERE id = ?""",
                (request.title, request.description, request.status_id,
                 request.assignee_id, request.id)
            )
            conn.commit()

    def delete(self, request_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM Requests WHERE id = ?", (request_id,))
            conn.commit()