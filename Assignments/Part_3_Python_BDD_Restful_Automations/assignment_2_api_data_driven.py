import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

# Data-driven test cases
test_data = [
    {"title": "foo",  "body": "bar",  "userId": 1},
    {"title": "test", "body": "data", "userId": 2},
    {"title": "abc",  "body": "xyz",  "userId": 3},
]


@pytest.mark.parametrize("payload", test_data)
def test_create_post_api(payload):
    # POST request with JSON payload
    response = requests.post(BASE_URL, json=payload)

    # Validate status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Validate response content (echoed back from server)
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

    print(f"PASS: created post id={data['id']} title='{data['title']}'")