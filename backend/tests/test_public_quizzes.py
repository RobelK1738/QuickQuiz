from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_public_quizzes_initially_empty(client):
    resp = client.get("/api/quizzes")
    assert resp.status_code == 200
    assert resp.json() == []

