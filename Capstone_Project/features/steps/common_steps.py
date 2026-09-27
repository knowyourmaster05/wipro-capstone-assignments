"""Cross-domain step definitions shared by all feature files."""
from __future__ import annotations

from behave import given, then

from core import ResponseValidator
from utils import SchemaLoader


@given('the "{service}" API client is ready')
def step_client_ready(context, service: str) -> None:
    from features.environment import _get_or_create_client
    _get_or_create_client(context, service)


@then("the response status code should be {status:d}")
def step_status_code(context, status: int) -> None:
    ResponseValidator.status_code(context.response, status)


@then("the response body code should be {code:d}")
def step_body_code(context, code: int) -> None:
    """Assert the business-level responseCode inside the JSON body."""
    actual = context.response.get("responseCode")
    if actual != code:
        raise AssertionError(
            f"Body responseCode mismatch\n"
            f"  Expected : {code}\n  Actual   : {actual}\n"
            f"  URL      : {context.response.url}\n"
            f"  Body     : {context.response.body}"
        )


@then('the response body should contain "{text}"')
def step_body_contains(context, text: str) -> None:
    ResponseValidator.contains_text(context.response, text)


@then('the response body should conform to the "{schema_name}" schema')
def step_schema_validation(context, schema_name: str) -> None:
    schema = SchemaLoader.get(schema_name)
    ResponseValidator.json_schema(context.response, schema)


@then("the response body should contain at least {min_count:d} product(s)")
def step_min_products(context, min_count: int) -> None:
    body = context.response.body or {}
    products = body.get("products") if isinstance(body, dict) else None
    count = len(products) if products else 0
    if count < min_count:
        raise AssertionError(
            f"Expected at least {min_count} products, found {count}"
            f"\n  URL : {context.response.url}"
            f"\n  Body: {context.response.body}"
        )
