"""Uniform reader for YAML / JSON / CSV test data."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parent.parent


def _resolve(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else _ROOT / p


class DataReader:
    """Reads test data and returns Python-native structures."""

    @staticmethod
    def read_yaml(path: str | Path) -> Any:
        p = _resolve(path)
        if not p.exists():
            raise FileNotFoundError(f"YAML not found: {p}")
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ValueError(f"YAML is empty: {p}")
        return data

    @staticmethod
    def read_json(path: str | Path) -> Any:
        p = _resolve(path)
        if not p.exists():
            raise FileNotFoundError(f"JSON not found: {p}")
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if data is None:
            raise ValueError(f"JSON is empty: {p}")
        return data

    @staticmethod
    def read_csv(path: str | Path) -> list[dict]:
        p = _resolve(path)
        if not p.exists():
            raise FileNotFoundError(f"CSV not found: {p}")
        with p.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            raise ValueError(f"CSV is empty: {p}")
        return rows

    @staticmethod
    def read_yaml_as_params(path: str | Path, key: str) -> list[tuple]:
        """Return list-of-tuples for Behave Scenario Outline substitution."""
        data = DataReader.read_yaml(path)
        records = data.get(key)
        if not records:
            raise ValueError(f"Key '{key}' missing or empty in {path}")
        return [tuple(rec.values()) for rec in records]

    @staticmethod
    def read_csv_as_params(path: str | Path) -> list[tuple]:
        rows = DataReader.read_csv(path)
        return [tuple(row.values()) for row in rows]
