import re

import pytest
from fastapi.testclient import TestClient
from tplapi.main import app
from tplapi.models.models import get_tasks_db


# --- Pytest Fixture to provide a clean TestClient for each test ---
@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI app.
    It overrides the 'get_tasks_db' dependency to ensure a clean, empty tasks_db
    for every test function.
    """

    # 1. Define the test-specific version of the dependency.
    # This function will be called instead of the original get_tasks_db().
    def override_get_tasks_db():
        # Crucial: Return a NEW, EMPTY dictionary for each test
        return {}

    # 2. Apply the override to the FastAPI app's dependency_overrides.
    # This tells FastAPI: "For the duration of this test, when someone depends on
    # 'get_tasks_db', call 'override_get_tasks_db' instead."
    app.dependency_overrides[get_tasks_db] = override_get_tasks_db

    # 3. Yield the TestClient.
    # The test function will receive this client.
    yield TestClient(app)

    # 4. Clean up the override after the test is done.
    # This is important! It ensures that the original dependency logic is restored
    # for any subsequent tests or if the app is run normally afterwards.
    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "<title>Templates API - Swagger UI</title>" in response.text


def test_info(client):
    response = client.get("/info")
    assert response.status_code == 200
    content = response.json()
    assert "build_number" in content
    # Check if the build_number looks like a SHA1 hash.
    assert re.match(r"^[a-f0-9]{40}$", content["build_number"])


def test_task(client):
    response = client.get("/task")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == []
