from app.database.connection import Database
from app.database.repositories import DeviceRepository, MemoryRepository
from app.schemas.contracts import DeviceDescriptor, DeviceType
from app.security.tokens import issue_token, verify_token, hash_token


def test_token_hash_verification():
    token = issue_token()
    assert verify_token(token, hash_token(token))
    assert not verify_token("wrong", hash_token(token))


def test_device_registration_and_memory(tmp_path):
    db = Database(str(tmp_path / "test.db"))
    db.initialize()
    descriptor = DeviceDescriptor(device_id="test-phone", device_type=DeviceType.ANDROID, display_name="Test Phone")
    token = issue_token()
    DeviceRepository(db).register(descriptor, token)
    assert DeviceRepository(db).list()[0]["device_id"] == "test-phone"
    repo = MemoryRepository(db)
    repo.add("test-phone", "user", "Hola BINGO")
    entries = repo.recent("test-phone")
    assert len(entries) == 1 and entries[0]["content"] == "Hola BINGO"


def test_device_enrollment_and_protected_memory(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient
    from app.core.config import get_settings
    from app.main import create_app

    monkeypatch.setenv("BINGO_DATABASE_PATH", str(tmp_path / "api.db"))
    monkeypatch.setenv("BINGO_ENROLLMENT_SECRET", "test-enrollment-secret")
    monkeypatch.setenv("BINGO_TOKEN_PEPPER", "test-pepper-value")
    get_settings.cache_clear()
    app = create_app()
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/devices/register", json={
                "enrollment_secret": "test-enrollment-secret",
                "device": {"device_id": "test-windows", "device_type": "windows", "display_name": "Test Windows"}
            })
            assert response.status_code == 200
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            saved = client.post("/api/v1/memory", headers=headers, json={"role": "user", "content": "Prueba"})
            assert saved.status_code == 200
            history = client.get("/api/v1/memory", headers=headers)
            assert history.status_code == 200
            assert history.json()["entries"][0]["content"] == "Prueba"
            assert client.get("/api/v1/devices").status_code == 401
    finally:
        get_settings.cache_clear()
