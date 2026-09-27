"""Product catalog service (AutomationExercise)."""
from __future__ import annotations
from core.base_client import BaseClient, APIResponse
from services._endpoints import AEEndpoints
from utils import get_logger


class ProductService:
    """Read + search + negative paths on the AE catalog endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client
        self.log = get_logger("services.product")

    def get_all_products(self) -> APIResponse:
        return self.client.get(AEEndpoints.PRODUCTS_LIST)

    def get_all_brands(self) -> APIResponse:
        return self.client.get(AEEndpoints.BRANDS_LIST)

    def search_product(self, term: str) -> APIResponse:
        self.log.info("Searching products for '%s'", term)
        return self.client.post(
            AEEndpoints.SEARCH_PRODUCT,
            data={"search_product": term},
        )

    def search_product_without_param(self) -> APIResponse:
        self.log.warning("Negative: searchProduct without required param")
        return self.client.post(AEEndpoints.SEARCH_PRODUCT, data={})

    def attempt_post_to_products(self) -> APIResponse:
        return self.client.post(AEEndpoints.PRODUCTS_LIST, data={})

    def attempt_put_to_brands(self) -> APIResponse:
        return self.client.put(AEEndpoints.BRANDS_LIST, data={})
