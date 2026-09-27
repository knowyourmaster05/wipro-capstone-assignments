"""High-level CRUD helpers on top of DBConnector for user_management."""
from __future__ import annotations

from utils.db_connector import DBConnector
from utils.logger import get_logger

logger = get_logger("utils.dbrepo")


COLUMNS = [
    "name", "email", "password", "title",
    "birth_date", "birth_month", "birth_year",
    "firstname", "lastname", "company",
    "address1", "address2", "country", "zipcode",
    "state", "city", "mobile_number",
]


class UserRepository:
    """Mirrors API user state into MySQL for cross-verification."""

    def insert_user(self, payload: dict, api_response_id: str | None = None) -> None:
        with DBConnector() as db:
            placeholders = ", ".join(["%s"] * (len(COLUMNS) + 1))
            cols = ", ".join(COLUMNS + ["api_response_id"])
            values = tuple(payload.get(c, "") for c in COLUMNS) + (api_response_id or "",)
            sql = f"INSERT INTO user_management ({cols}) VALUES ({placeholders})"
            sql += " ON DUPLICATE KEY UPDATE name=VALUES(name), company=VALUES(company)"
            db.execute(sql, values)
            logger.info("DB insert/update: %s", payload.get("email"))

    def update_user(self, payload: dict) -> None:
        with DBConnector() as db:
            assignments = ", ".join(f"{c}=%s" for c in COLUMNS if c != "email")
            values = tuple(payload.get(c, "") for c in COLUMNS if c != "email")
            sql = f"UPDATE user_management SET {assignments} WHERE email=%s"
            db.execute(sql, values + (payload.get("email"),))
            logger.info("DB updated: %s", payload.get("email"))

    def delete_user(self, email: str) -> None:
        with DBConnector() as db:
            db.execute("DELETE FROM user_management WHERE email=%s", (email,))
            logger.info("DB deleted: %s", email)

    def exists(self, email: str) -> bool:
        with DBConnector() as db:
            row = db.fetch_one("SELECT id FROM user_management WHERE email=%s", (email,))
            return row is not None

    def get_by_email(self, email: str) -> dict | None:
        with DBConnector() as db:
            return db.fetch_one("SELECT * FROM user_management WHERE email=%s", (email,))

