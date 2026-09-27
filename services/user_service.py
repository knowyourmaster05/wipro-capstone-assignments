"""User Management service (AutomationExercise)."""
from __future__ import annotations
from core.base_client import BaseClient, APIResponse
from services._endpoints import AEEndpoints
from utils import get_logger


class UserService:
    """Form-encoded user operations — AE does not accept JSON."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client
        self.log = get_logger("services.user")

    def create_user(self, payload: dict) -> APIResponse:
        self.log.info("create_user email=%s", payload.get("email"))
        return self.client.post(AEEndpoints.CREATE_ACCOUNT, data=payload)

    def delete_user(self, email: str, password: str) -> APIResponse:
        self.log.info("delete_user email=%s", email)
        return self.client.delete(AEEndpoints.DELETE_ACCOUNT,
                                  data={"email": email, "password": password})

    def update_user(self, payload: dict) -> APIResponse:
        self.log.info("update_user email=%s", payload.get("email"))
        return self.client.put(AEEndpoints.UPDATE_ACCOUNT, data=payload)

    def get_user_by_email(self, email: str) -> APIResponse:
        self.log.info("get_user_by_email email=%s", email)
        return self.client.get(AEEndpoints.GET_USER_BY_EMAIL, params={"email": email})
