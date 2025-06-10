import re

from fastapi.testclient import TestClient
from tplapi.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "<title>Templates API - Swagger UI</title>" in response.text


def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    content = response.json()
    assert "build_number" in content
    # Check if the build_number looks like a SHA1 hash.
    assert re.match(r"^[a-f0-9]{40}$", content["build_number"])


def test_task():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == []
