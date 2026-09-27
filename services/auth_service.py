"""Authentication service — verifyLogin + JSONPlaceholder user profile."""
from __future__ import annotations
from core.base_client import BaseClient, APIResponse
from services._endpoints import AEEndpoints, JPEndpoints
from utils import get_logger


class AuthService:
    """Framework-level authentication checks."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client
        self.log = get_logger("services.auth")

    def verify_login(self, email: str, password: str) -> APIResponse:
        return self.client.post(
            AEEndpoints.VERIFY_LOGIN,
            data={"email": email, "password": password},
        )

    def login_with_valid_credentials(self, email: str, password: str) -> APIResponse:
        resp = self.verify_login(email, password)
        self.log.info("Login verified for %s -> %s", email, resp.status_code)
        return resp

    def login_without_email(self, password: str) -> APIResponse:
        self.log.warning("Negative login: missing email")
        return self.client.post(AEEndpoints.VERIFY_LOGIN, data={"password": password})

    def login_with_invalid_credentials(self, email: str, password: str) -> APIResponse:
        self.log.warning("Negative login: invalid credentials for %s", email)
        return self.verify_login(email, password)

    def fetch_user_profile(self, user_id: int) -> APIResponse:
        return self.client.get(f"{JPEndpoints.USERS}/{user_id}")
