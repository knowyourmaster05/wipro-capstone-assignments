"""MySQL connection wrapper (mysql-connector-python)."""
from __future__ import annotations
from typing import Any

from utils.config_loader import Config
from utils.logger import get_logger

logger = get_logger("utils.db")


class DBConnector:
    """Lazy MySQL connector with dict cursors and context-manager support."""

    def __init__(self) -> None:
        self._cnx = None
        self._cursor = None
        self._cfg = {
            "host": Config.get("database.host", "localhost"),
            "port": Config.get("database.port", 3306),
            "user": Config.get("database.user", "root"),
            "password": Config.get("database.password", ""),
            "database": Config.get("database.name", "api_automation_db"),
        }

    def connect(self) -> "DBConnector":
        import mysql.connector
        self._cnx = mysql.connector.connect(**self._cfg)
        self._cursor = self._cnx.cursor(dictionary=True)
        logger.debug("Connected to MySQL: %s", self._cfg["database"])
        return self

    def close(self) -> None:
        try:
            if self._cursor:
                self._cursor.close()
            if self._cnx and self._cnx.is_connected():
                self._cnx.close()
        except Exception as exc:
            logger.warning("DB close error: %s", exc)
        finally:
            self._cursor = None
            self._cnx = None

    def _ensure(self) -> None:
        if self._cnx is None:
            self.connect()

    def execute(self, query: str, params: tuple | None = None) -> int:
        self._ensure()
        assert self._cursor is not None
        self._cursor.execute(query, params or ())
        verb = query.strip().split()[0].upper()
        if verb in {"INSERT", "UPDATE", "DELETE", "REPLACE"}:
            self._cnx.commit()
        return self._cursor.rowcount

    def fetch_one(self, query: str, params: tuple | None = None) -> dict | None:
        self._ensure()
        assert self._cursor is not None
        self._cursor.execute(query, params or ())
        return self._cursor.fetchone()

    def fetch_all(self, query: str, params: tuple | None = None) -> list[dict]:
        self._ensure()
        assert self._cursor is not None
        self._cursor.execute(query, params or ())
        return list(self._cursor.fetchall())

    def table_exists(self, name: str) -> bool:
        row = self.fetch_one(
            "SELECT COUNT(*) AS c FROM information_schema.tables "
            "WHERE table_schema = %s AND table_name = %s",
            (self._cfg["database"], name),
        )
        return bool(row and row["c"] > 0)

    def __enter__(self) -> "DBConnector":
        return self.connect()

    def __exit__(self, *exc: Any) -> None:
        self.close()
