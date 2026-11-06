from fastapi.testclient import TestClient
from app.main import create_app


def test_health():
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_module_list():
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/modules")
    assert response.status_code == 200
    assert "system_info" in response.json()["modules"]
