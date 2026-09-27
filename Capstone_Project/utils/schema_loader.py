"""Cached JSON schema loader."""
from __future__ import annotations
from pathlib import Path
from typing import Any

from utils.data_reader import DataReader

_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA_DIR = _ROOT / "schemas"

NAME_MAP: dict[str, str] = {
    "user": "user_schema.json",
    "product": "product_schema.json",
    "error": "error_schema.json",
    "login_response": "login_response_schema.json",
    "jp_post": "jsonplaceholder_post_schema.json",
}


class SchemaLoader:
    """Loads and caches JSON schemas by logical name."""

    _cache: dict[str, dict] = {}

    @classmethod
    def get(cls, name: str) -> dict[str, Any]:
        if name in cls._cache:
            return cls._cache[name]
        filename = NAME_MAP.get(name, f"{name}_schema.json")
        path = _SCHEMA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")
        schema = DataReader.read_json(path)
        cls._cache[name] = schema
        return schema

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()
