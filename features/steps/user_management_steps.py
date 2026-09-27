"""Step definitions for user_management.feature."""
from __future__ import annotations

from behave import given, when, then

from core import ResponseValidator
from services import UserService
from utils import PayloadFactory, UserRepository, get_logger

logger = get_logger("steps.user_mgmt")
_repo = UserRepository()


def _user_service(context) -> UserService:
    return UserService(context.client["automation_exercise"])


@given("I have created a user with a randomly generated payload")
@when("I create a user with a randomly generated payload")
def step_create_user(context) -> None:
    payload = PayloadFactory.create_user_payload()
    context.last_user = payload
    context.deleted_users.append(payload["email"])
    resp = _user_service(context).create_user(payload)
    context.response = resp
    logger.info("Created user: %s -> responseCode=%s",
                payload["email"], resp.get("responseCode"))
    if resp.get("responseCode") == 201:
        _repo.insert_user(payload, api_response_id=str(resp.get("responseCode")))


@when("I request user details for the last created user's email")
def step_get_user(context) -> None:
    assert context.last_user is not None, "No user has been created yet"
    context.response = _user_service(context).get_user_by_email(context.last_user["email"])


@when("I update the last created user's company to \"{company}\"")
def step_update_user(context, company: str) -> None:
    assert context.last_user is not None, "No user has been created yet"
    payload = PayloadFactory.update_user_payload(context.last_user, company=company)
    context.last_user = payload
    context.response = _user_service(context).update_user(payload)
    if context.response.get("responseCode") == 200:
        _repo.update_user(payload)


@when("I delete the last created user")
def step_delete_user(context) -> None:
    assert context.last_user is not None, "No user has been created yet"
    context.response = _user_service(context).delete_user(
        email=context.last_user["email"],
        password=context.last_user["password"],
    )
    if context.last_user["email"] in context.deleted_users:
        context.deleted_users.remove(context.last_user["email"])
    if context.response.get("responseCode") == 200:
        _repo.delete_user(context.last_user["email"])


@then("the response should contain the last created user's email")
def step_response_contains_email(context) -> None:
    assert context.last_user is not None
    ResponseValidator.contains_text(context.response, context.last_user["email"])


@then("the last created user should exist in the database")
def step_user_in_db(context) -> None:
    assert context.last_user is not None
    email = context.last_user["email"]
    assert _repo.exists(email), f"User {email} not found in DB"
    logger.info("DB verified: %s", email)


@then("the last created user should NOT exist in the database")
def step_user_not_in_db(context) -> None:
    assert context.last_user is not None
    email = context.last_user["email"]
    assert not _repo.exists(email), f"User {email} still present in DB"

