from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_content_type_is_json() -> None:
    response = client.get("/health")

    assert response.headers["content-type"].startswith("application/json")
