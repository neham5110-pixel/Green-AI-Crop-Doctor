
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_frontend_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "Green AI Crop Doctor" in response.text
