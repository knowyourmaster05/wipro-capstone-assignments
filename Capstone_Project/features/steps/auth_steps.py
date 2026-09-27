"""Step definitions for authentication.feature."""
from __future__ import annotations

from behave import when

from core import BaseClient
from services import AuthService
from services._endpoints import AEEndpoints
from utils import get_logger

logger = get_logger("steps.auth")


def _auth_service(context) -> AuthService:
    return AuthService(context.client["automation_exercise"])


_INVALID_PAYLOADS = {
    "missing email": {"password": "Test@1234"},
    "missing pass":  {"email": "someone@example.com"},
    "invalid email": {"email": "not-an-email", "password": "Test@1234"},
    "wrong creds":   {"email": "ghost@nowhere.com", "password": "WrongPass1!"},
}


@when('I attempt to verify login with the "{case}" payload')
def step_verify_login_invalid(context, case: str) -> None:
    payload = _INVALID_PAYLOADS[case]
    context.response = _auth_service(context).verify_login(
        email=payload.get("email", ""),
        password=payload.get("password", ""),
    )
    logger.warning("Negative login case '%s' -> responseCode=%s",
                   case, context.response.get("responseCode"))


@when("I verify login using the last created user's credentials")
def step_verify_login_valid(context) -> None:
    assert context.last_user is not None, "No user has been created yet"
    context.response = _auth_service(context).login_with_valid_credentials(
        email=context.last_user["email"],
        password=context.last_user["password"],
    )


@when("I send a DELETE request to the verify login endpoint")
def step_delete_verify_login(context) -> None:
    client: BaseClient = context.client["automation_exercise"]
    context.response = client.delete(AEEndpoints.VERIFY_LOGIN)

