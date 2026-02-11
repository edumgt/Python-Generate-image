from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_stack() -> None:
    response = client.get("/api/stack")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 5
    assert all("name" in item and "category" in item for item in payload)


def test_files() -> None:
    response = client.get("/api/files")
    assert response.status_code == 200
    payload = response.json()
    assert "python_files" in payload
    assert "cpu.py" in payload["python_files"]
