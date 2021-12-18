import json
import pytest
from fastapi.testclient import TestClient
from src.main import app
import os

client = TestClient(app)


test_request_data = json.load(open("tests/identify/data.json", "r"))
test_model_data = json.load(open("tests/models/data.json", "r"))
TEST_COLLECTION="testcollection"

@pytest.mark.parametrize("target_request", test_request_data)
def test_model_inference(target_request):
    response = client.post(
        "/local/models/default/inference", json=target_request)
    assert response.status_code == 200


def test_bad_create():
    response = client.post(
        "/local/models/default/create", json=test_model_data)
    assert response.status_code == 422


def test_good_create():
    response = client.post(
        f"/local/models/{TEST_COLLECTION}/create", json=test_model_data)
    os.remove(f"src/data/static/{TEST_COLLECTION}/models.json")
    os.rmdir(f"src/data/static/{TEST_COLLECTION}")
    assert response.status_code == 200

