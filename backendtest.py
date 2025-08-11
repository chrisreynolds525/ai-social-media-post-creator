from fastapi.testclient import TestClient
from backend import app

client = TestClient(app)

def test_generate_fallback():
    response = client.post("/api/generate", json={
        "topic": "Test topic",
        "platform": "twitter",
        "tone": "engaging",
        "count": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert len(data["posts"]) == 2
    for post in data["posts"]:
        assert "text" in post and "hashtags" in post
