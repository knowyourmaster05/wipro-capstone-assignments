"""Step definitions for product_catalog.feature."""
from __future__ import annotations

from behave import when

from services import ProductService
from utils import get_logger

logger = get_logger("steps.product")


def _product_service(context) -> ProductService:
    return ProductService(context.client["automation_exercise"])


@when("I fetch all products")
def step_fetch_products(context) -> None:
    context.response = _product_service(context).get_all_products()


@when("I fetch all brands")
def step_fetch_brands(context) -> None:
    context.response = _product_service(context).get_all_brands()


@when('I search for products with term "{term}"')
def step_search_products(context, term: str) -> None:
    context.response = _product_service(context).search_product(term)


@when("I search for products without the required parameter")
def step_search_no_param(context) -> None:
    context.response = _product_service(context).search_product_without_param()


@when("I send a POST request to the products list endpoint")
def step_post_products(context) -> None:
    context.response = _product_service(context).attempt_post_to_products()


@when("I send a PUT request to the brands list endpoint")
def step_put_brands(context) -> None:
    context.response = _product_service(context).attempt_put_to_brands()

