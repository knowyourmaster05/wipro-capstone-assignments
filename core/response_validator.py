"""Reusable response assertion helpers."""
from __future__ import annotations
from typing import Any

from jsonschema import validate as _validate
from jsonschema import ValidationError as _ValidationError

from core.base_client import APIResponse


def _fail(expected: Any, actual: Any, resp: APIResponse, label: str = "") -> None:
    raise AssertionError(
        f"{label}\n  Expected : {expected}\n  Actual   : {actual}"
        f"\n  URL      : {resp.url}\n  Body     : {resp.body}"
    )


class ResponseValidator:

    @staticmethod
    def status_code(response: APIResponse, expected: int | list[int]) -> None:
        exp = [expected] if isinstance(expected, int) else list(expected)
        if response.status_code not in exp:
            _fail(exp, response.status_code, response, "Status code mismatch")

    @staticmethod
    def json_schema(response: APIResponse, schema: dict) -> None:
        try:
            _validate(instance=response.body, schema=schema)
        except _ValidationError as exc:
            raise AssertionError(
                f"Schema validation failed: {exc.message}\n  Path: {list(exc.path)}"
                f"\n  URL : {response.url}\n  Body: {response.body}"
            ) from exc

    @staticmethod
    def key_present(response: APIResponse, key: str) -> None:
        sentinel = object()
        if response.get(key, sentinel) is sentinel:
            _fail(f"key '{key}' present", "missing", response, "Key missing")

    @staticmethod
    def key_equals(response: APIResponse, key: str, expected: Any) -> None:
        actual = response.get(key)
        if actual != expected:
            _fail(expected, actual, response, f"Value mismatch for '{key}'")

    @staticmethod
    def key_type(response: APIResponse, key: str, expected_type: type) -> None:
        actual = response.get(key)
        if not isinstance(actual, expected_type):
            _fail(expected_type.__name__, type(actual).__name__, response, f"Type mismatch for '{key}'")

    @staticmethod
    def response_time_under(response: APIResponse, max_ms: float) -> None:
        if response.elapsed_ms > max_ms:
            _fail(f"< {max_ms}ms", f"{response.elapsed_ms:.1f}ms", response, "Response too slow")

    @staticmethod
    def header_present(response: APIResponse, header: str) -> None:
        if header.lower() not in {k.lower() for k in response.headers}:
            _fail(f"header '{header}'", "missing", response, "Header missing")

    @staticmethod
    def contains_text(response: APIResponse, text: str) -> None:
        haystack = response.text or str(response.body)
        if text not in haystack:
            _fail(f"contains '{text}'", haystack[:200], response, "Substring not found")
