"""Environment-aware YAML configuration loader."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()

_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _ROOT / "configs"


class Config:
    """Static accessor for the active environment's YAML config."""

    _data: dict[str, Any] | None = None

    @classmethod
    def _load(cls) -> dict[str, Any]:
        env = os.getenv("ENV", "dev").lower()
        path = _CONFIG_DIR / f"{env}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            cls._data = yaml.safe_load(f) or {}
        return cls._data

    @classmethod
    def all(cls) -> dict[str, Any]:
        if cls._data is None:
            cls._load()
        return cls._data or {}

    @classmethod
    def get(cls, key_path: str, default: Any = None) -> Any:
        node: Any = cls.all()
        for part in key_path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    @classmethod
    def reload(cls) -> dict[str, Any]:
        cls._data = None
        return cls._load()
