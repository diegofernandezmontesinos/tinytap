from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_streak():

    response = client.post("/streak/test_user")

    assert response.status_code == 200
