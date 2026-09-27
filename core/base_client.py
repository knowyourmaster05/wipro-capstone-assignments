"""Session-based HTTP client with retry, masking, and response wrapping."""
from __future__ import annotations
import time
from typing import Any
from urllib.parse import urljoin

import requests

from configs import Config
from utils import get_logger

_SENSITIVE = {"password", "token", "authorization", "api_key", "secret"}
_RETRY_STATUS = {429, 500, 502, 503, 504}


class APIResponse:
    """Framework-level wrapper around requests.Response."""

    def __init__(self, response: requests.Response, method: str,
                 request_payload: dict | None, elapsed_ms: float) -> None:
        self._r = response
        self.method = method.upper()
        self.request_payload = request_payload
        self.elapsed_ms = elapsed_ms
        self.status_code = response.status_code
        self.headers = dict(response.headers)
        self.text = response.text
        self.url = response.url
        try:
            self.body: Any = response.json()
        except ValueError:
            self.body = response.text

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 400

    def json(self) -> Any:
        return self.body

    def get(self, key: str, default: Any = None) -> Any:
        node: Any = self.body
        for part in key.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return default
        return node

    def assert_status(self, expected: int | list[int]) -> None:
        exp = [expected] if isinstance(expected, int) else list(expected)
        if self.status_code not in exp:
            raise AssertionError(
                f"Status mismatch\n  Expected: {exp}\n  Actual: {self.status_code}"
                f"\n  URL: {self.url}\n  Body: {self.body}"
            )

    def __repr__(self) -> str:
        return f"<APIResponse {self.method} {self.url} -> {self.status_code} ({self.elapsed_ms:.1f}ms)>"


class BaseClient:
    """Session-based client with retry, masking and logging."""

    def __init__(self, service_name: str, base_url: str | None = None) -> None:
        self.service_name = service_name
        self.base_url = (base_url or Config.get(f"base_urls.{service_name}", "")).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Dibyojyoti-QA-Framework/1.0",
        })
        self._timeouts = Config.get("timeouts", {"connect": 10, "read": 30})
        self._retry_cfg = Config.get("retry", {"max_attempts": 3, "backoff_factor": 0.5})
        self.log = get_logger(f"core.{service_name}")

    @staticmethod
    def _mask(payload: dict | None) -> dict | None:
        if not isinstance(payload, dict):
            return payload
        return {k: ("***" if k.lower() in _SENSITIVE else v) for k, v in payload.items()}

    def _url(self, endpoint: str) -> str:
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> APIResponse:
        url = self._url(endpoint)
        # Only force JSON content-type if we're actually sending JSON.
        # When `data=` is used (form-encoded), let requests set the header.
        if "json" in kwargs and kwargs["json"] is not None:
            kwargs.setdefault("headers", {})
            kwargs["headers"].setdefault("Content-Type", "application/json")
        elif "data" in kwargs and kwargs["data"] is not None:
            self.session.headers.pop("Content-Type", None)
        timeout = (self._timeouts.get("connect", 10), self._timeouts.get("read", 30))
        attempts = int(self._retry_cfg.get("max_attempts", 3))
        backoff = float(self._retry_cfg.get("backoff_factor", 0.5))

        self.log.info("-> %s %s | payload=%s", method.upper(), url,
                      self._mask(kwargs.get("json") or kwargs.get("data")))

        last_exc: Exception | None = None
        for attempt in range(1, attempts + 1):
            start = time.perf_counter()
            try:
                resp = self.session.request(method, url, timeout=timeout, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                wrapped = APIResponse(resp, method, kwargs.get("json") or kwargs.get("data"), elapsed)
                self.log.info("<- %s %s | %s | %.1fms",
                              method.upper(), url, wrapped.status_code, elapsed)
                if wrapped.status_code in _RETRY_STATUS and attempt < attempts:
                    sleep_for = backoff * (2 ** (attempt - 1))
                    self.log.warning("Retrying %s %s (status=%s, attempt %d/%d, sleep=%.1fs)",
                                     method.upper(), url, wrapped.status_code, attempt, attempts, sleep_for)
                    time.sleep(sleep_for)
                    continue
                return wrapped
            except requests.RequestException as exc:
                last_exc = exc
                self.log.warning("Request error on %s %s: %s", method.upper(), url, exc)
                if attempt < attempts:
                    time.sleep(backoff * (2 ** (attempt - 1)))

        raise ConnectionError(f"Request failed after {attempts} attempts: {method} {url}") from last_exc

    def get(self, endpoint: str, **kw: Any) -> APIResponse:
        return self._request("GET", endpoint, **kw)

    def post(self, endpoint: str, **kw: Any) -> APIResponse:
        return self._request("POST", endpoint, **kw)

    def put(self, endpoint: str, **kw: Any) -> APIResponse:
        return self._request("PUT", endpoint, **kw)

    def patch(self, endpoint: str, **kw: Any) -> APIResponse:
        return self._request("PATCH", endpoint, **kw)

    def delete(self, endpoint: str, **kw: Any) -> APIResponse:
        return self._request("DELETE", endpoint, **kw)

    def set_auth(self, handler) -> None:
        handler.attach(self.session)

    def clear_auth(self) -> None:
        self.session.headers.pop("Authorization", None)
        self.session.cookies.clear()

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


if __name__ == "__main__":
    client = BaseClient(service_name="jsonplaceholder")
    resp = client.get("/users/1")
    print(resp)
    resp.assert_status(200)
    print("Body keys:", list(resp.body.keys()))
    client.close()

