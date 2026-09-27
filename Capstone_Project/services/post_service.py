"""Post service (JSONPlaceholder) — CRUD + contract practice."""
from __future__ import annotations
from core.base_client import BaseClient, APIResponse
from services._endpoints import JPEndpoints
from utils import get_logger


class PostService:
    """CRUD on JSONPlaceholder /posts for contract + negative testing."""

    def __init__(self, client: BaseClient) -> None:
        self.client = client
        self.log = get_logger("services.post")

    def get_all_posts(self) -> APIResponse:
        return self.client.get(JPEndpoints.POSTS)

    def get_post(self, post_id: int) -> APIResponse:
        return self.client.get(f"{JPEndpoints.POSTS}/{post_id}")

    def create_post(self, payload: dict) -> APIResponse:
        return self.client.post(JPEndpoints.POSTS, json=payload)

    def update_post_put(self, post_id: int, payload: dict) -> APIResponse:
        return self.client.put(f"{JPEndpoints.POSTS}/{post_id}", json=payload)

    def update_post_patch(self, post_id: int, payload: dict) -> APIResponse:
        return self.client.patch(f"{JPEndpoints.POSTS}/{post_id}", json=payload)

    def delete_post(self, post_id: int) -> APIResponse:
        return self.client.delete(f"{JPEndpoints.POSTS}/{post_id}")

    def get_comments_for_post(self, post_id: int) -> APIResponse:
        return self.client.get(f"{JPEndpoints.POSTS}/{post_id}/comments")
