"""Faker-based payload factories for idempotent test data."""
from __future__ import annotations
from uuid import uuid4

from faker import Faker

_fake = Faker()


def _unique_email() -> str:
    return f"{uuid4().hex[:8]}.{_fake.email()}"


class PayloadFactory:
    """Generates realistic, unique payloads per call."""

    @staticmethod
    def create_user_payload(overrides: dict | None = None) -> dict:
        payload = {
            "name": _fake.name(),
            "email": _unique_email(),
            "password": f"Aa1!{uuid4().hex[:6]}",
            "title": _fake.random_element(elements=("Mr", "Mrs")),
            "birth_date": f"{_fake.random_int(1, 28):02d}",
            "birth_month": _fake.month_name(),
            "birth_year": str(_fake.random_int(1970, 2005)),
            "firstname": _fake.first_name(),
            "lastname": _fake.last_name(),
            "company": _fake.company(),
            "address1": _fake.street_address(),
            "address2": _fake.secondary_address(),
            "country": "India",
            "zipcode": _fake.postcode(),
            "state": _fake.state(),
            "city": _fake.city(),
            "mobile_number": "".join(str(_fake.random_digit()) for _ in range(10)),
        }
        if overrides:
            payload.update(overrides)
        return payload

    @staticmethod
    def login_payload(email: str, password: str) -> dict:
        return {"email": email, "password": password}

    @staticmethod
    def update_user_payload(base: dict, **overrides) -> dict:
        merged = dict(base)
        merged.update(overrides)
        return merged

    @staticmethod
    def search_product_payload(term: str) -> dict:
        return {"search_product": term}

    @staticmethod
    def jsonplaceholder_post_payload(user_id: int | None = None) -> dict:
        return {
            "userId": user_id or _fake.random_int(1, 10),
            "title": _fake.sentence(nb_words=6),
            "body": _fake.paragraph(nb_sentences=3),
        }

    @staticmethod
    def jsonplaceholder_comment_payload(post_id: int | None = None) -> dict:
        return {
            "postId": post_id or _fake.random_int(1, 100),
            "name": _fake.sentence(nb_words=4),
            "email": _fake.email(),
            "body": _fake.paragraph(nb_sentences=2),
        }

    @staticmethod
    def negative_login_variants() -> list[dict]:
        return [
            {"scenario": "missing email", "payload": {"password": "Test@1234"},
             "expected_status": 400, "expected_message": "Bad request"},
            {"scenario": "missing pass", "payload": {"email": "a@b.com"},
             "expected_status": 400, "expected_message": "Bad request"},
            {"scenario": "invalid email", "payload": {"email": "not-an-email", "password": "Test@1234"},
             "expected_status": 400, "expected_message": "Bad request"},
            {"scenario": "wrong creds", "payload": {"email": "ghost@nowhere.com", "password": "WrongPass1!"},
             "expected_status": 404, "expected_message": "User not found"},
        ]
