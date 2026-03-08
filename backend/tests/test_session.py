from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_next_session():

    response = client.get("/session/next")

    assert response.status_code == 200
