"""Pluggable authentication handlers for the HTTP client."""
from __future__ import annotations
from abc import ABC, abstractmethod

import requests


class AuthHandler(ABC):
    """Strategy interface for attaching authentication to a session."""

    @abstractmethod
    def attach(self, session: requests.Session) -> None: ...


class NoAuth(AuthHandler):
    """Default — no authentication."""

    def attach(self, session: requests.Session) -> None:
        return None


class BasicAuth(AuthHandler):
    def __init__(self, username: str, password: str) -> None:
        self._auth = requests.auth.HTTPBasicAuth(username, password)

    def attach(self, session: requests.Session) -> None:
        session.auth = self._auth


class BearerTokenAuth(AuthHandler):
    def __init__(self, token: str) -> None:
        self._token = token

    def attach(self, session: requests.Session) -> None:
        session.headers["Authorization"] = f"Bearer {self._token}"


class ApiKeyAuth(AuthHandler):
    def __init__(self, key_name: str, key_value: str, location: str = "header") -> None:
        self._name = key_name
        self._value = key_value
        self._location = location

    def attach(self, session: requests.Session) -> None:
        if self._location == "header":
            session.headers[self._name] = self._value

    def query_params(self) -> dict:
        return {self._name: self._value} if self._location == "query" else {}


class SessionCookieAuth(AuthHandler):
    def __init__(self, cookies: dict) -> None:
        self._cookies = cookies

    def attach(self, session: requests.Session) -> None:
        session.cookies.update(self._cookies)
