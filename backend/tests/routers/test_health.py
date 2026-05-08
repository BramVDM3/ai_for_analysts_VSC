from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_running_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Library AI for Analysts backend is running."}


def test_health_endpoint_is_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
