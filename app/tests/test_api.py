from http import client
from fastapi.testclient import TestClient

from app.backend.api import app


client = TestClient(app)

def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == 200
